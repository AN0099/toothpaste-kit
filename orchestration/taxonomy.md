# Agent Taxonomy

## Grounding

The four surface names (chat, Cowork, Code, API) are Anthropic's actual product names, and this taxonomy is built on their real, current constraints rather than treating the names as arbitrary labels. Two things about this grounding matter for anyone extending the taxonomy later.

First, compliance and audit coverage for Cowork is an area of active change. As of this document's writing, one source describes Cowork activity as recently added to Compliance API and audit log coverage; an earlier source describes Cowork as excluded from both, with conversation history kept locally on the user's machine. Treat any claim about Cowork's audit posture in this document as **Derived**, not **Verified**, and check `docs.claude.com` before it becomes load-bearing in anything shared outside this project.

Second, the real fault line is not "chat versus everything else." It is whether a surface executes autonomously, multi-step, between human turns. Chat does not, by default. Cowork and Code do. This is the property the taxonomy routes on.

## Surfaces and sub-roles

### Chat (`chat`)

Conversational loop. Human present for every turn. No autonomous execution between turns beyond tool calls made and returned within a single turn. No persistent file workspace by default. Lowest setup cost; best suited to planning, drafting, and judgment calls that benefit from a human staying in the loop turn by turn.

### Cowork

Same underlying agentic engine as Code, retargeted at knowledge work: files, documents, spreadsheets, browser. Desktop app.

- **`cowork-interactive`**: human describes the outcome and stays present, able to redirect mid-task.
- **`cowork-delegated`**: human describes the outcome and leaves; Cowork executes multi-step work autonomously and the human returns later to review. This sub-role is functionally closest to a Code headless run, but confined to knowledge-work tools rather than a code environment.

### Code

Agentic coding assistant, terminal or IDE.

- **`code-interactive`**: human present, turn by turn, in a terminal or IDE session.
- **`code-headless-routine`**: runs on Anthropic-managed cloud infrastructure. Scheduled, API-triggered, or event-triggered (for example, a GitHub event). The human's machine does not need to be on. No human present during execution.
- **`code-local-routine`**: a desktop-scheduled task with the same unattended-execution profile as `code-headless-routine`, but requiring the local machine to stay on, since it runs on it rather than in the cloud.

### API

Programmatic access, no chat UI.

- **`api-raw`**: direct calls to the Messages API. Single request, single response. Any autonomy across multiple calls is built and owned by the calling application, not the API itself.
- **`api-agent-sdk`**: the Agent SDK, which packages the same autonomous, multi-step, tool-using loop that powers Code into a library the calling application controls. Functionally closer to `code-headless-routine` than to `api-raw`, despite both falling under "API."

### Human

The human is a node in the graph, not only the mechanism that moves messages between other nodes. Two roles, and they should not be conflated.

**`human-relay`**: passive. Copies a message produced by one agent and pastes it into another agent's surface, without editing its content or inserting judgment. A relay human's failure mode is transcription drift: dropping a line, retyping instead of pasting, summarizing instead of forwarding verbatim.

**`human-participant`**: active. Reads and contributes semantic content: makes a decision an LLM agent flagged as a judgment call, overrides a plan, breaks a tie. A participant human's failure mode is the inverse of the relay human's: silently editing content that should have been forwarded intact, without flagging that an edit happened.

A single human can hold both roles across a run, but should not hold both roles for the same message. If a human edits content while relaying it, that is a `human-participant` act, and the message log should say so (see `protocol.md`, relay fidelity).

## Capability matrix

| Surface | Autonomous multi-step execution | Human presence required during execution | Persistent workspace | Audit/compliance coverage | Regime |
|---|---|---|---|---|---|
| `chat` | No | Yes | No, per-session | Enterprise: yes | interactive-synchronous |
| `cowork-interactive` | Partial, redirectable | Yes | Yes, local | Evolving; verify live | interactive-synchronous |
| `cowork-delegated` | Yes | No | Yes, local | Evolving; verify live | autonomous-asynchronous |
| `code-interactive` | Partial, redirectable | Yes | Yes | Enterprise: yes | interactive-synchronous |
| `code-headless-routine` | Yes | No | Yes, cloud | Enterprise: yes (Routines are part of Code) | autonomous-asynchronous |
| `code-local-routine` | Yes | No, but machine must stay on | Yes, local | Enterprise: yes | autonomous-asynchronous |
| `api-raw` | No, caller-built | Depends on caller | Caller-defined | Caller-defined | programmatic-contractual |
| `api-agent-sdk` | Yes | No | Caller-defined | Caller-defined | autonomous-asynchronous |
| `human-relay` | N/A | N/A | N/A | N/A | N/A |
| `human-participant` | N/A | N/A | N/A | N/A | N/A |

## Regime, dial adjustment, and skill activation

This taxonomy's surfaces map to three behavioral regimes, and each regime carries its own adjustments to `working-preferences` dials and its own default skill activation. That mapping lives in the `surface-regimes` skill (`skills/surface-regimes/SKILL.md`), not duplicated here, so the two can't drift apart. The `regime` column above is the join key.
