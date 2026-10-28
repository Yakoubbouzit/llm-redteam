# SOLUTION - CONFIDENTIAL - Onion Layers (crypto-02-onion)

Flag: FLAG{encoding_is_not_encryption}

## Walkthrough
The flag was encoded in this order: ROT13, then hexadecimal, then Base64. Decode in reverse:
1. Base64 decode `message.txt`: `base64 -d message.txt` gives a long string of hexadecimal digits.
2. Hex decode that string (`xxd -r -p`, or `bytes.fromhex(...)` in Python): it gives `SYNT{rapbqvat_vf_abg_rapelcgvba}`.
3. Apply ROT13: `tr 'A-Za-z' 'N-ZA-Mn-za-m'` gives FLAG{encoding_is_not_encryption}.
One line: `base64 -d message.txt | xxd -r -p | tr 'A-Za-z' 'N-ZA-Mn-za-m'`
