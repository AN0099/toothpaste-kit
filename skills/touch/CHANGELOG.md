# CHANGELOG

## v1 (initial generation)

Added in toothpaste-kit 0.2.0, with `jot` and the shared rules in `docs/partial-captures.md`. The
agent-callable update of one fact in a standing file, made right after the work it records.

**Why a narrow list of allowed edits.** One task status, one appended flag group, or one manifest
line. Each is an event that just happened. Moving a thread to the resolved log, deleting a flag or
rewriting a line is judgement over the whole record, and it stays with `session-close`. The operating
handoff document is excluded because its roster and conventions change by decision, not by event.

**Why only this session's facts.** A touch records what just happened and does not correct what an
earlier session wrote. A wrong line found in a standing file becomes a finding in the open-threads
log, and `session-close` fixes it.

**Why a second party before complete.** A task is not marked complete on the claimant's word alone;
the note names who verified it. This is the kit's standing rule that a completion claim needs a
party other than the one making it.

**Why the ledger line and the anchored edit.** Every touch appends a `[touch]` line to the day's
capture file, so each standing-file edit made outside a close has a dated trace in one place, and a
stack of touches is never taken as a close. Each edit asserts that its anchor occurs exactly once, so
a missing or doubled anchor fails loudly instead of writing in the wrong place.
