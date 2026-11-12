# Data display

## § 1. Scope

(a) This standard applies to every exhibit the desk publishes: a table, chart, sparkline, or
diagram.

(b) The requirements take their concepts from four books by Edward Tufte, and 2(h) from ATP
6-01.1. The books are *The Visual Display of Quantitative Information* (VDQI), *Envisioning
Information* (EI), *Visual Explanations* (VE), and *Beautiful Evidence* (BE). The wording is the
desk's own.

(c) This standard does not cover presentation software or print resolution.

(d) In this standard, the words SHALL, SHALL NOT, SHOULD, SHOULD NOT, and MAY have the meanings
that BCP 14 (RFC 2119, RFC 8174) gives them. They have these meanings only when they appear in all
capitals.

## § 2. Form

(a) An exhibit SHALL exist to answer a question.

(b) Every number SHALL appear against a comparison (BE, principle 1, and EI, Small Multiples).

(c) A set of about 20 numbers or fewer SHOULD be a table (VDQI ch. 2).

(d) A pie chart SHALL NOT be used. A table SHOULD take its place (VDQI ch. 9).

(e) Several views of the same variables SHOULD be small multiples: one design, repeated, so that
only the data changes (VDQI ch. 8).

(f) A trend beside a word or number MAY be a sparkline, a word-sized graphic set in the line of
text (BE).

  (1) A sparkline's context, such as a normal range, SHOULD be shown with it.

(g) A chart SHOULD be wider than it is tall (VDQI ch. 9).

(h) A recurring readout SHOULD hold the short list of items its reader has declared.

  (1) A readout SHOULD be redesigned when its reader cannot find a critical item fast.

Notes: Graphics earn their place on large sets of numbers. Design does not rescue weak content (BE,
principle 6). A pie chart has low density and does not order its numbers along a visual dimension.
In a readout, a listed item reaches the reader at once, and rumor or speculation does not (ATP
6-01.1, paras 2-71 and 3-58).

## § 3. Integrity

(a) Marks SHALL measure in proportion to the numbers they show.

(b) A bar SHALL start at zero.

(c) Dimensions that carry information SHALL NOT exceed the dimensions in the data. Flat data takes
no perspective.

(d) Variation in an exhibit SHALL come from the data. A scale SHALL NOT change partway through.

(e) Scales and important events SHALL be labeled on the exhibit itself.

(f) Money over time SHOULD use deflated, standardized units.

(g) Data SHALL NOT be shown out of the context that gives it meaning.

Notes: The section follows VDQI ch. 2, and Appendix A states the test for 3(a). Requirement 3(b)
is the desk's reading of 3(a): a bar's length is its value. The books state the proportion, and
VDQI ch. 2 gives the case of a baseline set below zero to hide a loss.

## § 4. Ink

(a) Most of an exhibit's ink SHOULD show data (VDQI ch. 4).

  (1) Ink that shows nothing, or shows the same thing twice, SHOULD be removed, within reason.

  (2) Each exhibit SHOULD be revised for 4(a).

(b) Decoration, vibrating patterns, and heavy grids SHALL NOT be used (VDQI ch. 5).

  (1) A needed grid SHALL be muted.

(c) A frame SHOULD do data work where it can, as a range frame marks the minimum and maximum (VDQI
ch. 6).

(d) Visual distinctions SHOULD be the smallest that still read clearly (VE ch. 4).

(e) Layers SHOULD separate by weight, with the data on top (EI, Layering and Separation).

  (1) The designer SHOULD check what two marks make together, since two marks can produce a third,
  unwanted one between them.

(f) Removing data SHALL NOT be the cure for clutter. Better design, or a smaller and denser
graphic, SHOULD come first (EI and VDQI ch. 8).

Notes: Clutter is a design fault.

## § 5. Words

(a) Words, numbers, and images SHALL sit together, placed for the argument, whatever tool made each
one (BE, principle 4).

(b) Words SHOULD be spelled out, run left to right, and label the data directly, so that the reader
needs no key (VDQI ch. 9).

(c) An exhibit SHALL state its source, its authors where they matter, and its scales (BE,
principle 5).

(d) Where the point is a cause, the exhibit SHOULD show the mechanism as well as the outcome (BE,
principle 2).

(e) Rows SHOULD be ordered by something meaningful (VDQI ch. 9).

Notes: Alphabetical order suits a directory.

## § 6. Color

(a) Color SHALL have a job: to label, to measure, to represent, or to enliven. Color with no job
SHALL NOT be used (EI, Color and Information).

(b) Strong color SHOULD be used sparingly, on a muted ground (EI, from Eduard Imhof).

## Appendix A. Conformance

Requirement 3(a) is tested by the Lie Factor (VDQI ch. 2). The Lie Factor is the size of an effect
shown in the graphic, divided by its size in the data. An honest exhibit scores close to 1. The desk
fails 3(a) when the score is under 0.95 or over 1.05.

Check kinds: **mechanical** is a check in `scripts/style-check`, named by the
requirement it enforces, each with a planted positive and a clean negative in `--selftest`. A D
check reads an SVG file with `--svg`, and a Mermaid block in Markdown mode. **Review** is an item a
second reader checks by reading. **Judgment** has no check, and none is claimed.

| Requirement | Keyword | Check kind | Check |
|---|---|---|---|
| 1(a) to 1(c) | none | judgment | scope statements |
| 1(d) | none | review | BCP 14 citation present |
| 2(a), 2(b) | SHALL | judgment | the question and the comparison |
| 2(c) | SHOULD | review | a set of about 20 numbers or fewer is a table |
| 2(d) | SHALL NOT, SHOULD | mechanical | `D2d` FAIL on a Mermaid block whose first diagram line opens on `pie`, and on an SVG wedge: a `path` of one move and only line segments and arcs, counting each pair after `M` or `L`, each number after `H` or `V`, and each arc after `A` as one segment, with one arc and one or two lines, or two arcs and at most two lines, of different radii or drawn one after the other with a line |
| 2(e), 2(f), 2(f)(1) | SHOULD, MAY | review | small multiples, sparklines and their context |
| 2(g) | SHOULD | mechanical | `D2g` WARN on an SVG taller than wide, by its `viewBox` or else its `width` and `height` in absolute units |
| 2(h), 2(h)(1) | SHOULD | judgment | the reader's declared list |
| 3(a) | SHALL | review | the Lie Factor, above |
| 3(b) | SHALL | mechanical | `D3b` FAIL on two or more `rect` bars whose `id` or `class`, or an ancestor's, names bar, sharing a bottom or left edge, where a numeric `text` within 6 units of that edge, not placed inside the bars' span on the other axis, is not zero |
| 3(c) to 3(g) | SHALL, SHALL NOT, SHOULD | review | dimensions, scales, labels, units, context |
| 4(a) to 4(a)(2) | SHOULD | review | data ink |
| 4(b) | SHALL NOT | mechanical | `D4b` FAIL on an element referencing a `filter` that holds `feDropShadow`, or `feOffset` with `feGaussianBlur`, at an offset other than 0,0, and WARN on a fill or stroke referencing a gradient, except on an element or ancestor named colorbar |
| 4(b)(1) | SHALL | mechanical | `D4b1` FAIL on a line, path, polyline, or rect that, or whose ancestor, has an `id` or `class` naming grid, whose ink is over 0.6: the darkness of its stroke over white, by its opacity, times its width at the scale the viewBox is drawn at, a width under 1 counting as 1 |
| 4(c) | SHOULD | mechanical | `D4c` WARN on a `rect` with a visible stroke (width, opacity and the color's alpha above 0), at least 0.8 of the canvas each way |
| 4(d) to 4(f) | SHOULD, SHALL NOT | review | distinctions, layers, clutter |
| 5(a), 5(c) | SHALL | review | words placed with the data, and the source, authors, and scales |
| 5(b) | SHOULD | mechanical | `D5b` WARN on the outermost element whose `id` or `class` names legend |
| 5(d), 5(e) | SHOULD | review | mechanism, row order |
| 6(a) | SHALL, SHALL NOT | review | each color's job |
| 6(b) | SHOULD | mechanical | `D6b` WARN on more than one hue in fill, stroke, and stop-color, seen over white by its opacity, with HSL saturation of at least 0.5 and lightness from 0.25 to 0.75 |

Notes: Three checks are the desk's reading, and no book gives them. The gradient WARN in `D4b` reads
a gradient as decoration. A colorbar is exempt, since there the gradient measures under 6(a). The
exemption reads the element's name, so a gradient inside a group named colorbar passes.

Check `D3b` reads 3(b) from its notes. Check `D6b` reads "sparingly" in 6(b) as one strong hue.
Check `D5b` rests on 5(b) itself, which asks for no key, so it warns on any legend.

The thresholds are the desk's readings too. They are ink of 0.6 in `D4b1` and 0.8 of the canvas in
`D4c`. They are 6 units in `D3b` and 20 degrees of hue in `D6b`. A grid line drawn under 1 px counts
as 1 in `D4b1`, so a dark grid fails however thin.

## Changes

First edition in this repository.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
