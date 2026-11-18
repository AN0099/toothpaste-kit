#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2026 Aidan Naveja
#
# SPDX-License-Identifier: Apache-2.0

"""Check that every action a workflow uses is pinned.

usage: scripts/sbom.py
       scripts/sbom.py --selftest

Standard library only. Reads every .yml and .yaml file in .github/workflows of
the repository this script is in. A remote action must be pinned by a full
commit SHA, and a docker:// action by a sha256 digest, unless KNOWN_TAG_PINS
records it; local actions (./) are skipped. Exit 0 when every reference is
pinned. Exit 1, printing each one that is not to stderr, when any is not.
Exit 2 on a usage error.
"""

import os
import re
import sys
import tempfile

# Actions pinned by tag that the tree already records as a known gap. Each
# entry names where it is recorded. A tag pin not listed here fails; the list
# is meant to shrink, and a new entry needs the same kind of record.
KNOWN_TAG_PINS = {
}

SHA_RE = re.compile(r"^[0-9a-f]{40}$")
USES_RE = re.compile(r"^\s*(?:-\s+)?uses:\s*['\"]?([^'\"\s#]+)['\"]?\s*(?:#.*)?$")


def problems(repo):
    """One line for each action reference not pinned; empty is clean."""
    wf = os.path.join(repo, ".github", "workflows")
    out = []
    names = sorted(os.listdir(wf)) if os.path.isdir(wf) else []
    for name in (n for n in names if n.endswith((".yml", ".yaml"))):
        with open(os.path.join(wf, name), encoding="utf-8") as fh:
            for n, line in enumerate(fh, 1):
                m = USES_RE.match(line)
                if not m or m.group(1).startswith("./"):
                    continue
                uses = m.group(1)
                if uses.startswith("docker://"):
                    ok = "@sha256:" in uses
                else:
                    ok = bool(SHA_RE.match(uses.partition("@")[2]))
                if not ok and uses not in KNOWN_TAG_PINS:
                    by = "digest" if uses.startswith("docker://") else "full commit SHA"
                    out.append(f".github/workflows/{name}:{n}: {uses} is not pinned by {by}")
    return out


def selftest():
    """A tag pin must give a problem and a commit SHA or digest pin none."""
    cases = [("an action pinned by tag", "actions/setup-python@v5", True),
             ("an action pinned by commit SHA", "actions/checkout@" + "1" * 40, False),
             ("a docker action by tag", "docker://alpine:3.20", True),
             ("a docker action by digest", "docker://alpine@sha256:" + "a" * 64, False)]
    if KNOWN_TAG_PINS:
        cases.append(("a tag pin KNOWN_TAG_PINS records", sorted(KNOWN_TAG_PINS)[0], False))
    failed = 0
    for name, uses, want in cases:
        with tempfile.TemporaryDirectory(prefix="sbom-selftest-") as d:
            os.makedirs(os.path.join(d, ".github", "workflows"))
            with open(os.path.join(d, ".github", "workflows", "ci.yml"), "w", encoding="utf-8") as fh:
                fh.write(f"jobs:\n  x:\n    steps:\n      - uses: {uses}\n")
            got = problems(d)
        if bool(got) != want:
            print(f"sbom selftest FAIL: {name}: problems {got}")
            failed += 1
    print(f"sbom selftest: {len(cases) - failed} of {len(cases)} cases behaved")
    return 1 if failed else 0


def main(argv):
    if argv == ["--selftest"]:
        return selftest()
    if argv:
        print("usage: scripts/sbom.py [--selftest]", file=sys.stderr)
        return 2
    found = problems(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    for p in found:
        print(f"sbom: {p}", file=sys.stderr)
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
