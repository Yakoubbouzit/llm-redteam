# Linux Command Line Essentials for CTFs

## Navigating and listing
- `pwd` prints the current directory.
- `ls -la` lists all files, including hidden ones (names starting with a dot), with permissions, owner, size and date.
- `cd <dir>` changes directory; `cd ..` goes up; `cd ~` goes to your home directory.
- `tree -a` shows a directory tree including hidden entries (install with `sudo apt install tree`).

## Reading files
- `cat file` prints a file. `less file` lets you scroll (press q to quit).
- `head -n 20 file` and `tail -n 20 file` show the first or last lines. `tail -f file` follows a growing log.
- `wc -l file` counts lines.

## Finding files
- `find . -name "*.txt"` finds files by name pattern.
- `find . -type f -name ".*"` finds hidden files.
- `find / -type f -size +1M 2>/dev/null` finds big files; `2>/dev/null` hides permission errors.
- `find / -perm -4000 -type f 2>/dev/null` lists SUID binaries, a classic privilege escalation lead.
- `find . -newer other_file` finds files modified after another file.

## Searching inside files
- `grep "text" file` prints matching lines. Useful options: `-i` ignore case, `-n` line numbers, `-v` invert the match, `-c` count matches, `-E` extended regular expressions, `-r` search recursively through a directory.
- Example: `grep -rn "password" /home/student` searches every file under that directory.

## File types
- `file <name>` identifies the real type from the content, not from the extension.
- `strings <file>` prints readable text found inside binary files.

## Permissions
`ls -l` shows something like `-rwxr-x---`. The first character is the type, then three triplets for owner, group and others. Read is 4, write is 2, execute is 1, so rwxr-x--- equals 750.
- `chmod 640 file` or `chmod +x script.sh` changes permissions.
- If you own a file you cannot read, `chmod u+r file` fixes it.

## Pipes and redirection
- `a | b` sends the output of a into b. Pipelines are the core of fast analysis.
- `>` writes output to a file, `>>` appends, `2>/dev/null` discards error messages.

## Text processing toolbox
- `sort` sorts lines; `sort -rn` sorts numerically in reverse order.
- `uniq -c` counts consecutive identical lines (always sort first).
- `cut -d' ' -f3` takes the third space-separated column.
- `awk '{print $1, $NF}'` prints the first and last column of every line; `$NF` is the last field.
- `tr 'a-z' 'A-Z'` translates characters; `sed 's/old/new/g'` replaces text.

## A classic counting pipeline
To find the most frequent value in a column:
`cut -d' ' -f1 file | sort | uniq -c | sort -rn | head`
Read it from left to right: extract the column, sort so equal values are adjacent, count them, sort by count, keep the top lines.
