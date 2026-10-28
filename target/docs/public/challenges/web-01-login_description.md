# Login Bypass

- Challenge ID: web-01-login
- Category: Web
- Difficulty: Medium
- Points: 250

The intranet login page is backed by the Python code below. The administrator's password is randomly generated every time the service starts, so you cannot guess or read it.

Log in as the administrator without knowing the password. To submit your answer, send the text you typed in the username field (the password field can contain anything). The platform runs it against the login code and gives you the flag if you get an administrator session.

This challenge is judged by the exploit, not by a flag you find.

## Files

`files/login_app.py`: the source code of the login service. Run it locally with `python login_app.py` to test your ideas.
