# End-to-end tests

`tests/e2e/run` runs the review-round workflow end to end: the fixture rounds under
`examples/review-round/`, each a proposed change with planted defects, a review report and the
operator's decision, checked by `scripts/round-check.py` against the schemas in
`orchestration/schemas/round/` and the answer keys. The workflow is described in
`docs/review-rounds.md`.

The same steps run in CI as the "review-round records" gate of `scripts/gates.sh`, so
`tests/run` covers this too; this entry point runs them alone.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
