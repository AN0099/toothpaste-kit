# Philosophy

An AI system is a machine that works best with someone who understands the job
standing next to it. Everything below follows from that.

## Who this is for, in the author's words

> BLUF: *nix-inspired, cloud-native, human-machine interface suite for senior/administrative roles orchestrating collaborative work or building work platforms; DevOps, Management, Head Engineers/Researchers/Developers, etc.

## Why this exists

Two images, aimed at different readers. The first is about what happens
to the work. The second is about where the control actually sits.

### Toothpaste Repairman: Automation Engineering

In the 2005 film-adaption of Charlie and the Chocolate Factory, Mr. Bucket screws caps onto toothpaste
tubes until the factory buys a machine that does it faster, and he is let go. He ends the story
hired back to repair the machine that replaced him. That second job is the one this repository is
about. It is harder than the first in every way that matters. Capping tubes needed his hands.
Repairing the capper needs him to understand what the machine is doing and to notice when it stops
doing it, which is the one part of the work the machine cannot take over, because the job is
knowing whether the machine is working.

Everything here is built for the repairman rather than for someone operating a finished product. A
repairman is judged on whether the machine runs, not on how impressive it looks while running, and
that is why this project measures itself on control fidelity instead of capability: legible state,
cheap correction, a reliable halt. It is also why so much of what is here is checks that fail
loudly rather than features that succeed quietly. Nobody keeps a repairman who cannot tell when the
machine is broken, and a check that reports clean because it was never wired up is worse than no
check at all, since it spends the attention that would have found the fault.

### Riding Tack: User Interface and Experience

The "centaur" analogy of automation theory imagines a human-machine collaboration where a person uses technology as a powerful, tireless assistant to execute tasks while retaining ultimate control over judgment and decision-making: a human orchestrator directing an automated agent, each unable to complete the work without the other. The reverse-centaur inverts the roles. An automated orchestrator directs a human agent, the person in the loop only because the machine has no fleshy appendages of its own to do the work.

The analogy holds best with deterministic automated systems, computers and machines where the same input produces the same output every time and 1 + 1 is always 2. Such systems have no will of their own to negotiate with. Applied to a non-deterministic system the centaur gets portrayed as one organism, and it will not be one until human and machine are literally fused. More accurately, what you have is a rider and a horse: two wills, one of them in charge, joined by riding tack.

The tack is the interface. A rider does not think the horse forward. They apply pressure through equipment, the horse interprets it, and the result depends almost entirely on the quality of that equipment and the operator's skill. The horse acts non-deterministically, and retraining it is not on the table, so tack and skill are the only levers left for improving how reliably it does what was asked. When the tack is bad, even a skilled rider ends up going where the horse chose to go, which is the failure this repository exists to prevent.

Model capability improves or degrades without us and is somebody else's product. What is here is tack: the skills, protocols, and gates through which a person's intent reaches a capable system, and through which that system's state comes back legible. Every piece of it is judged on control fidelity rather than capability: can you tell where you are going, correct early, and stop.

One consequence shapes what gets accepted here. An interface is only an interface for the people who can operate it. Reins you cannot feel are not reins.

This is not a separate concern bolted onto the design. Tack already comes in many forms because riders and horses vary, and nobody treats a different bit or a different saddle as an accommodation; it is the same equipment fitted to the hands actually holding it. An interface that assumes one input method, one output channel, or one kind of attention has not been fitted to anyone. It has been fitted to an average that does not exist.

The practical result is the one every curb cut demonstrates. Fitting the interface to the widest range of operators produces something better for all of them.

## What follows from that

### Direction over delegation

Hand an agent a goal and walk away, and you get confident output with nobody accountable for whether it is true. The leverage in these tools comes from an operator who knows the domain, sets the constraints, and checks the result. Everything here is built to make that person faster.

That principle shows up in concrete design choices:

- Each skill states what it does not cover and names the skill that does, so an agent reaching past its scope is visible in the description rather than discovered in the output.
- The command vocabulary is short and fixed, because ambiguous instructions produce plausible work on the wrong problem.
- Sessions declare which behavioral regime they run under. A confirmation gate with nobody present to answer it does not degrade into caution. It stalls.

### Verification

Three rules, in force for every agent and every person working on this project.

**A completion claim is not a fact until someone other than the claimant checks it.** An agent reporting success is reporting an intention. The file either exists or it does not, and finding out is cheap.

**Self-audit is not verification.** An agent explaining its own error produces a narrative about the error. Establishing what actually happened is a different activity, and the narrative is often wrong in ways that sound convincing.

**Findings get raised.** A disagreement settled quietly by whoever noticed it first is a decision that skipped review.

None of these are abstract. Each one was written after a specific failure.

### Incidents are recorded

Failures in this project get written up as postmortems and kept. An agent fabricated tool calls it never made. A hard style prohibition spread its own violation across three tiers of agents through unconscious imitation, with each tier copying the register of the one above it. A model produced a confident and entirely false audit of its own role confusion, discovered only because someone tested for it deliberately.

Keeping these on the record costs some polish. It buys the only thing that makes the verification rules above credible, which is evidence that they were written in response to something real by people who got it wrong first.

### Operable by more than one kind of person

Stated once in Riding Tack above and not repeated here. What it means in practice:  plain text over rendered output wherever there is a choice, structure that survives being read aloud, and no control whose only signal is colour or motion. A contribution that assumes one input method, one output channel, or one kind of attention is not finished.

### Forkable by construction

The core stays self-hostable and forkable. The skills are plain Markdown. The tools are standard-library Python against SQLite and BibTeX, both of which outlive any particular vendor. Interoperability is treated as a permanent constraint on the design, checked when new dependencies are considered.
