# Security posture

What this project has, what it does not, and how each claim was checked.

**Read the evidence column, not the status column.** A posture document whose
rows say "yes" with nothing behind them is the same unverifiable clean result
this project's own conventions reject. Every row below either names a file that
exists or says plainly that the thing is absent.

## How to re-check this document

```sh
./scripts/gates.sh --selftest
```

covers the mechanical repository rules. Everything else in the tables below is a
file's existence or a host setting, and the Evidence column names which.

**What nothing here checks:** whether a document's content is adequate, only
that it exists. A `SECURITY.md` that says nothing useful passes an existence
check. Judgment of adequacy is a reader's, and the point of naming the file is
that a reader can go and form one.

## Documentation and process

| Control | State | Evidence |
|---|---|---|
| Licence, OSI approved | Present | `LICENSE`, MIT, names the individual holder |
| Security policy | Present | `SECURITY.md`. Defines a vulnerability for a repository that ships no service, names private GitHub reporting as primary with an email fallback, and commits to an initial response within seven days |
| Code of conduct | Present | `CODE_OF_CONDUCT.md`, with a real reporting address. States plainly that there is one maintainer and no independent escalation body, and asks a reporter to name an acceptable third party if the report concerns the maintainer |
| Contribution guide | Present | `CONTRIBUTING.md`, which names the script that enforces its own mechanical rules |
| Governance, decision process, roles | Present | `GOVERNANCE.md`. One maintainer, bus factor one stated as a known risk, merges and tags and pushes not delegated |
| Citation metadata | Present, incomplete by design | `CITATION.cff`, with `version` and `date-released` commented out until a release exists. See `docs/releasing.md` step 3 |
| Issue templates | Present | Four files under `.github/ISSUE_TEMPLATE/` |
| Project state, current | Present | `docs/project-state.md`, which carries its own last-updated date so a reader can judge staleness |

## Build, release and provenance

| Control | State | Evidence |
|---|---|---|
| Versioning scheme | **Defined, not yet applied** | `docs/releasing.md`: repo-wide semver, annotated tags |
| Tagged release | **Absent** | `git tag` returns nothing as of 2026-09-18. This is the single blocker under both target schemes |
| Release notes | Mechanism exists, no release to note | `CHANGELOG.md` at repository level, plus one per skill |
| Signed releases | Configured 2026-09-18 | SSH commit and tag signing, with a signing key held separately from the authentication key. `commit.gpgsign` and `tag.gpgsign` are both true. Every commit in the 0.1.0 set verifies as a good signature locally, and the default branch ruleset carries `required_signatures`, so an unsigned commit is rejected at the remote rather than merely discouraged. Twelve commits were rejected on the first push attempt for exactly this reason |
| Reproducible build | Not applicable | The kit ships documents and two scripts. There is no build |
| Dependency declaration | Present, and small by nature | `.github/dependabot.yml`, github-actions only. The repository ships no package manifest, so the surface is this small |
| Actions pinned by digest | **Not done** | Both workflows use `actions/checkout@v4`, a tag rather than a digest. Tag pinning is mutable. Resolving it needs the current digest, which has to be read from the upstream repository rather than guessed |

## Automated checks

| Control | State | Evidence |
|---|---|---|
| Mechanical gates in CI | Present | `.github/workflows/gates.yml`, calling `scripts/gates.sh`. Seven gates: em dash ban, private task ID ban, JSON wellformedness, registry self-consistency, skill frontmatter, the reflow script's selftest, and markdown structure |
| Those gates proved able to fail | Yes | `scripts/gates.sh --selftest` plants a positive for each of the first five gates and confirms it fires before the real run. Gate six carries three fixture assertions, gate seven plants one positive per markdown rule. Last run 2026-09-18: five of five plants fired, gate seven's rules all fired, then seven of seven gates passed |
| Commit hygiene check | Present | `.github/workflows/commit-attribution.yml` rejects AI attribution trailers |
| Least-privilege workflow tokens | Present | Both workflows declare `permissions: contents: read`. `commit-attribution.yml` declared none until 2026-09-18, when CodeQL's `actions/missing-workflow-permissions` found it. The gap had been recorded in this table before the scanner found it, and the record alone did not close it |
| Static analysis | Present for Python and Actions, absent for shell | CodeQL default setup, languages `python` and `actions`, threat model remote and local. First analysis 2026-09-18. `scripts/gates.sh` and `scripts/link-skills.sh` are shell and therefore unanalysed, which is the remaining gap in this row |
| Checks actually binding | **Unverified, and this is the important row** | A workflow gates nothing until it is a required status check in the ruleset on the default branch. That is a host setting and is not visible from the tree. Unverified for all three jobs. The names to select are the **job** names, which are `gates`, `markdownlint` and `check`, not the workflow names |
| Second party check on the markdown gate | Present, and it has caught two defects | `markdownlint-cli2` runs the real tool against the same rule IDs as `scripts/mdlint.py`. On its first run, 2026-09-18, it found `MD034` at `CODE_OF_CONDUCT.md` line 52 where `mdlint.py` reported the file clean: our rule fired on a whitespace delimited bare URL and not on one inside parentheses, and its only planted positive used the delimited shape, so the selftest proved the rule could fire rather than that it covered its field. Both are fixed, and MD034 now carries two differently shaped plants. The second defect is in the row below |
| The second party check on `skills/` | **Never ran, from the day it was added until 2026-09-18** | The job's second step passed `--config .markdownlint-cli2-skills.jsonc`, a filename `markdownlint-cli2` 0.14.0 refuses, so the step failed before reading any markdown. Correcting the name was not sufficient, because `--config` carries rules and not globs: the file's own `skills/**/*.md` was discarded and the root options file's `!skills/**` then excluded every file the step existed to check. Both were invisible because the step above it was failing on the bare URL in the row above. Now a directory-level options file run with `skills/` as the working directory, verified at the desk on the pinned version: 28 files linted, a planted bare URL reported, and a second top level heading correctly not reported |
| Code scanning alerts triaged with a recorded reason | Present | First CodeQL analysis, 2026-09-18, returned three alerts on the default branch. `actions/missing-workflow-permissions` was fixed. Two `py/path-injection` alerts in `scripts/reflow-md.py` lines 229 and 253 were dismissed as false positives: the flagged flow is an argparse positional reaching `open()`, so the path is operator input rather than untrusted data, and no containment check exists that would not also break the intended use |
| Alerts outstanding on the release branch | **Three dismissed, seven mitigated and awaiting re-analysis** | Ten high security severity alerts in `scripts/mdlint.py`, from the first analysis to run against the release commits. The three `py/path-injection` alerts were dismissed as false positives on 2026-09-18, on the same reasoning as the `reflow-md.py` pair: `sys.argv` paths reach `os.walk` and `open`, so the path is operator input rather than untrusted data. The seven `py/polynomial-redos` were not dismissible on that reasoning, because this linter parses contributor markdown inside a required check and a pathological input can hang the gate. One regex was rewritten to a linear form with identical output; the other six are bounded by a 2000 character limit that reports `MDLINT001` rather than skipping silently. Whether CodeQL reads that limit as a barrier is decided by the next analysis, and the fallback is a dismissal citing a mitigation that exists |

## What the README's badges claim

A badge is an assertion with a click-through. It says a thing exists and lets a
reader verify it in one action. **A badge may point at evidence and never
substitute for it**, so every badge in `README.md` has a row in this document
that says more than the badge does.

| Badge | What it asserts | What it does not |
|---|---|---|
| `gates` workflow status | The workflow ran on the default branch and its result | Whether it is a required check, which is the row above |
| Licence | The licence is MIT | Anything about the copyright holder, which `LICENSE` names |

Alt text on a status badge names the indicator rather than its value, because
the image is served by a third party and changes while the text in the
repository does not. A badge reading "passing" in alt text would report a clean
result to a reader who cannot see the image, on every future failure.

**Absent on purpose:**

- **A coverage badge.** There is no test suite. The Static analysis row above
  says so plainly, which is the honest form of the same information.
- **An OpenSSF Scorecard badge.** Scorecard measures branch protection, pinned
  dependencies and signed releases among others, and three of those are open
  rows in this document. The badge is worth adding once they close, not before.
- **A maintenance or activity badge.** `GOVERNANCE.md` states one maintainer
  and a bus factor of one, which is the same fact without the implication that
  a project's health is a colour.

## Access control

| Control | State | Evidence |
|---|---|---|
| Branch protection on the default branch | **Not verifiable from the tree** | A GitHub setting. Needs a written record, and the row above depends on it |
| Required review before merge | Not applicable as written | One maintainer. `GOVERNANCE.md` states why a self-merge ban would stop work rather than add review |
| Signed commits required | **Not configured** | No such requirement in the tree, and it cannot be set from the tree |
| Two-factor authentication on the account | **Not verifiable from the tree** | Account setting |
| Least-privilege collaborator access | Not applicable | No collaborators |

## Where a dependency is allowed to come from

There are two zones, and the same package can be correct in one and wrong in
the other. Keywords below are BCP 14, per `docs/document-layers.md`.

**The local core** is everything a contributor executes at their own desk:
`scripts/`, `hooks/`, `skills/`.

- Code in the local core MUST be this project's own, already present on a plain
  system, or an implementation of a published standard.
- A local core dependency MUST NOT be fetched from a package registry at run
  time.
- W3C, IETF, ANSI and ISO are the standards bodies this project borrows from.
  Others MAY be used.

**The runner** is CI.

- A pinned package MAY be invoked in a workflow step.
- A third party action MUST NOT be used. An action runs inside the workflow with
  the workflow's token; a package invoked in a step does not.
- A version pinned in a workflow MUST be exact.

The test for the local core is not whether a package is popular. It is whether
the thing being trusted is a specification anyone can read. A runner is a
throwaway container that already fetches and executes third party code before
any of this repository's code runs, so a pinned package there does not widen a
surface that was already open.

| Zone | Example | Allowed | Why |
|---|---|---|---|
| Local core | `scripts/mdlint.py` | Yes, it is this project's code | Standard library only, nothing installed |
| Local core | `markdownlint-cli2` at the desk | No | Fetches from a registry at run time, and adds a package manifest to a repository that ships none |
| Local core | WCAG technique IDs, RFC keyword usage | Yes | Published standards, readable at the source |
| Runner | `markdownlint-cli2` pinned in a workflow step | Yes | Disposable container, no token, exact version |
| Runner | A third party marketplace action | No | Runs with the workflow's token |
| Runner | `actions/checkout` | Yes, with the pin recorded above | First party, and unavoidable |

**Scope.** These rules govern this repository. Material held at higher
sensitivity is governed elsewhere by a stricter rule that is not published
here, and this document does not describe it.

## The gap between this document and a certification

This document is organised by control area rather than by criterion ID. The
criterion lists for both targets have not been transcribed from their published
source, and inventing IDs from recall would produce a document that looks
authoritative and cites nothing.

**What is needed next, and it is one task:** take the current published criteria
for the two targets, the OpenSSF Project Security Baseline at the maturity level
being sought and the OpenSSF Best Practices Badge questionnaire, and add a
criterion ID column to the tables above. The evidence is already gathered; what
is missing is the mapping, and inventing criterion IDs from memory would produce
a document that looks authoritative and cites nothing real. That is the failure
mode this project names most often.

**What is already true regardless of the mapping:** the blockers are the same
three rows. No tagged release, actions pinned by tag rather than digest, and no
written record of whether the checks are binding on the default branch. The
first is `docs/releasing.md`, the second needs an upstream digest read, and the
third is a host setting plus a line in this file.
