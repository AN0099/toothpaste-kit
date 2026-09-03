# Relay Protocol

## Format

Every message that crosses a surface boundary is a single block with two parts: a short human-readable header, and a JSON payload conforming to `schemas/request.json` or `schemas/response.json`.

```
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

The header exists so a `human-relay` agent never has to parse JSON to know where a message goes or, roughly, what it says. The JSON exists so any receiving LLM agent, or downstream tooling, can parse the message deterministically rather than re-deriving intent from prose. Neither half is optional. A message with only the header loses machine-parseability; a message with only JSON defeats the point of having a human-relay role at all.

## Turn-taking

Exactly one agent holds the token, meaning it is expected to produce the next message, at any point in a thread. The `to` field of the most recent message names who holds it.

An LLM agent that cannot itself format the header-plus-JSON block, for example a chat instance replying only in prose mid-conversation, delegates formatting to whichever human is acting as relay for that hop. The relay human's job in that case still excludes editing the LLM's actual content; only the wrapping is theirs to produce.

A `broadcast` intent has no single `to`. It is addressed to all agents in the thread, and each replies independently, referencing `in_reply_to`.

## Timing

Machine agents use `timeout_ms`. Human agents do not operate on millisecond timers, so a request addressed to a `human-relay` or `human-participant` agent should set `expected_response_by` instead, and the sending agent should not treat silence past that point as failure the way it would treat a machine timeout. Escalation on a missed human response is a judgment call for whoever is monitoring the thread, not an automatic protocol event.

## State handoff

Every new chat window starts with no memory of the thread. Two consequences follow.

First, any message addressed to a fresh `chat` or `cowork-interactive` agent should include enough of `templates/handoff-note.md`, inline or as a preceding paste, to bootstrap that agent without requiring it to ask. This is the same principle as the export-style session handoff document already used elsewhere in this project; this protocol generalizes it to apply across agents, not only across sessions of one agent.

Second, `thread_id` is the unit of continuity, not any single agent's memory. Nothing in this protocol assumes an agent remembers a prior message unless that message, or a handoff note summarizing it, is present in its current context.

## Relay fidelity

A `human-relay` agent forwards the JSON payload byte for byte. If a human needs to add a note, correct an error, or make a decision while relaying, that addition goes in a separate, clearly marked block appended after the original payload, not edited into it, and the `relayed_by` field on the next event in the thread should record that the human acted in a `human-participant` capacity for that hop. Silent edits during relay are the single most likely failure mode in this system, since they are invisible to both the sending and receiving LLM agents unless flagged.

## What this protocol does not solve

It does not resolve conflicting instructions arriving from two agents in the same thread; that remains a judgment call for whoever holds the token next.

It does not enforce that a human-relay agent actually behaves as a relay rather than a participant. That enforcement is social, not technical: the format makes deviation visible after the fact, by comparing the payload to what got pasted, but it does not prevent it.
