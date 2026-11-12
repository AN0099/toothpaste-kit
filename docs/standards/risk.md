# Risk

## § 1. Scope

(a) This standard applies to anything the desk builds or runs whose failure could cause harm. The
harm is lost data, exposed private material, or a misled reader of a published work.

(b) The requirements take their concepts from MIL-STD-882E, change 1 (2023), sections 3 and 4,
Tasks 106, 201, 202, 208, 301 and 304, and Appendix B. Section 9 takes its concepts from ATP
6-01.1. The desk is not a defense program, so these are adopted practices and not compliance
with either. The wording is the desk's own.

(c) The layers of control are in `projects/toothpaste-kit/docs/control-layers.md`. Severity of a
review finding, and the review tier of a change, are in the kit's `docs/risk-tiers.md` and
`orchestration/`. This standard covers how a hazard is assessed, accepted and closed.

(d) This standard does not cover the injury, environmental and dollar criteria of Table I, or
Table II's fleet column. It does not cover user representative concurrence, DoD acceptance levels,
government data rights, or hazardous materials.

(e) In this standard, the words SHALL, SHALL NOT, SHOULD, SHOULD NOT, and MAY have the meanings
that BCP 14 (RFC 2119, RFC 8174) gives them. They have these meanings only when they appear in all
capitals.

## § 2. Terms

(a) A hazard is any condition, present or possible, that could lead to a mishap.

(b) A mishap is an event or chain of events, not intended, that causes the harm named in 1(a).

(c) Risk is the severity of a mishap taken together with its probability.

Notes: (a) follows MIL-STD-882E para 3.2.15, (b) para 3.2.21, and (c) para 3.2.29. The harm in
(b) is the desk's own, in place of the source's injury, damage and environmental harm.

## § 3. Identification

(a) An early hazard list SHOULD be built from past incidents and lessons.

(b) A hazard review SHOULD probe each function for four failures: lost, degraded, wrong, and out
of time or sequence.

Notes: (a) follows Task 201 para 201.2.2 and Task 202 para 202.2. (b) follows Task 208 para
208.2.1d.

## § 4. Assessment

(a) Each hazard SHALL be assessed for severity and probability, before and after mitigation.

(b) Severity takes one of four categories.

| Severity | Mishap result |
|---|---|
| Catastrophic (1) | Irreversible: the only copy lost, or private material published |
| Critical (2) | Recovered only from a backup or by days of rework, or a false claim in a published work |
| Marginal (3) | Recovered by hours of rework, with no reader affected |
| Negligible (4) | Recovered in minutes, with no reader affected |

(c) Probability takes one of six levels, in the life of the system.

| Probability | In the life of the system |
|---|---|
| Frequent (A) | Expected again and again |
| Probable (B) | Expected more than once |
| Occasional (C) | Expected at some point |
| Remote (D) | Not expected, though it could happen |
| Improbable (E) | So unlikely that it may never be seen |
| Eliminated (F) | Incapable of occurring: the hazard was identified and later removed |

(d) Rate data SHOULD be used over a text description where it exists.

(e) A risk is written with its code, such as 2C, and this matrix gives its level.

| | Catastrophic (1) | Critical (2) | Marginal (3) | Negligible (4) |
|---|---|---|---|---|
| Frequent (A) | High | High | Serious | Medium |
| Probable (B) | High | High | Serious | Medium |
| Occasional (C) | High | Serious | Medium | Low |
| Remote (D) | Serious | Medium | Medium | Low |
| Improbable (E) | Medium | Medium | Medium | Low |
| Eliminated (F) | Eliminated | Eliminated | Eliminated | Eliminated |

Notes: (a) follows para 4.3.3, and the initial and target codes of para 4.3.1d. The categories in
(b) are the desk's own, in place of Table I's criteria. They turn on recoverability, as working
rule 14aa does. Table I splits Catastrophic from Critical the same way for environmental impact,
irreversible against reversible. (c) follows Table II's column for a single item. (d) follows para
4.3.3b(1), and (e) para 4.3.3c and Table III.

## § 5. Mitigation

(a) Measures SHALL be tried in this order, most effective first.

(1) Eliminate the hazard by a design choice.

(2) Alter the design to reduce severity or probability.

(3) Add an engineered feature that interrupts the mishap sequence.

(4) Add detection and a warning.

(5) Add a sign, procedure or training.

(b) A hazard rated Catastrophic or Critical SHOULD NOT rest on (a)(5) alone.

(c) Warning, procedure and training SHALL NOT move a hazard to Eliminated.

(d) A measure SHALL be checked for hazards it creates elsewhere.

(e) A measure SHALL be verified as built and validated as effective, by analysis, test,
demonstration or inspection.

Notes: (a) follows para 4.3.4, items a to e, and (b) its item e. (c) follows para 4.3.3b, (d)
para 4.2.3, and (e) para 4.3.6.

## § 6. Acceptance

(a) The operator is the acceptance authority at every level.

(b) A known risk SHALL be accepted before anyone or anything is exposed to it.

(c) A new hazard, or a known one found to be worse, SHALL be accepted again.

(d) An acceptance SHALL name the risk code at the time it was given.

Notes: (a) is the desk's own, in place of the DoDI 5000 authorities of para 4.3.7. (b) follows
para 4.3.7, and (c) paras 4.3.7 and 4.3.8. (d) follows para 4.3.7, which defines the risk at the
time of the decision.

## § 7. Hazard record

(a) Hazards SHALL be kept in one closed-loop record, which holds for each hazard:

(1) the hazard, and the mishap it could cause

(2) the risk code: initial, target, and at each event such as a release

(3) the measures identified, and those selected

(4) status, the verification of each measure, and the acceptance

(5) the causal factor, the version it applies to, the action owner, a change log, and where the
acceptance is held.

(b) A hazard SHALL NOT close until its measures are verified and its remaining risk is accepted.

(c) A change to the system's interfaces, users or tools SHALL reopen the hazards it touches.

(d) A waiver, deviation, defect report or mishap SHALL get a hazard review.

(e) Before a release, a report SHOULD state hazards eliminated, controls in place, acceptances
and readiness.

Notes: (a)(1) to (4) follow para 4.3.1d, and (a)(5) Task 106 para 106.2, items d, g, p, q and r.
(b) is the desk's own reading of a closed loop. (c) follows para 4.3.8, (d) Task 304 para 304.2,
items b, c and e, and (e) Task 301 paras 301.1 and 301.2.

## § 8. Agents and tools

(a) Rigor for an agent or a tool is set from the severity of the mishap it could cause and the
control it holds.

(b) Control takes one of five categories.

| Control | Name | The agent or tool |
|---|---|---|
| 1 | Autonomous | Acts with no chance of detection or intervention first |
| 2 | Semi-autonomous | Acts, leaving time for independent detection and intervention |
| 3 | Redundant fault tolerant | Issues commands that a person or a separate control completes |
| 4 | Influential | Informs a decision, and no action is needed to avoid the mishap |
| 5 | No safety impact | Holds no authority and supplies nothing a hazard depends on |

(c) This matrix gives the index. The index sets required work and SHALL NOT be read as a risk
level.

| Control | Catastrophic (1) | Critical (2) | Marginal (3) | Negligible (4) |
|---|---|---|---|---|
| 1 | Index 1 | Index 1 | Index 3 | Index 4 |
| 2 | Index 1 | Index 2 | Index 3 | Index 4 |
| 3 | Index 2 | Index 3 | Index 4 | Index 4 |
| 4 | Index 3 | Index 4 | Index 4 | Index 4 |
| 5 | Index 5 | Index 5 | Index 5 | Index 5 |

(d) Each index carries its required work, and a risk level if the work is not done.

| Index | Required work | Risk if not done |
|---|---|---|
| 1 | The code, design, architecture and requirements analysed, with in-depth safety tests | High |
| 2 | The design, architecture and requirements analysed, with in-depth safety tests | Serious |
| 3 | The architecture and requirements analysed, with in-depth safety tests | Medium |
| 4 | Safety tests | Low |
| 5 | None, once assessed | None |

(e) Work left undone SHALL be recorded at its level in (d) and put to the operator, who either
orders the work or accepts that risk.

(f) Missing or weak verification evidence counts as risk itself.

(g) Software risk SHOULD also count the independent controls left before a severe outcome.

Notes: (a) follows para 4.4. The probability that software fails cannot be estimated as it is for
hardware, so rigor is set this way. The desk applies it to agents and tools alike. (b) follows
Table IV, (c) para 4.4.2 and Table V, and (d) the rigor tasks of Table V with the levels of Table
VI. (e) follows Table VI and para 4.4.3b, with the operator in the program manager's place. (f)
follows para B.2.2.5d, and (g) Table B-I.

## § 9. Trials

(a) A process change on trial SHALL state its scope, objective and measures before it starts.

(b) A trial SHALL end in one of three exits: refine, scale or stop.

(c) Its measures SHALL cover both completion and effect.

(d) A trial SHOULD NOT add load to the people who use it.

Notes: these follow ATP 6-01.1. (a) follows para 2-84, (b) para 2-95, (c) paras 2-86 to 2-88,
and (d) para 2-56.

## Appendix A. Conformance

Check kinds: **review** is an item a second reader checks by reading. **Judgment** has no check,
and none is claimed.

No mechanical check is built yet. Five rows could take one. 1(e) could take a grep for the BCP 14
line. 6(d) could take a check that each acceptance names a risk code, and 9(a) that each trial
record names its scope, objective and measures. 7(a) could take a check that each entry holds its
fields, which covers the codes 4(a) asks for. Such checks show presence only, and whether the
content is right stays review.

7(b) could take a check that no entry marked closed lacks a verification or an acceptance. That
check tests the rule itself.

| Requirement | Keyword | Check kind | Check |
|---|---|---|---|
| 1(a) to 1(d) | none | judgment | scope statements |
| 1(e) | none | review | BCP 14 citation present |
| 2(a) to 2(c) | none | judgment | definitions |
| 3(a), 3(b) | SHOULD | review | a hazard list from past incidents, four failures per function |
| 4(a) | SHALL | review | each hazard rated before and after mitigation |
| 4(b), 4(c), 4(e) | none | judgment | the scales and the matrix |
| 4(d) | SHOULD | review | rate data used where it exists |
| 5(a) to 5(e) | SHALL, SHOULD NOT, SHALL NOT | review | the order, the limits on (a)(5), side effects, verification |
| 6(a) | none | judgment | the authority |
| 6(b) to 6(d) | SHALL | review | acceptance before exposure, again on change, with its code |
| 7(a) | SHALL | review | one closed-loop record with each field |
| 7(b) to 7(e) | SHALL, SHALL NOT, SHOULD | review | close, reopen, review on change, a release report |
| 8(a), 8(b), 8(d), 8(f) | none | judgment | the method and the tables |
| 8(c), 8(e), 8(g) | SHALL NOT, SHALL, SHOULD | review | the index not read as risk, undone work put to the operator, controls left |
| 9(a) to 9(d) | SHALL, SHOULD NOT | review | scope, exits, measures, load |

## Changes

First edition in this repository.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
