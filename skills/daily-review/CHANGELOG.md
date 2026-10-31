# CHANGELOG

## v5

Step 5 orders Next as Do first, then Decide, in the board's order. It also said "within each
serves group", which the lane board does not sort by, so an agent following it proposed an order
the board would not show.

## v4

Step 5 names the Most Important Task by the lane board's rule: the person's first task in Next,
in the order the step proposes, which the board shows and marks in words once phase 4 writes the
ranks. It had said the top Do task, falling back to
the top of Next, so a Do task later in Next could jump ahead of the person's first task.

## v3

The lanes table and Scope Pointer name `monthly-review` as part of the kit, now that it ships. No
change to the procedure.

## v2

The Scope Pointer names `weekly-review` as part of the kit, now that it ships. No change to the
procedure.

## v1 (initial)

The once-a-day lane pass, split out of `daily-dashboard`. The dashboard had become two things run
at different rates: a state view wanted several times a day as a thorough reorientation, and a
review of the task board wanted once. Run together, the board review was repeated every time the
state was wanted, or skipped with it. Now the dashboard keeps the state view, and this skill takes
the board, in the shape of a weekly and a monthly review, which the kit does not ship.

Three things are deliberate.

**A tool prepares every list; the person decides every move.** The skill proposes, asks and stops.
Moves are applied only after the answers, in one scripted edit that checks each task is still where
the board showed it. A review that moves tasks on its own has chosen the day's work for the person,
which is the failure `daily-dashboard` already guards against.

**Urgency is read from the task, not felt.** A task is urgent only with a due date and a stated
consequence. Without that rule everything drifts into Do, and the quadrant stops sorting anything.

**The lane-board tool is named by its contract, not its path.** A skill that names one tree's script
ships half of itself: the judging half arrives and the observing half does not. The skill says what
the tool must print, and the tree's `CLAUDE.md` names the command.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
