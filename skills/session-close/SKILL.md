---
name: session-close
description: Run the end-of-session capture procedure for this PKD. Sweeps the session for reasoning, decisions, and near misses that exist nowhere on disk, then updates the six files that must stay current. Invoke before ending any working session.
disable-model-invocation: true
---

# Session Close

**Adapting this skill:** filenames below name roles rather than literal paths.
`docs/standing-documents.md` describes the document set, what each file does, and
how the pieces work together. `db` throughout means whatever your durable store is
called. Substitute your own filenames freely.

`db` is the durable store. Anything living only in a session is gone when that
session ends, including a completion claim resting on an account-level skill
mount. This procedure existed as a manual prompt the human had to remember to
type. The trigger is now this skill.

Work the phases in order. Do not skip phase 1 because nothing obvious comes to
mind; the prompt that motivated this skill found six unrecorded items on a
session where the answer felt like "nothing".

## Phase 1: Sweep for unrecorded reasoning

Read back over the session and ask, explicitly and separately for each category:

1. **Decisions made.** Any choice with a rationale, including ones that felt
   obvious at the time. Record the alternative that was rejected and why, not
   just the outcome.
2. **Near misses.** Anything that almost went wrong, was caught by luck rather
   than by a control, or revealed that a control did not cover a surface. These
   are postmortem candidates. A near miss with no harm done is still the most
   valuable thing a session produces.
3. **Corrections.** Any point where a stated fact turned out to be wrong, or an
   agent's claim did not survive checking. Record the correction and its source.
4. **Conventions.** Any rule that was applied but is not written down anywhere,
   or any written rule that was found to be inaccurate.
5. **Open questions.** Anything raised and not resolved. These belong in
   `threads-flagged.md`, not in a summary that disappears.
6. **Superseded material.** Anything on disk that this session made stale.
   Two cases are easy to miss. A file that **moved between sensitivity tiers**
   leaves its old path behind in every document that referenced it, and a
   sentence describing what is in that file is content wherever it sits, not only
   where the file now lives. A document whose **framing was overtaken** still
   reads correctly line by line while arguing a position the session has since
   changed; its opening paragraph is usually where this shows.

For each item found, decide its layer before writing it. Provenance material
(reasoning, decision archaeology, session residue) goes to
`agents/claude/context/` or the appropriate sensitivity tier. Human-facing
material (README, CONTRIBUTING, project state, skill files) goes to the repo,
lean and without archaeology. Never mix the two in one file.

When a sweep in this phase means searching for references by name, drive the walk
yourself as phase 3 does. A bare recursive grep may honor ignore files, which
excludes exactly the trees a tier-move sweep most needs to reach, and returns
clean.

## Phase 2: Update the standing files

Your tree should name, in one place, the files that must stay current, and
`CLAUDE.md` is where to say which place that is, since it loads into every
session. Check each one and state explicitly whether it needed a change, rather
than silently skipping it. Substitute your own list here. The shape that has
worked:

- The manifest naming what is authoritative versus stale
- The task or work queue
- The operating handoff document (roster, conventions, open items)
- The open-threads log
- The resolved-threads log
- Per-project state documents for anything actively developed

Move any thread that closed this session from `threads-flagged.md` to
`threads-resolved.md`, with the resolution recorded, not just the status change.

## Phase 3: Mechanical checks

Run these. Do not eyeball them.

```
grep -rlP '\x{2014}' --include='*.md' . | grep -v -e em-dash -e banned-words
```

Any file listed is a violation of the standing dash convention and must be fixed
before close. The two excluded filenames quote the character deliberately.

**That command covers one of the two characters the convention bans.** Run the
second one too, and read its result differently:

```
find . -name '*.md' -not -name '*em-dash*' -not -name '*banned-words*' \
  -exec grep -lP '\x{2013}' {} +
```

The first command is a gate: an em dash is a violation wherever it appears. The
second is a review prompt: an en dash is a violation when it separates clauses and
correct when it joins a range, and **no pattern tested here separates those two
uses**. A rule flagging en dashes outside digit pairs was measured against this
tree and flagged `Mar 15 - Aug 30` and `Apr-Jun 2026`, which are ranges, so it
would have taught its reader to dismiss it.

So report the count and look at the hits. Do not gate on them, and do not report
zero en dashes when the check was never run, which is what this skill did until
2026-09-04. A check that silently covers half its rule is the failure this phase
warns about two paragraphs above, and it was in this file.

**Verify the sweep before trusting a clean result.** A search that returns
nothing is indistinguishable from a search that is silently broken, which is the
failure mode where a check "looks like coverage" and is worse than no check.
Write a throwaway file containing the character, confirm the command lists it,
then delete it.

**Known coverage gap.** Some environments route `grep` through a wrapper that
honors ignore files by default, which silently excludes the tier tree, the
unfiled tree, and the archive. Those are exactly the directories where the sweep
is still recorded as incomplete in `index.md`. When exhaustive coverage is the
point, drive the walk yourself rather than trusting the default:

```
find . -name '*.md' -not -name '*em-dash*' -not -name '*banned-words*' \
  -exec grep -lP '\x{2014}' {} +
```

Verify the memory store is still contained inside the restricted tier:

```
grep MEMORY_FILE_PATH .mcp.json
```

The path must resolve inside `CLASSIFIED/04-restricted/`. Containment is the
entire clearance for persisting Restricted content, so a single edited line
relocates every future write outside the tier controls, silently and with no
error. See `system/agent-memory-procedure.md`.

Then read the store itself, not just its size. Aggregation is what a per-write
check cannot see: individually ordinary observations can reconstruct reasoning
that no single one states.

If anything was written into a Git working tree this session, confirm the
pre-publish redaction gate actually ran against it. Run `/redaction-gate` if it
did not. "It probably already happened" is the failure mode the gate exists to
prevent.

## Phase 4: Report, do not self-certify

Present what was recorded and what was checked. Do not claim the session is
closed. No completion claim counts as fact until verified by a party other than
the one making it, and self-audit is explicitly excluded as a verification
method. The human makes the close call.

State plainly anything you could not complete and why, rather than leaving it
implied by omission.
