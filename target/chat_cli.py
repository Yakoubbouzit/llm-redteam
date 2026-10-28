from rag import answer, LEVEL
from judge import check_answer

print(f"CTF assistant (level: {LEVEL}).")
print("Ask questions in English. Submit with: /submit <challenge-id> <answer>. Type 'quit' to exit.")
while True:
    question = input("\nYou: ").strip()
    if question.lower() in {"quit", "exit"}:
        break
    if not question:
        continue
    if question.startswith("/submit"):
        parts = question.split(maxsplit=2)
        if len(parts) < 3:
            print("Usage: /submit <challenge-id> <answer>")
            continue
        result = check_answer(parts[1], parts[2])
        print(f"\nPlatform: {result['message']}")
        if result.get("flag"):
            print(f"Flag: {result['flag']}")
        continue
    text, sources = answer(question)
    print(f"\nAssistant: {text}\n\n[sources: {', '.join(sources) or 'none'}]")