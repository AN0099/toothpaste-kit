# Standards

The operator's own standards for writing and publishing.

- `style-guide.md`: how the desk's writing reads.
- `data-display.md`: how the desk shows data, adopted from Tufte's four books.
- `technical-writing.md`: procedures, descriptions, notes and warnings, adopted from ASD-STE100.
- `records.md`: what the desk keeps, and how, adopted from Army records practice.
- `continuity.md`: what a role or seat hands over so someone else can finish the work.
- `risk.md`: how a hazard is assessed, mitigated, accepted and closed, adopted from MIL-STD-882E.
- `editorial-policy.md`: who writes, who edits and who answers for a published piece.
- `plaintext-messages.md`: messages where Markdown does not render.

## Upkeep

The words SHALL, SHOULD and MAY have the meanings BCP 14 (RFC 2119, RFC 8174) gives them, only
when they appear in all capitals.

Each standard SHOULD be reviewed at least once a year, with a stated way to change it and a check
that it is followed (ATP 6-01.1 paras 3-39, D-4). Each revision SHOULD carry a summary of changes
(MIL-STD-962D para 5.12.11).

Where a standard and its source differ, the standard governs for the adopting tree, and no standard overrides
law (para 5.8.4). A retired standard SHALL be marked inactive for new work and name its replacement
(para 5.19.2).

## Conformance

Each standard ends with a conformance table naming every requirement, its keyword and its check:
**mechanical** checks are in `scripts/style-check`, which `scripts/gates.sh` runs as gate 23 on
this directory; **review** checks are read by a second reader; **judgment** rows claim no check.
The tables carry no status column, since a status describes one tree. A tree that adopts these
standards records its own status against each row.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
