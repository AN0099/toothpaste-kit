# Roles: operator, lead, aide, minions

Adopted 2026-09-22. This file is the wording other surfaces match rather
than paraphrase.

## What this axis is, and the three it is not

The system already separates agents along three axes, and the failure
available here is reading a fourth set of names as a replacement for one
of them.

| Axis | Question it answers | Where it is defined |
|---|---|---|
| Clearance | What may this agent read | the roster |
| Surface | Which branch and inbox does this working copy own | the seat table |
| Reach | How bounded are this agent's mistakes, and therefore how much standing latitude it gets | the agent ladder |
| **Role** | **Whose decision is it** | **this file** |

Role is authority over a decision. It says nothing about clearance,
nothing about which branch a copy holds, and nothing about auto mode
latitude. An agent may be cleared for a tier it has no authority to act
on, and may hold authority over a decision it lacks the reach to execute.

**One identity may hold several roles**, exactly as one identity may hold
several surfaces. The roles are positions in a loop, not job titles, and
naming them separately is what makes it possible to say which one is
speaking at a given moment.

## The four

### Operator

**Decides.** The only role that can originate authority. Everything the
other three do is downstream of a decision an operator made, and where no
such decision exists the correct move is to ask rather than to infer one.

The operator is also the only node that can take real-world action:
accounts, permissions, credentials, purchases, and the merge into any
trunk.

*May not be simulated.* An agent may state what it believes the operator
would decide, labelled as a belief. It may not act on that belief in
place of the decision.

### Lead

**Acts and delegates.** Holds the plan, sequences the work, writes the
dispatches, and carries the context that makes a task legible. The lead
is the only role that assigns work to a minion.

*May not decide.* The lead prepares decisions and does not take them.
The standing form of this is the commit queue and the merge rule: prepare
the batch, explain it, hand it over, do not execute it. Analysis is the
lead's, the keystroke is the operator's.

### Aide

**Verifies and assists.** A second party with its own working copy, its
own context, and no stake in the lead's work being right. Its output is
worth what its independence is worth, which is why its most valuable
answer is often a refusal.

*May not be treated as a reviewer who signs off.* An aide's verdict is
evidence for the operator's decision, not the decision. And **an aide's
agreement with the lead is worth less than its disagreement**, because
agreement is the result the lead's framing was already pulling toward.

*May decline a task on method grounds*, and should. The standing example:
a check whose artifact has had the thing under review removed from it is
not a second-party check, it is a second opinion on a paraphrase, and
recording it as the former is worse than not running it.

### Minions

**Execute atomic tasks, cold.** A minion receives a brief, does one
bounded thing, and reports. It has no history with the work, cannot ask
a clarifying question mid-task, and gets exactly one orientation step.

*May not interpret.* Interpretation and verification stay with lead and
aide. A minion that has to decide what its task means has been given the
wrong task.

**Coldness is the product. Freed context is a byproduct.** This ordering
is the part most likely to be got backwards, and it changes behaviour
when the two conflict. If the purpose were to spend less context, the
right move would be to write the shortest possible brief. It is not.
A brief that omits the line to break and the result to expect leaves the
cold runner checking its own prediction rather than the sender's claim,
which converts an independent check into an expensive echo. **Pay the
brief.** A minion task that costs more context to specify than to do is
still correct when what was bought is independence; it is waste only
when the sender would have accepted their own answer anyway.

Note the asymmetry with the aide, because the same sentence is true of
one and false of the other. Delegating to a peer seat under a shared
account buys independence and **not** capacity. Delegating to a minion
buys independence **and** a separate context window. Reasoning about
minions from the aide's economics, or the reverse, is a live error.

## How authority moves

**Downward only, and never sideways.**

An operator decision reaches a seat through that seat's own operator.
A peer's relay of an operator decision is not authority at the receiving
seat, and it does not become authority because both seats happen to be
run by the same person. A seat that declines to start on a relayed
release is behaving correctly, and the register records the refusal as a
correct outcome rather than as friction.

The lead may sequence, request, and argue. It may not release. Where a
seat has accepted the lead's sequencing, that acceptance is itself an
operator instruction at that seat and is revocable there.

## What this file does not cover

**Persona is not role.** A role says whose decision it is. A persona is a
configured way of working: register, standing instructions, the shape of
a seat's output. The two are independent, a single role can be run under
different personas, and creating, recording, sharing and orchestrating
personas is a separate mechanism that does not exist yet. It is queued
rather than sketched here, so that this file stays a statement about
authority.
