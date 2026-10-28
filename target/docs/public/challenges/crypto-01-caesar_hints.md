# Hints for: Caesar's Message (crypto-01-caesar)

## Hint 1

Look at the punctuation and the word lengths: they are preserved. This is a very old cipher that moves every letter by the same amount.

## Hint 2

This is a shift (Caesar) cipher. There are only 25 possible shifts, so you can try them all with a short script. You also know that the flag starts with FLAG.

## Hint 3

Compare the beginning of the flag in the ciphertext with FLAG: the distance between the letters gives the shift. Then apply the opposite shift to the whole message, with Python or with the `tr` command.
