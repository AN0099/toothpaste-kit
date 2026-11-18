#!/bin/sh

# SPDX-FileCopyrightText: 2026 Aidan Naveja
#
# SPDX-License-Identifier: Apache-2.0

# Symlink this repository's skills into a Claude skills directory.
#
# docs/installing.md describes copying instead, which is the right choice if you
# intend to edit the skills locally. Symlinking means `git pull` updates them in
# place rather than leaving a stale copy behind. docs/quickstart.md uses this
# script with a workspace target.
#
# Usage, from anywhere:
#   scripts/link-skills.sh                 links into ~/.claude/skills
#   scripts/link-skills.sh /path/to/skills links into that directory
#   scripts/link-skills.sh --all [DIR]     also links the optional skills
#   scripts/link-skills.sh --dry-run [DIR] prints the target directory and
#                                          every link it would create or skip;
#                                          writes nothing
#   scripts/link-skills.sh --base [DIR]    links every skill except the
#                                          maintainer's own layer,
#                                          house-preferences; combines with
#                                          --dry-run
#   scripts/link-skills.sh --selftest      runs it in a temporary directory and
#                                          checks the result; scripts/gates.sh
#                                          runs this (TK-111)
#
# Before writing anything, it prints the directory it will write to and every
# link it will create or skip. --dry-run stops there and writes nothing.
#
# The optional skills, listed below, are left out unless --all is given. They
# need a tool this kit does not yet ship: the three review skills read a
# lane-board tool. A link already in place for one is left as it is either way.
#
# Re-runnable. Existing symlinks are replaced. A real directory of the same name
# is left alone and reported, so a hand-edited local skill is never clobbered.
#
# Link targets are relative where the system supports it, so the links keep
# working if the tree is moved. GNU coreutils has `ln -r`; BSD and macOS do not,
# and there the targets are absolute. The script says which it used.

set -eu

# Skills linked only with --all. A change here is a change to the note on
# optional skills in README.md and docs/installing.md.
optional='daily-review
monthly-review
weekly-review'

if [ "${1:-}" = --selftest ]; then
    self=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)/$(basename -- "$0")
    root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
    tmp=$(mktemp -d)
    # Each signal gets its own handler with an exit: under sh, an EXIT trap
    # alone does not run on an interrupt (the lesson in scripts/gates.sh).
    trap 'rm -rf -- "${tmp:?}"' EXIT
    trap 'rm -rf -- "${tmp:?}"; exit 130' INT
    trap 'rm -rf -- "${tmp:?}"; exit 143' TERM
    fails=0
    ok()  { echo "ok   $1"; }
    bad() { echo "FAIL $1"; fails=$((fails + 1)); }
    want=$(cd "$root/skills" && for d in */; do [ -d "$d" ] && printf '%s\n' "${d%/}"; done \
        | grep -vxF "$optional")
    n=$(printf '%s\n' "$want" | grep -c .)
    # A real directory where one skill's link would go: it must be left alone.
    keep=$(printf '%s\n' "$want" | head -1)
    mkdir -p "$tmp/dest/$keep" && echo mine > "$tmp/dest/$keep/local.md"
    if sh "$self" "$tmp/dest" > "$tmp/out1" 2>&1; then ok "exits 0 into a directory holding one real skill directory"; else bad "exit non-zero: $(tail -1 "$tmp/out1")"; fi
    good=0
    for name in $want; do
        [ "$name" = "$keep" ] && continue
        if [ -L "$tmp/dest/$name" ] && [ "$(CDPATH= cd -- "$tmp/dest/$name" && pwd -P)" = "$(CDPATH= cd -- "$root/skills/$name" && pwd -P)" ]; then
            good=$((good + 1))
        else bad "$name is not a link to skills/$name"; fi
    done
    [ "$good" -eq $((n - 1)) ] && ok "each of $((n - 1)) skills links to its own skills/ directory" || bad "$good of $((n - 1)) skills linked correctly"
    n_opt=$(printf '%s\n' "$optional" | grep -c .)
    left=0
    for name in $optional; do
        [ -d "$root/skills/$name" ] || bad "optional skill $name has no skills/ directory"
        [ ! -e "$tmp/dest/$name" ] && grep -q "^skip  $name (optional" "$tmp/out1" && left=$((left + 1))
    done
    [ "$left" -eq "$n_opt" ] && ok "the $n_opt optional skills are left out and reported" || bad "$left of $n_opt optional skills left out and reported"
    if sh "$self" --all "$tmp/dest-all" > "$tmp/out-all" 2>&1; then
        good=0
        for name in $optional; do
            [ -L "$tmp/dest-all/$name" ] && [ "$(CDPATH= cd -- "$tmp/dest-all/$name" && pwd -P)" = "$(CDPATH= cd -- "$root/skills/$name" && pwd -P)" ] && good=$((good + 1))
        done
        [ "$good" -eq "$n_opt" ] && ok "--all links the $n_opt optional skills" || bad "--all linked $good of $n_opt optional skills"
    else bad "--all exited non-zero"; fi
    if [ ! -L "$tmp/dest/$keep" ] && [ "$(cat "$tmp/dest/$keep/local.md")" = mine ] && grep -q "^skip  $keep " "$tmp/out1"; then
        ok "a real directory of the same name is skipped, reported and left as it was"
    else bad "the real directory $keep was replaced or not reported"; fi
    # Point one link at the wrong skill first, so a second run that skipped
    # existing links would leave it wrong and fail here.
    moved=$(printf '%s\n' "$want" | grep -vx "$keep" | head -1)
    other=$(printf '%s\n' "$want" | grep -vx "$keep" | grep -vx "$moved" | head -1)
    rm -f "$tmp/dest/$moved" && ln -s "$root/skills/$other" "$tmp/dest/$moved"
    if sh "$self" "$tmp/dest" > "$tmp/out2" 2>&1 \
        && [ "$(CDPATH= cd -- "$tmp/dest/$moved" && pwd -P)" = "$(CDPATH= cd -- "$root/skills/$moved" && pwd -P)" ]; then
        ok "a second run replaces a wrong link with the right one and exits 0"
    else bad "the second run failed or left $moved pointing at $other"; fi
    mkdir -p "$tmp/fake/scripts" && cp "$self" "$tmp/fake/scripts/"
    if sh "$tmp/fake/scripts/$(basename -- "$self")" "$tmp/dest2" > "$tmp/out3" 2>&1; then
        bad "a tree with no skills/ exited 0"
    else grep -q 'no skills directory' "$tmp/out3" && ok "a tree with no skills/ exits non-zero and says why" || bad "no skills/ failed without its message"; fi
    # --dry-run must print the plan but create nothing, not even the directory.
    if sh "$self" --dry-run "$tmp/dryrun-dest" > "$tmp/out4" 2>&1; then
        if [ -e "$tmp/dryrun-dest" ]; then
            bad "--dry-run created $tmp/dryrun-dest"
        elif grep -q "^Target directory: $tmp/dryrun-dest$" "$tmp/out4" \
            && grep -q "would link  $keep" "$tmp/out4" \
            && grep -q "^dry-run: nothing written$" "$tmp/out4"; then
            ok "--dry-run prints the target and the plan, and writes nothing"
        else bad "--dry-run did not print the expected plan: $(cat "$tmp/out4")"; fi
    else bad "--dry-run exited non-zero"; fi
    # A normal run must print the plan before it writes its first link or skip.
    rm -rf "$tmp/order-dest"
    sh "$self" "$tmp/order-dest" > "$tmp/out5" 2>&1 || true
    plan_line=$(grep -n '^Target directory:' "$tmp/out5" | head -1 | cut -d: -f1)
    write_line=$(grep -nE '^(link|skip)  ' "$tmp/out5" | head -1 | cut -d: -f1)
    if [ -n "$plan_line" ] && [ -n "$write_line" ] && [ "$plan_line" -lt "$write_line" ]; then
        ok "the plan is printed before any link or skip line"
    else bad "the plan did not print before writing"; fi
    # --base must link every skill but house-preferences, and leave it out.
    if sh "$self" --base "$tmp/base-dest" > "$tmp/out6" 2>&1; then
        nb=0
        for name in $want; do
            [ "$name" = house-preferences ] && continue
            [ -L "$tmp/base-dest/$name" ] && nb=$((nb + 1))
        done
        if [ -e "$tmp/base-dest/house-preferences" ] || [ -L "$tmp/base-dest/house-preferences" ]; then
            bad "--base linked house-preferences"
        elif [ "$nb" -ne $((n - 1)) ]; then
            bad "--base linked $nb of $((n - 1)) base skills"
        elif ! grep -q "^omit  house-preferences (--base)$" "$tmp/out6"; then
            bad "--base did not report house-preferences as omitted"
        else ok "--base links the $((n - 1)) base skills, omits house-preferences and says so"; fi
    else bad "--base exited non-zero"; fi
    [ "$fails" -eq 0 ] && { echo "link-skills: selftest passed"; exit 0; }
    echo "link-skills: selftest FAILED ($fails)"; exit 1
fi

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
src="$repo_root/skills"

dry_run=0
all=0
base=0
dest=""
for arg in "$@"; do
    case "$arg" in
        --dry-run) dry_run=1 ;;
        --all) all=1 ;;
        --base) base=1 ;;
        -*) echo "error: unknown option $arg" >&2; exit 2 ;;
        *) dest=$arg ;;
    esac
done
dest=${dest:-$HOME/.claude/skills}

if [ ! -d "$src" ]; then
    echo "error: no skills directory at $src" >&2
    exit 1
fi

# is_optional NAME: NAME is on the list above and --all was not given.
is_optional() { [ "$all" -eq 0 ] && printf '%s\n' "$optional" | grep -qxF "$1"; }
# The maintainer's own layer over working-preferences. --base leaves it out;
# an existing link to it in the target is left as it is.
omitted() {
    [ "$base" -eq 1 ] && [ "$1" = house-preferences ]
}

echo "Target directory: $dest"
plan_linked=0
plan_skipped=0
for d in "$src"/*/; do
    [ -d "$d" ] || continue
    name=$(basename "$d")
    target="$dest/$name"
    if is_optional "$name"; then
        echo "  would skip  $name (optional; --all links it)"
        plan_skipped=$((plan_skipped + 1))
    elif omitted "$name"; then
        echo "  would omit  $name (--base)"
    elif [ -e "$target" ] && [ ! -L "$target" ]; then
        echo "  would skip  $name (a real directory is already there)"
        plan_skipped=$((plan_skipped + 1))
    else
        echo "  would link  $name"
        plan_linked=$((plan_linked + 1))
    fi
done
echo "$plan_linked to link, $plan_skipped to skip"

if [ "$dry_run" -eq 1 ]; then
    echo "dry-run: nothing written"
    exit 0
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
optional_n=0

for d in "$src"/*/; do
    [ -d "$d" ] || continue
    name=$(basename "$d")
    target="$dest/$name"

    if is_optional "$name"; then
        echo "skip  $name (optional; --all links it)"
        optional_n=$((optional_n + 1))
        continue
    fi
    if omitted "$name"; then
        echo "omit  $name (--base)"
        continue
    fi

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

if [ "$optional_n" -gt 0 ]; then
    echo "$optional_n optional skills not linked; --all links them."
fi
if [ "$skipped" -gt 0 ]; then
    echo "Skipped entries are real directories. Move or delete them, then re-run."
fi
