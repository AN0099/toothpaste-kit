# ACMM

An index of the files the kit added to meet ACMM criteria: what each file is, what it does,
and which criterion it was added for. Read it to find out why a file such as
`.cursor/rules/agents.mdc` exists in a repository that holds no rules for Cursor alone.

## What ACMM is here

ACMM is a scale of levels for how far a repository is set up for AI agents to work in it. At lower
levels agents only advise; at higher levels designated agents may open issues and pull requests
directly (issue #23). An outside evaluation scores the kit against it and opens one issue
per unmet criterion, titled `[ACMM Ln] Add ...`. Each issue names its level, a category, a
criterion ID such as `acmm:claude-md`, and a list of paths. A criterion is met when any one of
those paths exists; the issues state the evaluation checks only that the file exists and does not read it.

Levels run upward from L0, and each issue says which level its criterion helps the kit
reach. The issues name three levels, and the files for a fourth have begun:

| Level | Name (from the issues) | What its criteria ask for |
|---|---|---|
| L0 | None given; the issues say "Prerequisites not met" | Guardrails an agent needs first: tests, a pull request template, a code style configuration |
| L2 | Advisory | Instructions an agent reads, and records it learns from |
| L3 | Quality-Gated | Measures of change quality, and a record of each session |
| L4 | No issue opened | Not stated in an issue; the L4 changes are below, one section each |

No issue was opened at L1, so no file was added for it.

Because the evaluation reads only that a file exists, a file added here could pass while empty.
Each file below does the job its name says instead. Most of them restate rules the kit already
holds and name their source, adding no rule of their own, so the source file stays the authority
and the ACMM file is the place an agent or a tool looks first. A met criterion says nothing about
quality; [quality](quality.md) lists what the kit actually measures.

Each entry gives the file, what it is, what it does, and the criterion it was added for, with its
issue number.

## L0: prerequisites

The issues at this level call these the guardrails an agent needs before it can work safely. Two
L0 criteria are still open: end to end tests (issue #25) and a coverage gate (issue #27).

- **[`.github/pull_request_template.md`](../.github/pull_request_template.md).** The form every pull
  request opens with. It asks for the related issue, a checklist of the gates a change must pass,
  and how the author confirmed any step an agent reported, since an agent auditing its own work does
  not count. Added for
  `acmm:prereq-pr-template`, issue #24.
- **[`.editorconfig`](../.editorconfig).** Editor settings: UTF-8, LF line endings, a final newline,
  no trailing whitespace. Markdown style is enforced separately by the gates. Added for
  `acmm:prereq-code-style`, issue #26.
- **[`tests/run`](../tests/run).** The usual entry point for the test suite. It runs
  `./scripts/gates.sh --selftest`, the same command CI runs, so there is one suite and not two.
  Added for `acmm:prereq-test-suite`, issue #28.

## L2: advisory

The issues at this level ask for feedback loops: instructions an agent reads at the start, and
records it learns from. The three instruction files below each point at
[`AGENTS.md`](../AGENTS.md), which points at the files that hold the rules. `AGENTS.md` predates
this work and is not itself an ACMM file. [Risk tiers](risk-tiers.md#per-tool-instruction-files)
makes "adds no rule" a requirement a reviewer checks.

- **[`CLAUDE.md`](../CLAUDE.md).** The file Claude Code reads at session start. It imports
  `AGENTS.md` and holds no rule of its own. Added for `acmm:claude-md`, issue #31.
- **[`.github/copilot-instructions.md`](../.github/copilot-instructions.md).** The same pointer, in
  the place GitHub Copilot reads. Added for `acmm:copilot-instructions`, issue #32.
- **[`.cursor/rules/agents.mdc`](../.cursor/rules/agents.mdc).** The same pointer as an
  always-applied Cursor rule. Added for `acmm:cursor-rules`, issue #33.
- **[`docs/prompts/README.md`](prompts/README.md).** A catalog of the kit's reusable prompts, which
  are its skills. One entry per skill, linking its `SKILL.md` and giving its description copied
  without change. Added for
  `acmm:prompts-catalog`, issue #34.
- **[`corrections.jsonl`](../corrections.jsonl).** An empty file that marks the correction record's
  format and name. It stays empty: real records hold what was said in a conversation, so they live
  in the user's own workspace, outside any repository. Added for `acmm:correction-capture`,
  issue #35.
- **[`docs/corrections.md`](corrections.md).** The format of a correction record: one JSON line per
  point on which an agent corrected itself or challenged the user, with how many challenges were
  made and whether it stood down. Written with `corrections.jsonl` for issue #35, so the empty file
  has a definition. The [Correction Protocol](../skills/working-preferences/SKILL.md#correction-protocol)
  in `working-preferences` gained one line telling the agent to keep these records and read them
  before raising a point again.

## L3: quality-gated

The issues at this level ask for measurement: whether changes are accepted, how they are reviewed,
whether the tests pass on more than one system, and a record of each session.

- **[`docs/metrics.md`](metrics.md).** The pull request acceptance metric: merged against closed
  unmerged, and recorded reviews per pull request, with the read-only `gh` command that computes
  them and the dated figures. It says how to read the rate beside the review count. Added for
  `acmm:pr-acceptance-metric`, issue #38.
- **[`docs/review-rubric.md`](review-rubric.md).** What a reviewer checks on a pull request, in six
  numbered items, each restating a practice the kit already holds and naming its source. Added for
  `acmm:pr-review-rubric`, issue #39.
- **[`.github/workflows/ci.yml`](../.github/workflows/ci.yml).** The test matrix: the gate
  selftest on Linux and macOS, so a portability fault shows up. The gates workflow runs on Linux
  alone. Added for `acmm:ci-matrix`, issue #40.
- **[`docs/quality.md`](quality.md).** The quality dashboard as a page of text: each measure the
  kit has, where it lives, and how to read it, with what the measures leave out. Added for
  `acmm:quality-dashboard`, issue #41.
- **[`.claude/session-summary.md`](../.claude/session-summary.md).** The format a session summary
  takes, from the `session-log` skill: five questions, append only. It is a format only; real
  summaries are provenance and are kept outside the kit. Added for `acmm:session-summary`,
  issue #42.

Changed alongside: [security posture](security-posture.md#3-build-release-and-provenance) row 3.7
now covers `ci.yml` among the workflows that pin `actions/checkout` by tag, and `scripts/reorient`
now parses under bash 3.2.

## L4: the first change

These files arrive together as the first L4 change: an AI security policy, risk tiers, a labeler,
a nightly run and reflections. No issue names these criteria, so no entry here names one; the
labels below are the change's own.

- **[`SECURITY-AI.md`](../SECURITY-AI.md).** What an AI agent may and may not do in the
  kit, and which dependencies it may add. Each rule restates `CONTRIBUTING.md`,
  `GOVERNANCE.md` or the security posture and names its source. Vulnerability reporting stays in
  `SECURITY.md`.
- **[`docs/risk-tiers.md`](risk-tiers.md).** Which changes need which review. A tier is set by the
  paths a change touches, from 1 (documentation) to 4 (gates and workflows), and each tier's review
  includes every tier below it. Tiers grade change risk, not the sensitivity of content.
- **[`.github/labeler.yml`](../.github/labeler.yml).** The path rules that map changed files to
  labels such as `docs`, `skills` and `gates`. Read by the workflow below.
- **[`.github/workflows/labeler.yml`](../.github/workflows/labeler.yml).** Labels each pull
  request from those rules, so its risk tier shows at a glance. A label is a prompt for the
  reviewer and decides nothing. The action is pinned to a full commit and never checks out the
  pull request's code.
- **[`.github/workflows/nightly.yml`](../.github/workflows/nightly.yml).** The gate selftest once a
  day on Linux and macOS, so a change in a runner's tools shows up without a pull request to
  trigger it.
- **[`docs/reflections/README.md`](reflections/README.md).** The format of a reflection entry: a
  bounded record about one documentation row at a pinned version, ending in a one-sentence lesson
  shaped as a rule. Entries are never edited; a correction is a new entry that supersedes the old.
- **[`docs/reflections/001-predicted-doi-date.md`](reflections/001-predicted-doi-date.md).** The
  first entry: a date an outside system assigns is measured from that system, not predicted.
  Drawn from security posture row 3.2b.
- **[`docs/reflections/002-setting-not-visible-from-the-tree.md`](reflections/002-setting-not-visible-from-the-tree.md).**
  A setting that cannot be set from the tree is not established by reading the tree. Drawn from row
  6.3.
- **[`docs/reflections/003-plant-of-one-shape.md`](reflections/003-plant-of-one-shape.md).** A
  planted positive proves that a rule can fire, not that it covers its field. Drawn from row 4.7.

Changed alongside: [document layers](document-layers.md#exceptions) gains exception 5, which admits
a reflection entry as documentation and fixes its format, and
[contributing](../CONTRIBUTING.md#what-kind-of-writing-goes-in-this-repo) now names three
exceptions to the no-archaeology rule. The [changelog](../CHANGELOG.md) records both, with the
maintainer's decision that every per-tool instruction file points at `AGENTS.md`.

## L4: the second change

One workflow, added after the first change and separately from it. As with the first, no issue
names a criterion, so the entry names none.

- **[`.github/workflows/ai-fix.yml`](../.github/workflows/ai-fix.yml).** Acknowledges the `ai-fix`
  label on an issue, once, and routes the issue to the desk. No agent runs in CI, no stored secret
  is used, and the token is limited to issues. The label must exist first:
  `gh label create ai-fix --description "Route to the desk; no agent runs in CI"`.

## L4: the third change

A weekly proposal of job timeouts, and the timeouts it found missing. No issue names a criterion, so
the entry names none.

- **[`scripts/auto-qa-tuner.py`](../scripts/auto-qa-tuner.py), run by
  [`.github/workflows/auto-qa.yml`](../.github/workflows/auto-qa.yml).** Reads the last 100 runs of
  each workflow it tunes and proposes a timeout for each job listed in
  [`.github/auto-qa-tuning.json`](../.github/auto-qa-tuning.json), from how long its runs took and
  whether any ended at the timeout. It writes the proposals to the job summary and never edits a
  workflow: a person accepts one in a pull request. The rules the gates enforce are not thresholds and
  are never tuned; the gates jobs get timeouts like any other job.
- **`timeout-minutes: 5` on the `gates` and `markdownlint` jobs in [`gates.yml`](../.github/workflows/gates.yml).** The
  tuner's first proposals: neither job had a timeout, so each ran under GitHub's 360 minute default,
  and no run has taken a minute.
- **`timeout-minutes: 5` on `check` in
  [`commit-attribution.yml`](../.github/workflows/commit-attribution.yml).** The same proposal for
  the same reason: no timeout, and no run has taken a minute.

## L4: the fourth change

Branch and tag names, and a wider attribution check. No issue names a criterion, so the entry names
none.

- **[`scripts/check-branch-name`](../scripts/check-branch-name).** The one definition of an allowed
  branch or tag name, run by [`.githooks/pre-push`](../.githooks/pre-push), gate 13 in
  [`scripts/gates.sh`](../scripts/gates.sh), and the `branch-name` job in
  [`gates.yml`](../.github/workflows/gates.yml). The rulesets in
  [`.github/rulesets/`](../.github/rulesets/) apply its prefix list at the forge, and
  [`hooks/hookify.branch-name-guard.local.md`](../hooks/hookify.branch-name-guard.local.md) is the
  agent rule, its cases in [`tests/branch-guard-cases.tsv`](../tests/branch-guard-cases.tsv).
- **[`.githooks/commit-msg`](../.githooks/commit-msg), run by
  [`commit-attribution.yml`](../.github/workflows/commit-attribution.yml).** Now also refuses the
  `Assisted-by:` and `Agent-<name>:` trailers, and the workflow runs the hook rather than a copy of
  its pattern. Gate 14 runs it against [`tests/attribution-cases.tsv`](../tests/attribution-cases.tsv).

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
