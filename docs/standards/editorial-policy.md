# Editorial policy

## § 1. Scope

(a) This standard applies to anything published under the operator's name.

(b) Section 4's disclosure requirements for arXiv take their concepts from arXiv's moderation
policy on generative AI, as read 2026-11-05. The wording is the desk's own.

(c) In this standard, the words SHALL, SHALL NOT, SHOULD, SHOULD NOT, and MAY have the meanings
that BCP 14 (RFC 2119, RFC 8174) gives them. They have these meanings only when they appear in all
capitals.

## § 2. Authorship

(a) The operator SHALL be the sole author, and answers for every sentence.

(b) An AI SHALL NOT be named as an author or held at fault.

(c) An agent SHALL NOT sign off.

(d) No text SHALL become final without the operator's approval.

Notes: (a) follows arXiv's rule that each author answers in full for the contents, however they
were generated. (b) follows its rule that an AI tool is not listed as an author. Its rule that
errors in AI output are the author's supports never holding an AI at fault. (c) and (d) are the
desk's own.

## § 3. Editing

(a) The default track SHALL be this.

(1) The operator types rough prose.

(2) The lead copy-edits it to `style-guide.md`.

(3) The operator accepts each change.

(b) The lead SHALL NOT add a claim, fact or sentence of its own.

(c) A paper SHALL make one claim.

(d) A paper SHOULD be small and highly concise.

Notes: section 3 is the desk's own.

## § 4. Disclosure

(a) Subsections (b) to (g) apply to a paper on arXiv. They are on trial since 2026-11-05.

(b) A sentence passes the trace check when it traces to one the operator wrote.

(c) A paper whose AI help is copy-editing of the operator's own prose, and whose every final
sentence passes the trace check, MAY carry no statement.

(d) Where a sentence an AI wrote fails the trace check, the paper SHALL state it, or the sentence
SHALL be rewritten until it passes.

(e) AI used as the subject, an instrument, or part of the method SHALL be reported in full, with
the tool and version named.

(f) AI that writes analysis code, or produces results or figures, SHALL be reported.

(g) In a paper that studies the desk's own writing or editing workflow, the copy-edit SHALL be
reported.

(h) For any other venue, the venue's current policy SHALL be read at submission.

(i) A paper going to a venue and to arXiv SHALL meet both.

Notes: arXiv requires any significant use of a sophisticated tool to be reported, text-to-text
generative AI included, by the standards of the subject's methodology. It does not define
significant. (b) to (d) are the desk's reading of that line. (e) and (f) follow the duty to report
tools used in the research itself. (e) and (g) report AI use because it is then the paper's data.

## § 5. Pending

(a) The other editing tracks, the per-paper ledger and the cadence ladder SHALL join this standard
only once the operator accepts them.

Notes: all three come with a one-page workflow draft, due after the 0.6.0 tag and not yet written.
4(c) relies on the ledger, which does not exist yet.

## Appendix A. Conformance

Check kinds: **review** is an item a second reader checks by reading. **Judgment** has no check,
and none is claimed.

No mechanical check is built yet. Five requirements could take one. 1(c) could take a grep for the BCP
14 line. 2(a) and 2(b) could take a check that each paper's author list holds the operator alone
and no AI. 4(c) and 4(d) could take a tool that matches each final sentence against the
operator's typed prose, which would apply the trace check of 4(b). Such checks show presence or a
match only, and whether the content is right stays review.

| Requirement | Keyword | Check kind | Check |
|---|---|---|---|
| 1(a), 1(b) | none | judgment | scope statements |
| 1(c) | none | review | BCP 14 citation present |
| 2(a) to 2(d) | SHALL, SHALL NOT | review | sole author, no AI named, no agent sign-off, operator approval |
| 3(a), 3(b) | SHALL, SHALL NOT | review | the track followed, no claim added by the lead |
| 3(c) | SHALL | review | one claim per paper |
| 3(d) | SHOULD | review | small and concise |
| 4(a), 4(b) | none | judgment | scope and definition |
| 4(c) to 4(g) | MAY, SHALL | review | the statement or report each case asks for |
| 4(h), 4(i) | SHALL | review | the venue's policy read and met |
| 5(a) | SHALL | review | nothing pending used before it is accepted |

## Changes

First edition in this repository.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
