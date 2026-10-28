# Classical Ciphers: Caesar, Vigenere and Substitution

## Caesar cipher
Each letter is shifted by a fixed number of positions in the alphabet. With a shift of 3, A becomes D and Z becomes C. Only letters change; digits and punctuation stay.
- There are only 25 useful shifts, so brute force is instant.
- A crib is faster: if the plaintext starts with FLAG{ and the ciphertext starts with MSHN{, then F became M, which is a shift of 7.
- To decrypt a shift of k in Python:
```python
def shift(text, k):
    out = []
    for ch in text:
        if ch.isascii() and ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            out.append(chr((ord(ch) - base + k) % 26 + base))
        else:
            out.append(ch)
    return "".join(out)

for k in range(26):
    print(k, shift(ciphertext, -k))
```
- With `tr`, a shift of 13 (ROT13) is `tr 'A-Za-z' 'N-ZA-Mn-za-m'`. For another shift, rotate the target alphabet by the same amount.

## Vigenere cipher
The key is a word repeated along the message; each letter of the key gives a different Caesar shift.
- If you know a crib, subtract it from the ciphertext to recover part of the key.
- To find the key length, use the Kasiski examination (distances between repeated sequences) or the index of coincidence, then solve each column as a Caesar cipher using frequency analysis.

## Monoalphabetic substitution
Every letter is replaced by another letter according to a fixed table. There are 26! tables, so brute force is impossible, but frequency analysis works: in English the most common letters are E, T, A, O, I, N, S, H, R. Start with one-letter words (A, I), common three-letter words (THE, AND) and repeated patterns.

## Atbash
A becomes Z, B becomes Y and so on. It has no key: `tr 'A-Za-z' 'ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba'`.

## General method
1. Check whether punctuation and word lengths are preserved. If yes, it is probably a substitution or shift cipher.
2. Try the cheapest attack first (brute force a Caesar shift, test cribs).
3. Use frequency analysis when the text is long enough (more than about 100 letters).
