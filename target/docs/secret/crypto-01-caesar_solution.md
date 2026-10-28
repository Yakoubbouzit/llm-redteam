# SOLUTION - CONFIDENTIAL - Caesar's Message (crypto-01-caesar)

Flag: FLAG{caesar_would_be_proud}

## Walkthrough
1. In the ciphertext the flag appears as `MSHN{...}`. F -> M, L -> S, A -> H, G -> N: every letter moved forward by 7.
2. Decrypt by moving 7 back:
   `tr 'H-ZA-Gh-za-g' 'A-Za-z' < message.txt`
   or in Python with a shift of -7 (see the Caesar guide), or try all 26 shifts and look for FLAG{.
3. The plaintext reads: "Meet me at the old library at midnight ... The password for the vault is FLAG{caesar_would_be_proud}. ..."
