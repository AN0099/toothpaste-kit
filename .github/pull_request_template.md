# What this changes

<!-- One or two sentences. What changed, and why. -->

<!-- Keep every heading: scripts/check-pr-body checks that each is present and in order. Where a section does not apply, write "Does not apply" and why. -->

## Related issue or task

<!-- Link the issue, or give the public TK- id (for example TK-014). Do not use private task ID formats; CONTRIBUTING.md, "Use public task IDs only", defines them. -->

## Checks

Run this before opening the PR. It is the same command the `gates` job in CI runs.

```sh
./scripts/gates.sh --selftest
```

- [ ] `./scripts/gates.sh --selftest` passes
- [ ] Every commit is signed off (`git commit -s`)

## If this touches a skill

<!-- Read skills/skill-creation/SKILL.md first, keep name and description in the frontmatter, and after any rename run grep -rn '<old-name>' skills/. Say what you did. -->

## If this changes an orchestration message field

<!-- The schema that holds the field, protocol.md and taxonomy.md change together. Say which you changed. -->

## Verification

<!-- If an agent reported writing a file or finishing a step, say how you
confirmed it yourself. An agent auditing its own work does not count. -->

## Findings

<!-- Anything that looked wrong or inconsistent and that you did not fix here. Raise it instead of resolving it quietly. -->

## Drafted with an agent?

<!-- If no agent drafted any of it, leave the box empty and delete the Provenance section. -->

- [ ] Yes, and I checked the output mechanically

<details>
<summary>Provenance</summary>

<!-- If you ticked Yes: copy the Assisted-by and Agent-Effort trailers from your commits, one per line. Name any agent whose model is not on record as such, in words. Delete this section if no agent drafted any of it. -->

</details>

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
