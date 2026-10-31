# Security for AI agents

What an AI agent may and may not do in this repository. Each rule restates `CONTRIBUTING.md`,
`GOVERNANCE.md` or `docs/security-posture.md` and names its source; this file adds no rule of its own. Vulnerability
reporting is in `SECURITY.md`.

A change made by an agent follows the same rules as any other change. Source: `AGENTS.md`, "Rules
for every change".

## An agent may

- Edit files and prepare a change for a person to review. Source: `docs/security-posture.md`, row
  2.5, and `GOVERNANCE.md`, "What is deliberately not delegated".
- Run the checks the way CI runs them, with `./scripts/gates.sh --selftest`. Source:
  `CONTRIBUTING.md`, "Run the checks the way CI runs them".
- Raise a finding in the issue or pull request when something looks wrong or inconsistent. Source:
  `CONTRIBUTING.md`, "Raise findings instead of quietly resolving them".

## An agent may not

- Commit, merge, tag or push. These are not delegated: an agent edits and stages, and a person
  commits and pushes. Source: `docs/security-posture.md`, row 2.5, and `GOVERNANCE.md`, "What is
  deliberately not delegated".
- Report its own work as verified. A completion claim is confirmed by a party other than the one
  making it; an agent auditing its own work does not satisfy this. Source: `CONTRIBUTING.md`,
  "Verify completion claims before repeating them".
- Put tool attribution in a change prepared for commit, its proposed commit message or a pull
  request body: no `Co-Authored-By` line naming an AI, no session link, no generated-with footer.
  Source: `CONTRIBUTING.md`, "Commits and pull requests".
- Leave em dashes in text it drafted. Check the output mechanically before the change is handed
  over for commit. Source: `CONTRIBUTING.md`, "Rules that apply to every change".
- Use a task ID other than a public `TK-` id. Source: `CONTRIBUTING.md`, "Use public task IDs only".
- Stage operational or business material, or anything that names a client, an internal process,
  or a person's private details. If the side of that line is unclear, ask before staging. Source:
  `CONTRIBUTING.md`, "What does not belong here".
- Quietly resolve a disagreement with a unilateral fix. Source: `CONTRIBUTING.md`, "Raise findings
  instead of quietly resolving them".

## Dependencies an agent may add

| Where | Rule | Source |
|---|---|---|
| `scripts/`, `hooks/`, `skills/` | Code MUST be this project's own, already present on a plain system, or an implementation of a published standard. It MUST NOT be fetched from a package registry at run time | `docs/security-posture.md`, section 7, the local core |
| A workflow | A pinned package MAY be invoked in a step. A third party action MUST NOT be used. A pinned version MUST be exact | `docs/security-posture.md`, section 7, the runner |

Keywords are BCP 14, per `docs/document-layers.md`.

## What the controls here are not

The gates and hook rules are pattern-based. A hook rule is meant to state its own limits so that it is not
mistaken for a boundary. Source: `CONTRIBUTING.md`, "Hook rules". The gates do not cover en
dashes, prose quality, internal link validity, or whether any document's claims are true. Source:
`CONTRIBUTING.md`, "What these gates do not cover".

Workflow token permissions are current practice, not a rule: each workflow declares its own
`permissions`. Each declares `contents: read` except `ai-fix.yml`, which declares only
`issues: write` to comment on a labelled issue; `labeler.yml` adds `pull-requests: write` to label
pull requests. Source: the workflow files in `.github/workflows/`; `docs/security-posture.md`, row
4.4, records the practice.

The dependency rules above govern this repository. Source: `docs/security-posture.md`, section 7,
"Scope", which scopes section 7.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
