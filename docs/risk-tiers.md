# Risk tiers

Which changes need which review. The tier structure is this document's own arrangement: a tier is
set by what a change touches, a change that touches several paths takes the highest tier among
them, and each tier's review includes every tier below it. Each requirement within a tier restates
a rule held elsewhere in the kit and names its source.

The `labeler` workflow adds a path label to each pull request, which shows the tier at a glance.
The label is a prompt for the reviewer and decides nothing.

## The tiers

| Tier | Touches | Labels |
|---|---|---|
| 1 | Documentation and repository metadata: `docs/`, root Markdown files, `examples/`, `LICENSE`, `CITATION.cff`, `corrections.jsonl`, `.editorconfig`, `.gitignore` | `docs`, `examples`. `.editorconfig` and `.gitignore` carry no label |
| 2 | Skills, hook rules and agent configuration: `skills/`, `hooks/`, `.claude/`, `.cursor/` | `skills`, `hooks`, `agent-config` |
| 3 | Interfaces: a skill's frontmatter, `orchestration/` schemas, `protocol.md`, `taxonomy.md`, a documented rule | `orchestration`. A frontmatter or rule change carries no label of its own, so the reviewer sets the tier |
| 4 | Gates and workflows: `scripts/`, `tests/`, `.githooks/`, `.github/`, the `redaction-gate` skill, and gate configuration (`.markdownlint-cli2.jsonc`, `skills/.markdownlint-cli2.jsonc`) | `gates`, `workflows` |

## Per-tool instruction files

Every per-tool instruction file (`CLAUDE.md`, `.github/copilot-instructions.md` and
`.cursor/rules/agents.mdc`) points at `AGENTS.md` and adds no rule of its own. A change to one is
reviewed against this requirement in the tier its path sits in: tier 1 for `CLAUDE.md`, tier 2 for
`.cursor/rules/agents.mdc`, and tier 4 for `.github/copilot-instructions.md`. Source: the
maintainer's decision of 2026-10-20, recorded in the root `CHANGELOG.md` entry for `docs/risk-tiers.md`.

## Tier 1: documentation and repository metadata

Every requirement here applies to every tier 1 path, except the third, which applies to a document,
and the fifth, which applies to `CLAUDE.md`.

- `./scripts/gates.sh --selftest` passes, and the `gates` and `markdownlint` jobs in CI are green.
  Source: `GOVERNANCE.md`, "How a change lands", step 3, and `CONTRIBUTING.md`, "Run the checks the
  way CI runs them".
- No em dashes, public `TK-` task IDs only, no tool attribution. Source: `CONTRIBUTING.md`, "Rules
  that apply to every change" and "Commits and pull requests".
- A document is written for a person with a task, with no archaeology outside the exceptions in
  `docs/document-layers.md`. Source: `CONTRIBUTING.md`, "What kind of writing goes in this repo",
  and `docs/document-layers.md`, "Exceptions".
- A verifier other than the author confirms any completion claim. Source: `CONTRIBUTING.md`,
  "Verify completion claims before repeating them".
- `CLAUDE.md` meets the requirement in [Per-tool instruction files](#per-tool-instruction-files).
  Source: that section.

## Tier 2: skills, hook rules and agent configuration

This tier covers skills under `skills/`, hook rules under `hooks/` and agent configuration under
`.claude/` and `.cursor/`, and the first requirement below applies to a skill.

- The author read `skills/skill-creation/SKILL.md` first, frontmatter carries `name` and
  `description`, and a rename was followed by `grep -rn '<old-name>' skills/`. Source:
  `CONTRIBUTING.md`, "Skills", and `.github/pull_request_template.md`.
- A hook rule was tested against three cases: something that must trip it, something legitimate that
  must not, and the rule's own documentation. Its body states its limits. Source: `CONTRIBUTING.md`,
  "Hook rules".
- A skill or hook that leaks material it was meant to keep out is a vulnerability. Source:
  `SECURITY.md`, "What counts as a vulnerability here".
- `.claude/settings.json` keeps `attribution` empty and the session link disabled. It is the first
  of three layers against tool attribution, and it does not bind: the `commit-attribution`
  workflow, in tier 4, is the layer that binds. Source: `CONTRIBUTING.md`, "Commits and pull
  requests".
- An agent instruction file under `.cursor/` meets the requirement in
  [Per-tool instruction files](#per-tool-instruction-files). Source: that section.

## Tier 3: interfaces

- An issue is opened before the pull request. Source: `GOVERNANCE.md`, "How a change lands", step 1.
- A changed orchestration field changes the schema, `orchestration/protocol.md` and
  `orchestration/taxonomy.md` together. Source: `CONTRIBUTING.md`, "Orchestration".
- A change to the decision process is announced in the repository `CHANGELOG.md`. Source:
  `GOVERNANCE.md`, "Changing this document".

## Tier 4: gates and workflows

- A gate that fails open is the highest severity defect this project can have. The reviewer runs the
  check rather than reading the diff. Source: `GOVERNANCE.md`, "Security decisions", for the
  severity, and "How a change lands", for running the check.
- A new or changed gate is shown to fire on a planted positive before a clean result is trusted, and
  states its coverage. Source: `CONTRIBUTING.md`, "Run the checks the way CI runs them", and the
  header of `scripts/gates.sh`.
- The local copy and the CI copy of a gate stay one text. Source: `.github/workflows/gates.yml`, the
  header comment.
- A workflow uses no third party action and pins versions exactly. Source:
  `docs/security-posture.md`, section 7. As current practice rather than a rule, each workflow
  declares its own `permissions`, `contents: read` throughout, and `labeler.yml` adds
  `pull-requests: write` to label pull requests; row 4.4 records the practice.
- A workflow binds only once it is a required status check in the ruleset on the default branch.
  Source: `docs/security-posture.md`, row 4.6.
- The rulesets in `.github/rulesets/` and the branch name guard,
  `hooks/hookify.branch-name-guard.local.md`, are tier 4, although the guard sits in `hooks/`: its
  cases in `tests/branch-guard-cases.tsv` are a gate, and a weakened pattern fails open. Source:
  `CONTRIBUTING.md`, "Branch and tag names".
- `.github/copilot-instructions.md` meets the requirement in
  [Per-tool instruction files](#per-tool-instruction-files). Source: that section.

## What this does not cover

The tiers grade change risk. They do not grade the sensitivity of content, and they do not replace a
reviewer's judgment of a design or of whether a document's claims are true.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
