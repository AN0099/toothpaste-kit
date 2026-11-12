# Continuity

## § 1. Scope

(a) This standard applies to any role or seat that passes to someone else, for an absence or a
reassignment.

(b) The requirements take their concepts from ATP 6-01.1 Appendix I for the role, and from
DI-HFAC-81399B for each task. The desk is not a Federal agency, so these are adopted practices and
not compliance with either. The wording is the desk's own.

(c) This standard does not cover rank, unit or Army form fields, or a delivery deadline for the
package.

(d) In this standard, the words SHALL, SHALL NOT, SHOULD, SHOULD NOT, and MAY have the meanings
that BCP 14 (RFC 2119, RFC 8174) gives them. They have these meanings only when they appear in all
capitals.

## § 2. Package

(a) A package SHALL let a person who has not done the work finish it.

(b) A package SHALL name people by function.

(c) A credential SHALL NOT appear in a package.

(d) A package SHALL say where access is requested.

Notes: (a) follows ATP 6-01.1 para I-1, and (d) in part para I-4, which names accounts and special
permissions. (b) and (c) are the desk's own. Paras I-3 and I-8 ask for full names, and (b) asks
for the function instead.

## § 3. Role

(a) Each package SHALL hold these parts.

| Part | Holds |
|---|---|
| Position | Title, duties, added duties, who reviews the work |
| Operational knowledge | Mission, processes owned, accounts needed, where the procedures live |
| Current work | The 3 to 5 projects in hand, each with its deadline and point of contact |
| Calendar | Near and far events to attend or create |
| Equipment | What the role is responsible for, its location and status, and what is to be secured |
| Training | Skills the work needs, and any training scheduled |
| Leader guidance | Known concerns, daily checklist, weekly rhythm, products due |
| Out-going contact | How to reach the out-going person with later questions, and a sign-off |
| In-coming checklist | What the in-coming person confirms received |

(b) The out-going person SHALL sign the package.

Notes: the parts in (a) follow ATP 6-01.1 paras I-3 to I-9. Position is para I-3, the next three
parts I-4, Equipment I-5, Training I-6, Leader guidance I-7, Out-going contact I-8, and In-coming
checklist I-9. (b) follows para I-1.

## § 4. Critical tasks

(a) A critical task is one whose failure would likely raise cost or lower reliability,
efficiency, effectiveness, or safety.

(b) The package SHALL state the criteria that made each task critical, so that the list stays
short.

(c) Each critical task SHALL have these fields.

| Field | Para |
|---|---|
| Preconditions before starting | 3c(1) |
| Tools and equipment, and when they are available | 3c(19) |
| Job aids, training and references | 3c(23) |
| Information required, and information available | 3c(2), (3) |
| **Information the task needs that no document or system gives** | 3c(4) |
| The decisions open in the task, and the action each leads to | 3c(7), (8) |
| Performance standard: time, accuracy, completeness | 3b(6) |
| Time available, sequence, and what runs at the same time | 3b(9) to (11) |
| Who performs it, and what skills that takes | 3b(15), 3c(20) |
| Communications and the people involved | 3c(24), (26) |
| Feedback showing the action worked or failed | 3c(18) |
| How the task runs when part of the system has failed | 3b(3) |
| Probability and consequence of error, and how to recover | 3c(21), (22) |
| Hazards | 3c(25) |

(d) A role with physical work SHALL add the fields for body movement, workspace, and protective
equipment that apply to it.

Notes: (a) follows DI-HFAC-81399B, Use/relationship, and (b) its para 3a. The purpose clause in
(b), that the list stays short, is the desk's own. The Para column gives the DI para behind each
field in (c), and (d) follows paras 3c(10), (12), (13), and (30). The bold field is the desk's own
emphasis: it holds what a person knows and no document says, so a handover loses it most often.

## § 5. Degraded operations

(a) Each channel the role depends on, for messages, mail, and access, SHALL have a stated order of
four places: primary, alternate, contingency, and emergency. Each place SHALL carry its reason.

(b) A package SHALL say how a report travels when the primary is down.

(c) Each role SHALL state its order of succession and its standing aim before any absence. The
next seat can then work to the aim without orders.

(d) A worker that loses contact SHALL have a stated place to report and a stated way to learn what
changed.

(e) Each signal that reports health SHALL have a separate alarm that fires when the signal itself
cannot be sent or believed. A health signal can fail by staying green.

(f) Each degraded mode and fallback SHALL be checked and exercised on a stated schedule. One never
run is an assumption.

Notes: (a) and (b) follow ATP 6-01.1 para 3-62. In (c), the order of succession follows Figure
C-1, Annex Q para 5.a.(2), and working to the aim without orders follows para 1-41. Stating the
aim before an absence is the desk's own. (d) to (f) cover a seat lost with no handover and no
contact. They cite no source and are the desk's own.

## § 6. Recurring work

(a) Before a recurring meeting, report, or review is scheduled, it SHALL state its purpose,
inputs, outputs, what it feeds, and where past runs are kept.

(b) It SHOULD be judged against that statement later.

Notes: (a) follows ATP 6-01.1 para 3-12 for a meeting, and para 3-52 for what a report feeds. That
para names it as the person to receive the report. Where past runs are kept is the desk's own. (b)
follows para 3-12, which tests a meeting's usefulness.

## Appendix A. Conformance

Check kinds: **review** is an item a second reader checks by reading. **Judgment** has no check,
and none is claimed.

No mechanical check is built yet. Five rows could take one. 1(d) could take a grep for the BCP 14
line, and 2(c) a scan for credential patterns across each package. 3(a), 4(c) and 5(a) could take
a check that the nine parts, the 14 fields and the four places are present. Such a check shows
presence only, and whether the content is right stays review.

| Requirement | Keyword | Check kind | Check |
|---|---|---|---|
| 1(a) to 1(c) | none | judgment | scope statements |
| 1(d) | none | review | BCP 14 citation present |
| 2(a) | SHALL | judgment | whether a newcomer could finish the work |
| 2(b) to 2(d) | SHALL, SHALL NOT | review | people by function, no credential, access requests located |
| 3(a), 3(b) | SHALL | review | the nine parts present, and the sign-off |
| 4(a) | none | judgment | definition |
| 4(b) to 4(d) | SHALL | review | criteria stated, the fields present per task |
| 5(a), 5(b) | SHALL | review | an order of four per channel, each with its reason |
| 5(c) to 5(f) | SHALL | review | succession, a report point, a second alarm, an exercise schedule |
| 6(a) | SHALL | review | the statement exists before the first run |
| 6(b) | SHOULD | review | a later run judged against it |

## Changes

First edition in this repository.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
