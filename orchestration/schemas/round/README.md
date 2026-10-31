# Round artifact schemas

Three separate draft-07 schemas for the Local Change-Verification Round. Each kind is its own
committed document, so authorship, chronology and evidence stay separate and Git keeps the
record. None of them inherits from `event-base.json`, and none needs a relay identifier.

| File | Title | Records |
|---|---|---|
| `review-round.json` | ReviewRound | Intent: scope, base and target revisions, roles, required checks, restrictions |
| `review-report.json` | ReviewReport | Observation: the revision actually reviewed, check results, findings as claims, limitations, a recommendation |
| `operator-decision.json` | OperatorDecision | Authority: revision alignment, independent verification of each finding, the operator's decision |

A finding is a claim; it becomes Verified only after someone other than its reviewer reproduces it
with evidence. Git commits and artifact paths are the canonical evidence model. Relay identifiers
are optional future transport references, not prerequisites for a valid round. Mechanical
validation is evidence, not a substitute for operator accountability.

## Shared fields

Every document carries these, each schema defining its own copy (there is no shared base file).

| Field | Meaning |
|---|---|
| `schemaVersion` | `tpkit.review-round/v1alpha1`, `tpkit.review-report/v1alpha1` or `tpkit.operator-decision/v1alpha1` |
| `kind` | `ReviewRound`, `ReviewReport` or `OperatorDecision` |
| `metadata.id` | This document's identifier, lower case, digits, `.` and `-` |
| `metadata.roundId` | The round the document belongs to, the same in all three |
| `metadata.createdAt` | A date-time |
| `handling.visibility` | `public`, `private` or `restricted` |
| `handling.redaction` | `none`, `sanitized` or `pending-review` |
| `transport` | Optional: `relayEventId` and `relayThreadId`, each a string or null. Never required |

Handling labels are workflow metadata. They are not legal classification, compliance
certification or access control, and a document marked `restricted` is not safe for sensitive
material because of the label. Public fixtures hold synthetic content only.

Revisions and commits are full Git object names (40 or 64 hexadecimal characters), so two
revisions compare exactly. Paths are repository-relative: no leading `/`, no `\`, no `..` segment.
Role values are the four roles of `orchestration/ROLES.md` in lower case: `operator`, `lead`,
`aide`, `minion`. The list is written out in four places: each schema's `role` definition and `ROLES` in
`scripts/round-check.py`. A role added to or removed from `ROLES.md` must be changed in all four by
hand; `round-check.py --selftest`, which gate 18 runs, fails until the four agree with `ROLES.md`.

## ReviewRound

| Field | Meaning |
|---|---|
| `provenance.repository` | The repository under review, as its maintainers name it |
| `provenance.baseRevision`, `provenance.targetRevision` | The change under review. The target is the revision requested, which proves nothing about what a reviewer inspected |
| `provenance.artifactPath` | Where this packet is committed |
| `roles.reviewer.role`, `roles.verifier.role` | The declared roles. The schema cannot require them to differ; the validator does |
| `roles.decisionMaker.role` | Always `operator` |
| `scope.paths`, `scope.intent` | What to review and why, at least one path |
| `requiredChecks[]` | `id` and `command` for each mechanical check the reviewer runs |
| `restrictions` | `network`, `secrets` and `remoteAccess`, each `prohibited` or `permitted`, and optional `notes` |
| `fixture.answerKey` | Optional path to verifier material. Instructional separation only, not access control |

## ReviewReport

| Field | Meaning |
|---|---|
| `reviewer.role` | The role that reviewed |
| `reviewedRevision.revision` | The revision actually inspected |
| `reviewedRevision.evidence[]` | At least one item identifying that revision, such as `git rev-parse HEAD` output |
| `checks[]` | `id` and `status`: `passed`, `failed`, `not-run` or `blocked`. A pass is evidence, not acceptance |
| `findings[]` | `id`, `severity` (`major`, `minor`, `nit`, as in `orchestration/rounds.md`), `location.path`, optional `location.line`, `claim`, `evidence[]` (at least one), `proposedRemedy`, `verification` |
| `findings[].verification` | Always `{"status": "unverified", "verifiedBy": null, "evidence": []}`. A report cannot verify its own finding |
| `recommendation` | `status` (`accept`, `reject`, `request-revision`, `no-recommendation`) and `rationale`. Evidence for the operator, not a decision |
| `limitations[]` | Always present. An empty array means the reviewer states no limitation |
| `provenance.artifactPath`, `provenance.commit` | Where and in which commit this report is recorded |

An evidence item has a `description` and, optionally, a `path`, a `command` and captured `output`.

## OperatorDecision

| Field | Meaning |
|---|---|
| `references.reviewRound`, `references.reviewReport` | `artifactPath` and `commit` of the two documents decided on |
| `alignment.packetTargetRevision` | The packet's `targetRevision` |
| `alignment.reportReviewedRevision` | The report's reviewed revision, or null when it cannot be resolved |
| `alignment.status` | `matched` (the two are equal exactly), `mismatched` or `unresolved`. Matched needs a revision, not null |
| `verification.performedBy.role`, `verification.performedAt` | Who verified, and when |
| `verification.findings[]` | `findingId`, `status` (`reproduced`, `not-reproduced`, `not-applicable`, `blocked`), `evidence[]`, optional `note`. Reproduced and not-reproduced need at least one evidence item |
| `decision.madeBy.role` | Always `operator` |
| `decision.status` | `accept`, `reject`, `request-revision`, `abstain` or `rerun`. A mismatched or unresolved alignment allows only `abstain` or `rerun` |
| `decision.basedOnFindings[]` | Finding IDs the decision rests on, each reproduced with evidence |
| `decision.rationale` | Why |
| `decision.exceptions[]` | Optional `findingId` and `reason` for an explicit exception, such as accepting despite a reproduced finding. An exception never relabels a verification status |
| `decision.limitations[]` | Optional |
| `provenance.artifactPath`, `provenance.commit` | Where and in which commit this decision is recorded |

## What a schema decides, and what the validator decides

A schema sees one document. Rules that compare two documents, or two lists in one document, or a
document with the answer key, belong to the cross-artifact validator. The examples are in
`examples/review-round/schema-cases/`, indexed by `cases.json`, which records whether each is
expected to pass or fail. Gate 18 runs `scripts/round-check.py --cases` on it, so a case that
drifts from its `expect` fails the gates.

| Validation matrix row | Schema | Validator |
|---|---|---|
| `valid-complete-round` | Each document passes | Round IDs, alignment, citations agree |
| `valid-no-findings-when-answer-key-allows` | Each document passes | The answer key expects no findings |
| `valid-verification-rejects-finding` | Each document passes | The rejected finding is not cited |
| `reviewed-wrong-revision` | A mismatched or unresolved alignment with a normal decision fails; `matched` with a null revision fails | The two revisions are compared with the round and report |
| `self-verification` | A report that marks its own finding verified fails | The decision's verifier role differs from the report's reviewer role |
| `decision-cites-unverified-finding` | Not decidable | Every cited ID is reproduced in `verification.findings` |
| `missing-verification-evidence` | A reproduced finding without evidence fails | Also for cited findings |
| `missing-check-status` | A check without a listed status fails | Every required check has a result |
| `missing-answer-key-expectation` | Not decidable | The answer key has an expected-finding criterion |
| `unqualified-accept-with-reproduced-blocker` | Not decidable | Acceptance with a reproduced blocker needs an exception |
| `relay-required` | No schema requires a relay or routing field | The validator requires none either |

Structural validation checks declared roles. It cannot prove organizational, social or cognitive
independence, nor that a person performed each claimed observation.

## Keywords used

`type`, `required`, `properties`, `additionalProperties` (always `false`), `enum`, `const`,
`pattern`, `format` (`date-time`), `items`, `minItems`, `minLength`, `minimum`, `$ref` within the
file, and `if` with `then`. All are draft-07 keywords, so a full draft-07 validator applies the
same rules.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
