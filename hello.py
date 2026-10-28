import ollama

reponse = ollama.chat(
    model="llama3.2",
    messages=[{"role": "user", "content": "Explique ce qu'est un RAG en deux phrases."}],
)
print(reponse["message"]["content"])

# pour verifier si python parle bien à Llama