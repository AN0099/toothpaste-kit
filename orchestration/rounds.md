# Rounds: delegated work, checked and decided

A round is the unit in which the lead hands work to other seats, collects what comes back, has it
checked by someone other than its author, and puts the result in front of the operator. It gives
every delegation the same shape, and ties each step to the operator's decision, the only point in
the loop where a person decides. Roles are defined in [`ROLES.md`](ROLES.md).

Notes travel as files over a channel each installation chooses. For example, each seat has its own
branch in one shared repository, and a seat writes to the other seat's inbox directory on its own
branch. In that example, **checking mail** means fetching the other seats'
branches and reading what is new in your inbox there. A report is a file in the lead's inbox, on the
reporting seat's branch. Where a surface needs a structured message instead, the header and JSON
relay format is in [`protocol.md`](protocol.md).

## The round

A round is **one task, its dispatches and their replies**. Rounds are numbered `r1` upward, never
reused, and a round spans as many operator exchanges as it takes. The lead opens every message about
a round with the step it is on and the report it concerns (`Round step: r12, collect, report 2`; the
step-line format is a recommendation), so the operator never has to hold the structure in mind.

A round opened while another is open is an error. A re-check after fixes is **the open round's next
report**, never a new round.

| Step | Runner | What |
|---|---|---|
| 1. Collect | lead | Read every reply from the seats' branches, never from memory of what was assigned |
| 2. Orient | lead | Sort each item: verified, reported, blocked on a person, or a finding nobody was asked for |
| 3. Plan | lead | One row per seat: the task as done-looks-like, the files it owns, the material shipped with it, a timebox, a verifier who is not the author |
| 4. Decide | operator | Approves, amends or declines the plan, the merges and the decisions. Nothing is dispatched and nothing merges until the operator answers; silence is not an answer |
| 5. Dispatch | lead | One note per seat carrying only that seat's row and material; the round's row in the register gets its dispatch time |
| 6. Work | seats | Check mail, acknowledge before working, surface a block the moment it happens, then report |

**The steps repeat inside a round.** Each report is collected and its findings reproduced, the operator
decides what is fixed, and the lead re-dispatches; the loop runs until the close condition holds.

**Authority comes from a seat's own operator**, never from the lead's note alone
([`ROLES.md`](ROLES.md)). The note carries the task; the seat's operator approving it is what lets the
seat act.

**A finding that touches a [control](../docs/control-layers.md) outranks everything else in the
round.** Reproduce it before ranking it, because a finding is a claim.

## Reports and findings

`r12` is a round, `r12.2` its second report, and `r12.2.3` that report's third finding. A finding is
never written `r12.3`, which reads as a report.

A report says what was done, what was checked and how, and **what the check does not cover**. A check
that states no coverage is not a check.

## Severity

Every finding carries one of three grades. The verifier proposes it as evidence; the lead reproduces
the finding, and **the lead's grade stands**.

| Grade | Meaning | Effect on the round |
|---|---|---|
| major | A wrong result, or a broken rule, on input that ordinary use produces | Blocks the close; fixed and re-checked as the next report |
| minor | Wrong only on unusual input that real use could still produce, with a small and visible consequence; or a gap a reader would trip on | Fixed before the close by default; the operator may accept it instead |
| nit | Changes no real outcome: wording, a contrived input, or a test gap where the code is right | Never blocks a close; fixed by the lead or accepted, at the operator's choice. A lead's fix is listed in the next dispatch, so the verifier sees it; a fix made after the last report goes in the next round's dispatch, and that round's verifier checks it |

A dispatch may set its own close condition, such as "the round closes when the next report has no
finding above nit". When a grade is in doubt, the higher one stands until the lead has reproduced the
finding.

## Verification

**Work is verified only when someone other than its author has checked it.** The author's own run
supplies context the author does not notice supplying, so it cannot find what a cold reader finds.

**A tool or a written procedure is verified only when a second party has run it**, without the
author's context, with the questions they had to ask recorded as checks. Reading it is not running it.

Two clauses belong to the rule:

- **"Neither seat can check this independently" is an honest result**, recorded as the round's
  outcome. Forcing a weaker check to fill the field makes a rule that cannot fail, which is not a
  control.
- **A gate that refuses the verifier is a defect in the round**, not an inconvenience beside it. Name
  the gate in the round's result.

## Closing a round

A round closes when every seat has reported or its **timebox** (the time a dispatch allows) has
passed, **and no finding blocks it**: no major is open, and no minor is unfixed or unaccepted. Where a
dispatch sets its own close condition, that condition adds to this one for a seat that reports. The
lead writes the round's row in the **register**: one table row per round, with its number, dispatch
time, seats, task, state and result. **An unanswered seat is recorded as unanswered, not waited on**;
its row carries into the next plan.

**A close is finished only when the next plan is in front of the operator**, in the same message.
Every plan lists what it carries and checks the previous plan's carried items against its own rows,
so nothing parked "for the next round" is lost.

## Context at the boundary

Each seat writes one capture to its [capture file](../docs/glossary.md#c) at each session close,
using the [`session-log`](../skills/session-log/SKILL.md) questions, not one with every report. A person
invokes `session-log`; in an unattended loop, where no person is there to, an agent answers the
`session-log` questions itself.
A seat logs before it compacts. A compaction inside an open round is recorded in that round's row in
the register. After a compaction, a seat orients from the round's note, its last capture and its
branch's log, never from the summary alone.

The lead's context grows faster than a seat's, since it reads every report. For example, an
installation might set the lead to capture at a round close at least every three rounds, or once its
context passes 40% of the window, and to start no new work past 60%.

## What rounds deliberately do not add

- **No standups, ceremonies or estimates.** The round is a timebox, the plan table a board, a block
  row an impediment; nothing whose cost does not scale down to a few seats.
- **No agent-to-agent channel.** Seats never message each other directly; a verifier assignment is a
  row in the lead's plan.
- **No new tooling until a step has been done by hand twice.**

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
