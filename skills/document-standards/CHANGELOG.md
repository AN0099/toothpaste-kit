# CHANGELOG

## v1 (initial generation)

### Inspiration log

- **Anti-slop skill** (banned words, phrases, structural patterns, scoring rubric): lifted near-verbatim where exact phrasing matters for pattern matching, vocabulary and phrase lists specifically. Skill framing, when-to-use logic, and category organization paraphrased and restructured.
- **Progressive-loading discipline** (gateway, category index, individual skill tiering, stated token budgets): structural pattern adopted, not the specific 20-plus-skill scale the source examples operate at. Two-tier structure chosen deliberately given current content volume; see Three-Tier Threshold Framework in SKILL.md for when to revisit.
- **Agentic workflow principles** (task decomposition, tool use, memory management): principles ported to `working-preferences` (persist-vs-discard, stale-dependency check, decompose-vs-execute test), not built as a sibling skill here or there. The full tool-orchestration machinery those sources describe doesn't apply to this context.
- **tasteskill** (three dials, brief-inference read-back, mechanical pre-flight checklist): structural pattern adopted directly, content redesigned for text-document authoring rather than frontend or visual design.

### Placement decisions

- FORMALITY, DENSITY, and AUDIENCE_LEVEL dials stay in this skill, not `working-preferences`, since they are content-conditioned (vary by document type) rather than behavioral.
- A distilled version of the banned-words and structural-patterns content was folded into `working-preferences` directly, to guarantee coverage even when a task doesn't register as technical-document authoring. The full versions stay here for the deeper rigor actual document work warrants.

### Three-tier threshold

Logged as a standing check in SKILL.md, not a one-time decision. Re-evaluate whenever `references/templates/` grows or reference-file token cost changes materially.

## v2 (generic split)

**Data-recovery note:** this entry was never written to this file during initial build; reconstructed from the session event log during the RCA-remediation pass, then lost a second time when this file was reconciled from a stale copy. Restored now from the same reconstructed source.

Rewritten from a technical-writing-scoped skill to a universal one, triggering for any standalone generated document rather than only runbooks, ADRs, and similar. The netadmin, DevOps, and DevSecOps audience framing and the technical document-type presets split out into a new sibling skill, `technical-documents`, which extends this file rather than duplicating it. Dial mechanism, Content Read step, pre-flight checklist, scoring rubric, and anti-slop references stayed here, applying unchanged to both generic and technical documents.

## v3 (RCA remediation, turn-7 postmortem)

Companion entry to `working-preferences` v2; see that file for the full root-cause statement.

- **Finding 4, and the preset-priority half of the cross-skill fix:** Dials, Document-Type Presets. Added an explicit priority rule: when a document could match a preset in both this file and `technical-documents`, the more specific `technical-documents` preset wins whenever its trigger conditions are met.
- **Finding 6:** When to Use. Replaced the open-ended document-type example list with a definitional test: any generated artifact meant to be read, run, or referenced outside the chat turn, explicitly including code and scripts.
- **Finding 2, and the disclosure half of Finding 3:** Pre-flight Checklist. Added a required completion line at delivery, each item marked done or explicitly marked skipped with a reason, rather than leaving execution to be inferred from what's visible in the response.
- **Substitution half of Finding 3:** Content Read. Stated that `working-preferences`' distilled anti-slop list is a floor and this file's full reference check is the required ceiling; the distilled list never substitutes for it here.
- **Finding 5:** Content Read. Added an internal-consistency requirement: if the descriptive half of the one-line read names more than one document type or register, the stated dial values must reflect an actual blend or an explicit choice between them.
