# GNU Typist (Asciiverse packaging)

GNU Typist (gtypist), the GNU typing tutor (Simon Baldwin, 1998;
maintained by Mihai Gătejescu), packaged for the Asciiverse catalog. A
classic: don't change the tutor, its lessons or screens; packaging fixes
only, each listed in PATCHES.md and small enough for upstream.

- The first commit is the signed 2.10.1 release tarball (tag `2.10.1`),
  since Savannah's git (git.savannah.gnu.org/git/gtypist.git) returned
  HTTP 500. Upstream releases: https://ftp.gnu.org/gnu/gtypist/ (check
  the .sig against the GNU keyring).
- Build: `sh asciiverse/build.sh` (configure --prefix=/usr --disable-nls,
  `make -C src`), then `sh asciiverse/stage.sh`; run `stage/gtypist`.
  Configure rewrites the tracked `m4/Makefile`; `git checkout` it.
- Lessons: the start script puts `lib/lessons` on `GTYPIST_PATH`; our one
  source patch makes the default lesson (`gtypist.typ`) use it too.
- Preview: `python3 asciiverse/record-preview.py` (tmux, asciinema 3):
  lesson Q1, two drills at ~65 wpm with one typo. tmux takes a bare ";"
  as a command separator, so the bot sends keys as hex (`send-keys -H`).
