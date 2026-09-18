# Accessibility of the documents this repository ships

Companion to `docs/accessibility.md`, which covers the accessibility of the
interface the work is done through. This one covers the other half its section 8
lists as open: **the accessibility of what this repository publishes**, starting
with its own Markdown.

Sources read: local captures of `Techniques for WCAG 2.0`,
`Understanding Conformance`, and `Understanding Techniques for WCAG 2.2 Success
Criteria`, plus the URLs cited inline.

**Every technique ID below was read out of those captures**, or out of a URL
the maintainer supplied. Nothing here is cited from recall, which is the
repository's own rule about grounding a claim in a source, applied to itself.

The WCAG 2.0 capture is a snapshot. The living index is the
[W3C WCAG 2.1 techniques list](https://www.w3.org/WAI/WCAG21/Techniques/), and
where a technique below is not in the capture it is linked rather than quoted.

**2.0 and 2.1 are different documents, and a technique is not always revised
between them.** Where a technique carries a 2.0 URL as well, both are given:
citing only the 2.1 copy implies a revision that may not have happened, and
citing only the 2.0 copy points at a version that is no longer the one being
maintained. Where only one is given, that is the only one the maintainer has
supplied or the capture holds, and it is not a claim that the other does not
exist.

## Why a Markdown file is in scope at all

WCAG is written for web content, and a README is web content the moment GitHub
renders it. The rendering is HTML, and the Markdown decides what that HTML is:
`##` becomes `h2`, a pipe table becomes `table`, a bare URL becomes an anchor
whose text is the URL. So the author of the Markdown is choosing the semantics
whether or not they mean to.

The techniques below are the ones an author of Markdown can actually satisfy.
Techniques about form controls, live regions, ARIA authoring and timing are out
of scope here because this repository ships no application.

## The techniques that apply, and what each means in Markdown

### Structure

| Technique | What it requires | In Markdown |
|---|---|---|
| G141: Organizing a page using headings | Sections are introduced by headings | Every section starts with a `#` heading, not with bold text |
| H42: Using h1-h6 to identify headings | Headings are real headings | Never fake a heading with `**bold**` on its own line |
| H69: Providing heading elements at the beginning of each section of content | The heading comes first | No orphan prose above the heading it belongs to |
| G130: Providing descriptive headings | The heading says what the section holds | "Installing the skills" rather than "Setup" |
| G57: Ordering the content in a meaningful sequence | Reading order carries the meaning | The order of sections is the order a newcomer needs them |
| G115: Using semantic elements to mark up structure | Lists are lists, tables are tables | `-` for lists, pipe tables for tabular data, never spaces |
| H48: Using ol, ul and dl for lists or groups of links | A group of links is a list | The index at the top of the README is a list, not a paragraph |
| H51: Using table markup to present tabular information | Tables carry a header row | Every pipe table here has its `---` header separator |

### Navigation

| Technique | What it requires | In Markdown |
|---|---|---|
| G64: Providing a Table of Contents | A long document offers a way in | The index at the top of the README |
| G124: Adding links at the top of the page to each area of the content | Those links reach each area | Each index entry is an anchor link to a real heading |
| G91: Providing link text that describes the purpose of a link | The link text alone says where it goes | Never "here", "this", or a bare URL as the whole link text |
| H30: Providing link text that describes the purpose of a link for anchor elements | Same, for anchors specifically | `[the contribution guide](CONTRIBUTING.md)`, not `[CONTRIBUTING.md](CONTRIBUTING.md)` where the sentence needs more |
| G53: Identifying the purpose of a link using link text combined with the text of the enclosing sentence | The sentence may supply the rest | Acceptable, and weaker than link text that stands alone |
| F84: failure due to using a non-specific link such as "click here" ([2.1](https://www.w3.org/WAI/WCAG21/Techniques/failures/F84), [2.0](https://www.w3.org/TR/WCAG20-TECHS/F84.html)) | Non-specific link text is a failure, not a weakness | Absent from the local WCAG 2.0 capture, which is why the first citation here was 2.1 only. It is in 2.0 as well, and both URLs were supplied by the maintainer. This is the rule `scripts/mdlint.py` enforces as MD059 |
| G62: Providing a glossary | Terms of art are defined somewhere | This repository has jargon and no glossary. Named as a gap below |

### Content

| Technique | What it requires | In Markdown |
|---|---|---|
| G117: Using text to convey information that is conveyed by variations in presentation of text | Meaning never rests on styling alone | If **bold** marks something important, the words must say so too |
| G100 and G82: Providing a short text alternative that identifies the purpose of non-text content | Images carry alt text | Badges are images. `![build status](...)`, never `![](...)` |
| G18, G145, G17: Contrast ratios of 4.5:1, 3:1 and 7:1 | Text in images is readable | Applies to any badge or diagram this repository generates itself |
| G88: Providing descriptive titles | The document says what it is | The `h1` is the title of a README |

### Failures to avoid, named as failures in the source

| Failure | What it is |
|---|---|
| F32, F33, F34: using white space characters to control layout | Spaces or tabs used to make columns, align text, or create the look of a table. It reads correctly and parses as one run-on line |
| F72: using ASCII art without providing a text alternative | A diagram drawn in characters, with no prose saying what it shows |
| F91: not correctly marking up table headers | A pipe table without its header separator row |
| F25: the title of a Web page not identifying its contents | An `h1` that names the project and says nothing about it |

## Conformance, stated honestly

WCAG conformance is claimed per page against a level, and **this repository does
not claim conformance.** What it does is apply the techniques above to the
documents it ships, and record which ones it has checked.

The distinction matters and is the same one this repository makes everywhere
else: applying techniques is work, a conformance claim is an assertion about a
whole page that somebody has to be able to check. The techniques are listed with
IDs precisely so the claim can be checked later rather than asserted now.

**Two things block a real claim** and both are stated here rather than
discovered by a reader:

1. **The rendering is not ours.** GitHub decides the final HTML, the colour
   scheme and the contrast. Contrast criteria in particular are the renderer's,
   not the author's, except for images this repository generates.
2. **Contrast and colour are not checkable from here** for the same reason, and
   they are the criteria most often decisive.

## Gaps, named

- **No glossary**, which G62 asks for. This repository uses "surface", "regime",
  "seat", "gate", "control fidelity" and "tack" as terms of art. A reader who
  does not already know them has no single place to look.
- **An automated check exists.** `scripts/mdlint.py` is the seventh gate, run
  by `scripts/gates.sh` and by CI. It enforces nineteen
  markdownlint rules, using markdownlint's own rule IDs so the real tool is a
  drop-in later. Four of them exist for accessibility rather than tidiness:
  MD001, MD025 and MD041 for heading structure and title (G141, H42, G88, F25);
  MD045 for image alt text (G100, G82); MD059 and MD034 for link purpose (G91,
  H30, F84); MD056 for table structure (H51, F91). It states its own coverage,
  and `--selftest` plants a positive for every rule before a clean run is
  trusted.
- **The output side, produced artifacts** (PDF/UA and the document pipeline),
  is not covered in this repository, and `docs/accessibility.md` section 8 names
  it as a gap. This document covers Markdown only and does not stand in for it.

## Cross-references

- `docs/accessibility.md`: the input side, the interface the work is done
  through. Its section 8 lists the output-side standards work this document
  begins.
- `CONTRIBUTING.md`: the mechanical rules a change has to pass, and the script
  that enforces them.
