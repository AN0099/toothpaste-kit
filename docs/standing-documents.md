# Standing Documents

`redaction-gate` and `session-close` are procedures, and a procedure assumes somewhere to put its output. This document describes the document set those two assume: what each file is for, how the pieces work together, and the sensitivity scheme the redaction procedure depends on.

The structure and the mechanics are what is shared. The contents of any working instance of them are not, and will not be. That split is deliberate: how a thread log works is useful to anyone running one, while what is written in a particular thread log is nobody else's business.

## The organizing principle

Two layers, never mixed in one file.

**Provenance** is written for agents. Reasoning, decision archaeology, what a previous version got wrong, why an option was rejected. Verbose is correct here. It lives outside any published repository.

**Human-facing** documents are written for a person with a task. What a thing does, how to use it, what it does not cover. Lean, concrete, no archaeology. These live in the repository.

Both layers are kept. The failure this prevents is a README that reads like a lab notebook, and a design record that was compressed into uselessness because it shared a file with instructions.

## The document set

| Document | Role | Layer |
|---|---|---|
| `CLAUDE.md` | Instructions loaded into every session rooted in the tree. Conventions that must not be re-derived | Human-facing |
| `index.md` | Manifest. What is authoritative, what is stale, what was added when. Read first in any session | Human-facing |
| `lead-handoff.md` | Roster, standing conventions, adopted decisions, open items. The document a person or agent reads to take over | Provenance |
| `task-queue.json` | Tasks with status and assignee. Machine-readable, so a session can tell queued work from finished work | Provenance |
| `threads-flagged.md` | Loose ends raised mid-conversation that do not yet have a task. Each entry states what was flagged, why it matters, and current status | Provenance |
| `threads-resolved.md` | Where an entry moves once it closes, carrying the resolution and its reasoning, not just a status flip | Provenance |
| `project-state.md` | One per active project. Current state, what is built, what is not | Human-facing |
| Procedures | One per recurring operation. How to run it, and the reasoning that is not recoverable from the command itself | Human-facing |
| `postmortem-*.md` | One per incident or near miss. Kept permanently | Provenance, tiered |

## How they work together

**`index.md` is the entry point and it goes stale.** It names which documents must stay current, which is what `session-close` phase 2 checks. Trust it over memory of a previous session, and correct it when it is wrong.

**Threads move in one direction.** An entry is added to the open log when something is raised and not settled. It moves to the resolved log with its resolution written out. A status change alone loses the reason, which is the part worth keeping.

**Procedures record reasoning the command does not carry.** A procedure file exists when running the operation correctly depends on knowing why the flags are what they are. If the command is self-explanatory it does not need one.

**Postmortems are kept even when nothing broke.** A near miss with no damage is the most useful thing a session produces, because the control gap is visible and the cost of learning it was zero.

## Sensitivity tiering

The scheme sorts material into four tiers by audience, with physical isolation as the primary control rather than filesystem permissions. Two axes are tracked separately: who may read a thing, and whether a system may retain it at all.

The content-depth principle is what makes the tiers mean anything. The lower two tiers carry almost nothing sensitive regardless of how wide the audience is, because the concern there is optics rather than access. The third carries operational behavior with entities abstracted into categories. Only the fourth carries actual reasoning and real named entities.

The consequence that matters for `redaction-gate`: moving a fact to a lower tier means stripping the reasoning, not only deleting the names. A paragraph with every proper noun removed can still be restricted content.

## Why these filenames are here at all

The names above are real. The contents are not, and that is not an oversight in one direction or the other.

A filename either names a **role** or names a **subject**. A role name says what the file does for the system: a manifest, a work queue, a thread log. Every system organized this way has one, so the name discloses nothing except that you are organized. A subject name says what the file is about, and it is a fact about you before anyone opens it. An inventory of where credentials live, a ledger of who contributed what, a postmortem titled after the specific thing that went wrong: each of those leaks in the filename alone, and none of them appears here.

The same test applies to anything else leaving a private tree. Publish role names freely; treat a subject name as content, and redact it as content.

## Adapting this

Nothing here requires the filenames used above. Substitute your own. What the two skills actually depend on is that the roles exist and that someone can say which file plays each one:

- A manifest that says what is current
- A place where open questions go so they survive the session that raised them
- A separation between what a person reads and what an agent reads
- A sensitivity scheme with a stated rule for moving content outward
