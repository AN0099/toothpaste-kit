#!/usr/bin/env sh

# SPDX-FileCopyrightText: 2026 Aidan Naveja
#
# SPDX-License-Identifier: Apache-2.0

# Compliance checks that need a tool from outside this repository.
#
# scripts/gates.sh needs nothing but sh and python3, so a fresh clone can run
# every gate at once. Checks that depend on an installed linter live here
# instead, which keeps the gates runnable everywhere and gives each external
# tool one place to be named, pinned and explained.
#
# Coverage: REUSE compliance via `reuse lint`, which checks that every file
# declares a copyright and a licence and that each licence named has its text
# in LICENSES/. It does NOT check that a declaration is true: a passing lint is
# not an ownership clearance.
#
# A tool that is not installed is reported as SKIP, not checked, and never
# counted as a pass. CI runs with --require, so there a missing tool fails.
#
# Usage: scripts/compliance.sh                       run every check
#        scripts/compliance.sh --selftest            show each check can fire, then run them
#        scripts/compliance.sh --require [--selftest] a missing tool fails
#
# --selftest first runs this script's own logic against a stand-in reuse
# (check_harness below), so the counts, verdicts, exit codes and the plant are
# shown to work on a seat without reuse installed. Nothing here calls this
# script from scripts/gates.sh, so this harness is its only oracle.
#
# Install the linter: pipx install reuse==6.2.0 (the version CI pins in
# .github/workflows/compliance.yml).

cd "$(dirname "$0")/.." || exit 1

selftest=0
require=0
for arg in "$@"; do
  case "$arg" in
    --selftest) selftest=1 ;;
    --require)  require=1 ;;
    *) printf 'compliance: unknown argument %s\n' "$arg" >&2; exit 2 ;;
  esac
done

fail=0
pass_n=0
skip_n=0
total=0

check_start() { printf '\n== %s ==\n' "$1"; total=$((total + 1)); }
check_ok()    { printf 'PASS  %s\n' "$1"; pass_n=$((pass_n + 1)); }
check_bad()   { printf 'FAIL  %s\n' "$1"; fail=1; }
check_skip()  {
  if [ "$require" -eq 1 ]; then
    printf 'FAIL  %s: %s is not installed, and --require is set\n' "$1" "$2"; fail=1
  else
    printf 'SKIP  %s: %s is not installed, so this is NOT checked (%s)\n' "$1" "$2" "$3"
    skip_n=$((skip_n + 1))
  fi
}

# The tracked and new files, copied to a scratch root, so a plant never
# touches the working tree. Ignored files are left out, as reuse would.
copy_tree() {
  git ls-files -z --cached --others --exclude-standard \
    | tar --null -T - -cf - | tar -xf - -C "$1"
}

check_reuse() {
  check_start "REUSE compliance"
  if ! command -v reuse >/dev/null 2>&1; then
    check_skip "REUSE compliance" reuse "pipx install reuse==6.2.0"
    return
  fi
  if [ "$selftest" -eq 1 ]; then
    scratch=$(mktemp -d) || { check_bad "REUSE compliance: no scratch directory"; return; }
    copy_tree "$scratch" || { check_bad "REUSE compliance: copy failed"; return; }
    if ! reuse --root "$scratch" lint >/dev/null 2>&1; then
      printf 'PLANT FAIL  reuse rejected the clean copy, so a non-zero on the plant proves nothing\n'
      check_bad "REUSE compliance"; return
    fi
    printf 'no declaration here\n' > "$scratch/planted-undeclared.txt"
    if reuse --root "$scratch" lint >/dev/null 2>&1; then
      printf 'PLANT FAIL  reuse passed a file with no declaration\n'
      check_bad "REUSE compliance"; return
    fi
    printf 'PLANT ok    reuse rejects a file with no declaration and accepts the clean copy\n'
  fi
  if reuse lint; then
    check_ok "REUSE compliance"
  else
    check_bad "REUSE compliance"
  fi
}

# The harness: run this script in a scratch repository, with PATH holding only
# the tools it needs and a stand-in reuse, and check each outcome's exit code
# and lines. In mode "good" the stand-in passes only when the tree it lints
# holds the tracked and new files and no plant, and a --root copy also leaves
# the ignored file out; "pass" accepts everything and "fail" rejects
# everything. COMPLIANCE_HARNESS
# stops the inner runs from running the harness again.
check_harness() {
  check_start "compliance.sh harness"
  h=$(mktemp -d) || { check_bad "compliance.sh harness: no scratch directory"; return; }
  mkdir -p "$h/bin" "$h/bin-noreuse" "$h/repo/scripts" "$h/elsewhere" || { check_bad "compliance.sh harness: mkdir failed"; return; }
  for tool in sh git tar mktemp dirname; do
    tp=$(command -v "$tool") || { check_bad "compliance.sh harness: $tool not found"; return; }
    ln -s "$tp" "$h/bin/$tool"; ln -s "$tp" "$h/bin-noreuse/$tool"
  done
  cat > "$h/bin/reuse" <<'STUB'
#!/bin/sh
root=. last=
while [ $# -gt 0 ]; do
  case "$1" in --root) root=$2; shift ;; esac
  last=$1; shift
done
[ "$last" = lint ] || exit 3
case "$FAKE_REUSE" in pass) exit 0 ;; fail) exit 1 ;; esac
# The working tree holds the ignored file, as a real one would; reuse skips it
# there, but a --root copy must not hold it.
[ "$root" = . ] || [ ! -e "$root/ignored.txt" ] || exit 1
[ -e "$root/tracked.txt" ] && [ -e "$root/new.txt" ] && [ ! -e "$root/planted-undeclared.txt" ]
STUB
  chmod +x "$h/bin/reuse"
  cat scripts/compliance.sh > "$h/repo/scripts/compliance.sh" || { check_bad "compliance.sh harness: copy failed"; return; }
  ( cd "$h/repo" && export GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null &&
    git init -q && printf 'ignored.txt\n' > .gitignore && printf 't\n' > tracked.txt &&
    git add .gitignore tracked.txt scripts/compliance.sh &&
    git -c user.name=harness -c user.email=harness@invalid commit -qm harness &&
    printf 'n\n' > new.txt && printf 'i\n' > ignored.txt ) \
    || { check_bad "compliance.sh harness: scratch repository failed"; return; }
  h_bad=0
  # hcase BIN MODE "ARGS" RC LINE...: run from a directory that is not the
  # repository root, so the script must find its own root.
  hcase() {
    hb=$1 hm=$2 ha=$3 hrc=$4; shift 4
    hout=$(cd "$h/elsewhere" && COMPLIANCE_HARNESS=1 FAKE_REUSE=$hm GIT_CONFIG_NOSYSTEM=1 \
      GIT_CONFIG_GLOBAL=/dev/null PATH="$h/$hb" sh ../repo/scripts/compliance.sh $ha 2>&1)
    hgot=$?
    hwhy=
    [ "$hgot" -eq "$hrc" ] || hwhy="exit $hgot, want $hrc"
    for hl in "$@"; do
      case "$hout" in *"$hl"*) ;; *) hwhy="${hwhy:+$hwhy; }no line '$hl'" ;; esac
    done
    if [ -n "$hwhy" ]; then
      printf 'PLANT FAIL  harness %s %s [%s]: %s\n' "$hb" "$hm" "$ha" "$hwhy"; h_bad=1
    fi
    if [ -e "$h/repo/planted-undeclared.txt" ]; then
      printf 'PLANT FAIL  harness %s %s [%s]: plant left in the tree\n' "$hb" "$hm" "$ha"; h_bad=1
      rm -f "$h/repo/planted-undeclared.txt"
    fi
  }
  hcase bin-noreuse good "" 0 \
    "SKIP  REUSE compliance: reuse is not installed, so this is NOT checked (pipx install reuse==6.2.0)" \
    "0 of 1 checks passed, 1 not checked" "compliance: incomplete, 1 check(s) not run"
  hcase bin-noreuse good "--require" 1 \
    "FAIL  REUSE compliance: reuse is not installed, and --require is set" \
    "0 of 1 checks passed, 0 not checked" "compliance: FAILED"
  hcase bin good "" 0 "PASS  REUSE compliance" "1 of 1 checks passed, 0 not checked" "compliance: all passed"
  hcase bin good "--selftest --require" 0 \
    "PLANT ok    reuse rejects a file with no declaration and accepts the clean copy" \
    "PASS  REUSE compliance" "1 of 1 checks passed, 0 not checked" "compliance: all passed"
  hcase bin fail "" 1 "FAIL  REUSE compliance" "0 of 1 checks passed, 0 not checked" "compliance: FAILED"
  hcase bin fail "--selftest" 1 "PLANT FAIL  reuse rejected the clean copy" "compliance: FAILED"
  hcase bin pass "--selftest" 1 "PLANT FAIL  reuse passed a file with no declaration" "compliance: FAILED"
  hcase bin good "--bogus" 2 "compliance: unknown argument --bogus"
  case "$hout" in *"checks passed"*) printf 'PLANT FAIL  harness: an unknown argument still ran the checks\n'; h_bad=1 ;; esac
  if [ "$h_bad" -eq 0 ]; then
    printf 'PLANT ok    harness: 8 runs against a stand-in reuse gave the expected exit codes and lines\n'
    check_ok "compliance.sh harness"
    rm -rf "$h"
  else
    check_bad "compliance.sh harness"
    # Exit here, not through the verdict below: a broken fail flag or exit
    # code is among what the harness catches, and would hide its own failure.
    rm -rf "$h"
    printf 'compliance: FAILED, the harness shows this script is broken\n'; exit 1
  fi
}

if [ "$selftest" -eq 1 ] && [ -z "${COMPLIANCE_HARNESS:-}" ]; then
  check_harness
fi

check_reuse

printf '\n%s of %s checks passed, %s not checked\n' "$pass_n" "$total" "$skip_n"
if [ "$fail" -ne 0 ]; then
  printf 'compliance: FAILED\n'; exit 1
fi
if [ "$skip_n" -ne 0 ]; then
  printf 'compliance: incomplete, %s check(s) not run\n' "$skip_n"; exit 0
fi
printf 'compliance: all passed\n'
