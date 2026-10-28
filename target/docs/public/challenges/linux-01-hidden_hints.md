# Hints for: Hidden in Plain Sight (linux-01-hidden)

## Hint 1

In Linux, a file or directory whose name starts with a dot is hidden from the default `ls` output. Think about how to display everything.

## Hint 2

Use `ls -la` in each directory, or `find . -type f -name ".*"` to list every hidden file at once. Shell history files sometimes show where a user was looking.

## Hint 3

Start in the home directory and look at `.bash_history`. It points to a configuration directory. List it with `ls -a`, then follow the hidden directory inside. As a shortcut, `grep -r "FLAG{" .` searches every file below the current directory.
