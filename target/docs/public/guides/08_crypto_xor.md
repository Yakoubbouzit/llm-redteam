# XOR Encryption

XOR (written ^ in Python and C) combines two bits: the result is 1 only when the bits differ. Applied to bytes, it has three properties that matter in CTFs:
1. A ^ B ^ B = A: applying the same key twice gives back the original, so encryption and decryption are the same operation.
2. A ^ 0 = A: a zero byte leaves data unchanged.
3. If you know the plaintext and the ciphertext, you get the key: key = ciphertext ^ plaintext.

## Single-byte key
One byte (0 to 255) is XORed with every byte of the message. There are only 256 possible keys, so brute force is trivial: try all keys and keep outputs that look like text or contain FLAG{.
```python
data = bytes.fromhex(open("cipher.hex").read().strip())
for key in range(256):
    out = bytes(b ^ key for b in data)
    if b"FLAG{" in out:
        print(key, out)
```
A shortcut with a crib: if you know that the plaintext starts with "The", compute `key = data[0] ^ ord("T")` and check that it also decrypts the next bytes.

## Repeating key
A short key such as b"KEY" is repeated along the message. To break it:
1. Guess the key length, for example by finding the length that minimizes the normalized Hamming distance between blocks.
2. Split the ciphertext into columns, one per key position. Each column is a single-byte XOR problem.
3. Solve each column with letter frequency (the space character is the most common byte in English text).

## One-time pad and key reuse
A truly random key as long as the message, used once, is unbreakable. If the same key encrypts two messages, XORing the two ciphertexts removes the key and leaves plaintext1 ^ plaintext2, which can be attacked with cribs.

## Python tips
- `bytes.fromhex("4142")` converts hex text to bytes; `data.hex()` does the reverse.
- Iterating over a bytes object gives integers, so `b ^ key` works directly.
