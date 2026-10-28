# Hints for: Strings Attached (forensics-01-strings)

## Hint 1

Binary files are not only bytes: programs and image editors often leave readable text inside them.

## Hint 2

A command called `strings` prints the readable sequences found in any file. A minimum length like `-n 8` removes most noise.

## Hint 3

Pipe the output into grep to filter it: `strings -n 8 holiday_photo.jpg | grep -i comment`. You can also look at the first bytes with `xxd` to confirm the file type.
