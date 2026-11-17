# Review rubric

What a reviewer checks on a pull request. Each item restates a practice the kit already holds and names where it comes from. The rubric adds no rule of its own.

A reviewer is the party named in item 4. Work through the items in order and write down which ones were checked, since a review that does not say what it covered cannot be told apart from one that covered nothing.

## 1. Every check has a planted positive it is shown to catch

A check that has never returned a hit has not been shown capable of returning one. For any check the change adds or alters, find the input built to trip it and confirm the check fires on it. A clean result on the real tree is weak evidence on its own.

Source: `scripts/gates.sh`, the `run_selftest` function and the comment above it; `CONTRIBUTING.md`, "Run the checks the way CI runs them"; `docs/glossary.md`, "Planted positive".

## 2. The unfixed copy fails the new test

A test added with a fix has to fail on the code as it was before the fix. Run the new test against the unfixed copy and confirm it fails, then against the fixed copy and confirm it passes. A test that passes both ways proves nothing about the fix.

Source: this is the pairing `scripts/gates.sh` uses in `plant_rejected`, which takes the result on a bad fixture and the result on a clean one and accepts neither alone, because a rejection means nothing if the clean fixture is rejected too. Applying the same pair to a fix, with the unfixed copy as the bad fixture, extends that practice.

## 3. A check states its coverage

Every new or changed check says what it read and what it did not. Look for the coverage statement in the check's header or its output, and compare it with what the check actually does.

Source: `CONTRIBUTING.md`, the paragraph beginning "What these gates do not cover"; the coverage comment at the head of `scripts/gates.sh`; `docs/glossary.md`, "Coverage line".

## 4. The verifier is a different party from the author

A completion claim counts as fact only after someone other than the claimant has checked it. The author running their own checks is a self-audit. Confirm that the verification the pull request describes was done by another party, human or a separate tool such as the second-party markdown lint in CI.

Source: `docs/interaction-manual.md`, section 4, "Nobody self-certifies"; `CONTRIBUTING.md`, "Verify completion claims before repeating them"; `.github/pull_request_template.md`, the Verification section. `docs/concepts.md` indexes the same principle.

## 5. The gates pass

`./scripts/gates.sh --selftest` passes, and the `gates` job in CI is green. Confirm from the job result, not from the author's statement.

Source: `CONTRIBUTING.md`, "Run the checks the way CI runs them"; `.github/workflows/gates.yml`; `.github/pull_request_template.md`, the Checks section.

## 6. A wrong statement is corrected in place

If the change corrects something the kit stated as fact, the correction is recorded where the wrong statement lived, as a correction and not a silent replacement. The prediction that was wrong stays visible beside the measurement that replaced it.

Source: `docs/security-posture.md`, rows 3.2b and 6.3, which correct earlier statements in place and say so; `CHANGELOG.md`, where an entry states a correction in its own words (search for "orrect").

## Recording a review

Put the items checked in the review text, by number. An item that did not apply is marked as not applicable with a reason. An item not checked is marked as not checked, and the reviewer says so rather than leaving it out.

## What this rubric does not cover

It does not judge prose quality, the soundness of a design, or whether a document's claims are true. Those remain a reader's judgment, as `docs/security-posture.md` says of adequacy.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
