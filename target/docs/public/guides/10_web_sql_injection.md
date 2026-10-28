# SQL Injection

## What it is
SQL injection happens when user input is placed directly into an SQL query as text. The database cannot tell the difference between the query written by the developer and the part supplied by the user, so an attacker can change the meaning of the query.

## A vulnerable pattern
```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
```
If the username is `alice`, the query is normal. If the username contains a single quote, it closes the string early and the rest of the input is read as SQL.

## How to test for it
- Submit a single quote `'`. A database error, a changed page or a crash suggests the input reaches the query unfiltered.
- Observe how the query would be built and which part of it you control. Write out the full resulting query on paper.

## Core ideas
- Always-true conditions: adding `OR 1=1` or `OR '1'='1'` makes the WHERE clause match every row.
- Comments: `--` (followed by a space in some databases) ignores the rest of the line, which removes the password check. MySQL also supports `#`.
- Choosing the user: closing the string after a known user name and commenting out the rest targets that account.
- UNION attacks: `UNION SELECT` appends the rows of another query so that data from other tables appears in the result. The number of columns and their types must match.
- Blind techniques: when no data is shown, ask true/false questions and watch the response (boolean-based) or its delay (time-based).

## Dialect differences
SQLite, MySQL, PostgreSQL and SQL Server differ in comment syntax, string concatenation and available functions. SQLite does not allow several statements in one call from most drivers.

## Defense
- Use parameterized queries (prepared statements): `db.execute("SELECT * FROM users WHERE username = ? AND password = ?", (u, p))`.
- Store password hashes with a slow algorithm (bcrypt, argon2) and compare hashes, not plaintext.
- Give the database account the minimum privileges it needs.
- Validate input as a second layer, never as the only layer.

## Practice
Tools: sqlmap for automation (only on systems you are allowed to test), Burp Suite for intercepting requests. Free labs: PortSwigger Web Security Academy, DVWA and OWASP Juice Shop.
