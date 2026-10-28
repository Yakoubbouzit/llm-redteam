# Hints for: Onion Layers (crypto-02-onion)

## Hint 1

None of this is real encryption: there is no key. Each layer is a well-known encoding that can be recognized by its look.

## Hint 2

Start with the alphabet of the data. Letters, digits and a trailing `=` suggest Base64. After decoding, look at the new text again: it may be another encoding. Hexadecimal and ROT13 are likely candidates.

## Hint 3

Three layers were applied, so three decodings are needed, in the opposite order. Command line tools `base64`, `xxd` and `tr` can be chained with pipes, or you can use Python or CyberChef.
