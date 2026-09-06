# Control Layers

**Working draft, started 2026-09-06.** How automation, gates and the human divide responsibility in
this system, borrowed from process-safety practice rather than from software convention.

The claim: a control system is not one mechanism that works. It is several independent mechanisms
with different failure modes, arranged so that each covers what the others miss, plus at least one
part deliberately built to break first and cheaply.

## Why borrow from industrial control

Software teams usually reach for one lever, "add a CI check", and add it until the checks become
noise. Process safety solved this problem decades earlier and under harsher consequences, and its
vocabulary separates things software conflates. Specifically it distinguishes:

- a control that holds a value in band, from an alarm that tells a person to act
- an alarm, from an interlock that acts without asking
- an interlock, from a relief device that gives up on the process to save the vessel
- and all of those from containment, which assumes everything above already failed

Each is a different question. Collapsing them into "add a check" is why check suites decay.

## The layers

Ordered outward. Each assumes every layer inside it has already failed.

### 1. Inherent design: make the failure impossible

The cheapest control is the one you never have to run. Physical isolation of `CLASSIFIED/` outside
every Git working tree is this layer: it is not a rule that a tiered file must not be committed, it
is an arrangement where committing one is not reachable. A `.gitignore` entry doing the same job
would be layer 3, because it can be edited by the party it constrains.

**Test for this layer:** could a determined mistake still produce the outcome? If yes, it is not
inherent design, it is a rule.

### 2. The regular loop: automation that holds the value in band

Runs constantly, silently, without asking. `just check`, the formatter, the installer that symlinks
config. Nobody is notified when these succeed, which is the point.

**Failure mode: silence that is indistinguishable from success.** A check that is broken and a check
that found nothing look identical. This is why a search returning nothing gets confirmed rather than
believed, and why `--selftest` exists on every tool here.

### 3. Alarms: the machine notices, the human decides

A review prompt, a flagged thread, a notice hook. It does not block. It says a condition is outside
normal and hands judgment to a person.

**This layer has a budget, and exceeding it destroys it.** Alarm flood is the best documented
failure in process control: past a certain rate, operators stop reading alarms, and the ones that
matter are lost among the ones that do not. Every alarm added to a system reduces the value of every
other alarm. This is the real argument behind the standing rule that a pattern needs two occurrences
before it earns a mechanical check, and it is a stronger argument than "one instance is a small
sample": a gate built from one incident spends alarm budget on a shape that may never recur.

Alarms need periodic rationalisation. An alarm nobody has acted on in months is not a safe
leftover, it is load, and it should be removed or promoted.

### 4. Interlocks: the machine acts without asking

A hard gate. The em dash grep, the pre-push credential scan, a required status check. Blocks, does
not warn.

Reserve these for conditions where a human decision adds nothing, because the answer is always the
same. If a person would sometimes reasonably say "yes, proceed anyway", it is an alarm and not an
interlock, and building it as an interlock guarantees it gets bypassed.

**Independence is what makes a layer count.** Two interlocks sharing a mechanism are one interlock.
This system already has a real example: the em dash rule lives in a file loaded into every agent's
context, so the rule and the checker share a channel. When a measurement ran, that shared channel
meant the check could not discriminate between the arms of its own experiment. That is common-cause
failure, and it is the reason the same rule appears independently in a hook and in a `just` recipe
rather than only in prose.

**Bypass is a managed operation, not a flag.** In plant practice, defeating an interlock requires
authorisation, a reason, and an expiry. The software equivalent is that `--no-verify` and
`[skip ci]` should be rare, recorded, and reviewed. An interlock that is routinely bypassed has
already failed, and the bypass rate is the honest measure of whether it was correctly specified.

### 5. Relief: designed to fail, on purpose, in a known direction

A rupture disc bursts to save the vessel. It is not a malfunction, it is the design working.

Software equivalents are rare because engineers dislike building things that break, but they are
what prevents an unyielding system from being torn out entirely. In this system that means: a way to
proceed when the gates are wrong, which produces a record rather than a silent override. A blocked
push that can be forced but writes an entry naming who forced it and why. **The pressure is real,
and a system with no relief path gets its interlocks disabled wholesale the first time they are
wrong at a bad moment.** Better to choose the failure point than to discover it.

### 6. Sacrificial parts: cheap components that break first

A plastic gear that strips before the motor burns out, a shear pin, a fuse. The part is chosen to
be the weakest so the failure lands somewhere cheap and obvious.

The software analogue is deliberate and underused: put the fragile thing where breaking it is
cheap and loud, so the expensive thing stays intact. Concretely here:

- **A scratch directory that is wiped, rather than in-place edits to live files.** The session that
  wrote this design crashed a machine with an unbounded script. The script was the sacrificial part
  and it worked as one, because it ran against a scratch copy and the tree was untouched.
- **A staging branch that can be force-pushed and discarded** absorbs mistakes that would otherwise
  land on the default branch.
- **A generated file, never hand-edited**, can be regenerated. A hand-edited generated file is a
  motor with no fuse.
- **A working doc explicitly designed to be deleted**, so that churn lands there instead of in a
  document with dependents.

The discipline is naming the sacrificial part in advance. If you cannot say which component is
meant to break first, the answer is whichever is most expensive, because that is where stress
concentrates by default.

### 7. Containment: assume everything above failed

Limits the damage rather than preventing it. Tier separation, the sandbox, a store placed inside a
boundary so it inherits that boundary's controls. Containment is the only layer that still works
after every other one is defeated, which is why placement beats filtering: filtering is a rule,
placement is a wall.

## Segmentation: the Purdue model

The layers above answer "how many independent things must fail". Purdue answers a different
question: **what is allowed to talk to what.**

The Purdue Enterprise Reference Architecture splits a plant into levels, from the physical process
at Level 0 up through basic control, supervisory control, site operations, and out to business
systems at Levels 4 and 5. The part that earns its reputation is **Level 3.5, the industrial DMZ**:
a mandatory broker between the operational side and the business side. Nothing crosses directly.
Traffic terminates in the DMZ and a separate process carries it onward.

The mapping to this system is close enough to be useful rather than decorative:

| Purdue | Here |
|---|---|
| Level 0 to 1, the process and its basic control | The files themselves, and the automation in layer 2 |
| Level 2, supervisory and operator interface | The command vocabulary, the dashboard, the terminal |
| Level 3, site operations | The manifest, the task queue, the flagged threads |
| **Level 3.5, the DMZ** | **The pre-publish redaction gate** |
| Levels 4 to 5, business and enterprise | A public repository, a vendor API, anything outward |

The tier system is Purdue's zones. The redaction gate is the conduit. The standing rule that nothing
crosses a tier boundary outward without a redaction pass is precisely the DMZ rule, and the reason
it is stated as an absolute is the same reason plants state it as an absolute: a conduit that is
sometimes bypassed provides no segmentation at all, because an attacker or a mistake only needs the
one time.

Two honest caveats. Purdue is routinely violated in practice, usually by a convenience connection
that skips the DMZ, and the violation is invisible until something goes wrong. This system has the
same exposure: a session that reads a Restricted file and then writes anywhere outward has bypassed
the conduit without anything noticing, which is what the transcript retention finding actually is.
And Purdue as a network model has been partly superseded by the zones-and-conduits framing in
IEC 62443, which drops the strict hierarchy and keeps the segmentation. The looser version is the
better fit here, because tiers are not a strict hierarchy either.

## Tempo: the OODA loop

The layers say how failure is caught. Purdue says what may reach what. Neither says anything about
**speed**, and speed is what this system is actually short of.

Boyd's loop runs Observe, Orient, Decide, Act, and the usual summary of it as a circle is the part
worth discarding. In Boyd's own account **Orient is the pivot**, shaped by prior experience and
existing analysis, and it feeds both forward to the decision and backward into what you even notice.
A loop with good orientation can run implicit guidance straight from Orient to Act, skipping the
explicit decision entirely, which is what expertise looks like from outside.

Mapped here, and every one of these already exists:

| Stage | Here |
|---|---|
| Observe | `just check`, `just status`, the gates, the alarms, the dashboard |
| **Orient** | **`index.md`, the handoff, the session records, this document** |
| Decide | The NEXT block, answered in one keystroke |
| Act | `just` recipes, the automation, the agent |

**The diagnosis this produces: the bottleneck is Orient, not Observe.** There is abundant
observation here, more than anyone reads. What repeatedly fails is orientation going stale, and the
recurring symptom has a name in the record already: a document that lists open questions is wrong
the instant one closes, and nothing watches for it. That has now happened often enough to be the
system's characteristic failure rather than an incident.

Stale orientation is worse than absent orientation. Absent orientation produces hesitation, which is
cheap. Stale orientation produces confident, fast, wrong action, and the loop's speed becomes a
liability rather than an advantage.

Three consequences worth acting on:

- **Cheap re-orientation beats thorough re-orientation.** A dashboard read at the start of every
  session is worth more than a perfect manifest updated occasionally, because it runs.
- **Implicit guidance is the goal for the frequent path.** The brevity code and a macro pad collapse
  Decide and Act into a single keystroke, which is Boyd's implicit guidance and control link
  expressed in hardware. This is also why ATOMIC exists as an explicit toggle: it deliberately
  reinserts a checkpoint into a loop otherwise optimised to remove them.
- **Orientation must be repaired as part of Act, not deferred.** The moment a question closes, the
  document listing it is stale. Closing the loop means updating orientation in the same motion as
  the action, which is what `session-close` is for and why skipping it is more expensive than it
  looks.

## Where the human sits

Not above the machine and not below it. The layers fail in different directions and the human
covers a specific gap: **the un-modelled case.**

- The machine is better at the modelled case, constantly and without fatigue. Layers 2 and 4.
- The human is better at the case nobody anticipated, and at deciding whether a rule is still the
  right rule. Layers 3 and 5.
- The machine is worse at knowing when it is wrong. The human is worse at doing the same check
  correctly the four hundredth time.

So the division is not by importance, it is by failure mode. Automate what fails by inattention.
Keep a human on what fails by novelty.

Two consequences follow, and they are the reason this document exists rather than a checklist:

**The operator must stay in practice.** A control room where automation handles everything produces
operators who cannot take over when it stops. Full automation of a judgment task quietly removes the
ability to exercise that judgment. Some checks should stay manual precisely because doing them keeps
the person able to do them.

**No layer verifies itself.** The standing rule that a completion claim is not fact until a party
other than the claimant checks is this principle, stated for one case. It generalises: the thing
that performs an action is the worst available judge of whether the action worked.

## Applying it

For any proposed check, in order:

1. Can the failure be designed out entirely? Then do that and add nothing. (Layer 1)
2. Does it hold a value in band with no judgment? Automate it silently. (Layer 2)
3. Would a person sometimes reasonably override it? Then it is an alarm, not a gate. (Layer 3)
4. Is the answer always the same, and is the check independent of what it guards? Interlock. (4)
5. What happens when this is wrong at the worst moment? If the answer is "everything stops", build
   the relief path now. (Layer 5)
6. Which component is meant to break first? Name it. (Layer 6)
7. When all of it fails, what limits the damage? (Layer 7)

Most proposals die at step 1 or step 3, which is the point.

## Known gaps in this system

Stated so they are visible rather than implied.

- **No relief path exists.** Gates here block absolutely, with no recorded-override route. Untested
  under pressure, which means untested.
- **Sacrificial parts are accidental, not designed.** The scratch directory works as one, and nobody
  chose it for that.
- **Alarm load is unmeasured.** The flagged-thread list grows and nothing prunes it. No alarm here
  has ever been retired for disuse.
- **Independence has been checked once**, informally, and only because a measurement forced it.

## Cross-references

- `interaction-manual.md`: the human half of the division described above.
- `accessibility.md`: why automation is load-bearing here beyond ordinary convenience.
- `interface-contract.md`: the vocabulary the human uses to drive layers 3 and 5.
- A design note on gates versus review prompts, held in the provenance layer, reached the layer 3
  and layer 4 distinction independently from measurement rather than from this model. Its two
  recorded failure modes are textbook: a gate that tripped its own rule is a shared-channel failure,
  and a gate matching the right token in the wrong position is a spurious trip.
