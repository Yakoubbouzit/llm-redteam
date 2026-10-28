# SOLUTION - CONFIDENTIAL - One Byte Is Not Enough (crypto-03-xor)

Flag: FLAG{xor_with_one_byte_is_weak}

## Walkthrough
```python
data = bytes.fromhex(open("cipher.hex").read().strip())
for k in range(256):
    out = bytes(b ^ k for b in data)
    if b"FLAG{" in out:
        print(hex(k), out)
```
The key is 0x4b (decimal 75). The output is: "Message intercepted. The secret flag is FLAG{xor_with_one_byte_is_weak}"
