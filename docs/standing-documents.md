# Standing Documents

`redaction-gate` and `session-close` both name files that are not in this repository. They belong to the knowledge tree the kit was built against. This document describes that structure and how each file works, so the pointers resolve to something a reader can copy rather than to a private layout they have to guess at.

What follows is the shape. None of the content of those files is here, and none of it is going to be.

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
| Operating handoff | Roster, standing conventions, adopted decisions, open items. The document a person or agent reads to take over | Provenance |
| Work queue | Tasks with status and assignee. Machine-readable, so a session can tell queued work from finished work | Provenance |
| Open threads | Loose ends raised mid-conversation that do not yet have a task. Each entry states what was flagged, why it matters, and current status | Provenance |
| Resolved threads | Where an entry moves once it closes, carrying the resolution and its reasoning, not just a status flip | Provenance |
| Per-project state | One per active project. Current state, what is built, what is not | Human-facing |
| Procedures | One per recurring operation. How to run it, and the reasoning that is not recoverable from the command itself | Human-facing |
| Postmortems | One per incident or near miss. Kept permanently | Provenance, tiered |

## How they work together

**`index.md` is the entry point and it goes stale.** It names which documents must stay current, which is what `session-close` phase 2 checks. Trust it over memory of a previous session, and correct it when it is wrong.

**Threads move in one direction.** An entry is added to the open log when something is raised and not settled. It moves to the resolved log with its resolution written out. A status change alone loses the reason, which is the part worth keeping.

**Procedures record reasoning the command does not carry.** A procedure file exists when running the operation correctly depends on knowing why the flags are what they are. If the command is self-explanatory it does not need one.

**Postmortems are kept even when nothing broke.** A near miss with no damage is the most useful thing a session produces, because the control gap is visible and the cost of learning it was zero.

## Sensitivity tiering

The tree the kit was built against sorts material into four tiers by audience, with physical isolation as the primary control rather than filesystem permissions. Two axes are tracked separately: who may read a thing, and whether a system may retain it at all.

The content-depth principle is what makes the tiers mean anything. The lower two tiers carry almost nothing sensitive regardless of how wide the audience is, because the concern there is optics rather than access. The third carries operational behavior with entities abstracted into categories. Only the fourth carries actual reasoning and real named entities.

The consequence that matters for `redaction-gate`: moving a fact to a lower tier means stripping the reasoning, not only deleting the names. A paragraph with every proper noun removed can still be restricted content.

## Adapting this

Nothing here requires the filenames used above. Substitute your own. What the two skills actually depend on is that the roles exist and that someone can say which file plays each one:

- A manifest that says what is current
- A place where open questions go so they survive the session that raised them
- A separation between what a person reads and what an agent reads
- A sensitivity scheme with a stated rule for moving content outward
