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

**Use public task IDs only.** This project runs two task queues. The public one uses `TK-` ids (`TK-014`). The private queue and its open items use a phase-and-number form and an OPEN-prefixed form, spelled out in the pattern below. Neither appears in this repo. An id in the private format is a signal that private context came with it, so check what else the sentence carries:

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

Configure `user.email` before your first commit. Use the noreply address your forge provides, not a personal mailbox. An address in a public commit log is permanent, scraped quickly, and part of the commit hash, so correcting it later rewrites history.

One logical change per commit. Commit messages should say what changed and why. Keep generated output, index databases, and packed repository files out of the repo. `.gitignore` covers the known cases.

**No tool attribution in commit messages or pull request bodies.** No `Co-Authored-By` line naming an AI, no session links, no generated-with footers. A commit message records what changed and why; which editor, model, or agent was in the loop is not part of that and is not something a reader can act on.

Three layers enforce this, and only the third binds:

1. If you use Claude Code, `.claude/settings.json` in this repo sets `attribution` to empty and disables the session link. Nothing to remember.
2. A `commit-msg` hook lives in `.githooks/`. Enable it once per clone:

   ```
   git config core.hooksPath .githooks
   ```

   Git does not transmit hooks on clone, so this is opt-in, and `--no-verify` walks past it. Treat it as a fast local failure rather than a guarantee.
3. The `commit-attribution` workflow scans every commit in a pull request. It is the layer that binds, provided the maintainer has set it as a required status check in the ruleset on `main`. Without that setting it reports a failure and blocks nothing. Where it is required, a branch that reaches review with a trailer in its history needs those messages rewritten and the branch force-pushed.

Human co-author trailers are fine and expected. The rule is about tools.

## Hook rules

`hooks/` holds `hookify` rules as examples. They are inert where they sit and do nothing until copied into a `.claude/` directory.

A rule is one `.local.md` file: YAML frontmatter defining the match, then a Markdown body that is shown to the agent when it fires. The body is the part that matters. A rule that blocks without explaining why gets worked around or disabled, so the body should name what tripped, why the rule exists, and what to do instead. Several rules here cite the specific failure that motivated them for that reason.

Adding one:

- `action: block` stops the tool call. `action: warn` lets it through and adds a notice. Reach for `warn` unless the thing being prevented is unrecoverable. Most of the rules here warn, because reading sensitive material is normal work and the thing worth catching is what happens afterward.
- Match on command position, not bare substrings, for anything matching shell commands. A rule that fires on a tool name inside a quoted heredoc makes writing documentation about that tool impossible.
- Give the rule a false-positive escape and say what it is. If a contributor cannot get legitimate work past a rule, they will disable it, and a disabled rule protects nothing.
- Exempt by filename, not by weakening the pattern. Two rules here exempt files that must quote the thing they forbid.
- State the rule's limits in its own body. Every pattern-based rule has ways around it. Saying so is what keeps it from being mistaken for a boundary.

Test a rule against three cases before adding it: something that must trip it, something legitimate that must not, and the rule's own documentation.

## What does not belong here

Operational and business material lives outside this repository entirely and is never committed to it. Anything that names a client, an internal process, or a person's private details is out of scope for this repo regardless of where you found it. If you cannot tell which side of that line something falls on, ask before pushing.

## What kind of writing goes in this repo

Docs here are written for a person with a task. State what a thing does, how to use it, and what it does not cover. Skip the archaeology: which options were weighed, what a previous version got wrong, how the decision felt at the time.

That material is worth keeping and is kept, in a separate provenance layer outside this repo. Two exceptions live here on purpose. A skill's `CHANGELOG.md` records why that skill is shaped the way it is, because a later editor needs it to avoid silently undoing a deliberate choice. The repo-level `CHANGELOG.md` records what changed. Neither is a session log.

Practical test before you commit a doc: could a contributor who has never spoken to the maintainers act on it? If a sentence only makes sense to someone who was in the room, it belongs in the provenance layer.

## Questions

Ask. A question costs less than a wrong assumption acted on.
