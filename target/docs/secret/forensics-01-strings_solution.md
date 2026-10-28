# SOLUTION - CONFIDENTIAL - Strings Attached (forensics-01-strings)

Flag: FLAG{strings_reveals_hidden_text}

## Walkthrough
1. `file holiday_photo.jpg` reports JPEG data, but the image is garbage (random bytes with a valid header).
2. `strings -n 8 holiday_photo.jpg` prints a few readable lines: Software, Author, Comment, Camera.
3. The Comment line contains the flag: `strings -n 8 holiday_photo.jpg | grep Comment`

Flag: FLAG{strings_reveals_hidden_text}
