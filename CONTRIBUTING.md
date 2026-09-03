# Contributing

toothpaste-kit is maintained by Bridle Works. This covers what to read first, the rules that apply to every change, and how to submit one.

## Start here

Read `README.md` for what the project does and `philosophy.md` for why it works the way it does. Changing a skill also means reading `skills/skill-creation/SKILL.md` first, since it defines the required structure and the checklist a skill passes before it counts as live.

## Rules that apply to every change

**No em dashes in AI-generated text.** This is a hard rule. If you drafted anything here with an agent, check the output mechanically before committing:

```
grep -rnP '\x{2014}' .
```

**Verify completion claims before repeating them.** When an agent reports that it wrote a file, confirm the file exists and holds what it should. An agent auditing its own work does not satisfy this.

**Use public task IDs only.** This project runs two task queues. The public one uses `TK-` ids
(`TK-014`). The private queue and its open items use a phase-and-number form and an
OPEN-prefixed form, spelled out in the pattern below. Neither appears in this repo. An id in the private format is a signal that
private context came with it, so check what else the sentence carries:

```
grep -rnE '\b(P[0-9]+-[0-9]+|OPEN_[0-9]+)\b' .
```

That check must return nothing. The two formats cannot collide, so a single grep catches drift.

**Raise findings instead of quietly resolving them.** If something looks wrong or inconsistent, say so in the issue or the pull request. A unilateral fix hides the disagreement that prompted it.

## Skills

One directory per skill under `skills/`, containing `SKILL.md` and an optional `references/`. Frontmatter requires `name` and `description`.

The description decides when the skill loads, so it should state what the skill covers and what it does not, with a pointer to whichever skill handles the excluded part. Skills reference each other by name, so renaming one means updating every reference. Run `grep -rn '<old-name>' skills/` before you call it done.

## Orchestration

`orchestration/protocol.md` and the two JSON schemas define the message contract between agents. Changing a field means changing the schema, the protocol document, and `taxonomy.md` together, since they are read by separate agents that will not notice a partial update.

## Commits and pull requests

Configure `user.email` before your first commit. Use the noreply address your forge provides, not a
personal mailbox. An address in a public commit log is permanent, scraped quickly, and part of the
commit hash, so correcting it later rewrites history.

One logical change per commit. Commit messages should say what changed and why. Keep generated output, index databases, and packed repository files out of the repo. `.gitignore` covers the known cases.

## What does not belong here

Operational and business material lives outside this repository entirely and is never committed to it. Anything that names a client, an internal process, or a person's private details is out of scope for this repo regardless of where you found it. If you cannot tell which side of that line something falls on, ask before pushing.

## What kind of writing goes in this repo

Docs here are written for a person with a task. State what a thing does, how to use it, and what
it does not cover. Skip the archaeology: which options were weighed, what a previous version got
wrong, how the decision felt at the time.

That material is worth keeping and is kept, in a separate provenance layer outside this repo. Two
exceptions live here on purpose. A skill's `CHANGELOG.md` records why that skill is shaped the way
it is, because a later editor needs it to avoid silently undoing a deliberate choice. The repo-level
`CHANGELOG.md` records what changed. Neither is a session log.

Practical test before you commit a doc: could a contributor who has never spoken to the maintainers
act on it? If a sentence only makes sense to someone who was in the room, it belongs in the
provenance layer.

## Questions

Ask. A question costs less than a wrong assumption acted on.
