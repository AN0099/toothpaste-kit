# Accessibility

**Working draft, started 2026-09-06.** Standalone: it can be read without any other file in this
repository. Cross-referenced at the end for readers who want the parts it touches.

Scope is the accessibility of **the interface the work is done through**. The accessibility of what a
pipeline produces is a different problem, covered in a companion document named in the
cross-references.

## The claim

An interface is used by whoever is at the controls that day, and that changes. Injury, fatigue, a
broken wrist, a loud room, a bright room, a bad night: none of these are edge cases, and all of them
change what input is available. Designing for one symmetric, uninjured, silent-room operator is not a
neutral default, it is a specific assumption that is wrong a large fraction of the time, including
for the person who made it.

So this is an axis, not an accommodation. The practical difference is that an axis gets designed for
at the start, and an accommodation gets bolted on after someone complains.

## 1. Order the levers by what they remove

The instinct is to optimise typing, because typing is visible. That is usually the second problem.

1. **Pointer use.** Almost always the highest strain per hour and the least tracked, because nobody
   counts mouse movements the way they count keystrokes.
2. **Modifier keys and chords.** A held modifier is a sustained load, which is worse than a
   comparable number of taps. Pinky reaches are the common aggravator.
3. **Keystroke volume.** Real, and third.
4. **Reading load.** Not a strain issue directly, but noise costs more when output is being read
   aloud or navigated by keyboard.

Optimising 3 while leaving 1 in place is the standard mistake.

## 2. Pointer elimination

All configuration, no purchases.

- **Window management by keyboard.** Focus, move, resize and workspace switching bound to keys.
  Either a keyboard-driven window manager or the existing desktop's own bindings.
- **A launcher** such as `rofi`, `wofi` or the desktop's equivalent, replacing icon and menu clicking.
- **Keyboard browsing.** Vimium, Tridactyl, or the browser's native link-hinting and caret modes. Web
  browsing is usually the largest untracked source of pointer use in a working day.
- **Terminal-first file work.** A graphical file manager is a pointer surface. A shell with a fuzzy
  finder is not.
- **Voice-driven pointer replacement.** Grid and eye-tracking modes replace the mouse rather than the
  keyboard, which is why voice belongs here and not only in section 4.

## 3. Modifier and chord elimination

- **Home-row modifiers.** A home-row key held becomes a modifier and tapped stays a letter. This
  retires the pinky stretch for the common modifiers entirely, and it is the single best
  strain-to-effort change available. On Linux, `keyd` or `xremap` do this at the system level with no
  custom keyboard firmware.
- **Caps Lock remapped** to Control or Escape, retiring the worst-placed key on the board.
- **Application-level rebinding.** Any tool with a configurable keymap should have its painful chords
  retired rather than tolerated. For this project's harness that file is `~/.claude/keybindings.json`.

## 4. Voice input

The largest single lever, and the one where paying for a good tool is defensible.

**Talon Voice** is the serious option. It was built by and for people with repetitive strain injury,
which shows in what it optimises: programming and terminal work rather than prose dictation, and
crucially the mode switch between shell commands and free text, which is where most voice setups
break. It also provides pointer replacement, per section 2. A free tier exists.

**`nerd-dictation`** and **`numen`** are the local open-source alternatives, Whisper-backed, lighter
and less capable. Both worth knowing about for a machine that cannot run the commercial option.

Terminal user interfaces are among the harder surfaces for voice control, because the grammar must
cover shell commands and prose and the switch between them. That difficulty is a reason to start
early, not a reason to defer.

## 5. Keystroke volume

- **A brevity code for high-frequency input.** The design rules that generalise: frequency times cost
  is the number that matters rather than cost alone; no modifiers, since chording defeats the
  purpose; home row first; and hand balance ahead of mnemonics.
- **Hand balance is not symmetry.** If one hand is worse, the frequent path moves off it. If the
  better hand flares under sustained load, it is a better hand and not a spare one, so the answer is
  alternation rather than relocation. This has to be asked, not inferred: a design that is correct by
  general ergonomic principle can be exactly wrong for its operator, and it will look right until
  someone says which hand.
- **Shell abbreviations over aliases**, because they expand visibly and stay auditable.
- **Directory and history jumping**, such as `zoxide` and `atuin`, which remove path retyping.

**Hand balance assumes two hands, and that assumption should be visible rather than buried.** A
layout organised around alternating hands is unusable one-handed, and every code in it fails at once.
One-handed operation covers permanent limb difference and also a cast, a sling and holding something
in the other hand, so it is a temporary state at least as often as a permanent one. The design
consequence is that a single-hand mode belongs in the plan from the start, mirrored for either side,
built from same-hand rolls rather than alternation. This project has scoped that and not built it.

The transferable lesson is uncomfortable and worth stating plainly: an accessibility decision made
carefully for one body can exclude another, and it will look correct the whole time. The defence is
not better judgment, it is asking who else uses this.

## 5a. Audit the desk before buying anything

The most common finding when this work starts is that the expensive parts are already owned and
unconfigured. A programmable keyboard, a foot pedal, an audio interface, an eye tracker and a
macropad are individually unremarkable purchases that together constitute most of a strain-reduction
rig, and people accumulate them for unrelated reasons.

Two specifics worth knowing, because they change what is possible:

- **A QMK or ZMK keyboard moves remapping into firmware.** Home-row modifiers, layers and tap-hold
  behaviour then live below the operating system. On an immutable or atomic Linux desktop, where
  installing a system-level remapping daemon is the hard path, this turns the best available lever
  into the easiest one.
- **One-shot modifiers are the specific firmware feature to reach for first.** Tap a modifier and it
  applies to the next key rather than being held. That removes sustained modifier load entirely,
  which is the second lever in section 1, and it costs nothing to try.
- **Avoid combos and tap dance, however tempting.** Combos need simultaneous presses, which is the
  chording being designed out. Tap dance is timing-dependent, so it punishes slow or imprecise typing.
  Both get harder to use on exactly the days the hand is worse, which is when an accessibility feature
  most needs to work.

## 5b. Let the macro carry the verbosity

If a programmable key can emit a whole command, the brevity argument stops applying to that key.
One press is the floor regardless of what it sends, so the macro should emit the most legible form,
not the shortest. A transcript full of readable words is worth more later than one full of single
letters, and it costs nothing.

This produces a layering rather than a replacement, and the layers do not compete:

| Layer | Cost | Used when |
|---|---|---|
| A short typed code | one or two keys | Hand-typing on any keyboard |
| A macro key or macropad | one key | At the configured desk |
| Voice, or a foot pedal | no keys | Dictation, flare-ups, one hand |

A useful corollary: a second input device that **cannot** be reprogrammed is not necessarily a
problem. Give it the job that needs no reprogramming. A plain numpad staying a plain numpad can free
a programmable block to become a dedicated command surface with no layer key, and a layer key is
itself a cost worth avoiding.
- **A foot pedal breaks the two-hands assumption cheaply.** Push-to-talk for dictation is the
  obvious use, because holding a key to speak is a sustained load that the pedal removes entirely.
  Modifiers are the other. Pedals are common in transcription work and turn up secondhand.

## 6. Reading load and output noise

Relevant because sections 2 and 4 make keyboard navigation and speech output likely.

Flat text output, suppressed animation and spinners, and colour schemes that defer to the terminal's
own palette rather than overriding it. That last one is the better pattern generally: a user who has
already configured a high-contrast or low-blue-light scheme at the terminal level should have it
respected rather than replaced by a built-in "accessible" theme.

This project's harness exposes ten such settings. None are currently enabled, which is a gap rather
than a decision.

## 7. What tooling does not fix

Tooling reduces load per hour. It does not reduce hours. Scheduling, breaks and workload are the
other half and no configuration substitutes for them. Stated once, because a document that keeps
repeating it becomes a document nobody finishes.

## 8. Open

- None of the tooling in sections 2 through 4 is installed on the machine this was written for.
  Everything above is a research position, not a deployed configuration.
- Whether the harness accessibility settings at section 6 get enabled.
- Standards work for the output side, which is the companion document's scope, not this one's.

## Cross-references

- `interaction-manual.md`: the human-facing manual this supports, particularly its section on pricing
  the input.
- `interface-contract.md`: current status of the brevity code and the input syntax.
- `skills/working-preferences/SKILL.md`: normative location of the brevity code, the input syntax and
  the reply-cost rules.
- A companion document on the accessibility of produced artifacts, covering WCAG, PDF/UA and the
  document pipeline, is held outside this repository with the ingestion specification it belongs to.
