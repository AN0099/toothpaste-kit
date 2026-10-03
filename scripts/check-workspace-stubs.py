#!/usr/bin/env python3
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

Usage: scripts/check-workspace-stubs.py [DOC WORKSPACE]
Defaults to docs/standing-documents.md and examples/workspace.
Exits 1 on any finding, 2 if either input is missing.
"""

import os
import re
import sys

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


def main(argv):
    doc = argv[1] if len(argv) > 2 else "docs/standing-documents.md"
    root = argv[2] if len(argv) > 2 else "examples/workspace"
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
    sys.exit(main(sys.argv))
