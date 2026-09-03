# Relay Message Template

Copy this block. Fill every field. Paste the whole block into the receiving agent's surface.

```
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
    "kind": "llm | human",
    "surface": "<one of the taxonomy surfaces>",
    "regime": "<looked up from surface-regimes skill, not typed freely>",
    "active_skills": ["<looked up from surface-regimes skill's activation table>"]
  },
  "to": {
    "agent_id": "<...>",
    "kind": "llm | human",
    "surface": "<one of the taxonomy surfaces>",
    "regime": "<looked up from surface-regimes skill, not typed freely>",
    "active_skills": ["<looked up from surface-regimes skill's activation table>"]
  },
  "type": "request | response",

  "action": "<only for type=request: what the target is being asked to do>",
  "request_id": "<only for type=request>",
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
