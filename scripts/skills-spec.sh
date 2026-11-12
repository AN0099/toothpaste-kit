#!/usr/bin/env sh

# SPDX-FileCopyrightText: 2026 Aidan Naveja
#
# SPDX-License-Identifier: Apache-2.0

# Validates every skill under skills/ against the Agent Skills specification,
# with its reference validator, skills-ref 0.1.1, whose command is
# agentskills. The verification image pins it by hash
# (containers/verify/requirements.txt).
#
# Coverage: what skills-ref checks, which is the frontmatter of each SKILL.md:
# that name and description are present, the name's length, case and
# characters and that it matches its directory, the description's and
# compatibility's lengths, and that no top-level field is outside the six the
# specification defines. It does NOT read a skill's body, its scripts or its
# references, and it checks no rule this kit adds; scripts/gates.sh holds
# those. skills-ref 0.1.1 ends the frontmatter at the first --- anywhere in
# it, inside a value too, so a field after such a --- is not checked; no
# skill here has one.
#
# One exception, stated rather than hidden. The eight skills a person invokes
# set disable-model-invocation, a Claude Code field the specification does not
# define, so skills-ref rejects it. Those eight are listed below and validated
# as a copy with that one line removed from the frontmatter. The copy loses
# only that exact line, so skills-ref still sees any other field, and a copy
# that loses more than one line fails. A skill that sets the field and is not
# listed fails, and so does a listed skill that does not set it or has no
# directory.
#
# A missing tool fails the script and names it, as in scripts/schemas.sh: a
# "not checked" line has been read as a pass.
#
# Usage: scripts/skills-spec.sh              validate every skill
#        scripts/skills-spec.sh --selftest   first show the check rejects a
#                                            planted bad name, a missing
#                                            description, an unknown field, a
#                                            listing error each way, a copy
#                                            that lost more than the field line
#                                            and a missing tool, each for its
#                                            reason
#
# Run it in the verification container, which holds the tool:
#   containers/verify/verify . ./scripts/skills-spec.sh --selftest
#
# SKILLS_REF names the validator command, default agentskills; the selftest
# sets it to a name that is not installed, to show the missing-tool case.
# SKILLS_DIR names the skills directory, default skills.

self=$(cd "$(dirname "$0")" && pwd -P)/$(basename "$0")
cd "$(dirname "$0")/.." || exit 1

selftest=0
for arg in "$@"; do
  case "$arg" in
    --selftest) selftest=1 ;;
    *) printf 'skills-spec: unknown argument %s\n' "$arg" >&2; exit 2 ;;
  esac
done

ref=${SKILLS_REF:-agentskills}
skills_dir=${SKILLS_DIR:-skills}

# The skills a person invokes, which set the Claude Code field. A change here
# is a change to the table of those skills in README.md.
claude_field='disable-model-invocation: true'
claude_only='daily-dashboard
daily-review
merge-proxy
monthly-review
redaction-gate
session-close
session-log
weekly-review'

fail=0
pass_n=0
total=0

check_start() { printf '\n== %s ==\n' "$1"; total=$((total + 1)); }
check_ok()    { printf 'PASS  %s\n' "$1"; pass_n=$((pass_n + 1)); }
check_bad()   { printf 'FAIL  %s\n' "$1"; fail=1; }

tool_ok() {
  command -v "$1" >/dev/null 2>&1 || { printf 'skills-spec: %s is not installed; run in the verification container\n' "$1"; return 1; }
}

listed() { printf '%s\n' "$claude_only" | grep -qxF "$1"; }

# list_present DIR: every listed skill has DIR/NAME/SKILL.md, so a listed skill
# renamed or removed fails rather than passing with one copy fewer.
list_present() {
  lbad=0
  for name in $claude_only; do
    [ -f "$1/$name/SKILL.md" ] && continue
    printf 'skills-spec: %s is listed but %s/%s/SKILL.md does not exist\n' "$name" "$1" "$name"
    lbad=1
  done
  return "$lbad"
}

# has_field FILE: the frontmatter, between the first two --- lines, holds the
# Claude Code field.
has_field() {
  # exit inside a rule still runs END, so the answer is a flag END reads.
  awk -v f="$claude_field" 'NR == 1 && $0 == "---" { fm = 1; next }
    fm && $0 == "---" { exit } fm && $0 == f { hit = 1; exit } END { exit !hit }' "$1"
}

# strip FILE: FILE with the field's line removed from the frontmatter only.
strip() {
  awk -v f="$claude_field" 'NR == 1 && $0 == "---" { fm = 1; print; next }
    fm && $0 == "---" { fm = 0 } fm && $0 == f { next } { print }' "$1"
}

# validate_all DIR: every DIR/*/SKILL.md passes skills-ref, the listed ones as
# a stripped copy. Prints each failure and the count checked.
validate_all() {
  tool_ok "$ref" || return 1
  t=$(mktemp -d) || { printf 'skills-spec: no scratch directory\n'; return 1; }
  vbad=0
  n=0
  copies=0
  for f in "$1"/*/SKILL.md; do
    [ -f "$f" ] || continue
    d=$(dirname "$f"); name=$(basename "$d")
    n=$((n + 1))
    if listed "$name"; then
      if ! has_field "$f"; then
        printf 'skills-spec: %s is listed as a Claude Code skill but does not set the exact line %s\n' "$name" "$claude_field"
        vbad=1; continue
      fi
      if ! { mkdir "$t/$name" && strip "$f" > "$t/$name/SKILL.md"; }; then
        printf 'skills-spec: %s: could not write the copy\n' "$name"; vbad=1; continue
      fi
      removed=$(diff "$f" "$t/$name/SKILL.md" | grep -c '^[<>]')
      if [ "$removed" -ne 1 ]; then
        printf 'skills-spec: %s: the copy differs by %s lines, not the one field line\n' "$name" "$removed"
        vbad=1; continue
      fi
      target=$t/$name
      copies=$((copies + 1))
    else
      if has_field "$f"; then
        printf 'skills-spec: %s sets %s and is not listed in this script\n' "$name" "$claude_field"
        vbad=1; continue
      fi
      target=$d
    fi
    "$ref" validate "$target" || vbad=1
  done
  rm -rf "$t"
  [ "$n" -gt 0 ] || { printf 'skills-spec: no skills found under %s\n' "$1"; return 1; }
  printf '  checked %s skills, %s of them as a copy without %s\n' "$n" "$copies" "$claude_field"
  return "$vbad"
}

# plant NAME WANT DIR: validating DIR must fail and print WANT. Any failure
# alone would also pass a plant rejected for some other reason.
plant() {
  if pout=$(validate_all "$3" 2>&1); then
    printf 'PLANT FAIL  %s was accepted\n' "$1"; plant_bad=1
  else
    case "$pout" in
      *"$2"*) printf 'PLANT ok    %s is rejected\n' "$1" ;;
      *) printf 'PLANT FAIL  %s was rejected without "%s"\n' "$1" "$2"; plant_bad=1 ;;
    esac
  fi
}

# fixture DIR NAME FRONTMATTER: DIR/NAME/SKILL.md with that frontmatter.
fixture() {
  mkdir -p "$1/$2" && printf -- '---\n%s\n---\n\n# Body\n' "$3" > "$1/$2/SKILL.md"
}

selftest_run() {
  check_start "skills-spec selftest"
  s=$(mktemp -d) || { check_bad "skills-spec selftest: no scratch directory"; return; }
  plant_bad=0
  # A clean pass first, a plain skill and a listed one, or a rejected plant
  # proves nothing.
  fixture "$s/ok" plain 'name: plain
description: A plain skill.'
  fixture "$s/ok" session-log "name: session-log
description: A listed skill.
$claude_field"
  if ! validate_all "$s/ok" >/dev/null 2>&1; then
    printf 'PLANT FAIL  a clean tree was rejected, so a rejected plant proves nothing\n'
    check_bad "skills-spec selftest"; rm -rf "$s"; return
  fi
  fixture "$s/case" Bad-Name 'name: Bad-Name
description: A name in capitals.'
  plant "a name in capitals" "Skill name 'Bad-Name' must be lowercase" "$s/case"
  fixture "$s/desc" nodesc 'name: nodesc'
  plant "a missing description" 'Missing required field in frontmatter: description' "$s/desc"
  fixture "$s/field" extra 'name: extra
description: An unknown field.
planted: true'
  plant "an unknown field" 'Unexpected fields in frontmatter: planted' "$s/field"
  fixture "$s/second" session-log "name: session-log
description: A listed skill with a second unknown field.
$claude_field
planted: true"
  plant "a listed skill with a second unknown field" 'Unexpected fields in frontmatter: planted' "$s/second"
  fixture "$s/unlisted" unlisted "name: unlisted
description: Sets the field, not listed.
$claude_field"
  plant "the field on a skill not listed" 'unlisted sets disable-model-invocation: true and is not listed' "$s/unlisted"
  fixture "$s/stale" session-log 'name: session-log
description: Listed, does not set the field.'
  plant "a listed skill without the field" 'session-log is listed as a Claude Code skill but does not set' "$s/stale"
  fixture "$s/twice" session-log "name: session-log
description: The field written twice, so the copy loses two lines.
$claude_field
$claude_field"
  plant "a copy that differs by more than the field line" 'the copy differs by 2 lines' "$s/twice"
  # The list against the tree: the clean tree holds one of the eight.
  if pout=$(list_present "$s/ok" 2>&1); then
    printf 'PLANT FAIL  a listed skill with no directory was accepted\n'; plant_bad=1
  else
    case "$pout" in
      *"daily-dashboard is listed but $s/ok/daily-dashboard/SKILL.md does not exist"*)
        printf 'PLANT ok    a listed skill with no directory is rejected\n' ;;
      *) printf 'PLANT FAIL  a listed skill with no directory was rejected without its message\n'; plant_bad=1 ;;
    esac
  fi
  # A missing tool fails the whole script and names it.
  mout=$(env SKILLS_REF=skills-spec-selftest-not-installed sh "$self" 2>&1); mcode=$?
  case "$mcode:$mout" in
    1:*"skills-spec-selftest-not-installed is not installed"*) printf 'PLANT ok    a missing SKILLS_REF fails, exit 1, naming it\n' ;;
    *) printf 'PLANT FAIL  a missing SKILLS_REF gave exit %s, not 1 naming the tool\n' "$mcode"; plant_bad=1 ;;
  esac
  rm -rf "$s"
  if [ "$plant_bad" -eq 0 ]; then check_ok "skills-spec selftest"; else check_bad "skills-spec selftest"; fi
}

[ "$selftest" -eq 0 ] || selftest_run

check_start "skills against the Agent Skills specification, skills-ref 0.1.1"
if validate_all "$skills_dir" && list_present "$skills_dir"; then check_ok "skills"; else check_bad "skills"; fi

printf '\n%s of %s checks passed\n' "$pass_n" "$total"
if [ "$fail" -ne 0 ]; then
  printf 'skills-spec: FAILED\n'; exit 1
fi
printf 'skills-spec: all passed\n'
