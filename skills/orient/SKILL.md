---
name: orient
description: Re-establish where things actually stand before acting. Runs the tree's own reorient tool for the mechanical half, then answers four questions against its output: what moved, where the record disagrees with the tree, which carried assumption did not survive, and whether the next action changes. Deliberately cheap. Use after a compaction, after a handoff, when returning to a session, or before acting on any summary. Not a replacement for daily-dashboard, which opens a working day and ranks the work.
---

# When to Use

Whenever you are about to act on a belief about the state that you did not just verify. After a
compaction. After a handoff. Returning to a session left open. Before trusting a summary.

## The split this skill enforces

**Observing is mechanical and the model must not do it. Orienting is judgement and a script must not
do it.** Every token spent having a model rediscover which branch a tree is on is a token not spent
on the only part that needs a model, which is noticing that two records disagree.

That split is the cost argument. An unstructured reorientation runs eight to twelve exploratory
commands and reads all their output. This runs one.

## Phase 1: Observe, with the tool that already exists

```sh
just reorient          # or tracked/system/bin/reorient
just reorient --fetch  # when remote state matters; REFS says how stale it is
```

One command. Read its output. **Do not go looking for more.** It ends with a `COVERAGE` block
naming what it read and what it deliberately did not; if something you need is outside that block,
the fix is to extend the tool so the next run has it too, not to run an ad hoc command that leaves
no trace.

**Check for this tool before writing another one.** This skill was first written around a
second, near-identical tool built without looking, on a tree that already had this one and a
flagged thread describing it. The duplicate was deleted the same session. Prior art in this tree
is usually a `bin/` entry and a `just` recipe, and `just --summary` lists them.

## Phase 2: Orient

Four questions, answered against that output. Skip any with nothing to say.

1. **What moved that I did not move?** A branch tip, a capture, mail, a dirty file, a standing file
   older than the thing it describes. This one is always worth asking.
2. **Where does the record disagree with the tree?** A summary, a capture, a queue or a register
   saying one thing while the tool says another. **Name the disagreement rather than silently taking
   the tool's side**, because which one is wrong is itself the finding.
3. **What did I carry in that does not survive this?** State the assumption you arrived with and
   whether it held. A carried assumption that is never stated cannot be falsified.
4. **Does the next concrete action change?** Either name the new one or say the old one stands.

## Cost discipline

The report is a short message, not a document. Ten lines is normal and one line is fine: "Nothing
moved since the capture; the next action stands." **A long orient report means orienting turned into
working**, which is the failure this skill is shaped to avoid.

Write nothing to disk. Anything worth keeping belongs to `session-log` or `session-close`, and a
finding recorded in two places goes stale in one of them.

## Why this one may be model-invoked

`daily-dashboard` sets `disable-model-invocation` because it chooses a day's priority, and that is a
person's call. This skill chooses nothing. It reads and reports, and the compaction boundary that
most needs it is an event only the agent notices. So it is available to the agent, and it still ends
without starting any work.

# Scope Pointer

- `daily-dashboard`: the full start-of-day procedure. It reads the standing files, verifies
  carry-over, ranks todos and ends in questions. This is the cheap subset answering only "where are
  we", and running it does not discharge that one.
- `session-log`: the write half of the same boundary. This reads state, that records reasoning, and
  a compaction wants both.
- `session-close`: end of session. Nothing here substitutes for any part of it.
