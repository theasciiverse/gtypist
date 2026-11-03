# Asciiverse patches

GNU Typist 2.10.1, from the signed release tarball at
<https://ftp.gnu.org/gnu/gtypist/>, packaged for the Asciiverse. The
first commit is the tarball as released.

GNU Typist is a classic: the tutor, its lessons and its screens are
upstream's, unchanged. The one source change is small and meant for
upstream.

## Source

- **Default lesson found through `GTYPIST_PATH`.** gtypist already
  searches `GTYPIST_PATH` for a lesson named on the command line, but
  with no lesson named it only looked in the directory compiled in at
  build time. Now it searches `GTYPIST_PATH` for `gtypist.typ` first and
  falls back to the compiled-in directory as before. This lets an
  install that isn't in its configured prefix, like av's, open the main
  course, with or without options such as `-b`. (`src/gtypist.c`)

## Packaging

- Built by `asciiverse/build.sh`: upstream's configure with `--prefix=/usr
  --disable-nls`, then `make -C src`. Only the program is built; the
  lessons are plain files, and the manual ships as upstream's HTML.
- **No translations of the program's own messages** (NLS off): they
  need gettext catalogues at a fixed path, which an av install can't
  provide. All the lessons, including the Spanish, Czech, Romanian,
  Russian and KTouch ones, are included and work.
- The av archive holds a start script, the binary and lessons in `lib/`,
  and the manual in `doc/`. The start script adds `lib/lessons` to
  `GTYPIST_PATH`, so `gtypist esp.typ` and the like work.
- Personal bests and settings stay where upstream keeps them:
  `~/.gtypist-bestlog` and `~/.gtypistrc`.
- Linux builds are static (Alpine). Alpine has the wide-character
  `ncurses.h` only at the top of `/usr/include`, and on macOS the
  system's ncurses is used; on both, `asciiverse/build.sh` puts them
  under the `ncursesw` names configure looks for.
