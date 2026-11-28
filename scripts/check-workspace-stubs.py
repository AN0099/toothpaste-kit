#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2026 Aidan Naveja
#
# SPDX-License-Identifier: Apache-2.0

"""Check the example workspace against the document that describes it.

`examples/workspace/` holds stubs of the standing files, and
`docs/standing-documents.md` describes the same set in its "The document set"
table. Two copies of one list drift, so this checks them against each other:

1. Every stub file is named in the table's first column. A stub the document
   does not describe is a file a new user is handed with no account of it.
2. Every file the table names has a stub, except the names in EXEMPT, each
   with its reason. A described file with no stub is one the quickstart never
   creates and a skill later goes looking for.
3. Every stub under `.agents/` is listed in the stub `index.md`, since that
   list is what `session-close` reads to know which files to keep current.

Coverage, stated because a check that does not state its coverage is not a
check: file names and the index listing only. It does not read what a stub
says, whether its comments are accurate, or whether `CLAUDE.md` names the
right paths. A table row whose first cell has no backticked name (such as
"Procedures") is skipped, and a name containing `*` is a pattern, not a file.

Usage: scripts/check-workspace-stubs.py [WORKSPACE [TABLE]]
WORKSPACE defaults to examples/workspace and TABLE, the document holding "The
document set" table, to docs/standing-documents.md, both relative to the
working directory, so a run with no arguments checks this repository from its
root. --selftest checks one passing and one failing workspace in a temporary
tree, passing both paths as arguments.
Exits 1 on any finding or a failed selftest, 2 if either input is missing.
"""

import os
import re
import subprocess
import sys
import tempfile

# Described in the table, deliberately not stubbed.
EXEMPT = {
    # One per actively developed project; a new workspace has no project yet.
    "project-state.md": "one per project, and a new workspace has none",
}
IGNORED_FILES = {".gitkeep"}


def table_names(doc_path):
    names = set()
    in_table = False
    for line in open(doc_path, encoding="utf-8"):
        if line.startswith("## "):
            in_table = line.strip() == "## The document set"
            continue
        if not in_table or not line.startswith("|"):
            continue
        first = line.split("|")[1]
        m = re.search(r"`([^`]+)`", first)
        if m and "*" not in m.group(1):
            names.add(m.group(1))
    return names


def stub_files(root):
    found = []
    for dirpath, _dirs, files in os.walk(root):
        for f in files:
            if f in IGNORED_FILES:
                continue
            found.append(os.path.relpath(os.path.join(dirpath, f), root))
    return sorted(found)


DOC = "docs/standing-documents.md"
ROOT = "examples/workspace"


def selftest():
    with tempfile.TemporaryDirectory() as tmp:
        doc = os.path.join(tmp, "table.md")
        with open(doc, "w", encoding="utf-8") as f:
            f.write("## The document set\n\n| Document | Role |\n|---|---|\n"
                    "| `index.md` | Manifest |\n| `notes.md` | Notes |\n")
        for name in ("ok", "bad"):
            os.makedirs(os.path.join(tmp, name, ".agents"))
            with open(os.path.join(tmp, name, "index.md"), "w", encoding="utf-8") as f:
                f.write("- `.agents/notes.md`\n")
            open(os.path.join(tmp, name, ".agents", "notes.md"), "w").close()
        open(os.path.join(tmp, "bad", ".agents", "undescribed.md"), "w").close()
        # Run from the temporary tree, where neither default path exists, so a
        # run that ignored its arguments would exit 2 rather than pass.
        fails = 0
        for name, want in (("ok", 0), ("bad", 1)):
            got = subprocess.run(
                [sys.executable, os.path.abspath(__file__), os.path.join(tmp, name), doc],
                cwd=tmp, capture_output=True).returncode
            ok = got == want
            print(f"{'ok  ' if ok else 'FAIL'} {name} workspace exits {got}, wants {want}")
            fails += not ok
    print("check-workspace-stubs: selftest " + ("passed" if not fails else f"FAILED ({fails})"))
    return 1 if fails else 0


def main(argv):
    if argv[:1] == ["--selftest"]:
        return selftest()
    root = argv[0] if len(argv) > 0 else ROOT
    doc = argv[1] if len(argv) > 1 else DOC
    if not os.path.isfile(doc) or not os.path.isdir(root):
        print(f"::error::missing input: {doc} or {root}")
        return 2
    names = table_names(doc)
    if not names:
        print(f"::error file={doc}::no names read from 'The document set' table")
        return 2
    stubs = stub_files(root)
    bad = 0
    for s in stubs:
        if os.path.basename(s) not in names:
            print(f"::error file={root}/{s}::stub not described in {doc}")
            bad += 1
    stubbed = {os.path.basename(s) for s in stubs}
    for n in sorted(names - stubbed - set(EXEMPT)):
        print(f"::error file={doc}::{n} is described but has no stub in {root}")
        bad += 1
    index = os.path.join(root, "index.md")
    listed = open(index, encoding="utf-8").read() if os.path.isfile(index) else ""
    for s in stubs:
        if s.startswith(".agents" + os.sep) and f"`{s}`" not in listed:
            print(f"::error file={index}::{s} is not listed in the stub index")
            bad += 1
    print(f"  checked {len(stubs)} stubs against {len(names)} described files"
          f" ({len(EXEMPT)} exempt)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
