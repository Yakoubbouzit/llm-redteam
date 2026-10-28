# Hints for: Textbook RSA (crypto-04-rsa)

## Hint 1

RSA security relies on the difficulty of splitting the public modulus n into its two prime factors. Check how big n really is.

## Hint 2

n is small enough to be factored with a simple loop (trial division), with sympy's factorint, or with an online factor database. Once you have p and q, the private key follows from the RSA formulas.

## Hint 3

Compute phi = (p-1)*(q-1), then d = pow(e, -1, phi). Each number of the list is one character: decrypt each with pow(c, d, n) and convert the result to a character. There is also a second way that does not require factoring n at all: think about how many different characters exist.
