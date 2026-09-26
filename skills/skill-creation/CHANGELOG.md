# CHANGELOG

## v1 (initial generation)

Built alongside `skill-discovery` and the decision that skills are flat siblings with no parent
index file. The two skills split the work: this one governs the shape of a new skill file,
`skill-discovery` governs whether to build it at all.

**Why flat siblings.** A parent index file was considered and rejected at the current family size.
It adds a hop for every lookup and a file that must be updated on every addition, in exchange for
grouping that seven skills do not yet need. The revisit trigger is three or more skills in the
meta category, which is recorded in `skill-discovery/SKILL.md` rather than only in this entry, so
it survives this file falling out of rotation.

### Sources

- The required-section skeleton (frontmatter, opening scope section, flexible body, closing
  cross-reference section) came from inspecting the live skills directly. A common meta-skill
  pattern in circulation prescribes a fixed six-section shape (When to Use, Core Concepts,
  Patterns, Quick Reference, Anti-Patterns, Related Skills). That was evaluated and not adopted,
  because no skill actually in this system matches it.
- The sizing target and split ceiling use `working-preferences`' line count as the practical upper
  bound, rather than a number picked for its own sake.
- The three-tier reference-material threshold is deliberately not restated here. It points at
  `document-standards`' Three-Tier Threshold Framework instead, per the standing rule that a
  mechanic lives in one file and is referenced from the others.

### Build-environment note

This build ran against an uploaded copy of the live skill set rather than a direct connection to
it. An earlier draft in the same session compared that copy against an unrelated account's local
skill directory and reported a corrupted `technical-documents` and a missing `surface-regimes` as
current problems. Both findings were real but about the wrong target. The uploaded copy was clean.
Corrected before this file was finalized, and the Integration Checklist in `SKILL.md` reflects the
correction.

The general lesson is recorded because it recurs: a diff is only as meaningful as the confidence
that both sides are what you think they are.

### Open item at time of writing

Sibling cross-references, meaning the existing skills naming `skill-creation` and `skill-discovery`
in their own Scope Pointer sections, were left for a separate change rather than applied here.

## v2 (single-verb exception for boundary procedures)

The naming convention asked for a noun phrase of two or three words. `orient`, `jot` and `touch`,
added in 0.2.0, are each a single verb, and a review before that release found the conflict. The
convention now carries an exception rather than the three skills being renamed.

**Why an exception rather than a rename.** The noun-phrase rule names a domain, which suits a skill
that governs behaviour continuously. These three are procedures an agent runs on its own at one
moment, and for them the name is the instruction. A rename after release would also count as a
breaking change under `docs/releasing.md`, so the choice had to be made before 0.2.0 was tagged.
The exception is narrow: a skill that governs a domain still takes a noun phrase.
