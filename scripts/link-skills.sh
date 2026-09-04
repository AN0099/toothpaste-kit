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
#
# Link targets are relative where the system supports it, so the links keep
# working if the tree is moved. GNU coreutils has `ln -r`; BSD and macOS do not,
# and there the targets are absolute. The script says which it used.

set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
src="$repo_root/skills"
dest="${1:-$HOME/.claude/skills}"

if [ ! -d "$src" ]; then
    echo "error: no skills directory at $src" >&2
    exit 1
fi

mkdir -p "$dest"

# Probe once for relative-symlink support rather than assuming a coreutils flag.
probe="$dest/.link-skills-probe"
rm -f "$probe"
if ln -sr "$src" "$probe" 2>/dev/null; then
    relative=yes
else
    relative=no
fi
rm -f "$probe"

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

    if [ "$relative" = yes ]; then
        ln -sfnr "${d%/}" "$target"
    else
        ln -sfn "${d%/}" "$target"
    fi
    echo "link  $name"
    linked=$((linked + 1))
done

echo
if [ "$relative" = yes ]; then
    echo "$linked linked (relative targets), $skipped skipped, into $dest"
else
    echo "$linked linked (absolute targets, ln -r unavailable), $skipped skipped, into $dest"
fi

if [ "$skipped" -gt 0 ]; then
    echo "Skipped entries are real directories. Move or delete them, then re-run."
fi
