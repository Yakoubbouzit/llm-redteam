# Hints for: One Byte Is Not Enough (crypto-03-xor)

## Hint 1

The operation used to mix the bytes is a very common one in cryptography: it is its own inverse, so the same key encrypts and decrypts.

## Hint 2

It is XOR. The key is a single byte, which means there are only 256 possible keys. Convert the hexadecimal text to bytes first.

## Hint 3

Write a loop over every key from 0 to 255, XOR every byte of the data with it, and print the results that contain FLAG{ (or that are mostly printable text). Python's `bytes.fromhex` and a generator expression are enough.
