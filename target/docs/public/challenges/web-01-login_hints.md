# Hints for: Login Bypass (web-01-login)

## Hint 1

Read how the SQL query is built. Ask yourself what happens to the final query if the username contains a quote character.

## Hint 2

The username is pasted inside single quotes in the query. If you close the quote yourself, the rest of your input becomes SQL. SQL also has a comment syntax that makes the database ignore everything after it.

## Hint 3

Write down the final query for a username such as `x' ...`. You want the WHERE clause to select the admin row without the password check. Either target the admin user by name and comment out the password condition, or make the condition always true. Test it locally with `python login_app.py` before submitting.
