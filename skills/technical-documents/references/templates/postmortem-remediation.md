# Template: Incident Postmortem with Root-Cause-Driven Remediation Checklist

Generalized from the RCA-remediation document produced for the working-preferences/document-standards/technical-documents skill system, stripped of that system's specific content.

## When to Use

An incident, defect audit, or self-audit surfaced multiple findings, and the findings cluster into a small number of named patterns rather than standing alone. Use this shape when the goal is not just listing what went wrong, but tracing the findings to one shared mechanism and turning that mechanism into a numbered, file-targeted remediation plan.

## When Not to Use

A single-cause incident with one fix doesn't need this structure; state the cause and the fix directly. If the findings don't share a mechanism, forcing a unifying root-cause section produces a false pattern; report them as an unrelated list instead.

## Dial-Compatibility Range

FORMALITY 5-7, DENSITY 4-6, AUDIENCE_LEVEL 5-7. Matches this skill's Incident Postmortem preset. Push DENSITY toward 6-7 for an audience that will act on the checklist directly; pull toward 4-5 if the same document also needs to explain the incident to a reader unfamiliar with the system.

## Structure Sketch

1. **Restating the source finding-set's own grouping.** If the originating audit already grouped findings into patterns, restate that grouping and credit it as correct rather than re-deriving it. Note any finding that doesn't fit cleanly into the existing groups.
2. **The deeper, unifying root cause.** State the one mechanism that explains multiple named patterns at once. Show the mechanism operating in each pattern specifically, not just asserted once and left abstract. Name any existing mechanism in the system that was already positioned to catch this and explain why it didn't fire (manual/opt-in rather than mandatory, no forcing function, wrong scope).
3. **Remediation checklist.** One numbered step per finding or finding-cluster. Each step names its target file or component explicitly and states the amendment in one or two sentences, not a full rewrite inline. Close each step with which finding number(s) it resolves.
4. **Closing note.** State plainly that the checklist is a proposed plan, not yet applied, if that's the actual status. Name what applying it would concretely require (which files, whose sign-off). If the postmortem itself is a candidate for reuse as a template, say so and name what would need stripping to generalize it.

## Common Anti-Patterns

- Restating all nine (or however many) findings as flat prose without the pattern grouping. The grouping is the deliverable; the raw list is what the reader already has.
- Root cause stated once at the top and never connected back to each individual finding, leaving the reader to do that mapping themselves.
- Remediation steps that describe the intended fix in the abstract rather than naming the specific target file or section.
- Treating "proposed, not yet applied" as understood from context instead of stating it. A checklist that reads as already-shipped invites the reader to assume coverage that doesn't exist yet.
