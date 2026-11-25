---
name: technical-documents
description: Document-type presets and vocabulary for technical documents (runbooks, postmortems, ADRs, READMEs, handoffs, SOPs) for network admin and DevOps readers. Extends document-standards; does not redefine its dials, checklist or anti-slop references.
---

# When to Use

Layers on top of `document-standards` specifically for: runbooks, incident postmortems, ADRs, README files (technical or project-specific), on-call handoff notes, change-management docs, SOPs, and similar standalone technical documents aimed at readers who are senior network admins, DevOps engineers, or DevSecOps engineers, often people delegating work to juniors or evaluating documentation quality.

This skill assumes `document-standards` is already active. It adds document-type presets and audience framing on top of that base. It does not restate the FORMALITY/DENSITY/AUDIENCE_LEVEL dial mechanism, the Content Read step, the pre-flight checklist, the scoring rubric, or the anti-slop references, all of which live in `document-standards` and apply here unchanged.

**Preset priority:** when a document could plausibly match a preset in both this file and `document-standards`, this file's preset wins whenever its trigger conditions (audience, document type) are met, since it represents the more specific match. `document-standards`' own presets are the fallback for everything else.

Making a new skill is covered by `skill-creation`, and deciding whether a need justifies one, or locating an existing skill, by `skill-discovery`.

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

# Headers and Opening

Postmortems, ADRs, change-management docs and handoff notes are often read only as far as the opening paragraph, plus a skim of the headers. Write both for that reader.

**Open with the bottom line.** The first paragraph states the outcome: what failed and what fixed it, what was decided, what changes and when, what the next shift must act on. Context and history come after it. A reader who stops at the end of that paragraph has enough to act.

**Headers state findings.** A reader who sees only the headers should come away with the document's main points. A topic label names a bin; a signpost header says what is in it. Illustrative pairs:

| Signpost | Topic label |
|---|---|
| "Failover took 14 minutes because the health check timed out" | "Failover behavior" |
| "Option B keeps the existing VLAN plan" | "Option analysis" |
| "BGP flaps traced to an MTU mismatch on the new uplink" | "Root cause" |

Headers a document type fixes for findability keep their fixed names: a postmortem's Timeline and Action Items, an ADR's Status, Context, Decision and Consequences. The signpost rule covers the headers the author chooses. Runbooks and SOPs are procedures, so their headers name the action ("Drain the node", "Rotate the key"), following `document-standards`' rule on step labels.

# Templates

`references/templates/`: technical document-type templates (runbook, ADR, postmortem, and so on), populated iteratively as real documents get produced. Empty at initial build. Apply `document-standards`' Three-Tier Threshold Framework independently once this folder grows toward the same limits.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
