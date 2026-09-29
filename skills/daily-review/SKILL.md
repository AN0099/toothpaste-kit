---
name: daily-review
description: Once-a-day pass over the task board's lanes. Clarifies the Inbox to empty, checks each open task's priority quadrant, carries unfinished Doing work forward with its count, offers the Verify lane for close, and sets the order of Next and the day's Most Important Task. A tool prepares every list; the person decides every move, and nothing moves before they answer. Invoke once a day, after the dashboard if one is run. Does not replace the dashboard, which is the state view and may run any number of times.
disable-model-invocation: true
---

# When to Use

Once a day, before the first task is pulled from Next. Invoked by a person, never by an agent.

**Adapting this skill:** filenames below name roles rather than literal paths. It assumes a task
queue with lanes (below) and a **lane-board tool**: one command that prints every task grouped by
lane, with its priority, rank, assignee, carry count, due date and consequence, blocker and next
action, orders Next by quadrant and then rank, validates the queue before printing, and ends with a
coverage line naming the fields it did not read. **Check that line before starting**: a field this
review needs and the tool does not print is read by an ad hoc command, which is the failure the tool
exists to prevent, so extend the tool instead. `CLAUDE.md` names the
command. A tree without such a tool builds it before running this skill, for the reason `orient`
gives: a model re-deriving lanes from raw JSON is doing a script's job, and doing it inconsistently.

## The lanes

| Lane | Holds | Leaves by |
|---|---|---|
| Inbox | captured, not yet clarified | this review |
| Someday/Maybe | considered and parked | a monthly review, if the tree runs one |
| Next | ready to start, in order | a seat pulling its top task |
| Waiting | blocked on a named person, task or event | the blocker clearing |
| Doing | pulled; at most one per seat | finishing, to Verify |
| Verify | deliverable exists and a second party checked it | the person's word, to Done |
| Done, Archive | accepted; out of the board | a monthly review, if the tree runs one, archives |

**Priority is an Eisenhower quadrant**: Do, Decide, Delegate, Delete. **Urgent is read, not felt**:
a task is urgent only when it carries a due date and a stated consequence of missing it. Important
means it serves the long-term goals the tree has written down; where none are written, importance
is the person's call, and the review says so rather than inventing a basis.

## Phase 1: Observe

Run the lane-board command once and read all of it, including the coverage line. If it fails
validation, stop and report the fault: a board drawn from an invalid queue is a claim about the
queue, not the queue.

## Phase 2: Propose, lane by lane

For each step, a short table of proposed moves, one row per task, each with a one-line reason. **Do
not write anything yet.**

1. **Inbox to empty.** Each item gets a destination: Next (with a quadrant and a next action),
   Waiting (with its blocker), Someday/Maybe, a child of an existing task, or trash. Work that takes
   under two minutes is proposed as done now and noted in the capture file, not queued.
2. **Doing, carried.** Each task still in Doing from a previous day: carry it (it stays, and its
   carry count rises by one), move it back to Next, or move it to Waiting with a blocker. A task
   bumped by an interruption returns to the top of Next and its count does not rise. **A count of
   three or more is said aloud**: a task carried all week is a question for a weekly review, and
   the daily review names it so the question is not first asked there.
3. **Verify, offered for close.** Each task in Verify, with the second-party check its note records.
   Offer the close; never close it. A task whose note records no second party does not belong in
   Verify, and that is a finding, not a close.
4. **Quadrant check.** Every open task (Inbox, Next, Waiting, Doing) without a quadrant gets a
   proposed one. A task marked urgent with no due date or no consequence gets a proposal to drop to
   Decide, in whichever open lane it sits: a Waiting task keeps its quadrant when it returns to Next.
5. **Next, ordered.** Do first, then Decide, each in the order proposed. **The Most Important Task**
   is the top Do task for the person's own seat; when the person's seat has no Do task in Next, it
   is the top of Next for that seat, and the review says which rule chose it. Name it with its next
   action. For each agent seat whose Doing is empty, name its first pull, or say that Next holds
   nothing for that seat.
6. **Next actions.** Every task in Next, Waiting or Doing carries one concrete next action, since a
   task moves between lanes by that action. Propose one for each task the board shows without it.
   For a Waiting task, the action is whatever clears the blocker, and it names who takes it.

Keep each table to the tasks the step moves. A step with nothing to propose is one line saying so.

## Phase 3: Ask, then stop

Chat output, not a document: the dashboard's phase 0 applies here too. End with questions. One per
step that has proposals, each accepting that step's table as written; the person answers exceptions
by task ID in prose. Then stop.

## Phase 4: After the answers

Apply exactly the accepted moves, in one scripted edit that asserts each task's current lane before
changing it, so a task that moved since the board was read fails loudly instead of moving twice.
Write the accepted order of Next as each task's rank, 1 upward, and clear the rank of a task
leaving Next. Record each move in the task's note with the date and "daily review". Run the lane-board command
again and show the lanes that changed. **Nothing moves on a task the person did not answer**; an
unanswered row stays where it was and is listed as unanswered.

# Scope Pointer

- `daily-dashboard`: the state view. It checks the standing files and working trees against their
  claims; this reads the board and moves tasks. Run it first when both are wanted.
- `weekly-review` (not in this kit): Waiting's blockers, carry-over by count, the Done lane, and one Decide task
  scheduled so the important is not starved by the urgent.
- `monthly-review` (not in this kit): Someday adopted or rejected, and archive candidates chosen by the person.
- `session-close`: updates the standing files at the end of a session. A move made here is already
  in the queue and does not wait for it.
