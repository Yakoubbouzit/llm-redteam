# RSA Basics for CTFs

## How RSA works
1. Choose two large primes p and q. Compute n = p * q and phi = (p - 1) * (q - 1).
2. Choose a public exponent e that is coprime with phi (65537 is the usual value).
3. Compute the private exponent d, the modular inverse of e modulo phi.
4. The public key is (n, e). The private key is d.
5. To encrypt a number m smaller than n: c = m^e mod n.
6. To decrypt: m = c^d mod n.
Security rests on the difficulty of finding p and q from n.

## Python
```python
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)          # modular inverse (Python 3.8+)
m = pow(c, d, n)             # decryption
text = m.to_bytes((m.bit_length() + 7) // 8, "big")
```

## Common weaknesses
- Small primes: if n is small, factor it. Trial division is enough up to about 10^12; sympy's `factorint(n)` and the online database factordb.com handle many more cases.
- Textbook RSA without padding: the same plaintext always gives the same ciphertext. If a message is encrypted byte by byte, only 256 ciphertexts exist, so an attacker can encrypt every possible byte with the public key, build a lookup table and decrypt the message without ever factoring n.
- Small e with small messages: if m^e is smaller than n, the modulus never applies and you can take the e-th root of c.
- Reused primes between two keys: gcd(n1, n2) reveals a shared prime.
- Common modulus, Wiener's attack (large e, small d) and Hastad's broadcast attack are common intermediate topics.
Real systems use 2048-bit or larger moduli and padding schemes such as OAEP.

## Tools
Python with pow() is enough for most challenges. Others: sympy, pycryptodome, RsaCtfTool (https://github.com/RsaCtfTool/RsaCtfTool), SageMath for heavy math.

## Workflow
1. Read n, e and c. Is n small or does it have an obvious structure?
2. Try to factor n.
3. Compute phi and d, then decrypt.
4. If the ciphertext is a list of small numbers, suspect byte-by-byte encryption and consider the lookup table attack.
