# Relay Protocol

## Format

Every message that crosses a surface boundary, except a faculty consultation (see Which format applies), is a single block with two parts: a short human-readable header, and a JSON payload conforming to `schemas/request.json` or `schemas/response.json`.

```text
---
from: <agent_id> (<surface>)
to: <agent_id> (<surface>)
thread: <thread_id>
intent: request | response | handoff | broadcast
---
<one to three line plain-language summary of what this message asks for or reports>

​```json
{ the actual event, matching event-base.json plus request.json or response.json }
​```
```

The header exists so a human relay agent never has to parse JSON to know where a message goes or, roughly, what it says. The JSON exists so any receiving LLM agent, or downstream tooling, can parse the message deterministically rather than re-deriving intent from prose. Neither half is optional. A message with only the header loses machine-parseability; a message with only JSON defeats the point of having a human relay role at all.

## Turn-taking

Exactly one agent holds the token, meaning it is expected to produce the next message, at any point in a thread. The `to` field of the most recent message names who holds it.

An LLM agent that cannot itself format the header-plus-JSON block, for example a chat instance replying only in prose mid-conversation, delegates formatting to whichever human is acting as relay for that hop. The relay human's job in that case still excludes editing the LLM's actual content; only the wrapping is theirs to produce. A faculty consultation does not use this route; it uses the lighter format described under Which format applies.

A `broadcast` intent is addressed to all agents in the thread, and each replies independently, referencing `in_reply_to`. Its event still carries the one `to` that `schemas/event-base.json` requires.

## Timing

Machine agents use `timeout_ms`. Human agents do not operate on millisecond timers, so a request addressed to an agent with `kind: "human"` should set `expected_response_by` instead, and the sending agent should not treat silence past that point as failure the way it would treat a machine timeout. Escalation on a missed human response is a judgment call for whoever is monitoring the thread, not an automatic protocol event.

## State handoff

Every new chat window starts with no memory of the thread. Two consequences follow.

First, any message addressed to a fresh `chat` or `cowork-interactive` agent should include enough of `templates/handoff-note.md`, inline or as a preceding paste, to bootstrap that agent without requiring it to ask. This is the same principle as the session handoff document in [`examples/workspace/.agents/lead-handoff.md`](../examples/workspace/.agents/lead-handoff.md); this protocol generalizes it to apply across agents, not only across sessions of one agent.

Second, `thread_id` is the unit of continuity, not any single agent's memory. Nothing in this protocol assumes an agent remembers a prior message unless that message, or a handoff note summarizing it, is present in its current context.

## Relay fidelity

A human agent with `role: "relay"` forwards the JSON payload byte for byte. If a human needs to add a note, correct an error, or make a decision while relaying, that addition goes in a separate, clearly marked block appended after the original payload, not edited into it, and the `relayed_by` field on the next event in the thread should record that the human acted with `role: "participant"` for that hop. Silent edits during relay are the single most likely failure mode in this system, since they are invisible to both the sending and receiving LLM agents unless flagged.

## What this protocol does not solve

It does not resolve conflicting instructions arriving from two agents in the same thread; that remains a judgment call for whoever holds the token next.

It does not enforce that a human agent claiming `role: "relay"` actually behaves as one rather than as a participant. That enforcement is social, not technical: the format makes deviation visible after the fact, by comparing the payload to what got pasted, but it does not prevent it.

## Which format applies

Two formats exist, and the pair of agents decides which one is used.

| Sender and receiver | Format |
|---|---|
| A Claude-tier agent and another Claude-tier agent | The header and JSON payload described under Format, unchanged |
| A Claude-tier agent and a faculty | The faculty-consultation format described below |

A faculty is a model a Claude-tier agent routes part of a task to, as defined in the [glossary](../docs/glossary.md) and governed by [the routing threshold](routing-threshold.md). It is consulted in an ordinary chat interface, which will not reliably emit the JSON payload, so the lighter format applies to every faculty consultation and the JSON payload is never required of a faculty. No other pair is covered by this section. A human relay between a Claude-tier agent and a faculty still follows Relay fidelity: the reply is forwarded as the faculty wrote it.

## Faculty-consultation format

The consulting Claude-tier agent sends its request as ordinary prose; this protocol prescribes no request format for a faculty. The faculty's reply is plain Markdown with no JSON payload and no header block, using these eight headers in this order. Every header appears, and a header with nothing to report says "None".

### Task

One or two sentences restating what the faculty was asked to do, so the reply stands alone if separated from the request.

### Output status

One of: complete, partial, or could not do. A partial or could-not-do status says what is missing.

### Key result

The answer itself, stated first and plainly. Anything the consulting agent will use goes here.

### Evidence and artifacts

The sources, quotations, file names, commands or outputs the result rests on. A source the faculty cites is listed here with its location, so the consulting agent can check it. Strip any signed or token-bearing URL before it lands in a file, per Gate 3.

### Assumptions

What the faculty took as given without being told. An assumption the result depends on is marked as such.

### Confidence

Low, medium or high, with one line of reason. This is the faculty's own estimate and is not a trust label.

### Open questions

What the faculty could not settle and what would settle it.

### Required next decision

What the consulting agent must decide before the result is used, or "None" if the result can be used as it stands.

## Trust label for a faculty reply

The reply carries no trust label from the faculty. The consulting Claude-tier agent assigns the label to the reply's content under [Gate 3: Trust-label assignment](routing-threshold.md#gate-3-trust-label-assignment), which this protocol does not restate. Confidence above does not set the label.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
