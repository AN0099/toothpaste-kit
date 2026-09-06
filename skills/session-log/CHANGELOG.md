# CHANGELOG

## v1 (initial)

Mid-session capture for the compaction boundary. Writes the reasoning from the
recent stretch to one append-only provenance file, in a single pass, and stops.

`session-close` already covered the end of a session. What nothing covered was the
middle, where context gets compacted several times a day and reasoning disappears
without anything going wrong visibly. The obvious answer was to run `session-close`
more often, and that answer does not survive contact with its price: it sweeps a
whole session by category, updates six standing files, and runs mechanical checks
with a verification step on each. Correct once. Absurd three times in an afternoon,
and a procedure too expensive to run when it is needed is one that does not run.

Four things are deliberate.

**The skill is aimed at one loss, not at summarizing.** The tree survives
compaction; files written this session are still on disk and a later session can
open them. What does not survive is why they look like that. So the operative rule
is that a sentence recoverable by reading the file it describes does not belong in
the log. That rule is most of the cost difference between this skill and
`session-close`, and it is stated as a rule rather than as advice because
"summarize what happened" reliably produces a restatement of the diff.

**It says out loud that it does not discharge `session-close`.** A capture file on
disk looks like a closed session to whoever finds it next, and the cheap procedure
sitting next to the expensive one is exactly the setup where the cheap one quietly
becomes the only one that ever runs. The skill has to deny that in its own text,
because the file it produces cannot.

**The exclusion list is explicit.** Do not touch the standing files, do not run the
dash sweep, do not verify a completion claim, do not re-read files to confirm what
you are writing. Each of those is a real temptation and each one individually looks
like an improvement. Together they are how this skill becomes a second copy of
`session-close` within a few revisions, at which point there is again no cheap
option and the compaction boundary is uncovered again.

**Five questions rather than four.** The first run of this skill, against the session that built
it, produced two items that fit none of the original four: that past sessions are readable on disk
as transcripts, and that slash commands are parsed only at the start of a message. Both were
established by evidence during the work, neither was a decision or a correction, and neither could
have been recovered by reading anything in the store. That is a distinct category and it was
missing. It is also the category most likely to be dropped, because findings of this kind arrive as
a side effect of doing something else and do not look like output at the time.

**Appending rather than rewriting.** A later entry contradicting an earlier one is a
correction, and both halves are worth keeping. Rewriting the file to stay tidy
destroys the more valuable of the two.

**`disable-model-invocation` stays set, and the tension it creates is real.** The
argument against setting it is specific to this skill: the model usually knows
compaction is approaching and the human usually does not, so the party best placed
to trigger the capture is the one forbidden from doing it. That argument is sound
and it still loses, for two reasons.

The first is that skill triggering is fuzzy. An agent-invocable skill fires on a
frontmatter description matching what the agent thinks it is doing, and this one's
description is dense with words that appear constantly in ordinary work: session,
log, capture, context, compact. A write procedure with a hair trigger produces
files nobody asked for, and the cheap procedure that fires on its own is also the
one that starts standing in for `session-close` without anyone deciding that.

The second is that model invocation is the wrong instrument for the problem
anyway. The need is not judgment about whether a capture is warranted; it is
knowing that compaction is imminent, which is a fact about the harness rather than
about the work. A hook on a pre-compaction event is the mechanically correct
carrier: it fires deterministically, needs no model judgment, and leaves the
trigger with the human by surfacing a prompt rather than writing a file. That is
the same shape as the tier read notices already in `hooks/`, which warn rather than
act.

Recorded as a build item rather than an implementation, because whether this
harness exposes a pre-compaction hook event was not verified when this was written,
and `system/hookify-notes.md` establishes that guessing at the rule engine's
behavior produces silently broken rules. Check before building.
