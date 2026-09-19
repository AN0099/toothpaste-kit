# Document layers

How a statement's force is marked, and which statements belong in this
repository at all.

Two independent questions decide where a sentence goes. Answer both.

1. **Force.** Is the sentence a requirement, a recommendation, a permission, or
   an explanation? See [Requirements language](#requirements-language) and
   [Normative and informative](#normative-and-informative).
2. **Kind.** Is the sentence documentation, or is it the record of how a
   decision was reached? See [Documentation and provenance](#documentation-and-provenance).

The second question is the one that gets answered wrong. A true, well written,
useful paragraph can still belong in a different repository.

## Requirements language

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT,
RECOMMENDED, MAY and OPTIONAL in this repository's documents are to be
interpreted as described in [BCP 14](https://www.rfc-editor.org/info/bcp14),
when, and only when, they appear in all capitals.

Lowercase "must" and "should" carry no such force.

[RFC 7322] section 4.8.2 requires that a document using this interpretation
cite RFC 2119 and carry it as a normative reference, and that the section doing
so appear at or after the introduction. That is why this section is here and
why [BCP 14] is listed below as normative rather than informative.

A document MAY decline the interpretation, provided it says so. [RFC 7322]
section 3 is itself an example: it states that it does not use RFC 2119
terminology, and defines its own lowercase "must" and "should" instead. What is
not permitted is using the capitals without saying which reading applies.

## Normative and informative

**Normative** text states what a conforming reader does. It uses a BCP 14
keyword, and it is testable: a reader can say whether a given commit, document
or run satisfies it.

**Informative** text helps a reader apply a normative statement. It explains a
mechanism, gives an example, or names a consequence. It creates no obligation.

The terms are borrowed from [RFC 7322] section 4.8.6, which applies them to
**references**: normative references are "essential to implementing or
understanding the content", informative references "provide additional
information". This repository applies the same split to prose as well, which is
an extension of the cited definition rather than the definition itself.

A document MAY contain both. A normative statement MUST be phrased so that
removing every informative sentence around it leaves the requirement intact.

### The mechanism test

Informative text in this repository states a **present-tense mechanism**: the
constraint that makes the requirement necessary. It does not narrate.

| Allowed | Not allowed |
|---|---|
| A GitHub action runs with the workflow's token; a package invoked in a step does not. | The action was rejected after the third time this came up. |
| A pushed tag cannot be re-signed without moving it. | Signing was added once the key existed. |
| `reflow-md`'s fixtures are the input and expected output of its own test. | A bulk fix edited them and broke the test. |

Both columns are true. The right column belongs in provenance, because it is
about the project's history rather than about the reader's task.

## Documentation and provenance

**Documentation** is written for a reader with a task. It describes the system
as it is now, in present tense.

**Provenance** is the record of how the system came to be: which options were
weighed, what was tried, what failed, when a rule changed and why, who raised
it. It is written for whoever maintains the system later.

Both are worth keeping. They MUST NOT share a file.

- Documentation lives in this repository.
- Provenance lives outside it, in the operator's working notes.

### What marks a sentence as provenance

Any one of these is sufficient:

- A date that is not itself data. A release date in `CHANGELOG.md` and a
  "checked" date in a status table are data. "Stated 2026-09-18" is provenance.
- A prior state of the document or the system: "this said eleven", "used to
  sit in", "was first stated as", "went from".
- An event: something was tried, broke, was found, was re-argued, was nearly
  missed.
- A first-person narrator, or an actor at all. Documentation has no protagonist.
- A justification of the document's own editorial choices, such as noting that
  something is being stated rather than hidden.

### Where provenance goes instead

Removed passages are appended to the operator's provenance notes with the
source path, the text removed, and what replaced it. Nothing is deleted in the
course of this separation: a passage that is worth removing from a public
document is usually worth keeping somewhere.

## Exceptions

Four kinds of dated or historical statement are documentation, not provenance,
and MUST be kept:

1. **`CHANGELOG.md`**, whose entire subject is what changed and when.
2. **A status document's measurement dates.** "Verified on <date>" tells a
   reader how stale the claim is, which is what the reader needs.
3. **A citation's date or version.** Standards are versioned and a reader needs
   to know which version was read.
4. **A stated limitation.** "This check covers sixteen of eighteen rules" and
   "this repository does not claim conformance" are current facts about the
   system and are load bearing. They are not archaeology, and removing them
   would make a document overclaim.

## How this is checked

`scripts/mdlint.py` checks document **structure** and cannot check any of the
above. The separation is a review obligation, not a gate.

A contributor SHOULD read a changed document once with a single question: does
any sentence here describe this project's past rather than its present? A
reviewer MUST reject a document that mixes the layers, even where every
sentence in it is accurate.

Claiming a mechanical check for this would be worse than having none, because a
clean result from a check that cannot see the defect stops the search.

## References

Cited by tag. Full entries, with the normative and informative split, are in
[the references and prior work list](../references.md).

- **[BCP 14]** normative. Cited as [RFC 7322] section 4.8.2 requires.
- **[RFC 7322]** informative. Source of the conventions above.
- **[GFM]** normative. The dialect these documents render as.
