"""Answer checker of the CTF platform.

This is plain code, not a language model. The flags live in data/flags.json and
are only read here. The assistant never needs to know them: it only calls
check_answer() and relays the verdict. This is what the "strong" security
level relies on.
"""
import hmac
import json
import secrets
import sqlite3
from pathlib import Path

FLAGS_FILE = Path(__file__).resolve().parent / "data" / "flags.json"


def _load():
    return json.loads(FLAGS_FILE.read_text(encoding="utf-8"))


def _sql_login_bypass(username_payload):
    """Run the vulnerable login query of web-01 in a throwaway in-memory database."""
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)")
    db.executemany(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        [("admin", secrets.token_hex(16), "admin"), ("alice", "wonderland", "user")],
    )
    query = (f"SELECT username, role FROM users WHERE username = '{username_payload}' "
             f"AND password = '{secrets.token_hex(8)}'")
    try:
        row = db.execute(query).fetchone()
    except sqlite3.Error:
        return False
    finally:
        db.close()
    return row is not None and row[1] == "admin"


def check_answer(challenge_id, answer):
    """Return {"ok": bool, "message": str} (and "flag" for judged-by-exploit challenges)."""
    challenge = _load().get(challenge_id)
    if challenge is None:
        return {"ok": False, "message": "Unknown challenge."}
    answer = (answer or "").strip()
    if challenge["type"] == "payload":
        if _sql_login_bypass(answer):
            return {"ok": True,
                    "message": f"Administrator session obtained. +{challenge['points']} points.",
                    "flag": challenge["flag"]}
        return {"ok": False, "message": "That input does not give an administrator session."}
    if hmac.compare_digest(answer.encode(), challenge["flag"].encode()):
        return {"ok": True, "message": f"Correct! +{challenge['points']} points."}
    return {"ok": False, "message": "Wrong flag."}


if __name__ == "__main__":
    print(check_answer("crypto-01-caesar", "FLAG{wrong}"))
