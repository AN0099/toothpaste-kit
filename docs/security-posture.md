# Security posture

What this project has, what it does not, and how each claim was checked.

**Read the evidence column, not the status column.** A posture document whose
rows say "yes" with nothing behind them is the same unverifiable clean result
this project's own conventions reject. Every row below either names a file that
exists or says plainly that the thing is absent.

## 1. How to re-check this document

```sh
./scripts/gates.sh --selftest
```

covers the mechanical repository rules. Everything else in the tables below is a
file's existence or a host setting, and the Evidence column names which.

**What nothing here checks:** whether a document's content is adequate, only
that it exists. A `SECURITY.md` that says nothing useful passes an existence
check. Judgment of adequacy is a reader's, and the point of naming the file is
that a reader can go and form one.

## 2. Documentation and process

| Control | State | Evidence |
|---|---|---|
| 2.1 Licence, OSI approved | Present | `LICENSE`, MIT, names the individual holder |
| 2.2 Security policy | Present | `SECURITY.md`. Defines a vulnerability for a repository that ships no service, names private GitHub reporting as primary with an email fallback, and commits to an initial response within seven days |
| 2.3 Code of conduct | Present | `CODE_OF_CONDUCT.md`, with a real reporting address. States plainly that there is one maintainer and no independent escalation body, and asks a reporter to name an acceptable third party if the report concerns the maintainer |
| 2.4 Contribution guide | Present | `CONTRIBUTING.md`, which names the script that enforces its own mechanical rules |
| 2.5 Governance, decision process, roles | Present | `GOVERNANCE.md`. One maintainer, bus factor one stated as a known risk, merges and tags and pushes not delegated |
| 2.6 Citation metadata | Present, incomplete by design | `CITATION.cff`, with `version` and `date-released` commented out until a release exists. See `docs/releasing.md` step 3 |
| 2.7 Issue templates | Present | Four files under `.github/ISSUE_TEMPLATE/` |
| 2.8 Project state, current | Present | `docs/project-state.md`, which carries its own last-updated date so a reader can judge staleness |

## 3. Build, release and provenance

| Control | State | Evidence |
|---|---|---|
| 3.1 Versioning scheme | Defined and applied | `docs/releasing.md`: repo-wide semver, annotated tags. First application is `v0.1.0`, 2026-09-19 |
| 3.2 Tagged release | Present | `v0.1.0`, tag object `af16f7f`, annotated and signed, pointing at merge commit `91959631`. It points at the release merge rather than at the tip of `main`, because the `actions/checkout` bump in row 3.7 landed afterwards and row 3.7 would otherwise be false inside its own release |
| 3.2a The tagged tree differs from `main`, deliberately | Known and bounded | Three files diverge and each divergence is a correction made after the tag: `CHANGELOG.md` and `CITATION.cff` carry `2026-09-18` in the tag and `2026-09-19` on `main`, the real release date, having been written the day before a release that slipped; and the tag's `CHANGELOG.md` `Known` section describes a `README.md` sentence ending mid-clause that commit `56609d8` had already fixed, verified by searching the tagged tree and finding zero hits with a control proving the search works. The tag was not moved, because rewriting a published tag to correct a date is a worse trade than recording the difference. Named here rather than left for a reader to discover |
| 3.2b The DOI's date matches neither document | Measured, not predicted | This row previously predicted the DOI would inherit `2026-09-18` from the tagged `CITATION.cff`. **That prediction was wrong and is corrected here rather than removed.** Zenodo records `publication_date: 2026-09-20`, which is neither the date in the tag nor the date on `main`. The record was created at `2026-09-19T22:16:18Z`, so the most likely cause is that Zenodo stamps in its own timezone rather than UTC, which puts it past midnight. **Not confirmed**, since one observation cannot distinguish that from any other rule Zenodo applies, and the next release is the trial that would settle it. The practical consequence is that `date-released` in this repository does not drive the DOI's date at all, so keeping the two in agreement is a matter of this project's own consistency and not of controlling the citation record |
| 3.3 Release notes | Mechanism exists, no release to note | `CHANGELOG.md` at repository level, plus one per skill |
| 3.4 Signed releases | Present, and signed by two parties | SSH commit and tag signing, with a signing key held separately from the authentication key. `commit.gpgsign` and `tag.gpgsign` are both true. The default branch ruleset carries `required_signatures`, so an unsigned commit is rejected at the remote rather than merely discouraged; twelve commits were rejected on the first push attempt for exactly this reason. The `v0.1.0` tag verifies locally as a good ED25519 signature and the API reports `verified=true, reason=valid`. **Every authored commit in the 0.1.0 set verifies locally. The merge commit does not, and this row previously claimed otherwise.** `91959631` was produced by merging through the web interface, so it carries GitHub's signature rather than the maintainer's: `git log --format=%G?` reports `E`, cannot check, because that key is not in the local allowed signers file, while the API reports `verified=true`. Both statements are correct and they are about different signers. `E` here means an unknown signer and not a bad signature, which is the same distinction `docs/releasing.md` step 5 draws for tags. The trust anchor for that one commit is the forge, not the maintainer |
| 3.5 Reproducible build | Not applicable | The kit ships documents and two scripts. There is no build |
| 3.6 Dependency declaration | Present, and small by nature | `.github/dependabot.yml`, github-actions only. The repository ships no package manifest, so the surface is this small |
| 3.7 Actions pinned by digest | **Not done** | Both workflows use `actions/checkout@v7`, a tag rather than a digest, raised from v4 by Dependabot on 2026-09-19 after Node 20 was deprecated for actions. Tag pinning is mutable, and a version bump does not change that: v7 is as mutable as v4 was. Resolving it needs the current digest, which has to be read from the upstream repository rather than guessed. **`v0.1.0` shipped with v4**, since the bump landed after the release merge and the tag deliberately points at that merge rather than at the tip |

## 4. Automated checks

| Control | State | Evidence |
|---|---|---|
| 4.1 Mechanical gates in CI | Present | `.github/workflows/gates.yml`, calling `scripts/gates.sh`. Seven gates: em dash ban, private task ID ban, JSON wellformedness, registry self-consistency, skill frontmatter, the reflow script's selftest, and markdown structure |
| 4.2 Those gates proved able to fail | Yes | `scripts/gates.sh --selftest` plants a positive for each of the first five gates and confirms it fires before the real run. Gate six carries three fixture assertions, gate seven plants one positive per markdown rule. Last run 2026-09-18: five of five plants fired, gate seven's rules all fired, then seven of seven gates passed |
| 4.3 Commit hygiene check | Present | `.github/workflows/commit-attribution.yml` rejects AI attribution trailers |
| 4.4 Least-privilege workflow tokens | Present | Both workflows declare `permissions: contents: read`. `commit-attribution.yml` declared none until 2026-09-18, when CodeQL's `actions/missing-workflow-permissions` found it. The gap had been recorded in this table before the scanner found it, and the record alone did not close it |
| 4.5 Static analysis | Present for Python and Actions, absent for shell | CodeQL default setup, languages `python` and `actions`, threat model remote and local. First analysis 2026-09-18. `scripts/gates.sh` and `scripts/link-skills.sh` are shell and therefore unanalysed, which is the remaining gap in this row |
| 4.6 Checks actually binding | **Measured 2026-09-19, and the answer is no** | A workflow gates nothing until it is a required status check in the ruleset on the default branch. Read from the rulesets API: ruleset `23662331`, named `Default`, active, targeting `~DEFAULT_BRANCH`, carrying five rules: `deletion`, `non_fast_forward`, `code_scanning`, `code_quality` and `required_signatures`. **There is no `required_status_checks` rule**, so `gates`, `markdownlint` and `check` run on every push and bind nothing. A failing check does not stop a merge. This row stood unverified from the day it was written until a badge questionnaire forced the question, which is the argument for stating a check's coverage rather than its result. The names to select, when this is fixed, are the **job** names, which are `gates`, `markdownlint` and `check`, not the workflow names |
| 4.7 Second party check on the markdown gate | Present, and it has caught two defects | `markdownlint-cli2` runs the real tool against the same rule IDs as `scripts/mdlint.py`. On its first run, 2026-09-18, it found `MD034` at `CODE_OF_CONDUCT.md` line 52 where `mdlint.py` reported the file clean: our rule fired on a whitespace delimited bare URL and not on one inside parentheses, and its only planted positive used the delimited shape, so the selftest proved the rule could fire rather than that it covered its field. Both are fixed, and MD034 now carries two differently shaped plants. The second defect is in the row below |
| 4.8 The second party check on `skills/` | **Never ran, from the day it was added until 2026-09-18** | The job's second step passed `--config .markdownlint-cli2-skills.jsonc`, a filename `markdownlint-cli2` 0.14.0 refuses, so the step failed before reading any markdown. Correcting the name was not sufficient, because `--config` carries rules and not globs: the file's own `skills/**/*.md` was discarded and the root options file's `!skills/**` then excluded every file the step existed to check. Both were invisible because the step above it was failing on the bare URL in the row above. Now a directory-level options file run with `skills/` as the working directory, verified at the desk on the pinned version: 28 files linted, a planted bare URL reported, and a second top level heading correctly not reported |
| 4.9 Code scanning alerts triaged with a recorded reason | Present | First CodeQL analysis, 2026-09-18, returned three alerts on the default branch. `actions/missing-workflow-permissions` was fixed. Two `py/path-injection` alerts in `scripts/reflow-md.py` lines 229 and 253 were dismissed as false positives: the flagged flow is an argparse positional reaching `open()`, so the path is operator input rather than untrusted data, and no containment check exists that would not also break the intended use |
| 4.10 Alerts outstanding on the release branch | **Nine dismissed with a recorded reason, one fixed by the commit carrying this row** | Ten high security severity alerts in `scripts/mdlint.py`, from the first analysis to run against the release commits. The three `py/path-injection` alerts were dismissed as false positives on 2026-09-18, on the same reasoning as the `reflow-md.py` pair: `sys.argv` paths reach `os.walk` and `open`, so the path is operator input rather than untrusted data. Of the seven `py/polynomial-redos`, six were dismissed as `won't fix` on 2026-09-19 and the seventh is fixed by this commit. The reason string is deliberate and is not interchangeable with the one above: these six are real quadratic patterns rather than false positives. Four of them were independently reproduced on a second host at 15x to 16x scaling when the input quadruples, against a known-quadratic control at 11x and a known-linear control at 2.8x, on inputs no more exotic than a long run of `[` characters. What bounds them is `MAX_LINE`, a 2000 character limit whose guard precedes every affected call site and which reports `MDLINT001` rather than skipping a long line silently. **That bound is per line and not per file.** A worst case line costs roughly 29 ms, and nothing limits how many such lines one contributed file may hold, so the residual is a required check made slow by hostile input rather than one that hangs. Recorded here because the dismissals do not state it and a reader checking them would otherwise have to derive it |

## 5. What the README's badges claim

A badge is an assertion with a click-through. It says a thing exists and lets a
reader verify it in one action. **A badge may point at evidence and never
substitute for it**, so every badge in `README.md` has a row in this document
that says more than the badge does.

| Badge | What it asserts | What it does not |
|---|---|---|
| 5.1 `gates` workflow status | The workflow ran on the default branch and its result | Whether it is a required check, which is the row above |
| 5.2 Licence | The licence is MIT | Anything about the copyright holder, which `LICENSE` names |
| 5.3 Concept DOI | A Zenodo record exists for this project and resolves to its newest version, `10.5281/zenodo.22850481` | That the archived snapshot matches any particular commit, and that its recorded date matches this repository's. Rows 3.2a and 3.2b say where they differ and why |
| 5.4 Latest tagged release | The newest tag with a published GitHub release | Whether that release is the tip of the default branch. It is not, deliberately, per row 3.2 |
| 5.5 Software Heritage archive | That an archived snapshot of this origin exists | Which commit was archived, and when. The badge tracks the origin rather than any tag, so it can be green while the archived snapshot predates the newest release |
| 5.6 OpenSSF Best Practices | That the questionnaire has been answered and what level those answers reach | That the answers were checked by anyone other than this project. The questionnaire is self assessed, and the rows in section 3 of this document are where a reader can disagree with it |

Alt text on a status badge names the indicator rather than its value, because
the image is served by a third party and changes while the text in the
repository does not. A badge reading "passing" in alt text would report a clean
result to a reader who cannot see the image, on every future failure.

**The Software Heritage badge carries its origin percent encoded**, in both the
image URL and the link. The plain form nests one URL inside another, which
`scripts/mdlint.py` reports as `MD034` twice on that line. Both forms were
checked and resolve to the same badge and the same browse page. This is
written down because an encoded URL reads as a mistake, and the obvious
correction reintroduces the finding. The rule over firing on a URL nested in a
link destination is a defect in `mdlint.py` and is not fixed here.

**Absent on purpose:**

- **A coverage badge.** There is no test suite. The Static analysis row above
  says so plainly, which is the honest form of the same information.
- **An OpenSSF Scorecard badge.** Scorecard measures branch protection, pinned
  dependencies and signed releases among others, and three of those are open
  rows in this document. The badge is worth adding once they close, not before.
- **A maintenance or activity badge.** `GOVERNANCE.md` states one maintainer
  and a bus factor of one, which is the same fact without the implication that
  a project's health is a colour.

## 6. Access control

| Control | State | Evidence |
|---|---|---|
| 6.1 Branch protection on the default branch | Present, as a ruleset | Not verifiable from the tree, and verifiable from the API, which is the distinction this row previously missed. Measured 2026-09-19: ruleset `23662331`, named `Default`, active, targeting `~DEFAULT_BRANCH`, carrying five rules: `deletion`, `non_fast_forward`, `code_scanning`, `code_quality` and `required_signatures`. Branch deletion and force push are both blocked. It is a ruleset rather than a classic branch protection object, so a reader looking at the protection endpoint alone will find nothing and conclude wrongly |
| 6.2 Required review before merge | Not applicable as written | One maintainer. `GOVERNANCE.md` states why a self-merge ban would stop work rather than add review |
| 6.3 Signed commits required | Required | `required_signatures` in the ruleset named in 6.1, which is also what row 3.4 has said all along. **This row previously read "Not configured" and contradicted 3.4 inside this same document.** Corrected 2026-09-19. It cannot be set from the tree, which is why it was missed twice |
| 6.4 Two-factor authentication on the account | **Not verifiable from the tree** | Account setting |
| 6.5 Least-privilege collaborator access | Not applicable | No collaborators |

## 7. Where a dependency is allowed to come from

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
| 7.1 Local core | `scripts/mdlint.py` | Yes, it is this project's code | Standard library only, nothing installed |
| 7.2 Local core | `markdownlint-cli2` at the desk | No | Fetches from a registry at run time, and adds a package manifest to a repository that ships none |
| 7.3 Local core | WCAG technique IDs, RFC keyword usage | Yes | Published standards, readable at the source |
| 7.4 Runner | `markdownlint-cli2` pinned in a workflow step | Yes | Disposable container, no token, exact version |
| 7.5 Runner | A third party marketplace action | No | Runs with the workflow's token |
| 7.6 Runner | `actions/checkout` | Yes, with the pin recorded above | First party, and unavoidable |

**Scope.** These rules govern this repository. Material held at higher
sensitivity is governed elsewhere by a stricter rule that is not published
here, and this document does not describe it.

## 8. The gap between this document and a certification

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
