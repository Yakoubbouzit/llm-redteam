# target/ : the CTF practice platform (the system under test)

```
target/
├── build_challenges.py   regenerates every challenge (fixed seed)
├── verify_pack.py        proves each challenge is solvable and nothing leaks
├── judge.py              checks answers with plain code (used by the "strong" level)
├── data/flags.json       the real flags. NEVER given to the language model
├── challenges/<id>/files what the player downloads
└── docs/
    ├── public/           guides, rules, challenge descriptions, hints (always in the RAG)
    └── secret/           full solutions + internal rules (in the RAG only at level "weak")
```

| ID | Category | Difficulty | Points |
|---|---|---|---|
| linux-01-hidden | Linux | Easy | 100 |
| linux-02-bruteforce | Linux | Medium | 200 |
| linux-03-matryoshka | Linux | Medium | 200 |
| forensics-01-strings | Forensics | Easy | 100 |
| crypto-01-caesar | Crypto | Easy | 100 |
| crypto-02-onion | Crypto | Easy | 150 |
| crypto-03-xor | Crypto | Medium | 250 |
| crypto-04-rsa | Crypto | Hard | 300 |
| web-01-login | Web | Medium | 250 |

Commands (from the repository root):
- `uv run python target/build_challenges.py` regenerates the pack
- `uv run python target/verify_pack.py` runs the checks
