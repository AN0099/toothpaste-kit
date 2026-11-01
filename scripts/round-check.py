#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2026 Aidan Naveja
#
# SPDX-License-Identifier: Apache-2.0

"""Validate Local Change-Verification Round documents.

Usage:
  scripts/round-check.py [--repo REPO_DIR] ROUND_DIR [ROUND_DIR ...]
  scripts/round-check.py --cases CASES_DIR
  scripts/round-check.py --selftest

A round directory holds up to three JSON documents, named after their
schemas in orchestration/schemas/round/: review-round.json,
review-report.json and operator-decision.json. Each document present is
checked against its schema. It finds its schemas from its own location, so
it can be run from any directory.

--repo names the repository the rounds are committed in. Each commit a
record cites must then exist there, and each references commit must hold
the record at its artifactPath. Without --repo, commits are checked only for
format.

--cases checks a schema-cases directory against its cases.json: each pass
case meets its schema and its directory passes as a round; each fail case is
refused, by its schema or, planted into valid/valid-complete-round, by the
cross-artifact checks.

Standard library only, as the gates are (CONTRIBUTING.md). This is not a
general JSON Schema engine: it implements the draft-07 subset the round
schemas use. Before validating anything it walks every schema and fails,
naming the keyword, on any key it does not implement, so a schema edit that
needs a keyword this file lacks fails here instead of passing silently. The
schemas stay ordinary draft-07, so a full validator gives the same answer.

Keywords implemented: type, required, properties, additionalProperties
(boolean or schema), enum, const, pattern, format (date-time), items,
minItems, minLength and $ref within the same file. $schema, $id, title,
description and definitions are structure or annotations.

Exit status: 0 all documents valid, 1 a document failed, 2 usage or schema
error.
"""

import copy
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime

SCHEMA_DIR = "orchestration/schemas/round"
KINDS = ("review-round", "review-report", "operator-decision")

KNOWN_KEYWORDS = {
    "$schema", "$id", "title", "description", "definitions",
    "type", "required", "properties", "additionalProperties", "enum",
    "const", "pattern", "format", "items", "minItems", "minLength", "$ref",
    "minimum", "if", "then", "else",
}


class SchemaError(Exception):
    """The schema itself is unusable; exit 2, never a document failure."""


def check_keywords(node, where, errors):
    """Fail on any keyword not implemented here, wherever a subschema can sit."""
    if not isinstance(node, dict):
        errors.append(f"{where}: a schema must be an object")
        return
    for key, value in node.items():
        if key not in KNOWN_KEYWORDS:
            errors.append(f"{where}: unimplemented JSON Schema keyword: {key}")
        elif key in ("properties", "definitions") and isinstance(value, dict):
            for name, sub in value.items():
                check_keywords(sub, f"{where}/{key}/{name}", errors)
        elif key in ("items", "additionalProperties", "if", "then", "else") and isinstance(value, dict):
            check_keywords(value, f"{where}/{key}", errors)


def resolve_ref(ref, root):
    if not ref.startswith("#"):
        raise SchemaError(f"$ref {ref!r}: only references within the same file are supported")
    node = root
    for part in ref[1:].strip("/").split("/"):
        if part == "":
            continue
        part = part.replace("~1", "/").replace("~0", "~")
        if not isinstance(node, dict) or part not in node:
            raise SchemaError(f"$ref {ref!r} does not resolve")
        node = node[part]
    return node


TYPES = {
    "object": lambda v: isinstance(v, dict),
    "array": lambda v: isinstance(v, list),
    "string": lambda v: isinstance(v, str),
    "boolean": lambda v: isinstance(v, bool),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "null": lambda v: v is None,
}


def is_date_time(value):
    # RFC 3339: a full date, a time and an offset. fromisoformat alone would
    # accept a bare date or a time with no offset.
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}:\d{2}(\.\d+)?([Zz]|[+-]\d{2}:\d{2})", value):
        return False
    try:
        datetime.fromisoformat(value.upper().replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def json_equal(a, b):
    """Equality as JSON Schema means it: true is not 1, though 1 is 1.0."""
    if isinstance(a, bool) or isinstance(b, bool):
        return isinstance(a, bool) and isinstance(b, bool) and a == b
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(json_equal(x, y) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(json_equal(a[k], b[k]) for k in a)
    return type(a) is type(b) and a == b or (TYPES["number"](a) and TYPES["number"](b) and a == b)


def validate(inst, schema, root, path, errors):
    if "$ref" in schema:
        validate(inst, resolve_ref(schema["$ref"], root), root, path, errors)
        return
    if "type" in schema:
        wanted = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        for t in wanted:
            if t not in TYPES:
                raise SchemaError(f"unknown type {t!r}")
        if not any(TYPES[t](inst) for t in wanted):
            errors.append(f"{path}: expected {' or '.join(wanted)}, got {json.dumps(inst)[:60]}")
            return
    if "const" in schema and not json_equal(inst, schema["const"]):
        errors.append(f"{path}: must be {json.dumps(schema['const'])}, got {json.dumps(inst)[:60]}")
    if "enum" in schema and not any(json_equal(inst, e) for e in schema["enum"]):
        errors.append(f"{path}: {json.dumps(inst)[:60]} is not one of {', '.join(json.dumps(e) for e in schema['enum'])}")
    if "minimum" in schema and TYPES["number"](inst) and inst < schema["minimum"]:
        errors.append(f"{path}: {inst} is less than the minimum {schema['minimum']}")
    if "if" in schema:
        trial = []
        validate(inst, schema["if"], root, path, trial)
        branch = "then" if not trial else "else"
        if branch in schema:
            validate(inst, schema[branch], root, path, errors)
    if isinstance(inst, str):
        if "minLength" in schema and len(inst) < schema["minLength"]:
            errors.append(f"{path}: shorter than {schema['minLength']} character(s)")
        if "pattern" in schema and re.search(schema["pattern"], inst) is None:
            errors.append(f"{path}: {inst!r} does not match {schema['pattern']!r}")
        if "format" in schema:
            if schema["format"] != "date-time":
                raise SchemaError(f"unimplemented format: {schema['format']}")
            if not is_date_time(inst):
                errors.append(f"{path}: {inst!r} is not an RFC 3339 date-time with an offset")
    if isinstance(inst, dict):
        for name in schema.get("required", []):
            if name not in inst:
                errors.append(f"{path}: missing required field {name!r}")
        props = schema.get("properties", {})
        for name, value in inst.items():
            if name in props:
                validate(value, props[name], root, f"{path}.{name}", errors)
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}: field {name!r} is not allowed here")
            elif isinstance(schema.get("additionalProperties"), dict):
                validate(value, schema["additionalProperties"], root, f"{path}.{name}", errors)
    if isinstance(inst, list):
        if "minItems" in schema and len(inst) < schema["minItems"]:
            errors.append(f"{path}: needs at least {schema['minItems']} item(s), has {len(inst)}")
        if "items" in schema:
            for i, item in enumerate(inst):
                validate(item, schema["items"], root, f"{path}[{i}]", errors)


# ---------------------------------------------------------------- cross-artifact
# Field paths follow orchestration/schemas/round/. The decision's verification
# entries name their finding with findingId; the alignment status values are
# matched, mismatched and unresolved.
# A copy of the roles orchestration/ROLES.md defines; --selftest compares them.
ROLES = ("operator", "lead", "aide", "minion")
CHECK_STATUSES = ("passed", "failed", "not-run", "blocked")
NORMAL_DECISIONS = ("accept", "reject", "request-revision")


class _Missing:
    """An absent field. Prints as "missing", so a message that interpolates
    an absent value reads as plain words."""

    def __repr__(self):
        return "missing"

    __str__ = __repr__


MISSING = _Missing()


def get(doc, dotted):
    node = doc
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node:
            return MISSING
        node = node[part]
    return node


def repo_relative(path):
    """Why a path is not repository-relative, or None when it is."""
    if not isinstance(path, str) or path == "":
        return "is not a non-empty string"
    if path.startswith("/") or re.match(r"^[A-Za-z]:", path):
        return "is absolute"
    if "\\" in path:
        return "contains a backslash"
    if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*://", path):
        return "is a URL"
    if ".." in path.split("/"):
        return "has a .. segment"
    return None


# The handoff's artifactRequirements, copied so that a document is checked
# against the spec itself and not only against the schemas: a schema that
# drops a required path would otherwise let every document through.
SPEC = {
    "review-round": ("tpkit.review-round/v1alpha1", "ReviewRound", (
        "metadata.id", "metadata.roundId", "metadata.createdAt", "handling.visibility",
        "handling.redaction", "provenance.repository", "provenance.baseRevision",
        "provenance.targetRevision", "provenance.artifactPath", "roles.reviewer.role",
        "roles.verifier.role", "roles.decisionMaker.role", "scope.paths", "scope.intent",
        "requiredChecks", "restrictions")),
    "review-report": ("tpkit.review-report/v1alpha1", "ReviewReport", (
        "metadata.id", "metadata.roundId", "metadata.createdAt", "handling.visibility",
        "handling.redaction", "reviewer.role", "reviewedRevision.revision",
        "reviewedRevision.evidence", "checks", "findings", "recommendation", "limitations",
        "provenance.artifactPath", "provenance.commit")),
    "operator-decision": ("tpkit.operator-decision/v1alpha1", "OperatorDecision", (
        "metadata.id", "metadata.roundId", "metadata.createdAt", "handling.visibility",
        "handling.redaction", "references.reviewRound.artifactPath",
        "references.reviewRound.commit", "references.reviewReport.artifactPath",
        "references.reviewReport.commit", "alignment.packetTargetRevision",
        "alignment.reportReviewedRevision", "alignment.status", "verification.performedBy.role",
        "verification.performedAt", "verification.findings", "decision.madeBy.role",
        "decision.status", "decision.basedOnFindings", "decision.rationale",
        "provenance.artifactPath", "provenance.commit")),
}
# The reviewRound semantic rule: restrictions state at least these postures.
# Their values are the schema's to fix; this checks only that each is stated.
POSTURES = ("network", "secrets", "remoteAccess")
SPEC_FINDING = ("id", "severity", "location.path", "claim", "evidence", "proposedRemedy",
                "verification.status", "verification.verifiedBy", "verification.evidence")


def first_missing(doc, paths):
    """The shortest absent prefix of each dotted path, each named once, in
    the order the paths give them."""
    seen = []
    for dotted in paths:
        parts = dotted.split(".")
        for n in range(1, len(parts) + 1):
            prefix = ".".join(parts[:n])
            if get(doc, prefix) is MISSING:
                if prefix not in seen:
                    seen.append(prefix)
                break
    return seen


SCHEMA_MISSING = re.compile(r"^\$((?:\.[A-Za-z0-9_]+|\[\d+\])*): missing required field '([^']+)'$")
SPEC_MISSING = re.compile(r"^(\S+) is required by (?:artifactRequirements|findingRequiredFields)$")


def schema_missing_paths(errors):
    """The dotted paths the schema already reported as missing."""
    out = set()
    for e in errors:
        m = SCHEMA_MISSING.match(e)
        if m:
            out.add((m.group(1) + "." + m.group(2)).lstrip("."))
    return out


def spec_check(docs):
    """Each document against artifactRequirements directly: schemaVersion,
    kind and every required path present (null counts as present, since the
    spec fixes some initial values as null)."""
    out = []
    for kind, doc in sorted(docs.items()):
        version, title, paths = SPEC[kind]
        for field, want in (("schemaVersion", version), ("kind", title)):
            if get(doc, field) != want:
                out.append((kind, "spec-required-field",
                            f"{field} must be {want!r}, got {get(doc, field)!r}"
                            if get(doc, field) is not MISSING else f"{field} is missing"))
        # One line per absent section: when `decision` is missing, name it
        # once rather than each of its required subfields.
        for dotted in first_missing(doc, paths):
            out.append((kind, "spec-required-field", f"{dotted} is required by artifactRequirements"))
        if kind == "review-round" and get(doc, "restrictions") is not MISSING:
            for posture in POSTURES:
                value = get(doc, "restrictions." + posture)
                if not isinstance(value, str) or not value.strip():
                    out.append((kind, "restrictions-posture",
                                f"restrictions.{posture} must state the round's posture; "
                                f"the spec requires network, secrets and remote access"))
        if kind == "review-report" and isinstance(get(doc, "findings"), list):
            for i, f in enumerate(doc["findings"]):
                for dotted in first_missing(f if isinstance(f, dict) else {}, SPEC_FINDING):
                    out.append((kind, "spec-required-field",
                                f"findings[{i}].{dotted} is required by findingRequiredFields"))
    return out


def cross_check(docs):
    """Invariants that span documents. docs maps kind to a parsed document;
    any kind may be absent. Returns (artifact, invariant, message) triples."""
    out = []
    rnd = docs.get("review-round")
    rep = docs.get("review-report")
    dec = docs.get("operator-decision")

    def bad(kind, invariant, message):
        out.append((kind, invariant, message))

    out.extend(spec_check(docs))

    # Shared round ID.
    ids = {k: get(d, "metadata.roundId") for k, d in docs.items()}
    if len({v for v in ids.values() if v is not MISSING}) > 1:
        bad("all", "shared-round-id",
            "metadata.roundId differs: " + ", ".join(f"{k}={v}" for k, v in sorted(ids.items())))

    # Roles come from ROLES.md. ROLES above is a copy, as is each schema's
    # role enum; --selftest (selftest_roles) fails if any copy differs.
    role_paths = {"review-round": ("roles.reviewer.role", "roles.verifier.role", "roles.decisionMaker.role"),
                  "review-report": ("reviewer.role",),
                  "operator-decision": ("verification.performedBy.role", "decision.madeBy.role")}
    for kind, paths in role_paths.items():
        for path in paths:
            value = get(docs.get(kind, {}), path)
            if kind in docs and value is not MISSING and value not in ROLES:
                bad(kind, "roles-from-roles-md", f"{path} is {value!r}, not one of {', '.join(ROLES)}")

    # Repository-relative paths.
    path_fields = {"review-round": ("provenance.artifactPath", "fixture.answerKey"),
                   "review-report": ("provenance.artifactPath",),
                   "operator-decision": ("provenance.artifactPath",
                                         "references.reviewRound.artifactPath",
                                         "references.reviewReport.artifactPath")}
    for kind, paths in path_fields.items():
        for path in paths:
            value = get(docs.get(kind, {}), path)
            if kind in docs and value is not MISSING and repo_relative(value):
                bad(kind, "repository-relative-path", f"{path} {value!r} {repo_relative(value)}")
    if rnd is not None:
        for i, value in enumerate(get(rnd, "scope.paths") if isinstance(get(rnd, "scope.paths"), list) else []):
            if repo_relative(value):
                bad("review-round", "repository-relative-path", f"scope.paths[{i}] {value!r} {repo_relative(value)}")
    report_ids = set()
    if rep is not None:
        for i, f in enumerate(get(rep, "findings") if isinstance(get(rep, "findings"), list) else []):
            if not isinstance(f, dict):
                continue
            if f.get("id") in report_ids:
                bad("review-report", "finding-id-unique",
                    f"findings[{i}].id {f.get('id')!r} is already used by an earlier finding; ids are unique in the report")
            report_ids.add(f.get("id"))
            loc = get(f, "location.path")
            if loc is not MISSING and repo_relative(loc):
                bad("review-report", "repository-relative-path", f"findings[{i}].location.path {loc!r} {repo_relative(loc)}")
            # A reviewer cannot verify its own finding.
            if get(f, "verification.status") not in (MISSING, "unverified") or \
               get(f, "verification.verifiedBy") not in (MISSING, None) or \
               get(f, "verification.evidence") not in (MISSING, []):
                bad("review-report", "report-findings-unverified",
                    f"finding {f.get('id')!r} is not in the initial state (unverified, verifiedBy null, no evidence): "
                    "only a party other than the reviewer verifies, in the OperatorDecision")

    # Every check states its status, and every required check is reported.
    if rep is not None:
        checks = get(rep, "checks") if isinstance(get(rep, "checks"), list) else []
        reported = {}
        for i, c in enumerate(checks):
            status = get(c, "status") if isinstance(c, dict) else MISSING
            if status not in CHECK_STATUSES:
                bad("review-report", "explicit-check-status",
                    f"checks[{i}] ({get(c, 'id') if isinstance(c, dict) else c!r}) has status {'missing' if status is MISSING else repr(status)}, "
                    f"not one of {', '.join(CHECK_STATUSES)}")
            if isinstance(c, dict):
                reported[c.get("id")] = status
        if rnd is not None:
            for rc in get(rnd, "requiredChecks") if isinstance(get(rnd, "requiredChecks"), list) else []:
                cid = rc.get("id") if isinstance(rc, dict) else rc
                if cid not in reported:
                    bad("review-report", "explicit-check-status",
                        f"required check {cid!r} from the round packet has no entry in checks")

    if dec is None:
        return out

    # Revision alignment.
    status = get(dec, "alignment.status")
    packet = get(dec, "alignment.packetTargetRevision")
    reviewed = get(dec, "alignment.reportReviewedRevision")
    if status not in ("matched", "mismatched", "unresolved"):
        bad("operator-decision", "explicit-alignment-status",
            f"alignment.status is {'missing' if status is MISSING else repr(status)}, not matched, mismatched or unresolved")
    if rnd is not None and packet != get(rnd, "provenance.targetRevision"):
        bad("operator-decision", "revision-alignment",
            f"alignment.packetTargetRevision {packet!r} is not the round's provenance.targetRevision {get(rnd, 'provenance.targetRevision')!r}")
    if rep is not None and reviewed != get(rep, "reviewedRevision.revision"):
        bad("operator-decision", "revision-alignment",
            f"alignment.reportReviewedRevision {reviewed!r} is not the report's reviewedRevision.revision {get(rep, 'reviewedRevision.revision')!r}")
    if status == "matched" and packet != reviewed:
        bad("operator-decision", "revision-alignment",
            f"alignment.status is matched but {packet!r} and {reviewed!r} differ")
    if status == "mismatched" and packet == reviewed and packet is not MISSING:
        bad("operator-decision", "revision-alignment", "alignment.status is mismatched but the revisions are equal")
    outcome = get(dec, "decision.status")
    if status in ("mismatched", "unresolved") and outcome in NORMAL_DECISIONS:
        bad("operator-decision", "revision-alignment",
            f"decision.status {outcome!r} relies on a report whose reviewed revision is {status}; "
            "a normal accept, reject or request-revision cannot proceed")

    # The operator decides.
    # A missing decision section is reported once, by the spec layer.
    if isinstance(get(dec, "decision"), dict) and get(dec, "decision.madeBy.role") != "operator":
        bad("operator-decision", "operator-decides",
            f"decision.madeBy.role is {get(dec, 'decision.madeBy.role')!r}, must be operator")

    # Verification by a role other than the reviewer, with evidence.
    verifier = get(dec, "verification.performedBy.role")
    reviewer = get(rep, "reviewer.role") if rep is not None else MISSING
    if reviewer is MISSING and rnd is not None:
        reviewer = get(rnd, "roles.reviewer.role")
    verified = {}
    entries = get(dec, "verification.findings")
    for i, v in enumerate(entries if isinstance(entries, list) else []):
        if not isinstance(v, dict):
            continue
        fid = v.get("findingId")
        verified[fid] = v
        if rep is not None and fid not in report_ids:
            bad("operator-decision", "finding-exists",
                f"verification.findings[{i}] names {fid!r}, which the report does not contain")
        if v.get("status") == "reproduced":
            if reviewer is not MISSING and verifier == reviewer:
                bad("operator-decision", "independent-verification",
                    f"finding {fid!r} is reproduced by role {verifier!r}, the same role as the reviewer")
            if not v.get("evidence"):
                bad("operator-decision", "reproduction-evidence",
                    f"finding {fid!r} is marked reproduced with no evidence")

    # Cited findings are reproduced, with evidence.
    cited = get(dec, "decision.basedOnFindings")
    for fid in cited if isinstance(cited, list) else []:
        v = verified.get(fid)
        if v is None:
            bad("operator-decision", "cites-reproduced-only",
                f"decision.basedOnFindings cites {fid!r}, which has no verification.findings entry")
        elif v.get("status") != "reproduced":
            bad("operator-decision", "cites-reproduced-only",
                f"decision.basedOnFindings cites {fid!r}, whose verification status is {v.get('status')!r}, not reproduced")
        elif not v.get("evidence"):
            bad("operator-decision", "cites-reproduced-only",
                f"decision.basedOnFindings cites {fid!r}, which has no reproduction evidence")

    # An accept with a reproduced blocker (major, per orchestration/rounds.md)
    # needs an explicit exception naming that finding, with a reason.
    if get(dec, "decision.status") == "accept":
        severity = {f.get("id"): f.get("severity") for f in
                    (get(rep, "findings") if rep is not None and isinstance(get(rep, "findings"), list) else [])
                    if isinstance(f, dict)}
        exceptions = get(dec, "decision.exceptions")
        excepted = {e.get("findingId") for e in (exceptions if isinstance(exceptions, list) else [])
                    if isinstance(e, dict) and isinstance(e.get("reason"), str) and e["reason"].strip()}
        for v in verified.values():
            fid = v.get("findingId")
            if v.get("status") == "reproduced" and severity.get(fid) == "major" and fid not in excepted:
                bad("operator-decision", "accept-needs-exception",
                    f"decision.status is accept, but major finding {fid!r} was reproduced and "
                    "decision.exceptions has no entry with a reason for it")
    return out


# ---------------------------------------------------------------- answer key
# A fixture's answer key (the packet's fixture.answerKey, a repository path)
# states the expected outcome. Its format is the one in
# examples/review-round/verifier/answer-key.json. Matching here is mechanical:
# a required expected finding is matched by a report finding at one of its
# locationPaths with at least its minimumSeverity. Whether the finding means
# what the key means is the verifier's call, by the key's equivalence text.
SEVERITY_RANK = {"nit": 0, "minor": 1, "major": 2}
# The answer key's fields. Closed, so a misspelled field fails rather than
# being read as absent.
KEY_FIELDS = {"roundId", "theme", "noFindingsAcceptable", "expectedFindings",
              "expectedDecision", "expectedVerification"}
KEY_FINDING_FIELDS = {"id", "required", "findingClass", "minimumSeverity", "locationPaths",
                      "equivalence", "expectedEvidence"}
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def answer_key_check(key, docs):
    """Expected-outcome invariants. Returns (artifact, invariant, message)
    triples like cross_check."""
    out = []

    def bad(invariant, message, kind="answer-key"):
        out.append((kind, invariant, message))

    if not isinstance(key, dict):
        bad("answer-key-shape", "the answer key is not a JSON object")
        return out
    for k in sorted(set(key) - KEY_FIELDS):
        bad("answer-key-shape", f"unknown field {k!r}; the answer key has {', '.join(sorted(KEY_FIELDS))}")
    if not isinstance(key.get("roundId"), str) or not key.get("roundId").strip():
        bad("answer-key-shape", "roundId must be a non-empty string")
    if key.get("expectedDecision") not in NORMAL_DECISIONS:
        bad("answer-key-shape", f"expectedDecision must be one of {', '.join(NORMAL_DECISIONS)}")
    nfa = key.get("noFindingsAcceptable")
    expected = key.get("expectedFindings")
    if not isinstance(nfa, bool):
        bad("answer-key-shape", "noFindingsAcceptable must be true or false")
    if not isinstance(expected, list):
        bad("answer-key-shape", "expectedFindings must be a list")
        expected = []
    required = []
    ids = set()
    for i, e in enumerate(expected):
        if isinstance(e, dict):
            for k in sorted(set(e) - KEY_FINDING_FIELDS):
                bad("answer-key-shape", f"expectedFindings[{i}] has unknown field {k!r}")
            fid = e.get("id")
            if not isinstance(fid, str) or not fid.strip() or fid in ids:
                bad("answer-key-shape", f"expectedFindings[{i}] needs an id that is a non-empty "
                    "string and unique in the key")
            ids.add(fid if isinstance(fid, str) else None)
        if not isinstance(e, dict) or not isinstance(e.get("required"), bool) \
           or e.get("minimumSeverity") not in SEVERITY_RANK \
           or not isinstance(e.get("locationPaths"), list) or not e.get("locationPaths") \
           or not all(isinstance(x, str) and x for x in e.get("locationPaths")):
            bad("answer-key-shape", f"expectedFindings[{i}] needs required (true or false), "
                f"minimumSeverity ({', '.join(SEVERITY_RANK)}) and a non-empty locationPaths list")
            continue
        if e["required"]:
            required.append(e)
    if nfa is False and not required:
        bad("missing-answer-key-expectation",
            "noFindingsAcceptable is false but no expected finding is required, "
            "so nothing distinguishes a correct review from an empty one")
    rnd = docs.get("review-round")
    if rnd is not None and key.get("roundId") != get(rnd, "metadata.roundId"):
        bad("shared-round-id", f"answer key roundId {key.get('roundId')!r} is not the packet's "
            f"{get(rnd, 'metadata.roundId')!r}")

    rep = docs.get("review-report")
    if rep is not None:
        findings = [f for f in get(rep, "findings") if isinstance(f, dict)] \
            if isinstance(get(rep, "findings"), list) else []
        if not findings and nfa is False:
            bad("no-findings-against-planted-defect",
                "the report has no findings, but the answer key says this fixture holds a defect "
                "a correct review finds", "review-report")
        for e in required:
            hit = any(get(f, "location.path") in e["locationPaths"]
                      and SEVERITY_RANK.get(f.get("severity"), -1) >= SEVERITY_RANK[e["minimumSeverity"]]
                      for f in findings)
            if findings and not hit:
                bad("required-finding-missing",
                    f"no finding at {' or '.join(e['locationPaths'])} with severity "
                    f"{e['minimumSeverity']} or higher matches expected finding {e.get('id')!r}",
                    "review-report")

    dec = docs.get("operator-decision")
    want = key.get("expectedDecision")
    if isinstance(get(dec, "decision"), dict) and isinstance(want, str) \
       and get(dec, "alignment.status") == "matched" \
       and get(dec, "decision.status") != want:
        bad("expected-decision",
            f"decision.status is {get(dec, 'decision.status')!r}; the answer key expects {want!r}",
            "operator-decision")
    return out


# Matrix relay-required: a normal local round needs no relay or routing data.
RELAY_FIELDS = ("transport", "relayEventId", "relayThreadId", "requestId", "eventId", "threadId",
                "event_id", "thread_id", "request_id", "from", "to", "capabilities", "capabilityProfile")


def relay_required(node, where, errors):
    """Refuse a schema that makes a relay or routing field required."""
    if isinstance(node, dict):
        for name in node.get("required", []) if isinstance(node.get("required"), list) else []:
            if name in RELAY_FIELDS:
                errors.append(f"{where}: relay-required: {name!r} is required; a local round must "
                              "not need relay, routing or capability data")
        for key, child in node.items():
            if key != "required":
                relay_required(child, f"{where}/{key}", errors)
    elif isinstance(node, list):
        for i, child in enumerate(node):
            relay_required(child, f"{where}/{i}", errors)


def load_schemas(schema_dir):
    schemas, errors = {}, []
    for kind in KINDS:
        path = os.path.join(schema_dir, kind + ".json")
        try:
            with open(path, encoding="utf-8") as f:
                schemas[kind] = json.load(f)
        except (OSError, ValueError) as e:
            raise SchemaError(f"{path}: cannot load schema: {e}")
        check_keywords(schemas[kind], path, errors)
        relay_required(schemas[kind], path, errors)
    if errors:
        raise SchemaError("\n".join(errors))
    return schemas


def round_findings(docs):
    """Cross-artifact and answer-key findings for one round's documents, as
    (artifact, invariant, message) triples, and the answer key path if any."""
    found = cross_check(docs)
    key_path = get(docs.get("review-round", {}), "fixture.answerKey")
    if isinstance(key_path, str) and not repo_relative(key_path):
        full = os.path.join(REPO_ROOT, key_path)
        try:
            with open(full, encoding="utf-8") as f:
                found.extend(answer_key_check(json.load(f), docs))
        except (OSError, ValueError) as e:
            found.append(("review-round", "answer-key-readable",
                          f"fixture.answerKey {key_path!r} cannot be read: {e}"))
    return found, key_path


REVISION = re.compile(r"^([0-9a-f]{40}|[0-9a-f]{64})$")


def repo_findings(docs, repo):
    """With --repo: each commit a record cites exists in that repository, and
    each references commit holds the record at its artifactPath. Without
    it, commits are checked only for format."""
    found = []

    def has(obj):
        return subprocess.run(["git", "-C", repo, "cat-file", "-e", obj],
                              capture_output=True).returncode == 0

    for kind in ("review-report", "operator-decision"):
        commit = get(docs.get(kind, {}), "provenance.commit")
        if isinstance(commit, str) and REVISION.match(commit) and not has(commit + "^{commit}"):
            found.append((kind, "commit-in-repo",
                          f"provenance.commit {commit} is not a commit in {repo}"))
    for ref in ("reviewRound", "reviewReport"):
        commit = get(docs.get("operator-decision", {}), f"references.{ref}.commit")
        path = get(docs.get("operator-decision", {}), f"references.{ref}.artifactPath")
        if not (isinstance(commit, str) and REVISION.match(commit)):
            continue
        if not has(commit + "^{commit}"):
            found.append(("operator-decision", "commit-in-repo",
                          f"references.{ref}.commit {commit} is not a commit in {repo}"))
        elif isinstance(path, str) and not repo_relative(path) and not has(f"{commit}:{path}"):
            found.append(("operator-decision", "commit-in-repo",
                          f"references.{ref}.commit {commit} does not hold {path!r}"))
    return found


BASE_CASE = os.path.join("valid", "valid-complete-round")


def run_cases(cases_dir, schemas):
    """Check a schema-cases directory against its cases.json. Returns
    (problems, number of cases). A pass case must meet its schema, and its
    directory must pass as a round. A fail case must be refused, by its
    schema or, put in place of its kind in the valid-complete-round
    documents, by the cross-artifact and answer-key checks."""
    problems = []
    try:
        with open(os.path.join(cases_dir, "cases.json"), encoding="utf-8") as f:
            cases = json.load(f)["cases"]
    except (OSError, ValueError, KeyError, TypeError) as e:
        return [f"{cases_dir}/cases.json: cannot read a cases list: {e}"], 0
    base = os.path.join(cases_dir, BASE_CASE)
    rounds = set()
    for i, case in enumerate(cases):
        file, kind, expect = (case.get(k) if isinstance(case, dict) else None
                              for k in ("file", "schema", "expect"))
        where = f"{cases_dir}/cases.json case {i} ({file})"
        if kind not in KINDS or expect not in ("pass", "fail") or not isinstance(file, str):
            problems.append(f"{where}: needs file, schema ({', '.join(KINDS)}) and expect (pass or fail)")
            continue
        try:
            with open(os.path.join(cases_dir, file), encoding="utf-8") as f:
                doc = json.load(f)
        except (OSError, ValueError) as e:
            problems.append(f"{where}: cannot read: {e}")
            continue
        errors = []
        validate(doc, schemas[kind], schemas[kind], "$", errors)
        if expect == "pass":
            if errors:
                problems.append(f"{where}: expected to pass its schema, got: {errors[0]}")
            rounds.add(os.path.dirname(os.path.join(cases_dir, file)))
        elif not errors:
            docs = {}
            for k in KINDS:
                try:
                    with open(os.path.join(base, k + ".json"), encoding="utf-8") as f:
                        docs[k] = json.load(f)
                except (OSError, ValueError) as e:
                    problems.append(f"{where}: passes its schema, and {base} cannot be read "
                                    f"to plant it: {e}")
                    break
            else:
                base_id = get(docs["review-round"], "metadata.roundId")
                if get(doc, "metadata.roundId") != base_id:
                    problems.append(f"{where}: passes its schema, and is from round "
                                    f"{get(doc, 'metadata.roundId')!r}, not {BASE_CASE}'s "
                                    f"{base_id!r}, so the cross-artifact checks cannot judge it")
                    continue
                docs[kind] = doc
                if not round_findings(docs)[0]:
                    problems.append(f"{where}: expected to fail, but its schema and the cross-artifact "
                                    f"checks, with it planted in {BASE_CASE}, both accept it")
    for round_dir in sorted(rounds):
        problems.extend(check_round(round_dir, schemas))
    return problems, len(cases)


def check_round(round_dir, schemas, repo=None):
    """Return problem lines for one round directory. Each names the round,
    the artifact and the violated invariant."""
    problems, docs, reported = [], {}, {}
    for kind in KINDS:
        path = os.path.join(round_dir, kind + ".json")
        if not os.path.exists(path):
            continue
        try:
            with open(path, encoding="utf-8") as f:
                docs[kind] = json.load(f)
        except (OSError, ValueError) as e:
            problems.append(f"{path}: cannot read: {e}")
            continue
        errors = []
        validate(docs[kind], schemas[kind], schemas[kind], "$", errors)
        problems.extend(f"{path}: schema: {e}" for e in errors)
        reported[kind] = schema_missing_paths(errors)
    if not docs and not problems:
        problems.append(f"{round_dir}: no round documents ({', '.join(k + '.json' for k in KINDS)})")
    round_id = next((get(d, "metadata.roundId") for d in docs.values()
                     if isinstance(get(d, "metadata.roundId"), str)), "?")
    found, key_path = round_findings(docs)
    if repo is not None:
        found.extend(repo_findings(docs, repo))
    for kind, invariant, message in found:
        # A section the schema already reported missing is not reported
        # again by the spec layer.
        m = SPEC_MISSING.match(message) if invariant == "spec-required-field" else None
        if m and m.group(1) in reported.get(kind, ()):
            continue
        if kind == "answer-key":
            where = key_path
        else:
            where = os.path.join(round_dir, kind + ".json") if kind in KINDS else round_dir
        problems.append(f"round {round_id}: {where}: {invariant}: {message}")
    return problems


def selftest():
    """Each keyword must reject a planted bad instance and accept a good one."""
    root = {
        "definitions": {"rev": {"type": "string", "pattern": "^[0-9a-f]{40}$"}},
        "type": "object",
        "additionalProperties": False,
        "required": ["kind", "at", "rev", "tags", "note", "mode"],
        "properties": {
            "kind": {"const": "ReviewRound"},
            "at": {"type": "string", "format": "date-time"},
            "rev": {"$ref": "#/definitions/rev"},
            "tags": {"type": "array", "minItems": 1, "items": {"type": "string", "minLength": 1}},
            "note": {"type": ["string", "null"]},
            "mode": {"enum": ["a", "b"]},
            "extra": {"type": "object", "additionalProperties": {"type": "integer"}},
            "line": {"type": "integer", "minimum": 1},
            "flag": {"const": 1},
            "pick": {"enum": [0, "x"]},
        },
        "if": {"required": ["mode"], "properties": {"mode": {"const": "b"}}},
        "then": {"required": ["line"]},
        "else": {"properties": {"note": {"type": "null"}}},
    }
    good = {"kind": "ReviewRound", "at": "2026-10-31T09:40:06-07:00", "rev": "a" * 40,
            "tags": ["x"], "note": None, "mode": "a", "extra": {"n": 1}, "flag": 1, "pick": 0}
    plants = {
        "const": {"kind": "ReviewReport"},
        "format date-time": {"at": "2026-10-31"},
        "format date-time offset": {"at": "2026-10-31T09:40:06"},
        "$ref pattern": {"rev": "abc"},
        "minItems": {"tags": []},
        "minLength": {"tags": [""]},
        "type list": {"note": 3},
        "enum": {"mode": "c"},
        "additionalProperties false": {"surprise": 1},
        "additionalProperties schema": {"extra": {"n": "1"}},
        "minimum": {"line": 0},
        "if/then": {"mode": "b"},
        "if/else": {"note": "set"},
        "const type-strict": {"flag": True},
        "enum type-strict": {"pick": False},
    }
    failed = 0
    errors = []
    validate(good, root, root, "$", errors)
    if errors:
        print(f"selftest FAIL: the good instance was rejected: {errors}")
        failed += 1
    for name, patch in plants.items():
        bad = dict(good, **patch)
        errors = []
        validate(bad, root, root, "$", errors)
        if not errors:
            print(f"selftest FAIL: planted {name} was not rejected")
            failed += 1
    for name, patch in {"then branch satisfied": {"mode": "b", "line": 1, "note": "set"},
                        "minimum boundary": {"line": 1}, "const 1.0 equals 1": {"flag": 1.0}}.items():
        errors = []
        validate(dict(good, **patch), root, root, "$", errors)
        if errors:
            print(f"selftest FAIL: good instance ({name}) was rejected: {errors}")
            failed += 1
    errors = []
    check_keywords(root, "plant", errors)
    check_keywords({"if": {"properties": {"x": {"oneOf": []}}}}, "plant", errors)
    if len(errors) != 1:
        print(f"selftest FAIL: keyword guard inside if gave {errors}")
        failed += 1
    missing = dict(good)
    del missing["rev"]
    errors = []
    validate(missing, root, root, "$", errors)
    if not any("missing required field 'rev'" in e for e in errors):
        print("selftest FAIL: planted missing required field was not rejected")
        failed += 1
    errors = []
    check_keywords({"properties": {"x": {"oneOf": []}}}, "plant", errors)
    if not errors:
        print("selftest FAIL: an unimplemented keyword was not refused")
        failed += 1
    try:
        resolve_ref("other.json#/x", root)
        print("selftest FAIL: a cross-file $ref was not refused")
        failed += 1
    except SchemaError:
        pass
    relay_ok = True
    errors = []
    relay_required({"properties": {"transport": {"required": ["relayEventId"]}}, "required": ["kind", "transport"]},
                   "plant", errors)
    if len(errors) != 2:
        print(f"selftest FAIL: planted relay requirements gave {len(errors)} of 2 refusals")
        relay_ok = False
    errors = []
    relay_required(root, "plant", errors)
    if errors:
        print(f"selftest FAIL: a schema with no relay requirement was refused: {errors}")
        relay_ok = False
    if relay_ok:
        COVERED.add("relay-required")
    else:
        failed += 1
    engine_cases = len(plants) + 10
    cross_failed, cross_cases = selftest_cross()
    failed += cross_failed
    cases_failed, cases_cases = selftest_cases()
    failed += cases_failed
    cross_cases += cases_cases
    # The gate's own plant copies only this script and the schemas into a bare
    # tree. With no examples/review-round there, the fixture checks have
    # nothing to read; once the directory exists, a missing file fails.
    fixture_present = os.path.isdir(os.path.join(REPO_ROOT, "examples", "review-round"))
    if not fixture_present:
        print("selftest skip: no examples/review-round in this tree, so the templates and"
              " history are not checked")
    tmpl_failed, tmpl_cases = selftest_templates() if fixture_present else (0, 0)
    failed += tmpl_failed
    cross_cases += tmpl_cases
    hist_failed, hist_cases = selftest_history() if fixture_present else (0, 0)
    failed += hist_failed
    cross_cases += hist_cases
    cwd_failed, cwd_cases = selftest_cwd() if fixture_present else (0, 0)
    failed += cwd_failed
    cross_cases += cwd_cases
    repo_failed, repo_cases = selftest_repo() if fixture_present else (0, 0)
    failed += repo_failed
    cross_cases += repo_cases
    roles_failed, roles_cases = selftest_roles()
    failed += roles_failed
    cross_cases += roles_cases
    edge_failed, edge_cases = selftest_edges()
    failed += edge_failed
    cross_cases += edge_cases
    for row in MATRIX_ROWS:
        if row in MATRIX_PENDING:
            print(f"selftest note: matrix row {row} pending: {MATRIX_PENDING[row]}")
        elif row not in COVERED:
            print(f"selftest FAIL: matrix row {row} has no case that behaved")
            failed += 1
    covered = sum(1 for row in MATRIX_ROWS if row in COVERED)
    print(f"round-check selftest: matrix rows covered {covered} of {len(MATRIX_ROWS)}"
          f"{f', {len(MATRIX_PENDING)} pending' if MATRIX_PENDING else ''}")
    total = engine_cases + cross_cases
    print(f"round-check selftest: {total - failed} of {total} cases behaved")
    return 1 if failed else 0


def selftest_edges():
    """Edge cases of the engine, the cross-artifact and answer-key checks,
    check_round and the command line, each pinned to the result it gives."""
    def trio(edit):
        docs = copy.deepcopy(valid_trio())
        edit(docs)
        return docs

    def fired(found):
        return {inv for _, inv, _ in found}

    def errs(fn, *args):
        out = []
        fn(*args, out)
        return out

    def dec_alone(d):
        del d["review-round"], d["review-report"]
        del d["operator-decision"]["verification"]["performedBy"]
        d["operator-decision"]["alignment"] = {"status": "mismatched"}

    def key(**kw):
        k = valid_key()
        k.update(kw)
        return k

    def cli(*args):
        return subprocess.run([sys.executable, os.path.abspath(__file__), *args],
                              capture_output=True, text=True).returncode

    def round_dir(text):
        with tempfile.TemporaryDirectory(prefix="round-check-edge.") as tmp:
            with open(os.path.join(tmp, "review-round.json"), "w", encoding="utf-8") as f:
                f.write(text)
            return check_round(tmp, load_schemas(os.path.join(REPO_ROOT, SCHEMA_DIR)))

    def no_findings(d):
        d["review-report"]["findings"] = []

    def severity(value):
        return lambda d: d["review-report"]["findings"][0].update(severity=value)

    cases = {
        "date-time with a lower-case t": lambda: is_date_time("2026-10-31t09:40:06Z"),
        "date-time with a lower-case z": lambda: is_date_time("2026-10-31T09:40:06z"),
        "objects with other keys differ": lambda: json_equal({"a": 1}, {"b": 1}) is False,
        "lists of other lengths differ": lambda: json_equal([1], [1, 2]) is False,
        "a type mismatch stops there": lambda: len(errs(validate, 5, {"type": "string", "const": "x"},
                                                        {}, "$")) == 1,
        "pattern matches anywhere": lambda: errs(validate, "xab", {"pattern": "ab"}, {}, "$") == [],
        "keyword guard inside else": lambda: len(errs(check_keywords, {"else": {"oneOf": []}}, "p")) == 1,
        "a drive letter is absolute": lambda: repo_relative("C:/x") == "is absolute",
        "mismatched with no revisions is not equal":
            lambda: not any("revisions are equal" in m for _, _, m in cross_check(trio(dec_alone))),
        "a decision alone names no unknown finding": lambda: "finding-exists" not in fired(cross_check(trio(dec_alone))),
        "no reviewer role, no self-verification":
            lambda: "independent-verification" not in fired(cross_check(trio(dec_alone))),
        "unresolved cannot accept": lambda: any("relies on a report" in m for _, _, m in cross_check(trio(
            lambda d: d["operator-decision"]["alignment"].update(status="unresolved")
            or d["operator-decision"]["decision"].update(status="accept")))),
        "cited with no evidence": lambda: "cites-reproduced-only" in fired(cross_check(trio(
            lambda d: d["operator-decision"]["verification"]["findings"][0].update(evidence=[])))),
        "noFindingsAcceptable not boolean, no expectation finding":
            lambda: "missing-answer-key-expectation" not in fired(answer_key_check(
                key(noFindingsAcceptable=None, expectedFindings=[]), valid_trio())),
        "noFindingsAcceptable not boolean, empty report":
            lambda: "no-findings-against-planted-defect" not in fired(answer_key_check(
                key(noFindingsAcceptable=None), trio(no_findings))),
        "an unknown severity is below nit": lambda: "required-finding-missing" in fired(answer_key_check(
            key(expectedFindings=[dict(valid_key()["expectedFindings"][0], minimumSeverity="nit")]),
            trio(severity("critical")))),
        "an empty report misses no required finding": lambda: "required-finding-missing" not in fired(
            answer_key_check(key(noFindingsAcceptable=True), trio(no_findings))),
        "an absolute answer key is not read": lambda: "answer-key-readable" not in fired(round_findings(trio(
            lambda d: d["review-round"].update(fixture={"answerKey": "/nonexistent/answer-key.json"})))[0]),
        "a non-string roundId names round ?":
            lambda: {p.split(":")[0] for p in round_dir('{"metadata": {"roundId": 5}}')
                     if p.startswith("round ")} == {"round ?"},
        "an unreadable document is not a missing one":
            lambda: not any("no round documents" in p for p in round_dir("{")),
        "--cases after --repo is a usage error": lambda: cli("--repo", REPO_ROOT, "--cases", REPO_ROOT) == 2,
        "a dash argument is a usage error": lambda: cli("--bogus") == 2,
        "--repo that is not a directory": lambda: cli("--repo", os.path.join(REPO_ROOT, "no-such-dir"), "x") == 2,
    }
    failed = 0
    for name, case in cases.items():
        try:
            ok = case()
        except Exception as e:  # a crash is a case that did not behave
            ok, name = False, f"{name} ({type(e).__name__}: {e})"
        if not ok:
            print(f"selftest FAIL: edge case {name} did not behave")
            failed += 1
    return failed, len(cases)


def selftest_cases():
    """--cases on a cases directory built from valid_trio, with schemas that
    accept anything, so only the expectations and the cross-artifact plant
    decide. One good set must raise nothing; each wrong expectation must."""
    open_schemas = {k: {} for k in KINDS}
    trio = valid_trio()
    cites_unverified = copy.deepcopy(trio["operator-decision"])
    cites_unverified["verification"]["findings"][0]["status"] = "not-reproduced"
    other_round = copy.deepcopy(trio["operator-decision"])
    other_round["metadata"]["roundId"] = "another-round"
    good = [(BASE_CASE + "/" + k + ".json", k, "pass") for k in KINDS] + \
        [("invalid/cites-unverified.json", "operator-decision", "fail")]
    sets = [("good", good, False),
            ("valid document marked fail", good + [(BASE_CASE + "/operator-decision.json",
                                                    "operator-decision", "fail")], True),
            ("invalid document marked pass", good + [("invalid/cites-unverified.json",
                                                      "operator-decision", "pass")], True),
            ("fail case from another round", good + [("invalid/other-round.json",
                                                      "operator-decision", "fail")], True)]
    failed = 0
    for name, cases, want in sets:
        with tempfile.TemporaryDirectory(prefix="round-check-cases.") as tmp:
            os.makedirs(os.path.join(tmp, BASE_CASE))
            os.makedirs(os.path.join(tmp, "invalid"))
            files = {BASE_CASE + "/" + k + ".json": trio[k] for k in KINDS}
            files["invalid/cites-unverified.json"] = cites_unverified
            files["invalid/other-round.json"] = other_round
            for rel, doc in files.items():
                with open(os.path.join(tmp, rel), "w", encoding="utf-8") as f:
                    json.dump(doc, f)
            with open(os.path.join(tmp, "cases.json"), "w", encoding="utf-8") as f:
                json.dump({"cases": [{"file": a, "schema": b, "expect": c} for a, b, c in cases]}, f)
            problems, _ = run_cases(tmp, open_schemas)
        if bool(problems) != bool(want):
            print(f"selftest FAIL: --cases {name}: wanted {'problems' if want else 'none'}, "
                  f"got {problems or 'none'}")
            failed += 1
    return failed, len(sets)


# The templates adopters copy, and the kind each must be. A template that
# drops a field artifactRequirements needs fails here, not in someone's round.
TEMPLATES = (("examples/review-round/reviewer/templates/review-report.template.json", "review-report"),
             ("examples/review-round/verifier/templates/operator-decision.template.json",
              "operator-decision"))


def selftest_templates():
    """Each template against SPEC: schemaVersion, kind and every required
    path present. Placeholder values are fine; missing fields are not."""
    failed = 0
    for rel, kind in TEMPLATES:
        try:
            with open(os.path.join(REPO_ROOT, rel), encoding="utf-8") as f:
                doc = json.load(f)
        except (OSError, ValueError) as e:
            print(f"selftest FAIL: template {rel} cannot be read: {e}")
            failed += 1
            continue
        found = spec_check({kind: doc})
        if found:
            print(f"selftest FAIL: template {rel} misses what artifactRequirements needs: "
                  f"{'; '.join(m for _, _, m in found)}")
            failed += 1
    return failed, len(TEMPLATES)


def selftest_history():
    """Run the fixture's history/build.sh, so a patch that drifts from
    revisions.json fails here and not only in a hand run. Then plant a drift in
    a copy of the history and check that build.sh refuses it."""
    history = os.path.join(REPO_ROOT, "examples", "review-round", "history")
    if not os.path.isfile(os.path.join(history, "build.sh")):
        print("selftest FAIL: examples/review-round/history/build.sh is missing")
        return 1, 1
    if shutil.which("git") is None:
        print("selftest FAIL: git is needed to build the fixture history")
        return 1, 1
    failed = 0
    with tempfile.TemporaryDirectory(prefix="round-check-history.") as tmp:
        def build(hist, out):
            return subprocess.run(["sh", os.path.join(hist, "build.sh"), os.path.join(tmp, out)],
                                  capture_output=True, text=True).returncode
        rc = build(history, "built")
        if rc != 0:
            print(f"selftest FAIL: history/build.sh exited {rc}; the fixture patches drifted"
                  " from revisions.json")
            failed += 1
        drifted = os.path.join(tmp, "history")
        shutil.copytree(history, drifted)
        rev = os.path.join(drifted, "revisions.json")
        with open(rev, encoding="utf-8") as f:
            text = f.read()
        with open(rev, "w", encoding="utf-8") as f:
            f.write(re.sub(r'("targetRevision": *")[0-9a-f]', r"\g<1>x", text, count=1))
        rc = build(drifted, "drifted")
        if rc != 1:
            print(f"selftest FAIL: build.sh exited {rc} on planted drift; wanted 1")
            failed += 1
    return failed, 2


# The handoff's validationMatrix rows. The selftest fails when a row has no
# case that behaved, unless it is listed in MATRIX_PENDING with the reason.
MATRIX_ROWS = (
    "valid-complete-round", "valid-no-findings-when-answer-key-allows",
    "valid-verification-rejects-finding", "reviewed-wrong-revision", "self-verification",
    "decision-cites-unverified-finding", "missing-verification-evidence", "missing-check-status",
    "missing-answer-key-expectation", "unqualified-accept-with-reproduced-blocker", "relay-required")
MATRIX_PENDING = {}
MATRIX_OF = {
    "revision-alignment": "reviewed-wrong-revision",
    "independent-verification": "self-verification",
    "report-findings-unverified": "self-verification",
    "cites-reproduced-only": "decision-cites-unverified-finding",
    "reproduction-evidence": "missing-verification-evidence",
    "explicit-check-status": "missing-check-status",
    "missing-answer-key-expectation": "missing-answer-key-expectation",
    "accept-needs-exception": "unqualified-accept-with-reproduced-blocker",
}
COVERED = set()


def valid_trio():
    """A complete, consistent round: the planted defect reported, reproduced
    by a different role with evidence, and a request-revision decision."""
    target = "1" * 40
    meta = lambda i: {"id": i, "roundId": "selftest-round", "createdAt": "2026-10-31T10:00:00Z"}
    handling = {"visibility": "public", "redaction": "none"}
    rnd = {"schemaVersion": "tpkit.review-round/v1alpha1", "kind": "ReviewRound",
           "metadata": meta("round-1"), "handling": handling,
           "provenance": {"repository": "selftest", "baseRevision": "0" * 40,
                          "targetRevision": target, "artifactPath": "rounds/review-round.json"},
           "roles": {"reviewer": {"role": "aide"}, "verifier": {"role": "lead"},
                     "decisionMaker": {"role": "operator"}},
           "scope": {"paths": ["docs/guide.md"], "intent": "selftest"},
           "requiredChecks": [{"id": "gates", "command": "./scripts/gates.sh"}],
           "restrictions": {"network": "prohibited", "secrets": "prohibited", "remoteAccess": "prohibited"}}
    rep = {"schemaVersion": "tpkit.review-report/v1alpha1", "kind": "ReviewReport",
           "metadata": meta("report-1"), "handling": handling, "reviewer": {"role": "aide"},
           "reviewedRevision": {"revision": target, "evidence": [{"description": "git rev-parse HEAD"}]},
           "checks": [{"id": "gates", "status": "passed"}],
           "findings": [{"id": "f1", "severity": "major", "location": {"path": "docs/guide.md"},
                         "claim": "c", "evidence": [{"description": "e"}], "proposedRemedy": "r",
                         "verification": {"status": "unverified", "verifiedBy": None, "evidence": []}}],
           "recommendation": {"status": "request-revision", "rationale": "r"},
           "limitations": [], "provenance": {"artifactPath": "rounds/review-report.json", "commit": "2" * 40}}
    dec = {"schemaVersion": "tpkit.operator-decision/v1alpha1", "kind": "OperatorDecision",
           "metadata": meta("decision-1"), "handling": handling,
           "references": {"reviewRound": {"artifactPath": "rounds/review-round.json", "commit": "3" * 40},
                          "reviewReport": {"artifactPath": "rounds/review-report.json", "commit": "2" * 40}},
           "alignment": {"packetTargetRevision": target, "reportReviewedRevision": target, "status": "matched"},
           "verification": {"performedBy": {"role": "lead"}, "performedAt": "2026-10-31T11:00:00Z",
                            "findings": [{"findingId": "f1", "status": "reproduced",
                                          "evidence": [{"description": "reproduced"}]}]},
           "decision": {"madeBy": {"role": "operator"}, "status": "request-revision",
                        "basedOnFindings": ["f1"], "rationale": "r"},
           "provenance": {"artifactPath": "rounds/operator-decision.json", "commit": "4" * 40}}
    return {"review-round": rnd, "review-report": rep, "operator-decision": dec}


def roles_md_names(text):
    """The role headings under "## The four" in ROLES.md, lower case, with
    a plural heading ("Minions") read as its role ("minion")."""
    names, inside = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            inside = line.strip() == "## The four"
        elif inside and line.startswith("### "):
            name = line[4:].strip().lower()
            names.append(name[:-1] if name.endswith("s") and name[:-1] in ROLES else name)
    return names


def role_list_problems(roles_md_text, schemas):
    """Every copy of the role list must equal the roles ROLES.md defines:
    ROLES here and each schema's role enum."""
    want = roles_md_names(roles_md_text)
    out = []
    if sorted(want) != sorted(ROLES):
        out.append(f"ROLES.md defines {want}; round-check.py ROLES is {list(ROLES)}")
    for kind, schema in sorted(schemas.items()):
        enum = schema.get("definitions", {}).get("role", {}).get("enum")
        if enum is None or sorted(enum) != sorted(want):
            out.append(f"{kind}.json role enum is {enum}; ROLES.md defines {want}")
    return out


def selftest_cwd():
    """Run this script on the expected round from a directory outside the
    repository, so a path read relative to the current directory fails here."""
    expected = os.path.join(REPO_ROOT, "examples", "review-round", "verifier", "expected")
    with tempfile.TemporaryDirectory(prefix="round-check-cwd.") as tmp:
        run = subprocess.run([sys.executable, os.path.abspath(__file__), expected],
                             cwd=tmp, capture_output=True, text=True)
    if run.returncode != 0:
        last = (run.stdout + run.stderr).strip().splitlines()[:1]
        print(f"selftest FAIL: run from outside the repository, the expected round exited"
              f" {run.returncode}: {last}")
        return 1, 1
    return 0, 1


def selftest_repo():
    """With --repo, the commits a round cites must exist there, and each
    references commit must hold its artifactPath. Commit the expected round
    into a scratch repository, point the records at real commits, then plant
    a missing commit and a commit without the record."""
    if shutil.which("git") is None:
        print("selftest FAIL: git is needed to check --repo")
        return 1, 1
    expected = os.path.join(REPO_ROOT, "examples", "review-round", "verifier", "expected")
    failed, cases = 0, 0
    with tempfile.TemporaryDirectory(prefix="round-check-repo.") as repo:
        def git(*args):
            return subprocess.run(["git", "-C", repo, "-c", "user.name=selftest",
                                   "-c", "user.email=selftest@example.invalid", *args],
                                  capture_output=True, text=True, check=True).stdout.strip()
        git("init", "-q")
        rdir = os.path.join(repo, "r")
        os.makedirs(rdir)
        docs = {}
        for kind in KINDS:
            with open(os.path.join(expected, kind + ".json"), encoding="utf-8") as f:
                docs[kind] = json.load(f)
        commits = {}
        for kind in KINDS[:2]:
            docs[kind]["provenance"]["artifactPath"] = f"r/{kind}.json"
            if kind == "review-report":
                docs[kind]["provenance"]["commit"] = commits["review-round"]
            with open(os.path.join(rdir, kind + ".json"), "w", encoding="utf-8") as f:
                json.dump(docs[kind], f)
            git("add", "-A")
            git("commit", "-q", "-m", kind)
            commits[kind] = git("rev-parse", "HEAD")
        dec = docs["operator-decision"]
        dec["provenance"].update(artifactPath="r/operator-decision.json",
                                 commit=commits["review-report"])
        dec["references"]["reviewRound"].update(artifactPath="r/review-round.json",
                                                commit=commits["review-round"])
        dec["references"]["reviewReport"].update(artifactPath="r/review-report.json",
                                                 commit=commits["review-report"])
        good = copy.deepcopy(dec)
        plants = {"valid": None,
                  "missing commit": ("reviewReport", "commit", "f" * 40),
                  "commit without the record": ("reviewReport", "commit", commits["review-round"])}
        for name, plant in plants.items():
            dec = copy.deepcopy(good)
            if plant:
                dec["references"][plant[0]][plant[1]] = plant[2]
            with open(os.path.join(rdir, "operator-decision.json"), "w", encoding="utf-8") as f:
                json.dump(dec, f)
            fired = {inv for _, inv, _ in repo_findings(docs | {"operator-decision": dec}, repo)}
            cases += 1
            if plant is None and fired:
                print(f"selftest FAIL: --repo on a round with real commits found {sorted(fired)}")
                failed += 1
            elif plant is not None and "commit-in-repo" not in fired:
                print(f"selftest FAIL: --repo did not catch a planted {name}")
                failed += 1
        # A provenance.commit that names a tree, not a commit, is caught; a
        # references artifactPath that is not repository-relative is the
        # path check's to report, so --repo does not look it up.
        tree = copy.deepcopy(good)
        tree["provenance"]["commit"] = git("rev-parse", commits["review-report"] + "^{tree}")
        absolute = copy.deepcopy(good)
        absolute["references"]["reviewRound"]["artifactPath"] = "/r/review-round.json"
        for name, dec, want in (("tree as provenance.commit", tree, True),
                                ("absolute references artifactPath", absolute, False)):
            cases += 1
            got = "commit-in-repo" in {inv for _, inv, _ in repo_findings(docs | {"operator-decision": dec}, repo)}
            if got != want:
                print(f"selftest FAIL: --repo on a {name} {'missed' if want else 'raised'} commit-in-repo")
                failed += 1
    return failed, cases


def selftest_roles():
    """The four copies of the role list agree with orchestration/ROLES.md,
    and a fifth role planted in ROLES.md is caught."""
    path = os.path.join(REPO_ROOT, "orchestration", "ROLES.md")
    if not os.path.exists(path):
        print("selftest skip: no orchestration/ROLES.md in this tree, so the role lists are not compared")
        return 0, 0
    with open(path, encoding="utf-8") as f:
        text = f.read()
    schemas = load_schemas(os.path.join(REPO_ROOT, SCHEMA_DIR))
    failed = 0
    problems = role_list_problems(text, schemas)
    if problems:
        print(f"selftest FAIL: role lists disagree with ROLES.md: {problems}; update all four by hand")
        failed += 1
    planted = text.replace("## How authority moves", "### Auditor\n\n## How authority moves", 1)
    if planted == text or not role_list_problems(planted, schemas):
        print("selftest FAIL: a fifth role planted in ROLES.md was not caught")
        failed += 1
    return failed, 2


def selftest_cross():
    """Each invariant must fire on its planted violation; the valid round must raise nothing."""

    def plant(edit):
        docs = copy.deepcopy(valid_trio())
        edit(docs)
        return docs

    def setp(kind, dotted, value):
        def edit(docs):
            node = docs[kind]
            parts = dotted.split(".")
            for part in parts[:-1]:
                node = node[part] if not isinstance(node, list) else node[int(part)]
            if isinstance(node, list):
                node[int(parts[-1])] = value
            else:
                node[parts[-1]] = value
        return edit

    def delp(kind, dotted):
        def edit(docs):
            node = docs[kind]
            parts = dotted.split(".")
            for part in parts[:-1]:
                node = node[part] if not isinstance(node, list) else node[int(part)]
            del node[parts[-1]]
        return edit

    other = "9" * 40
    cases = [
        ("accept-needs-exception", setp("operator-decision", "decision.status", "accept")),
        ("accept-needs-exception", lambda d: d["operator-decision"]["decision"].update(
            status="accept", exceptions=[{"findingId": "f1", "reason": " "}])),
        ("accept-needs-exception", lambda d: d["operator-decision"]["decision"].update(
            status="accept", exceptions=[{"findingId": "f2", "reason": "not this finding"}])),
        ("spec-required-field", delp("review-round", "restrictions")),
        ("restrictions-posture", delp("review-round", "restrictions.secrets")),
        ("restrictions-posture", setp("review-round", "restrictions.network", " ")),
        ("restrictions-posture", setp("review-round", "restrictions.remoteAccess", None)),
        ("restrictions-posture", setp("review-round", "restrictions", {})),
        ("spec-required-field", delp("review-round", "roles.decisionMaker")),
        ("spec-required-field", delp("review-report", "reviewedRevision.evidence")),
        ("spec-required-field", delp("review-report", "findings.0.proposedRemedy")),
        ("spec-required-field", delp("review-report", "findings.0.verification.verifiedBy")),
        # A later finding: a second one, complete except for proposedRemedy.
        ("spec-required-field", lambda d: d["review-report"]["findings"].append(
            {k: v for k, v in copy.deepcopy(d["review-report"]["findings"][0]).items()
             if k != "proposedRemedy"} | {"id": "f2"})),
        # Two findings with one id: a verification entry could name only one of them.
        ("finding-id-unique", lambda d: d["review-report"]["findings"].append(
            copy.deepcopy(d["review-report"]["findings"][0]) | {"severity": "minor"})),
        ("spec-required-field", delp("operator-decision", "references.reviewReport.commit")),
        ("spec-required-field", setp("operator-decision", "schemaVersion", "tpkit.operator-decision/v1")),
        ("spec-required-field", setp("review-report", "kind", "Report")),
        ("shared-round-id", setp("review-report", "metadata.roundId", "another-round")),
        ("roles-from-roles-md", setp("review-report", "reviewer.role", "reviewer")),
        ("roles-from-roles-md", setp("review-round", "roles.reviewer.role", "reviewer")),
        ("roles-from-roles-md", setp("review-round", "roles.verifier.role", "verifier")),
        ("roles-from-roles-md", setp("review-round", "roles.decisionMaker.role", "owner")),
        ("roles-from-roles-md", setp("operator-decision", "verification.performedBy.role", "verifier")),
        ("roles-from-roles-md", setp("operator-decision", "decision.madeBy.role", "owner")),
        ("repository-relative-path", setp("review-round", "provenance.artifactPath", "/abs/round.json")),
        ("repository-relative-path", setp("review-round", "scope.paths", ["../outside.md"])),
        ("repository-relative-path", setp("operator-decision", "references.reviewReport.artifactPath", "https://example.invalid/r.json")),
        ("repository-relative-path", setp("review-report", "findings.0.location.path", "https://example.invalid/README.md")),
        ("repository-relative-path", setp("review-report", "findings.0.location.path", "/abs/README.md")),
        ("report-findings-unverified", setp("review-report", "findings.0.verification",
                                            {"status": "reproduced", "verifiedBy": "aide", "evidence": [{"description": "self"}]})),
        # One clause each, the other two left in the initial state.
        ("report-findings-unverified", setp("review-report", "findings.0.verification.status", "reproduced")),
        ("report-findings-unverified", setp("review-report", "findings.0.verification.verifiedBy", "aide")),
        ("report-findings-unverified", setp("review-report", "findings.0.verification.evidence", [{"description": "self"}])),
        ("explicit-check-status", setp("review-report", "checks", [{"id": "gates"}])),
        ("explicit-check-status", setp("review-report", "checks", [])),
        ("explicit-check-status", setp("review-report", "checks", [{"id": "gates", "status": "ok"}])),
        ("explicit-alignment-status", setp("operator-decision", "alignment.status", "ok")),
        ("revision-alignment", lambda d: (setp("review-report", "reviewedRevision.revision", other)(d),
                                          setp("operator-decision", "alignment.reportReviewedRevision", other)(d))),
        ("revision-alignment", lambda d: (setp("review-report", "reviewedRevision.revision", other)(d),
                                          setp("operator-decision", "alignment.reportReviewedRevision", other)(d),
                                          setp("operator-decision", "alignment.status", "mismatched")(d))),
        ("revision-alignment", setp("operator-decision", "alignment.packetTargetRevision", other)),
        # Claims mismatched while both revisions are equal; rerun, so only that branch can fire.
        ("revision-alignment", lambda d: (setp("operator-decision", "alignment.status", "mismatched")(d),
                                          setp("operator-decision", "decision.status", "rerun")(d),
                                          setp("operator-decision", "decision.basedOnFindings", [])(d))),
        # Every role but the operator, and no role at all.
        *[("operator-decides", setp("operator-decision", "decision.madeBy.role", r)) for r in ROLES if r != "operator"],
        ("operator-decides", delp("operator-decision", "decision.madeBy.role")),
        ("independent-verification", setp("operator-decision", "verification.performedBy.role", "aide")),
        # No report: the reviewer's role comes from the round's roles.reviewer.role.
        ("independent-verification", lambda d: (d.pop("review-report"),
                                                setp("operator-decision", "verification.performedBy.role",
                                                     d["review-round"]["roles"]["reviewer"]["role"])(d))),
        ("reproduction-evidence", setp("operator-decision", "verification.findings.0.evidence", [])),
        ("cites-reproduced-only", setp("operator-decision", "verification.findings.0.status", "not-reproduced")),
        ("cites-reproduced-only", setp("operator-decision", "decision.basedOnFindings", ["f9"])),
        ("finding-exists", setp("operator-decision", "verification.findings.0.findingId", "f9")),
        # An unknown id on an entry that is not reproduced, one case per such status.
        *[("finding-exists", lambda d, st=st: d["operator-decision"]["verification"]["findings"].append(
            {"findingId": "f9", "status": st, "evidence": [], "note": "planted"}))
          for st in ("not-reproduced", "not-applicable", "blocked")],
        ("cites-reproduced-only", setp("operator-decision", "verification.findings.0.status", "blocked")),
        ("cites-reproduced-only", setp("operator-decision", "verification.findings.0.status", "not-applicable")),
        ("cites-reproduced-only", setp("operator-decision", "verification.findings", [])),
    ]
    key_failed, key_cases = selftest_answer_key(plant)
    failed = key_failed
    # Each check beside the planted cases goes through extra(), which counts
    # it, so the total below is the number of checks that ran.
    extras = 0

    def extra(problem, message):
        nonlocal failed, extras
        extras += 1
        if problem:
            print(f"selftest FAIL: {message}")
            failed += 1
        return not problem

    clean = cross_check(valid_trio())
    extra(clean, f"the valid round raised {clean}")

    def rejects(d):
        # A second finding, checked by the verifier and not reproduced; not cited.
        f2 = copy.deepcopy(d["review-report"]["findings"][0])
        f2.update(id="f2", severity="minor")
        d["review-report"]["findings"].append(f2)
        d["operator-decision"]["verification"]["findings"].append(
            {"findingId": "f2", "status": "not-reproduced",
             "evidence": [{"description": "followed the reviewer's steps; the behaviour did not occur"}]})
    excepted = cross_check(plant(lambda d: d["operator-decision"]["decision"].update(
        status="accept", exceptions=[{"findingId": "f1", "reason": "accepted for this release; fix tracked"}])))
    extra(excepted, f"an accept with an explicit exception raised {excepted}")
    # The two other alignment statuses, each with a decision allowed for it,
    # are valid rounds: a mismatched revision with rerun, and an unresolved
    # one (the report gives no revision) with abstain.
    def misaligned(status, outcome, reviewed):
        def edit(d):
            d["review-report"]["reviewedRevision"]["revision"] = reviewed
            d["operator-decision"]["alignment"].update(reportReviewedRevision=reviewed, status=status)
            d["operator-decision"]["decision"].update(status=outcome, basedOnFindings=[])
        return edit
    for status, outcome, reviewed in (("mismatched", "rerun", other), ("unresolved", "abstain", None)):
        raised = cross_check(plant(misaligned(status, outcome, reviewed)))
        extra(raised, f"a valid round with alignment {status} and decision {outcome} raised {raised}")
    # An accept needs an exception for each reproduced major finding only:
    # a reproduced minor f2 without one is valid.
    def minor_unexcepted(d):
        f2 = copy.deepcopy(d["review-report"]["findings"][0])
        f2.update(id="f2", severity="minor")
        d["review-report"]["findings"].append(f2)
        d["operator-decision"]["verification"]["findings"].append(
            {"findingId": "f2", "status": "reproduced",
             "evidence": [{"description": "repeated the reviewer's steps; the behaviour occurred"}]})
        d["operator-decision"]["decision"].update(
            status="accept", exceptions=[{"findingId": "f1", "reason": "accepted for this release; fix tracked"}])
    minor = cross_check(plant(minor_unexcepted))
    extra(minor, f"an accept leaving a reproduced minor finding without an exception raised {minor}")
    def unverified_nit(d):
        # A finding the verifier did not check has no entry; the decision does not cite it.
        f2 = copy.deepcopy(d["review-report"]["findings"][0])
        f2.update(id="f2", severity="nit")
        d["review-report"]["findings"].append(f2)
    unchecked = cross_check(plant(unverified_nit))
    extra(unchecked, f"a reported finding with no verification entry, not cited, raised {unchecked}")
    raised = cross_check(plant(rejects)) + answer_key_check(valid_key(), plant(rejects))
    if extra(raised, f"valid-verification-rejects-finding raised {raised}"):
        COVERED.add("valid-verification-rejects-finding")
    # An absent section is named once by the spec layer, not once per
    # subfield, and a section the schema reported is not reported again.
    gone = [m for _, inv, m in spec_check(plant(delp("operator-decision", "decision")))
            if inv == "spec-required-field"]
    extra(gone != ["decision is required by artifactRequirements"], f"an absent decision section gave {gone}")
    # The cross-checks do not then report the absent section's subfields.
    nodec = plant(delp("operator-decision", "decision"))
    again = [p for p in cross_check(nodec) + answer_key_check(valid_key(), nodec)
             if p[1] != "spec-required-field"]
    extra(again, f"an absent decision section also raised {again}")
    extra(schema_missing_paths(["$: missing required field 'decision'",
                                "$.findings[0].verification: missing required field 'evidence'"]) !=
          {"decision", "findings[0].verification.evidence"}, "schema_missing_paths misread a schema message")
    # An absent field must read as "missing" in a message, never as an
    # object's repr.
    absent = cross_check(plant(delp("operator-decision", "decision.madeBy.role")))
    leaked = [m for _, _, m in absent if "<object" in m]
    extra(leaked or not any("madeBy.role is missing" in m for _, _, m in absent),
          f"an absent decision.madeBy.role reads as {[m for _, _, m in absent]}")
    for invariant, edit in cases:
        raised = cross_check(plant(edit))
        leaked = [m for _, _, m in raised if "<object" in m]
        if leaked:
            print(f"selftest FAIL: planted {invariant} message leaks an object repr: {leaked}")
            failed += 1
        fired = {inv for _, inv, _ in raised}
        if invariant not in fired:
            print(f"selftest FAIL: planted {invariant} violation did not fire (fired: {sorted(fired) or 'nothing'})")
            failed += 1
        elif invariant in MATRIX_OF:
            COVERED.add(MATRIX_OF[invariant])
    return failed, len(cases) + extras + key_cases


def valid_key():
    return {"roundId": "selftest-round", "noFindingsAcceptable": False,
            "expectedFindings": [{"id": "planted", "required": True, "minimumSeverity": "major",
                                  "locationPaths": ["docs/guide.md"]}],
            "expectedDecision": "request-revision"}


def selftest_answer_key(plant):
    """The answer-key invariants: each planted case fires its invariant, and
    the two valid rounds (planted defect found; no defect, no findings) raise
    nothing from either check."""
    failed = 0

    def run(edit_docs=None, edit_key=None):
        docs = plant(edit_docs or (lambda d: None))
        key = valid_key()
        if edit_key:
            edit_key(key)
        return docs, key

    def no_findings(d):
        d["review-report"]["findings"] = []
        d["review-report"]["recommendation"]["status"] = "accept"
        d["operator-decision"]["verification"]["findings"] = []
        d["operator-decision"]["decision"].update(status="accept", basedOnFindings=[])

    def allow_none(k):
        k.update(noFindingsAcceptable=True, expectedFindings=[], expectedDecision="accept")

    def unresolved_rerun(d):
        # The report gives no revision, so the expected decision does not
        # apply: rerun differs from it and is valid.
        d["review-report"]["reviewedRevision"]["revision"] = None
        d["operator-decision"]["alignment"].update(reportReviewedRevision=None, status="unresolved")
        d["operator-decision"]["decision"].update(status="rerun", basedOnFindings=[])

    valid = [("valid-complete-round", run()), ("valid-no-findings-when-answer-key-allows", run(no_findings, allow_none)),
             ("valid-unresolved-round-reruns", run(unresolved_rerun))]
    for name, (docs, key) in valid:
        raised = cross_check(docs) + answer_key_check(key, docs)
        if raised:
            print(f"selftest FAIL: {name} raised {raised}")
            failed += 1
        else:
            COVERED.add(name)

    def setkey(field, value):
        return lambda k: k.__setitem__(field, value)

    def finding(field, value):
        def edit(d):
            d["review-report"]["findings"][0].update({field: value} if field != "path"
                                                     else {"location": {"path": value}})
        return edit

    planted = [
        ("no-findings-against-planted-defect", run(no_findings)),
        ("missing-answer-key-expectation", run(edit_key=setkey("expectedFindings", []))),
        ("missing-answer-key-expectation", run(edit_key=lambda k: k["expectedFindings"][0].update(required=False))),
        ("answer-key-shape", run(edit_key=lambda k: k.pop("noFindingsAcceptable"))),
        ("answer-key-shape", run(edit_key=lambda k: k["expectedFindings"][0].update(required="yes"))),
        ("required-finding-missing", run(finding("path", "README.md"))),
        ("required-finding-missing", run(finding("severity", "minor"))),
        ("expected-decision", run(lambda d: d["operator-decision"]["decision"].update(status="reject"))),
        ("shared-round-id", run(edit_key=setkey("roundId", "another-round"))),
        ("answer-key-shape", run(edit_key=setkey("noFindingAcceptable", False))),
        ("answer-key-shape", run(edit_key=lambda k: k["expectedFindings"][0].update(requried=True))),
        ("answer-key-shape", run(edit_key=lambda k: k.pop("roundId"))),
        ("answer-key-shape", run(edit_key=lambda k: k.pop("expectedDecision"))),
        ("answer-key-shape", run(edit_key=setkey("expectedDecision", "approve"))),
        ("answer-key-shape", run(edit_key=lambda k: k["expectedFindings"].append(
            dict(k["expectedFindings"][0], required=False)))),
        ("answer-key-shape", run(edit_key=lambda k: k["expectedFindings"][0].update(locationPaths=[3]))),
        # One case per clause of an entry's shape.
        ("answer-key-shape", run(edit_key=lambda k: k["expectedFindings"][0].update(minimumSeverity="critical"))),
        ("answer-key-shape", run(edit_key=lambda k: k["expectedFindings"][0].pop("minimumSeverity"))),
        ("answer-key-shape", run(edit_key=lambda k: k["expectedFindings"][0].update(locationPaths=[]))),
        ("answer-key-shape", run(edit_key=lambda k: k["expectedFindings"][0].pop("locationPaths"))),
        ("answer-key-shape", run(edit_key=lambda k: k["expectedFindings"][0].update(locationPaths="docs/guide.md"))),
        ("answer-key-shape", run(edit_key=lambda k: k["expectedFindings"][0].update(locationPaths=[""]))),
    ]
    for invariant, (docs, key) in planted:
        try:
            fired = {inv for _, inv, _ in answer_key_check(key, docs)}
        except Exception as e:
            fired = {f"{type(e).__name__} raised"}
        if invariant not in fired:
            print(f"selftest FAIL: planted {invariant} answer-key violation did not fire "
                  f"(fired: {sorted(fired) or 'nothing'})")
            failed += 1
        elif invariant in MATRIX_OF:
            COVERED.add(MATRIX_OF[invariant])

    # A key the packet names but that cannot be read: a missing file
    # (OSError) and a malformed one (ValueError). Each must be a problem, not
    # a traceback. REPO_ROOT points at a scratch tree for the two cases.
    global REPO_ROOT
    unreadable = [("missing", None), ("malformed", '{"roundId": "selftest-round", ')]
    saved = REPO_ROOT
    with tempfile.TemporaryDirectory() as tmp:
        REPO_ROOT = tmp
        try:
            for name, text in unreadable:
                if text is not None:
                    with open(os.path.join(tmp, "key.json"), "w", encoding="utf-8") as f:
                        f.write(text)
                docs = plant(lambda d: d["review-round"].__setitem__("fixture", {"answerKey": "key.json"}))
                try:
                    fired = {inv for _, inv, _ in round_findings(docs)[0]}
                except Exception as e:
                    fired = {f"{type(e).__name__} raised"}
                if "answer-key-readable" not in fired:
                    print(f"selftest FAIL: a {name} answer key gave {sorted(fired) or 'nothing'}, "
                          "not answer-key-readable")
                    failed += 1
        finally:
            REPO_ROOT = saved
    return failed, len(valid) + len(planted) + len(unreadable)


def main(argv):
    if argv == ["--selftest"]:
        return selftest()
    cases_dir, repo = None, None
    if len(argv) >= 3 and argv[0] == "--repo":
        repo, argv = argv[1], argv[2:]
        if not os.path.isdir(repo):
            print(f"::error::--repo {repo}: not a directory")
            return 2
    if len(argv) == 2 and argv[0] == "--cases" and repo is None:
        cases_dir = argv[1]
    elif not argv or any(a.startswith("-") for a in argv):
        print(__doc__.strip().split("\n\n")[1], file=sys.stderr)
        return 2
    try:
        schemas = load_schemas(os.path.join(REPO_ROOT, SCHEMA_DIR))
    except SchemaError as e:
        for line in str(e).splitlines():
            print(f"::error::{line}")
        return 2
    if cases_dir is not None:
        problems, n = run_cases(cases_dir, schemas)
        for p in problems:
            print(f"::error::{p}")
        print(f"  round-check: {n} case(s), {len(problems)} problem(s)")
        return 1 if problems else 0
    problems = []
    for round_dir in argv:
        problems.extend(check_round(round_dir, schemas, repo))
    for p in problems:
        print(f"::error::{p}")
    print(f"  round-check: {len(argv)} round(s), {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
