# Brute Force Hunter

- Challenge ID: linux-02-bruteforce
- Category: Linux
- Difficulty: Medium
- Points: 200

The server `srv01` raised an alert: someone seems to have guessed their way into an account over SSH. You received a copy of its authentication log.

Find the address that launched the brute-force attack, the account it finally got into, and how many failed password attempts it made before succeeding. Count only lines containing "Failed password" that come from that address.

Flag format: FLAG{<attacker_ip>_<compromised_user>_<number_of_failed_password_lines>}
Example of the shape: FLAG{192.0.2.1_bob_42}

## Files

`files/auth.log`: the SSH authentication log (a few thousand lines, two days of activity).
