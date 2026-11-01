# What this changes

<!-- One or two sentences. What changed, and why. -->

<!-- Tick every box in a section that applies. Where a section or an item does not apply, replace its boxes with a line saying "Does not apply" and why; scripts/check-pr-body fails on an empty box. -->

## Related issue or task

<!-- Link the issue, or give the public TK- id (for example TK-014). Do not use private task ID formats; CONTRIBUTING.md, "Use public task IDs only", defines them. -->

## Checks

Run this before opening the PR. It is the same command the `gates` job in CI runs.

```sh
./scripts/gates.sh --selftest
```

- [ ] `./scripts/gates.sh --selftest` passes
- [ ] No em dashes in any file I changed
- [ ] Only public `TK-` task IDs appear
- [ ] Every `.json` I touched parses
- [ ] Markdown I touched passes `scripts/mdlint.py`
- [ ] Every commit is signed off (`git commit -s`)
- [ ] No `Co-Authored-By` naming an AI, session link or generated-with footer in my commits or this PR

## If this touches a skill

- [ ] I read `skills/skill-creation/SKILL.md` first
- [ ] `name` and `description` are in the frontmatter
- [ ] I ran `grep -rn '<old-name>' skills/` after any rename

## If this changes an orchestration message field

- [ ] The schema that holds the field, `protocol.md` and `taxonomy.md` changed together

## Verification

<!-- If an agent reported writing a file or finishing a step, say how you
confirmed it yourself. An agent auditing its own work does not count. -->

## Findings

<!-- Anything that looked wrong or inconsistent and that you did not fix here. Raise it instead of resolving it quietly. -->

## Drafted with an agent?

<!-- If no agent drafted any of it, replace the box with the line "No." and delete the Provenance section. -->

- [ ] Yes, and I checked the output mechanically

<details>
<summary>Provenance</summary>

<!-- If you ticked Yes: copy the Assisted-by and Agent-Effort trailers from your commits, one per line. Name any agent whose model is not on record as such, in words. Delete this section if no agent drafted any of it. -->

<!-- Then, from the repository root, run `python3 scripts/spdx-fragment.py origin/main..HEAD` (two dots; use the base your branch starts from if it is not origin/main). It prints an SPDX 3.0.1 JSON document built from those same trailers. Paste the output below them in a json code block. Values for each model come from scripts/spdx-models.json, which ships empty; for a model with no entry the script marks the package noAssertion and prints a warning, so say so here instead of guessing the values. -->

</details>

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
