# CHANGELOG

## v1 (initial generation)

Built alongside `skill-creation`. That skill governs the shape of a new skill file; this one
governs whether a recurring need is worth a skill at all, and how an existing skill gets found.

### Sources

- The Worthiness Test (frequency, reusability, complexity, stability) adapts a scoring approach
  from external skill-planning material. The source used a numeric threshold calibrated for a
  library of twenty-plus skills. That was simplified here to a low, medium, or high rating,
  because a cutoff tuned for a library that size is not meaningful for a family of seven.
- An earlier proposal folded this test into `document-standards`' Three-Tier Threshold Framework
  rather than giving it a skill of its own. This build gives it a dedicated skill instead. The
  difference is deliberate and is recorded here so a later reader does not mistake it for an
  oversight.
- The locating-skills section deliberately does not propose a gateway or index file at the current
  family size. That option was weighed and rejected: it costs a hop on every lookup and a file that
  must be updated on every addition. The revisit trigger is three or more skills in the meta
  category, and it lives in `SKILL.md` as well as here, so it is not lost when this entry stops
  being read.

### Open item at time of writing

Sibling cross-references, meaning the existing skills naming `skill-discovery` in their own Scope
Pointer sections, were left for a separate change rather than applied here.
