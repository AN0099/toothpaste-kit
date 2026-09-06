# Interaction Manual

**Working draft.** Human-facing half of a pair. The machine-facing half is
`skills/working-preferences/SKILL.md`, which is normative: where this document and that one disagree,
that one is right. This one explains why the rules are shaped as they are and how to use them. It
restates no rule verbatim, so the two cannot drift apart on wording.

Audience: anyone who wants to work with a capable language model the way this project does, and
anyone joining a team that already does. No prior familiarity with this repository is assumed.

## Why a manual and not a prompt

Most advice about working with these systems is a list of phrasings that worked once. That does not
transfer, because the phrasing was never the mechanism.

What transfers is a small number of habits that make the work legible and correctable: a closed
vocabulary for the moves you make often, an explicit distinction between things you are asserting and
things you are still deciding, and a standing rule that nobody's claim of completion counts until
someone else checks it. Those habits are what this document teaches. They hold across vendors and
they outlive any particular model.

The thesis the rest of the project argues, in one line: the machine works, and the leverage sits with
whoever understands the job well enough to specify it and check it.

## 1. Give the model a closed vocabulary

Ordinary conversation is a bad control surface. "Can you tidy this up a bit" has no defined effect,
so its effect varies, and when it varies you cannot tell whether the model misbehaved or your
instruction was empty.

Fix this by defining a small set of words that mean exactly one thing, and using them for the moves
you make constantly. This project uses seventeen. The exact list matters far less than three
properties of it:

- **Closed.** New words are added deliberately, not invented mid-conversation.
- **Defined in one place.** There is a single file that says what each word does, and it is loaded
  into the session rather than remembered.
- **Cheap to type.** See section 6. A vocabulary you avoid using because it is tiring is not a
  vocabulary.

The payoff is that a one-word message reliably produces a specific behaviour, and when it does not,
you have found a real defect rather than a misunderstanding.

## 2. Separate what is settled from what is not

The most expensive failure in long work is the model quietly revising something you had already
decided, then building on the revision.

Three states are worth marking explicitly:

- **Settled and immutable.** The model may not revise it. If new reasoning contradicts it, the
  reasoning is re-examined, not the settled content.
- **Load-bearing but revisable.** The model may propose changing it, but must surface what else
  breaks before it does.
- **Withdrawn.** Treated as never said, including anything derived from it.

Marking these costs one word each and removes an entire class of drift. Without the marks, everything
in the conversation has the same status, which means nothing does.

## 3. Set the dials, do not describe the mood

Vague quality instructions produce vague compliance. Instead, name the axes that actually vary and
set each one:

- **How much autonomy.** Confirm every step, or build the whole thing and show you at the end.
- **How much initiative.** Do exactly what was asked, or flag adjacent problems you notice.
- **How much rigor.** State your best judgment, or verify before every claim.

Say where each sits and adjust when it is wrong. "Be more careful" names none of these and therefore
changes none of them.

## 4. Nobody self-certifies

**A completion claim is not a fact until a party other than the one claiming it has checked.**
Self-audit is not verification, for models and people alike. A model asked whether it finished will
almost always say yes, and it is not lying; it has no reliable access to the difference between
having done the work and having produced text describing the work.

Practical forms this takes:

- Run the check rather than reading the code and concluding it would pass.
- When a check returns nothing, confirm the check works. A search that is silently broken and a
  search that found nothing look identical.
- Re-read state before acting on a reading taken earlier in the session. Things change underneath
  you, including things you changed yourself.
- Prefer evidence that could have come out the other way. A count, a hash, a diff.

This is the single highest-value habit in the document and the one most often skipped, because
skipping it feels like moving faster and does so right up until it does not.

## 5. Structure the message so it can be parsed

Long instructions carrying several tasks are normal and fine. What matters is that the boundaries are
visible.

- **One separator for independent tasks.** Anything after it is a new deliverable, not a continuation.
  This project uses a semicolon. Any consistent mark works; consistency is the whole point.
- **A different separator for qualifiers.** A clause that constrains or scopes the task before it,
  rather than starting a new one. This project uses a comma.
- **Point at locations.** Naming a file and a section number is far cheaper than describing where you
  mean, and it removes an entire round trip.
- **State urgency as consequence.** "This is blocking the release" reorders work correctly. "Urgent"
  does not, because everything is.

A model that has been told what your separators mean will treat a five-task message as five tasks. One
that has not will usually answer the last one.

## 6. Price the input

Interface cost is a real constraint and it is routinely designed out of view.

This project discovered its own command vocabulary was the most physically expensive text its
operator typed: seventeen commands, all capitalised, meaning a held modifier key on the highest
frequency input in the system. It had been designed for legibility to the machine, and its cost to
the human had never been counted.

The general rules, which apply to any interface you build or adopt:

- **Frequency times cost is the number that matters**, not cost alone. The rare expensive thing is
  fine. The common expensive thing is what injures people.
- **Modifier keys and pointer use cost more than keystrokes.** Optimising letters while leaving the
  mouse in the loop solves the smaller problem.
- **Ask whose hands.** Ergonomic defaults assume a symmetric, uninjured operator. That assumption is
  frequently wrong and is cheap to check. Guessing produced a wrong answer here that looked
  completely correct until someone said which hand.

See `accessibility.md`, which treats this as a design axis rather than an accommodation.

## 7. Make questions cheap to answer

This is the same principle as section 6 applied to the model's output rather than the human's input.

Every question the model asks is paid for in the human's effort. So: batch questions rather than
asking them one at a time; present choices that can be answered with a single character; and where a
sensible default exists, take it and say so, rather than blocking. A stated assumption that turns out
wrong costs one short correction. A blocking question costs a full round trip before any work starts.

Reserve genuinely blocking questions for cases where proceeding would be unsafe or would waste the
work if the guess is wrong.

## 8. Correct without ceremony

When the model is wrong, say so plainly and move on. When it notices its own error, it should state
the correction and continue, not apologise at length or narrate the mistake.

The useful discipline is on the other side: **keep the error visible in the record when the error is
instructive.** A design note that shows a wrong first answer and what made it wrong is worth more
than one that shows only the final answer, because the reader learns the failure mode rather than
just the result. Overwrite mistakes in code; preserve them in reasoning.

## 9. Two layers, never mixed

Keep reasoning and results in different files.

- **Reasoning, decision history, session residue.** Written for the machine and for whoever picks up
  the work cold. Verbose is correct here. Nothing is too obvious to write down.
- **Results.** README, guides, specifications, this document. Lean and concrete. No archaeology.

When both need the same fact, the result states it and the reasoning layer keeps the argument. Mixing
them produces documents that are too long for the reader who wants the answer and too thin for the
reader who wants the why.

## 10. What not to do

- Do not ask the model to confirm it followed instructions. It will say yes. Check instead.
- Do not accumulate rules faster than you can enforce them. An unenforced rule teaches everyone that
  rules are optional.
- Do not build a mechanical gate from a single incident. One occurrence is a sample of one, and a
  gate shaped around it reads as coverage while providing almost none. Wait for the second, and write
  down in advance what the second would look like.
- Do not let a document that lists open questions go stale. The moment one closes, the document is
  wrong, and nothing will tell you.
- Do not confuse a model that is agreeable with a model that is correct.

## Cross-references

- `skills/working-preferences/SKILL.md`: normative machine-facing rules, the command vocabulary, the
  brevity code, and the input syntax. Everything above is explanation; that file is the contract.
- `interface-contract.md`: working doc tracking which parts of the contract are live and which are
  designed but not yet promoted.
- `accessibility.md`: input strain and pointer elimination treated as a design axis.
- `skills/commands/SKILL.md`: the vocabulary index, for looking one up without loading the whole
  ruleset.
- `README.md`: what this repository is and the argument it makes.
