---
name: pass-options-carried
rules: 4 6
note: new; open Q2 carries its option lines re-indented and in another order, which keeps every digit's meaning; answered Q3 takes new options
# SPDX-FileCopyrightText: 2026 Aidan Naveja
# SPDX-License-Identifier: Apache-2.0
---

<!-- previous:
Q1. Commit the staged set as one commit? (f / d)
Q2. Which register does the archive read? (1 / 2 / d)
    1 = merge the current register in first
    2 = use the register as it stands
Q3. Where does the finding go? (1 / 2 / d)
    1 = the flag log
    2 = the session log
-->
Readback: Q1 f (commit); Q3 1 (the flag log).

Committed as one commit and logged.

Q1. Push the branch now? (f / d)
Q2. Which register does the archive read? (1 / 2 / d)
  2 = use the register as it stands
  1 = merge the current register in first
Q3. Tag which release? (1 / 2 / d)
    1 = the release candidate
    2 = the final release
