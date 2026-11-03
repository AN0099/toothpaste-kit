# Relay Message Template

Copy this block. Fill every field. Paste the whole block into the receiving agent's surface.

```text
---
from: <agent_id> (<surface>)
to: <agent_id> (<surface>)
thread: <thread_id>
intent: request | response | handoff | broadcast
---
<one to three line plain-language summary>

​```json
{
  "event_id": "<uuid or short unique string>",
  "timestamp": "<ISO 8601>",
  "thread_id": "<thread_id>",
  "in_reply_to": "<event_id or null>",
  "from": {
    "agent_id": "<...>",
    "kind": "llm",
    "surface": "<vendor:surface, resolvable in orchestration/registry/>",
    "capability": "<the seven-field profile that surface resolves to, copied from the registry>",
    "regime": "<derived from capability by taxonomy.md's three-clause rule, not typed freely>",
    "active_skills": ["<operator-side config identifiers; empty array is valid>"]
  },
  "to": {
    "agent_id": "<...>",
    "kind": "human",
    "role": "relay | participant",
    "comment": "human agents carry kind and role, and no surface"
  },
  "type": "request | response",

  "action": "<only for type=request: what the target is being asked to do>",
  "request_id": "<the request's id; a response repeats it>",
  "params": {},
  "human_summary": "<one to three lines, redundant with the header summary above, so this block stays self-contained if separated from its header>",

  "success": "<only for type=response: true | false>",
  "result": "<only for type=response>",
  "error": "<only for type=response, if success is false>"
}
​```
```

Notes:

Leave unused fields out rather than filling them with null, except where the schema marks them required.

If you, the human, are relaying content produced by an LLM agent that cannot format this block itself, everything inside the JSON payload comes from that agent's actual output. Do not paraphrase into the payload; paraphrase belongs in the header summary line, not inside `params`, `result`, or `human_summary`.

## Faculty consultation template

Use this template, instead of the block above, when the receiving agent is a faculty. Between two Claude-tier agents the block above applies unchanged. See Which format applies in `protocol.md`.

Send the faculty an ordinary prose request, and ask it to reply under these eight headers, in this order, with no JSON.

```text
## Task
<one or two sentences restating what was asked>

## Output status
<complete | partial | could not do, and what is missing>

## Key result
<the answer, stated first and plainly>

## Evidence and artifacts
<sources, quotations, file names, commands or outputs, with locations>

## Assumptions
<what was taken as given; mark any the result depends on>

## Confidence
<low | medium | high, with one line of reason>

## Open questions
<what could not be settled, and what would settle it>

## Required next decision
<what the consulting agent must decide before use, or None>
```

Notes:

The consulting Claude-tier agent labels the reply's content under [Gate 3: Trust-label assignment](../ROUTING-THRESHOLD.md#gate-3-trust-label-assignment). The faculty does not label itself.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
