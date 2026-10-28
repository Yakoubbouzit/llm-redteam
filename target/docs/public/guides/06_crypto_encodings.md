# Encodings: Base64, Hex, ROT13 and Friends

An encoding is NOT encryption. It changes the representation of data without any secret key, so anyone who recognizes it can reverse it. CTF authors love to stack several encodings in layers.

## How to recognize them
- Base64: letters, digits, `+` and `/`, often ending with `=` or `==`. Length is a multiple of 4.
- Base32: only uppercase letters A to Z and digits 2 to 7, often ending with `=`.
- Hexadecimal: only 0-9 and a-f, even number of characters. Two hex characters are one byte.
- ROT13: looks like English text with wrong letters. Punctuation and digits are unchanged.
- URL encoding: `%20` style sequences.
- Binary: groups of 8 digits made of 0 and 1.

## Decoding on the command line
- Base64: `echo 'SGVsbG8=' | base64 -d`
- Base32: `echo 'JBSWY3DP' | base32 -d`
- Hex to bytes: `echo '48656c6c6f' | xxd -r -p` (package xxd)
- Bytes to hex: `echo -n 'Hello' | xxd -p`
- ROT13: `echo 'Uryyb' | tr 'A-Za-z' 'N-ZA-Mn-za-m'`
- Chain steps with pipes, for example: `base64 -d input.txt | xxd -r -p`

## Decoding in Python
```python
import base64, codecs
base64.b64decode("SGVsbG8=")          # b'Hello'
bytes.fromhex("48656c6c6f")            # b'Hello'
codecs.decode("Uryyb", "rot13")        # 'Hello'
```

## Peeling layers
1. Look at the data and decide which encoding it most resembles.
2. Decode one layer.
3. Look at the result again. The output of one layer is the input of the next.
4. Stop when you obtain readable text or the FLAG{ prefix.
CyberChef (https://gchq.github.io/CyberChef/) lets you chain these operations visually and has a "Magic" operation that guesses encodings.
