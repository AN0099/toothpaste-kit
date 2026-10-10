---
name: monthly-review
description: Once-a-month pass over the parts of the task board that only a long interval shows. Adopts or rejects each Someday/Maybe item, asks whether each long-stalled Waiting task is still committed work, and lets the person choose which of the tool's archive candidates leave the board, and by which door. A tool prepares every list; the person decides every move, and nothing moves before they answer. Invoke once a month, after that week's weekly review. Does not replace the weekly review, which chases blockers and reads the Done lane.
disable-model-invocation: true
---

# When to Use

Once a month, on a fixed day, after that week's weekly review. Invoked by a person, never by an
agent.

**Adapting this skill:** filenames below name roles rather than literal paths. It assumes the same
task queue, lanes and **lane-board tool** as `daily-review`, and reads its lanes table from there
rather than restating it. It also assumes an **archive**: a separate store that archived tasks move
into with their full record, which the lane-board tool reads when it resolves a dependency, so an
archived predecessor that left as reference still counts as complete. `CLAUDE.md` names the command and the archive.
**Check the tool's coverage line before starting**: this review needs each Someday item's added
date and note, each Waiting task's blocker and note, and the tool's list of archive candidates.
A field the tool does not print is a reason to extend the tool, not to read the queue by hand.

## Why a monthly pass exists

The weekly review keeps the board honest about what is moving. Two things it leaves alone on
purpose, because a week is too short to judge them. **Someday/Maybe fills and is never read**:
parking an idea is cheap, and a list nobody reviews stops being a list of options and becomes a
place ideas go to be forgotten. **Done fills and never empties**: every finished task stays in view,
and a board that shows everything ever finished hides what is open. This pass reads both, once a
month, and is the only procedure that archives a task the board has been holding. (The daily
review's trash door is for Inbox items not yet clarified.)

## The archive's rules

These hold whatever the person answers, and the proposals in phase 2 never break them.

1. **Nothing is archived except by a review.** A tool may list candidates; the person moves them.
2. **A Done task is an archive candidate when no open task depends on it and no open flag cites
   it.** Both conditions are mechanical, so the tool lists the candidates. A Done task the tool
   does not list fails one of them, and is not proposed. If the review thinks the tool is wrong
   about one, that is a finding about the tool, reported, never a move.
3. **Age alone never rejects.** An idea that is only parked stays in Someday/Maybe however old it
   is. It is rejected when it is no longer relevant to the work, and the review says what changed.
4. **The archive has two doors.** A Done task leaves as **reference**: it happened and may be cited.
   A rejected proposal, or a task no longer worth doing, leaves as **trash**, marked irrelevant
   rather than done, so the record never claims work that was not performed.
   **Trash never satisfies a dependency.** A task that an open task depends on is not proposed
   for trash; its row names the dependent and proposes resolving that first, by dropping the
   dependency or rejecting the dependent too, in the same answer. Otherwise the dependent would
   read as unblocked by work nobody did.
5. **An archived task keeps its full record**, with the date it left the board, the review that
   moved it and the door it left by.

## Phase 1: Observe

Run the lane-board command once and read all of it, including the coverage line and the archive
candidates. If it fails validation, stop and report the fault. Read the notes of the Someday items
and Waiting tasks this review proposes to move; earlier reviews recorded their moves there, and the
notes are the only record of how a task got where it is.

## Phase 2: Propose, lane by lane

For each step, a short table of proposed moves, one row per task, each with a one-line reason. **Do
not write anything yet.** A step with nothing to propose is one line saying so.

1. **Someday/Maybe, decided.** Every item in the lane. Propose one of: **adopt** it into Next, with
   a quadrant and a concrete next action; **keep** it parked, with one line on why it is still worth
   keeping; or **reject** it to the archive as trash, with what changed to make it irrelevant (rule
   3; and rule 4, never while an open task depends on it). An item adopted here enters Next's order through the next daily review.
2. **Waiting, stalled.** Every Waiting task that weekly reviews have chased more than once with no
   change to its blocker, as their notes record. The weekly review asks whether the blocker is still
   true; this asks whether the task is still committed work. Propose one of: keep it Waiting, with
   the blocker restated and a next action naming who takes it; move it to Someday/Maybe, because
   it is worth keeping and nobody is committed to it; or archive it as trash, because it is no
   longer worth doing (rule 4: never while an open task depends on it).
3. **Done, archived.** Every candidate the tool lists, and only those (rule 2). Propose one of:
   archive it as reference, or keep it in Done with the reason, such as a task about to be cited by
   work that is not yet a task. A long list is normal at the first monthly review and is not a
   finding.

## Phase 3: Ask, then stop

Chat output, not a document. End with questions: one per step that has proposals, each accepting
that step's table as written, and the person answers exceptions by task ID in prose. Then stop.

## Phase 4: After the answers

Apply exactly the accepted moves, in one scripted edit that asserts each task's current lane before
changing it, so a task that moved since the board was read fails loudly instead of moving twice.
A task adopted into Next takes the bottom rank of its quadrant unless the person names another.
An archived task moves to the archive with its full record, the date, "monthly review" and its door
(rule 5); a trash entry is marked irrelevant and never complete. Record each move that stays on the
board in the task's note with the date and "monthly review". Run the lane-board command again:
it must validate, the archived count must rise by exactly the number of accepted archive moves,
every dependency on an archived task must still resolve, and none may resolve through a trash
entry. Show the lanes that changed. **Nothing
moves on a task the person did not answer**; an unanswered row stays where it was and is listed as
unanswered.

# Scope Pointer

- `weekly-review`: the once-a-week pass. It chases Waiting's blockers, names carried work and reads
  the Done lane back. A Waiting task it has chased more than once with no change reaches step 2
  here; a task it reads in Done reaches step 3 only once the tool lists it.
- `daily-review`: the once-a-day pass. It empties the Inbox and orders Next, which is where a task
  adopted here takes its place.
- `daily-dashboard`: the state view. It checks the standing files and working trees against their
  claims; this reads the board.
- `session-close`: updates the standing files at the end of a session. A move made here is already
  in the queue and does not wait for it.
