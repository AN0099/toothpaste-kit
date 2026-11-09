#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2026 Aidan Naveja
#
# SPDX-License-Identifier: Apache-2.0

"""Validate the bill of materials against the published SPDX 3.0.1 model.

scripts/sbom.py checks its own output against rules restated from the model,
with the standard library. This runs what it cannot: the model's own SHACL
shapes, with pyshacl, and each licence id against the SPDX licence list.

The model, its JSON-LD context and the licence list are not in this tree. The
verification image downloads them, checked by digest, into /opt/schemas
(containers/verify/Containerfile), and this script checks each digest again
before it uses the file, so a file that is not the pinned one fails rather than
validating against something else.

The model is passed as both shapes and ontology, with inference off. Its shapes
reach a subclass through the ontology, so a File is held to what Element
requires. RDFS inference would add each parent type to the data, and the model's
abstract-class shapes then reject every node.

Coverage: the types, cardinalities, datatypes and vocabularies the shapes state,
on every node the JSON-LD context can name, and each licence id and exception in
each top-level node of type simplelicensing_LicenseExpression, a deprecated id
failing. A word starting LicenseRef- or DocumentRef- is taken as the document's
own and is not looked up.
It does NOT check:
- that a licence expression's structure parses, or that it names any id at all:
  an empty expression passes;
- the form of a LicenseRef- or DocumentRef- id, beyond its prefix;
- that a declared licence is the right one;
- that an xsd:dateTimeStamp value is a real date: rdflib has no converter for the
  type, so only the model's pattern applies, and 2026-13-45T99:99:99Z passes;
- a property or type the JSON-LD context does not define: the context drops it
  before the shapes see it, and sbom.py's closed checks are what fail it.

An id live on the wrong list, a licence used as an exception or the reverse, is
rejected with a message calling it deprecated.

A missing tool or file fails the script and names it, as in scripts/schemas.sh.

Usage: scripts/sbom-shapes.py              validate the tree's bill of materials
       scripts/sbom-shapes.py --selftest   first show each check rejects a plant,
                                           each for its reason

Run it in the verification container, which holds the tools and files:
  containers/verify/verify . ./scripts/sbom-shapes.py --selftest

SBOM_SHAPES_TOOL names the validator module; the selftest sets it to a name that
is not installed, to show the missing-tool case.
"""

import copy
import hashlib
import importlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

# The pinned files: file name in the directory, sha256. The same digests are in
# the Containerfile's ADD lines; a new version changes both.
PINS = {
    "spdx-3.0.1-model.ttl": "30ebb4af2d70a9809044ef46f44cc3dc5125226d70f818a50ed2e1d5f404c593",
    "spdx-3.0.1-context.jsonld": "c72b0928f094c83e5c127784edb1ebca2af74a104fcacc007c332b23cbc788bd",
    "spdx-licenses-3.29.0.json": "47d1cc681abe31166b342b6cc4aab13a6ba8ea5c48794697fe3bf8b1dbaf509a",
    "spdx-exceptions-3.29.0.json": "59ee7c150de521d635cbf9367b8cf543b8da6781ea3ac1c073d305524f84ada2",
}
SCHEMAS_DIR = "/opt/schemas"
CONTEXT_URL = "https://spdx.org/rdf/3.0.1/spdx-context.jsonld"
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Rejected(Exception):
    """The input fails a check, or a tool or file the check needs is missing."""


def read_pinned(directory, name):
    path = os.path.join(directory, name)
    try:
        with open(path, "rb") as f:
            data = f.read()
    except OSError:
        raise Rejected(f"{path} is missing; run in the verification container") from None
    got = hashlib.sha256(data).hexdigest()
    if got != PINS[name]:
        raise Rejected(f"{path} has sha256 {got}, pinned {PINS[name]}")
    return data


def load_tool():
    name = os.environ.get("SBOM_SHAPES_TOOL", "pyshacl")
    try:
        return importlib.import_module(name), importlib.import_module("rdflib")
    except ImportError:
        raise Rejected(f"{name} is not installed; run in the verification container") from None


def check_shapes(doc, directory):
    pyshacl, rdflib = load_tool()
    if doc.get("@context") != CONTEXT_URL:
        raise Rejected(f"@context is {doc.get('@context')!r}, not {CONTEXT_URL}")
    context = json.loads(read_pinned(directory, "spdx-3.0.1-context.jsonld"))
    model = read_pinned(directory, "spdx-3.0.1-model.ttl")
    # The context is a URL and the check has no network, so the pinned copy
    # stands in for it.
    local = dict(doc, **{"@context": context["@context"]})
    data = rdflib.Graph().parse(data=json.dumps(local), format="json-ld")
    shapes = rdflib.Graph().parse(data=model, format="turtle")
    conforms, _, text = pyshacl.validate(
        data, shacl_graph=shapes, ont_graph=shapes, inference="none", advanced=True
    )
    if not conforms:
        raise Rejected(text)


def check_licences(doc, directory):
    licences = json.loads(read_pinned(directory, "spdx-licenses-3.29.0.json"))["licenses"]
    exceptions = json.loads(read_pinned(directory, "spdx-exceptions-3.29.0.json"))["exceptions"]
    live = {x["licenseId"] for x in licences if not x["isDeprecatedLicenseId"]}
    live_exceptions = {x["licenseExceptionId"] for x in exceptions if not x["isDeprecatedLicenseId"]}
    known = {x["licenseId"] for x in licences} | {x["licenseExceptionId"] for x in exceptions}
    expressions = [
        n["simplelicensing_licenseExpression"]
        for n in doc["@graph"]
        if n.get("type") == "simplelicensing_LicenseExpression"
        and "simplelicensing_licenseExpression" in n
    ]
    # A document with no licence expression would otherwise pass this check unread.
    if not expressions:
        raise Rejected("no licence expression in the document")
    problems = []
    for expression in expressions:
        after_with = False
        for word in re.findall(r"[^\s()]+", expression):
            if word.upper() in ("AND", "OR"):
                continue
            if word.upper() == "WITH":
                after_with = True
                continue
            listed = live_exceptions if after_with else live
            word = word.rstrip("+")
            after_with = False
            if word.startswith(("LicenseRef-", "DocumentRef-")) or word in listed:
                continue
            state = "deprecated" if word in known else "not on the SPDX licence list"
            problems.append(f"{word} in {expression!r} is {state}")
    if problems:
        raise Rejected("\n".join(problems))


def build_sbom():
    run = subprocess.run(
        [sys.executable, os.path.join(REPO, "scripts", "sbom.py")],
        cwd=REPO, capture_output=True, text=True, check=False,
    )
    if run.returncode != 0:
        raise Rejected(f"scripts/sbom.py exited {run.returncode}:\n{run.stderr}")
    return json.loads(run.stdout)


def first(doc, kind):
    return next(n for n in doc["@graph"] if n.get("type") == kind)


def set_expression(doc, value):
    first(doc, "simplelicensing_LicenseExpression")["simplelicensing_licenseExpression"] = value


def drop_expressions(doc):
    doc["@graph"] = [
        n for n in doc["@graph"] if n.get("type") != "simplelicensing_LicenseExpression"
    ]


# Each plant: name, the change, the check it must fail, the rejection it is for.
# Any failure alone would also pass a plant rejected for some other reason.
PLANTS = [
    ("a File without creationInfo, which Element requires",
     lambda d: first(d, "software_File").pop("creationInfo"), check_shapes,
     "Result Path: ns1:creationInfo"),
    ("a Relationship without its to",
     lambda d: first(d, "Relationship").pop("to"), check_shapes, "Result Path: ns1:to"),
    ("a Relationship without its from",
     lambda d: first(d, "Relationship").pop("from"), check_shapes, "Result Path: ns1:from"),
    ("a relationshipType outside the vocabulary",
     lambda d: first(d, "Relationship").__setitem__("relationshipType", "notAType"), check_shapes,
     "RelationshipType/notAType"),
    ("a CreationInfo without specVersion",
     lambda d: first(d, "CreationInfo").pop("specVersion"), check_shapes, "Result Path: ns1:specVersion"),
    ("a created value that misses the model's pattern",
     lambda d: first(d, "CreationInfo").__setitem__("created", "yesterday"), check_shapes,
     "Value does not match pattern"),
    ("an instance of an abstract class",
     lambda d: first(d, "software_File").__setitem__("type", "Artifact"), check_shapes,
     "is an abstract class"),
    ("another @context",
     lambda d: d.__setitem__("@context", "https://spdx.org/rdf/3.0.0/spdx-context.jsonld"),
     check_shapes, "@context is"),
    ("a licence id not on the list",
     lambda d: set_expression(d, "Apache-2.0 AND Planted-1.0"), check_licences,
     "Planted-1.0 in 'Apache-2.0 AND Planted-1.0' is not on the SPDX licence list"),
    ("a deprecated licence id",
     lambda d: set_expression(d, "GPL-2.0"), check_licences, "GPL-2.0 in 'GPL-2.0' is deprecated"),
    ("an exception not on the list",
     lambda d: set_expression(d, "Apache-2.0 WITH Planted-exception"), check_licences,
     "Planted-exception in"),
    # Held to the id only: the message wrongly calls MIT deprecated (see the docstring).
    ("a licence id used as an exception",
     lambda d: set_expression(d, "Apache-2.0 WITH MIT"), check_licences, "MIT in"),
    ("no licence expression at all",
     drop_expressions, check_licences, "no licence expression in the document"),
]


def plant_rejected(name, check, doc, directory, want):
    try:
        check(doc, directory)
    except Rejected as e:
        if want in str(e):
            print(f"PLANT ok    {name} is rejected")
            return True
        print(f'PLANT FAIL  {name} was rejected without "{want}"')
        return False
    print(f"PLANT FAIL  {name} was accepted")
    return False


def selftest(doc, directory):
    print("\n== sbom-shapes selftest ==")
    ok = True
    # A clean pass first, or a rejected plant proves nothing.
    try:
        check_shapes(doc, directory)
        check_licences(doc, directory)
        # A compound expression and the document's own ids pass as well.
        compound = copy.deepcopy(doc)
        set_expression(compound, "(Apache-2.0 OR MIT+) AND GPL-2.0-only WITH Classpath-exception-2.0 AND LicenseRef-own")
        check_licences(compound, directory)
    except Rejected as e:
        print(f"PLANT FAIL  a clean document was rejected, so a rejected plant proves nothing:\n{e}")
        return False
    for name, change, check, want in PLANTS:
        planted = copy.deepcopy(doc)
        change(planted)
        ok = plant_rejected(name, check, planted, directory, want) and ok
    # A file that is not the pinned one, though the document still matches it.
    # Only that file differs, so the plant reaches the check it is for.
    for name, check, altered in (
        ("a model with the wrong digest", check_shapes, "spdx-3.0.1-model.ttl"),
        ("a context with the wrong digest", check_shapes, "spdx-3.0.1-context.jsonld"),
        ("a licence list with the wrong digest", check_licences, "spdx-licenses-3.29.0.json"),
        ("an exception list with the wrong digest", check_licences, "spdx-exceptions-3.29.0.json"),
    ):
        with tempfile.TemporaryDirectory() as scratch:
            for pinned in PINS:
                shutil.copy(os.path.join(directory, pinned), scratch)
            os.chmod(os.path.join(scratch, altered), 0o644)
            with open(os.path.join(scratch, altered), "a", encoding="utf-8") as f:
                f.write("\n")
            ok = plant_rejected(name, check, doc, scratch, f"{altered} has sha256") and ok
    with tempfile.TemporaryDirectory() as empty:
        ok = plant_rejected("a missing licence list", check_licences, doc, empty, "is missing") and ok
    # A missing tool fails the whole script and names it.
    missing = "sbom-shapes-selftest-not-installed"
    run = subprocess.run(
        [sys.executable, os.path.abspath(__file__)],
        env=dict(os.environ, SBOM_SHAPES_TOOL=missing),
        capture_output=True, text=True, check=False,
    )
    if run.returncode == 1 and f"{missing} is not installed" in run.stdout + run.stderr:
        print("PLANT ok    a missing validator fails, exit 1, naming it")
    else:
        print(f"PLANT FAIL  a missing validator gave exit {run.returncode}, not 1 naming the tool")
        ok = False
    print("PASS  sbom-shapes selftest" if ok else "FAIL  sbom-shapes selftest")
    return ok


def main(argv):
    if argv not in ([], ["--selftest"]):
        print(f"sbom-shapes: unknown arguments {' '.join(argv)}", file=sys.stderr)
        return 2
    try:
        doc = build_sbom()
        if argv and not selftest(doc, SCHEMAS_DIR):
            print("sbom-shapes: FAILED")
            return 1
        check_shapes(doc, SCHEMAS_DIR)
        print("PASS  bill of materials against the SPDX 3.0.1 shapes")
        check_licences(doc, SCHEMAS_DIR)
        print("PASS  licence ids against the SPDX licence list 3.29.0")
    except Rejected as e:
        print(f"{e}\nsbom-shapes: FAILED")
        return 1
    print("sbom-shapes: all passed")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
