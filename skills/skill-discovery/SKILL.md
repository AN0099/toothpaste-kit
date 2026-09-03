---
name: skill-discovery
description: How a recurring need gets recognized as worth turning into a skill, and how an existing skill in this system gets located once built. Covers the worthiness test and the discovery process itself, not what happens inside a skill once it's triggered (each skill's own frontmatter description handles that) or how to structure a new skill file (see skill-creation).
---

# When to Use

Two situations: deciding whether something that just came up repeatedly should become a skill instead of being handled once and forgotten, and figuring out which existing skill, if any, already covers a task before assuming none does or building a duplicate.

# Worthiness Test

Score a candidate on four factors before building.

| Factor | Question |
|---|---|
| Frequency | Has this actually come up more than once, or is this the first time? |
| Reusability | Would the same content serve a different task later, or is this specific to what's happening right now? |
| Complexity | Is there enough structure here (rules, dials, checklists) to be worth formalizing, or is it a single fact? |
| Stability | Is this settled enough to write down, or still actively changing session to session? |

Rate each low, medium, or high. Don't build a numeric scale for a six-skill family, that's precision the current scale doesn't need. A candidate scoring low on three or more factors is answered once and left in the conversation. A candidate scoring medium or above on at least three factors is a real skill candidate, run it through `skill-creation`.

Low frequency alone doesn't disqualify a candidate that's high on the other three. A rule this stable and this complex is worth capturing the first time it's articulated cleanly, waiting for repetition just means re-deriving it from scratch next time. Low stability is the harder disqualifier: a skill built on a rule still in flux gets stale before it's used, and a stale skill actively misleads in a way an unanswered question doesn't.

This is the missing piece under `document-standards`' Three-Tier Threshold Framework. That framework decides when a skill's reference material needs more structure. This decides whether a recurring need needs a skill at all. Different question, same standing-check spirit: re-evaluate per candidate rather than deciding once and reusing the verdict.

# Locating an Existing Skill

Given the family's current size, six skills, discovery works by reading frontmatter `description` fields directly rather than through a dedicated routing file. Each skill's `description` already states what it covers and what it explicitly doesn't, with a pointer to whichever sibling does instead. The descriptions collectively function as the index.

Two failure modes worth checking for before concluding no skill covers something:

- **Boundary drift.** A skill's stated scope in its `description` no longer matches what it actually does, because the file was edited without the description being updated to match. Check the description against the actual sections, not just the description in isolation.
- **Split coverage.** The need spans two skills' stated boundaries (a technical document authored under a specific surface regime touches `technical-documents`, `document-standards`, and `surface-regimes` at once). This isn't a gap, it's normal for skills that layer rather than replace each other. Confirm the layering is intentional (each skill's own trigger conditions, not a manual choice) rather than picking one skill and ignoring the others.

# When Description-Matching Stops Being Enough

Reading six descriptions to find the right one doesn't need a dedicated gateway file. That overhead only starts paying for itself once there are enough skills in one category that scanning descriptions individually gets slow. One source project in this project's own research used four `discover-*` gateway files for eight downstream skills, roughly two skills per category. If this system's meta-skill category (this file, `skill-creation`, and whatever ends up adjacent to them) grows to three or more, revisit whether a dedicated `discover-skill-standards` gateway earns its place, rather than assuming the current description-matching approach scales indefinitely.

# Scope Pointer

What a skill does once it's found and triggered is that skill's own content, not repeated here. How to structure a new skill file, once the Worthiness Test above says build one, is `skill-creation`'s job.
