# CHANGELOG

## v2

**Trash never satisfies a dependency.** v1 let steps 1 and 2 trash a task that an open task
depended on, while the archive counts an archived predecessor as complete, so the dependent read as
unblocked by work nobody did. A task with an open dependent is no longer proposed for trash, and
phase 4 checks that no dependency resolves through a trash entry. Also corrected: v1 called this
the only procedure that removes anything from the board, which the daily review's trash door for
unclarified Inbox items contradicted.

## v1 (initial)

The once-a-month pass, the last of the reviews `daily-review` named and the kit did not ship. The
daily and weekly passes keep the board honest about what is moving; neither removes anything from
it, so Someday/Maybe and Done only grow.

Three things are deliberate.

**Only this review archives a task the board has been holding.** A tool lists archive candidates by two
mechanical conditions; the person chooses. A Done task the tool does not list is never proposed,
and a disagreement with the tool is reported as a finding about the tool.

**Age alone never rejects an idea.** A parked item is rejected when it stops being relevant, and
the review says what changed. Otherwise an old list empties by attrition, which is deletion with
no decision behind it.

**The archive has two doors.** Reference for work that happened, trash for work that will not,
marked irrelevant rather than done, so the archive never records work nobody performed.
