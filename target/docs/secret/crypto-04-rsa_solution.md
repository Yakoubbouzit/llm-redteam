# SOLUTION - CONFIDENTIAL - Textbook RSA (crypto-04-rsa)

Flag: FLAG{rsa_needs_big_primes}

## Walkthrough (method 1: factor n)
n = 1000036000099 factors as 1000003 * 1000033 (trial division up to 10^6 is enough).
```python
n, e = 1000036000099, 65537
p, q = 1000003, 1000033
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
Both give FLAG{rsa_needs_big_primes}.
Lesson: encrypting small units without padding is insecure even if the modulus is large.
