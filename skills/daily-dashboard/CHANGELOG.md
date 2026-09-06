# CHANGELOG

## v1 (initial)

Start-of-session orientation. Reads the standing files, verifies carry-over work
against the working trees, and presents state, ranked todos, roadmap, and the
decisions waiting on a person.

It is the mirror of `session-close`. That skill exists because anything living
only in a session is gone when the session ends; this one exists because writing
the residue down accomplishes nothing if the next session opens by reciting the
previous one's closing claim instead of checking the tree. The pair is one loop,
and only one half of it was built.

Four things are deliberate.

**Phase 2 treats the last session's report as a claim.** The instance this skill
was reconstructed from ran a precondition table against the working tree and found
two defects inside the documents it was quoting: a queue task with no `status`
field, and a manifest entry naming a file that was not on disk under that name.
Neither was what the session set out to look for. Nothing else in the system reads
all the standing files together, so the dashboard is the only place those surface,
which is why recording them is required rather than incidental.

**The todo ranking rule is fixed, and the skill has to state it.** Rank by whether
something is currently unprotected or falsely reporting clean, not by effort or
age. The reasoning is the same one behind `session-close` phase 3: a check that
reports clean because it was never wired up is worse than an absent check, because
it consumes the attention that would have gone to the gap. A ranking the human
cannot see is a ranking the human cannot overrule, so it goes in the output.

**Phase 0 forbids writing the dashboard to disk.** The obvious next step from a
good morning summary is a daily note file, and that would duplicate every standing
file it draws from. This tree also has a standing rule against generating a
document without explicit permission. A request for a dashboard is not that
permission.

**Phase 4 stops.** The procedure ends on numbered questions and takes no action on
them. A dashboard that begins the top-ranked item has picked the day's priority on
the human's behalf using a ranking it invented in the previous section.
`disable-model-invocation` is set for the matching reason, and the same one
`session-close` gives: an agent should not decide that the day has started any
more than it should decide the session is over.

**Alternative considered and rejected:** folding this into `session-close` as a
reopening phase, so one skill covered both ends of the loop. Rejected because the
two run at different times, under different information, and with opposite
failure modes. `session-close` fails by not looking hard enough at the session;
this fails by trusting what the session wrote. One file cannot hold both warnings
without each diluting the other, and `skill-creation`'s split ceiling would be
reached on the merged file anyway.

### Sources

Reconstructed from a single prior instance in this system's own session history,
2026-09-04, where the procedure was typed as an ad hoc prompt: "This is the start
of a new work day ... overview project-state & immediate todo's and roadmap items,
like a dashboard for the workday." The four-section shape, the todo ranking rule,
and the closing question block are taken from the response that prompt produced.
Adopted from it: the precondition table, the ranked todo list, the separation of
roadmap from decisions waiting on the human, and the closing questions. Added on
top of it: phase 0, the requirement to walk every working tree rather than the
remembered one, and the instruction to record standing-file defects found in
passing, which that instance did well but by accident rather than by procedure.
