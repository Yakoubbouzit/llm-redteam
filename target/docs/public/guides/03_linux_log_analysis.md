# Analyzing Linux Authentication Logs

## Where the logs are
On Debian and Ubuntu systems SSH and login events are written to `/var/log/auth.log`. On Red Hat systems the file is `/var/log/secure`. In a CTF you are usually given a copy of the file.

## Line format
A typical sshd line has this structure:
`Oct 14 02:10:05 srv01 sshd[4121]: Failed password for invalid user admin from 203.0.113.50 port 51234 ssh2`
Fields: month, day, time, hostname, process and PID, then the message.

Common messages:
- `Failed password for <user> from <ip> port <n> ssh2`: a wrong password for an existing account.
- `Failed password for invalid user <name> from <ip> ...`: the account does not exist.
- `Invalid user <name> from <ip> port <n>`: sshd noticed an unknown account name.
- `Accepted password for <user> from <ip> ...` or `Accepted publickey for ...`: a successful login.
- `pam_unix(sshd:session): session opened for user <user>`: a session started.

## Spotting a brute-force attack
A brute-force attack looks like hundreds of failed logins from the same source address in a short time, often with many different user names. The most important question is whether a successful login follows the failures.

## Useful commands
- Count failed attempts per source address. The address is always the 3rd field from the end of a "Failed password" line, so `$(NF-3)` works for both valid and invalid users:
  `grep "Failed password" auth.log | awk '{print $(NF-3)}' | sort | uniq -c | sort -rn | head`
- List successful logins: `grep "Accepted" auth.log`
- Check one address: `grep "203.0.113.50" auth.log | grep -c "Failed password"`
- See which accounts an address tried: `grep "from 203.0.113.50" auth.log | grep "Invalid user" | awk '{print $8}' | sort | uniq -c | sort -rn`
- Look at what happened around a time: `grep "Oct 14 03:" auth.log | head -50`

## Reading the result
1. Rank source addresses by number of failures.
2. Take the top address and search for an `Accepted` line from it.
3. If one exists, the account named on that line is compromised.
4. Compare the first failure and the first success to understand the timeline.

## Defensive measures
fail2ban or rate limiting stops repeated failures, key-based authentication removes password guessing entirely, and disabling password login or root login in `sshd_config` reduces the attack surface.
