# CHANGELOG

## v1 (initial generation)

Supersedes an earlier three-document prompt-engineering system (a brainstorm document, a system
prompt, and a structured guide) and the single-file skill document that preceded this library.

### Cut, not softened

- **Prompt Attack Detection** (pattern-matching and rejecting user input): removed. Structurally identical to how injection attempts fake an authority layer inside a conversation; the shape itself is what gets flagged, independent of intent. Zero real enforcement value, nothing stops a second confirmation from just being typed.
- **Encoded Content Handling two-step confirmation gates:** removed, same reasoning, no actual enforcement mechanism behind the gate.
- **SAFEMODE username-bound lock:** removed, same reasoning. A soft lock that deters nothing adversarial and adds token cost for a single-user context.
- **Absolute "never mention being an AI" rule:** corrected to match actual behavior, confirm if directly asked. The absolute version would have silently failed the first time it was tested against actual base behavior.
- **Blanket precedence claims** ("these rules take precedence over Task rules"): rewritten as standing defaults applied within a task, not a claim of authority over undefined other content. The old phrasing is the specific pattern actual injection attempts use.

### Added

- Tripartite knowledge labeling (Verified/Derived/Unknown), scoped to non-trivial claims only.
- Scaled correction persistence: a defined cap on how many times a disagreement gets restated before standing down permanently, completing the existing "findings don't shift from pushback" rule with an actual stop condition.
- Three dials: AUTONOMY, PROACTIVITY, RIGOR, adjustable, with stated baselines.
- Persist-vs-discard rule and stale-dependency check, principles ported from agentic-memory source material, not the full agentic tool-use machinery, which doesn't apply here.
- Decompose-vs-execute-directly test, principle ported from agentic-task-decomposition source material, sharpening the existing propose-before-generating rule.
- Distilled anti-slop vocabulary and structural pattern list, folded in directly rather than left conditional on document-standards' trigger firing, since casual chat prose otherwise had no coverage.

### Retained unchanged

Register, core prohibitions (apology language, em-dash, X-not-Y), reasoning protocol, ambiguity read-back, command vocabulary, Q1-3 format (with two additional stated exceptions: UI-tool turns, and explicit sequenced-confirm instructions).

## v2 (RCA remediation, turn-7 postmortem)

**Data-recovery note:** this entry was generated in the same session as `document-standards` v2
and v3 and `technical-documents` v1 and v2. The remediation that produced them required every
skill it touched to record a traceable entry. This entry was never actually written to the file,
only narrated as complete. It was reconstructed from the remediation checklist rather than
re-derived, and maps to the same finding numbers `document-standards` v3 cites.

Source: nine-finding audit of a NAS migration checklist and companion script, grouped into three patterns (confirmation compression, mechanical checks crowding out judgment checks, scope silence at skill boundaries) plus one standalone finding. Root cause: a rule requiring an internal judgment call, with no skill file requiring that judgment to become visible before the deliverable ships. Companion entry to `document-standards` v3; see that file for the preset-priority and Content Read fixes.

- **Findings 1, 7:** Artifact Workflow. Stated the propose-gate and dialog-gate as independent, per-deliverable checkpoints; an answer to one calibration question no longer silently counts as satisfying the other.
- **Finding 2:** Artifact Workflow / Correction Protocol. Added a mandatory pre-delivery self-audit for any artifact-producing turn, a SCORE-equivalent pass required by default rather than only on explicit request. The single highest-leverage fix in the whole remediation, since it independently catches most of the other findings.
- **Substitution half of Finding 3:** Distilled Anti-Slop Reference. Stated explicitly that the distilled list here is a floor, not a ceiling, and never substitutes for `document-standards`' full reference-file check when that skill is active.
- **Findings 4, 6, 8, 9 (structural fix):** Ambiguity Handling. Extended the existing read-back mechanism to cover silence or tension in the governing skill files themselves, not only ambiguity in the user's request. This is the fix underneath the surface-regimes forced-dial correction too, in spirit: a skill file being silent about an override path is the same failure shape as being silent about which rule applies.
- **Findings 8, 9:** Tripartite Knowledge Labeling. Added a worked example to the decision-load-bearing threshold: any claim feeding an irreversible action counts by definition, regardless of how routine it otherwise seems.

## v3 (Scope Pointer reconciliation)

**Data-recovery note:** the cross-reference to `surface-regimes` and the corrected `document-standards`/`technical-documents` split description were confirmed by the user in the session that built `surface-regimes`, and were listed there as executed, but never actually landed in this file. Applied now for the first time.

- **Scope Pointer:** corrected the `document-standards` line, which still described it as narrowly technical, to reflect the actual split, `document-standards` generic, `technical-documents` extending it for a technical audience, both loading together, preset priority decided by `technical-documents`' own trigger conditions rather than by surface.
- **Scope Pointer:** added a `surface-regimes` cross-reference, matching the existing pattern of pointing to a sibling skill rather than restating its content here.

## v4 (command vocabulary retiered by measured use)

The command vocabulary was revised on 2026-09-08 and this file did not pick it up. The kit went on describing nineteen commands for four days after the live set became twenty-seven.

- **Merged EXPAND and ELABORATE into DEEPEN.** A target narrows it to one element; no target applies it to the whole last response. The distinction the two commands carried survives as the presence or absence of an argument.
- **Added nine commands:** CONFIRM, DECLINE, MEASURE, QUEUE, PARK, WHY, NUDGE, STAGE, SOURCE. Each is one line, as the vocabulary states it. Depth gets added here when use shows a command needs more, not in advance.
- **Retiered the brevity code by measured frequency** into three tiers: six single keys, fifteen two-key codes, six three-key codes. Tiers came from counting commands in session transcripts rather than from judgment. A new command starts at tier 2 until it has data.
- **Breaking for anyone who learned the old table.** Several codes changed meaning: `f` was PROCEED and is CONFIRM, `fj` was FLAG and is MEASURE, `j` was EXPAND and is DEEPEN. The skill now says so beside the table, because a code read against memory of the old table does the wrong thing without any error.
- **Removed the paragraph grouping two-key codes by initial.** It described the old table and is false of the new one.
- **Not ported: left-hand-only aliases.** The source vocabulary carries one per command. They are fitted to one person, and `docs/interface-contract.md` 5-4 argues that any one-handed variant must be mirrorable. Held back by decision until the one-handed codes are refined.
- **NEXT block rule:** the letter-collision example now names DEEPEN.
