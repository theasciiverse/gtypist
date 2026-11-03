#!/bin/sh
# Builds gtypist (src/gtypist). Linux: run inside alpine:3.22 for a fully
# static binary (ncursesw linked in); macOS: run on the runner with CC_ARCH
# set to x86_64 or arm64, linking the system's ncurses. Other Linux (local
# testing) links ncursesw shared.
#   docker run --rm -v "$PWD":/src -w /src alpine:3.22 sh asciiverse/build.sh
# Only src/ is built: the lessons are plain files, and the manual and the
# translations would need makeinfo and gettext (NLS is off; see PATCHES.md).
# The binary is configured for /usr (DATADIR /usr/share/gtypist, used by
# the system packages); the av start script points GTYPIST_PATH at its own
# lessons instead.
set -eu

# A git checkout gives every file the same age, which can make automake
# want to regenerate; restore the order of the release tarball.
touch aclocal.m4
touch configure config.h.in
find . -name Makefile.in -exec touch {} +

if [ -f /etc/alpine-release ]; then
  apk add --no-cache build-base ncurses-dev ncurses-static >/dev/null
  # configure wants <ncursesw/ncurses.h>; Alpine's ncurses-dev has the
  # wide-character ncurses.h only at the top of /usr/include, so name it.
  # _GNU_SOURCE from the start: some files include <stdlib.h> before
  # config.h defines it, and Alpine's fortify headers then miss mempcpy.
  shim="$PWD/build/alpine-ncursesw"
  mkdir -p "$shim/ncursesw"
  printf '#include <ncurses.h>\n' > "$shim/ncursesw/ncurses.h"
  export CPPFLAGS="-I$shim -DNCURSES_WIDECHAR=1 -D_GNU_SOURCE" LDFLAGS="-static"
elif [ "$(uname)" = Darwin ]; then
  # configure wants <ncursesw/ncurses.h> and -lncursesw; macOS's ncurses
  # is wide-character capable under other names, so name them.
  shim="$PWD/build/macos-ncursesw"
  mkdir -p "$shim/ncursesw"
  printf '#include <curses.h>\n' > "$shim/ncursesw/ncurses.h"
  ln -sf "$(xcrun --show-sdk-path)/usr/lib/libncurses.tbd" "$shim/libncursesw.tbd"
  export CPPFLAGS="-I$shim -D_XOPEN_SOURCE_EXTENDED" LDFLAGS="-L$shim"
fi
export CC="cc${CC_ARCH:+ -arch $CC_ARCH}"

[ -f Makefile ] && make distclean >/dev/null 2>&1 || true
./configure --prefix=/usr --disable-nls >/dev/null
make -C src
strip src/gtypist
