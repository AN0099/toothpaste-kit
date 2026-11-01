#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2026 Aidan Naveja
#
# SPDX-License-Identifier: Apache-2.0

"""Write an SPDX 3.0.1 JSON-LD software bill of materials for the kit.

usage: scripts/sbom.py [--repo DIR]
       scripts/sbom.py --selftest

Standard library only. Reads the tree at DIR (default: the repository this
script is in) and prints one JSON-LD document to stdout:

- one software_File for every file git tracks that REUSE covers, with its
  copyright text and a hasDeclaredLicense relationship to its licence, both
  taken from the REUSE data already in the tree: the file's own
  SPDX-FileCopyrightText and SPDX-License-Identifier tags, a `<file>.license`
  sidecar, and the annotations in REUSE.toml;
- one software_Package for every GitHub Action a workflow in
  .github/workflows uses, by the ref it is pinned to;
- a software_Package for the kit itself, which contains every file and
  depends on every action at build time.

Files REUSE does not cover are left out: LICENSE*, COPYING*, everything under
LICENSES/, REUSE.toml, `*.license` sidecars (their tags apply to the file they
sit beside), symbolic links and submodules.

Exit 0 with the document on stdout. Exit 1, printing each problem to stderr
and no document, when a covered file has no licence or no copyright, when a
licence it names has no text under LICENSES/, or when an action is pinned by
anything other than a full commit SHA (unless KNOWN_TAG_PINS records it).
Before printing, it checks the document's shape against the SPDX 3.0.1 model
as far as the standard library allows (see validate(), which says what is not
checked) and exits 1 on any problem, printing no document.
Exit 2 on a usage error or a tree it cannot read.
"""

import fnmatch
import json
import os
import re
import subprocess
import sys
import tomllib

CONTEXT_URL = "https://spdx.org/rdf/3.0.1/spdx-context.jsonld"
CREATION_INFO_ID = "_:creationinfo"
PACKAGE_NAME = "toothpaste-kit"

# Actions pinned by tag that the tree already records as a known gap. Each
# entry names where it is recorded. A tag pin not listed here fails; the list
# is meant to shrink, and a new entry needs the same kind of record.
KNOWN_TAG_PINS = {
    "actions/checkout@v7": "docs/security-posture.md row 3.7 (Actions pinned by digest: Not done)",
}

# The tag patterns are not this file's own tags, so REUSE skips them.
# REUSE-IgnoreStart
TAG_RE = {
    "copyright": re.compile(r"SPDX-FileCopyrightText:\s*(.*)$"),
    "licence": re.compile(r"SPDX-License-Identifier:\s*(.*)$"),
}
# REUSE-IgnoreEnd
# Comment closers REUSE also strips from the end of a tag's value.
CLOSERS = ("-->", "*/", "#}", "%>", "--}}")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
USES_RE = re.compile(r"^\s*(?:-\s+)?uses:\s*['\"]?([^'\"\s#]+)['\"]?\s*(?:#.*)?$")
LICENCE_ID_RE = re.compile(r"[A-Za-z0-9.+-]+(?::[A-Za-z0-9.+-]+)?")


def fail(msg):
    print(f"sbom: {msg}", file=sys.stderr)
    sys.exit(2)


def git(repo, *args):
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True)
    if r.returncode != 0:
        fail(f"git {' '.join(args)}: {r.stderr.decode(errors='replace').strip()}")
    return r.stdout


def tracked_files(repo):
    """Regular files git tracks, as repository-relative paths."""
    out = []
    for entry in git(repo, "ls-files", "-s", "-z").split(b"\0"):
        if not entry:
            continue
        meta, _, path = entry.partition(b"\t")
        mode = meta.split()[0]
        if mode in (b"100644", b"100755"):
            out.append(path.decode("utf-8", "surrogateescape"))
    return sorted(out)


def reuse_covers(path):
    name = os.path.basename(path)
    return not (name.startswith(("LICENSE", "COPYING")) or path.startswith("LICENSES/")
                or path == "REUSE.toml" or path.endswith(".license"))


def clean(value):
    value = value.strip()
    for c in CLOSERS:
        if value.endswith(c):
            value = value[: -len(c)].rstrip()
    return value


def read_tags(text):
    """The copyright and licence tags in a text, skipping REUSE-Ignore blocks."""
    tags = {"copyright": [], "licence": []}
    ignoring = False
    for line in text.splitlines():
        if "REUSE-IgnoreStart" in line:
            ignoring = True
        if not ignoring:
            for kind, rx in TAG_RE.items():
                m = rx.search(line)
                if m and clean(m.group(1)):
                    tags[kind].append(clean(m.group(1)))
        if "REUSE-IgnoreEnd" in line:
            ignoring = False
    return tags


def file_tags(repo, path):
    """Tags from a sidecar if there is one, else from the file. A file that is
    not UTF-8 text carries none of its own."""
    for p in (path + ".license", path):
        full = os.path.join(repo, p)
        if p != path and not os.path.isfile(full):
            continue
        try:
            with open(full, encoding="utf-8") as fh:
                return read_tags(fh.read())
        except UnicodeDecodeError:
            return {"copyright": [], "licence": []}
        except OSError as e:
            fail(f"cannot read {p}: {e}")


def glob_match(pattern, path):
    """REUSE.toml path matching: `*` stays within a directory, `**` crosses."""
    rx = ""
    i = 0
    while i < len(pattern):
        if pattern.startswith("**/", i):
            rx += "(?:.*/)?"
            i += 3
        elif pattern.startswith("**", i):
            rx += ".*"
            i += 2
        elif pattern[i] == "*":
            rx += "[^/]*"
            i += 1
        elif pattern[i] == "?":
            rx += "[^/]"
            i += 1
        else:
            rx += re.escape(pattern[i])
            i += 1
    return re.fullmatch(rx, path) is not None


def load_annotations(repo):
    path = os.path.join(repo, "REUSE.toml")
    if not os.path.isfile(path):
        return []
    try:
        with open(path, "rb") as fh:
            data = tomllib.load(fh)
    except (OSError, tomllib.TOMLDecodeError) as e:
        fail(f"cannot read REUSE.toml: {e}")
    out = []
    for i, a in enumerate(data.get("annotations", [])):
        paths = a.get("path", [])
        paths = [paths] if isinstance(paths, str) else paths
        as_list = lambda v: [v] if isinstance(v, str) else list(v or [])
        precedence = a.get("precedence", "closest")
        if precedence not in ("closest", "aggregate", "override"):
            fail(f"REUSE.toml annotations[{i}]: unknown precedence {precedence!r}")
        out.append({"paths": paths, "precedence": precedence,
                    "copyright": as_list(a.get("SPDX-FileCopyrightText")),
                    "licence": as_list(a.get("SPDX-License-Identifier"))})
    return out


def reuse_info(repo, path, annotations):
    """Copyright and licence for one file, applying REUSE.toml precedence. The
    last annotation whose path matches is the one that applies."""
    own = file_tags(repo, path)
    match = None
    for a in annotations:
        if any(glob_match(p, path) for p in a["paths"]):
            match = a
    if match is None:
        return own
    if match["precedence"] == "override":
        return {"copyright": match["copyright"], "licence": match["licence"]}
    if match["precedence"] == "aggregate":
        return {k: own[k] + [v for v in match[k] if v not in own[k]] for k in own}
    # closest: the file's own tags win, kind by kind.
    return {k: own[k] or match[k] for k in own}


def licence_ids(expr):
    words = re.findall(r"[^\s()]+", expr)
    return [w for w in words if w.upper() not in ("AND", "OR", "WITH")]


def workflow_actions(repo):
    """(workflow path, line number, uses value) for every remote action."""
    wf = os.path.join(repo, ".github", "workflows")
    out = []
    if not os.path.isdir(wf):
        return out
    for name in sorted(os.listdir(wf)):
        if not name.endswith((".yml", ".yaml")):
            continue
        rel = f".github/workflows/{name}"
        with open(os.path.join(wf, name), encoding="utf-8") as fh:
            for n, line in enumerate(fh, 1):
                m = USES_RE.match(line)
                if m and not m.group(1).startswith("./"):
                    out.append((rel, n, m.group(1)))
    return out


def collect(repo):
    """Return (files, actions, problems)."""
    problems = []
    annotations = load_annotations(repo)
    licences = os.path.join(repo, "LICENSES")
    files = []
    for path in tracked_files(repo):
        if not reuse_covers(path):
            continue
        info = reuse_info(repo, path, annotations)
        if not info["licence"]:
            problems.append(f"{path}: no licence (no SPDX-License-Identifier, sidecar or REUSE.toml annotation)")
        if not info["copyright"]:
            problems.append(f"{path}: no copyright (no SPDX-FileCopyrightText, sidecar or REUSE.toml annotation)")
        for expr in info["licence"]:
            for lid in licence_ids(expr):
                if not os.path.isfile(os.path.join(licences, lid + ".txt")):
                    problems.append(f"{path}: licence {lid} has no LICENSES/{lid}.txt")
        files.append({"path": path, **info})
    actions = {}
    for wf, n, uses in workflow_actions(repo):
        if uses.startswith("docker://"):
            ok = "@sha256:" in uses
            name, ref = uses, uses.rpartition("@")[2] if ok else ""
        else:
            name, _, ref = uses.partition("@")
            ok = bool(SHA_RE.match(ref))
        if not ok and uses not in KNOWN_TAG_PINS:
            problems.append(f"{wf}:{n}: {uses} is not pinned by a full commit SHA")
        actions.setdefault(uses, {"name": name, "ref": ref, "pinned": ok, "where": []})["where"].append(f"{wf}:{n}")
    return files, [actions[k] for k in sorted(actions)], problems


def build(repo, files, actions):
    head = git(repo, "rev-parse", "HEAD").decode().strip()
    created, author = git(repo, "log", "-1", "--format=%cI%x00%an", "HEAD").decode().strip().split("\0")
    created = to_utc_z(created)
    urn = lambda kind, n: f"urn:toothpaste-kit:{head}:sbom-{kind}-{n}"
    agent_id, tool_id, kit_id = urn("agent", 1), urn("tool", 1), urn("package", 0)
    graph = [
        {"type": "CreationInfo", "@id": CREATION_INFO_ID, "specVersion": "3.0.1",
         "created": created, "createdBy": [agent_id], "createdUsing": [tool_id]},
        {"type": "Agent", "spdxId": agent_id, "creationInfo": CREATION_INFO_ID, "name": author},
        {"type": "Tool", "spdxId": tool_id, "creationInfo": CREATION_INFO_ID, "name": "scripts/sbom.py"},
        {"type": "software_Package", "spdxId": kit_id, "creationInfo": CREATION_INFO_ID,
         "name": PACKAGE_NAME, "software_packageVersion": head},
    ]
    exprs = {}
    file_ids, rels = [], []
    for i, f in enumerate(files, 1):
        fid = urn("file", i)
        file_ids.append(fid)
        graph.append({"type": "software_File", "spdxId": fid, "creationInfo": CREATION_INFO_ID,
                      "name": f["path"], "software_copyrightText": "\n".join(f["copyright"])})
        expr = " AND ".join(f"({e})" if len(f["licence"]) > 1 and " " in e else e for e in f["licence"])
        if expr not in exprs:
            exprs[expr] = urn("licence", len(exprs) + 1)
            graph.append({"type": "simplelicensing_LicenseExpression", "spdxId": exprs[expr],
                          "creationInfo": CREATION_INFO_ID, "simplelicensing_licenseExpression": expr})
        rels.append((fid, "hasDeclaredLicense", [exprs[expr]], None))
    action_ids = []
    for i, a in enumerate(actions, 1):
        aid = urn("action", i)
        action_ids.append(aid)
        node = {"type": "software_Package", "spdxId": aid, "creationInfo": CREATION_INFO_ID,
                "name": a["name"], "software_packageVersion": a["ref"],
                "comment": ("pinned by commit SHA" if a["pinned"] else
                            "pinned by tag, which is mutable: " + KNOWN_TAG_PINS.get(f"{a['name']}@{a['ref']}", ""))
                + "; used at " + ", ".join(a["where"])}
        if not a["name"].startswith("docker://"):
            node["software_downloadLocation"] = f"https://github.com/{a['name']}"
            node["software_packageUrl"] = f"pkg:githubactions/{a['name']}@{a['ref']}"
        graph.append(node)
    rels.append((kit_id, "contains", file_ids, None))
    if action_ids:
        rels.append((kit_id, "dependsOn", action_ids, "build"))
    for n, (frm, kind, to, scope) in enumerate(rels, 1):
        node = {"type": "LifecycleScopedRelationship" if scope else "Relationship", "spdxId": urn("relationship", n),
                "creationInfo": CREATION_INFO_ID, "from": frm, "relationshipType": kind, "to": to}
        if scope:
            node["scope"] = scope
        graph.append(node)
    graph.append({"type": "SpdxDocument", "spdxId": urn("document", 1), "creationInfo": CREATION_INFO_ID,
                  "name": f"{PACKAGE_NAME} SBOM", "rootElement": [kit_id],
                  "profileConformance": ["core", "software", "simpleLicensing"]})
    return {"@context": CONTEXT_URL, "@graph": graph}


# The shape check. What it covers, from the SPDX 3.0.1 model: the type of every
# node is one this script may emit; every property a node carries is one the
# model gives that type (closed, so a misspelt property fails) and each
# required property is there; spdxIds are unique IRIs; every reference
# (creationInfo, createdBy, createdUsing, from, to, rootElement) resolves to a
# node of the right type in the same graph; `created` is a UTC dateTime of the
# model's pattern; relationshipType, scope and profileConformance are in the
# model's vocabularies; every package URL is a well-formed purl.
# What it does NOT check: JSON-LD context expansion (the context is a URL and
# nothing is fetched), the model's SHACL shapes as such (rules here are
# restated from the model, not read from its shape file), whether a licence
# expression parses or its ids are on the SPDX licence list, and anything a
# type outside this script's output would need.
ELEMENT_PROPS = {"type", "spdxId", "creationInfo", "name", "comment", "description", "summary"}
SHAPES = {
    # type: (required beyond the element core, optional)
    "Agent": (set(), set()),
    "Tool": (set(), set()),
    "software_Package": ({"name"}, {"software_packageVersion", "software_downloadLocation",
                                    "software_packageUrl", "software_copyrightText"}),
    "software_File": ({"name"}, {"software_copyrightText"}),
    "simplelicensing_LicenseExpression": ({"simplelicensing_licenseExpression"}, set()),
    "Relationship": ({"from", "relationshipType", "to"}, set()),
    "LifecycleScopedRelationship": ({"from", "relationshipType", "to"}, {"scope"}),
    "SpdxDocument": ({"rootElement"}, {"profileConformance", "element", "dataLicense"}),
}
RELATIONSHIP_TYPES = {
    "affects", "amendedBy", "ancestorOf", "availableFrom", "configures", "contains", "coordinatedBy",
    "copiedTo", "delegatedTo", "dependsOn", "descendantOf", "describes", "doesNotAffect", "expandsTo",
    "exploitCreatedBy", "fixedBy", "fixedIn", "foundBy", "generates", "hasAddedFile", "hasAssessmentFor",
    "hasAssociatedVulnerability", "hasConcludedLicense", "hasDataFile", "hasDeclaredLicense",
    "hasDeletedFile", "hasDependencyManifest", "hasDistributionArtifact", "hasDocumentation",
    "hasDynamicLink", "hasEvidence", "hasExample", "hasHost", "hasInput", "hasMetadata",
    "hasOptionalComponent", "hasOptionalDependency", "hasOutput", "hasPrerequisite",
    "hasProvidedDependency", "hasRequirement", "hasSpecification", "hasStaticLink", "hasTest",
    "hasTestCase", "hasVariant", "invokedBy", "modifiedBy", "other", "packagedBy", "patchedBy",
    "publishedBy", "reportedBy", "republishedBy", "serializedInArtifact", "testedOn", "trainedOn",
    "underInvestigationFor", "usesTool",
}
SCOPES = {"build", "design", "development", "other", "runtime", "test"}
PROFILES = {"ai", "build", "core", "dataset", "expandedLicensing", "extension", "lite", "security",
            "simpleLicensing", "software"}
DATETIME_RE = re.compile(r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$")
PURL_RE = re.compile(r"^pkg:[a-z][a-z0-9.+-]*/[^@?#\s]+(@[^?#\s]+)?(\?[^#\s]*)?(#\S*)?$")
IRI_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:\S+$")
# Which type each reference must resolve to; "Element" is any element.
REFS = {"from": "Element", "to": "Element", "rootElement": "Element", "createdBy": "Agent",
        "createdUsing": "Tool"}
# The licence a hasDeclaredLicense relationship points at.
LICENCE_TARGETS = {"simplelicensing_LicenseExpression"}


def validate(doc):
    """Problems with a document's shape, as a list of strings; empty is clean."""
    out = []
    if not isinstance(doc, dict) or set(doc) != {"@context", "@graph"}:
        return ["the document must be an object with exactly @context and @graph"]
    if doc["@context"] != CONTEXT_URL:
        out.append(f"@context is {doc['@context']!r}, not {CONTEXT_URL}")
    graph = doc["@graph"]
    if not isinstance(graph, list):
        return out + ["@graph must be a list"]
    infos = {n.get("@id"): n for n in graph if isinstance(n, dict) and n.get("type") == "CreationInfo"}
    elements = {}
    for i, n in enumerate(graph):
        where = f"@graph[{i}]"
        if not isinstance(n, dict):
            out.append(f"{where}: not an object")
            continue
        t = n.get("type")
        if t == "CreationInfo":
            allowed, required = {"type", "@id", "specVersion", "created", "createdBy", "createdUsing", "comment"}, \
                {"@id", "specVersion", "created", "createdBy"}
        elif t in SHAPES:
            req, opt = SHAPES[t]
            required = {"spdxId", "creationInfo"} | req
            allowed = ELEMENT_PROPS | req | opt
            sid = n.get("spdxId")
            if not isinstance(sid, str) or not IRI_RE.match(sid):
                out.append(f"{where}: spdxId {sid!r} is not an IRI")
            elif sid in elements:
                out.append(f"{where}: spdxId {sid} is not unique")
            else:
                elements[sid] = n
        else:
            out.append(f"{where}: type {t!r} is not one this check knows")
            continue
        for p in sorted(set(n) - allowed):
            out.append(f"{where} ({t}): property {p} is not in the model for this type")
        for p in sorted(required - set(n)):
            out.append(f"{where} ({t}): required property {p} is missing")
        for p, v in n.items():
            if p not in ("to", "createdBy", "createdUsing", "rootElement", "element", "profileConformance") \
                    and not isinstance(v, str):
                out.append(f"{where} ({t}): {p} must be a string")
            elif p in ("to", "createdBy", "createdUsing", "rootElement", "element", "profileConformance") \
                    and not (isinstance(v, list) and v and all(isinstance(x, str) for x in v)):
                out.append(f"{where} ({t}): {p} must be a non-empty list of strings")
    for i, n in enumerate(graph):
        if not isinstance(n, dict) or (n.get("type") not in SHAPES and n.get("type") != "CreationInfo"):
            continue
        where, t = f"@graph[{i}] ({n['type']})", n["type"]
        if t == "CreationInfo":
            if n.get("specVersion") != "3.0.1":
                out.append(f"{where}: specVersion {n.get('specVersion')!r} is not 3.0.1")
            if not DATETIME_RE.match(str(n.get("created", ""))):
                out.append(f"{where}: created {n.get('created')!r} is not a UTC dateTime")
        elif n.get("creationInfo") not in infos:
            out.append(f"{where}: creationInfo {n.get('creationInfo')!r} names no CreationInfo")
        for p, want in REFS.items():
            v = n.get(p)
            for ref in (v if isinstance(v, list) else [v] if isinstance(v, str) else []):
                got = elements.get(ref)
                if got is None:
                    out.append(f"{where}: {p} {ref} names no element in the graph")
                elif want != "Element" and got.get("type") != want:
                    out.append(f"{where}: {p} {ref} is a {got.get('type')}, not a {want}")
        if t in ("Relationship", "LifecycleScopedRelationship"):
            rt = n.get("relationshipType")
            if rt not in RELATIONSHIP_TYPES:
                out.append(f"{where}: relationshipType {rt!r} is not in the vocabulary")
            if rt == "hasDeclaredLicense":
                for ref in n.get("to") or []:
                    if ref in elements and elements[ref].get("type") not in LICENCE_TARGETS:
                        out.append(f"{where}: hasDeclaredLicense points at a {elements[ref].get('type')}")
            if "scope" in n and n["scope"] not in SCOPES:
                out.append(f"{where}: scope {n['scope']!r} is not in the vocabulary")
        if t == "SpdxDocument":
            for p in n.get("profileConformance") or []:
                if p not in PROFILES:
                    out.append(f"{where}: profileConformance {p!r} is not in the vocabulary")
        if "software_packageUrl" in n and not PURL_RE.match(str(n["software_packageUrl"])):
            out.append(f"{where}: software_packageUrl {n['software_packageUrl']!r} is not a purl")
    if len(infos) != 1:
        out.append(f"the graph holds {len(infos)} CreationInfo nodes, not 1")
    if sum(1 for n in elements.values() if n.get("type") == "SpdxDocument") != 1:
        out.append("the graph holds no single SpdxDocument")
    return out


def to_utc_z(iso):
    from datetime import datetime, timezone
    return datetime.fromisoformat(iso).astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run(repo):
    files, actions, problems = collect(repo)
    if problems:
        for p in problems:
            print(f"sbom: {p}", file=sys.stderr)
        return 1
    doc = build(repo, files, actions)
    shape = validate(doc)
    if shape:
        for p in shape:
            print(f"sbom: output shape: {p}", file=sys.stderr)
        return 1
    json.dump(doc, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


def selftest():
    """Build small git trees in a temporary directory. Each planted case must
    give the problem it names; each clean case must give none and the tags it
    names. Prints a count and returns the exit code."""
    import shutil
    import tempfile

    # Built from parts, so neither REUSE nor this script reads them as this
    # file's own tags.
    cr, li = "SPDX-" + "FileCopyrightText: ", "SPDX-" + "License-Identifier: "
    head = lambda lic="Apache-2.0", who="2026 T": f"# {cr}{who}\n# {li}{lic}\n"
    sha = "1" * 40
    base = {
        "LICENSES/Apache-2.0.txt": "Apache text\n",
        "LICENSE": "Apache text\n",
        "REUSE.toml": 'version = 1\n[[annotations]]\npath = ["**/*.json"]\nprecedence = "aggregate"\n'
                      f'SPDX-FileCopyrightText = "2026 T"\nSPDX-License-Identifier = "Apache-2.0"\n',
        "a.py": head() + "print(1)\n",
        "docs/b.md": "# B\n\n<!--\n" + cr + "2026 T\n\n" + li + "Apache-2.0\n-->\n",
        "data/c.json": "{}\n",
        ".github/workflows/ci.yml": head() + f"jobs:\n  x:\n    steps:\n      - uses: actions/labeler@{sha} # v7\n"
                                    "      - uses: ./local-action\n",
    }
    wf = ".github/workflows/ci.yml"
    step = lambda uses: lambda t: t.__setitem__(wf, t[wf] + f"      - uses: {uses}\n")
    toml_add = lambda block: lambda t: t.__setitem__("REUSE.toml", t["REUSE.toml"] + "[[annotations]]\n" + block)

    planted = [
        ("a file with no licence", lambda t: t.__setitem__("e.py", f"# {cr}2026 T\n"), "e.py: no licence"),
        ("a file with no copyright", lambda t: t.__setitem__("e.py", f"# {li}Apache-2.0\n"), "e.py: no copyright"),
        ("a file with no tags at all", lambda t: t.__setitem__("e.txt", "plain\n"), "e.txt: no licence"),
        ("a licence with no text under LICENSES/", lambda t: t.__setitem__("e.py", head("MIT")), "licence MIT has no LICENSES/MIT.txt"),
        ("one licence of an expression with no text", lambda t: t.__setitem__("e.py", head("Apache-2.0 OR MIT")), "licence MIT has"),
        ("tags only inside an ignore block", lambda t: t.__setitem__("e.py", "# REUSE-IgnoreStart\n" + head() + "# REUSE-IgnoreEnd\n"),
         "e.py: no licence"),
        ("a binary file with no sidecar", lambda t: t.__setitem__("e.bin", b"\xff\xfe\x00"), "e.bin: no licence"),
        ("an override annotation with no licence", toml_add('path = "a.py"\nprecedence = "override"\nSPDX-FileCopyrightText = "2026 T"\n'),
         "a.py: no licence"),
        ("an action pinned by tag", step("actions/setup-python@v5"), "actions/setup-python@v5 is not pinned"),
        ("an action pinned by a short SHA", step("actions/setup-python@1111111"), "is not pinned"),
        ("an action pinned by branch", step("actions/setup-python@main"), "is not pinned"),
        ("an action with no ref", step("actions/setup-python"), "is not pinned"),
        ("the known tag pin's action at another tag", step("actions/checkout@v8"), "actions/checkout@v8 is not pinned"),
        ("a quoted tag pin", step('"actions/setup-python@v5"'), "is not pinned"),
        ("a docker action by tag", step("docker://alpine:3.20"), "docker://alpine:3.20 is not pinned"),
    ]
    clean = [
        ("the base tree", lambda t: None, "a.py", ["2026 T"], ["Apache-2.0"]),
        ("a Markdown file tagged at the end", lambda t: None, "docs/b.md", ["2026 T"], ["Apache-2.0"]),
        ("a JSON file covered by REUSE.toml", lambda t: None, "data/c.json", ["2026 T"], ["Apache-2.0"]),
        ("a binary file with a sidecar", lambda t: (t.__setitem__("e.bin", b"\xff\xfe\x00"),
                                                    t.__setitem__("e.bin.license", head())), "e.bin", ["2026 T"], ["Apache-2.0"]),
        ("closest: the file's own tags win", lambda t: t.__setitem__("data/d.json", "{}\n") or toml_add(
            'path = "a.py"\nSPDX-FileCopyrightText = "2026 Other"\nSPDX-License-Identifier = "Apache-2.0"\n')(t),
         "a.py", ["2026 T"], ["Apache-2.0"]),
        ("closest: the annotation fills a missing kind", lambda t: (t.__setitem__("e.py", f"# {li}Apache-2.0\n"), toml_add(
            'path = "e.py"\nSPDX-FileCopyrightText = "2026 Other"\n')(t)), "e.py", ["2026 Other"], ["Apache-2.0"]),
        ("aggregate: both", lambda t: toml_add('path = "a.py"\nprecedence = "aggregate"\nSPDX-FileCopyrightText = "2026 Other"\n')(t),
         "a.py", ["2026 T", "2026 Other"], ["Apache-2.0"]),
        ("override: the annotation only", lambda t: toml_add(
            'path = "a.py"\nprecedence = "override"\nSPDX-FileCopyrightText = "2026 Other"\nSPDX-License-Identifier = "Apache-2.0"\n')(t),
         "a.py", ["2026 Other"], ["Apache-2.0"]),
        ("the last matching annotation wins", lambda t: (toml_add(
            'path = "**/*.json"\nprecedence = "override"\nSPDX-FileCopyrightText = "2026 Last"\nSPDX-License-Identifier = "Apache-2.0"\n')(t)),
         "data/c.json", ["2026 Last"], ["Apache-2.0"]),
        ("`*` does not cross a directory", lambda t: (t.__setitem__("data/sub/e.json", "{}\n"), toml_add(
            'path = "data/*.json"\nprecedence = "override"\nSPDX-FileCopyrightText = "2026 Top"\nSPDX-License-Identifier = "Apache-2.0"\n')(t)),
         "data/sub/e.json", ["2026 T"], ["Apache-2.0"]),
        ("the known tag pin", step("actions/checkout@v7"), "a.py", ["2026 T"], ["Apache-2.0"]),
        ("a docker action by digest", step("docker://alpine@sha256:" + "a" * 64), "a.py", ["2026 T"], ["Apache-2.0"]),
    ]

    def make(edit):
        tree = dict(base)
        edit(tree)
        d = tempfile.mkdtemp(prefix="sbom-selftest-")
        for path, body in tree.items():
            full = os.path.join(d, path)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, "wb") as fh:
                fh.write(body if isinstance(body, bytes) else body.encode())
        env = dict(os.environ, GIT_AUTHOR_NAME="T", GIT_AUTHOR_EMAIL="t@example.com", GIT_COMMITTER_NAME="T",
                   GIT_COMMITTER_EMAIL="t@example.com", GIT_AUTHOR_DATE="2026-10-31T12:00:00Z",
                   GIT_COMMITTER_DATE="2026-10-31T12:00:00Z", GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
        for args in (["init", "-q"], ["add", "-A"], ["commit", "-q", "-m", "t"]):
            subprocess.run(["git", "-C", d, *args], env=env, check=True, capture_output=True)
        return d

    failed = 0
    total = len(planted) + len(clean)
    for name, edit, want in planted:
        d = make(edit)
        try:
            _, _, problems = collect(d)
        finally:
            shutil.rmtree(d)
        if not any(want in p for p in problems):
            print(f"sbom selftest FAIL: planted {name}: no problem containing {want!r} (got {problems})")
            failed += 1
    for name, edit, path, want_c, want_l in clean:
        d = make(edit)
        try:
            files, _, problems = collect(d)
        finally:
            shutil.rmtree(d)
        got = next((f for f in files if f["path"] == path), None)
        if problems or got is None or got["copyright"] != want_c or got["licence"] != want_l:
            print(f"sbom selftest FAIL: clean {name}: problems {problems}, {path} read as {got}")
            failed += 1
    import copy
    d = make(lambda t: None)
    try:
        good = build(d, *collect(d)[:2])
    finally:
        shutil.rmtree(d)
    first = lambda doc, typ: next(n for n in doc["@graph"] if n.get("type") == typ)
    shapes = [
        ("an unknown type", lambda g: g["@graph"].append({"type": "software_Snippet"}), "is not one this check knows"),
        ("a misspelt property", lambda g: first(g, "software_File").__setitem__("software_copyrightTxt", "x"),
         "property software_copyrightTxt is not in the model"),
        ("a missing required property", lambda g: first(g, "Relationship").pop("relationshipType"),
         "required property relationshipType is missing"),
        ("a duplicate spdxId", lambda g: first(g, "Tool").__setitem__("spdxId", first(g, "Agent")["spdxId"]), "is not unique"),
        ("a dangling reference", lambda g: first(g, "Relationship").__setitem__("to", ["urn:x:nothing"]),
         "names no element"),
        ("createdBy naming a Tool", lambda g: first(g, "CreationInfo").__setitem__("createdBy", [first(g, "Tool")["spdxId"]]),
         "not a Agent"),
        ("a local created time", lambda g: first(g, "CreationInfo").__setitem__("created", "2026-10-31T12:00:00+01:00"),
         "is not a UTC dateTime"),
        ("another specVersion", lambda g: first(g, "CreationInfo").__setitem__("specVersion", "3.0"), "is not 3.0.1"),
        ("an unknown relationshipType", lambda g: first(g, "Relationship").__setitem__("relationshipType", "licensedAs"),
         "not in the vocabulary"),
        ("an unknown scope", lambda g: first(g, "LifecycleScopedRelationship").__setitem__("scope", "ci"), "scope 'ci'"),
        ("an unknown profile", lambda g: first(g, "SpdxDocument").__setitem__("profileConformance", ["sbom"]),
         "profileConformance 'sbom'"),
        ("a malformed purl", lambda g: next(n for n in g["@graph"] if "software_packageUrl" in n).__setitem__(
            "software_packageUrl", "githubactions/actions/labeler"), "is not a purl"),
        ("a licence relationship to a file", lambda g: first(g, "Relationship").__setitem__("to", [first(g, "software_File")["spdxId"]]),
         "hasDeclaredLicense points at a software_File"),
        ("a missing creationInfo target", lambda g: first(g, "Tool").__setitem__("creationInfo", "_:other"),
         "names no CreationInfo"),
        ("a to that is not a list", lambda g: first(g, "Relationship").__setitem__("to", first(g, "Agent")["spdxId"]),
         "must be a non-empty list"),
        ("another context", lambda g: g.__setitem__("@context", "https://spdx.org/rdf/3.0.0/spdx-context.jsonld"),
         "@context is"),
    ]
    total += 1 + len(shapes)
    if validate(good):
        print(f"sbom selftest FAIL: the built document has shape problems: {validate(good)}")
        failed += 1
    for name, edit, want in shapes:
        doc = copy.deepcopy(good)
        edit(doc)
        got = validate(doc)
        if not any(want in p for p in got):
            print(f"sbom selftest FAIL: planted shape {name}: no problem containing {want!r} (got {got})")
            failed += 1
    print(f"sbom selftest: {total - failed} of {total} cases behaved")
    return 1 if failed else 0


def main(argv):
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    args = list(argv)
    if args == ["--selftest"]:
        return selftest()
    if args[:1] == ["--repo"] and len(args) == 2:
        repo = args[1]
    elif args:
        fail("usage: scripts/sbom.py [--repo DIR] | --selftest")
    return run(repo)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
