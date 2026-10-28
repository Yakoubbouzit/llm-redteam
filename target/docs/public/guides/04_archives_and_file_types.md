# Archives, Compression and File Types

Extensions can lie. Challenge authors often remove or change them. Identify files by their content.

## Identify first
- `file mystery` prints the detected type, for example "Zip archive data", "gzip compressed data", "bzip2 compressed data" or "POSIX tar archive".
- `xxd mystery | head -3` shows the first bytes. Common magic numbers:
  - gzip: 1f 8b
  - zip: 50 4b 03 04 (ASCII "PK")
  - bzip2: 42 5a 68 (ASCII "BZh")
  - xz: fd 37 7a 58 5a 00
  - tar: the text "ustar" at offset 257
  - PNG: 89 50 4e 47; JPEG: ff d8 ff; ELF: 7f 45 4c 46; PDF: 25 50 44 46 ("%PDF")

## Extract by type
- zip: `unzip file` (list with `unzip -l file`; install with `sudo apt install unzip`).
- tar: `tar -xf file` (tar detects gzip, bzip2 and xz automatically). List with `tar -tf file`.
- gzip: tools expect a `.gz` suffix. Without it, rename the file: `mv name name.gz && gunzip name.gz`. Or stream it: `gzip -dc < name > output`.
- bzip2: `mv name name.bz2 && bunzip2 name.bz2`, or `bzip2 -dc < name > output`.
- xz: `xz -dc < name > output`.
- 7z and rar: `7z x file` (package p7zip-full).

## Nested layers
Challenges often wrap data in several layers of different formats. The method never changes:
1. Run `file` on the current file.
2. Extract it with the matching tool.
3. Repeat on the result until you reach plain text.
Use one directory per layer so you do not lose track of the order.

## Passwords and embedded files
- `zip2john` followed by `john` can crack weak zip passwords.
- `binwalk file` scans for embedded files and `binwalk -e file` extracts them.
