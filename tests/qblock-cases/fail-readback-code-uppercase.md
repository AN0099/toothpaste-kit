---
name: fail-readback-code-uppercase
rules: 8
note: new; Q1's code read back in uppercase without its meaning, found by a second agent's probe
# SPDX-FileCopyrightText: 2026 Aidan Naveja
# SPDX-License-Identifier: Apache-2.0
---

<!-- previous:
Q1. Commit the staged set as one commit? (f / d)
Q2. Which register does the archive read? (1 / 2 / d)
    1 = merge the current register in first
    2 = use the register as it stands
Q3. Record the finding in the flag log? (f / j / d)
-->
Readback: Q1 F; Q2 2 (use the register as it stands); Q3 d (do not record).

Committed as one commit.

Q1. Push the branch now? (f / d)
Q2. Open the pull request as a draft? (f / d)
Q3. Tag the release? (f / d)
