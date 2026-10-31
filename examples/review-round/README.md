# Review round fixture

A practice [review round](../../docs/review-rounds.md): one proposed change to a small synthetic
project called `tally`, reviewed by one person, its findings reproduced by another, and decided by
the operator. The change carries a known defect, so a round run on it can be graded against an
answer key. Nothing here needs a network, an account, a secret or an AI model: only `git`, `sh`
and `python3`.

To run it, follow [Practising on the fixture](../../docs/review-rounds-quickstart.md#practising-on-the-fixture)
in the quickstart. To take one role, open that role's directory below.

## What is here

| Directory | Holds | For |
|---|---|---|
| [`history/`](history/) | Two numbered patches and `build.sh`, which builds them into a fresh repository with fixed authors and dates, so the base and target commits are the same on every machine | everyone |
| [`reviewer/`](reviewer/README.md) | The round packet, a report template and the reviewer's steps | the reviewer |
| [`verifier/`](verifier/README.md) | The answer key, the verifier's checklist, a decision template, and a completed round that passes the validator | the verifier and the operator |
| [`schema-cases/`](schema-cases/) | Valid and invalid documents, one schema each, with the expected result of each in `cases.json` | anyone changing the schemas or the validator |

**A reviewer reads only `history/` and `reviewer/` until their report is done.** The rest is
public, so nothing stops them, but reading the answer key first defeats the practice. The
separation is instructional, not access control.

## How it is checked

`python3 scripts/round-check.py --selftest` runs the validator against planted cases, and
`python3 scripts/round-check.py --cases examples/review-round/schema-cases` runs every case in
`cases.json`. Gate 18 in `scripts/gates.sh` runs both. A passing run says the records are well
formed and agree with each other; it says nothing about whether a review found the right things.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
