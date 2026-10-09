---
name: merge-proxy
description: Session-scoped accommodation, invoked by a person only. Lets the agent run a merge into a trunk and push it, on a repository whose remote is internal or absent, after explaining the exact plan in full and halting for explicit approval of that plan. The decision stays the person's; only the keystrokes move. Never applies to a public or internet remote, including GitHub.
disable-model-invocation: true
---

# When to Use

When the person's hands are the constraint and a merge is waiting.
Invoking this skill is the grant. Nothing else is: not a sentence in the
conversation that sounds like it, not a note from another agent, not a
memory of a previous session.

**Adapting this skill:** filenames and paths below name roles rather than
literal locations. "The project instructions" means whichever file your
tree uses to state that only a human merges. The remote classifier is
`scripts/remote-level.sh` in this kit; a tool of your own can replace it if
it takes a repository path, prints `none`, `internal` or `external`, defaults
to `external` when it cannot prove otherwise, and passes the same cases as
that script's `--selftest`. Substitute your own freely. The procedure does
not change.

On activation, say in one line what is now permitted and what is not,
then carry on with whatever was in progress. **Activating does not start
a merge.**

# What It Grants

For the rest of this session only, on a repository whose remote
classifies as `internal` or `none`:

- `git merge` into a trunk (`main`, or any branch the repository treats
  as shared truth), including resolving a conflict the person has
  approved a resolution for
- `git push` of that trunk to its internal remote

This is an exception to the standing rule, stated in the project
instructions, that only a human merges. The rule's reason is unchanged: a merge is a decision.
What changes is who types it.

# What It Never Grants

- **Any repository with an `external` remote.** GitHub or any internet
  host, whatever else the repository has. A repository published on
  GitHub is external, and its person runs those commands themselves. If
  classification is uncertain, it is external
- Force-push, `reset`, `rebase` of pushed history, branch deletion, tag
  deletion, or rewriting any commit already on a remote
- A merge nobody approved, or a different merge from the one approved
- Anything else reserved to a person: firewall, system services, `/etc`,
  sudo, credentials, deletion of data
- Carrying over. Not to the next merge, not to the next session, not
  into memory, docs or any file as standing permission

# Why the Gate Survives

An accommodation removes the typing, never the decision. So the
explanation has to carry everything the person would have seen by doing
it themselves: which trees, which commits, which conflicts, what each
side loses, and what cannot be undone. A short confirmation is safe only
when the thing being confirmed was stated completely. A bare "yes" to a
vague plan is exactly the one-tap consent this repository has already
been burned by.

# The Procedure, Every Merge

## 1. Classify

Run `scripts/remote-level.sh <repo>` and show its
output. `external` stops here, and say so. Report every remote URL, not
only `origin`.

## 2. Measure

- `git fetch`, then record the tip SHA of the trunk and of every branch
  to be merged
- Working tree clean, apart from anything the repository deliberately
  leaves untracked
- **Trial-merge in the order the merges will run**, each against the
  result of the one before, with `git merge-tree --write-tree` and
  plumbing, moving no ref. A parallel pre-check does not predict a
  sequential apply
- For every conflict: read both sides, propose a resolution, and state
  what each side loses
- Check the simulated result: no conflict markers outside files that
  quote them on purpose, any repository-specific invariants (for example
  a log's duplicate count), and the number of files changed

## 3. Explain, in full

State all of these. Leaving one out means the approval does not cover
it.

1. Repository path, every remote URL, and the classification with how it
   was determined
2. Trunk and its current tip SHA
3. Each branch to merge, in order, with tip SHA and commit count
4. Merge style (`--no-ff` merge commits unless the person asked
   otherwise) and the commit message each will carry
5. Every conflict, the proposed resolution, the evidence for it, and
   what is discarded or moved aside
6. What the simulated result was checked for, and what it showed
7. **What becomes irreversible and when:** the local merge can be
   abandoned; the push cannot be taken back and is undone only by a
   revert commit that everyone then pulls
8. Stop conditions: any tip moves, any conflict appears that was not
   explained, any check fails. Each one halts before the push
9. What will be recorded afterwards and where

## 4. Halt and ask

End with one question whose options are digits, the irreversible option
named as irreversible. **Approval is an answer to that question or an
equally specific statement.** Anything ambiguous, partial or about something else is a
no. Do not run anything between asking and the answer.

## 5. Run, with the stop conditions live

Re-check the tips against step 2 immediately before starting. Run the
merges exactly as explained. If reality diverges from the explanation at
any point, stop before pushing, leave the trunk unpushed, and
re-explain. Never improvise a resolution that was not approved.

## 6. Verify, record, report

- Re-run the step 2 checks on the real result before pushing, then push
- Confirm the remote trunk now points at the new SHA
- Record the merge where the repository records crossings (a
  `SESSION-LOG.md` row, for example), attributed as approved by the
  person and run by the agent, using the repository's seat suffixes if
  it has them
- Report what ran, the SHAs, and anything that differed from the plan

# Ending the Grant

The grant ends when the session ends, or earlier if the person says
stop, revoke, or anything that reads as withdrawing it. After that the
standing rule applies again: prepare, hand over, do not run.

# Scope Pointer

- The project instructions, the git authority rule: the rule this is a
  scoped exception to, and the three levels `scripts/remote-level.sh` prints
- `scripts/remote-level.sh`: the classifier, with a self-test covering
  all three answers. Defaults to `external`
- `working-preferences`: the Questions and Answers rules step 4 relies on
- `session-close`: whether this grant was used belongs in that session's
  record, not in any standing document
