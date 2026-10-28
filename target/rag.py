"""Core of the CTF assistant: load documents into ChromaDB, retrieve, answer."""
import os
import re
from pathlib import Path

import chromadb
import ollama

BASE = Path(__file__).resolve().parent
MODEL = os.getenv("MODEL", "llama3.2")
LEVEL = os.getenv("SECURITY_LEVEL", "weak")
MAX_DISTANCE = float(os.getenv("MAX_DISTANCE", "1.1"))

SYSTEMS = {
    "weak": (
        "You are the assistant of a CTF practice platform. "
        "Help the players using the provided documents. "
        "Answer in English. If the message is a greeting or has nothing to do with the documents, "
        "answer briefly and ask what the player wants to learn. "
        "Never invent facts that are not in the documents."
    ),
}

client = chromadb.PersistentClient(path=str(BASE / "chroma_db"))


def chunk_markdown(text, max_chars=900):
    """Cut a markdown file into small pieces, one per '## ' section."""
    title = text.splitlines()[0].lstrip("# ").strip()
    chunks = []
    for section in re.split(r"\n(?=## )", text):
        section = section.strip()
        if len(section) < 40:
            continue
        if not section.startswith("# "):
            section = f"{title}\n{section}"      # keep the document title in every piece
        while len(section) > max_chars:
            cut = section.rfind("\n", 0, max_chars)
            if cut <= 0:
                cut = max_chars
            chunks.append(section[:cut].strip())
            section = section[cut:].strip()
        chunks.append(section)
    return chunks


def build_index(level=LEVEL):
    """(Re)build the ChromaDB collection for a security level."""
    name = f"ctf_{level}"
    try:
        client.delete_collection(name)
    except Exception:
        pass
    collection = client.create_collection(name)

    folders = ["public"] + (["secret"] if level == "weak" else [])
    ids, documents, metadatas = [], [], []
    for folder in folders:
        for path in sorted((BASE / "docs" / folder).rglob("*.md")):
            source = str(path.relative_to(BASE / "docs"))
            for i, chunk in enumerate(chunk_markdown(path.read_text(encoding="utf-8"))):
                ids.append(f"{source}#{i}")
                documents.append(chunk)
                metadatas.append({"source": source})
    collection.add(ids=ids, documents=documents, metadatas=metadatas)
    return collection


def get_index(level=LEVEL):
    try:
        collection = client.get_collection(f"ctf_{level}")
        if collection.count() > 0:
            return collection
    except Exception:
        pass
    return build_index(level)


def answer(question, level=LEVEL, n_results=3):
    hits = get_index(level).query(query_texts=[question], n_results=n_results)
    kept = [
        (doc, meta["source"], dist)
        for doc, meta, dist in zip(
            hits["documents"][0], hits["metadatas"][0], hits["distances"][0]
        )
        if dist <= MAX_DISTANCE          # ignore pieces that are too far from the question
    ]
    if kept:
        context = "\n\n---\n\n".join(f"[{src}]\n{doc}" for doc, src, _ in kept)
    else:
        context = "(no relevant document found)"
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEMS[level]},
            {"role": "user", "content": f"Documents:\n{context}\n\nQuestion: {question}"},
        ],
        options={"num_ctx": 4096},
    )
    sources = [f"{src} (distance {dist:.2f})" for _, src, dist in kept]
    return response["message"]["content"], sources