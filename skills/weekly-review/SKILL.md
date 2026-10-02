---
name: weekly-review
description: Once-a-week pass over the task board's slower lanes. Chases each Waiting task's blocker, names every task carried in Doing by its count, reads the week's Done lane back against what was planned, and schedules one important task that nothing urgent is forcing. A tool prepares every list; the person decides every move, and nothing moves before they answer. Invoke once a week, after a daily review. Does not replace the daily review, which empties the Inbox and orders Next.
disable-model-invocation: true
---

# When to Use

Once a week, on a fixed day, after that day's daily review. Invoked by a person, never by an agent.

**Adapting this skill:** filenames below name roles rather than literal paths. It assumes the same
task queue, lanes and **lane-board tool** as `daily-review`, and reads its lanes table and its
definition of urgency from there rather than restating them. `CLAUDE.md` names the command. **Check
the tool's coverage line before starting**: this review needs each task's blocker, carry count, due
date, consequence and quadrant, and for a Done task its close date and verification, and a field the tool does not print is a reason to extend the tool,
not to read the queue by hand.

## Why a weekly pass exists

The daily review handles what arrives and what is next. Three things move too slowly for it to see.
A blocker named on Monday is still named on Friday, and nobody has asked whether it is still true.
A task carried one day at a time never looks stuck on any single day. And because urgency is read
from due dates, the Decide quadrant never forces itself onto the day: each important task loses to
something urgent every morning, and is never refused, only postponed. This pass looks at all three
on purpose, once a week, so the daily pass can stay short.

## Phase 1: Observe

Run the lane-board command once and read all of it, including the coverage line. If it fails
validation, stop and report the fault. If the week's daily reviews recorded their moves in each
task's note, as `daily-review` asks, read the notes of the tasks this review proposes to move; they
are the only record of how a task got where it is.

## Phase 2: Propose, lane by lane

For each step, a short table of proposed moves, one row per task, each with a one-line reason. **Do
not write anything yet.** A step with nothing to propose is one line saying so.

1. **Waiting, chased.** For each Waiting task, ask whether its blocker is still true, and who
   clears it. Propose one of: keep it Waiting with the blocker restated and a next action naming who
   takes it; return it to Next because the blocker has cleared; or, where the blocker is a person
   who has not answered, a next action to ask them again by a named day. A blocker that names no
   person, task or event is a finding: it cannot clear, so it is not a blocker.
2. **Doing, by count.** Every task in Doing whose carry count is three or more, with its count and
   its next action. Propose one of: split it, so the part that can finish this week is a task of
   its own; return it to Next, freeing the seat; or keep it, with the reason it is still the right
   work. A task carried all week is a plan that did not survive contact, and the question is which
   part of the plan was wrong, not who was slow.
3. **Done, read back.** Every task that reached Done since the last weekly review. For each, say
   whether its verification, as written when the task was added, was the check that actually
   closed it. A close that rested on a different check is not reopened here; it is named, so the
   next task written in that shape states its verification more honestly. Then list anything the
   week finished that has no task, and propose recording it, so the Done lane is a true record of
   the week.
4. **One important task, scheduled.** Choose one Decide task from Next and propose a day this
   week on which it is the person's first work. Record the day in its next action and its note,
   **never as a due date**: a due date with a consequence makes a task urgent, and turning an
   important task into an urgent one to get it done is the starvation this step exists to stop.
   Choose by the long-term goals the tree has written down; where none are written, the choice is
   the person's, and the review says so rather than inventing a basis.

## Phase 3: Ask, then stop

Chat output, not a document. End with questions: one per step that has proposals, each accepting
that step's table as written, and the person answers exceptions by task ID in prose. Then stop.

## Phase 4: After the answers

Apply exactly the accepted moves, in one scripted edit that asserts each task's current lane before
changing it. A task returning to Next takes the bottom rank of its quadrant unless the person names
another. Record each move in the task's note with the date and "weekly review". Run the lane-board
command again and show the lanes that changed. **Nothing moves on a task the person did not answer**;
an unanswered row stays where it was and is listed as unanswered.

# Scope Pointer

- `daily-review`: the once-a-day pass. It empties the Inbox, orders Next and names the day's Most
  Important Task. This skill does none of those, and a task scheduled here enters Next's order
  through the next daily review.
- `daily-dashboard`: the state view. It checks the standing files and working trees against their
  claims; this reads the board.
- `monthly-review` (not in this kit): Someday adopted or rejected, and archive candidates chosen by
  the person. A Waiting task chased here more than once with no change is a candidate for it.
- `session-close`: updates the standing files at the end of a session. A move made here is already
  in the queue and does not wait for it.
