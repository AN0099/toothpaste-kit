# Records

## § 1. Scope

(a) This standard applies to what the desk keeps in its durable store.

(b) The requirements take their concepts from AR 25-400-2 (2022, change 1), DA Pam 25-403 (2022),
and ATP 6-01.1. The desk is not a Federal agency, so these are adopted practices and not
compliance with any of them. The wording is the desk's own.

(c) This standard sets no retention periods. Each one needs a stated decision by the operator.
It does not cover agency approval of schedules, ARIMS, record numbers, the Army's retention
labels, or permanent status for wartime and contingency records.

(d) In this standard, the words SHALL, SHALL NOT, SHOULD, SHOULD NOT, and MAY have the meanings
that BCP 14 (RFC 2119, RFC 8174) gives them. They have these meanings only when they appear in all
capitals.

## § 2. Categories

(a) A record is evidence of a decision, procedure, or operation, in any medium.

(b) A non-record is an extra copy kept only for reference. They are kept apart from records.

(c) A personal paper is material not used to conduct the work. Personal papers SHALL be filed
apart from records.

(d) An item whose category is in doubt SHALL be treated as a record.

(e) A record is temporary or permanent.

(f) A short-term record has no value beyond the work that made it. A long-term record holds value
beyond that work, such as legal or historical value, or a lesson learned.

Notes: (a) follows AR 25-400-2 para 3-2b, (b) para 3-3a, (c) para 3-4a, and (d) para 3-3b. (e)
follows para 3-2e, and (f) DA Pam 25-403 para 3-2d(4)(e).

## § 3. Disposition

(a) A record held in more than one place SHALL have one identified record copy.

(b) A record with no stated disposition SHALL be kept.

(c) A record SHALL NOT be destroyed except under a stated disposition.

(d) A disposition SHALL run by time, by an event, or by both. A record waiting on an event SHALL
name the event.

(e) A retention period SHALL begin at a cutoff. A record past its cutoff SHALL take no additions.

(f) Destruction SHALL have the owner's approval, given after notice.

(g) A hold SHALL stop destruction until whoever placed it lifts it.

(1) When a hold is lifted, disposition SHALL run from the record's original date, not from the
end of the hold.

Notes: (a) follows DA Pam 25-403 para 2-9a. (b) follows AR 25-400-2 paras 3-6 and 4-1, and (c)
para 3-9a. (d) follows DA Pam 25-403 para 7-7b, (e) para 7-6, and (f) para 7-14a. (g) follows AR
25-400-2 para 6-1, and (g)(1) DA Pam 25-403 para 10-4e.

## § 4. Loss and continuity

(a) A lost record SHALL be reported and rebuilt from other copies. A list SHALL name what cannot
be rebuilt.

(b) A record made in an unofficial channel SHOULD reach the official store within a stated time.

(c) Records needed to resume work are essential records. They SHALL be named and duplicated off
site, and access to them SHALL be tested twice a year.

(d) Before a system or format is retired, its records and their metadata SHALL move to one that
keeps them usable.

(e) A list that links people to roles or access SHALL have one record copy, and no other copy
outside its tier.

Notes: (a) follows DA Pam 25-403 para 7-12e. (b) follows para 4-1c(3), which sets 20 days for
its own case. (c) follows paras 11-2, 11-6, and 11-7b, and (d) para 4-9c(2). (e) is the desk's
own. Such a list does the most harm if lost.

## § 5. Description and finding

(a) A record SHOULD state who made it and when, and who may change it. It SHOULD state its one
location, and whether it is draft, checked, or final.

(b) A name SHOULD carry a date and a subject. A recurring product SHALL keep one name.

(c) A low-use or expired item SHOULD be reviewed for archive.

(d) The items most needed SHOULD sit one step from an index.

(e) A search that finds nothing SHOULD be recorded.

Notes: (a) follows ATP 6-01.1 paras 3-29 and 3-74, and its status follows para A-8 and table A-2.
(b) follows para 3-70, (c) paras 1-15, A-10, and A-11, (d) para 3-31, and (e) para A-25. The
reason for (e) is the desk's own: a failed search marks a gap in the index.

## § 6. Lessons

(a) A lesson SHALL count only once it is checked and tied to a change in behavior.

(b) A lesson SHOULD be recorded near the event, in one repository. It SHOULD set what happened
against what should have happened.

Notes: (a) and the one repository in (b) follow ATP 6-01.1 paras 4-24 to 4-27. The comparison in
(b) follows para 1-13, which holds the review after an event. "Near the event" is the desk's
reading of it.

## § 7. Controls

(a) A system that holds records SHOULD provide each control below, built into the system or kept
beside it.

| Control | Ensures |
|---|---|
| Reliability | A full and accurate account that later work can depend on |
| Authenticity | Nothing is added, removed, changed, used, or hidden without authority |
| Integrity | Complete and unaltered, shown by audit trails |
| Usability | A reader can find, open, show, and understand it |
| Content | The information the creator produced is preserved |
| Context | Cross-references show the circumstances of the record |
| Structure | Format and the relationships between data elements are maintained |

Notes: the seven controls are AR 25-400-2 para 4-4a.

## Appendix A. Conformance

Check kinds: **review** is an item a second reader checks by reading. **Judgment** has no check,
and none is claimed.

No mechanical check is built yet. Four rows could take one. 1(d) could take a grep for the BCP
14 line. 3(a) and 4(e) could take content hashes across the store. The first sentence of 5(b) could
take a date pattern in the file name.

| Requirement | Keyword | Check kind | Check |
|---|---|---|---|
| 1(a) to 1(c) | none | judgment | scope statements |
| 1(d) | none | review | BCP 14 citation present |
| 2(a), 2(b), 2(e), 2(f) | none | judgment | definitions |
| 2(c), 2(d) | SHALL | review | personal papers apart, doubt read as a record |
| 3(a) | SHALL | review | one record copy named for a record held twice |
| 3(b), 3(c) | SHALL, SHALL NOT | review | nothing destroyed without a stated disposition |
| 3(d), 3(e) | SHALL | judgment | no disposition is stated yet, by 1(c) |
| 3(f), 3(g), 3(g)(1) | SHALL | review | approval and holds, at each destruction |
| 4(a) | SHALL | review | a loss report and its list |
| 4(b) | SHOULD | judgment | no time is stated yet |
| 4(c) | SHALL | review | essential records named, copied off site, access tested |
| 4(d) | SHALL | review | a migration before a retirement |
| 4(e) | SHALL | review | one record copy of each list of people |
| 5(a) to 5(e) | SHOULD, SHALL | review | description, names, archive, index, failed searches |
| 6(a), 6(b) | SHALL, SHOULD | review | a lesson's check and change |
| 7(a) | SHOULD | review | the seven controls, per system |

## Changes

First edition in this repository.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
