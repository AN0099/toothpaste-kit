#!/usr/bin/env sh

# SPDX-FileCopyrightText: 2026 Aidan Naveja
#
# SPDX-License-Identifier: Apache-2.0

# Validates the two metadata files that declare a published schema against
# that schema: security-insights.yml against OpenSSF Security Insights 2.2.0,
# with cue, and CITATION.cff against Citation File Format 1.2.0, with
# check-jsonschema.
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
# files agree with each other or with the tree.
#
# A missing tool or schema fails the script and names it, as in
# scripts/compliance.sh: a "not checked" line has been read as a pass.
#
# Usage: scripts/schemas.sh              validate both files
#        scripts/schemas.sh --selftest   first show each check rejects a planted
#                                        bad file, a schema with the wrong digest
#                                        and a missing tool, each for its reason
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
  rm -rf "$s"
  if [ "$plant_bad" -eq 0 ]; then check_ok "schemas selftest"; else check_bad "schemas selftest"; fi
}

[ "$selftest" -eq 0 ] || selftest_run

check_start "security-insights.yml against Security Insights 2.2.0"
if validate_si "$dir" security-insights.yml; then check_ok "security-insights.yml"; else check_bad "security-insights.yml"; fi

check_start "CITATION.cff against Citation File Format 1.2.0"
if validate_cff "$dir" CITATION.cff; then check_ok "CITATION.cff"; else check_bad "CITATION.cff"; fi

printf '\n%s of %s checks passed\n' "$pass_n" "$total"
if [ "$fail" -ne 0 ]; then
  printf 'schemas: FAILED\n'; exit 1
fi
printf 'schemas: all passed\n'
