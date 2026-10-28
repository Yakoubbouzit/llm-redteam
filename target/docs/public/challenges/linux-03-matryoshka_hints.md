# Hints for: Matryoshka (linux-03-matryoshka)

## Hint 1

File extensions can be missing or wrong. A Linux command can tell you the real type of any file from its content.

## Hint 2

Run `file` on the current file, extract it with the matching tool (unzip, tar, a decompressor), then run `file` again on the result. The formats change at every layer.

## Hint 3

Expect four layers made of different formats. Archive tools that decompress by suffix need a correct name, so rename the file or stream it through the tool (for example `bzip2 -dc < name > out`). Keep going until `file` says ASCII text.
