# Examples

Each directory here is one worked example. Each is complete, runs from the repository root with no
network, account or secret, and is checked by a gate in `scripts/gates.sh`, so it cannot drift
from the documents that describe it.

| Example | What it is | Start with | Checked by |
|---|---|---|---|
| [`workspace/`](workspace/) | The workspace the quickstart copies: a `CLAUDE.md` naming where the other files are, the manifest `index.md`, and stubs of the standing files under `.agents/` | [Quickstart, step 3](../docs/quickstart.md#3-copy-the-example-workspace) | `scripts/check-workspace-stubs.py` and `reorient --selftest` |
| [`review-round/`](review-round/) | A practice review round: a small synthetic project with a proposed change that carries a known defect, the material for each role, an answer key, and schema test cases | [`review-round/README.md`](review-round/README.md) | `scripts/round-check.py --selftest` and `--cases` (gate 18) |

## Why `workspace/` has no README of its own

Every file in `workspace/` is copied into your workspace by the quickstart, and the stub check
fails on a file that `docs/standing-documents.md` does not describe. A README there would be
copied into every new workspace and would fail that gate, so this page describes it instead.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
