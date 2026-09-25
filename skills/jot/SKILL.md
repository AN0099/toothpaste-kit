---
name: jot
description: Agent-callable micro-capture at a clean boundary. Appends one short, marked entry of decisions, corrections and findings from the stretch just finished to the day's capture file. Costs about one reply. Does not replace or satisfy session-log or session-close.
---

# When to Use

Right after a commit, a dispatch, or a closed decision, when something from the stretch just
finished would be lost to compaction and the person is not about to run `session-log`. Called by
the agent. The shared rules, marker and placement are in `docs/partial-captures.md`; read that
first.

## What to write

One entry, **fifteen lines at most**, under `## HH:MM [jot] <what the stretch was>`, time from
`date`. Answer only these, and skip any with nothing in it:

1. **Decisions and the alternative rejected.**
2. **Corrections.** What was stated as fact and turned out wrong, and what corrected it.
3. **Findings the tree does not hold.** Established by evidence, recorded by no file.

These are `session-log`'s first, second and fourth questions. Its open questions and its
where-the-work-stands paragraph are left out on purpose: open questions belong in the flag register,
where `touch` can put them, and the restart paragraph is only worth writing when a restart is near,
which is `session-log`'s moment.

## What it must not do

- Read any file to confirm what it writes. If unsure, write the uncertainty.
- Restate what a file on disk already says.
- Edit anything other than appending its entry. Standing files are `touch`'s.
- Run when compaction is near. Prompt the person to run `session-log` instead.

# Scope Pointer

- `session-log`: the person-run capture this is the small sibling of. A jot does not satisfy it.
- `touch`: the other partial. It records facts in standing files; this records reasoning.
- `session-close`: resets the partial count. Nothing here substitutes for any part of it.
