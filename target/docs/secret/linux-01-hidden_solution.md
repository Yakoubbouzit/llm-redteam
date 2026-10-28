# SOLUTION - CONFIDENTIAL - Hidden in Plain Sight (linux-01-hidden)

Flag: FLAG{dotfiles_hide_in_plain_sight}

## Walkthrough
1. Go to the files: `cd challenges/linux-01-hidden/files/home/student`
2. `ls` shows only Documents, Downloads, Music and Pictures. Use `ls -la` to see hidden entries: `.bash_history`, `.cache`, `.config`.
3. `cat .bash_history` shows the student went to `~/.config` and ran `ls -a`.
4. `ls -la .config` reveals a hidden directory `.archive`; `ls -la .config/.archive` reveals `.old_notes.txt`.
5. `cat .config/.archive/.old_notes.txt` prints the flag.

Shortcuts: `find . -type f -name ".*"` or `grep -r "FLAG{" .`

Flag: FLAG{dotfiles_hide_in_plain_sight}
