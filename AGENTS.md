# Agents

Instructions for a coding agent working in this repository. They point at the files that hold the
rules; nothing here adds one.

- **Rules for every change:** `CONTRIBUTING.md`, which a change made by an agent follows like any other.
- **Terms of art:** `docs/glossary.md`, each term with the file that defines it.
- **Checks:** `./scripts/gates.sh --selftest`, the same command CI runs, also run by `tests/run`. Its
  header states what each gate covers. Checks that need an installed tool, REUSE among them, are
  `./scripts/compliance.sh --selftest`.
- **Skills:** read `skills/skill-creation/SKILL.md` before changing one.
- **Branch names:** `CONTRIBUTING.md`, "Branch and tag names", checked by `scripts/check-branch-name`.
- **Commits:** `CONTRIBUTING.md`, "Commits and pull requests": provenance as `Assisted-by:` and
  `Agent-Effort:` trailers with values read from the tool, never a co-author line, session link or
  footer. The `Signed-off-by:` line is the human's; an agent never adds one for them.
- **Pull requests:** `.github/pull_request_template.md` lists what a reviewer expects.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
