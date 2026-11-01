#!/usr/bin/env python3
"""Records asciiverse/gtypist.cast, GNU Typist's catalog preview, at
100x30 (hub/RECORDING.md): the main menu, lesson Q1's first screens, then
DRILLS drills (default 2) typed by a steady typist at about 65 wpm, who
makes one mistake in the second drill; then back out and quit.

The bot types what the drill shows: drill text sits on every other row
below the instruction, with the typing row under each. Keys go to tmux as
hex bytes, since tmux would take a bare ";" as a command separator. A
fresh HOME keeps your own bestlog out. asciinema 3 records inside tmux.
Usage, from the repo root after asciiverse/build.sh and stage.sh:
    python3 asciiverse/record-preview.py"""
import os, random, subprocess, tempfile, time

s = "gtypist-preview"
drills = int(os.environ.get("DRILLS", 2))
home = tempfile.mkdtemp()
random.seed(7)

def screen():
    return subprocess.run(["tmux", "capture-pane", "-p", "-t", s],
                          capture_output=True, text=True).stdout.split("\n")
def key(k, wait):
    subprocess.run(["tmux", "send-keys", "-t", s, k]); time.sleep(wait)
def typech(ch):
    subprocess.run(["tmux", "send-keys", "-t", s, "-H"]
                   + ["%02x" % b for b in ch.encode()])
    time.sleep(random.uniform(0.10, 0.26) + (0.15 if ch == " " and random.random() < 0.2 else 0))

subprocess.run(["tmux", "kill-session", "-t", s], stderr=subprocess.DEVNULL)
subprocess.run(["tmux", "new-session", "-d", "-s", s, "-x", "100", "-y", "30",
    f"HOME={home} TERM=xterm-256color COLORTERM=truecolor LANG=C.UTF-8 "
    "asciinema rec --overwrite -q -i 2 --window-size 100x30 "
    "--capture-env TERM,COLORTERM,LANG -c ./stage/gtypist "
    "asciiverse/gtypist.cast"])
time.sleep(2.0)
key("Enter", 1.8)                 # welcome screen
key("Enter", 1.5)                 # series menu: Q
key("Enter", 2.0)                 # Q1
for _ in range(3):                # the tutorial screens
    key("Enter", 1.6)

for n in range(drills):
    rows = screen()
    # the instruction is the first row after the title; the drill text
    # starts two rows below it, on every other row
    top = next(i for i, l in enumerate(rows) if l.strip() and i > 0)
    lines = []
    for l in rows[top + 2::2]:
        if not l.strip() or "Drill" in l: break
        lines.append(l.rstrip())
    for li, text in enumerate(lines):
        typo = n == 1 and li == 0     # one slip, in the second drill
        for i, ch in enumerate(text):
            if typo and i >= len(text) // 2 and ch != " ":
                typech("e" if ch != "e" else "r")   # wrong key; carry on
                typo = False
                continue
            typech(ch)
        key("Enter", 1.0)
    time.sleep(1.5)                   # read the speed box
    if any("too high" in l for l in screen()):
        key("Enter", 1.0); continue   # (shouldn't happen at one slip)
    key("n", 1.2) if n < drills - 1 else None

key("e", 1.0); key("y", 1.5)         # leave the lesson: are you sure? yes
key("Escape", 1.2)                    # series menu
key("Escape", 1.5)                    # quit
subprocess.run(["tmux", "kill-session", "-t", s], stderr=subprocess.DEVNULL)
