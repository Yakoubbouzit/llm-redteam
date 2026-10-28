# Looking Inside Binary Files: strings, hex dumps and metadata

## Why it works
Programs, images, documents and memory dumps are binary, but they often contain readable text: error messages, file paths, comments, metadata, passwords or flags left by mistake. Extracting that text is one of the first steps of any forensics or reverse engineering task.

## strings
- `strings file` prints sequences of printable characters (default minimum length 4).
- `strings -n 8 file` keeps only sequences of 8 or more characters, which removes most noise.
- `strings -t x file` prints the hexadecimal offset of each match.
- `strings -e l file` looks for 16-bit little-endian text (common in Windows files).
- Combine with grep: `strings -n 6 file | grep -i "flag\|password\|secret"`.
- `strings` is part of the binutils package: `sudo apt install binutils`.

## Hex dumps
- `xxd file | head -20` shows offsets, hexadecimal bytes and an ASCII column.
- `hexdump -C file | less` is an alternative.
- The first bytes (the magic number) tell you the real file type. Compare them with `file`: if they disagree, the file was modified.

## Metadata
- `exiftool image.jpg` prints metadata such as author, camera, software, GPS position and comments.
- `binwalk image.jpg` finds files hidden inside other files.
- Documents (docx, xlsx, pptx) are zip archives: `unzip document.docx -d out` lets you read the XML inside.

## Typical workflow
1. `file name`: what is it supposed to be?
2. `xxd name | head`: does the header match?
3. `strings -n 6 name | less`: is there readable text?
4. `exiftool name` and `binwalk name`: metadata and embedded files.
5. Only then consider heavier tools.
