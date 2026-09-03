# CHANGELOG

## v2

Two internal contradictions removed. Both were found by running the skill against live document
tasks rather than by reading it, and in both cases the executing agent produced correct output but
reported that it had guessed, which is the failure worth preventing: a rule that forces a guess
produces inconsistent behavior across invocations without ever looking broken.

**The Content Read could not be one line.** The step specified a one-line read-back, while a later
paragraph in the same section required the stated dials to reflect a blend whenever the read names
two document types. A blend cannot be justified inside the line it modifies. The read is now one
line with an explicit second sentence for the case where dials depart from the preset or blend two
types. Keep both halves: shortening it back to a bare one-liner reinstates the contradiction, and
dropping the one-line constraint invites a paragraph of preamble before every document.

**The completion statement could not be a line.** The pre-flight checklist holds seven items and
asked for each to be marked done or skipped, in "a short completion line." Seven marks do not fit
in a line, so the instruction resolved in practice to a summary claim that the checks ran, which is
precisely what the statement exists to evidence rather than assert. It is now specified as a block,
one entry per item, with permission to cite an already-visible mechanical trace instead of
restating it. That last clause matches the equivalent carve-out in `working-preferences`'
pre-delivery self-audit, so the two files agree on what a mechanical check owes the reader.

**Neither this skill nor `technical-documents` said when to decline to generate.** Two of the three
eval tasks supplied almost no verifiable specifics, so the pre-flight ban on fake-precise numbers
correctly forced bracketed placeholders throughout, and both executing agents asked, unprompted,
whether they should have posed a clarifying question instead. The rules gave them no answer. A new
`# When Not to Generate Yet` section routes that case to `working-preferences`'
dialog-before-large-builds gate and requires the chosen path to be stated either way. The template
exception is deliberate: a document requested as a template has placeholders as its content, and
folding it into the general rule would gate the one case that should never be gated.

### Measurement

Against three document tasks (runbook, cover letter, hybrid announcement), the skill scored 24/24
on procedural and output assertions versus 10/24 unassisted. Cost was +51% tokens and +111% wall
time. Of the marginal token cost, roughly 22% is loading the skill and its reference files, about
4,600 tokens in total; the remaining 78% is the verification work the skill requires. The reference
files are cheap and worth keeping whole. Anyone tempted to trim them for cost should trim the
mandated passes instead, and should expect to lose the checks along with them.

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
