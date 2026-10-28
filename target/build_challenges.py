#!/usr/bin/env python3
"""Generate the CTF challenge pack.

For every challenge it writes:
  challenges/<id>/files/...            files given to the player
  docs/public/challenges/<id>_*.md     description and hints (always in the RAG)
  docs/secret/<id>_solution.md         full walkthrough (only in the RAG at level "weak")
  data/flags.json                      flags used by judge.py (never in the RAG)

Run it again at any time: the seed is fixed, so the output is identical.
"""
import base64
import bz2
import codecs
import datetime as dt
import gzip
import io
import json
import random
import tarfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FILES = ROOT / "challenges"
PUB = ROOT / "docs" / "public" / "challenges"
SEC = ROOT / "docs" / "secret"
DATA = ROOT / "data"

rng = random.Random(1337)
REGISTRY = {}


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, bytes):
        path.write_bytes(content)
    else:
        path.write_text(content, encoding="utf-8")


def fill(text, **values):
    """Replace @NAME@ markers (avoids clashes with shell and Python braces)."""
    for key, value in values.items():
        text = text.replace(f"@{key}@", str(value))
    return text


def register(cid, title, category, difficulty, points, kind, flag,
             description, files_note, hints, solution):
    REGISTRY[cid] = {"flag": flag, "points": points, "type": kind}
    header = (
        f"# {title}\n\n"
        f"- Challenge ID: {cid}\n"
        f"- Category: {category}\n"
        f"- Difficulty: {difficulty}\n"
        f"- Points: {points}\n\n"
    )
    write(PUB / f"{cid}_description.md",
          header + description.strip() + "\n\n## Files\n\n" + files_note.strip() + "\n")
    hints_md = f"# Hints for: {title} ({cid})\n\n" + "\n\n".join(
        f"## Hint {i}\n\n{h.strip()}" for i, h in enumerate(hints, 1)) + "\n"
    write(PUB / f"{cid}_hints.md", hints_md)
    write(SEC / f"{cid}_solution.md",
          f"# SOLUTION - CONFIDENTIAL - {title} ({cid})\n\n"
          f"Flag: {flag}\n\n" + solution.strip() + "\n")


# --------------------------------------------------------------------------
# LINUX 01 - hidden files
# --------------------------------------------------------------------------
def build_linux_01():
    cid = "linux-01-hidden"
    flag = "FLAG{dotfiles_hide_in_plain_sight}"
    home = FILES / cid / "files" / "home" / "student"
    tree = {
        "Documents/todo.txt": "- finish the networking lab\n- email the professor about the exam date\n- back up the laptop (ask IT where the old notes went)\n",
        "Documents/lab_report_draft.txt": "Lab 3: Subnetting\n\nWe calculated the network and broadcast addresses for three subnets.\nTODO: add the diagram and the conclusion.\n",
        "Documents/shopping_list.txt": "coffee\nnotebooks\nUSB cable\n",
        "Downloads/readme.txt": "Downloaded from the course portal. Nothing interesting here.\n",
        "Downloads/slides_week2.txt": "Week 2: TCP/IP model, ports and protocols.\n",
        "Pictures/vacation_notes.txt": "Photos are on the external drive.\n",
        "Music/playlist.txt": "lofi beats\nsynthwave\nclassical\n",
        ".bash_history": "ls\ncd Documents\ncat todo.txt\nls -la\ncd ~/.config\nls -a\nexit\n",
        ".cache/thumbs.db": "binary thumbnail cache (not a real database)\n",
        ".config/settings.ini": "[ui]\ntheme=dark\nfont=monospace\n",
        ".config/.archive/.old_notes.txt": "Old notes, moved here so nobody finds them.\nProject vault code (do not share): " + flag + "\n",
    }
    for rel, content in tree.items():
        write(home / rel, content)

    register(
        cid, "Hidden in Plain Sight", "Linux", "Easy", 100, "flag", flag,
        """
A student's laptop was handed to the IT desk. The student swears that the project vault code is somewhere in the home directory, but nobody can find it with a normal file listing.

Explore the home directory and recover the vault code.

Flag format: FLAG{...}
""",
        "`files/home/student/`: a copy of the student's home directory.",
        [
            "In Linux, a file or directory whose name starts with a dot is hidden from the default `ls` output. Think about how to display everything.",
            "Use `ls -la` in each directory, or `find . -type f -name \".*\"` to list every hidden file at once. Shell history files sometimes show where a user was looking.",
            "Start in the home directory and look at `.bash_history`. It points to a configuration directory. List it with `ls -a`, then follow the hidden directory inside. As a shortcut, `grep -r \"FLAG{\" .` searches every file below the current directory.",
        ],
        fill("""
## Walkthrough
1. Go to the files: `cd challenges/linux-01-hidden/files/home/student`
2. `ls` shows only Documents, Downloads, Music and Pictures. Use `ls -la` to see hidden entries: `.bash_history`, `.cache`, `.config`.
3. `cat .bash_history` shows the student went to `~/.config` and ran `ls -a`.
4. `ls -la .config` reveals a hidden directory `.archive`; `ls -la .config/.archive` reveals `.old_notes.txt`.
5. `cat .config/.archive/.old_notes.txt` prints the flag.

Shortcuts: `find . -type f -name ".*"` or `grep -r "FLAG{" .`

Flag: @FLAG@
""", FLAG=flag),
    )


# --------------------------------------------------------------------------
# LINUX 02 - brute force in auth.log
# --------------------------------------------------------------------------
def build_linux_02():
    cid = "linux-02-bruteforce"
    attacker = "203.0.113.77"
    victim = "deploy"
    failures = 612
    flag = f"FLAG{{{attacker}_{victim}_{failures}}}"

    users = ["alice", "bob", "carol", "dave", "deploy"]
    internal = [f"10.0.0.{i}" for i in range(10, 40)] + [f"192.168.1.{i}" for i in range(20, 60)]
    events = []
    seq = [0]

    def stamp(t):
        return f"{t:%b} {t.day:>2} {t:%H:%M:%S}"

    def add(t, message):
        seq[0] += 1
        events.append((t, seq[0], f"{stamp(t)} srv01 {message}"))

    def pid():
        return rng.randint(1000, 60000)

    def port():
        return rng.randint(30000, 65000)

    base = dt.datetime(2026, 10, 13, 0, 0, 0)

    # Normal activity from the internal network over two days.
    for _ in range(900):
        t = base + dt.timedelta(seconds=rng.randint(0, 2 * 86400 - 1))
        user, ip, p, prt = rng.choice(users), rng.choice(internal), pid(), port()
        if rng.random() < 0.08:
            add(t, f"sshd[{p}]: Failed password for {user} from {ip} port {prt} ssh2")
            t += dt.timedelta(seconds=rng.randint(3, 15))
        method = rng.choice(["publickey", "password", "publickey"])
        add(t, f"sshd[{p}]: Accepted {method} for {user} from {ip} port {prt} ssh2")
        add(t, f"sshd[{p}]: pam_unix(sshd:session): session opened for user {user}(uid=1001) by (uid=0)")
        t_end = t + dt.timedelta(minutes=rng.randint(1, 240))
        add(t_end, f"sshd[{p}]: pam_unix(sshd:session): session closed for user {user}")

    def brute(ip, count, start, names):
        t = start
        for _ in range(count):
            t += dt.timedelta(seconds=rng.randint(1, 9))
            name, p, prt = rng.choice(names), pid(), port()
            if name in users or name == "root":
                add(t, f"sshd[{p}]: Failed password for {name} from {ip} port {prt} ssh2")
            else:
                add(t, f"sshd[{p}]: Invalid user {name} from {ip} port {prt}")
                add(t, f"sshd[{p}]: Failed password for invalid user {name} from {ip} port {prt} ssh2")
        return t

    names = ["root", "admin", "test", "ubuntu", "oracle", "deploy", "postgres", "git", "user", "pi"]
    t_end = brute(attacker, failures, dt.datetime(2026, 10, 14, 2, 10, 0), names)
    p, prt = pid(), port()
    t_ok = t_end + dt.timedelta(seconds=7)
    add(t_ok, f"sshd[{p}]: Accepted password for {victim} from {attacker} port {prt} ssh2")
    add(t_ok, f"sshd[{p}]: pam_unix(sshd:session): session opened for user {victim}(uid=1001) by (uid=0)")
    # Noisy decoys that never get in.
    brute("198.51.100.23", 187, dt.datetime(2026, 10, 13, 16, 30, 0), names)
    brute("192.0.2.88", 54, dt.datetime(2026, 10, 14, 9, 5, 0), names[:5])

    events.sort(key=lambda e: (e[0], e[1]))
    write(FILES / cid / "files" / "auth.log", "\n".join(e[2] for e in events) + "\n")

    register(
        cid, "Brute Force Hunter", "Linux", "Medium", 200, "flag", flag,
        """
The server `srv01` raised an alert: someone seems to have guessed their way into an account over SSH. You received a copy of its authentication log.

Find the address that launched the brute-force attack, the account it finally got into, and how many failed password attempts it made before succeeding. Count only lines containing "Failed password" that come from that address.

Flag format: FLAG{<attacker_ip>_<compromised_user>_<number_of_failed_password_lines>}
Example of the shape: FLAG{192.0.2.1_bob_42}
""",
        "`files/auth.log`: the SSH authentication log (a few thousand lines, two days of activity).",
        [
            "Brute force means many failures from one source. You need to count failures per source address, then check whether that source also has a successful login.",
            "Use `grep \"Failed password\"` to keep failures, `awk` to extract the address, then `sort | uniq -c | sort -rn | head` to rank the sources. Several addresses attack the server, but only one of them gets in.",
            "The address is the third field from the end of a Failed password line, so `awk '{print $(NF-3)}'` works for every line. Take the top address, run `grep Accepted auth.log | grep <address>` to find the compromised account, and count its failures with `grep -c`.",
        ],
        fill("""
## Walkthrough
1. Rank failures per source address:
   `grep "Failed password" auth.log | awk '{print $(NF-3)}' | sort | uniq -c | sort -rn | head`
   The top three are @IP@ (@N@ failures), 198.51.100.23 (187) and 192.0.2.88 (54). Internal addresses have only a handful of failures each.
2. Check which of them logged in successfully:
   `grep "Accepted" auth.log | grep "@IP@"`
   Result: `Accepted password for @USER@ from @IP@`. The other two noisy addresses never succeeded.
3. Count the failures of the attacker:
   `grep "Failed password" auth.log | grep -c "from @IP@ "`
   Result: @N@.
4. Build the flag: FLAG{@IP@_@USER@_@N@}

Why the others are decoys: they brute-force too, but there is no Accepted line from them.
""", IP=attacker, USER=victim, N=failures),
    )


# --------------------------------------------------------------------------
# LINUX 03 - nested archives
# --------------------------------------------------------------------------
def build_linux_03():
    cid = "linux-03-matryoshka"
    flag = "FLAG{nested_archives_need_the_file_command}"
    layer1 = gzip.compress((flag + "\n").encode(), mtime=0)
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w") as tf:
        info = tarfile.TarInfo("inner")
        info.size = len(layer1)
        info.mtime = 0
        tf.addfile(info, io.BytesIO(layer1))
    layer3 = bz2.compress(buf.getvalue())
    zbuf = io.BytesIO()
    with zipfile.ZipFile(zbuf, "w") as zf:
        zf.writestr(zipfile.ZipInfo("payload", date_time=(2026, 10, 1, 0, 0, 0)), layer3)
    write(FILES / cid / "files" / "package.dat", zbuf.getvalue())

    register(
        cid, "Matryoshka", "Linux", "Medium", 200, "flag", flag,
        """
A colleague sent you a single file called `package.dat` and said: "the access code is inside, I packed it several times to keep it safe". There are no file extensions to help you, and every layer has a generic name.

Unpack everything and recover the code.

Flag format: FLAG{...}
""",
        "`files/package.dat`: a file wrapped in several layers of different formats.",
        [
            "File extensions can be missing or wrong. A Linux command can tell you the real type of any file from its content.",
            "Run `file` on the current file, extract it with the matching tool (unzip, tar, a decompressor), then run `file` again on the result. The formats change at every layer.",
            "Expect four layers made of different formats. Archive tools that decompress by suffix need a correct name, so rename the file or stream it through the tool (for example `bzip2 -dc < name > out`). Keep going until `file` says ASCII text.",
        ],
        """
## Walkthrough
Work in an empty directory and always run `file` before extracting.
1. `file package.dat` -> Zip archive data. `unzip package.dat` extracts a file named `payload`.
2. `file payload` -> bzip2 compressed data. `bzip2 -dc < payload > layer3` (or rename to payload.bz2 and run `bunzip2 payload.bz2`).
3. `file layer3` -> POSIX tar archive. `tar -xf layer3` extracts a file named `inner`.
4. `file inner` -> gzip compressed data. `gzip -dc < inner` prints the flag (or rename to inner.gz and run `gunzip inner.gz; cat inner`).

Layer order from the outside: zip, bzip2, tar, gzip, plain text.
""",
    )


# --------------------------------------------------------------------------
# FORENSICS 01 - strings in a binary
# --------------------------------------------------------------------------
def build_forensics_01():
    cid = "forensics-01-strings"
    flag = "FLAG{strings_reveals_hidden_text}"
    header = b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00"
    noise_a = bytes(rng.randrange(256) for _ in range(6000))
    noise_b = bytes(rng.randrange(256) for _ in range(9000))
    meta = (b"\x00Software: PhotoEdit 2.1\x00Author: intern_042\x00"
            b"Comment: " + flag.encode() + b"\x00Camera: generic phone\x00")
    write(FILES / cid / "files" / "holiday_photo.jpg", header + noise_a + meta + noise_b + b"\xff\xd9")

    register(
        cid, "Strings Attached", "Forensics", "Easy", 100, "flag", flag,
        """
An intern sent a holiday photo to the whole company, but the file will not open properly and the security team suspects someone left a note inside it.

Inspect the file and recover the hidden text.

Flag format: FLAG{...}
""",
        "`files/holiday_photo.jpg`: a file that claims to be a JPEG image.",
        [
            "Binary files are not only bytes: programs and image editors often leave readable text inside them.",
            "A command called `strings` prints the readable sequences found in any file. A minimum length like `-n 8` removes most noise.",
            "Pipe the output into grep to filter it: `strings -n 8 holiday_photo.jpg | grep -i comment`. You can also look at the first bytes with `xxd` to confirm the file type.",
        ],
        fill("""
## Walkthrough
1. `file holiday_photo.jpg` reports JPEG data, but the image is garbage (random bytes with a valid header).
2. `strings -n 8 holiday_photo.jpg` prints a few readable lines: Software, Author, Comment, Camera.
3. The Comment line contains the flag: `strings -n 8 holiday_photo.jpg | grep Comment`

Flag: @FLAG@
""", FLAG=flag),
    )


# --------------------------------------------------------------------------
# CRYPTO 01 - Caesar
# --------------------------------------------------------------------------
def caesar(text, shift):
    out = []
    for ch in text:
        if ch.isascii() and ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            out.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            out.append(ch)
    return "".join(out)


def build_crypto_01():
    cid = "crypto-01-caesar"
    flag = "FLAG{caesar_would_be_proud}"
    plain = ("Meet me at the old library at midnight. Bring the documents and tell no one. "
             "The password for the vault is " + flag + ". Destroy this message after reading.")
    cipher = caesar(plain, 7)
    write(FILES / cid / "files" / "message.txt", cipher + "\n")

    register(
        cid, "Caesar's Message", "Crypto", "Easy", 100, "flag", flag,
        """
Two agents exchange messages using a very old technique. You intercepted one of them. Decrypt it and find the password.

Flag format: FLAG{...}
""",
        "`files/message.txt`: the intercepted message.",
        [
            "Look at the punctuation and the word lengths: they are preserved. This is a very old cipher that moves every letter by the same amount.",
            "This is a shift (Caesar) cipher. There are only 25 possible shifts, so you can try them all with a short script. You also know that the flag starts with FLAG.",
            "Compare the beginning of the flag in the ciphertext with FLAG: the distance between the letters gives the shift. Then apply the opposite shift to the whole message, with Python or with the `tr` command.",
        ],
        fill("""
## Walkthrough
1. In the ciphertext the flag appears as `MSHN{...}`. F -> M, L -> S, A -> H, G -> N: every letter moved forward by 7.
2. Decrypt by moving 7 back:
   `tr 'H-ZA-Gh-za-g' 'A-Za-z' < message.txt`
   or in Python with a shift of -7 (see the Caesar guide), or try all 26 shifts and look for FLAG{.
3. The plaintext reads: "Meet me at the old library at midnight ... The password for the vault is @FLAG@. ..."
""", FLAG=flag),
    )


# --------------------------------------------------------------------------
# CRYPTO 02 - encoding layers
# --------------------------------------------------------------------------
def build_crypto_02():
    cid = "crypto-02-onion"
    flag = "FLAG{encoding_is_not_encryption}"
    step1 = codecs.encode(flag, "rot13")
    step2 = step1.encode().hex()
    step3 = base64.b64encode(step2.encode()).decode()
    write(FILES / cid / "files" / "message.txt", step3 + "\n")

    register(
        cid, "Onion Layers", "Crypto", "Easy", 150, "flag", flag,
        """
A careless developer "protected" a secret by encoding it several times, believing that more layers means more security. The result is stored in a text file.

Peel the layers one by one and read the secret.

Flag format: FLAG{...}
""",
        "`files/message.txt`: one line of text.",
        [
            "None of this is real encryption: there is no key. Each layer is a well-known encoding that can be recognized by its look.",
            "Start with the alphabet of the data. Letters, digits and a trailing `=` suggest Base64. After decoding, look at the new text again: it may be another encoding. Hexadecimal and ROT13 are likely candidates.",
            "Three layers were applied, so three decodings are needed, in the opposite order. Command line tools `base64`, `xxd` and `tr` can be chained with pipes, or you can use Python or CyberChef.",
        ],
        fill("""
## Walkthrough
The flag was encoded in this order: ROT13, then hexadecimal, then Base64. Decode in reverse:
1. Base64 decode `message.txt`: `base64 -d message.txt` gives a long string of hexadecimal digits.
2. Hex decode that string (`xxd -r -p`, or `bytes.fromhex(...)` in Python): it gives `@ROT@`.
3. Apply ROT13: `tr 'A-Za-z' 'N-ZA-Mn-za-m'` gives @FLAG@.
One line: `base64 -d message.txt | xxd -r -p | tr 'A-Za-z' 'N-ZA-Mn-za-m'`
""", ROT=step1, FLAG=flag),
    )


# --------------------------------------------------------------------------
# CRYPTO 03 - single byte XOR
# --------------------------------------------------------------------------
def build_crypto_03():
    cid = "crypto-03-xor"
    flag = "FLAG{xor_with_one_byte_is_weak}"
    key = 0x4B
    plain = "Message intercepted. The secret flag is " + flag
    cipher_hex = bytes(b ^ key for b in plain.encode()).hex()
    write(FILES / cid / "files" / "cipher.hex", cipher_hex + "\n")

    register(
        cid, "One Byte Is Not Enough", "Crypto", "Medium", 250, "flag", flag,
        """
A custom encryption tool "mixes" every byte of a message with a secret value. You recovered an encrypted message, written in hexadecimal. The tool's author insists that nobody can break it without the key.

Prove him wrong.

Flag format: FLAG{...}
""",
        "`files/cipher.hex`: the encrypted message in hexadecimal.",
        [
            "The operation used to mix the bytes is a very common one in cryptography: it is its own inverse, so the same key encrypts and decrypts.",
            "It is XOR. The key is a single byte, which means there are only 256 possible keys. Convert the hexadecimal text to bytes first.",
            "Write a loop over every key from 0 to 255, XOR every byte of the data with it, and print the results that contain FLAG{ (or that are mostly printable text). Python's `bytes.fromhex` and a generator expression are enough.",
        ],
        fill("""
## Walkthrough
```python
data = bytes.fromhex(open("cipher.hex").read().strip())
for k in range(256):
    out = bytes(b ^ k for b in data)
    if b"FLAG{" in out:
        print(hex(k), out)
```
The key is @KEY@ (decimal @KEYD@). The output is: "@PLAIN@"
""", KEY=hex(key), KEYD=key, PLAIN=plain),
    )


# --------------------------------------------------------------------------
# CRYPTO 04 - textbook RSA byte by byte
# --------------------------------------------------------------------------
def build_crypto_04():
    cid = "crypto-04-rsa"
    flag = "FLAG{rsa_needs_big_primes}"
    p, q, e = 1000003, 1000033, 65537
    n = p * q
    ciphertext = [pow(b, e, n) for b in flag.encode()]
    write(FILES / cid / "files" / "output.txt",
          f"n = {n}\ne = {e}\nciphertext = {ciphertext}\n")

    register(
        cid, "Textbook RSA", "Crypto", "Hard", 300, "flag", flag,
        """
A student implemented RSA from a textbook and encrypted a secret one character at a time. The public key and the list of encrypted values are in the file below.

Recover the secret message.

Flag format: FLAG{...}
""",
        "`files/output.txt`: the public modulus n, the public exponent e, and the list of ciphertext numbers.",
        [
            "RSA security relies on the difficulty of splitting the public modulus n into its two prime factors. Check how big n really is.",
            "n is small enough to be factored with a simple loop (trial division), with sympy's factorint, or with an online factor database. Once you have p and q, the private key follows from the RSA formulas.",
            "Compute phi = (p-1)*(q-1), then d = pow(e, -1, phi). Each number of the list is one character: decrypt each with pow(c, d, n) and convert the result to a character. There is also a second way that does not require factoring n at all: think about how many different characters exist.",
        ],
        fill("""
## Walkthrough (method 1: factor n)
n = @N@ factors as @P@ * @Q@ (trial division up to 10^6 is enough).
```python
n, e = @N@, @E@
p, q = @P@, @Q@
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)
print("".join(chr(pow(c, d, n)) for c in ciphertext))
```
## Method 2: lookup table, no factoring
Each character is encrypted separately, so only 256 ciphertext values exist. Encrypt every byte with the public key and map back:
```python
table = {pow(b, e, n): chr(b) for b in range(256)}
print("".join(table[c] for c in ciphertext))
```
Both give @FLAG@.
Lesson: encrypting small units without padding is insecure even if the modulus is large.
""", N=n, E=e, P=p, Q=q, FLAG=flag),
    )


# --------------------------------------------------------------------------
# WEB 01 - SQL injection (judged by payload)
# --------------------------------------------------------------------------
LOGIN_APP = '''"""Login service of the intranet (source code provided for the audit)."""
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
'''


def build_web_01():
    cid = "web-01-login"
    flag = "FLAG{sql_injection_bypasses_login}"
    write(FILES / cid / "files" / "login_app.py", LOGIN_APP)

    register(
        cid, "Login Bypass", "Web", "Medium", 250, "payload", flag,
        """
The intranet login page is backed by the Python code below. The administrator's password is randomly generated every time the service starts, so you cannot guess or read it.

Log in as the administrator without knowing the password. To submit your answer, send the text you typed in the username field (the password field can contain anything). The platform runs it against the login code and gives you the flag if you get an administrator session.

This challenge is judged by the exploit, not by a flag you find.
""",
        "`files/login_app.py`: the source code of the login service. Run it locally with `python login_app.py` to test your ideas.",
        [
            "Read how the SQL query is built. Ask yourself what happens to the final query if the username contains a quote character.",
            "The username is pasted inside single quotes in the query. If you close the quote yourself, the rest of your input becomes SQL. SQL also has a comment syntax that makes the database ignore everything after it.",
            "Write down the final query for a username such as `x' ...`. You want the WHERE clause to select the admin row without the password check. Either target the admin user by name and comment out the password condition, or make the condition always true. Test it locally with `python login_app.py` before submitting.",
        ],
        """
## Walkthrough
The query is built by string formatting:
`SELECT username, role FROM users WHERE username = '<u>' AND password = '<p>'`

Username payload: `admin' --`
Resulting query: `SELECT username, role FROM users WHERE username = 'admin' --' AND password = '<anything>'`
Everything after `--` is a comment, so the password is never checked and the admin row is returned.

Another accepted payload: `' OR '1'='1' --` (the condition is always true and the first row is the admin user).

Defense: use parameterized queries: `db.execute("SELECT username, role FROM users WHERE username = ? AND password = ?", (username, password))`.
""",
    )


def main():
    for builder in (build_linux_01, build_linux_02, build_linux_03, build_forensics_01,
                    build_crypto_01, build_crypto_02, build_crypto_03, build_crypto_04,
                    build_web_01):
        builder()
    write(DATA / "flags.json", json.dumps(REGISTRY, indent=2) + "\n")
    print(f"{len(REGISTRY)} challenges generated")
    for cid, meta in REGISTRY.items():
        print(f"  {cid:24} {meta['points']:>4} pts  {meta['type']}")


if __name__ == "__main__":
    main()
