# Plaintext messages

## § 1. Scope

(a) This standard applies to a message sent where Markdown does not render, such as Signal.

(b) This standard does not apply where a variation of Markdown renders, such as Discord.

(c) In this standard, the words SHALL, SHALL NOT, SHOULD, SHOULD NOT, and MAY have the meanings
that BCP 14 (RFC 2119, RFC 8174) gives them. They have these meanings only when they appear in all
capitals.

## § 2. Markup

(a) The writer SHALL strip markup that shows as text, such as bold, backticks, and headings.

(b) The writer SHALL keep `- ` list items.

Notes: A hyphen reads as plain text, so removing it over-strips.

## § 3. Layout

(a) A blank line SHALL follow a numbered title (`1. Title`), before its body.

(b) A blank line SHALL follow a lead-in (`What I need from you:`), before its list.

(c) Each paragraph SHALL be one line, with no hard wraps.

Notes: These requirements rest on a reviewed edit of a plaintext message.

## § 4. Content

(a) First person SHALL follow who speaks.

  (1) A solo desk SHALL write "I" and "my".

  (2) The writer SHALL use "our" only for the two parties together.

(b) A message SHALL NOT state what both parties already know.

Notes: A message is a concise communication, not a record.

## Appendix A. Conformance

Check kinds: **mechanical** is a check in `scripts/style-check --plaintext`, named by
the requirement it enforces, each with a planted positive and a clean negative in `--selftest`.
**Review** is an item a second reader checks by reading. **Judgment** has no check, and none is
claimed.

| Requirement | Keyword | Check kind | Check |
|---|---|---|---|
| 1(a), 1(b) | none | judgment | scope statements |
| 1(c) | none | review | BCP 14 citation present |
| 2(a) | SHALL | mechanical, review | `P2a` reads `**` or `__` closed on the same line, a backtick, a line opening on one to six `#` and a space, an `=` underline under a text line, and a line of three or more `*` or `_` alone, and other markup by review |
| 2(b) | SHALL | review | each `- ` item of the draft is kept |
| 3(a) | SHALL | mechanical | `P3a` a numbered line outside a numbered list, followed by a non-blank line that is not numbered at any indent |
| 3(b) | SHALL | mechanical | `P3b` a line ending in a colon followed by a non-blank line |
| 3(c) | SHALL | mechanical | `P3c` a non-blank line after a non-blank line, unless it opens a list item after a break, an item, or a sentence end before any straight or curly closing quote, or follows a line `P3a` or `P3b` reads |
| 4(a) | SHALL | review | first person follows who speaks, by 4(a)(1) and 4(a)(2) |
| 4(a)(1), 4(a)(2) | SHALL | review | "I" and "my" for a solo desk, "our" only for both parties |
| 4(b) | SHALL NOT | judgment | what both parties know |

## Changes

First edition in this repository.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
