---
name: skill-creation
description: How to add a new skill to this system, once the decision to build one is already made. Naming convention, required section shape, a sizing target and split ceiling, and the integration and pre-publish checklists a new skill runs through before it counts as live. Does not decide whether a recurring need is worth a skill in the first place (see skill-discovery) or check a skill file's prose against content-quality standards (see document-standards, which still governs SKILL.md and CHANGELOG.md as generated documents).
---

# When to Use

Any time a new skill is being added to this system, an existing skill is being split into more than one file, or a skill is being renamed. Assumes the worthiness question, is this actually recurring, reusable, complex, and stable enough to earn a skill, is already resolved. That test lives in `skill-discovery`, not here.

# Naming Convention

- Lowercase, hyphen-separated, noun phrase naming the skill's domain, not a verb phrase describing an action: `document-standards`, `working-preferences`, `skill-discovery`. Not `write-documents` or `discover-skills`.
- Two words, occasionally three, matching the existing family (`working-preferences`, `document-standards`, `technical-documents`, `surface-regimes`, `skill-creation`, `skill-discovery`). A name needing more than three words signals the skill's scope is too wide. Narrow it or split it before naming it.
- No version number, date, or status word in the name itself. No `document-standards-v2`, no `skill-creation-draft`. Versioning lives in the skill's own `CHANGELOG.md`. The name describes the domain, which shouldn't change with revisions.
- Check for collision and near-collision before finalizing, not only exact duplicates. `skill-creation` and `skill-create` triggering on similar phrasing is as much a problem as an exact match.

# Required Sections

Every `SKILL.md` in this system follows the same three-position skeleton. Only the middle position varies by skill.

1. **Frontmatter.** `name` and `description` only, nothing else. `description` states what the skill covers, when to use it, and what it explicitly does not cover, with a pointer to whichever sibling skill does, since that boundary line is what triggering accuracy depends on.
2. **Opening scope section.** First heading after frontmatter, states when this skill applies. Named `# When to Use` for skills that trigger conditionally on document type or task (`document-standards`, `technical-documents`, this skill). Named for the skill's actual subject when the skill is closer to a standing behavioral default (`working-preferences` opens with `# Role & Register` instead, since it's near-always active rather than conditionally triggered). Either way, this section is required and comes first.
3. **Body sections.** As many as the skill's content actually needs, in whatever order reads best. No fixed universal middle, because the live skills don't share one. A behavioral-defaults skill and a document-preset skill genuinely don't have the same shape. What's required is internal to each skill, not shared across the family.
4. **Closing cross-reference section.** Last heading, named `# Scope Pointer` or `# References` in the existing skills. States what's explicitly out of scope here and which sibling skill covers it. This is what keeps the family's boundaries legible without a parent file.

A `CHANGELOG.md` sibling to `SKILL.md` is required, not optional, and not embedded inside `SKILL.md` itself. See Pre-Publish Checklist.

# Sizing Target and Split Ceiling

Target for `SKILL.md` itself: under roughly 150 lines. The largest live skill, `working-preferences`, runs about 140 lines and covers standing register, prohibitions, six other sections, and a full command vocabulary. That's close to the practical ceiling for a file someone can hold in working memory while editing it.

Ceiling: 250 lines, or the point where a single body section is doing enough independent work that it reads like a second skill wearing this one's frontmatter. Past either trigger, split: move reference material (word lists, templates, detailed tables) into `references/*.md` and `references/templates/`, keep `SKILL.md` as the entry point with pointers. Same two-tier structure `document-standards` already uses.

Don't re-derive a separate threshold for when `references/` itself needs to go three-tier (gateway plus category index plus individual files). `document-standards`' own Three-Tier Threshold Framework already owns that question and states it as a standing check, not a one-time decision. Apply it to this skill's reference material too rather than building a second version of the same rule.

# Integration Checklist

Files to check, not necessarily all to change, every time a skill is added:

- `skills/<name>/SKILL.md` and `skills/<name>/CHANGELOG.md`: always, the two required files for any skill.
- `skills/<name>/references/`: only if the skill actually has reference material at build time. Don't scaffold an empty folder for content that doesn't exist yet. The templates convention this system already uses (empty at initial build, populated as real instances get produced) applies to whole reference files too, not only the `templates/` subfolder.
- Repo-level `README.md`: add a row for the new skill.
- External source provenance, if the new skill draws on outside material: record it in the skill's own `CHANGELOG.md` under a `### Sources` heading, naming what was drawn from where, what was adopted, and what was deliberately left out. This repo keeps that provenance per skill rather than in a single index file.
- Sibling skills' own cross-reference sections: any existing skill whose `# Scope Pointer` or `# References` section states a boundary the new skill now sits on the other side of needs that line updated to name the new skill. Otherwise the boundary claim goes stale the moment the new skill ships. This is an edit to a file this skill doesn't own. Flag it for confirmation rather than applying it unilaterally, the same handling `surface-regimes/CHANGELOG.md` v1 used for the identical situation.
- Repo-level `CHANGELOG.md`: add an entry for the new skill's addition, separate from the entry inside the skill's own changelog. The repo-level file records that the skill set changed; the skill-level file records why that skill is shaped the way it is.

# Pre-Publish Checklist

Structural validity, run before a skill counts as live. Separate from content-quality review, which is `document-standards`' job, since `SKILL.md` and `CHANGELOG.md` are themselves generated documents.

- Frontmatter present, valid YAML, exactly two keys (`name`, `description`), no trailing content between the two `---` fences beyond those keys.
- `name` in frontmatter matches the folder name exactly.
- Required sections present: opening scope section first, closing cross-reference section last (see Required Sections above).
- No duplicate or near-duplicate skill name anywhere in the live system, checked by listing, not by memory of what's already there.
- `CHANGELOG.md` exists as a sibling file, has at least a `## v1` entry, and is not embedded inside `SKILL.md`.
- Every sibling skill named in this skill's closing cross-reference section actually exists live. Every sibling skill that should now reference this one back has been flagged per the Integration Checklist above, not silently skipped.
- File written and verified on disk, not only shown in a chat transcript. This project has a documented history of the second being mistaken for the first. Treat that history as a standing reason to check, not a one-time note.

# Scope Pointer

Whether a recurring need is worth turning into a skill at all, and how an existing skill gets located and triggered once built, are `skill-discovery`'s job, not this one. Content-quality standards for the prose inside `SKILL.md` and `CHANGELOG.md` (register, banned vocabulary, structural patterns) are `document-standards`' job, applied here like any other generated document.
