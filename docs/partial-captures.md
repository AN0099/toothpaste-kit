# Partial captures: the rules `jot` and `touch` share

`session-log`, `session-close` and `daily-dashboard` are run by a person, because they are expensive
and because each one either decides something or certifies something. Between them the agent still
needs to record things as they happen. Two small skills cover that, `jot` for reasoning and `touch`
for standing-file facts. This file holds the rules both depend on, so neither restates them.

## A partial capture never reads as a full one

Both skills write something that looks like the output of a larger procedure. The defect to prevent
is a later reader, human or agent, taking a stack of partials as proof that the larger procedure
ran. So:

- **Every partial is marked in its heading**, with `[jot]` or `[touch]`, and the marker is the
  first thing after the time. A reader scanning headings sees what kind of entry it is before
  reading any of it.
- **Neither discharges anything.** A day with ten jots and no `session-log` before a compaction has
  lost what `session-log` would have kept. A day with twenty touches and no `session-close` was
  never closed.
- **The count is visible.** An orient tool counts partials written since the last close, so the
  debt shows at every orientation instead of accumulating silently. `session-close` writes a
  heading containing `session-close run`, and that heading resets the count.

## Where they go

The day's capture file in the provenance layer, the same file `session-log` appends to, named by
the tree's always-loaded config. `jot` appends its entry there. `touch` edits a standing file and
then appends a one-line ledger entry there, so every standing-file edit made outside a close has a
dated trace in one place.

## Heading shape

```text
## HH:MM [jot] <what the stretch was>
## HH:MM [touch] <file>: <the fact, in a few words>
```

`HH:MM` comes from `date` at the moment of writing. Never write a placeholder minute or a time
ahead of the clock; a tree can gate both mechanically, and this one does.

## When the agent calls them

At a clean boundary: right after a commit, a dispatch, or a closed decision, when the fact is fresh
and nothing else is mid-flight. Not in the middle of a task, and not as a substitute for the
person's `session-log` when compaction is near. Near compaction the right move is to prompt the
person to run `session-log`.
