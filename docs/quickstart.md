# Quickstart

Gets the loop running in an afternoon. Everything after step 3 is
optional and can wait until something forces it.

This page is deliberately thin. Each section points at the document that
holds the full statement rather than restating it, because two copies of
a rule is how the rules start disagreeing.

## What you are building

One durable store that outlives any session, and a short loop that keeps
it current. The rule that makes it work: **if it is not written into the
store, it did not happen.** A session transcript is not the store.

Two layers, never mixed in one file. Provenance is written for agents and
is verbose by design. Human-facing documents are written for a person
with a task and carry no archaeology. Full statement in
[document-layers.md](document-layers.md).

## 1. The skeleton

```sh
mkdir -p ~/store/{workspace,intake}
cd ~/store/workspace
mkdir -p .agents/context .claude/skills tracked projects
git init tracked
```

`tracked/` is version controlled and everything beside it is deliberately
not. `.agents/context/` is the provenance layer and never sits inside the
repository. `projects/` holds real repositories, each with its own git.

Write the in-or-out rule down once, in a `TRACKING.md`, and follow it. A
workable default: **if it is authored, it goes in; if it is accumulated,
it stays out.**

## 2. The file the agent reads every session

`CLAUDE.md` at the workspace root. Start with five conventions and add
only when something bites you:

```markdown
- No completion claim is fact until verified by someone other than the
  claimer. Self-audit is not verification.
- State a check's coverage, or it is not a check.
- Verify a check against a planted positive before believing a clean
  result.
- Two occurrences before a conclusion, including for a diagnosis.
- Two document layers, never mixed in one file.
```

Then write `index.md`, even at ten lines. It is the manifest of what is
authoritative versus stale, it is read first every session, and it
outranks memory of past sessions. See
[standing-documents.md](standing-documents.md) for the full document set
and how the pieces relate.

## 3. The loop

Three skills, each a directory under `.claude/skills/` holding a
`SKILL.md`.

| Skill | When | What it does |
|---|---|---|
| `daily-dashboard` | Session start | Reads the standing files, checks their claims against the tree, reports carry-over and ranked work, then stops |
| `session-log` | Before a compaction | Captures only what compaction destroys: decisions and the alternative rejected, corrections, open questions, findings no file holds |
| `session-close` | Session end | Sweeps the session, updates the standing files, runs the mechanical checks |

The property that matters: the dashboard **checks the previous session's
claims against the tree rather than reciting them.** Those disagree more
often than they agree, and the disagreement is the output.

**Start with `session-log`.** It is the cheapest of the three and it
prevents the most expensive loss.

## 4. Later, when you need it

**Sensitivity tiers.** Split by directory rather than by configuration
once the store holds material with different audiences. A sibling
directory outside every working tree beats a `.gitignore` line, because a
line in a config file is a control that fails silently. See
[security-posture.md](security-posture.md).

**Git authority.** Decide what an agent may do by where the remote
points. Anything reachable from the internet is read and edit only.
Internal remotes can take commits and branch pushes. **A merge into a
trunk is a decision rather than a record, so a person runs it.**

**A second agent.** Give each seat a mailbox directory and let mail be
commits, with one register file and one writer. Two things that will
bite: a directory listing reads one branch, so mail on another branch is
invisible until you diff or merge, and a single-writer register goes
stale at the writer's rate rather than the work's.

## 5. The rules that do the real work

1. **A check that has never failed has not been shown able to fail.**
2. **State a check's coverage or it is not a check.** A check reading part
   of its field and returning clean is worse than no check, because a
   clean result stops the search.
3. **Two occurrences before a conclusion.** One passing trial is not
   confirmation of a cause.
4. **A grep is a data point, never sole evidence.** Run it against input
   known to match and input known not to. A single-line pattern cannot
   match a sentence that wraps.
5. **No completion claim is fact until a second party verifies it.**

Everything else here is one of these applied to a specific surface.

## 6. What bites in the first week

- **Mixing the layers.** Session reasoning in a README makes it
  unreadable and unpublishable at once.
- **A gate verified by typing it.** Shell aliases mean the command you
  type and the command in the script can be different programs. Test the
  script.
- **Trusting `--dry-run`.** It proves a command assembles, never that it
  runs.
- **Provenance inside a repository that later gains a remote.** Decide
  the location before the first capture.
- **Copying the ceremony wholesale.** Much of this is sized for one
  person with agents, where the alternative to written procedure is one
  person's memory. Take the method and size the mechanisms yourself.
