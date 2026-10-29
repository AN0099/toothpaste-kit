# Project State

Current status of toothpaste-kit. For what the project is and how to use it, start with
`README.md`.

Last updated 2026-10-28.

## Live

Eighteen skills in three classes.

Seven govern agent behavior and are in daily use: `working-preferences`, `document-standards`,
`technical-documents`, `surface-regimes`, `skill-creation`, `skill-discovery`, `commands`.

Eight are human-invoked procedures: `redaction-gate`, `session-close`,
`daily-dashboard`, `daily-review`, `weekly-review`, `monthly-review`, `session-log` and `merge-proxy`. All eight set `disable-model-invocation`, which is the point in
each case. A gate a model can invoke to satisfy itself is not a gate, and an agent should not decide
on its own that a session is over or that a working day has started.

Three are procedures an agent may run on its own at a clean boundary: `orient`, `jot` and `touch`.
None sets `disable-model-invocation`, because each reads or records and none decides anything, and
none satisfies `session-log` or `session-close`.

`hooks/` carries seven `hookify` rule examples, inert where they sit. `scripts/` carries
`link-skills.sh`, `reflow-md.py` with a fixture and `--selftest`, and `remote-level.sh`, the remote
classifier `merge-proxy` runs, with its own `--selftest`, and `reorient`, the observing half of
`orient`, whose `--selftest` runs it on `examples/workspace/`. `link-skills.sh`
writes relative symlink targets where `ln -r` exists, so the links survive the tree being moved.
`examples/workspace/` is the workspace `docs/quickstart.md` copies, and
`scripts/check-workspace-stubs.py` checks its stubs against `docs/standing-documents.md`.

The orchestration protocol has run relay traffic across Claude, local models, and several vendor
surfaces. The message schema requires a seven-field capability profile as the normative part, and
treats a product name as a label resolved through `orchestration/registry/`.
Existing relay traffic stays wire-valid, since the eight Anthropic surface strings are unchanged and
became the seed entries of `registry/anthropic.json`. Build against `capability` rather than against
`surface`.

## In progress

Two skill families are specced and not yet built:

- **reference-architecture**: governs how specific a technical document can be before it stops
  being safe to publish.
- **content-pipeline**: note-mining, public-writing register, and publishing workflow.

## Recent changes

The changes up to 0.1.0. Each later release has its own section below, newest first, starting
with Unreleased; `CHANGELOG.md` is the full log.

- **0.1.0 release preparation.** `docs/releasing.md` added, holding the versioning scheme and a
  signed-tag procedure that separates a GitHub signing key from an authentication key.
  `docs/security-posture.md` added as the authoritative per-row posture record, and it owns the
  section stating what the README's badges claim and what they do not. `GOVERNANCE.md`,
  `.github/dependabot.yml` and the `gates.yml` workflow added. `README.md` gained a badge line and
  an accessibility paragraph directly below it, so a reader meets the evidence before the claims.
- `scripts/mdlint.py` no longer diverges from markdownlint on MD056. It counted raw pipe
  characters, so a correctly escaped GFM cell read as an extra column and following the rule could
  not make a file clean. markdownlint 0.41.1 counts micromark table tokens instead, which was read
  out of its `lib/md056.mjs` rather than recalled. An escaped pipe is now removed before counting,
  with a paired selftest that also proves the rule still fires on a real extra cell. Found by
  second-party review.
- The orchestration event schema now requires a `capability` profile and the `regime` derived from
  it, and treats `surface` as an optional namespaced string resolved against a new `registry/`
  directory. Human agents carry `kind` and a `role` of `relay` or `participant`, which retires the
  two human members of the old surface enum and with them the meaningless combination `kind: llm`
  with `surface: human-relay`. Every registry entry carries `confidence`, `verified_on`, and
  `sources`, so a capability claim about a product that ships weekly has its own expiry date.
  `anthropic.json` holds eight surfaces; `openai.json`, `google.json`, and `local.json` are empty and
  are the intended first-contribution surface. Reasoning in `orchestration/CHANGELOG.md`.
- `surface-regimes` went to v3, deriving regime from the capability profile and re-keying its
  activation table from seven product-name rows to three regime rows. No activation decision changed
  for any of the seven original rows. The Failure-Mode Note carried forward verbatim.
- `orchestration/ingestion/` lost a duplicate. `VENDOR-AGNOSTIC-DIGEST-SPEC-UPGRADE.md` was a strict
  superset of its base file and was folded into it, which also picked up a typo fix and a run-on
  that had swallowed a heading.
- `SECURITY.md`, `CODE_OF_CONDUCT.md`, `CITATION.cff`, `.github/ISSUE_TEMPLATE/` (four files) and
  the `README.md` Contributing section are **committed**. The code of conduct's reporting contact
  is a real address.

- `redaction-gate` went to v2.1, carrying a fix and a feature. The fix restores a Step 4 rule that
  was present in the maintainer's working copy and described in the CHANGELOG while being absent
  from the published skill: a redaction is proposed only where the content is unnecessary, and a
  load-bearing finding halts and warns instead. It was dropped by the pass that generalized the
  skill for publication, alongside a dated internal statistic that was correctly removed. Anyone
  running the published skill before v2.1 had a gate weaker than its own documentation. The feature
  is a Step 3 derived-values check: a corpus pass matches strings, so it cannot see a value computed
  from restricted content rather than copied out of it, and the check is syntactic rather than an
  index of known digests, since building that index would assemble the thing it exists to control.
- The two procedure skills are no longer maintained as separate local copies. `session-close` and
  `redaction-gate` were real directories in the maintainer's skills folder, diverging from the
  published versions; both are now symlinks like the other seven, so this repo is the single source
  for all nine. The `redaction-gate` defect above was found by diffing those copies while retiring
  them, which is the only reason it surfaced.
- `session-close` now names `CLAUDE.md` as the place a tree should say where its standing-files list
  lives. The generic instruction told the reader to substitute their own list and never said where
  the list should be recorded, which left the pointer nowhere once the tree-specific copy was gone.

- Published. The repository was deleted and recreated to clear AI attribution trailers from three
  commits, since force-pushed commits stay reachable on GitHub by SHA. Three enforcement layers are
  built: `.claude/settings.json` suppressing the trailers at source, an opt-in `commit-msg` hook,
  and a `commit-attribution` workflow. The first two are bypassable by anyone who has not opted in.
  The third binds only while it is set as a required status check in a ruleset on the default
  branch. Whether that ruleset is configured on this repository is unverified.
  `docs/security-posture.md` owns that row. See also `CONTRIBUTING.md`.
- `docs/standing-documents.md` added, describing the document set `redaction-gate` and
  `session-close` assume. Structure and mechanics are shared; contents are not.
- `README.md`'s framing section rewritten around determinism rather than around fusion being
  impossible, and the accessibility consequence stated as fitment rather than accommodation.

- A full-repo audit found six inaccuracies and fixed them. The largest: `commands` routed to
  sixteen per-command files that never existed in any commit. `README.md` still pointed at the
  pre-reorganization schema paths. `skill-discovery` counted the family as six skills.
- `document-standards` went to v2. Two instructions in it could not be followed as written, and a
  third case, a request too underspecified to generate against, had no rule at all. Found by
  running the skill against live document tasks. See that skill's `CHANGELOG.md`.
- The `lib-*` reference-library toolchain moved out of this repo. It served the maintainer's
  personal knowledge base rather than the kit, and now lives alongside that.
- `README.md`, `CONTRIBUTING.md`, and `philosophy.md` were rewritten. The old versions carried
  operational detail that belonged elsewhere and pointed at files this repo does not contain.

## Known gaps

- No eval suite for the skills in this repo (TK-069). An eval harness covering
  `document-standards` exists and is not ready to ship here. Skills are otherwise
  validated by use and review. The CI half of this gap is closed: `gates.yml` is
  installed and runs eleven mechanical gates plus a second-party markdown lint, so
  the checks `CONTRIBUTING.md` documents are now enforced rather than merely
  documented.
- No drift detection for this repo's own documents (TK-070). A checker exists that records a source path
  and a content hash next to a claim and rehashes on demand, reporting whether
  a claim's source is current, moved, changed, or gone. It is deterministic, costs no tokens, and is
  not ready to ship here. The full-repo audit that found six inaccuracies below is the kind of pass
  it is meant to make unnecessary.
- **Closed 2026-09-19: 0.1.0 is released.** Tag `v0.1.0`, six badges on the README, and the
  `identifiers` block in `CITATION.cff` filled with the Zenodo concept DOI rather than left
  commented. This bullet previously named the release as the critical path for the security
  posture work; that path is now walked, so what follows is what the release left open rather
  than what it blocks.
  - **The OpenSSF Best Practices Badge reads 97 percent.** Project 14726. Exactly
    two criteria are short, `know_secure_design` and `know_common_errors`, both `MUST` and both
    marked Unmet by choice pending an assessment rather than left unanswered. The figure was
    derived by parsing all 67 passing criteria out of `criteria.yml` and checking each answer
    against its own attributes, which is why it is two rather than an estimate. The badge image
    is live, so the questionnaire reaching passing updates the README with no further commit.
  - **Branch protection is in place and is stronger than the bullet assumed.** Ruleset
    `23662331` carries six rules with five required contexts bound. A direct push to the default
    branch cannot succeed at all, established by attempting one: the `code_scanning` rule demands
    CodeQL results for a commit the remote has not accepted. No `pull_request` rule declares
    this, so the constraint is emergent rather than configured, and `docs/security-posture.md`
    rows 4.6 and 6.1 now say so.
  - **Still open and the maintainer's:** the education suite that would let the two `MUST`
    criteria be answered Met (TK-071).
- Skill interfaces now have a deprecation rule (`docs/releasing.md`, Deprecation), and no
  interface change has cited it yet (TK-073). How a skill's revision relates to the kit version
  is stated in the same file, under Skill revisions (TK-072).
- Three follow-ups left open by the 0.4.0 checks. Two lines of `scripts/reorient`'s mail
  check have no selftest row, though its behavior there has not been shown wrong.
  `weekly-review` does not record each chase in the task note, which `monthly-review` needs
  in order to count them. `orient` names `scripts/reorient` by a path that exists only in a kit
  clone, not in a workspace.

## Security posture, and what is actually in place

**Nothing here is claimed as achieved.** Each row states what exists in the tree today, checked
rather than recalled.

| Expected by a reviewer | In this repository today |
|---|---|
| License | `LICENSE`, present, Apache 2.0 from release 0.5.0; `CITATION.cff` and `README.md` name the individual copyright holder |
| Security policy | `SECURITY.md`, present. No coordinated-disclosure timeline stated |
| Code of conduct | `CODE_OF_CONDUCT.md`, present, with a real reporting address and no escalation body, stated plainly |
| Contribution guide | `CONTRIBUTING.md`, present. Documents two mechanical checks that nothing enforces |
| Citation metadata | `CITATION.cff`, present, `version` and `date-released` commented out |
| Issue templates | Four under `.github/ISSUE_TEMPLATE/` |
| Governance and roles | **Absent.** No `GOVERNANCE.md`, no stated decision process, one maintainer |
| Automated checks in CI | **Two workflows**, `commit-attribution.yml` and `gates.yml`. The latter runs eleven mechanical gates plus a second-party markdown lint |
| Versioning and releases | **Absent.** No tags, no releases, no release notes |
| Dependency management | **Absent.** No `dependabot.yml`. The repository ships no package manifest, which is why |
| Static analysis | **Absent.** The tree is Markdown, shell and one Python script; nothing scans the shell or the Python |
| Signed commits or releases | **Not configured in this repository** |
| Branch protection | Not verifiable from the tree. It is a host setting and belongs in a written record |

**`docs/security-posture.md` is authoritative for this table** and carries an evidence column per
row; `docs/releasing.md` holds the versioning scheme. The shorter table here is kept because it is
the record of what was true when the work started.

Since that record, governance, versioning and branch protection have closed; see
`docs/security-posture.md` for each row's current state. The ordering above is not a plan.
The plan, once the target tier is fixed, belongs in its own document with one row per criterion and
a pointer to the evidence, because a posture claim without per-criterion evidence is the same
unverifiable clean result this project's own conventions reject.

## Unreleased

Merged to `main` after 0.5.0, listed under Unreleased in `CHANGELOG.md`.

- **Orchestration digest (pull request #60).** One digest spec, with the extraction packet linked
  from it.
- **Branch guard (pull request #61).** The branch guard sees quoted global options, and its known
  limits are stated.
- **Frontmatter gate (pull request #63).** A gate checks each skill description's length and YAML
  form.
- **`scripts/check-qblock` (pull request #62).** A checker for the closing question block, with
  cases in `tests/qblock-cases/`.
- **Session skill pointers (pull request #65).** `orient`, `session-log` and `session-close` point
  at the shipped `examples/workspace/CLAUDE.md`.
- **`scripts/link-skills.sh` (pull request #66).** Prints its plan before writing, and `--dry-run`
  writes nothing.
- **Registry schema check (pull request #67).** `scripts/schema-check.py` validates every vendor
  file against the registry schema.
- **Commit provenance (pull request #68).** Commits record tool help as `Assisted-by:` and
  `Agent-Effort:` trailers and need a sign-off; `scripts/check-pr-body` checks a pull request body
  against the template.

## In v0.5.0

- **Licence and provenance.** The licence moves to Apache 2.0 (pull request #57), with REUSE
  compliance (pull request #58): every file declares its copyright and licence, and
  `scripts/compliance.sh` runs `reuse lint`. Contributions carry a Developer Certificate of Origin
  sign-off.
- **Branch and tag names (pull request #59).** `scripts/check-branch-name` is the one definition of
  an allowed name, run by `.githooks/pre-push`, a gate and the `branch-name` CI job.
- **`scripts/gates.sh`** goes from ten gates to fourteen.
- **The second L4 change.** `.github/workflows/ai-fix.yml` acknowledges the `ai-fix` label
  once per issue and routes the issue to the desk; no agent runs in CI and no stored secret is
  used. `SECURITY-AI.md`, `docs/acmm.md` and security posture rows 3.7 and 4.4 name it.
- **`docs/acmm.md` (pull request #46).** An index of the files the kit added for ACMM
  criteria, naming the criterion and pull request behind each. Security posture rows 3.7 and
  4.4 state the rule for every workflow instead of a count, and `daily-review` step 5 names the
  Most Important Task from the order the review proposes.
- **ACMM L4, part a (pull request #45).** `SECURITY-AI.md`; `docs/risk-tiers.md`, including the
  rule that every per-tool instruction file points at `AGENTS.md` and adds no rule; a path
  labeler (`.github/labeler.yml` and its workflow); `.github/workflows/nightly.yml`; and
  `docs/reflections/`, three filed entries and a README. `docs/document-layers.md` gains
  exception 5, under which a filed reflection may be reformatted but never reworded.
- **ACMM L3 measurement (pull request #44).** `docs/metrics.md`, `docs/review-rubric.md`,
  `docs/quality.md`, `.claude/session-summary.md`, and `.github/workflows/ci.yml`, a test matrix
  on Linux and macOS. `scripts/reorient` now parses under bash 3.2.
- **`docs/concepts.md`.** Each idea a contributor needs, grouped under four headings, with a
  link to every file that carries it, deepest first; the README links it beside the glossary.
- **Skill cross-references.** Four skills point to `skill-creation` and `skill-discovery`;
  recorded in `CHANGELOG.md` under Unreleased.
- **Agent instruction files and two learning artifacts (ACMM L2, issues #31 to #35).**
  `CLAUDE.md`, `.github/copilot-instructions.md` and `.cursor/rules/agents.mdc` point at
  `AGENTS.md` and add no rule of their own; `docs/prompts/README.md` catalogs the skills from
  their descriptions; `docs/corrections.md` gives the correction record's format, and the
  Correction Protocol now keeps those records in the user's own workspace, outside any
  repository, with the root `corrections.jsonl` left empty.
- **`docs/glossary.md`.** The kit's terms of art, one entry each, with a link
  to the file that defines each in full. The README links it, and
  `docs/document-accessibility.md` now claims G62 (providing a glossary) and
  names G55 (linking to definitions) as a gap.
- **`skills/session-log` v3.** The description says the capture records
  decisions, corrections, open questions and findings, and `orient` v3,
  `session-close` v6, the README and `docs/quickstart.md` describe it to match.
  Only the description was tested.
- **Contributor files.** A pull request template, `.editorconfig`, a root
  `AGENTS.md` that points coding agents at the files holding the rules, and
  `tests/run`, the usual entry point for `scripts/gates.sh --selftest`.
- **`scripts/link-skills.sh --selftest`**, run by an eleventh gate (TK-111).
- **`scripts/reorient`** says `TASK not checked` when `ps` is missing, rather
  than reporting no shells (TK-112).
- **`scripts/reorient` names what it skips.** A path among the root,
  `projects/*` and `REORIENT_REPOS` that is not a repository gets a
  `not a repository` line, and MAIL says `none` or `not read` instead of
  printing nothing. Five selftest checks cover it.

## In v0.4.0

- **`skills/merge-proxy/`.** A procedure a person invokes: for that session an
  agent may run and push a trunk merge on a repository whose remote is
  internal or absent, after explaining the plan and halting for approval of
  each merge. `scripts/remote-level.sh` classifies the remote first; a ninth
  gate runs its selftest.
- **`skills/weekly-review/`.** The once-a-week pass over a task board's
  slower lanes: Waiting blockers, carried work, the Done lane, and one
  important task given a day.
- **`skills/monthly-review/`.** The once-a-month pass: Someday adopted or
  rejected, long-stalled Waiting work questioned, and archive candidates
  chosen by the person, leaving by the reference or the trash door.
- **`scripts/reorient`.** The `orient` skill's observing tool, shipped with
  it at last; a tenth gate runs its selftest on `examples/workspace/`.
- **The issue #11 fix.** `docs/quickstart.md` is one path in six steps;
  alternatives moved to a new installing guide, `docs/installing.md`; the
  quickstart copies `examples/workspace/`, whose stubs an eighth gate checks.
  `session-close` v5 (BREAKING) and `session-log` v2 came with it.
- **Skill versioning in `docs/releasing.md`.** Skill revisions, a skill's
  interface, and a Deprecation rule.
- **Selftest rows for `scripts/reorient`**, added after the 2026-10-09 cutoff
  and touching the selftest only.

## In v0.3.0

- **`skills/daily-review/`.** The once-a-day pass over a task board's lanes,
  split out of `daily-dashboard`. It proposes moves and asks; it moves
  nothing the person did not answer.
- **A Cadence section in `docs/releasing.md`.** A release review every two
  weeks on a Tuesday, which publishes a release only when the review admits
  one.
- **`CITATION.cff` lists only the concept DOI.** Each version DOI is recorded
  in `docs/releasing.md` by the release after it.

## In v0.2.0

- **`orchestration/ROLES.md`.** Defines operator, lead, aide and minions as an
  axis of authority over a decision, explicitly separate from the three axes
  the kit already had: clearance, working surface, and reach. It also states
  that persona is not role, and leaves persona unbuilt.
- **`skills/orient/`.** It does the judgement half of a reorientation and
  delegates the mechanical half to whatever state tool the adopting tree has,
  rather than shipping one.
- **`skills/jot/` and `skills/touch/`.** Two small skills an agent may call
  itself at a clean boundary: `jot` appends a short record of decisions,
  corrections and findings, and `touch` makes one fact-level update to a
  standing file. Their shared rules are in `docs/partial-captures.md`,
  including the one that matters most: neither satisfies `session-log` or
  `session-close`, and each marks its entry so it cannot be mistaken for
  one.
- **`working-preferences` v5.** Adds a Context Cadence section, and replaces
  the NEXT block with Questions and Answers: three labeled questions, each
  closing with the codes it accepts, answered as `f q1; 2 q2`. Mirrored in
  `docs/interface-contract.md`, `docs/control-layers.md` and `skills/commands/`.
- **`README.md` and `docs/quickstart.md`**, the quickstart batch.

## Open questions

- Whether `orchestration/registry/` stays JSON or moves to YAML. It was authored as JSON for
  consistency with `schemas/`, without weighing that against the declarative-configuration
  conventions the target audience works in. Needs dev-2.
- **Copyright holder: settled.** Bridle Works is the name of this project and is not a formed
  entity, so it cannot hold a copyright. Copyright rests with the individual authors, currently one
  person, and `CITATION.cff` and `README.md` name that person. Forming Bridle Works later and moving the copyright to
  it would require a written assignment from every individual holder, which is a formality today
  and a collection problem once outside contributors land.

- Whether `skills/orient/` should ship a reference state tool or keep delegating. Delegating
  keeps it portable and leaves an adopter with a skill whose first phase they must supply.
- Whether `commands` should split, since the twenty-seven-command vocabulary has grown informal
  extensions that were never audited against the original set.
- Whether skills should declare version compatibility with each other, given how often they
  cross-reference by name.
- Whether the two closing-section names `skill-creation` permits are too narrow. `surface-regimes`
  closes with `# Failure-Mode Note` and `technical-documents` with `# Templates`. Both are more
  informative than the generic names the checklist allows, which suggests the rule needs widening
  rather than those two files needing renaming.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
