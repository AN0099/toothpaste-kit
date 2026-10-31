# Glossary

The terms of art this repository uses, one entry each, in alphabetical order.
Each entry gives the short meaning and links to the file that defines the term
in full. Where this page and the linked file differ, the linked file governs.

Commands in the command vocabulary are listed once, under
[command vocabulary](#c), rather than one entry each; their full definitions
are in [`working-preferences`](../skills/working-preferences/SKILL.md).

[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) ·
[H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [N](#n) ·
[O](#o) · [P](#p) · [Q](#q) · [R](#r) · [S](#s) · [T](#t) · [U](#u) ·
[V](#v) · [W](#w)

## A

- **Adapting this skill**: the paragraph near the top of a procedure skill saying its filenames name roles, not literal paths, and that a tree substitutes its own. Each procedure skill carries one, as [`daily-review`](../skills/daily-review/SKILL.md#when-to-use) does; [standing documents](standing-documents.md#adapting-this) lists the roles the files play.
- **Aide**: the role that verifies and assists. A second party with its own working copy and context and no stake in the lead's work being right. Its verdict is evidence for the operator's decision, never the decision. See [roles](../orchestration/ROLES.md#aide).
- **Alarm**: a control layer that notices a condition outside normal and hands the judgment to a person without blocking anything. Alarms share a budget: each one added lowers the value of the rest. See [control layers](control-layers.md#3-alarms-the-machine-notices-the-human-decides).
- **Answer grammar**: how a reply to a question block is written. Segments separated by `;`, each `<code> qN`, as in `f q1; 2 q2; d q3`. Prose in a segment, or after `pr:`, outranks a conflicting code, and `(c: ...)` attaches a comment. See [`working-preferences`](../skills/working-preferences/SKILL.md#questions-and-answers).
- **Answer key**: in a review round's teaching fixture, the file that says which findings a report must contain, where, at what severity, and the expected decision. `scripts/round-check.py` checks a report against it when the packet names it. See [review rounds](review-rounds.md#the-fixture-and-its-answer-key).
- **Anti-slop**: the lists of words, phrases and structures that mark text as generated, removed from anything written. A distilled list in [`working-preferences`](../skills/working-preferences/SKILL.md#distilled-anti-slop-reference) applies everywhere; the full reference in [`document-standards`](../skills/document-standards/SKILL.md#references) applies to any document.
- **Autonomous-asynchronous**: the regime in which no person is present while the work runs, and output is reviewed afterwards if at all. Question blocks are suppressed and decisions are logged rather than gated. See [the three regimes](../skills/surface-regimes/SKILL.md#three-regimes) and [the mechanics by regime](../skills/surface-regimes/SKILL.md#mechanic-adjustments-by-regime).

## B

- **BCP 14**: the IETF convention under which MUST, SHOULD, MAY and their relatives carry defined force, here only when written in capitals. See [document layers](document-layers.md#requirements-language).
- **BREAKING**: the label a release puts beside a skill whose interface it removes, renames, narrows or reverses, a weakened guarantee included, with a one-line migration saying what to do instead. See [releasing](releasing.md#a-skills-interface).
- **Brevity code**: a lowercase home-row code for each command in the command vocabulary, one to three keys, tiered by measured frequency and balanced across the hands. `f` is CONFIRM, `j` DEEPEN, `d` DECLINE, `k` FLAG, `s` REVIEW, `l` HELP. A code counts only as a whole message or paired with a question label. See [`working-preferences`](../skills/working-preferences/SKILL.md#brevity-code) and [the interface contract](interface-contract.md#3-the-brevity-code-and-the-constraint-that-shaped-it).
- **Bridle Works**: the umbrella the kit belongs to, one of its kits. See [contributing](../CONTRIBUTING.md) and [the README](../README.md).

## C

- **Capability vector**: seven vendor-independent fields that describe what a surface can do: `interface`, `autonomy`, `human_presence`, `workspace`, `tool_execution`, `egress` and `audit`. A surface's values are its capability profile, and the regime is derived from them. See [the taxonomy](../orchestration/taxonomy.md#the-capability-vector).
- **Capture file**: the day's append-only file in the provenance layer, where `session-log` writes its entries and `jot` and `touch` leave theirs. See [partial captures](partial-captures.md#where-they-go).
- **Carry count**: how many daily reviews a task has stayed in Doing. A count of three or more is said aloud. See [`daily-review`](../skills/daily-review/SKILL.md).
- **Clean boundary**: a point after a commit, a dispatch or a closed decision, with the work's current state already on disk. The only point at which a compaction is proposed. See [`working-preferences`](../skills/working-preferences/SKILL.md#context-cadence).
- **Clearance**: what an agent may read, set in the roster. One of the axes role is independent of. See [roles](../orchestration/ROLES.md#what-this-axis-is-and-the-three-it-is-not).
- **Command vocabulary**: the closed set of twenty-seven ALLCAPS commands (CONFIRM, DEEPEN, DECLINE, FLAG, STAGE and the rest), each with a brevity code. See [`working-preferences`](../skills/working-preferences/SKILL.md#command-vocabulary), indexed in [`commands`](../skills/commands/SKILL.md).
- **Containment**: the outermost control layer. It limits damage after every other layer has failed, through placement such as tier separation or a sandbox. See [control layers](control-layers.md#7-containment-assume-everything-above-failed).
- **Content-depth principle**: what makes the sensitivity tiers mean something. The lower tiers carry almost nothing sensitive; the third carries operational behaviour with entities abstracted; only the fourth carries real reasoning and named entities. Moving a fact down a tier means stripping the reasoning as well as the names. See [standing documents](standing-documents.md#sensitivity-tiering).
- **Content Read**: the one line stated before a document is generated, naming its type, audience and dial values. A read-back, not a question. See [`document-standards`](../skills/document-standards/SKILL.md#content-read).
- **Context cadence**: when the agent raises compaction: from about 60k tokens of context a status line, the CTX line (`CTX ~75k est; next clean boundary: <what>`, about every 20k), an offer to compact from about 100k, and past 130k a warning in every reply, finishing only the current step and then stopping to ask. See [`working-preferences`](../skills/working-preferences/SKILL.md#context-cadence).
- **Control fidelity**: what this project is judged on in place of capability: legible state, cheap correction, a reliable halt. See [the philosophy](../philosophy.md#riding-tack-interface-and-experience).
- **Coverage line**: the closing statement of a check or tool that names what it read and what it did not. A check that does not state its coverage is not a check. See [contributing](../CONTRIBUTING.md) and [`orient`](../skills/orient/SKILL.md).

## D

- **Derived**: a claim inferred from established principles and labelled as an inference. One of three knowledge labels, with verified and unknown. See [`working-preferences`](../skills/working-preferences/SKILL.md#tripartite-knowledge-labeling).
- **Derived-candidate**: the trust label for faculty output that is plausible and not yet checked. See [the routing threshold](../orchestration/ROUTING-THRESHOLD.md#gate-3-trust-label-assignment).
- **Derived-grounded**: the trust label for faculty output checked independently against ground truth, such as a file's existence, or output that cites its sources. See [the routing threshold](../orchestration/ROUTING-THRESHOLD.md#gate-3-trust-label-assignment).
- **Dials**: numeric settings from 1 to 10 that tune behaviour. AUTONOMY, PROACTIVITY and RIGOR govern work in [`working-preferences`](../skills/working-preferences/SKILL.md#dials); formality, density and audience level govern documents in [`document-standards`](../skills/document-standards/SKILL.md).
- **Dispatch**: the message in which the lead assigns work; the lead writes the dispatches and is the only role that assigns work to a minion. The [routing threshold](../orchestration/ROUTING-THRESHOLD.md#gate-3-trust-label-assignment) also calls an agent sending part of a task to a faculty the dispatching agent. See [roles](../orchestration/ROLES.md#lead).
- **DMZ (Level 3.5)**: in the Purdue model, the broker between the operational and business sides that nothing crosses directly. Here it is the pre-publish redaction gate. See [control layers](control-layers.md#segmentation-the-purdue-model).
- **Documentation**: text written for a reader with a task, describing the system as it is now. It lives in this repository and never shares a file with provenance. See [document layers](document-layers.md#documentation-and-provenance).

## E

- **Egress**: the capability field that says where content goes when a surface processes it: `local`, `operator-hosted` or `vendor-cloud`. The join key for any sensitivity gate. See [the taxonomy](../orchestration/taxonomy.md#the-capability-vector).
- **Eisenhower quadrant**: a task's priority, one of Do, Decide, Delegate and Delete. A task is urgent only when it carries a due date and a stated consequence of missing it. See [`daily-review`](../skills/daily-review/SKILL.md#the-lanes).

## F

- **Faculty**: a model a Claude-tier agent may route part of a task to, local or vendor-hosted, under the routing threshold. See [the routing threshold](../orchestration/ROUTING-THRESHOLD.md).
- **Finding**: one claim in a report that something is wrong or missing, numbered within its report (`r12.2.3` is report 2's third finding) and graded major, minor or nit. See [rounds](../orchestration/rounds.md#reports-and-findings). Separately, a review round's finding is one entry in the reviewer's report, which stays Reported until someone other than the reviewer reproduces it; see [review rounds](review-rounds.md#reported-and-verified).

## G

- **Gate**: a mechanical check that blocks. `scripts/gates.sh` runs this repository's gates locally and in CI; how each gate is itself tested is under [selftest](#s). A gate is the interlock layer applied to a repository. See [contributing](../CONTRIBUTING.md) and [control layers](control-layers.md#4-interlocks-the-machine-acts-without-asking).
- **GFM**: GitHub Flavored Markdown, the dialect this repository's documents are written in and render as. See [document layers](document-layers.md#references).

## H

- **Handoff document**: the file a person or agent reads to take over: roster, standing conventions, adopted decisions, open items. Provenance layer. See [the document set](standing-documents.md#the-document-set).
- **Human-facing**: the document layer written for a person with a task: lean, concrete, no archaeology. The other layer is provenance. See [standing documents](standing-documents.md#the-organizing-principle).

## I

- **Inbox**: two senses. The first [lane](#l) of the task board, holding what is captured and not yet clarified; and a seat's mail directory, where mail arrives as commits. See [`daily-review`](../skills/daily-review/SKILL.md#the-lanes) and [growing the workspace](installing.md#growing-the-workspace).
- **Informative**: text that helps a reader apply a requirement and creates no obligation. See [document layers](document-layers.md#normative-and-informative).
- **Inherent design**: the innermost control layer, an arrangement in which the failure cannot be reached at all. A rule that a determined mistake could still break is not inherent design. See [control layers](control-layers.md#1-inherent-design-make-the-failure-impossible).
- **Interactive-synchronous**: the regime in which a person is present and can answer before the next step runs. The default when the regime is unclear. See [`surface-regimes`](../skills/surface-regimes/SKILL.md#three-regimes).
- **Interlock**: a control layer that blocks without asking, reserved for conditions where a person's decision would always be the same. See [control layers](control-layers.md#4-interlocks-the-machine-acts-without-asking).

## J

- **Jot**: a partial capture of reasoning: one short entry of decisions, corrections and findings, marked `[jot]` in the capture file. It discharges nothing. See [`jot`](../skills/jot/SKILL.md) and [partial captures](partial-captures.md).

## K

- **Kit**: this repository, Toothpaste Kit (`tp-kit`): a skill library, an agent relay protocol and a set of mechanical gates for multi-agent work with a person in charge of it. See [the README](../README.md).

## L

- **Lane**: a column of the task board: Inbox, Someday/Maybe, Next, Waiting, Doing, Verify, and Done or Archive. See [`daily-review`](../skills/daily-review/SKILL.md#the-lanes).
- **Lane-board tool**: the one command that prints every task grouped by lane and ends with a coverage line. The review skills assume it. See [`daily-review`](../skills/daily-review/SKILL.md).
- **Lead**: the role that acts and delegates. It holds the plan, sequences the work and writes the dispatches. It prepares decisions and does not take them. See [roles](../orchestration/ROLES.md#lead).
- **Level**: how far a repository's remotes reach, as `scripts/remote-level.sh` reports it: `none`, `internal` or `external`. A host it cannot prove internal is external. The level sets what an agent may do: commit with `none`, commit and push its own branch with `internal`, and only read, edit and stage with `external`; a merge into a trunk is always a person's. The [Purdue model](#p) and [DMZ](#d) use level in the plant sense, and a [sensitivity tier](#s) is not a level. See [the README](../README.md#scripts), [the level script](../scripts/remote-level.sh) and [growing the workspace](installing.md#growing-the-workspace).

## M

- **Major**: the severity grade for a wrong result or a broken rule on input that ordinary use produces. It blocks a round's close. See [rounds](../orchestration/rounds.md#severity). A review round uses the same three grades for its findings, without the rule about closing; see [review rounds](review-rounds.md).
- **Manifest**: the file, `index.md` by default, that says what is authoritative, what is stale and what was added when, and names which documents must stay current. Read first in any session. See [the document set](standing-documents.md#the-document-set) and [how the documents work together](standing-documents.md#how-they-work-together).
- **Merge-proxy**: a skill a person invokes to let the agent type a trunk merge they have decided, for one session, on a repository whose level is `internal` or `none`, and only after the agent explains the exact plan in full and halts for explicit approval of it. It never applies to an external remote. See [`merge-proxy`](../skills/merge-proxy/SKILL.md).
- **Minion**: the role that executes one atomic task cold, from a brief, and reports. It does not interpret. See [roles](../orchestration/ROLES.md#minions).
- **Minor**: the severity grade for a wrong result with a small, visible consequence, or a gap a reader would trip on. Fixed before the close unless the operator accepts it. See [rounds](../orchestration/rounds.md#severity).
- **Most Important Task**: the one task the daily review sets for the day. See [`daily-review`](../skills/daily-review/SKILL.md).

## N

- **Nit**: the severity grade for a finding that changes no real outcome: wording, a contrived input, or a test gap where the code is right. It never blocks a close. See [rounds](../orchestration/rounds.md#severity).
- **Normative**: text that states what a conforming reader does, uses a BCP 14 keyword, and can be tested. See [document layers](document-layers.md#normative-and-informative).

## O

- **OODA loop**: Observe, Orient, Decide, Act. Here Orient is the pivot, and stale orientation is the system's characteristic failure. See [control layers](control-layers.md#tempo-the-ooda-loop).
- **Operator**: the role that decides. The only role that originates authority, and the only one that takes real-world action such as a merge into a trunk. It may not be simulated. See [roles](../orchestration/ROLES.md#operator).

## P

- **Partial capture**: an entry written by `jot` or `touch`, marked in its heading so it never reads as the output of `session-log` or `session-close`. See [partial captures](partial-captures.md).
- **Participant**: the active human role in a relay: reads and adds content, such as a decision, an override or a tie-break. Its failure mode is an unflagged edit. The passive role is relay; one person should not hold both for the same message, and an edit made while relaying is a participant act that the log should record. See [the taxonomy](../orchestration/taxonomy.md#human).
- **Planted positive**: an input made to contain what a check looks for, run to prove the check can fire before its clean result is trusted. See [contributing](../CONTRIBUTING.md).
- **Programmatic-contractual**: the regime in which another program makes a single request and takes a single response, with no chat UI. Output is a data contract, not prose, unless the caller asks for prose. See [`surface-regimes`](../skills/surface-regimes/SKILL.md#three-regimes).
- **Provenance**: the record of how the system came to be: options weighed, what failed, why a rule changed. Written for agents and later maintainers, kept outside this repository. See [document layers](document-layers.md#documentation-and-provenance).
- **Purdue model**: a plant segmentation model by levels, used here to say what may reach what: the files at the bottom, the public repository and vendor APIs at the top, and the redaction gate between. See [control layers](control-layers.md#segmentation-the-purdue-model).

## Q

- **Question block**: the three numbered questions, Q1 to Q3, that close a reply needing a decision, one per line, each ending with the codes it accepts. Alternatives are digits, `1` the recommendation; `f` always does what the question names, and `d` always stops. See [`working-preferences`](../skills/working-preferences/SKILL.md#questions-and-answers).

## R

- **Reach**: how bounded an agent's mistakes are, and therefore how much standing latitude it gets. One of the axes role is independent of. See [roles](../orchestration/ROLES.md#what-this-axis-is-and-the-three-it-is-not).
- **Readback**: the first line of a reply to answers, restating each answer's meaning before any work, so a misread is caught before it becomes an action. See [`working-preferences`](../skills/working-preferences/SKILL.md#questions-and-answers).
- **Redaction gate**: the pre-publish check run before content crosses a tier boundary outward, against the local restricted material, with the decision handed to a person. See [`redaction-gate`](../skills/redaction-gate/SKILL.md).
- **Regime**: one of three operating modes derived from a surface's capability profile: interactive-synchronous, autonomous-asynchronous and programmatic-contractual. Each adjusts the dials and which skills load. See [`surface-regimes`](../skills/surface-regimes/SKILL.md).
- **Register**: the table of rounds, one row each: number, dispatch time, seats, task, state and result. See [rounds](../orchestration/rounds.md#closing-a-round).
- **Registry**: the directory `orchestration/registry/`, one file per vendor, describing what each surface can actually do. The protocol reads that capability, never the product name. See [the surface registry](../orchestration/registry/README.md).
- **Regular loop**: the control layer of automation that runs constantly and silently, such as a formatter or a check recipe. Its failure mode is silence that looks like success. See [control layers](control-layers.md#2-the-regular-loop-automation-that-holds-the-value-in-band).
- **Relay**: the passive human role: copies a message between surfaces without changing it. Its failure mode is transcription drift. See [the taxonomy](../orchestration/taxonomy.md#human) and [the relay protocol](../orchestration/protocol.md#relay-fidelity).
- **Relief**: a control layer designed to fail on purpose in a known direction, such as a forced push that writes a record naming who forced it and why. See [control layers](control-layers.md#5-relief-designed-to-fail-on-purpose-in-a-known-direction).
- **Report**: a seat's reply to a round's dispatch, numbered within the round (`r12.2`): what was done, how it was checked, and what the check does not cover. A re-check after fixes is the next report, never a new round. See [rounds](../orchestration/rounds.md#reports-and-findings).
- **Reproduced**: a review-round finding's status once a role other than the reviewer has repeated its evidence and recorded their own. Only a reproduced finding can be cited in the operator's decision. See [review rounds](review-rounds.md#reported-and-verified).
- **Review round**: one change, one review of it, the verification of that review and one decision, kept as three records (the packet, the reviewer's report and the operator's decision) and checked by `scripts/round-check.py`. Not a [round](#r), which is one task with its dispatches and replies. See [review rounds](review-rounds.md) and [the quickstart](review-rounds-quickstart.md).
- **Role**: authority over a decision: operator, lead, aide or minion. One identity may hold several. Role is independent of clearance, seat and reach. See [roles](../orchestration/ROLES.md).
- **Role name**: a filename that says what a file does for the system, such as a manifest or a thread log. Published freely, unlike a subject name, which says what a file is about and is treated as content. See [standing documents](standing-documents.md#why-these-filenames-are-here-at-all).
- **Roster**: the part of the handoff document where each agent's clearance is set. See [the document set](standing-documents.md#the-document-set) and [roles](../orchestration/ROLES.md#what-this-axis-is-and-the-three-it-is-not).
- **Round**: one task: the lead's dispatches for it and the replies, numbered `r1` upward, checked by a seat other than the author and decided by the operator. See [rounds](../orchestration/rounds.md). Not a [review round](#r), which records one change's review.
- **Routing threshold**: four ordered gates (sensitivity, capability, cost, trust label) that decide whether part of a task goes to a local model, a vendor faculty or the agent itself. See [the routing threshold](../orchestration/ROUTING-THRESHOLD.md).

## S

- **Sacrificial part**: a cheap component chosen to break first so failure lands somewhere cheap and loud, such as a scratch directory or a generated file. See [control layers](control-layers.md#6-sacrificial-parts-cheap-components-that-break-first).
- **Seat**: one working copy of an agent, holding its own branch and inbox; [roles](../orchestration/ROLES.md#what-this-axis-is-and-the-three-it-is-not) calls this axis Surface. Authority never moves sideways between seats, even when one person runs both. See [roles](../orchestration/ROLES.md#how-authority-moves).
- **Selftest**: a tool's `--selftest` option, which runs the tool on inputs whose right answer is known, such as planted positives, a fixture or scratch repositories, and fails when the answer is wrong. Three of the gates in `scripts/gates.sh` run a tool's selftest, and `gates.sh --selftest` plants a positive for each of the others. See [contributing](../CONTRIBUTING.md), [the README](../README.md#scripts) and [the gate script](../scripts/gates.sh).
- **Sensitivity tier**: one of the four groups material is sorted into by audience, with physical isolation as the main control. Who may read a thing and whether a system may keep it are tracked separately; the routing threshold calls the second the storage-persistence axis. See [standing documents](standing-documents.md#sensitivity-tiering) and [the routing threshold](../orchestration/ROUTING-THRESHOLD.md).
- **Skill revision**: a skill's version label, kept in that skill's own `CHANGELOG.md` and named in each release that moves it. See [releasing](releasing.md#skill-revisions).
- **Standing documents**: the document set a tree keeps: `CLAUDE.md`, the manifest, the handoff document, the task queue, the thread logs, per-project state, procedures and postmortems, each in one of the two layers. The manifest names which must stay current, and `session-close` checks those. See [the document set](standing-documents.md#the-document-set) and [how the documents work together](standing-documents.md#how-they-work-together).
- **Surface**: a place an agent runs, such as a chat window, a terminal session or an API call, scored on the capability vector. [Roles](../orchestration/ROLES.md#what-this-axis-is-and-the-three-it-is-not) uses Surface for a different axis, the working copy that owns a branch and inbox, which this page calls a seat, under [S](#s). See [the taxonomy](../orchestration/taxonomy.md#surfaces-and-sub-roles).

## T

- **Tack**: the interface through which a person's intent reaches a capable system and its state comes back: the skills, protocols and gates. From the image of a rider and a horse. See [the philosophy](../philosophy.md#riding-tack-interface-and-experience).
- **Task board**: the task queue seen lane by lane, as the [lane-board tool](#l) prints it. See [`daily-review`](../skills/daily-review/SKILL.md#when-to-use).
- **Thread**: a loose end raised mid-conversation that has no task yet. It is added to the open-threads log and moves to the resolved log with its resolution written out. See [standing documents](standing-documents.md#how-they-work-together).
- **Timebox**: the time a round's dispatch allows. A round whose timebox passes closes with the silent seat recorded as unanswered. See [rounds](../orchestration/rounds.md#closing-a-round).
- **Token**: in the relay protocol, the right to produce the next message in a thread, held by whoever the latest message is addressed to. See [the relay protocol](../orchestration/protocol.md#turn-taking).
- **Touch**: a partial capture of one fact-level edit to a standing file, with a line marked `[touch]` in the capture file. It discharges nothing. See [`touch`](../skills/touch/SKILL.md) and [partial captures](partial-captures.md).
- **Trunk**: `main`, or any branch a repository treats as shared truth. A merge into it is a decision rather than a record, so a person decides it; [merge-proxy](#m) moves only the typing. See [`merge-proxy`](../skills/merge-proxy/SKILL.md), [growing the workspace](installing.md#growing-the-workspace) and [roles](../orchestration/ROLES.md#operator).
- **Trust label**: the grade a dispatching agent gives a faculty's output: a default on receipt, raised only by the agent's own check, on the scale unknown, derived-candidate, derived-grounded, verified. Verified is reserved for content the agent confirmed directly. Output inherits the weakest unverified label in its chain. See [the routing threshold](../orchestration/ROUTING-THRESHOLD.md#gate-3-trust-label-assignment).
- **Two occurrences**: the bar a pattern must reach before it earns a mechanical check, and a cause before it counts as a diagnosis. See [control layers](control-layers.md#3-alarms-the-machine-notices-the-human-decides) and [the example workspace](../examples/workspace/CLAUDE.md).

## U

- **Unknown**: a claim that needs information not currently available. One of three knowledge labels, with verified and derived. See [`working-preferences`](../skills/working-preferences/SKILL.md#tripartite-knowledge-labeling).

## V

- **Verified**: a claim known with certainty from provided or trained information. One of three knowledge labels, with derived and unknown. Separately, a completion claim counts as fact only once a party other than the claimant has checked it. See [`working-preferences`](../skills/working-preferences/SKILL.md#tripartite-knowledge-labeling) and [control layers](control-layers.md#where-the-human-sits).
- **Verifier**: the seat that checks a round's work, never its author. It proposes each finding's grade; the lead's grade stands. See [rounds](../orchestration/rounds.md#severity). Separately, in a [review round](#r), the verifier is the role that reproduces the reviewer's findings, which must differ from the reviewer's role; see [review rounds](review-rounds.md#reported-and-verified).
- **Verify lane**: the lane for work whose deliverable exists and has been checked by a second party. It leaves for Done only on the person's word. See [`daily-review`](../skills/daily-review/SKILL.md#the-lanes).

## W

- **WCAG**: the W3C Web Content Accessibility Guidelines. This repository applies their Markdown-relevant techniques to the documents it ships. See [document accessibility](document-accessibility.md).

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
