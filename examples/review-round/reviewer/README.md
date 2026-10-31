# Review round fixture: the reviewer path

You are the reviewer (role `aide`) in a practice review round. The change under review is in a small
synthetic project called `tally`. Your job is to find what is wrong with the change, show evidence
for each finding, and recommend an outcome. Someone in another role checks your findings afterwards.

Everything you need is in this directory and in `examples/review-round/history/`. Nothing here needs
a network, an account, a secret or an AI model: only `git`, `sh` and `python3`.

Other material under `examples/review-round/` belongs to other roles in the exercise. It is public,
so nothing stops you reading it, but reading it before you finish defeats the practice. The
separation is instructional, not access control.

## What is here

- `review-round.json`: the round packet. It names the base and target revisions, the scope, the
  roles, the required checks and the restrictions.
- `templates/review-report.template.json`: the report you fill in. Every `REPLACE` is yours to
  replace.

## Steps

Run these from the root of this repository.

1. Build the fixture repository into a directory that does not exist yet:

   ```sh
   examples/review-round/history/build.sh /tmp/tally-review
   ```

   It prints `baseRevision` and `targetRevision` and ends with `revisions match revisions.json`.
   Check that `targetRevision` is the one in `review-round.json`.

2. Read the change:

   ```sh
   git -C /tmp/tally-review diff HEAD~1 HEAD
   ```

   Read the files in the packet's `scope.paths` at the target revision as well. Ask whether each
   statement the change makes is true.

3. Run each required check from the packet in the fixture repository, and keep its output:

   ```sh
   cd /tmp/tally-review && ./check.sh --selftest
   ```

   A check that passes is evidence about that check, not acceptance of the change.

4. Make a round directory and copy the packet into it, then copy the template there as
   `review-report.json` and fill it in:

   ```sh
   mkdir -p rounds/tally-lines-1
   cp examples/review-round/reviewer/review-round.json rounds/tally-lines-1/
   cp examples/review-round/reviewer/templates/review-report.template.json \
       rounds/tally-lines-1/review-report.json
   ```

   The commands run from the kit checkout, so `rounds/` is made inside it. The kit ignores no
   round directory, so it shows as untracked files there. Delete it when the round is done, or
   commit it in the repository the round belongs to.

   - `reviewedRevision.revision` is the output of `git -C /tmp/tally-review rev-parse HEAD`.
   - Give every required check an entry in `checks` with its status: `passed`, `failed`, `not-run`
     or `blocked`.
   - Give each finding evidence that someone else can repeat. Leave its `verification` as the
     template has it: unverified, `verifiedBy` null, no evidence. You cannot verify your own finding.
   - A report with no findings is allowed, if you found nothing.
   - Say in `limitations` what you did not check.

5. Check the round directory:

   ```sh
   python3 scripts/round-check.py rounds/tally-lines-1
   ```

   It exits 0 when the documents are well formed and agree with each other. That says nothing about
   whether your review found the right things; the next role in the round decides that.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
