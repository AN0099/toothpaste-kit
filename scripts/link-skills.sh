#!/bin/sh
# Symlink this repository's skills into a Claude skills directory.
#
# The README's `cp -r` is simpler and is the right choice if you intend to edit
# the skills locally. Symlinking instead means `git pull` updates them in place
# rather than leaving a stale copy behind.
#
# Usage, from anywhere:
#   scripts/link-skills.sh                 links into ~/.claude/skills
#   scripts/link-skills.sh /path/to/skills links into that directory
#
# Re-runnable. Existing symlinks are replaced. A real directory of the same name
# is left alone and reported, so a hand-edited local skill is never clobbered.

set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
src="$repo_root/skills"
dest="${1:-$HOME/.claude/skills}"

if [ ! -d "$src" ]; then
    echo "error: no skills directory at $src" >&2
    exit 1
fi

mkdir -p "$dest"

linked=0
skipped=0

for d in "$src"/*/; do
    [ -d "$d" ] || continue
    name=$(basename "$d")
    target="$dest/$name"

    if [ -e "$target" ] && [ ! -L "$target" ]; then
        echo "skip  $name (a real directory is already there)"
        skipped=$((skipped + 1))
        continue
    fi

    ln -sfn "${d%/}" "$target"
    echo "link  $name"
    linked=$((linked + 1))
done

echo
echo "$linked linked, $skipped skipped, into $dest"

if [ "$skipped" -gt 0 ]; then
    echo "Skipped entries are real directories. Move or delete them, then re-run."
fi
