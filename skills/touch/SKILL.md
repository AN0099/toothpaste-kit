---
name: touch
description: Agent-callable single-fact update to a standing file, made right after the work it records. One queue status, one new flag, or one state line, plus a marked ledger line in the day's capture file. Never moves, resolves or rewrites; never runs checks. Does not replace or satisfy session-close.
---

# When to Use

Immediately after the work a standing file should now reflect: a task finished and verified by a
second party, an open question raised, a state change a later session must see. Called by the agent.
The shared rules, marker and placement are in `docs/partial-captures.md`; read that first.

## The allowed edits

One fact per call, and only these kinds:

| Standing file | Allowed |
|---|---|
| Task queue | Set one task's status, with a dated note saying what verified it and who the second party was |
| Open-threads log | Append one dated group before the resolved section |
| Manifest | Append one line to the current state section |

**The fact must have come from this session's work.** A touch records what just happened; it does
not correct what an earlier session wrote. A wrong line found in a standing file goes into the
open-threads log as a finding, and `session-close` fixes it.

Then append to the day's capture file:

```
## HH:MM [touch] <file>: <the fact, in a few words>
```

Time from `date`. Build every edit with a script that asserts its anchor occurs exactly once, so a
missing or doubled anchor fails loudly instead of writing in the wrong place.

## What it must not do

- Mark a task complete on the claimant's word alone. Complete needs a second party, named in the
  note.
- Move a thread to the resolved log, delete a flag, or rewrite an existing line. Those are judgment
  over the whole record, and they are `session-close`'s.
- Run the dash sweep or any other check, or state that one passed.
- Touch the operating handoff document. Its roster and conventions change by decision, not by
  event.

# Scope Pointer

- `session-close`: the full update of every standing file, with the sweep and the checks. It resets
  the partial count, and a stack of touches does not discharge it.
- `jot`: the other partial. It records reasoning; this records facts.
- `daily-dashboard`: reads the standing files and checks them against the tree, so a touch that got
  a fact wrong is caught there if not before.
