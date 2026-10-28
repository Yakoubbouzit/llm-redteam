# SOLUTION - CONFIDENTIAL - Brute Force Hunter (linux-02-bruteforce)

Flag: FLAG{203.0.113.77_deploy_612}

## Walkthrough
1. Rank failures per source address:
   `grep "Failed password" auth.log | awk '{print $(NF-3)}' | sort | uniq -c | sort -rn | head`
   The top three are 203.0.113.77 (612 failures), 198.51.100.23 (187) and 192.0.2.88 (54). Internal addresses have only a handful of failures each.
2. Check which of them logged in successfully:
   `grep "Accepted" auth.log | grep "203.0.113.77"`
   Result: `Accepted password for deploy from 203.0.113.77`. The other two noisy addresses never succeeded.
3. Count the failures of the attacker:
   `grep "Failed password" auth.log | grep -c "from 203.0.113.77 "`
   Result: 612.
4. Build the flag: FLAG{203.0.113.77_deploy_612}

Why the others are decoys: they brute-force too, but there is no Accepted line from them.
