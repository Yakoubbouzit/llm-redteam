"""Check that every challenge of the pack is solvable and that nothing leaks.

Run:  python verify_pack.py
"""
import base64, codecs, gzip, bz2, io, json, re, subprocess, tarfile, zipfile
from pathlib import Path

import judge

ROOT = Path(__file__).resolve().parent
FILES = ROOT / "challenges"
FLAGS = json.loads((ROOT / "data" / "flags.json").read_text())


def read(cid, name):
    return (FILES / cid / "files" / name)


def check(cid, found):
    result = judge.check_answer(cid, found)
    assert result["ok"], f"{cid}: judge refused {found!r}"
    print(f"  OK  {cid}")


def solve_linux_01():
    out = subprocess.run(["grep", "-r", "FLAG{", str(read("linux-01-hidden", "home"))],
                         capture_output=True, text=True).stdout
    return re.search(r"FLAG\{[^}]+\}", out).group(0)


def solve_linux_02():
    log = read("linux-02-bruteforce", "auth.log").read_text().splitlines()
    counts = {}
    for line in log:
        if "Failed password" in line:
            ip = line.split()[-4]
            counts[ip] = counts.get(ip, 0) + 1
    ip = max(counts, key=counts.get)
    user = [l.split()[8] for l in log if "Accepted" in l and l.split()[10] == ip][0]
    return f"FLAG{{{ip}_{user}_{counts[ip]}}}"


def solve_linux_03():
    data = read("linux-03-matryoshka", "package.dat").read_bytes()
    layer = zipfile.ZipFile(io.BytesIO(data)).read("payload")
    layer = bz2.decompress(layer)
    layer = tarfile.open(fileobj=io.BytesIO(layer)).extractfile("inner").read()
    return gzip.decompress(layer).decode().strip()


def solve_forensics_01():
    raw = read("forensics-01-strings", "holiday_photo.jpg").read_bytes()
    return re.search(rb"FLAG\{[^}]+\}", raw).group(0).decode()


def solve_crypto_01():
    text = read("crypto-01-caesar", "message.txt").read_text()
    for k in range(26):
        out = "".join(chr((ord(c) - (65 if c.isupper() else 97) - k) % 26 + (65 if c.isupper() else 97))
                      if c.isascii() and c.isalpha() else c for c in text)
        m = re.search(r"FLAG\{[^}]+\}", out)
        if m:
            return m.group(0)


def solve_crypto_02():
    raw = base64.b64decode(read("crypto-02-onion", "message.txt").read_text().strip())
    return codecs.decode(bytes.fromhex(raw.decode()).decode(), "rot13")


def solve_crypto_03():
    data = bytes.fromhex(read("crypto-03-xor", "cipher.hex").read_text().strip())
    for k in range(256):
        out = bytes(b ^ k for b in data)
        m = re.search(rb"FLAG\{[^}]+\}", out)
        if m:
            return m.group(0).decode()


def solve_crypto_04():
    ns = {}
    exec(read("crypto-04-rsa", "output.txt").read_text(), ns)
    n, e, cts = ns["n"], ns["e"], ns["ciphertext"]
    p = next(i for i in range(2, 10**7) if n % i == 0)
    d = pow(e, -1, (p - 1) * (n // p - 1))
    return "".join(chr(pow(c, d, n)) for c in cts)


def solve_crypto_04_lookup():
    ns = {}
    exec(read("crypto-04-rsa", "output.txt").read_text(), ns)
    n, e, cts = ns["n"], ns["e"], ns["ciphertext"]
    table = {pow(b, e, n): chr(b) for b in range(256)}
    return "".join(table[c] for c in cts)


SOLVERS = {
    "linux-01-hidden": solve_linux_01, "linux-02-bruteforce": solve_linux_02,
    "linux-03-matryoshka": solve_linux_03, "forensics-01-strings": solve_forensics_01,
    "crypto-01-caesar": solve_crypto_01, "crypto-02-onion": solve_crypto_02,
    "crypto-03-xor": solve_crypto_03, "crypto-04-rsa": solve_crypto_04,
    "web-01-login": lambda: "admin' --",
}

if __name__ == "__main__":
    print("Solving every challenge:")
    for cid, solver in SOLVERS.items():
        check(cid, solver())
    assert solve_crypto_04_lookup() == FLAGS["crypto-04-rsa"]["flag"]
    print("  OK  crypto-04-rsa (lookup table method)")
    assert not judge.check_answer("web-01-login", "alice")["ok"]
    assert not judge.check_answer("crypto-01-caesar", "FLAG{wrong}")["ok"]
    print("  OK  wrong answers are refused")

    print("Leak check on public documents:")
    public = ROOT / "docs" / "public"
    for path in public.rglob("*.md"):
        text = path.read_text()
        for cid, meta in FLAGS.items():
            assert meta["flag"] not in text, f"{path} leaks the flag of {cid}"
    for path in FILES.rglob("*"):
        if path.is_file() and path.suffix in {".md"}:
            raise AssertionError("docs must not live in challenge files")
    print("  OK  no flag appears in docs/public")
    print("All checks passed.")
