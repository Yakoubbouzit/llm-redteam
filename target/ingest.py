from rag import build_index, LEVEL

collection = build_index(LEVEL)
print(f"Level '{LEVEL}': {collection.count()} chunks indexed")