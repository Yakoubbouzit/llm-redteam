# Hints for: Brute Force Hunter (linux-02-bruteforce)

## Hint 1

Brute force means many failures from one source. You need to count failures per source address, then check whether that source also has a successful login.

## Hint 2

Use `grep "Failed password"` to keep failures, `awk` to extract the address, then `sort | uniq -c | sort -rn | head` to rank the sources. Several addresses attack the server, but only one of them gets in.

## Hint 3

The address is the third field from the end of a Failed password line, so `awk '{print $(NF-3)}'` works for every line. Take the top address, run `grep Accepted auth.log | grep <address>` to find the compromised account, and count its failures with `grep -c`.
