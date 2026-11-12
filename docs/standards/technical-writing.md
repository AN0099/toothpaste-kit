# Technical writing

## § 1. Scope

(a) This standard applies to text a person acts on or relies on to run something. That text is
a procedure, a runsheet, a description of how a system works, a note, or a warning.

(b) `style-guide.md` governs where this standard is silent.

(c) In this standard, the words SHALL, SHALL NOT, SHOULD, SHOULD NOT, and MAY have the meanings
that BCP 14 (RFC 2119, RFC 8174) gives them. They have these meanings only when they appear in all
capitals.

(d) Desk text does not claim conformance to ASD-STE100.

Notes: Taken from the writing rules in ASD-STE100 Issue 9, Part 1 (2025-01-15). The wording here is
the desk's own. The source's rule numbers are given in the notes to each section.

## § 2. Procedures

(a) An instruction SHALL use the imperative.

(b) A sentence SHALL carry one instruction, unless the actions occur at the same time.

(c) The length of a sentence SHOULD be not greater than 20 words.

(d) A condition SHALL come before its command, closed by a comma: "When the gate passes, stage the
patch."

(e) Notes.

  (1) A note SHALL give information only.

  (2) A note SHALL NOT use the imperative, or set a requirement or limit.

(f) Complex text SHOULD be a vertical list.

(g) A procedure SHALL name each of the following:

  (1) who runs each task

  (2) the action to take if a likely change of circumstances occurs

  (3) to whom the runner reports completion

Notes: ASD-STE100 rules: (a) 5.3, (b) 5.2, (c) 5.1, (d) 5.4, (e) 5.5, (f) 4.3. Requirement (g) is
ATP 6-01.1 para G-6.

## § 3. Descriptions

(a) A sentence SHALL have one topic.

(b) Information SHOULD arrive gradually.

(c) The length of a sentence SHOULD be not greater than 25 words.

(d) A paragraph SHALL have one topic.

(e) The number of sentences in a paragraph SHOULD be not greater than six.

(f) Transition words SHOULD mark the structure of the text.

(g) A writer MAY use the passive only where the actor is unknown.

Notes: ASD-STE100 rules: (a) 4.1, (b) 6.1, (c) 6.3, (d) and (e) 6.4 to 6.6, (f) 6.2, (g) 3.6.

Requirement (g) is tighter than `style-guide.md`, since a reader acting on the text has to know who
does what.

## § 4. Warnings

(a) A warning SHALL open with a word that names the level of risk.

(b) A warning SHALL state a clear command or condition first.

(c) A warning SHOULD state the risk or the result.

Notes: ASD-STE100 rules: (a) 7.1, (b) 7.2, (c) 7.3.

## § 5. Language

(a) A verb SHALL describe an action: "inspect the log", never "do an inspection of the log".

(b) A writer SHALL NOT omit words to shorten a sentence.

(c) A writer SHALL NOT use contractions.

(d) A noun SHOULD take an article or a demonstrative where one applies.

(e) The length of a multi-word noun SHOULD be not greater than three words, and a writer writes a
longer technical noun in full.

(f) Technical nouns.

  (1) A technical noun SHOULD be short and known in its field.

  (2) A technical noun SHALL NOT be slang or used as a verb.

(g) One item SHALL have one name throughout.

(h) A one-word verb SHOULD replace a phrasal verb.

(i) A writer SHALL NOT use semicolons.

(j) Language SHALL be gender-neutral.

Notes: ASD-STE100 rules: (a) 3.7, (b) and (c) 4.2, (d) 4.5, and (e) 2.1 and 2.2. The rules for
(f) are 1.7 to 1.10, (g) 1.11 and 9.4, (h) 9.3, (i) 8.1, and (j) GR-7.

## § 6. AI-assisted writing

(a) An agent SHALL assist and a person SHALL answer for the result, as `editorial-policy.md`
states.

(b) An agent's text SHALL be checked against its sources before anyone relies on it.

(c) Sensitive material SHALL stay under the desk's tier rules before it reaches any model.

Notes: Taken from the STE Maintenance Group's white paper on ASD-STE100 and artificial
intelligence, June 2026, which is advice.

The paper names variable accuracy, weakened terminology
control, and limited traceability as the risks behind (b). An automated check for these rules gives
evidence of conformance, and its accuracy varies.

## § 7. Outside this standard

(a) The desk does not adopt the Part 2 dictionary, or any rule not cited above, including those
that depend on it. A controlled vocabulary needs a term list and a checker the desk does not have.

(b) The desk does not adopt the paper's advice to mark AI-assisted content, since
`editorial-policy.md` decides disclosure by venue.

## Appendix A. Conformance

Check kinds: **mechanical** is a check in `scripts/style-check --technical`, named by the
requirement it enforces, each with a planted positive and a clean negative in `--selftest`.
**Review** is an item a second reader checks by reading. **Judgment** has no check, and none is
claimed.

| Requirement | Keyword | Check kind | Check |
|---|---|---|---|
| 1(a), 1(b), 1(d) | none | judgment | scope statements |
| 1(c) | none | review | BCP 14 citation present |
| 2(a) | SHALL | review | each instruction is imperative |
| 2(b) | SHALL | review | one instruction per sentence |
| 2(c) | SHOULD | mechanical, review | `T3c` flags a sentence greater than 25 words, and 21 to 25 in a procedure by review |
| 2(d) | SHALL | review | condition first, closed by a comma |
| 2(e)(1), 2(e)(2) | SHALL, SHALL NOT | review | each note informs only |
| 2(f) | SHOULD | judgment | what is complex |
| 2(g) | SHALL | review | runner, contingency, report-to named |
| 3(a), 3(d) | SHALL | review | one topic per sentence and paragraph |
| 3(b), 3(f) | SHOULD | judgment | order and structure words |
| 3(c) | SHOULD | mechanical | `T3c` sentence greater than 25 words |
| 3(e) | SHOULD | mechanical | `T3e` paragraph of more than six sentences |
| 3(g) | MAY | review | each passive has an unknown actor |
| 4(a), 4(b), 4(c) | SHALL, SHOULD | review | level word, command first, risk stated |
| 5(a), 5(b), 5(d), 5(h) | SHALL, SHALL NOT, SHOULD | review | verbs, omitted words, articles, phrasal verbs |
| 5(c) | SHALL NOT | mechanical, review | `T5c` n't, 're, 've, 'll, 'm, and 'd, and 's after 13 listed words, outside quotes, and any other 's and quoted text by review |
| 5(e), 5(f)(1) | SHOULD | judgment | noun length and currency in the field |
| 5(f)(2), 5(g) | SHALL NOT, SHALL | review | slang, nouns as verbs, one name per item |
| 5(i) | SHALL NOT | mechanical, review | `T5i` semicolon, U+037E, or U+FF1B outside code, quotes, entities that do not render one, and URLs opening on `http`, `https`, or `www.`, and quoted text by review |
| 5(j) | SHALL | mechanical, review | `T5j` eight gendered pronouns outside quotes, and quoted text, a pronoun a person states, and other gendered wording by review |
| 6(a), 6(b), 6(c) | SHALL | review | person answers, sources checked, tier rules kept |
| 7(a), 7(b) | none | judgment | exclusions |

## Changes

First edition in this repository.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
