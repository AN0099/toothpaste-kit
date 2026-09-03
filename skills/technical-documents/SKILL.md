---
name: technical-documents
description: Document-type presets and audience-specific vocabulary for technical documents (runbooks, incident postmortems, ADRs, README files, on-call handoff notes, change-management docs, SOPs) aimed at senior network admin, DevOps, and DevSecOps readers. Extends document-standards; does not redefine its dials, checklist, or anti-slop references.
---

# When to Use

Layers on top of `document-standards` specifically for: runbooks, incident postmortems, ADRs, README files (technical or project-specific), on-call handoff notes, change-management docs, SOPs, and similar standalone technical documents aimed at readers who are senior network admins, DevOps engineers, or DevSecOps engineers, often people delegating work to juniors or evaluating documentation quality.

This skill assumes `document-standards` is already active. It adds document-type presets and audience framing on top of that base. It does not restate the FORMALITY/DENSITY/AUDIENCE_LEVEL dial mechanism, the Content Read step, the pre-flight checklist, the scoring rubric, or the anti-slop references, all of which live in `document-standards` and apply here unchanged.

**Preset priority:** when a document could plausibly match a preset in both this file and `document-standards`, this file's preset wins whenever its trigger conditions (audience, document type) are met, since it represents the more specific match. `document-standards`' own presets are the fallback for everything else.

# Document-Type Presets

| Type | FORMALITY | DENSITY | AUDIENCE_LEVEL |
|---|---|---|---|
| Runbook | 4 | 7 | 7 |
| Incident postmortem | 6 | 5 | 6 |
| ADR | 7 | 4 | 6 |
| Technical README | 4 | 5 | 4 |
| On-call handoff note | 3 | 8 | 8 |
| Change-management doc | 7 | 5 | 5 |
| SOP | 6 | 6 | 5 |

# Vibe-Word to Dial Mapping (Technical)

| Signal | FORMALITY | DENSITY | AUDIENCE_LEVEL |
|---|---|---|---|
| "runbook" / "on-call doc" | 4-5 | 7-8 | 6-8 |
| "postmortem" / "incident report" | 6-7 | 5-6 | 5-7 |
| "ADR" / "design doc" | 6-8 | 4-5 | 5-7 |
| "audit doc" / "compliance" | 8-9 | 5-6 | 5-6 |

# Templates

`references/templates/`: technical document-type templates (runbook, ADR, postmortem, and so on), populated iteratively as real documents get produced. Empty at initial build. Apply `document-standards`' Three-Tier Threshold Framework independently once this folder grows toward the same limits.
