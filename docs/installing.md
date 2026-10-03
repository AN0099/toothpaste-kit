# Installing

The [quickstart](quickstart.md) is one path: the kit cloned to
`~/toothpaste-kit`, a workspace at `~/tpkit-workspace`, and every skill
symlinked into that workspace. This guide says what each of those choices
does, what the alternatives are, and what each alternative costs. Run the
quickstart first unless you already know which alternative you want.

## What goes where

Claude Code loads the kit's parts in different ways, and each part goes
where its loading rule fits:

| Part | Claude Code feature | When it loads | Where the quickstart puts it |
|---|---|---|---|
| Conventions every session needs | `CLAUDE.md` | Every session, in full | The workspace root |
| Procedures such as `session-log` | Skills | The description every session, the body when invoked | `.claude/skills/` in the workspace |
| Mechanical gates such as the dash ban | Hooks, through the `hookify` plugin | On the event they match | Not installed by the quickstart; see Hooks below |
| Standing files and session logs | Ordinary files the skills read and write | When a skill opens them | The workspace root and `.agents/` |

The split follows the Claude Code documentation on
[matching features to a goal](https://code.claude.com/docs/en/features-overview):
a rule Claude must always know goes in `CLAUDE.md`, a procedure used
sometimes goes in a skill, and **a rule that must hold every time goes in a
hook**, because an instruction in `CLAUDE.md` or a skill is a request and a
hook is enforcement.

## Workspace-level or user-level skills

The quickstart installs the skills into one workspace's `.claude/skills/`.
The alternative is your user directory, `~/.claude/skills/`, where they load
in every project you open.

| | Workspace-level | User-level |
|---|---|---|
| Loads in | Sessions started in that workspace | Every session on this account |
| Finds the standing files | Yes, through the workspace's `CLAUDE.md` | Only in a directory whose `CLAUDE.md` names them |
| Command | `scripts/link-skills.sh <workspace>/.claude/skills` | `scripts/link-skills.sh` with no argument |

**Workspace-level is the default** because the loop depends on the
workspace's `CLAUDE.md`: `session-log` and `session-close` read it to find
where to write, and stop and ask when it says nothing. A skill installed
for every project reaches projects with no such file.

**A user-level copy shadows the workspace copy.** When a skill of the same
name exists at both levels, Claude Code uses the user-level one. Installing
at both levels, then updating only the workspace, leaves every session
running the old user-level version with nothing to say so. Install at one
level. To check, list both directories:

```sh
ls ~/.claude/skills ~/tpkit-workspace/.claude/skills
```

**Install the whole set.** The skills name each other in their Scope
Pointer sections, and a subset leaves those pointers leading nowhere.
Claude Code chooses a skill by its frontmatter `description`;
`skills/skill-discovery/SKILL.md` says how that resolution works.

## Symlink or copy

`scripts/link-skills.sh` symlinks each skill into the target directory.
Updating the clone then updates every installed skill, and the clone must
stay where it is. Targets are relative where `ln -r` exists, so moving
the clone and the workspace together keeps the links working; on systems
without it, such as macOS, they are absolute and the script says so.

Copy instead if you intend to edit the skills yourself:

```sh
cp -R ~/toothpaste-kit/skills/* ~/tpkit-workspace/.claude/skills/
```

A copy does not change when the clone does. Updating it means copying again
over your edits, so keep edited skills under their own names. The script
never overwrites a real directory: it reports `skip` and leaves it.

## Personal settings that are not shared

`CLAUDE.local.md` beside `CLAUDE.md` holds instructions for you alone.
Claude Code loads it after `CLAUDE.md` and it is meant to stay out of
version control. Put machine paths and personal preferences there, and
conventions everyone working in the workspace follows in `CLAUDE.md`.

## Hooks

`hooks/` in the kit holds seven rule files for the `hookify` plugin. They are
examples: they do nothing until the plugin is installed and the files are
copied into the workspace.

1. Install the plugin for the workspace, from inside it:

   ```sh
   cd ~/tpkit-workspace
   claude plugin install hookify@claude-plugins-official --scope project
   ```

2. Copy the rules you want into the workspace's `.claude/` directory:

   ```sh
   cp ~/toothpaste-kit/hooks/hookify.em-dash-gate.local.md ~/tpkit-workspace/.claude/
   ```

3. Start a new Claude Code session in the workspace.

`hookify.em-dash-gate.local.md` works anywhere: it blocks a write containing
an em dash. The other six assume a tiered directory scheme and name its
paths; edit their patterns to your own paths before enabling them, or they
match nothing and report clean.

## Updating

The quickstart's clone follows `main`. To update it:

```sh
git -C ~/toothpaste-kit pull
~/toothpaste-kit/scripts/link-skills.sh ~/tpkit-workspace/.claude/skills
```

Symlinked skills update with the pull. Run `scripts/link-skills.sh` again
with the same target afterwards, since an update can add a skill and the
script links only what exists when it runs. Read `CHANGELOG.md` in the clone
for what changed; a skill's own `CHANGELOG.md` says why.

The example workspace is not updated by a pull. Your workspace's files are
yours from the moment you copy them.

## Removing

Remove the skill links, then the clone. The links are found by where they
point, so a skill of your own in the same directory is left alone:

```sh
find ~/tpkit-workspace/.claude/skills -maxdepth 1 -type l -lname '*toothpaste-kit/skills/*' -delete
rm -rf ~/toothpaste-kit
```

The workspace is your work. Delete it separately, and only once you no
longer need its session logs.

## Growing the workspace

The quickstart's workspace is the smallest one the loop runs in. These are
the additions that tend to come next, each when something forces it.

**A place for unsorted imports.** Material arrives faster than it can be
filed: exports, downloads, notes from elsewhere. Give it a directory
**beside** the workspace, such as `~/store/intake/` with the workspace at
`~/store/workspace/`, so that an agent started in the workspace does not
read it before you have looked at it. Sort from there into the workspace.

**A repository for what you author.** Put the files you write and want
history for in one git repository inside the workspace, such as
`tracked/`, and leave what accumulates (session logs, queues, imports)
outside it. Write the in-or-out rule down once and follow it. A workable
default: **if it is authored, it goes in; if it is accumulated, it stays
out.** Projects you work on sit beside it, each its own repository.

**Sensitivity tiers.** Split by directory rather than by configuration once
the store holds material with different audiences. A sibling directory
outside every working tree beats a `.gitignore` line, because a line in a
config file is a control that fails silently. See
[security-posture.md](security-posture.md).

**Git authority.** Decide what an agent may do by where the remote points.
Anything reachable from the internet is read and edit only. Internal
remotes can take commits and branch pushes. **A merge into a trunk is a
decision rather than a record, so a person runs it.**

**A second agent.** Give each seat a mailbox directory and let mail be
commits, with one register file and one writer. A directory listing reads
one branch, so mail on another branch is invisible until you diff or merge,
and a single-writer register goes stale at the writer's rate rather than
the work's.

## What bites in the first week

- **Mixing the layers.** Session reasoning in a README makes it unreadable
  and unpublishable at once. Full statement in
  [document-layers.md](document-layers.md).
- **A gate verified by typing it.** Shell aliases mean the command you type
  and the command in a script can be different programs. Test the script.
- **Trusting `--dry-run`.** It proves a command assembles, never that it
  runs.
- **Provenance inside a repository that later gains a remote.** Decide the
  location before the first session log.
- **Copying the ceremony wholesale.** Much of this is sized for one person
  with agents, where the alternative to written procedure is one person's
  memory. Take the method and size the mechanisms yourself.

The rules underneath all of it are in `CLAUDE.md` in the example workspace,
and [standing-documents.md](standing-documents.md) describes the full
document set.
