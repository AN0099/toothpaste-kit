# CHANGELOG

## v1 (initial generation)

Added in toothpaste-kit 0.2.0. The cheap reorientation: after a compaction, a handoff or a return to
a session, before any belief about the state is acted on.

**Why the split between observing and orienting.** Observing which branch a tree is on, what mail
arrived and what is dirty is mechanical, so a script does it and the model reads one output.
Noticing that two records disagree is judgement, so the model does that and no script tries. An
unstructured reorientation spends eight to twelve exploratory commands on the mechanical half. This
spends one.

**Why the tree's own tool and not a new one.** The skill delegates observation to whatever state
tool the adopting tree already has, and says to extend that tool rather than run an ad hoc command,
so the next run has the same coverage. It was first written around a second, near-identical tool
built without checking for the first, and the duplicate was deleted the same session.

**Why it may be model-invoked.** It chooses nothing. It reads and reports, and the boundary that
most needs it, a compaction, is an event only the agent notices. `daily-dashboard` sets
`disable-model-invocation` because it chooses a day's priority; this skill has no such choice to
make, and it still ends without starting any work.

**Why it writes nothing.** Anything worth keeping belongs to `session-log` or `session-close`, and a
finding recorded in two places goes stale in one of them.
