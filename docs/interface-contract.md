# Interface Contract

**Working doc for an effort in flight, started 2026-09-06.** Machine-facing half of a pair; the
human-facing half is `interaction-manual.md`.

**This document is not normative and is designed to be deleted.** `skills/working-preferences/SKILL.md`
is the source of truth for every rule named here. This file exists to track what is live, what is
designed and not yet promoted, and what is still open, for the duration of one effort. When the effort
closes, anything still useful folds into the skill and this file goes away. Keeping it any longer
would create exactly the drift the pairing is meant to avoid.

## 1. What the contract covers

Three surfaces, which had never been described together:

1. **Command vocabulary.** Seventeen closed commands, defined in `working-preferences`, indexed in
   `skills/commands`.
2. **Brevity code.** Lowercase home-row equivalents for all seventeen. New 2026-09-06.
3. **Input syntax.** How a message is segmented into tasks and qualifiers, and how the model should
   parse it. New 2026-09-06, and previously unwritten anywhere despite being in constant use.

Item 3 is the one worth noticing. The separators had been used consistently for the whole life of the
project and no document described them, so every session rediscovered them by inference or failed to.

## 2. Status

| Element | State | Where it lives |
|---|---|---|
| Seventeen ALLCAPS commands | Live, unchanged | `working-preferences`, `commands` |
| Brevity code, 17 codes | **Promoted 2026-09-06** | `working-preferences` |
| Input syntax, 10 rules | **Promoted 2026-09-06** | `working-preferences` |
| Reply-cost rules, 4 | **Promoted 2026-09-06** | `working-preferences` |
| `commands` index updated with codes | **Open** | Nothing yet |
| `CHANGELOG.md` entry for the above | **Open** | Nothing yet |
| Q1-3 format compliance | **Open, see 5-2** | `working-preferences` `# Format` |

## 3. The brevity code, and the constraint that shaped it

3-1. Codes are lowercase, unmodified, and drawn from the home row. **A code is recognised only when
it is the entire message**, which is the same rule the harness applies to slash commands and which
removes the need for a sigil.

3-2. **Hand balance is the organising constraint, ahead of mnemonics.** Single keys are assigned by
descending command frequency with the hands alternating down the list. Every two-key code takes one
key from each hand. No code repeats a finger.

3-3. **The first version was wrong, and the reason it was wrong is the reusable part.** It assigned
the most frequent command to the strongest finger, which is correct general ergonomics. It was the
wrong answer because it put the highest-frequency command on the operator's worse hand, and nothing
in keyboard theory could have revealed that. Three of its two-key codes were same-hand as well.

3-4. **The rule this yields:** a strain-reduction design cannot be derived from the interface alone.
It requires the specific body it is for, and asking costs one question. A design that looks correct
by general principle can be exactly wrong for its user, and it will not announce this.

## 4. Input syntax, condensed

Full statement is in `working-preferences`. The shape, for orientation:

- Semicolon opens an independent task. Comma modifies the task before it.
- Semicolon order is not priority order. Priority is carried by content.
- `filename: section instruction` targets a location rather than a whole file.
- `also X` appends without displacing.
- `yes to X` confirms X only and is silent on everything else proposed.
- Urgency arrives as a stated real-world consequence, not as a label, and should reorder work.
- Permission grants are scoped and time-boxed. A grant to read is not a grant to delete.
- Corrections lead with what to undo, then what was meant.
- Typos are frequent, injury-related, and never to be queried.

## 5. Open items

5-1. **`skills/commands/SKILL.md` still lists only the ALLCAPS forms.** It is the discoverability
index, so a code absent from it is a code an agent cannot find. This is the same failure the kit
already documents elsewhere: written but not mounted, one step short of not existing.

5-2. **The `# Format` rule requiring three follow-up questions after every response was not being
honoured during the session that wrote this document.** Found by reading the skill in order to edit
it, which is the only reason it surfaced. Two readings are possible and they lead to different fixes:
the rule is live and compliance lapsed, or the rule has fallen out of use and should be retired. It
is the operator's call and it is not made here.

5-3. **Whether the brevity code should extend beyond the seventeen.** The commands are conversational
control verbs. Procedures are slash commands and were deliberately excluded from the vocabulary. If
typing `/session-close` is itself a cost worth removing, that is a separate decision about slash
commands, not an extension of this code.

5-4. **FLAGGED 2026-09-06: a one-handed variant of the brevity code. Scoped here, deliberately not
built.**

*What breaks.* The current code's organising constraint is hand alternation, and for a one-handed
user that is not a neutral property, it is a hard failure. All ten two-key codes require both hands
and none of them can be typed. Four of the seven single keys sit on the wrong side. The feature and
the defect are the same design decision, which is the useful part of this flag: an accessibility
choice made for one body can exclude another, and hand balance looked unambiguously correct until
this question was asked.

*What a variant needs.*

- **Two mirrored variants, or one that is mechanically mirrorable.** Handedness is not predictable
  and a single-hand layout that assumes the left excludes half its users.
- **Same-hand digraphs throughout**, which is the exact inverse of the current rule. One hand's home
  row is five keys, giving five singles and twenty-five ordered pairs, so seventeen commands fit
  inside one hand's home position with room left.
- **Inward rolls preferred, same-finger repeats forbidden.** With four usable fingers on five keys
  this constrains harder than the two-handed case and is the part that needs real care.
- **Sequential, never chorded.** Simultaneity is the thing a single hand cannot cheaply do.
- **No timing dependency.** The existing rule that a code is only a code when it is the entire
  message already gives this for free, since nothing is disambiguated by how fast keys arrive. That
  rule turns out to be the most portable decision in the design.

*What decides it.* Whether the variant is offered as a chosen mode or detected, and whether the
mirrored pair is generated from one canonical layout or authored twice. Neither is answered.

*Scope beyond the code.* One-handed operation is not only a permanent limb difference. It covers a
cast, a sling, a healing tendon, and holding something in the other hand. That makes it a
temporary-state axis as much as a permanent one, which argues for it being a switchable mode rather
than a separate build. It is also the case where voice, a foot pedal and eye tracking stop being
supplements and become the primary interface.

*Status:* flagged, scoped, not started. No layout has been designed and none should be until the
mirroring question is answered, because that decision determines whether the work is one layout or
two.

5-5. **Whether any of this belongs in the published kit or stays local.** The vocabulary and the
syntax generalise. The specific hand assignment does not: it is fitted to one person's laterality.
The current split puts the general design rule in the public documents and the personal specifics
in the restricted tier. That split is asserted here and has not been reviewed.

## 6. Deliberately excluded

- **Personal medical or physical detail.** The design rule is public; the specifics that produced it
  are not. This follows the project's own standing rule that process is what to teach and specifics
  are what to hide.
- **A second machine-facing ruleset.** Everything normative goes in `working-preferences`. This
  document points; it does not restate.

## Cross-references

- `skills/working-preferences/SKILL.md`: normative. The contract itself.
- `skills/commands/SKILL.md`: the index, pending the update at 5-1.
- `interaction-manual.md`: the human-facing half, explaining why these rules exist.
- `accessibility.md`: the wider input-strain effort this code is one part of.
