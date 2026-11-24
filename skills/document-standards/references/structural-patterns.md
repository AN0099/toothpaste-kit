# Structural Patterns to Avoid

Full reference. Distilled versions of the highest-value patterns live in `working-preferences` for universal coverage; this file adds detection detail and lower-frequency patterns for document-authoring work specifically.

## Binary Contrasts (X-not-Y family)

The full category, not just the comma-separated form already banned in `working-preferences`:

| Pattern | Fix |
|---|---|
| "Not because X. Because Y." | State Y directly. |
| "[X] isn't the problem. [Y] is." | State the actual problem. |
| "The answer isn't X. It's Y." | State Y. |
| "It feels like X. It's actually Y." | State Y. |
| "stops being X and starts being Y" | Describe the actual change directly. |
| "not just X but also Y" | State both plainly, or pick the one that matters. |

## Negative Listing

Listing what something is not before revealing what it is:

- "Not a X... Not a Y... A Z."
- "It wasn't X. It wasn't Y. It was Z."

Fix: state Z. The reader doesn't need the runway.

## Dramatic Fragmentation

- "[Noun]. That's it. That's the [thing]."
- "X. And Y. And Z."

Fix: complete sentences. Trust content over presentation.

## Rhetorical Setups

- "What if [reframe]?"
- "Here's what I mean:"
- "Think about it:"

Fix: make the point directly. Let the reader draw conclusions.

## Triplets

Groups of three adjectives, clauses, or sentences used as a default shape rather than because the content genuinely has three parts. Use two, four, one, or five instead when that's what the content actually calls for.

## Tortured Metaphor and Simile

Overly articulate comparisons that overwork a single idea, producing forced or mismatched imagery: "They wove metal into sensual artifacts," "The seeds of his betrayal bloomed into a thunderstorm of regret." A comparison that requires unpacking to make sense is a comparison that shouldn't ship.

## Inhuman Emotion

Flowery excitement about mundane things a typical person wouldn't actually get excited about: "an exciting shade of grey." A signal the sentence is performing enthusiasm rather than reporting it.

## False Agency

Giving inanimate things human verbs, avoiding naming the actual actor:

| Pattern | Fix |
|---|---|
| "a complaint becomes a fix" | Name who fixed it. |
| "the decision emerges" | Name who decided. |
| "the culture shifts" | Name who changed what behavior. |
| "the data tells us" | Name who read the data and concluded what. |

## Narrator-from-a-Distance

Floating above the scene instead of naming a specific actor:

- "Nobody designed this."
- "This happens because..."
- "People tend to..."

Fix: put the actor in the scene. Name who did what.

## Parataxis

Short declarative sentences stacked with no connective tissue: "Short sentence. Then another. Then another." Reads as performed simplicity rather than actual clarity. Fix: connect related thoughts with subordinate clauses, conjunctions, or semicolons that show how the ideas relate.

## Passive Voice

A sentence names its actor. The passive stays in three cases: the actor is unknown, it brings the topic
forward, or it carries the thread from the last sentence.

| Pattern | Fix |
|---|---|
| "X was created" | Name who created it. |
| "It is believed that" | Name who believes it. |
| "Mistakes were made" | Name who made them. |

## Sentence Starters to Avoid

- Sentences opening with What, When, Where, Which, Who, Why, or How.
- Paragraphs opening with "So."
- "Certainly," "Absolutely," "Sure," as response openers.
- "However," "Furthermore," "Moreover," "Additionally," "Interestingly," "Notably," "Importantly," "Indeed," as sentence or paragraph openers.

## Rhythm Patterns

- No three consecutive sentences of the same length.
- No em-dashes as a design flourish or dramatic pause (already a hard ban, restated here for document context).
- No every-paragraph-ends-punchily pattern. Vary how paragraphs close.

## Generic Ordinal Step Labels

"Step 1 / Step 2," "Stage 1 / Stage 2," "Phase 01 / Phase 02" used as the label itself. The actual step content is the label; if progression must be shown, use the verb-noun directly ("Install," "Configure," "Ship").

## Patterns Adapted from humanizer

Each entry below covers a pattern the sections above did not, adapted from blader/humanizer v4.0.0 (MIT), which draws on Wikipedia's "Signs of AI writing". Rewritten in this file's form; the examples there are not copied.

- **Sayings that sound deep.** "At its core," "the real question is," "what really matters," "the heart of the matter." An ordinary point dressed as a hidden truth. Replace the saying with the specific point.
- **Arguing with no one.** "To be clear," "I'm not saying," "this isn't about," "some might say." An objection or option the text never raised, usually left over from a draft. Remove the rebuttal along with its target.
- **Hyphenated pairs everywhere.** Compound modifiers stacked for weight ("data-driven, outcome-focused, user-centric"). Keep one only when it is the precise term.
- **Shallow -ing phrases.** "Highlighting," "underscoring," "reflecting," "fostering," "showcasing" bolted onto a plain fact to make it sound deeper. Keep the fact; drop the phrase unless the source supports what it claims.
- **Borrowed authority.** "Experts agree," "studies show," "industry observers note" with no source the reader can follow. Name the source or drop the claim.
- **Avoiding is, are and has.** "Serves as," "stands as," "functions as," "boasts," "features" in place of a plain verb. Write is, are, has.
- **Bold as decoration.** Bold scattered over phrases that carry no more weight than their neighbours, or a bold lead-in on every bullet by habit. Bold marks what a skimming reader must not miss, and little else.
- **Decorative headings.** A heading over a two-line section, or a heading per paragraph. A heading earns its place when a reader would jump to it.
- **Curly quotation marks** in plain text, code, or Markdown where straight quotes are the convention.
- **Chatbot residue.** "I hope this helps," "great question," "let me know if," "certainly!" A document is not a reply.
- **Knowledge-limit disclaimers.** "As of my last update," "I cannot verify," or a guess presented as a date. State what is known and its source, or mark the gap once.
- **A heading repeated in the first sentence.** "## Installation" followed by "This section covers installation." Start with the content.
- **Writing about the document instead of its subject.** What the text replaced, how it was assembled, a legend the reader can already see. Previous versions belong in change logs; how it was made belongs in provenance (the two-layer rule).
- **Re-explaining what the reader knows.** Defining terms the stated audience uses daily. Set by the AUDIENCE_LEVEL dial, not by habit.

## Generic Conclusions

A conclusion that would hold just as well for a neighbouring topic: swap the system, the release or the team and the sentence is still true ("a complex picture emerges," "plays an important role," "further work is needed"). Nothing could make it wrong, so it tells the reader nothing. Fix: name the specific finding and what it rests on, or cut the sentence. Adapted from leiverkus/research-superpowers' semantic-wiki-review.

**When not to act.** Leave a watched phrase alone inside a quotation, a title, a proper name, or a passage that discusses the phrase rather than uses it. A third-party source keeps its wording, as the em dash scope rule already says.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
