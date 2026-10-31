#!/usr/bin/env sh

# SPDX-FileCopyrightText: 2026 Aidan Naveja
#
# SPDX-License-Identifier: Apache-2.0

# Mechanical gates for this repository.
#
# One implementation, run from two places: `.github/workflows/gates.yml` in
# CI, and by hand before a push. That is deliberate. A gate whose CI copy and
# local copy are separate texts can diverge, and the divergence is invisible
# until a contributor's clean local run is rejected by CI. It also means a
# gate checked by typing its line is not the gate that is installed, which is
# the failure this repository's conventions single out.
#
# Every gate blocks. Two of them are stated in CONTRIBUTING.md as absolutes,
# and a warn-level implementation of a stated absolute weakens the rule it
# claims to enforce.
#
# Coverage, stated because a check that does not state its coverage is not a
# check. These seventeen gates cover: the em dash ban, the private task ID ban,
# JSON wellformedness, registry self-consistency (including every vendor
# file's shape against surface-descriptor.schema.json, checked by
# scripts/schema-check.py, which fails loudly on any schema keyword it does
# not implement rather than skip it), skill frontmatter (presence, and each
# description's length and one-line YAML scalar rules), the
# reflow script's own selftest, markdown structure via scripts/mdlint.py,
# which states its own nineteen-rule coverage in its header, and the example
# workspace's stubs against docs/standing-documents.md via
# scripts/check-workspace-stubs.py, which states its own coverage too, and
# the remote classifier's own selftest in scripts/remote-level.sh, and
# scripts/reorient's selftest, which runs it on examples/workspace as a second
# tree and against planted positives, and scripts/link-skills.sh's selftest,
# which links the skills into a temporary directory and checks each link, and
# the hooks/ rules' structure, regex validity and planted cases via
# scripts/check-hooks.py, which states its own coverage, including the branch
# name guard's cases in tests/branch-guard-cases.tsv, and the branch and tag
# name rule's selftest in scripts/check-branch-name, which also fails if the
# ruleset's prefix list has drifted from the script's, and the commit-msg
# hook's attribution, provenance and sign-off rules against
# tests/attribution-cases.tsv and three sign-off cases, and the
# question block checker's selftest in scripts/check-qblock against
# tests/qblock-cases/, which states its own eight-rule coverage, and the pull
# request body checker's selftest in scripts/check-pr-body, which plants each
# finding it reports, and the SPDX fragment builder's selftest in
# scripts/spdx-fragment.py, which builds fragments from commits in a scratch
# repository and checks each models file rule. They
# do NOT cover: en dashes (ranges and clause separators are not mechanically
# separable, so that stays a review prompt), prose quality, internal link
# validity, whether a skill's Scope Pointer is last, or whether any document's
# claims are true.
#
# Usage: scripts/gates.sh            run every gate
#        scripts/gates.sh --selftest show each gate can fire, then run them

set -u

# Most gates run python3. Without it they fail with a message about the gate,
# not about python3, so say so once, before any gate runs.
if ! command -v python3 >/dev/null 2>&1; then
  echo "gates: python3 is not installed, and most gates need it. Install python3 and run again."
  exit 2
fi

fail=0
pass_n=0
gate_start() { printf '\n== %s ==\n' "$1"; }
gate_ok()    { printf 'PASS  %s\n' "$1"; pass_n=$((pass_n + 1)); }
gate_bad()   { printf 'FAIL  %s\n' "$1"; fail=1; }

EM=$(printf '\342\200\224')   # U+2014, built rather than typed so this file
                              # does not contain the character it forbids

# ---------------------------------------------------------------- 1
gate_em_dash() {
  gate_start "no em dashes"
  # Options before `--`: after it, --exclude-dir is read as a file name and
  # .git is searched. Exit 2 means grep could not run the search, and an
  # empty result from a search that never ran is not a pass.
  hits=$(grep -rl --exclude-dir=.git -- "$EM" . 2>&1); rc=$?
  if [ "$rc" -gt 1 ]; then
    printf '%s\n' "$hits" | sed 's/^/  /'
    echo "::error::grep could not run this gate (exit $rc)"
    gate_bad "no em dashes"
  elif [ -n "$hits" ]; then
    printf '%s\n' "$hits" | sed 's/^/  /'
    echo "::error::em dash found in the files listed above"
    echo "  Exempt by filename if a file must quote one; do not loosen the pattern."
    gate_bad "no em dashes"
  else
    gate_ok "no em dashes"
  fi
}

# ---------------------------------------------------------------- 2
gate_task_ids() {
  gate_start "no private task IDs"
  hits=$(grep -rnE --exclude-dir=.git '\b(P[0-9]+-[0-9]+|OPEN_[0-9]+)\b' . 2>&1); rc=$?
  if [ "$rc" -gt 1 ]; then
    printf '%s\n' "$hits" | sed 's/^/  /'
    echo "::error::grep could not run this gate (exit $rc)"
    gate_bad "no private task IDs"
  elif [ -n "$hits" ]; then
    printf '%s\n' "$hits" | sed 's/^/  /'
    echo "::error::private task ID format found in the lines above"
    echo "  This repo uses TK- ids only. A private-format id usually means"
    echo "  private context arrived with it, so check the whole sentence."
    gate_bad "no private task IDs"
  else
    gate_ok "no private task IDs"
  fi
}

# ---------------------------------------------------------------- 3
gate_json() {
  gate_start "every .json parses"
  bad=0
  for f in $(find . -path ./.git -prune -o -name '*.json' -print | sort); do
    if ! python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "$f" 2>/dev/null; then
      echo "::error file=$f::invalid JSON"
      bad=1
    fi
  done
  [ "$bad" -eq 0 ] && gate_ok "every .json parses" || gate_bad "every .json parses"
}

# ---------------------------------------------------------------- 4
gate_registry() {
  gate_start "registry entries are self-consistent"
  if python3 - <<'PY'
import glob, json, sys

def derive(c):
    if c["interface"] == "programmatic" and c["autonomy"] == "none":
        return "programmatic-contractual"
    if c["human_presence"] == "required":
        return "interactive-synchronous"
    return "autonomous-asynchronous"

bad = 0
files = [p for p in glob.glob("orchestration/registry/*.json")
         if not p.endswith("surface-descriptor.schema.json")]
for path in files:
    doc = json.load(open(path))
    for s in doc["surfaces"]:
        got = derive(s["capability"])
        if got != s["regime"]:
            print(f"::error file={path}::{s['id']} states regime "
                  f"{s['regime']}, capability derives {got}")
            bad += 1
        if not s["id"].startswith(doc["vendor"] + ":"):
            print(f"::error file={path}::{s['id']} is not under "
                  f"vendor namespace {doc['vendor']}")
            bad += 1
        if s["confidence"] == "verified" and not s["sources"]:
            print(f"::error file={path}::{s['id']} claims confidence "
                  f"'verified' with no sources")
            bad += 1
n = sum(len(json.load(open(p))["surfaces"]) for p in files)
print(f"  checked {n} surface entries across {len(files)} registry files")
sys.exit(1 if bad else 0)
PY
  then
    if python3 scripts/schema-check.py
    then gate_ok "registry entries are self-consistent"
    else gate_bad "registry entries are self-consistent"; fi
  else gate_bad "registry entries are self-consistent"; fi
}

# ---------------------------------------------------------------- 5
# The description is checked against the YAML rules for a one-line scalar
# rather than parsed, because the gates run on python3 alone and no YAML
# parser ships with it. A presence check passed skills/orient with an
# unquoted ": " that a strict loader rejects. Covers: at most 250 characters
# as written, one line, and for a plain value no ": " or trailing ":", no
# " #" (the rest is a comment), no leading indicator; a quoted value must
# close, may be followed by a comment, and is otherwise accepted. Does NOT
# cover block scalars, tags, anchors, or the name field's value. The
# selftest calls this same function.
check_descriptions() {
  python3 - "$@" <<'PY'
import re, sys
MAX = 250
def problems(v):
    p = []
    if len(v) > MAX: p.append("longer than %d characters (%d)" % (MAX, len(v)))
    if v[:1] == '"':
        if not re.fullmatch(r'"(?:[^"\\]|\\.)*"(?:\s+#.*)?', v): p.append("double quote not closed")
    elif v[:1] == "'":
        if not re.fullmatch(r"'(?:[^']|'')*'(?:\s+#.*)?", v): p.append("single quote not closed")
    elif not v: p.append("empty")
    else:
        if v[0] in ",[]{}#&*!|>%@`" or (v[0] in "-?:" and v[1:2] in ("", " ")):
            p.append("plain value starts with indicator %r" % v[0])
        if re.search(r":(\s|$)", v): p.append('plain value contains ": " (quote it, or use "; ")')
        if re.search(r"\s#", v): p.append('plain value contains " #", which starts a comment')
    return p
bad = 0
for f in sys.argv[1:]:
    lines = open(f, encoding="utf-8").read().split("\n")
    end = lines.index("---", 1) if lines[:1] == ["---"] and "---" in lines[1:] else 0
    for i in range(1, end):
        if not lines[i].startswith("description:"): continue
        p = problems(lines[i][len("description:"):].strip())
        # A blank line inside a plain value folds, so the value continues
        # past it: look at the next line that is not blank.
        nxt = next((l for l in lines[i + 1:end] if l.strip()), "")
        if nxt[:1] in (" ", "\t"):
            p.append("continues onto a second line")
        for m in p:
            print("::error file=%s,line=%d::frontmatter description %s" % (f, i + 1, m))
            bad = 1
sys.exit(bad)
PY
}

gate_frontmatter() {
  gate_start "skill frontmatter present and valid"
  bad=0
  n=0
  for f in skills/*/SKILL.md; do
    n=$((n + 1))
    head -6 "$f" | grep -q '^name:' || { echo "::error file=$f::missing frontmatter name"; bad=1; }
    head -6 "$f" | grep -q '^description:' || { echo "::error file=$f::missing frontmatter description"; bad=1; }
  done
  check_descriptions skills/*/SKILL.md || bad=1
  echo "  checked $n skills"
  [ "$bad" -eq 0 ] && gate_ok "skill frontmatter present and valid" || gate_bad "skill frontmatter present and valid"
}

# ---------------------------------------------------------------- 6
gate_reflow() {
  gate_start "reflow-md selftest"
  if python3 scripts/reflow-md.py --selftest; then
    gate_ok "reflow-md selftest"
  else
    gate_bad "reflow-md selftest"
  fi
}

# ---------------------------------------------------------------- 7
gate_markdown() {
  gate_start "markdown structure"
  if python3 scripts/mdlint.py .; then
    gate_ok "markdown structure"
  else
    gate_bad "markdown structure"
  fi
}

# ---------------------------------------------------------------- 8
gate_stubs() {
  gate_start "example workspace matches standing-documents.md"
  if python3 scripts/check-workspace-stubs.py; then
    gate_ok "example workspace matches standing-documents.md"
  else
    gate_bad "example workspace matches standing-documents.md"
  fi
}

# ---------------------------------------------------------------- 9
gate_remote_level() {
  gate_start "remote-level selftest"
  if bash scripts/remote-level.sh --selftest; then
    gate_ok "remote-level selftest"
  else
    gate_bad "remote-level selftest"
  fi
}

gate_link_skills() {
  gate_start "link-skills selftest"
  if sh scripts/link-skills.sh --selftest; then
    gate_ok "link-skills selftest"
  else
    gate_bad "link-skills selftest"
  fi
}

gate_hooks() {
  gate_start "hooks rules"
  if python3 scripts/check-hooks.py; then
    gate_ok "hooks rules"
  else
    gate_bad "hooks rules"
  fi
}

gate_reorient() {
  gate_start "reorient selftest"
  if bash scripts/reorient --selftest; then
    gate_ok "reorient selftest"
  else
    gate_bad "reorient selftest"
  fi
}

# ---------------------------------------------------------------- 13
gate_branch_names() {
  gate_start "branch and tag name rule"
  if sh scripts/check-branch-name --selftest; then
    gate_ok "branch and tag name rule"
  else
    gate_bad "branch and tag name rule"
  fi
}

# ---------------------------------------------------------------- 14
# Runs the hook itself, so the pattern tested is the one installed. ATTR_HOOK
# lets the selftest point it at a weakened copy.
gate_attribution() {
  gate_start "commit attribution hook"
  hook=${ATTR_HOOK:-.githooks/commit-msg}
  msg=$(mktemp) || { gate_bad "commit attribution hook: no scratch file"; return; }
  tab=$(printf '\t')
  n=0
  bad=0
  while IFS= read -r line || [ -n "$line" ]; do
    case "$line" in ''|'#'*) continue ;; esac
    want=${line%%"$tab"*}
    trailer=${line#*"$tab"}
    # %b splits a case of several trailers joined by \n into lines.
    printf 'subject\n\nbody\n\n%b\nSigned-off-by: Test Author <author@example.com>\n' "$trailer" > "$msg"
    if GIT_AUTHOR_NAME='Test Author' GIT_AUTHOR_EMAIL=author@example.com \
      sh "$hook" "$msg" >/dev/null 2>&1; then got=allow; else got=block; fi
    n=$((n + 1))
    if [ "$got" != "$want" ]; then
      printf '  wanted %s, got %s: %s\n' "$want" "$got" "$trailer"; bad=1
    fi
  done < tests/attribution-cases.tsv
  # The sign-off rule: the author's own line passes, another person's or none
  # fails.
  for c in 'allow:Signed-off-by: Test Author <author@example.com>' \
           'block:Signed-off-by: Someone Else <else@example.com>' \
           'block:no sign-off'; do
    want=${c%%:*}
    printf 'subject\n\n%s\n' "${c#*:}" > "$msg"
    if GIT_AUTHOR_NAME='Test Author' GIT_AUTHOR_EMAIL=author@example.com \
      sh "$hook" "$msg" >/dev/null 2>&1; then got=allow; else got=block; fi
    n=$((n + 1))
    if [ "$got" != "$want" ]; then
      printf '  wanted %s, got %s: %s\n' "$want" "$got" "${c#*:}"; bad=1
    fi
  done
  rm -f "${msg:?}"
  printf '  %s cases\n' "$n"
  if [ "$n" -gt 0 ] && [ "$bad" -eq 0 ]; then
    gate_ok "commit attribution hook"
  else
    gate_bad "commit attribution hook"
  fi
}

# ---------------------------------------------------------------- 15
gate_qblock() {
  gate_start "question block checker"
  if python3 scripts/check-qblock --selftest; then
    gate_ok "question block checker"
  else
    gate_bad "question block checker"
  fi
}

# ---------------------------------------------------------------- 16
gate_pr_body() {
  gate_start "pull request body checker"
  if python3 scripts/check-pr-body --selftest >/dev/null; then
    gate_ok "pull request body checker"
  else
    gate_bad "pull request body checker"
  fi
}

# ---------------------------------------------------------------- 17
gate_spdx() {
  gate_start "spdx-fragment selftest"
  if python3 scripts/spdx-fragment.py --selftest; then
    gate_ok "spdx-fragment selftest"
  else
    gate_bad "spdx-fragment selftest"
  fi
}

run_all() {
  gate_em_dash
  gate_task_ids
  gate_json
  gate_registry
  gate_frontmatter
  gate_reflow
  gate_markdown
  gate_stubs
  gate_remote_level
  gate_reorient
  gate_link_skills
  gate_hooks
  gate_branch_names
  gate_attribution
  gate_qblock
  gate_pr_body
  gate_spdx
  printf '\n%s of 17 gates passed\n' "$pass_n"
  [ "$fail" -eq 0 ] || { echo "gates: FAILED"; return 1; }
  echo "gates: all passed"
  return 0
}

# A gate that has never returned a hit has not been shown capable of
# returning one, so each of the first five, and the eighth, is run against a
# planted positive in a scratch tree, as are 12, 13, 14, 15, 16 and 17. Gates 6, 9, 10 and
# 11 run their tools' own selftests, which carry their own planted cases, and
# gate 7 plants one positive per rule below.
run_selftest() {
  tmp=$(mktemp -d) || return 1
  # Each signal gets its own handler WITH an exit. A handler that only cleans
  # up returns to where the shell was interrupted, so the run continued against
  # a scratch tree that had just been deleted. Codes are the conventional
  # 128 plus the signal number.
  trap 'rm -rf "$tmp"' EXIT
  trap 'rm -rf "$tmp"; exit 130' INT
  trap 'rm -rf "$tmp"; exit 143' TERM
  plant_fail=0
  plant_n=0 # counted as the plants run, so the closing line cannot drift from the code
  # The two senses are opposite and conflating them reports backwards, which
  # is how the first draft of this selftest "failed" against gates that were
  # working. A search gate fires by FINDING the plant, so exit 0 is correct.
  # A validity gate fires by REJECTING the plant, so non-zero is correct.
  plant_found() {    # expects exit 0: the search found the planted positive
    plant_n=$((plant_n + 1))
    if [ "$1" -eq 0 ]; then
      printf 'PLANT ok    %s fires on a planted positive\n' "$2"
    else
      printf 'PLANT FAIL  %s did not find a planted positive\n' "$2"; plant_fail=1
    fi
  }
  # A validity gate fires by REJECTING the plant, so non-zero is correct. But
  # non-zero is also what a validator returns when it cannot open the file at
  # all, and those are not the same result. Checked: pointing the JSON and
  # frontmatter plants at a path that does not exist produced PLANT ok from
  # both. So a validity plant takes two exit codes, and the clean fixture is
  # what makes the rejection mean anything.
  plant_rejected() { # $1 exit on the bad fixture, $2 exit on the good one
    plant_n=$((plant_n + 1))
    if [ "$1" -ne 0 ] && [ "$2" -eq 0 ]; then
      printf 'PLANT ok    %s rejects a plant and accepts a clean fixture\n' "$3"
    elif [ "$1" -eq 0 ]; then
      printf 'PLANT FAIL  %s accepted a planted positive\n' "$3"; plant_fail=1
    else
      printf 'PLANT FAIL  %s rejected its own clean fixture, so the non-zero on the plant proves nothing\n' "$3"; plant_fail=1
    fi
  }

  # The two search gates run as installed, by calling their own functions in
  # a planted tree. A copy of a gate's grep line can fire while the line in
  # the gate is blind, which is what happened before this selftest called
  # them. The clean fixture holds the same plant inside .git, so it also
  # proves the .git exclusion works.
  run_gate() { ( cd "$1" && fail=0 && "$2" >/dev/null 2>&1; exit "$fail" ) }
  mkdir -p "$tmp/g-bad/.git" "$tmp/g-ok/.git"
  printf 'text %s text\n' "$EM" > "$tmp/g-bad/a.md"
  printf 'text %s text\n' "$EM" > "$tmp/g-ok/.git/a.md"
  run_gate "$tmp/g-bad" gate_em_dash; bad=$?
  run_gate "$tmp/g-ok" gate_em_dash
  plant_rejected $bad $? "em dash gate"

  # Assembled, for the same reason EM is: a literal here makes this file
  # itself a hit for the gate it is testing, and the real run then fails on
  # the test fixture rather than on the repository.
  rm -f "$tmp/g-bad/a.md" "$tmp/g-ok/.git/a.md"
  printf 'see P%s-%s for detail\n' 12 34 > "$tmp/g-bad/b.md"
  printf 'see P%s-%s for detail\n' 12 34 > "$tmp/g-ok/.git/b.md"
  run_gate "$tmp/g-bad" gate_task_ids; bad=$?
  run_gate "$tmp/g-ok" gate_task_ids
  plant_rejected $bad $? "private task ID gate"

  printf '{"unclosed": \n' > "$tmp/c.json"
  python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "$tmp/c.json" 2>/dev/null
  bad=$?
  printf '{"closed": true}\n' > "$tmp/c-ok.json"
  python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "$tmp/c-ok.json" 2>/dev/null
  plant_rejected $bad $? "JSON parse gate"

  # a registry file whose stated regime contradicts its own capability
  cat > "$tmp/r.json" <<'JSON'
{"vendor":"acme","surfaces":[{"id":"acme:x","regime":"interactive-synchronous",
 "capability":{"interface":"programmatic","autonomy":"none","human_presence":"optional"},
 "confidence":"verified","sources":[]}]}
JSON
  python3 - "$tmp/r.json" <<'PY' >/dev/null 2>&1
import json, sys
def derive(c):
    if c["interface"] == "programmatic" and c["autonomy"] == "none":
        return "programmatic-contractual"
    if c["human_presence"] == "required":
        return "interactive-synchronous"
    return "autonomous-asynchronous"
doc = json.load(open(sys.argv[1]))
bad = 0
for s in doc["surfaces"]:
    if derive(s["capability"]) != s["regime"]: bad += 1
    if s["confidence"] == "verified" and not s["sources"]: bad += 1
sys.exit(1 if bad else 0)
PY
  bad=$?

  # The same validator against an entry whose regime does match its capability.
  cat > "$tmp/r-ok.json" <<'JSON'
{"vendor":"acme","surfaces":[{"id":"acme:x","regime":"programmatic-contractual",
 "capability":{"interface":"programmatic","autonomy":"none","human_presence":"optional"},
 "confidence":"verified","sources":["https://example.com/doc"]}]}
JSON
  python3 - "$tmp/r-ok.json" <<'PY' >/dev/null 2>&1
import json, sys
def derive(c):
    if c["interface"] == "programmatic" and c["autonomy"] == "none":
        return "programmatic-contractual"
    if c["human_presence"] == "required":
        return "interactive-synchronous"
    return "autonomous-asynchronous"
doc = json.load(open(sys.argv[1]))
bad = 0
for s in doc["surfaces"]:
    if derive(s["capability"]) != s["regime"]: bad += 1
    if s["confidence"] == "verified" and not s["sources"]: bad += 1
sys.exit(1 if bad else 0)
PY
  plant_rejected $bad $? "registry consistency gate"

  # schema-check.py validates every registry vendor file against
  # surface-descriptor.schema.json. The plant breaks a vendor file's shape
  # (sources as a string, not an array), not the schema.
  for d in sc-bad sc-ok; do
    mkdir -p "$tmp/$d/orchestration/registry" "$tmp/$d/orchestration/schemas" "$tmp/$d/scripts"
    cp orchestration/registry/surface-descriptor.schema.json "$tmp/$d/orchestration/registry/"
    cp orchestration/schemas/event-base.json "$tmp/$d/orchestration/schemas/"
    cp scripts/schema-check.py "$tmp/$d/scripts/"
  done
  cat > "$tmp/sc-bad/orchestration/registry/acme.json" <<'JSON'
{"vendor":"acme","surfaces":[{"id":"acme:x","display_name":"X",
 "capability":{"interface":"programmatic","autonomy":"none","human_presence":"optional",
 "workspace":"none","tool_execution":"none","egress":"local","audit":"unknown"},
 "regime":"programmatic-contractual","confidence":"derived","verified_on":"2026-10-27",
 "sources":"not-an-array"}]}
JSON
  cat > "$tmp/sc-ok/orchestration/registry/acme.json" <<'JSON'
{"vendor":"acme","surfaces":[{"id":"acme:x","display_name":"X",
 "capability":{"interface":"programmatic","autonomy":"none","human_presence":"optional",
 "workspace":"none","tool_execution":"none","egress":"local","audit":"unknown"},
 "regime":"programmatic-contractual","confidence":"derived","verified_on":"2026-10-27",
 "sources":[]}]}
JSON
  ( cd "$tmp/sc-bad" && python3 scripts/schema-check.py ) >/dev/null 2>&1
  bad=$?
  ( cd "$tmp/sc-ok" && python3 scripts/schema-check.py ) >/dev/null 2>&1
  plant_rejected $bad $? "schema-check gate"

  mkdir -p "$tmp/skills/nofm" "$tmp/skills/withfm"
  printf -- '---\ndescription: has no name\n---\n' > "$tmp/skills/nofm/SKILL.md"
  head -6 "$tmp/skills/nofm/SKILL.md" | grep -q '^name:'
  bad=$?
  printf -- '---\nname: withfm\ndescription: has one\n---\n' > "$tmp/skills/withfm/SKILL.md"
  head -6 "$tmp/skills/withfm/SKILL.md" | grep -q '^name:'
  plant_rejected $bad $? "frontmatter gate"

  # One plant per description rule, each against the same clean fixture, which
  # holds one passing case per allowed form. A rule that stopped firing fails
  # its own line here rather than hiding behind another rule's plant.
  fm() { printf -- '---\nname: x\ndescription: %s\n---\n' "$2" > "$tmp/$1.md"; }
  {
    printf -- '---\nname: ok\ndescription: plain text, a:b and a#b, see sibling\n'
    printf 'description: "quoted: with \\" escaped # inside" # and a comment\n'
    printf "description: 'single: it''s fine'\n"
    printf 'description: -leading dash word\n'
    printf 'description: %0250d\n---\n' 0
  } > "$tmp/fm-ok.md"
  check_descriptions "$tmp/fm-ok.md" >/dev/null; good=$?
  fm long "$(printf '%0251d' 0)"
  fm colon 'index of things: with a colon'
  fm colonend 'ends with a colon:'
  fm hash 'text # then a comment'
  fm indicator '&anchor-looking start'
  fm dquote '"never closed'
  fm squote "'it's not doubled'"
  printf -- '---\nname: x\ndescription: first line\n  second line\n---\n' > "$tmp/multi.md"
  printf -- '---\nname: x\ndescription: first line\n\n  after a blank line\n---\n' > "$tmp/multiblank.md"
  for p in long colon colonend hash indicator dquote squote multi multiblank; do
    check_descriptions "$tmp/$p.md" >/dev/null; bad=$?
    plant_rejected $bad $good "frontmatter description: $p"
  done
  # The rules above, through the gate as installed, so a gate that stopped
  # calling check_descriptions is caught too. The plant is the orient case.
  mkdir -p "$tmp/fg-bad/skills/a" "$tmp/fg-ok/skills/a"
  printf -- '---\nname: a\ndescription: Orient first: then act\n---\n' > "$tmp/fg-bad/skills/a/SKILL.md"
  printf -- '---\nname: a\ndescription: Orient first; then act\n---\n' > "$tmp/fg-ok/skills/a/SKILL.md"
  run_gate "$tmp/fg-bad" gate_frontmatter; bad=$?
  run_gate "$tmp/fg-ok" gate_frontmatter
  plant_rejected $bad $? "frontmatter gate, description as installed"

  # A stub the document does not describe, against a stub it does.
  # The script takes no paths, so each planted tree has the repository's layout.
  stubs="$PWD/scripts/check-workspace-stubs.py"
  for t in st-bad st-ok; do
    mkdir -p "$tmp/$t/docs" "$tmp/$t/examples/workspace/.agents"
    printf '## The document set\n\n| Document | Role |\n|---|---|\n| `index.md` | Manifest |\n| `notes.md` | Notes |\n' > "$tmp/$t/docs/standing-documents.md"
    printf -- '- `.agents/notes.md`\n' > "$tmp/$t/examples/workspace/index.md"
    : > "$tmp/$t/examples/workspace/.agents/notes.md"
  done
  : > "$tmp/st-bad/examples/workspace/.agents/undescribed.md"
  ( cd "$tmp/st-bad" && python3 "$stubs" ) >/dev/null 2>&1
  bad=$?
  ( cd "$tmp/st-ok" && python3 "$stubs" ) >/dev/null 2>&1
  plant_rejected $bad $? "workspace stub gate"

  # Each plant is a copy of the real hooks with one fault, so only the check
  # aimed at that fault can reject it: an uncompilable pattern added, then a
  # blocking rule weakened so one of its planted cases no longer fires.
  hk="$PWD/scripts/check-hooks.py"
  for d in hk-bad hk-case hk-ok; do mkdir -p "$tmp/$d" && cp -R hooks "$tmp/$d/hooks"; done
  printf -- '---\nname: broken\nevent: bash\naction: block\nconditions:\n  - field: command\n    operator: regex_match\n    pattern: (unclosed\n---\n' > "$tmp/hk-bad/hooks/hookify.broken.local.md"
  nogi=hooks/hookify.repomix-no-gitignore.local.md
  sed 's/pattern: --no-gitignore/pattern: --never-given/' "$nogi" > "$tmp/hk-case/$nogi"
  ( cd "$tmp/hk-bad" && python3 "$hk" ) >/dev/null 2>&1
  bad=$?
  ( cd "$tmp/hk-ok" && python3 "$hk" ) >/dev/null 2>&1
  plant_rejected $bad $? "hooks gate, pattern"
  ( cd "$tmp/hk-case" && python3 "$hk" ) >/dev/null 2>&1
  bad=$?
  ( cd "$tmp/hk-ok" && python3 "$hk" ) >/dev/null 2>&1
  plant_rejected $bad $? "hooks gate, planted case"

  # Gate 13: the rule's own selftest must fail when the ruleset's prefix list
  # drifts from the script's. The copy drops one prefix from the ruleset.
  for d in bn-bad bn-ok; do
    mkdir -p "$tmp/$d/scripts" "$tmp/$d/.github/rulesets" && cp scripts/check-branch-name "$tmp/$d/scripts/"
  done
  cp .github/rulesets/branch-names.json "$tmp/bn-ok/.github/rulesets/"
  grep -v 'refs/heads/licence/' .github/rulesets/branch-names.json > "$tmp/bn-bad/.github/rulesets/branch-names.json"
  sh "$tmp/bn-bad/scripts/check-branch-name" --selftest >/dev/null 2>&1
  bad=$?
  sh "$tmp/bn-ok/scripts/check-branch-name" --selftest >/dev/null 2>&1
  plant_rejected $bad $? "branch name gate, prefix drift"

  # Gate 14: a copy of the hook missing one trailer must fail its cases.
  sed 's/Assisted-by/Assisted-xx/' .githooks/commit-msg > "$tmp/commit-msg-weak"
  ( fail=0; ATTR_HOOK="$tmp/commit-msg-weak" gate_attribution >/dev/null 2>&1; exit "$fail" )
  bad=$?
  ( fail=0; gate_attribution >/dev/null 2>&1; exit "$fail" )
  plant_rejected $bad $? "attribution gate, weakened hook"

  # Gate 15: the selftest must fail when a fail case is filed as a pass case.
  for d in qb-bad qb-ok; do
    mkdir -p "$tmp/$d/scripts" "$tmp/$d/tests" && cp scripts/check-qblock "$tmp/$d/scripts/"
    cp -R tests/qblock-cases "$tmp/$d/tests/"
  done
  mv "$tmp/qb-bad/tests/qblock-cases/fail-no-block.md" "$tmp/qb-bad/tests/qblock-cases/pass-no-block.md"
  python3 "$tmp/qb-bad/scripts/check-qblock" --selftest >/dev/null 2>&1
  bad=$?
  python3 "$tmp/qb-ok/scripts/check-qblock" --selftest >/dev/null 2>&1
  plant_rejected $bad $? "question block gate, fail case filed as pass"

  # Gate 16: a copy of the checker without its empty-box rule must fail its
  # own selftest.
  mkdir -p "$tmp/pb/scripts" && grep -v 'found += unticked(body)' scripts/check-pr-body > "$tmp/pb/scripts/check-pr-body"
  python3 "$tmp/pb/scripts/check-pr-body" --selftest >/dev/null 2>&1
  bad=$?
  python3 scripts/check-pr-body --selftest >/dev/null 2>&1
  plant_rejected $bad $? "pull request body gate, rule removed"

  # Gate 17: a copy of the builder whose releaseTime pattern ends in $ rather
  # than \Z, so it accepts a trailing newline, must fail its own selftest.
  mkdir -p "$tmp/sp/scripts" && sed '/^RELEASE_TIME_RE/s/\\Z"/$"/' scripts/spdx-fragment.py > "$tmp/sp/scripts/spdx-fragment.py"
  python3 "$tmp/sp/scripts/spdx-fragment.py" --selftest >/dev/null 2>&1
  bad=$?
  python3 scripts/spdx-fragment.py --selftest >/dev/null 2>&1
  plant_rejected $bad $? "spdx-fragment gate, releaseTime pattern loosened"

  printf '\n'
  [ "$plant_fail" -eq 0 ] || { echo "selftest: a gate could not be shown to fail. Do not trust a clean run."; return 1; }
  echo "selftest: all $plant_n planted positives fired."
  echo
  echo "== gate 7 plants its own positives, one per rule =="
  python3 scripts/mdlint.py --selftest >/dev/null 2>&1
  rc=$?
  # exit 1 here means findings in the tree, which run_all reports properly.
  # Only a plant failure is fatal to the selftest itself.
  if python3 scripts/mdlint.py --selftest 2>&1 | grep -q 'PLANT FAIL'; then
    echo "selftest: an mdlint rule could not be shown to fire."
    return 1
  fi
  echo "mdlint: every rule fired on its plant."
  echo
  echo "Now the real run."
  run_all
}

case "${1:-}" in
  --selftest) run_selftest ;;
  '')         run_all ;;
  *)          echo "usage: scripts/gates.sh [--selftest]" >&2; exit 2 ;;
esac
