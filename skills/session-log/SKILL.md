---
name: session-log
description: Mid-session capture, run when the conversation is about to be compacted, handed off, or otherwise lose its detail while the work is unfinished. Writes the reasoning from the recent stretch to one append-only file in a single pass, with no verification sweep and no standing-file updates. Deliberately cheaper and narrower than session-close, which it does not replace and does not satisfy.
disable-model-invocation: true
---

# When to Use

Mid-session, when context is about to be compacted or handed to another agent and the work is not
finished. Invoked by a person.

**Adapting this skill:** filenames below name roles rather than literal paths. `db` throughout means
whatever your durable store is called. Substitute your own filenames freely.

`session-close` is expensive on purpose. It sweeps a whole session by category, updates every
standing file, and runs mechanical checks. That price is correct once, at the end. It is wrong three
times in an afternoon, and a procedure too expensive to run at the moment it is needed is a
procedure that does not get run. The gap this fills is the compaction boundary, where reasoning is
lost quietly and nothing is on fire.

**Running this does not satisfy `session-close`.** It skips the sweep, the standing files, and the
checks by design. A session that ends after a `session-log` is a session that was never closed. Say
so in the log rather than letting the file's existence imply otherwise.

## What compaction actually destroys

Only one thing, and aiming at it is what keeps this cheap.

The tree survives compaction. Files written this session are still on disk, and a later session can
read them. What does not survive is **why they look like that**: the alternative that was rejected,
the constraint that ruled it out, the thing that turned out to be false halfway through.

So do not restate what a file says. If a sentence could be recovered by opening the file it
describes, it does not belong in the log. This single rule is most of the cost difference between
this skill and `session-close`.

## Scope

The stretch since the last capture, not the session. If an earlier `session-log` exists for today,
start after it. If not, start wherever the current line of work began.

## What to write

Five questions. Answer only the ones with something to answer, and skip the rest without comment
rather than writing "none" five times.

1. **Decisions and the alternative rejected.** The choice, the reason, and what was turned down.
2. **Corrections.** Anything stated as fact that turned out to be wrong, and what corrected it.
3. **Open questions.** Raised and unresolved. Include who or what is blocking.
4. **Findings the tree does not hold.** Something established this stretch by evidence, about the
   harness, the tooling, or the environment, that no file in the store records and no file would
   have produced. A correction is the tree being wrong about something; this is the tree never
   having known it. These are the most expensive things to rediscover and the easiest to lose,
   because they arrive as a side effect of doing something else and never look like output.
5. **Where the work stands.** One paragraph a future session can restart from. Name the next
   concrete action, not the goal.

## Where it goes

One dated file in the provenance layer, `session-<date>-<slug>.md`, created on the first capture of
the day and appended to after that. Append, never rewrite: a later entry contradicting an earlier one
is a correction worth having both halves of. Head each entry with the time.

**Do not invent the directory.** The tree states where its provenance layer lives, in the same
always-loaded config that names the standing-files list, and that statement is the binding. Read it
rather than guessing, because the plausible guesses are wrong in a way that does damage: a capture
written into the repo puts session residue in a tree that may later get a remote, which is the exact
mixing the two-layer rule forbids. If the tree says nothing, stop and ask rather than picking a path.

Provenance is verbose by default and stays out of any public repo. Nothing written here goes into a
human-facing document.

## What this skill deliberately does not do

Do not update the manifest, the queue, the handoff document, or the threads logs. Do not run the
dash sweep or any other mechanical check. Do not verify a completion claim. Do not read files to
confirm what you are writing; if you are unsure whether something happened, write the uncertainty
down and move on. Each of these belongs to `session-close`, and pulling one of them forward is how
this skill turns into a second copy of that one.

# Scope Pointer

- `session-close`: the full end-of-session procedure. Everything this skill skips lives there, and
  a log written here does not discharge it.
- `daily-dashboard`: the start-of-session half of the loop. It reads the standing files, which this
  skill never writes to, so a log captured here reaches the next day only through `session-close`.
- `document-standards`: does not apply. This file is provenance for agents, not a generated document
  for a reader, and the two layers are never mixed in one file.
