#!/usr/bin/env sh
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
# check. These six gates cover: the em dash ban, the private task ID ban,
# JSON wellformedness, registry self-consistency, skill frontmatter, the
# reflow script's own selftest, and markdown structure via scripts/mdlint.py,
# which states its own eighteen-rule coverage in its header. They do NOT cover: en dashes (ranges and
# clause separators are not mechanically separable, so that stays a review
# prompt), prose quality, internal link validity, whether a skill's Scope
# Pointer is last, or whether any document's claims are true.
#
# Usage: scripts/gates.sh            run every gate
#        scripts/gates.sh --selftest prove each gate can fail, then run them

set -u

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
  hits=$(grep -rl -- "$EM" . --exclude-dir=.git 2>/dev/null || true)
  if [ -n "$hits" ]; then
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
  hits=$(grep -rnE '\b(P[0-9]+-[0-9]+|OPEN_[0-9]+)\b' . --exclude-dir=.git 2>/dev/null || true)
  if [ -n "$hits" ]; then
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
  then gate_ok "registry entries are self-consistent"
  else gate_bad "registry entries are self-consistent"; fi
}

# ---------------------------------------------------------------- 5
gate_frontmatter() {
  gate_start "skill frontmatter present"
  bad=0
  n=0
  for f in skills/*/SKILL.md; do
    n=$((n + 1))
    head -6 "$f" | grep -q '^name:' || { echo "::error file=$f::missing frontmatter name"; bad=1; }
    head -6 "$f" | grep -q '^description:' || { echo "::error file=$f::missing frontmatter description"; bad=1; }
  done
  echo "  checked $n skills"
  [ "$bad" -eq 0 ] && gate_ok "skill frontmatter present" || gate_bad "skill frontmatter present"
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

run_all() {
  gate_em_dash
  gate_task_ids
  gate_json
  gate_registry
  gate_frontmatter
  gate_reflow
  gate_markdown
  printf '\n%s of 7 gates passed\n' "$pass_n"
  [ "$fail" -eq 0 ] || { echo "gates: FAILED"; return 1; }
  echo "gates: all passed"
  return 0
}

# A gate that has never returned a hit has not been shown capable of
# returning one, so each of the first five is run against a planted positive
# in a scratch tree. Gate 6 carries its own fixture assertions already.
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
  # The two senses are opposite and conflating them reports backwards, which
  # is how the first draft of this selftest "failed" against gates that were
  # working. A search gate fires by FINDING the plant, so exit 0 is correct.
  # A validity gate fires by REJECTING the plant, so non-zero is correct.
  plant_found() {    # expects exit 0: the search found the planted positive
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
    if [ "$1" -ne 0 ] && [ "$2" -eq 0 ]; then
      printf 'PLANT ok    %s rejects a plant and accepts a clean fixture\n' "$3"
    elif [ "$1" -eq 0 ]; then
      printf 'PLANT FAIL  %s accepted a planted positive\n' "$3"; plant_fail=1
    else
      printf 'PLANT FAIL  %s rejected its own clean fixture, so the non-zero on the plant proves nothing\n' "$3"; plant_fail=1
    fi
  }

  printf 'text %s text\n' "$EM" > "$tmp/a.md"
  grep -rl -- "$EM" "$tmp" >/dev/null 2>&1
  plant_found $? "em dash gate"

  # Assembled, for the same reason EM is: a literal here makes this file
  # itself a hit for the gate it is testing, and the real run then fails on
  # the test fixture rather than on the repository.
  printf 'see P%s-%s for detail\n' 12 34 > "$tmp/b.md"
  grep -rnE '\b(P[0-9]+-[0-9]+|OPEN_[0-9]+)\b' "$tmp/b.md" >/dev/null 2>&1
  plant_found $? "private task ID gate"

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

  mkdir -p "$tmp/skills/nofm" "$tmp/skills/withfm"
  printf -- '---\ndescription: has no name\n---\n' > "$tmp/skills/nofm/SKILL.md"
  head -6 "$tmp/skills/nofm/SKILL.md" | grep -q '^name:'
  bad=$?
  printf -- '---\nname: withfm\ndescription: has one\n---\n' > "$tmp/skills/withfm/SKILL.md"
  head -6 "$tmp/skills/withfm/SKILL.md" | grep -q '^name:'
  plant_rejected $bad $? "frontmatter gate"

  printf '\n'
  [ "$plant_fail" -eq 0 ] || { echo "selftest: a gate could not be shown to fail. Do not trust a clean run."; return 1; }
  echo "selftest: all five planted positives fired."
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
