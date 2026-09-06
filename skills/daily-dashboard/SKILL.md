---
name: daily-dashboard
description: Open a working day with a dashboard of where the tree actually stands. Reads the standing files, verifies carry-over work against the working trees rather than trusting the last session's closing report, then presents project state, ranked todos, roadmap, and the decisions waiting on the human. Invoke at the start of a working session. The mirror of session-close, which writes what this reads; it does not capture session residue, and it does not begin the work it lists.
disable-model-invocation: true
---

# When to Use

At the start of a working session, before any task is chosen. Invoked by a person, never by an agent.

**Adapting this skill:** filenames below name roles rather than literal paths. `docs/standing-documents.md` describes the document set, what each file does, and how the pieces work together. `db` throughout means whatever your durable store is called. Substitute your own filenames freely.

`session-close` writes the day's residue to disk. This skill reads it back. The two are one loop, and the loop only closes if the reading half checks the tree instead of reciting what the last session claimed. Those disagree more often than they agree. The session this skill was reconstructed from found a queue task with no status field and a manifest naming a file that was not on disk, both inside the documents it was quoting.

Work the phases in order. Phase 4 is the point of the whole procedure.

## Phase 0: This is chat output, not a document

The dashboard is a message. Do not write it to a file, and do not open a daily note, a summary, or a scratch document to hold it, unless asked for one in the same breath. Everything in it worth keeping is already some standing file's job, and a second copy is how two sources of truth get born. This tree also has a standing rule against generating a document without explicit permission, and a dashboard is not that permission.

## Phase 1: Read the standing files

`CLAUDE.md` names where the list of must-stay-current files lives. Read the manifest first. It is the file that says what is authoritative versus stale, it goes out of date, and it still outranks memory of past sessions and this skill's description of it.

Then read, and name which ones you read:

- the manifest, for what is authoritative versus stale
- the task or work queue, for phase, counts, assignees, and blocked items
- the operating handoff document, for roster and standing conventions
- the open-threads log, for what is blocked and on whom
- per-project state documents for anything actively developed

Read the files themselves. Summarizing from the manifest's one-line description of a document is how a dashboard reports a state that stopped being true days ago.

## Phase 2: Verify carry-over against the tree

The previous session's closing report is a claim, not a state. Check it.

Walk every Git working tree in the store, not only the one you remember being active, and report per tree: branch, sync state against its remote, staged and unstaged files, untracked files. Name the files. A count is not something a person can act on.

If the last session ended with a command sequence that was drafted and never run, reproduce it as runnable steps, and restate its preconditions as checks you ran just now. A precondition verified yesterday is not verified. Present the result as a short table so a failed check is visible rather than buried in prose.

While reading, record any defect you trip over in the standing files themselves: a task missing a field, a manifest entry naming a path that does not exist, a status that contradicts what the tree shows. These are the highest-value output of this phase, because nothing else in the system looks for them and the dashboard is the only procedure that reads all of these files together.

## Phase 3: Assemble four sections

In this order, and do not reorder them by what seems interesting.

1. **Carry-over.** What was left mid-flight, with the precondition table from phase 2 and the exact commands. First, because it is the only time-sensitive section.
2. **Project state.** A short block per active project: what it is, what moved last session, what is uncommitted, known gaps. Include projects that saw no activity and say so. A project silently absent from the dashboard reads as a project that is fine.
3. **Immediate todos, ranked.** Rank by whether something is currently unprotected or falsely reporting clean, not by effort, age, or queue order. A check that reports clean because it was never wired up outranks a feature that is merely missing: the first is actively lying, the second is only absent. State the ranking rule in the section so the human can overrule it.
4. **Roadmap and decisions waiting on the human.** Queue phases with counts, then the decisions that are the human's to make, each written as the question rather than as a topic. Keep "specced, not built" on its own line so it stops competing with work that is ready to start.

## Phase 4: End with questions, and stop

Close with numbered questions, `Q1` onward. Take no action on any of them. The first asks whether to run the carry-over sequence; the last asks which item is today's actual work. Then stop.

This is the phase the skill exists for. A dashboard that slides into doing the work has chosen the day's priority for the human, using a ranking it invented four paragraphs earlier. `disable-model-invocation` is set for the same reason: an agent does not get to decide the day has started.

# Scope Pointer

- `session-close`: the other half of the loop, and the one that writes what this reads. Anything this skill finds unrecorded belongs to that procedure, not this one. Do not capture session residue here.
- `session-log`: mid-session capture. It writes to the provenance layer only and never to the
  standing files this skill reads, so anything it captured reaches here only after a `session-close`.
- `working-preferences`: source of truth for the command vocabulary and for the standing Q1 through Q3 convention that phase 4 extends.
- `redaction-gate`: runs before content crosses a sensitivity boundary outward. This skill crosses none; it reads local state and reports in chat. If the day's work will cross one, that gate is a separate invocation.
- `document-standards`: governs any document written as a result of the dashboard. It does not govern the dashboard itself, which is chat output, not a generated document.
