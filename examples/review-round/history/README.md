# Fixture history

The two commits of the practice project `tally`, as patch files, and the script that builds them.

- `0001-baseline.patch`: the base revision, the project before the change.
- `0002-proposed-change.patch`: the target revision, the change under review. Its blank context
  lines end in whitespace, as a diff's do; stripping it would change the commit it builds.
- `build.sh DIR`: builds both commits into a new repository at `DIR`, which must not exist yet. It
  fixes the author, committer and dates and reads none of your Git configuration, so the hashes
  are the same on every run, and it ends by comparing them with `revisions.json`.
- `revisions.json`: the expected `baseRevision` and `targetRevision`, which the round packets copy.

```sh
examples/review-round/history/build.sh /tmp/tally-review
```

Build outside the kit checkout, so the fixture's repository is not nested inside this one.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
