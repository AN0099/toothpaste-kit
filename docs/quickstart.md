# Quickstart

Six steps, in order, from nothing to a first session log on disk. Each step
ends with what you should now see. If you see something else, stop there:
the steps after it assume it worked.

This page has one path and no options. Other ways to install, and what each
part is for, are in [the installing guide](installing.md).

## What you will have at the end

A workspace directory that Claude Code starts in, holding the files the
kit's skills read, with every skill installed into it. You will have run one
skill, `session-log`, and it will have written a file. That file is the
point of the kit: **if work is not written into the store, it did not
happen.**

## 1. Check the prerequisites

You need Claude Code, git, and a POSIX shell, on Linux. Run:

```sh
claude --version
git --version
ls ~/toothpaste-kit ~/tpkit-workspace
```

**You should now see** a version number from each of the first two, and
`No such file or directory` for both paths in the third. If either path
exists, stop: the steps below create both, and this page does not cover
installing over an existing copy.

## 2. Clone the kit

```sh
git clone https://github.com/AN0099/toothpaste-kit.git ~/toothpaste-kit
```

**You should now see** `~/toothpaste-kit/skills/` and
`~/toothpaste-kit/examples/workspace/` when you run:

```sh
ls ~/toothpaste-kit/skills ~/toothpaste-kit/examples/workspace
```

The clone is the kit. Your own work never goes inside it, so that updating
the kit never touches your work.

## 3. Copy the example workspace

```sh
cp -R ~/toothpaste-kit/examples/workspace ~/tpkit-workspace
ls -A ~/tpkit-workspace ~/tpkit-workspace/.agents
```

**You should now see** `.agents`, `CLAUDE.md` and `index.md` in the
workspace, and `context`, `lead-handoff.md`, `task-queue.json`,
`threads-flagged.md` and `threads-resolved.md` in `.agents`.

These are the standing files the skills read. `CLAUDE.md` tells every
session where the others are: the session logs go in `.agents/context/`, and
`index.md` lists the files that must stay current. The rest are stubs with
comments saying what goes in them. Leave them as they are for now.

## 4. Install the skills into the workspace

```sh
~/toothpaste-kit/scripts/link-skills.sh ~/tpkit-workspace/.claude/skills
```

**You should now see** one `link` line per skill, then a summary line
ending `0 skipped, into` and the workspace's `.claude/skills` path.

Each skill is now a symlink into the clone, so updating the clone updates
the skills.

## 5. Start Claude Code in the workspace

```sh
cd ~/tpkit-workspace
claude
```

If this is the first time Claude Code has run for your user account, it
first asks you to choose a theme and to sign in; complete both. It then
asks whether you trust the folder. Answer yes.

**You should now see** `session-log` in the list when you type
`/session` at the prompt. The skills run when you type their names this
way; none of the loop's skills starts on its own.

## 6. Run `session-log`

`session-log` records reasoning that a long conversation would otherwise
lose, so it needs something to record. Type this as a message first:

```text
We decided to keep the workspace at ~/tpkit-workspace, outside the kit's
clone, so that updating the kit never touches our own files.
```

Then type:

```text
/session-log
```

When it finishes, type this at the Claude Code prompt to list the folder:

```text
! ls .agents/context
```

**You should now see** one file named `session-` followed by today's date
and a short slug, ending `.md`. It holds an entry headed with the time,
recording the decision you typed.

## Done

The loop is running. Two more skills complete it: type `/session-close` at
the end of a working session and `/daily-dashboard` at the start of the
next one. [The installing guide](installing.md) covers updating and
removing the kit, installing for every project instead of one, hooks, and
what to read next.
