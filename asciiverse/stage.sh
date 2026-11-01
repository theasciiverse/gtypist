#!/bin/sh
# Lays out the av archive in stage/: the start script at the top, the
# binary and the lessons in lib/, and the manual (HTML) with the licence.
set -eu
rm -rf stage && mkdir -p stage/lib/lessons stage/doc
cp asciiverse/gtypist stage/gtypist
cp src/gtypist stage/lib/gtypist
cp lessons/*.typ stage/lib/lessons/
cp doc/gtypist.html stage/doc/
cp COPYING README NEWS PATCHES.md stage/
