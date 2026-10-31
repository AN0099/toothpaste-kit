# Quality

What quality this project measures, where each measure lives, and how to read it. Measures only. Each entry names a file or command a reader can run.

## The measures

| Measure | Where it lives | What it tells you |
|---|---|---|
| Mechanical gates | `scripts/gates.sh` | Whether the repository's stated mechanical rules hold now |
| Gate selftests | `scripts/gates.sh --selftest` and each tool's own `--selftest` | Whether each gate can fail |
| Coverage statements | The header of `scripts/gates.sh`, `CONTRIBUTING.md`, each tool's header | What each check read and what it did not |
| Second-party markdown lint | `markdownlint` job in `.github/workflows/gates.yml` | Whether a tool other than `scripts/mdlint.py` agrees |
| Corrections in place | `docs/security-posture.md` and `CHANGELOG.md` | What the project stated wrongly and how it was fixed |
| PR acceptance | `docs/metrics.md` | Merged against closed unmerged, and recorded reviews |
| Review rubric | `docs/review-rubric.md` | What a reviewer checked on a change |
| CI matrix | `.github/workflows/ci.yml` | Whether the selftest passes on Linux and macOS |

## How to read each one

**Mechanical gates.** Run `./scripts/gates.sh`. The last lines give the count of gates passed out of the total and either `gates: all passed` or `gates: FAILED`. Any failure names the file and rule.

**Gate selftests.** Run `./scripts/gates.sh --selftest`. Before the real run it prints a `PLANT ok` line for each planted positive, one or more for every gate not named below, and a `PLANT FAIL` line for any that did not fire. If any plant fails, the script says not to trust a clean run, and that is the instruction to follow. Gate 7 prints its own line, `mdlint: every rule fired on its plant.`, after `scripts/mdlint.py --selftest` plants one positive per rule. Gates 6, 9, 10 and 11 have no plant in this selftest; they run their tools' own selftests in the real run. `tests/run` is the same command.

**Coverage statements.** A clean gate result is read with the coverage statement beside it. The gates do not cover en dashes, prose quality, internal link validity, whether a skill's closing section is last, or whether any document's claims are true. Anything in that list is not measured, whatever the gates report.

**Second-party markdown lint.** The `markdownlint` job runs the real tool against the rules `scripts/mdlint.py` reimplements. If the two disagree, `CONTRIBUTING.md` says the defect is in `scripts/mdlint.py`. Its status as a required check is stated in `docs/security-posture.md`, rows 4.6 to 4.8.

**Corrections in place.** Read `docs/security-posture.md` for rows that say a prior claim was wrong, such as 3.2b and 6.3, and the `CHANGELOG.md` entries that state a correction (search for "orrect"; the wording varies). A correction recorded in place is a measure that the project checks its own statements. The absence of corrections is not evidence of accuracy.

**PR acceptance.** Read `docs/metrics.md`: the figures carry their date and the command that produced them. Read the acceptance rate with the review count.

**Review rubric.** `docs/review-rubric.md` is a checklist and produces no figure. A review is read for which of its six items were recorded as checked.

**CI matrix.** The `test` job in `ci.yml` reports one result per operating system. A pass on both means the selftest ran clean on each. A failure on macOS alone is a portability finding about the scripts.

## What these measures leave out

They do not measure documentation adequacy, design quality, or whether the skills behave as described when used. Those are judged by a reader.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
