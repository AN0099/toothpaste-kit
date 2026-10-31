# Review round fixture: verifier material

This directory is for the verifier (role `lead`) and the operator, not the reviewer. It holds the
answer key for the round `tally-lines-1`, a checklist for verifying a reviewer's report, and a
completed expected round.

The separation from the reviewer's material is instructional, not access control. Everything here
is public in the repository, so a reviewer can read it. The exercise only works if they do not
read it first. When the result must be trusted as an assessment, keep the answer key private, hand
it out separately, or have a facilitator hold it.

## What is here

- `answer-key.json`: the expected findings, each with equivalence criteria and expected evidence;
  whether a report with no findings is acceptable (it is not); and the expected decision.
- `expected/`: a completed round that passes `scripts/round-check.py`: the packet as the operator
  holds it, with `fixture.answerKey` set, the reviewer's report, and the operator's decision.
- `templates/operator-decision.template.json`: the decision record the verifier and operator fill in.

## The answer key's fields

`scripts/round-check.py` reads the answer key when the packet's `fixture.answerKey` names it. The
field sets are closed: an unknown field, such as a misspelled one, fails with `answer-key-shape`
rather than being read as absent. These fields are checked:

- `roundId`: a non-empty string, equal to the packet's `metadata.roundId`.
- `noFindingsAcceptable`: `true` or `false`. When it is `false`, at least one expected finding must
  be `required`, and a report with no findings fails.
- `expectedFindings`: a list. Each entry needs `id` (a non-empty string, unique in the key),
  `required` (`true` or `false`), `minimumSeverity` (`nit`, `minor` or `major`) and `locationPaths`
  (a non-empty list of paths). A required entry is met by a report finding at one of its paths with
  at least its severity.
- `expectedDecision`: `accept`, `reject` or `request-revision`. The operator's decision must match it
  when the decision's alignment is `matched`.

`theme`, `expectedVerification`, and each finding's `findingClass`, `equivalence` and
`expectedEvidence` are allowed but not checked. They are for the person verifying the review: a
script can check where a finding is, not what it means.

## The planted defect

The proposed change adds a `--lines` option to `tally.py` and rewrites the README's "Before a push"
section. The baseline README said `./check.sh --selftest` runs its built-in cases and checks those
only, which is true. The new text says the check "validates every contributor change: when it exits
0, your change to `tally.py` is correct and ready to merge".

That is false. `check.sh` runs four fixed word-count cases and nothing else; it has no case for
`--lines`. A change that breaks `--lines` completely still passes. This is the class "operator-facing
documentation/behavior mismatch": the documentation claims more than the gate does, and passing the
gate cannot support the claim. The expected decision is `request-revision`.

A second, lesser finding is acceptable: `--lines` has no case in `check.sh`. It does not replace the
first. A report that names only the missing case has missed that the README now tells contributors
to trust a check that cannot catch their mistakes.

## Checklist

Work from a fresh build, not from the reviewer's directory:

```sh
examples/review-round/history/build.sh /tmp/tally-verify
```

1. **Revision.** The report's `reviewedRevision.revision` equals the packet's
   `provenance.targetRevision`. If it does not, record `mismatched` (or `unresolved` when the
   report gives no revision you can resolve). The decision can then only be `abstain` or `rerun`.
2. **Required checks.** Each check in the packet has an entry in the report's `checks` with an
   explicit status. Rerun it yourself.
3. **Findings against the key.** Match each report finding to an `expectedFindings` entry by its
   `equivalence` text, not by its ID. The reviewer chose their own IDs.
4. **Required finding present.** If no finding matches `readme-check-overclaim`, the review missed
   the planted defect. A report with no findings fails this round.
5. **Reproduce.** For each finding you will rely on, repeat the evidence yourself in the fresh build.
   For the required finding, make `tally.py` wrong in a way the check does not cover and show that
   `./check.sh --selftest` still passes. Record `reproduced` or `not-reproduced` with your own
   evidence, under your role, never the reviewer's.
6. **Decision.** The operator cites only reproduced findings with evidence. With the required finding
   reproduced, the expected outcome is `request-revision`. Accepting despite it needs an entry in
   `decision.exceptions` that names the finding and the reason.
7. **Validate.** Run `python3 scripts/round-check.py` on the round directory holding all three
   records. Its `review-round.json` must be the packet as the operator holds it, the one with
   `fixture.answerKey` (as in `expected/review-round.json`), not the reviewer's copy. With the
   reviewer's packet the answer-key checks do not run, so a report with no findings would pass.
   Exit 0 means the records are well formed and agree with each other, and, with the answer key,
   that the report finds what the key requires. It does not mean the review or the decision is
   right; steps 3 to 6 are for that.

## Limits

- The answer key's equivalence criteria are for a person to apply. A script can check that a report
  has findings and where they are, not that a finding means what the key means.
- The commits in `expected/` (`provenance.commit` and `references.*.commit`) are synthetic values. A
  file cannot name the commit that adds it, and this example is not recorded in a real round.
- The fixture is synthetic. Its evidence was captured from the fixture, not from a real project.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
