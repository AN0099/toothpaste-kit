# Review rounds: the Local Change-Verification Round

A review round is how one proposed change to a repository is reviewed, has its findings reproduced
by someone other than the reviewer, and is then accepted, rejected or sent back for revision by the
operator. It is version 0.1 of the Local Change-Verification Round, and it runs on one machine,
from files committed to Git.

This page is the specification as the kit implements it. The steps to run one are in
[the review-round quickstart](review-rounds-quickstart.md).

**A review round is not a [round](../orchestration/rounds.md).** A round is one task with its
dispatches and replies between seats. A review round is narrower: one change, one review of it,
the verification of that review, and one decision. The two share the rule that a finding is a
claim, and the roles in [`ROLES.md`](../orchestration/ROLES.md).

## The rule it exists for

**A finding is a claim; it becomes Verified only after someone other than its reviewer reproduces
it with evidence.** A finding the reviewer has written down is Reported. It is Verified only when
a party other than the reviewer reproduces it against the revision under review and records its
own evidence. An operator decision may cite only findings that were reproduced that way.

Four more statements hold for every review round:

- **Git commits and artifact paths are the canonical evidence model.** Each record names the
  revisions it concerns by commit hash, and names other records by their repository-relative path
  and the commit that holds them.
- **Relay identifiers are optional future transport references, not prerequisites for a valid
  round.** A round never needs the relay format in [`protocol.md`](../orchestration/protocol.md),
  an event ID, a thread ID, or an agent's capability profile.
- **Mechanical validation is evidence, not a substitute for operator accountability.** A passing
  check says the records are well formed and consistent with each other. It does not say the
  change is correct, or that the review was complete.
- **The operator decides.** Checks and the reviewer's recommendation are evidence put in front of
  the operator; neither accepts anything.

## The steps

| Step | Who | Record |
|---|---|---|
| 1. Create the round | not fixed | `ReviewRound`: the base and target revisions, the scope, the restrictions, the expected roles, the required checks, and the fixture's answer key if there is one |
| 2. Review the target revision | aide | None yet: the reviewer identifies the revision it actually examined, runs the required checks and keeps the evidence |
| 3. Submit the report | aide | `ReviewReport`: the revision reviewed, each check's status, the findings, the limitations, a recommendation |
| 4. Verify each finding | lead | Recorded in the next record: each finding reproduced, not reproduced, not applicable or blocked, with the verifier's own evidence |
| 5. Decide | operator | `OperatorDecision`: whether the revisions align, the verification of each finding, and the decision |

The roles in the table are the reference assignment; version 0.1 does not fix who creates the
round. What the records require is that the
reviewer and the verifier of a reproduced finding are declared as different roles, and that the
decision is made by `operator`.

Each record is committed to Git before the next step starts. The three are separate files and
none is edited to move the round on, so each keeps its own author, time and evidence.

## The three records

All three are JSON documents, checked against draft-07 JSON Schemas. Each is closed: a field the
schema does not name is an error, because a record that carries authority must not carry fields
nobody checks. Field names below are paths into the document.

**Every record has:**

| Field | Meaning |
|---|---|
| `schemaVersion` | Which record format this is: `tpkit.review-round/v1alpha1`, `tpkit.review-report/v1alpha1` or `tpkit.operator-decision/v1alpha1`, matching `kind` |
| `kind` | `ReviewRound`, `ReviewReport` or `OperatorDecision`, in the same order |
| `metadata.id` | This record's own stable ID |
| `metadata.roundId` | The round's ID, the same in all three records |
| `metadata.createdAt` | When the record was made, as a date-time with an offset |
| `handling.visibility` | `public`, `private` or `restricted` |
| `handling.redaction` | `none`, `sanitized` or `pending-review` |
| `provenance.artifactPath` | Where this record lives, relative to the root of the repository the round is committed in, which is not the kit unless the round is committed there. The validator checks only that it is relative, not that the file is there |

Roles are always lower case: `operator`, `lead`, `aide` or `minion`, the four in `ROLES.md`.

Every id, such as `metadata.roundId`, a check's `id` or a finding's `id`, uses only lower-case
letters, digits, `.` and `-`, and starts with a letter or digit (`^[a-z0-9][a-z0-9.-]*$`): `f1`,
not `F1`.

Every field named `evidence`, in any record, is a list of entries, never a string or a single
entry. Each entry has `description`, and may have `command`, `output` (the captured text) and
`path` (repository-relative); no other field is allowed. For example:

```json
"evidence": [
  {
    "description": "Revision checked out in the fixture repository",
    "command": "git -C /tmp/tally-review rev-parse HEAD",
    "output": "1127c5ce8d21469eee448329cf30323c2e5a08ac"
  }
]
```

### ReviewRound

The round packet. It records what was asked, not what happened.

| Field | Meaning |
|---|---|
| `provenance.repository` | The repository under review |
| `provenance.baseRevision` | The commit the change starts from |
| `provenance.targetRevision` | The commit the reviewer is asked to review. It records the request only; it does not show what the reviewer actually looked at |
| `roles.reviewer.role`, `roles.verifier.role`, `roles.decisionMaker.role` | Who is expected to do each part |
| `scope.paths`, `scope.intent` | Which paths are in scope, and what the change is meant to do |
| `requiredChecks` | The mechanical checks the reviewer must run and report, each with an `id` and a `command`, both required, and an optional `description`, for example where to run it. No other field is allowed |
| `restrictions.network`, `restrictions.secrets`, `restrictions.remoteAccess` | The round's posture on each, `prohibited` or `permitted`, with optional `restrictions.notes` |
| `fixture.answerKey` | Optional: where the verifier's answer key is, for a teaching fixture |
| `transport.relayEventId`, `transport.relayThreadId` | Optional, and never needed |

### ReviewReport

What the reviewer saw and claims.

| Field | Meaning |
|---|---|
| `reviewer.role` | The reviewer's role |
| `reviewedRevision.revision` | The commit the reviewer actually examined |
| `reviewedRevision.evidence` | How that revision was identified, for example the output of `git rev-parse HEAD` |
| `checks` | Each required check with a status. `passed`: it ran and reported success; that is evidence about the check, not acceptance of the change. `failed`: it ran and reported failure, including a nonzero exit. `blocked`: you tried and it could not run, for example a missing tool or a forbidden network; say what stopped it in `note`. `not-run`: you did not try; say why in `note`. A check with no status is an error |
| `findings` | The reviewer's claims. Each has `id` (unique in the report), `severity` (`major`, `minor` or `nit`), `location.path`, `claim`, `evidence` and `proposedRemedy` |
| `recommendation.status`, `recommendation.rationale` | `accept`, `reject`, `request-revision` or `no-recommendation`, and why. It is a recommendation, not a decision |
| `limitations` | What the review did not cover. Always present; an empty list means the reviewer states no limitation |
| `provenance.commit` | The commit the report was written against: `HEAD` when it was written. A file cannot hold the hash of the commit that adds it, so the commit that holds the report is recorded in the decision's `references.reviewReport` |

Each finding also carries `verification`, and in a report it is always the unverified state:
`status` is `unverified`, `verifiedBy` is `null` and `evidence` is empty. A reviewer cannot record
its own finding as reproduced.

### OperatorDecision

The verification of each finding and the operator's decision, in one record.

| Field | Meaning |
|---|---|
| `references.reviewRound`, `references.reviewReport` | The path and commit of the round packet and of the report |
| `alignment.packetTargetRevision` | The round's `targetRevision`, copied |
| `alignment.reportReviewedRevision` | The report's `reviewedRevision.revision`, copied |
| `alignment.status` | `matched` only if the two are the same commit, compared exactly; otherwise `mismatched`, or `unresolved` if either cannot be resolved |
| `verification.performedBy.role`, `verification.performedAt` | Who verified the findings, and when |
| `verification.findings` | One entry per reported finding the verifier checked, naming it by `findingId`. A reported finding with no entry is unverified, and the decision cannot cite it. Each entry's status is `reproduced`, `not-reproduced`, `not-applicable` or `blocked`, with the verifier's evidence |
| `decision.madeBy.role` | Always `operator` |
| `decision.status` | `accept`, `reject` or `request-revision`; or, when the alignment is not `matched`, `abstain` or `rerun` |
| `decision.basedOnFindings` | The finding IDs the decision rests on. Each must be `reproduced`, with evidence |
| `decision.rationale` | Why, in words |
| `decision.exceptions` | Optional: each explicit exception the operator makes, such as accepting despite a reproduced finding |

## Revision alignment

The round names the revision it asks to have reviewed; the report names the revision that was
reviewed. They can differ: a branch moved, the reviewer checked out the wrong commit, or a fix was
pushed during the review. So the decision records both and says whether they match.

**Only an exact match lets the decision rest on the report.** If the revisions differ, or one of
them cannot be resolved to a commit, the report is not evidence about the requested target, and a
normal accept, reject or request-revision decision on that target must not be made from it. The
operator can still record why, ask for the review to be run again, or record an explicit
exception.

**A reproduced blocking finding needs an explicit exception to accept.** A blocking finding is one
the report grades `major`, the grade that blocks the close in [rounds](../orchestration/rounds.md).
If one is reproduced, an accept without an entry for it in `decision.exceptions`, naming the
finding and giving a reason, is an error. The operator may still accept; the exception is how the
record shows that they did so knowingly.

## Reported and Verified

| Status | Set by | Means | Can a decision cite it? |
|---|---|---|---|
| `unverified` | the reviewer, in the report | The finding is Reported: a claim nobody else has checked | No |
| `reproduced` | the verifier, in the decision | Someone other than the reviewer reproduced it, with evidence | Yes, and only with that evidence recorded |
| `not-reproduced` | the verifier | The verifier tried and could not reproduce it | No |
| `not-applicable` | the verifier | It does not apply to this revision or scope | No |
| `blocked` | the verifier | The verifier could not attempt it | No |

The difference between the last three is whether the verifier tried and whether the finding
applies. `not-reproduced` means it applies and the attempt did not show it. `not-applicable` means
no attempt was needed, because the finding is outside the round's revision or scope. `blocked`
means it applies but no attempt was possible. For the last two, the reason belongs in the entry's
`note`.

A finding moves from Reported to Verified only in the decision, never by editing the report.

## What validation can and cannot show

The validator, `scripts/round-check.py`, uses only the Python standard library and needs no
network. It checks each record against its schema and, separately, against the fields the
specification requires, so a schema that drifts from the specification is caught. It then checks
the records against each other: the same round ID in all three, the alignment, the role of each
verifier against the reviewer's, that every cited finding is reproduced with evidence, that every
check has a status, and that a fixture's answer key is met. Given `--repo DIR`, the repository the
round is committed in, it also checks that each cited commit exists there and that each
`references` commit holds the record at its `artifactPath`; without it, commits are checked only
for format. A problem between records names the
round, the record and the rule that was broken; a problem within one record names the file and the
field. `./scripts/gates.sh` runs it, as gate 18, over every round directory under `examples/`, and
with `--cases` over `examples/review-round/schema-cases/`, so the fixture, the examples and each
schema case's recorded `expect`, invalid cases included, are checked on every gate run.

**It cannot show independence.** It checks that the declared verifier role differs from the
declared reviewer role. It cannot show that two different people, or two independent processes,
did the work.

**It cannot show that anyone looked.** It can check that evidence and references are recorded.
It cannot show that a person made each observation the evidence describes.

**An exception is not a reproduction.** A decision may record an explicit exception or a
limitation, but nothing it records turns an unverified finding into a reproduced one.

## Handling labels

`handling.visibility` and `handling.redaction` are workflow labels that say how a record is meant
to be handled. They are not a legal classification, a compliance certification or an access
control, and labelling a record `restricted` does not make it safe to hold restricted material.
Public fixtures hold synthetic content and synthetic evidence only. Sensitive work needs its own
handling and review process outside this workflow.

## The fixture and its answer key

The kit ships a teaching fixture in `examples/review-round/`: a small synthetic project with a
proposed change that carries a known defect.

| Directory | Holds | For |
|---|---|---|
| `history/` | Numbered patch files and `build.sh`, which builds them into a fresh repository outside the kit with fixed authors and dates, so the base and target commits are the same on every run | everyone |
| `reviewer/` | The round packet, a report template and step-by-step instructions | the reviewer |
| `verifier/` | `answer-key.json`, a checklist in its README, a decision template, and in `expected/` a completed round that passes the validator | the verifier and the operator |

The reviewer's packet does not name the answer key. The packet in `verifier/expected/` does, in
`fixture.answerKey`, and when a packet names one the validator checks the round against it: a
report with no findings fails when the key says that is not acceptable, each required finding
must be matched by a report finding, and a decision on a matched alignment must be the key's
expected decision. That last rule is for the fixture: it grades a practice decision, and a real
round has no answer key. A key that requires no finding while rejecting an empty report is itself
an error.

**The match is mechanical.** A report finding matches an expected one by its location and a
minimum severity, not by what it says. The verifier still reads each finding against the key's
equivalence criteria; the validator only catches a report that could not be right.

A round does not have to produce findings. Against a fixture whose answer key expects none, a
report with no findings passes; what fails is a report that misses what the answer key expects.

**The separate directory keeps the answer key out of the reviewer's instructions. It is not a
secret.** Anyone who can read the repository can read the answer key. If an assessment really
needs a confidential answer key, keep the key private or hand it out separately; this repository
does not do that.

## Not in version 0.1

These are left out on purpose. Do not read their absence as a gap to fill in this workflow:

- A dispatch record, an acknowledgement record, a standalone collection record and a close or
  handoff record. Collection is part of the decision record in 0.1.
- Relay transport, and any mapping between round records and relay events.
- More than one reviewer, dissent between reviewers, and confidential or concern reporting.
- Signatures and cryptographic attestations.
- Rounds spanning more than one repository.
- Automatic merge, deployment or acceptance, a scheduler or task graph, a service, a database, a
  dashboard or any web interface.
- Procedures for restricted or regulated work, and private delivery of answer keys.

A review round is a narrow, local reference workflow. It is not a general orchestration platform,
a control plane, or evidence of compliance with any regulation.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
