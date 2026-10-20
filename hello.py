import ollama

reponse = ollama.chat(
    model="llama3.2",
    messages=[{"role": "user", "content": "Explique c'est quoi un Rag"}],
)
print(reponse["message"]["content"])
