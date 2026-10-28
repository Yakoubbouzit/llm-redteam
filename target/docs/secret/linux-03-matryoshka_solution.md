# SOLUTION - CONFIDENTIAL - Matryoshka (linux-03-matryoshka)

Flag: FLAG{nested_archives_need_the_file_command}

## Walkthrough
Work in an empty directory and always run `file` before extracting.
1. `file package.dat` -> Zip archive data. `unzip package.dat` extracts a file named `payload`.
2. `file payload` -> bzip2 compressed data. `bzip2 -dc < payload > layer3` (or rename to payload.bz2 and run `bunzip2 payload.bz2`).
3. `file layer3` -> POSIX tar archive. `tar -xf layer3` extracts a file named `inner`.
4. `file inner` -> gzip compressed data. `gzip -dc < inner` prints the flag (or rename to inner.gz and run `gunzip inner.gz; cat inner`).

Layer order from the outside: zip, bzip2, tar, gzip, plain text.
