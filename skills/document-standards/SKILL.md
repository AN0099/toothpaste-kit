---
name: document-standards
description: Universal writing and quality standards for any standalone document Claude generates, reports, essays, letters, resumes, README files, technical docs, and everything else. Covers formality/density/audience dials, a Content Read step, a pre-flight checklist, and a full anti-slop reference. Does not cover conversational chat responses (see working-preferences) or document-type presets specific to network admin and DevOps audiences (see technical-documents).
---

# When to Use

Test, not a list: any generated artifact meant to be read, run, or referenced outside the chat turn itself gets these standards applied. This explicitly includes code and script files, not only prose documents. Reports, essays, letters, resumes, cover letters, blog posts, README files, runbooks, and generated scripts all pass this test.

Out of scope: conversational chat responses, covered by `working-preferences`' distilled anti-slop reference. Document-type-specific presets and vocabulary for network admin, DevOps, and DevSecOps audiences are covered by the `technical-documents` skill, which extends this one rather than replacing it.

# Dials

**FORMALITY (1-10):** 1 is casual and conversational, 10 is formal or ceremonial.
**DENSITY (1-10):** 1 is explanatory, spelled-out prose, 10 is terse reference material.
**AUDIENCE_LEVEL (1-10):** 1 is written for a reader who needs the why, 10 is written for a reader who only needs the what.

## Vibe-Word to Dial Mapping

| Signal | FORMALITY | DENSITY | AUDIENCE_LEVEL |
|---|---|---|---|
| "quick reference" / "cheat sheet" | 2-3 | 8-9 | 7-9 |
| "onboarding guide" / "explainer" | 3-4 | 2-3 | 1-3 |
| "formal report" / "proposal" | 7-8 | 5-6 | 5-6 |
| "casual note" / "internal memo" | 2-3 | 4-5 | 4-6 |
| "creative or narrative piece" | varies by voice | 2-4 | varies |

## Document-Type Presets (General)

| Type | FORMALITY | DENSITY | AUDIENCE_LEVEL |
|---|---|---|---|
| Resume / cover letter | 6 | 6 | 5 |
| Formal report | 7 | 5 | 5 |
| Blog post / article | 4 | 4 | 3 |
| Internal memo | 3 | 6 | 6 |
| General README | 4 | 5 | 4 |

Technical document types (runbooks, ADRs, incident postmortems, on-call handoff notes, change-management docs, SOPs) and their audience-specific presets live in `technical-documents`, which layers on top of these dials rather than duplicating them.

**Preset priority:** when a document could plausibly match a preset in both this file and `technical-documents`, the `technical-documents` preset wins whenever its trigger conditions (audience, document type) are met, since it represents the more specific match. This file's own presets are the fallback for everything else.

# Content Read

Before generating, state a one-line read: "Reading this as: [document type] for [audience], dials at [F/D/A]." This is a read-back, not a question; proceed unless corrected.

This is the document-specific instantiation of `working-preferences`' Ambiguity Handling principle. Document type and target audience are the variables that actually vary per task, so the dial-setting step lives here rather than in the universal file.

`working-preferences`' distilled anti-slop list is a floor that applies everywhere. The full reference-file check below is the required ceiling for any document that triggers this skill; the distilled list never substitutes for it here.

If the descriptive half of the one-line read names more than one document type or register, the stated dial values must reflect an actual blend or an explicit, stated choice between them, not the values for only one of the named types. Check the two halves against each other before proceeding.

# Pre-flight Checklist

Run before shipping any document:

- Zero em-dashes, zero en-dash-as-separator. Grep-verify, don't eyeball it.
- No banned vocabulary or phrases from `references/banned-words.md`.
- No structural patterns from `references/structural-patterns.md`.
- Fake-precise numbers only if real or explicitly labeled as example.
- One copy register maintained throughout; no mixing technical, editorial, and marketing tone in the same document.
- Every claim traces to something real, stated, or explicitly marked as illustrative.
- Scoring rubric run (below), threshold met.

State a short completion line at delivery: each item above marked done, or explicitly marked skipped with a reason. Don't leave checklist execution to be inferred from what happens to be visible in the response.

# Scoring Rubric

Rate 1-10 on each dimension:

| Dimension | Question |
|---|---|
| Directness | Statements or announcements? |
| Rhythm | Varied or metronomic? |
| Trust | Respects reader intelligence? |
| Authenticity | Sounds human? |
| Density | Anything cuttable? |

Below 35/50: revise before shipping.

# Three-Tier Threshold Framework

Switch from the current two-tier structure (`SKILL.md` plus flat `references/`) to a three-tier structure (gateway plus category index plus individual skill files) when any of the following trip:

- Template count in `references/templates/` exceeds 8 files.
- Combined reference-file token cost (banned-words plus structural-patterns plus examples loaded together) exceeds roughly 8K tokens.
- A second, genuinely distinct dial system emerges that this file's FORMALITY/DENSITY/AUDIENCE_LEVEL structure doesn't serve well.

This is a standing check, not a one-time decision. Re-evaluate whenever `references/templates/` grows. `technical-documents` has its own templates folder and should apply this same threshold independently.

# References

- `references/banned-words.md`: full categorized vocabulary and phrase lists, lifted near-verbatim from source material where exact phrasing matters for pattern matching.
- `references/structural-patterns.md`: full pattern catalog with detection signals.
- `references/examples.md`: before/after transformation pairs.
- `references/templates/`: general document-type templates, populated iteratively as real documents get produced. Empty at initial build.
