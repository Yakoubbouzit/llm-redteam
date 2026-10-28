# CTF Methodology: How to Approach a Challenge

A Capture The Flag (CTF) challenge is a small puzzle with a hidden string called a flag. On this platform every flag looks like FLAG{some_text_here}. Finding it proves that you solved the challenge.

## Step 1: Read the description twice
Descriptions contain clues. Note the category (Linux, crypto, forensics, web), the files you are given, the flag format, and any unusual word choice. Authors rarely add useless details.

## Step 2: Identify what you are looking at
Before trying to solve anything, find out what the data is.
- Run `file <name>` on every file. Do not trust extensions.
- Run `ls -la` to see hidden files, sizes and permissions.
- Look at the first bytes with `xxd <file> | head`.
- Read text files completely before using tools on them.

## Step 3: Form a hypothesis
Ask: what is the simplest transformation that would produce this data? Encoded text, a classic cipher, a compressed archive, a hidden file, a vulnerable query, a weak key. Always try the simple explanation first. Most beginner and intermediate challenges are solved by one well-chosen command.

## Step 4: Use known formats as cribs
You know the flag starts with FLAG{ . In crypto challenges this known text, called a crib, lets you test a guess immediately: if a decryption attempt produces FLAG{ somewhere, you most likely found the key.

## Step 5: Automate repeated work
If you must try 26 shifts, 256 keys or thousands of log lines, write a short script in Python or a shell pipeline. Typing by hand leads to mistakes.

## Step 6: Keep notes
Write down every command you run and what it returned. When you are stuck, your notes show what you already ruled out. After solving, a short write-up (what you saw, what you tried, what worked) is the best way to remember the technique.

## When you are stuck
1. Re-read the description and the hints you already have.
2. Change the tool, not just the options.
3. Take a break; many solutions become obvious after ten minutes away.
4. Ask for a hint, not for the answer. A hint gives a direction; a solution teaches nothing.

## Ethics
Only test systems you own or have written permission to test. CTF platforms and practice labs are legal training grounds. The same techniques used against real systems without authorization are illegal.
