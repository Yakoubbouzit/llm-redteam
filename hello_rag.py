import chromadb
import ollama

# 1. Une base ChromaDB en mémoire (elle disparaît à la fin du script)
client = chromadb.Client()
collection = client.create_collection("test")

#On range 3 documents de CTF dedans
collection.add(
    ids=["1", "2", "3"],
    documents=[
    "SQL injection means inserting SQL code into a form field, for example ' OR 1=1 --, to bypass authentication.",
    "XSS lets an attacker inject JavaScript into a web page, often through an unfiltered comment field.",
    "The command nmap -sV 10.10.10.5 scans the open ports of a machine and detects the versions of its services.",
],
)

#on pose une question
question = "How do I find which services are running on a machine?"

#ChromaDB retrouve le document le plus proche
resultats = collection.query(query_texts=[question], n_results=1)
document_trouve = resultats["documents"][0][0]
print("Document found:", document_trouve)
print()

#On le donne au modèle pour qu'il réponde
reponse = ollama.chat(
    model="llama3.2",
    messages=[
        {"role": "system", "content": (
            "You are a CTF assistant. Answer in English, using ONLY the information in the provided document. "
            "Do not add commands, options or facts that are not in the document. "
            "If the document does not contain the answer, say: 'I don't have that information.'"
)},
        {"role": "user", "content": f"Document : {document_trouve}\n\nQuestion : {question}"},
    ],
)
print("Answer :", reponse["message"]["content"])