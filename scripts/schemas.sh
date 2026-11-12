#!/usr/bin/env sh

# SPDX-FileCopyrightText: 2026 Aidan Naveja
#
# SPDX-License-Identifier: Apache-2.0

# Validates the two metadata files that declare a published schema against
# that schema: security-insights.yml against OpenSSF Security Insights 2.2.0,
# with cue, and CITATION.cff against Citation File Format 1.2.0, with
# check-jsonschema.
#
# Also checks this tree's own JSON Schema draft-07 files with check-jsonschema,
# a full validator: every file declaring "$schema" against the draft-07
# metaschema, then the documents each one governs. The registry's vendor files,
# the review-round examples and every row of schema-cases/cases.json are real
# documents; the expected failures must fail on validation, not on a schema
# that cannot load. request.json, response.json and event-base.json have no
# documents in this tree, so this script builds a sample of each, which shows
# that each loads and that the $refs a sample reaches resolve, and nothing
# about a $ref no sample reaches, a required field no plant drops, or a
# message anyone sends. The two review-round templates hold
# placeholders that fail by design, so they are not validated.
#
# The schemas are not in this tree. The verification image downloads each from
# the commit its release tag points at, checked by digest, into /opt/schemas
# (containers/verify/Containerfile), so a third-party schema and its licence
# stay out of the repository. This script checks each digest again before it
# uses a schema, so a schema that is not the pinned one fails rather than
# validating against something else.
#
# Coverage: that each file matches its schema's structure, field names, types
# and patterns, closed: a field the schema does not define fails, because
# #SecurityInsights is a CUE definition, and a definition is closed. cue vet
# requires every value to be concrete when it is given a data file, so a
# required field left out fails as an incomplete value.
# It does NOT check that a value is true, that a link resolves, or that the
# files agree with each other or with the tree. For the draft-07 documents,
# scripts/schema-check.py and scripts/round-check.py stay the checks on the
# host, standard library only; the rules no schema can state are theirs.
#
# A missing tool or schema fails the script and names it, as in
# scripts/compliance.sh: a "not checked" line has been read as a pass.
#
# Usage: scripts/schemas.sh              validate the metadata files and the JSON Schemas
#        scripts/schemas.sh --selftest   first show each check rejects a planted
#                                        bad file, a schema with the wrong digest
#                                        and a missing tool, each for its reason,
#                                        and the same for the draft-07 checks
#
# Run it in the verification container, which holds the tools and schemas:
#   containers/verify/verify . ./scripts/schemas.sh --selftest
#
# SCHEMAS_DIR names the schema directory, default /opt/schemas. SCHEMAS_CUE and
# SCHEMAS_CJS name the cue and check-jsonschema commands; the selftest sets one
# to a name that is not installed, to show the missing-tool case.

self=$(cd "$(dirname "$0")" && pwd -P)/$(basename "$0")
cd "$(dirname "$0")/.." || exit 1

selftest=0
for arg in "$@"; do
  case "$arg" in
    --selftest) selftest=1 ;;
    *) printf 'schemas: unknown argument %s\n' "$arg" >&2; exit 2 ;;
  esac
done

dir=${SCHEMAS_DIR:-/opt/schemas}
cue=${SCHEMAS_CUE:-cue}
cjs=${SCHEMAS_CJS:-check-jsonschema}

# The pinned schemas: file name in $dir, sha256. The same digests are in the
# Containerfile's ADD lines; a new schema version changes both.
si_schema=security-insights-2.2.0.cue
si_sha=4e4b61470b5484fc8969f2a8a77ffbe0712a7c8a870c2079188f246c14cd58b1
cff_schema=cff-1.2.0.json
cff_sha=0b8d22140da702d766df318dcff3a91af2f39521298dcf36d76315fd99cc169b

# Every file in this tree that declares a JSON Schema. A new one fails the
# coverage check until it is listed here and given its documents below.
json_schemas='orchestration/registry/surface-descriptor.schema.json
orchestration/schemas/event-base.json
orchestration/schemas/request.json
orchestration/schemas/response.json
orchestration/schemas/round/operator-decision.json
orchestration/schemas/round/review-report.json
orchestration/schemas/round/review-round.json'
registry_schema=orchestration/registry/surface-descriptor.schema.json
round_schemas=orchestration/schemas/round
cases_dir=examples/review-round/schema-cases
# What check-jsonschema prints when a document fails. It exits 1 on a schema it
# cannot load as well, so the exit code alone cannot tell the two apart.
rejected='Schema validation errors were encountered'

fail=0
pass_n=0
total=0

check_start() { printf '\n== %s ==\n' "$1"; total=$((total + 1)); }
check_ok()    { printf 'PASS  %s\n' "$1"; pass_n=$((pass_n + 1)); }
check_bad()   { printf 'FAIL  %s\n' "$1"; fail=1; }

# digest_ok DIR FILE SHA: the schema exists and has the pinned digest.
digest_ok() {
  [ -f "$1/$2" ] || { printf 'schemas: %s/%s is missing; run in the verification container\n' "$1" "$2"; return 1; }
  got=$(sha256sum "$1/$2" | cut -d' ' -f1)
  [ "$got" = "$3" ] || { printf 'schemas: %s/%s has sha256 %s, pinned %s\n' "$1" "$2" "$got" "$3"; return 1; }
}

tool_ok() {
  command -v "$1" >/dev/null 2>&1 || { printf 'schemas: %s is not installed; run in the verification container\n' "$1"; return 1; }
}

# validate_si DIR FILE and validate_cff DIR FILE: exit 0 only if the schema in
# DIR is the pinned one, the tool is installed and FILE matches.
validate_si() {
  tool_ok "$cue" && digest_ok "$1" "$si_schema" "$si_sha" \
    && "$cue" vet -d '#SecurityInsights' "$1/$si_schema" "$2"
}
validate_cff() {
  tool_ok "$cjs" && digest_ok "$1" "$cff_schema" "$cff_sha" \
    && "$cjs" --schemafile "$1/$cff_schema" "$2"
}

# coverage_ok ROOT: the JSON files under ROOT that declare "$schema" are exactly
# the list above. It reads *.json only.
coverage_ok() {
  # .venv, venv and node_modules are ignored by .gitignore and may hold vendored
  # schemas; the verification container copies the whole checkout.
  found=$(cd "$1" && find . \( -name .git -o -name .venv -o -name venv -o -name node_modules \) -prune \
    -o -name '*.json' -exec grep -l '"\$schema"' {} + | sed 's|^\./||' | sort)
  listed=$(printf '%s\n' "$json_schemas" | sort)
  [ "$found" = "$listed" ] || {
    printf 'schemas: the files declaring "$schema" differ from the list in this script.\nFound:\n%s\n' "$found"
    return 1
  }
}

# metaschema_ok FILE...: each file declares draft-07 and is valid draft-07.
# check-jsonschema picks the metaschema from the file's own $schema, so a file
# moved to another draft would be checked against that draft.
metaschema_ok() {
  for f in "$@"; do
    grep -Eq '"\$schema": *"http://json-schema.org/draft-07/schema#?"' "$f" || {
      printf 'schemas: %s does not declare draft-07\n' "$f"; return 1; }
  done
  tool_ok "$cjs" && "$cjs" --check-metaschema "$@"
}

# doc_ok SCHEMA FILE: the document matches the schema.
doc_ok() {
  tool_ok "$cjs" && "$cjs" --schemafile "$1" "$2"
}

# registry_ok: every vendor file matches the descriptor schema.
registry_ok() {
  rc=0 n=0
  for f in orchestration/registry/*.json; do
    [ "$f" = "$registry_schema" ] && continue
    n=$((n + 1))
    doc_ok "$registry_schema" "$f" || rc=1
  done
  [ "$n" -gt 0 ] || { printf 'schemas: no registry vendor files found\n'; return 1; }
  return "$rc"
}

# examples_ok: each review-round example, by file name, matches its schema.
examples_ok() {
  docs=$(find examples/review-round \( -name review-round.json -o -name review-report.json -o -name operator-decision.json \) \
    -not -path '*/schema-cases/*' -not -path '*/templates/*' | sort)
  [ -n "$docs" ] || { printf 'schemas: no review-round examples found\n'; return 1; }
  rc=0
  for f in $docs; do
    doc_ok "$round_schemas/$(basename "$f")" "$f" || rc=1
  done
  return "$rc"
}

# cases_ok DIR: each row of DIR/cases.json gives the result it expects, and an
# expected failure is a validation failure rather than a schema that cannot load.
cases_ok() {
  tool_ok "$cjs" || return 1
  rows=$(python3 -c 'import json, sys
for c in json.load(open(sys.argv[1]))["cases"]:
    print(c["expect"], c["schema"], c["file"])' "$1/cases.json") || { printf 'schemas: %s/cases.json cannot be read\n' "$1"; return 1; }
  [ -n "$rows" ] || { printf 'schemas: %s/cases.json has no rows\n' "$1"; return 1; }
  rc=0
  while read -r want schema file; do
    out=$("$cjs" --schemafile "$round_schemas/$schema.json" "$1/$file" 2>&1); code=$?
    case "$want:$code" in
      pass:0) ;;
      fail:1)
        case "$out" in
          *"$rejected"*) ;;
          *) printf 'schemas: %s failed for another reason:\n%s\n' "$file" "$out"; rc=1 ;;
        esac ;;
      *) printf 'schemas: %s expected %s, exit %s\n%s\n' "$file" "$want" "$code" "$out"; rc=1 ;;
    esac
  done <<ROWS
$rows
ROWS
  return "$rc"
}

# sample KIND DROP: a message document of KIND, without the field DROP if named.
sample() {
  python3 -c 'import json, sys
kind, drop = sys.argv[1], sys.argv[2]
agent = {"agent_id": "sample", "kind": "human", "role": "relay"}
doc = {"event_id": "e1", "timestamp": "2026-01-01T00:00:00Z", "thread_id": "t1", "from": agent, "to": agent}
if kind == "request":
    doc.update(type="request", action="sample", request_id="r1")
if kind == "response":
    doc.update(type="response", request_id="r1", success=True)
doc.pop(drop, None)
print(json.dumps(doc))' "$1" "${2:-}"
}

# messages_ok: a built sample of each message kind matches its schema.
messages_ok() {
  mt=$(mktemp -d) || { printf 'schemas: no scratch directory\n'; return 1; }
  rc=0
  for kind in event-base request response; do
    sample "$kind" > "$mt/$kind.json" && doc_ok "orchestration/schemas/$kind.json" "$mt/$kind.json" || rc=1
  done
  rm -rf "$mt"
  return "$rc"
}

# plant NAME WANT CMD...: the command must exit non-zero and print WANT, the
# rejection the plant is for. Any non-zero exit alone would also pass a plant
# rejected for some other reason, such as a path the tool cannot read.
plant() {
  pn=$1; want=$2; shift 2
  if pout=$("$@" 2>&1); then
    printf 'PLANT FAIL  %s was accepted\n' "$pn"; plant_bad=1
  else
    case "$pout" in
      *"$want"*) printf 'PLANT ok    %s is rejected\n' "$pn" ;;
      *) printf 'PLANT FAIL  %s was rejected without "%s"\n' "$pn" "$want"; plant_bad=1 ;;
    esac
  fi
}

# missing_tool VAR NAME: the whole script, with VAR set to a command that is not
# installed, exits 1 and names it.
missing_tool() {
  mout=$(env "$1=$2" sh "$self" 2>&1); mcode=$?
  case "$mcode:$mout" in
    1:*"$2 is not installed"*) printf 'PLANT ok    a missing %s fails, exit 1, naming it\n' "$1" ;;
    *) printf 'PLANT FAIL  a missing %s gave exit %s, not 1 naming the tool\n' "$1" "$mcode"; plant_bad=1 ;;
  esac
}

selftest_run() {
  check_start "schemas selftest"
  s=$(mktemp -d) || { check_bad "schemas selftest: no scratch directory"; return; }
  plant_bad=0
  # A clean pass first, or a rejected plant proves nothing.
  if ! validate_si "$dir" security-insights.yml >/dev/null 2>&1 || ! validate_cff "$dir" CITATION.cff >/dev/null 2>&1; then
    printf 'PLANT FAIL  a clean file was rejected, so a rejected plant proves nothing\n'
    check_bad "schemas selftest"; rm -rf "$s"; return
  fi
  # A field the schema does not define, and a value its pattern refuses.
  { cat security-insights.yml; printf 'planted-unknown-field: true\n'; } > "$s/si-field.yml"
  plant "security-insights.yml with an undefined field" '"planted-unknown-field": field not allowed' \
    validate_si "$dir" "$s/si-field.yml"
  sed 's/^\(  schema-version:\) .*/\1 "2.2"/' security-insights.yml > "$s/si-version.yml"
  plant "security-insights.yml with a bad schema-version" 'header."schema-version": invalid value "2.2" (out of bound' \
    validate_si "$dir" "$s/si-version.yml"
  grep -v '^  schema-version:' security-insights.yml > "$s/si-required.yml"
  plant "security-insights.yml without its required schema-version" 'header."schema-version": incomplete value' \
    validate_si "$dir" "$s/si-required.yml"
  sed 's/^cff-version: .*/cff-version: 1.1.0/' CITATION.cff > "$s/cff-version.cff"
  plant "CITATION.cff with a wrong cff-version" "'1.1.0' does not match" \
    validate_cff "$dir" "$s/cff-version.cff"
  grep -v '^title:' CITATION.cff > "$s/cff-title.cff"
  plant "CITATION.cff without its required title" "'title' is a required property" \
    validate_cff "$dir" "$s/cff-title.cff"
  # A schema that is not the pinned one, though the file still matches it.
  if ! { mkdir "$s/schemas" && cp "$dir/$si_schema" "$dir/$cff_schema" "$s/schemas/" \
    && printf '\n' >> "$s/schemas/$si_schema" && printf '\n' >> "$s/schemas/$cff_schema"; }; then
    check_bad "schemas selftest: copying the schemas failed"; rm -rf "$s"; return
  fi
  plant "a Security Insights schema with the wrong digest" "$si_schema has sha256" \
    validate_si "$s/schemas" security-insights.yml
  plant "a CFF schema with the wrong digest" "$cff_schema has sha256" \
    validate_cff "$s/schemas" CITATION.cff
  # A missing tool fails the whole script and names it, for each tool.
  missing_tool SCHEMAS_CUE schemas-selftest-not-installed
  missing_tool SCHEMAS_CJS schemas-selftest-not-installed
  # The draft-07 checks. A schema the list does not name, and one that is not
  # valid draft-07.
  mkdir "$s/root" && cp -R orchestration "$s/root/" && printf '{"$schema": "x"}\n' > "$s/root/orchestration/planted.json"
  plant "a schema-declaring file not in the list" 'differ from the list' coverage_ok "$s/root"
  sed 's/"title": "RequestEvent"/"title": 7/' orchestration/schemas/request.json > "$s/not-draft-07.json"
  plant "a schema that is not valid draft-07" "7 is not of type 'string'" metaschema_ok "$s/not-draft-07.json"
  # A document of each set. The first reaches event-base.json through a $ref
  # across directories, and the two samples through a $ref beside them.
  sed 's/"interface": "[^"]*"/"interface": "planted"/' orchestration/registry/anthropic.json > "$s/registry.json"
  plant "a registry file with a value event-base.json refuses" "'planted' is not one of" doc_ok "$registry_schema" "$s/registry.json"
  grep -v '"schemaVersion"' examples/review-round/reviewer/review-round.json > "$s/review-round.json"
  plant "a review-round example without a required field" "$rejected" doc_ok "$round_schemas/review-round.json" "$s/review-round.json"
  for kind in request response; do
    sample "$kind" event_id > "$s/$kind.json"
    plant "a $kind without event-base's event_id" "'event_id' is a required property" doc_ok "orchestration/schemas/$kind.json" "$s/$kind.json"
  done
  # A row whose expected result is wrong, and an expected failure caused by a
  # schema that cannot load, which an exit code alone would pass.
  cp -R "$cases_dir" "$s/flipped" && cp -R "$cases_dir" "$s/noload"
  python3 -c 'import json, sys
for d, field, old, new in ((sys.argv[1], "expect", "pass", "fail"), (sys.argv[2], "schema", None, "no-such-schema")):
    t = json.load(open(d + "/cases.json"))
    row = [c for c in t["cases"] if c["expect"] == ("pass" if old else "fail")][0]
    row[field] = new
    json.dump(t, open(d + "/cases.json", "w"))' "$s/flipped" "$s/noload"
  plant "a case expecting the wrong result" 'expected fail, exit 0' cases_ok "$s/flipped"
  plant "an expected failure from a schema that cannot load" 'failed for another reason' cases_ok "$s/noload"
  rm -rf "$s"
  if [ "$plant_bad" -eq 0 ]; then check_ok "schemas selftest"; else check_bad "schemas selftest"; fi
}

[ "$selftest" -eq 0 ] || selftest_run

check_start "security-insights.yml against Security Insights 2.2.0"
if validate_si "$dir" security-insights.yml; then check_ok "security-insights.yml"; else check_bad "security-insights.yml"; fi

check_start "CITATION.cff against Citation File Format 1.2.0"
if validate_cff "$dir" CITATION.cff; then check_ok "CITATION.cff"; else check_bad "CITATION.cff"; fi

check_start "every schema-declaring file is listed"
if coverage_ok .; then check_ok "schema list"; else check_bad "schema list"; fi

check_start "the 7 schemas declare and pass the draft-07 metaschema"
# shellcheck disable=SC2086 # the list is paths with no spaces, one word each
if metaschema_ok $json_schemas; then check_ok "metaschema"; else check_bad "metaschema"; fi

check_start "orchestration/registry/*.json against surface-descriptor.schema.json"
if registry_ok; then check_ok "registry"; else check_bad "registry"; fi

check_start "the review-round examples against their schemas"
if examples_ok; then check_ok "review-round examples"; else check_bad "review-round examples"; fi

check_start "$cases_dir/cases.json, every row"
if cases_ok "$cases_dir"; then check_ok "schema cases"; else check_bad "schema cases"; fi

check_start "a built sample of each message schema"
if messages_ok; then check_ok "message samples"; else check_bad "message samples"; fi

printf '\n%s of %s checks passed\n' "$pass_n" "$total"
if [ "$fail" -ne 0 ]; then
  printf 'schemas: FAILED\n'; exit 1
fi
printf 'schemas: all passed\n'
