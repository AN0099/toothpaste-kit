# Tests

The test suite is `scripts/gates.sh --selftest`, the same command CI runs. Run it with `tests/run`
from the repository root, or by its path from anywhere. What each gate covers, and how each is shown
able to fire (by a planted positive, or by the tool's own selftest) before a clean result is
trusted, is in the header of `scripts/gates.sh` and in `CONTRIBUTING.md`.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
