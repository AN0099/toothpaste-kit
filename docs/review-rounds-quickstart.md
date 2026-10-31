# Review-round quickstart

The steps to run one review round, from the round packet to the operator's decision. What each
record means, and what the checks cannot show, is in [Review rounds](review-rounds.md). That page
is reference, not a step: you can start here and look up a record or a check there when a step
needs it. Read [What validation can and cannot show](review-rounds.md#what-validation-can-and-cannot-show)
before you rely on a passing check.

Each step is marked with its kind:

- **[person]**: someone decides or judges. No script does this part, and a passing check does not
  stand in for it.
- **[script]**: a command does it, and its output is evidence for the next person step.

Run every command from the repository root. Nothing here needs a network connection, a secret or
an account. Keep the three records of one round in one directory, named `review-round.json`,
`review-report.json` and `operator-decision.json`. The kit does not fix where that directory is,
and ignores none: a round directory inside a kit checkout shows as untracked files there, so
commit it in the repository it belongs to. For the practice round, that is a scratch repository of
its own; see [Practising on the fixture](#practising-on-the-fixture).

## Before you start

1. **[script]** Check that the validator works on this machine:

   ```sh
   python3 scripts/round-check.py --selftest
   ```

   You should now see a line ending `cases behaved`, and the command exits 0. It needs Python 3
   and nothing else.

## Create the round

2. **[person]** Decide what is to be reviewed: the base and target commits, the paths in scope,
   what the change is meant to do, the checks the reviewer must run, and the round's network,
   secrets and remote-access posture. Name the reviewer's and the verifier's roles; they must
   differ. A role is one of the four in `orchestration/ROLES.md`: `operator`, `lead`, `aide` or
   `minion`, and the validator rejects any other name. The decision maker is always `operator`.
   The practice round uses `aide` for the reviewer and `lead` for the verifier, and its packet is
   already written: see [Practising on the fixture](#practising-on-the-fixture).
3. **[person]** Write `review-round.json`. Its fields are in two tables of
   [The three records](review-rounds.md#the-three-records): "Every record has", which every record
   needs, and "ReviewRound", for the packet's own fields. Its schema is
   `orchestration/schemas/round/review-round.json`.
4. **[script]** Validate it, then commit it:

   ```sh
   python3 scripts/round-check.py path/to/round-dir
   ```

   You should now see `round-check: 1 round(s), 0 problem(s)`, and the command exits 0. If you
   see lines beginning `::error::` and it exits 1, see [Reading a failure](#reading-a-failure),
   fix the record and run it again. Then commit the record in the repository the round belongs
   to, on whatever branch that repository uses for its rounds; the kit does not choose one. Run
   from the kit, that is:

   ```sh
   git -C path/to/repo add round-dir/review-round.json
   git -C path/to/repo commit -m "Round <roundId>: packet"
   ```

   For the practice round, `path/to/repo` is `/tmp/tally-round` and `round-dir` is
   `tally-lines-1`. Steps 9 and 14 commit their records the same way.

## The reviewer's path

Steps 5 to 9 fill in one file, `review-report.json`, next to the packet in the round directory.
Start from the template rather than an empty file: copy
[`review-report.template.json`](../examples/review-round/reviewer/templates/review-report.template.json)
into the round directory as `review-report.json` and replace every `REPLACE`. The template already
has every required field, including the ones no step below mentions:

- `schemaVersion` and `kind`, which stay as they are;
- `metadata.id`, an id you choose for the report, and `metadata.roundId`, the packet's;
- `metadata.createdAt`, the time you finish, such as `2026-01-02T13:00:00Z`;
- `handling`, the same labels as the packet's;
- `reviewer.role`, your role;
- `provenance.artifactPath`, the report's path set as in step 4. For the practice round it is
  `tally-lines-1/review-report.json`, not the template's example.

For the practice round:

```sh
cp examples/review-round/reviewer/templates/review-report.template.json \
    /tmp/tally-round/tally-lines-1/review-report.json
```

5. **[script]** In the repository under review, not the kit, check out the target revision and
   record which commit you actually have:

   ```sh
   git -C path/to/reviewed-repo checkout --detach <targetRevision>
   git -C path/to/reviewed-repo rev-parse HEAD
   ```

   For the practice round, the repository is `/tmp/tally-review`. `build.sh` leaves it at the
   target already, so the checkout changes nothing there, and running it does no harm.

   This hash goes in `reviewedRevision.revision`, and the command and its output go in
   `reviewedRevision.evidence` as an entry in a list, with a `description`; the shape and an
   example are under [The three records](review-rounds.md#the-three-records).

   If the hash is not the round's `targetRevision`, do not review a different commit as if it
   were the target. Keep the hash you actually have in `reviewedRevision.revision`, say in that
   evidence entry's `description` that it differs from the target, and add an entry to
   `limitations` naming both commits. The operator then records the alignment as `mismatched` at
   step 12, and the decision can only be `abstain` or `rerun`.
6. **[script]** Run each check in the round's `requiredChecks`, in the repository under review.
   Record each one as an entry in the report's `checks` list: `id` (the check's `id` in the
   packet) and `status` (`passed`, `failed`, `not-run` or `blocked`) are required, and `command`,
   `output` and `note` are optional. `failed` means it ran and reported failure; `blocked` means
   you tried and it could not run at all, such as a missing tool. A check you did not try is
   `not-run`, never left out. For `blocked` and `not-run`, say why in `note`.

   A check that passed is evidence about that check, not acceptance of the change. A check can
   pass while the change is wrong in a way the check does not test, so keep reviewing at step 7
   when every check passes. For the practice round:

   ```json
   "checks": [
     {
       "id": "selftest",
       "status": "passed",
       "command": "./check.sh --selftest",
       "output": "check: 4 cases passed"
     }
   ]
   ```
7. **[person]** Review the change: every file in the packet's `scope.paths`, documentation and
   comments as well as code. For each statement the change makes, about what the code does or
   what a check proves, ask whether it is true at the target revision. A wrong claim in prose is
   a finding like a wrong result in code.

   Write each problem as an entry in the report's `findings` list, with these fields, all
   required:

   - `id`: a name you choose for the finding, unique in the report. Like every id in the
     records, it uses only lower-case letters, digits, `.` and `-`, and starts with a letter or
     digit: `f1` or `parse-error`, not `F1` or `f_1`.
   - `severity`, one of the grades in [rounds](../orchestration/rounds.md):
     - `major`: a wrong result, or a broken rule, on input that ordinary use produces. It blocks
       the close.
     - `minor`: wrong only on unusual input, with a small and visible consequence, or a gap a
       reader would trip on.
     - `nit`: changes no real outcome, such as wording.
   - `location.path`, the file, relative to the root of the repository under review: in the
     practice round `tally.py`, not `/tmp/tally-review/tally.py`. The validator rejects an
     absolute path, a `..` segment, a backslash or a URL. `location.line` is optional.
   - `claim`: what is wrong, in one or two sentences.
   - `evidence`: a list of entries in the same shape as in step 5, that someone else can repeat.
   - `proposedRemedy`: what would fix it.
   - `verification`: exactly this object, as the template has it. You cannot verify your own
     finding; the verifier records that in a later record, and the validator rejects anything
     else here:

     ```json
     "verification": {"status": "unverified", "verifiedBy": null, "evidence": []}
     ```
8. **[person]** Write what the review did not cover in `limitations`, and your recommendation.
   `limitations` is a list of non-empty strings, one per thing you did not cover, and it must
   always be present: with nothing to declare, write `"limitations": []`, never leave it out.

   The recommendation is not a decision. It is an object with two required fields: `status`, one
   of `accept`, `reject`, `request-revision` or `no-recommendation`, and `rationale`, a non-empty
   string saying why. Nothing downstream depends on it: the verifier checks your findings, not
   your recommendation, and the operator decides at step 13 and may decide differently. The
   validator checks only its shape, not whether the decision agrees with it.
9. **[script]** Set `provenance.commit` to the commit you wrote the report against: `HEAD` of
   the repository the round is committed in, read before you commit the report. That is not the
   repository under review, whose commit is already in `reviewedRevision.revision`. For the
   practice round:

   ```sh
   git -C /tmp/tally-round rev-parse HEAD
   ```

   It prints the commit that added the packet at step 4. On its own the validator checks only
   that the value is a full commit hash (40 or 64 hex characters), so a hash from the wrong
   repository passes; step 14 shows how to have it check the commit exists. Then validate
   `review-report.json` as in step 4, and commit it.

## The verifier's path

The verifier is a different role from the reviewer.

10. **[person]** For each finding in the report, try to reproduce it against the reviewed
    revision, and keep your own evidence; the reviewer's evidence is not yours. Work in your own
    checkout at that revision, never in the reviewer's repository: reproducing a finding often
    means editing files, and an edit there changes the evidence under review. For the practice
    round, build a fresh copy with `examples/review-round/history/build.sh /tmp/tally-verify`.
    Record each with one status, chosen by what happened:

    - `reproduced`: you tried, and saw what the finding claims.
    - `not-reproduced`: the finding is about the reviewed revision and scope, you tried, and you
      did not see what it claims.
    - `not-applicable`: you did not need to try, because the finding is about something outside
      the round, such as a path not in `scope.paths` or code that is not in the reviewed
      revision.
    - `blocked`: the finding applies and you meant to try, but could not, for example for lack of
      a tool, an environment or access.

    A `reproduced` or `not-reproduced` entry needs at least one evidence item. For
    `not-applicable` and `blocked`, give the reason in `note`; the validator does not require it,
    but without it the operator cannot tell the two apart from a skipped finding.
11. **[person]** Record the result in the `verification` section of `operator-decision.json`,
    the third record, which the operator completes at steps 12 and 13. There is no fourth file,
    and the report's own `verification` blocks stay as the reviewer left them. Start from
    [`operator-decision.template.json`](../examples/review-round/verifier/templates/operator-decision.template.json),
    copied next to the other two records. The section has three required fields:

    - `performedBy.role`: your role;
    - `performedAt`: the time you finished, such as `2026-01-02T13:30:00Z`;
    - `findings`: one entry per finding you verified, each with `findingId` (the report
      finding's `id`), `status`, and `evidence` (a list in the same shape as step 5). `note` is
      optional. A finding with no entry is not an error, but the operator cannot cite it at
      step 13.

    This section is also the round's record of collection, the "Collect" step of
    [rounds](../orchestration/rounds.md): reading the reviewer's report from where it was handed
    back, not from memory of what was asked. In version 0.1 there is no separate collection
    record.

## The operator's path

12. **[person]** Copy the round's `targetRevision` and the report's `reviewedRevision.revision`
    into `alignment`, and set `alignment.status` to `matched` only if they are the same commit.
    Otherwise it is `mismatched`, or `unresolved` if either cannot be resolved. Resolve each one
    in a checkout of the reviewed repository, such as the verifier's from step 10:

    ```sh
    git -C /tmp/tally-verify rev-parse --verify --quiet "<revision>^{commit}"
    ```

    It prints the commit's full hash and exits 0, or prints nothing and exits 1 when the
    repository has no such commit; that is `unresolved`. Both fields hold full hashes, so a
    resolved revision prints itself back. The validator checks the copies and the comparison; it
    cannot see the repository, so only this command shows that a revision exists.

    Then fill `references`, which says which copies of the other two records the decision rests
    on. It has two required entries, `reviewRound` and `reviewReport`, each with `artifactPath`
    (the record's path, relative to the repository the round is committed in) and `commit` (the
    commit that added that version of it: step 4 for the packet, step 9 for the report). For the
    practice round:

    ```sh
    git -C /tmp/tally-round log -1 --format=%H -- tally-lines-1/review-round.json
    git -C /tmp/tally-round log -1 --format=%H -- tally-lines-1/review-report.json
    ```

    with `artifactPath` `tally-lines-1/review-round.json` and `tally-lines-1/review-report.json`.
    As with `provenance.commit`, the validator checks only the format unless it is given the
    repository (step 14).
13. **[person]** Decide, in the `decision` section. Set `decision.madeBy.role` to `operator`. If
    the alignment is `matched`, `decision.status` is `accept`, `reject` or `request-revision`, and
    `decision.basedOnFindings` lists the ids of the findings it rests on, each one the verifier
    recorded as `reproduced`. The list may be empty: for `abstain` or `rerun` it usually is, and a
    decision that rests on no reproduced finding, such as an `accept` of a clean report, has
    nothing to list. Then `decision.rationale` should say what the decision rests on instead. If
    the alignment is not `matched`, the only decisions open are `abstain` and `rerun`. To
    accept despite a reproduced `major` finding, add an entry to the list `decision.exceptions`
    with two required fields, `findingId` (the finding's id) and `reason` (why you accept it, not
    blank):

    ```json
    {"findingId": "parse-error", "reason": "Accepted for this release; the fix is tracked."}
    ```

    Write the reason for the decision in words in `decision.rationale`.
14. **[script]** Validate the round directory, then commit `operator-decision.json`:

    ```sh
    python3 scripts/round-check.py path/to/round-dir
    ```

    You should now see `round-check: 1 round(s), 0 problem(s)`, and the command exits 0. That
    means the three records are well formed and consistent. It does not mean the decision is
    right; that stays the operator's.

    The commits the records cite are checked only for format, unless you also give the
    repository the round is committed in. Then each `provenance.commit` must be a commit there,
    and each `references` commit must hold the record at its `artifactPath`. For the practice
    round:

    ```sh
    python3 scripts/round-check.py --repo /tmp/tally-round /tmp/tally-round/tally-lines-1
    ```

## Reading a failure

The validator prints one line per problem, beginning `::error::`, then the count line, and exits 1.
A problem between records names the round, the record and the rule it broke; a problem within
one record names the file and the field path, such as `schema: $: missing required field 'kind'`.
Fix that record and run the command again. Exit 2 means the command was used wrongly or a schema
could not be loaded, not that a record is wrong.

A failure is about the records, not about the people. A verifier role equal to the reviewer's, or
a decision citing a finding that was not reproduced, is a failure even when the work behind it was
careful, because the record does not show the independence the round requires.

## Practising on the fixture

`examples/review-round/` holds a practice round with a planted defect. The change under review is
not in the kit: build it into a fresh repository first.

```sh
examples/review-round/history/build.sh /tmp/tally-review
```

You should now see the base and target revisions, and a last line
`build.sh: revisions match revisions.json`. The directory must not exist yet: if it does,
`build.sh` changes nothing, says `already exists; give a path that does not` and exits 2. For a
second practice run, give new paths, or delete `/tmp/tally-review` and `/tmp/tally-round` from the
first run if you no longer need them. The target is the commit you review; steps 5 and 6
run in that repository, not in the kit.

The practice round's records belong to no project, so give them a scratch repository of their own,
outside the kit, and commit each record there when a step says to commit it:

```sh
git init /tmp/tally-round
```

Keep the round directory in it, for example `/tmp/tally-round/tally-lines-1`, and run the
validator from the kit with that path. Every commit a record cites, in `provenance.commit` or
`references`, is a commit in `/tmp/tally-round`, and every path a record names, such as
`provenance.artifactPath`, is relative to it: `tally-lines-1/review-round.json`, not the kit's
`examples/review-round/reviewer/review-round.json` that the copied packet still carries.

Steps 2 and 3 are already done for the practice round: its packet,
`examples/review-round/reviewer/review-round.json`, fixes the revisions, the scope, the intent, the
roles and the required checks. Copy it into your round directory rather than writing your own; a
packet of your own would not match the answer key, and the answer-key checks would fail for reasons
the reviewer cannot see. Step 4 still applies to the copy: set its `provenance.artifactPath` as
above, validate it, and commit it in `/tmp/tally-round`.

For the practice round, the reviewer follows `examples/review-round/reviewer/README.md` in place
of steps 5 to 9 here; it covers the same steps for this fixture, and where the two differ, it
takes precedence. The one exception is where it makes the round directory: use
`/tmp/tally-round/tally-lines-1` as above rather than `rounds/` inside the kit. The reviewer
reads no other material under `examples/review-round/`, the answer key included. The verifier
and the operator follow `examples/review-round/verifier/README.md`, which holds the answer key's
checklist; `verifier/expected/` is a completed round to compare against. The answer key is in a
separate directory so the reviewer is not handed it. It is not hidden: anyone who can read the
repository can read it.

The packet the reviewer copies has no `fixture.answerKey`, so validating the practice round runs
none of the answer-key checks: 0 problems then says nothing about whether the review found the
planted defect, and a report with no findings passes. To run them, the verifier validates a copy
of the round whose packet names the key, as `verifier/expected/review-round.json` does. Leave the
committed packet as it is, since the decision's `references` cite it. From the kit root:

```sh
cp -r /tmp/tally-round/tally-lines-1 /tmp/tally-keyed
python3 - <<'PY'
import json
p = "/tmp/tally-keyed/review-round.json"
d = json.load(open(p))
d["fixture"] = {"answerKey": "examples/review-round/verifier/answer-key.json"}
json.dump(d, open(p, "w"), indent=2)
PY
python3 scripts/round-check.py /tmp/tally-keyed
```

The key's path is relative to the kit, so run the validator from the kit. A report that misses
the planted defect then fails, with `no-findings-against-planted-defect` when it has no findings
and `required-finding-missing` when none is where the key expects. Delete `/tmp/tally-keyed`
afterwards.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
