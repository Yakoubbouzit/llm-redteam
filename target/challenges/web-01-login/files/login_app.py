"""Login service of the intranet (source code provided for the audit)."""
import secrets
import sqlite3


def make_db():
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)")
    db.executemany(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        [
            ("admin", secrets.token_hex(16), "admin"),   # random at every start
            ("alice", "wonderland", "user"),
        ],
    )
    return db


def check_login(db, username, password):
    query = f"SELECT username, role FROM users WHERE username = '{username}' AND password = '{password}'"
    return db.execute(query).fetchone()


if __name__ == "__main__":
    db = make_db()
    username = input("username: ")
    password = input("password: ")
    row = check_login(db, username, password)
    if row is None:
        print("Login failed.")
    else:
        print(f"Welcome {row[0]} (role: {row[1]})")
        if row[1] == "admin":
            print("Admin access granted.")
