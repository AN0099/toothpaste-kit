# CHANGELOG

## v1 (initial generation)

Added in toothpaste-kit 0.2.0, with `touch` and the shared rules in `docs/partial-captures.md`. The
agent-callable capture of reasoning at a clean boundary, between the person-run procedures.

**Why a partial capture exists.** `session-log` and `session-close` are run by a person because
they are expensive and because each one decides or certifies something. Between them, reasoning from
a finished stretch can still be lost to compaction. A jot costs about one reply and keeps the part
most likely to be lost.

**Why only three of `session-log`'s questions.** Decisions, corrections and findings are kept. Open
questions are left out because they belong in the flag register, where `touch` can put them. The
where-the-work-stands paragraph is left out because it is only worth writing when a restart is
near, which is `session-log`'s moment.

**Why the marker and the limits.** Every entry is headed `[jot]` so a stack of partials is never
taken as proof that `session-log` ran. Fifteen lines at most, no reading files to confirm, and no
edits beyond the append keep it small enough that calling it does not become a second session-log.
Near compaction the skill prompts the person to run `session-log` instead.
