#!/usr/bin/env sh
# SPDX-FileCopyrightText: 2026 Aidan Naveja
#
# SPDX-License-Identifier: Apache-2.0
# Builds the review-round fixture's Git history in a fresh repository.
#
# The history is two commits, each made from a numbered patch file in this
# directory: 0001-baseline.patch and 0002-proposed-change.patch. Author,
# committer and dates are fixed, and the user's Git configuration is not read,
# so the commit hashes are the same on every run and every machine. They are
# compared with revisions.json, which the round packet's baseRevision and
# targetRevision copy.
#
# The patches are applied to a repository outside this one, never inside it:
# a nested .git in the kit is what the patch-file packaging avoids.
#
# Usage: build.sh [DIR]   build into DIR, which must not exist yet;
#                         without DIR, into a new temporary directory
# Prints the directory and both revisions. Exit 0 when the hashes match
# revisions.json, 1 when they drift, 2 on a usage or setup problem.
# Needs git and nothing else: no network, no account.
set -eu

here=$(cd "$(dirname "$0")" && pwd)
if [ $# -gt 1 ]; then
    echo "usage: build.sh [DIR]" >&2
    exit 2
fi
if [ $# -eq 1 ]; then
    if [ -e "$1" ]; then
        echo "build.sh: $1 already exists; give a path that does not" >&2
        exit 2
    fi
    mkdir -p "$1"
    dir=$(cd "$1" && pwd)
else
    dir=$(mktemp -d "${TMPDIR:-/tmp}/review-round-fixture.XXXXXX")
fi

# Ignore the user's and the system's Git configuration: hooks, signing,
# templates and line-ending settings would change the commits or their hashes.
GIT_CONFIG_GLOBAL=/dev/null
GIT_CONFIG_NOSYSTEM=1
GIT_AUTHOR_NAME=Fixture
GIT_AUTHOR_EMAIL=fixture@example.invalid
GIT_COMMITTER_NAME=Fixture
GIT_COMMITTER_EMAIL=fixture@example.invalid
export GIT_CONFIG_GLOBAL GIT_CONFIG_NOSYSTEM GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL \
    GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL

git -C "$dir" -c init.defaultBranch=main init -q --template=
commit() {
    git -C "$dir" apply --whitespace=nowarn "$here/$1"
    git -C "$dir" add -A
    GIT_AUTHOR_DATE=$2 GIT_COMMITTER_DATE=$2 git -C "$dir" commit -q -m "$3"
}
commit 0001-baseline.patch 2026-01-01T00:00:00Z "Baseline: tally and its built-in checks"
commit 0002-proposed-change.patch 2026-01-02T00:00:00Z "Add --lines and document the pre-push check"

base=$(git -C "$dir" rev-parse HEAD~1)
target=$(git -C "$dir" rev-parse HEAD)
echo "fixture repository: $dir"
echo "baseRevision:   $base"
echo "targetRevision: $target"
want() { sed -n "s/.*\"$1\": *\"\([0-9a-f]*\)\".*/\1/p" "$here/revisions.json"; }
if [ "$base" != "$(want baseRevision)" ] || [ "$target" != "$(want targetRevision)" ]; then
    echo "::error::build.sh: the built revisions differ from revisions.json; the patches, dates or messages changed" >&2
    exit 1
fi
echo "build.sh: revisions match revisions.json"
