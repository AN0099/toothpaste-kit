# Philosophy

## The name

A toothpaste factory automates away the job of the man who caps the tubes. He does not get that job back. He gets a different one that exists only because the machine does: keeping it running, understanding what it does, pointing it at the right work. The reference is Charlie's father in Charlie and the Chocolate Factory.

That is the thesis. An AI system is a machine that works best with someone who understands the job standing next to it.

The README states the same relationship as a rider and a horse joined by tack. The two images are aimed at different readers and neither replaces the other. The factory is about what happens to the work. The tack is about where the control actually sits.

## Direction over delegation

Hand an agent a goal and walk away, and you get confident output with nobody accountable for whether it is true. The leverage in these tools comes from an operator who knows the domain, sets the constraints, and checks the result. Everything here is built to make that person faster.

That principle shows up in concrete design choices:

- Each skill states what it does not cover and names the skill that does, so an agent reaching past its scope is visible in the description rather than discovered in the output.
- The command vocabulary is short and fixed, because ambiguous instructions produce plausible work on the wrong problem.
- Sessions declare which behavioral regime they run under. A confirmation gate with nobody present to answer it does not degrade into caution. It stalls.

## Verification

Three rules, in force for every agent and every person working on this project.

**A completion claim is not a fact until someone other than the claimant checks it.** An agent reporting success is reporting an intention. The file either exists or it does not, and finding out is cheap.

**Self-audit is not verification.** An agent explaining its own error produces a narrative about the error. Establishing what actually happened is a different activity, and the narrative is often wrong in ways that sound convincing.

**Findings get raised.** A disagreement settled quietly by whoever noticed it first is a decision that skipped review.

None of these are abstract. Each one was written after a specific failure.

## Incidents are recorded

Failures in this project get written up as postmortems and kept. An agent fabricated tool calls it never made. A hard style prohibition spread its own violation across three tiers of agents through unconscious imitation, with each tier copying the register of the one above it. A model produced a confident and entirely false audit of its own role confusion, discovered only because someone tested for it deliberately.

Keeping these on the record costs some polish. It buys the only thing that makes the verification rules above credible, which is evidence that they were written in response to something real by people who got it wrong first.

## Operable by more than one kind of person

An interface is only an interface for the people who can operate it. A project whose entire product is the contact surface between a person and a machine has no coherent way to treat accessibility as something added at the end, because the accessibility of that surface is the thing working or not working.

In practice this means plain text over rendered output wherever there is a choice, structure that survives being read aloud, and no control whose only signal is colour or motion. A contribution that assumes one input method, one output channel, or one kind of attention is not finished.

## Forkable by construction

The core stays self-hostable and forkable. The skills are plain Markdown. The tools are standard-library Python against SQLite and BibTeX, both of which outlive any particular vendor. Interoperability is treated as a permanent constraint on the design, checked when new dependencies are considered.
