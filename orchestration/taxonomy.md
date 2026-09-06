# Agent Taxonomy

## Grounding

This taxonomy describes what a surface can do. Product names are a label on top of that, resolved
through `registry/`.

Two things about that ordering matter for anyone extending the taxonomy later.

First, the real fault line is not "chat versus everything else." It is whether a surface executes
autonomously, multi-step, between human turns. Chat does not, by default. Cowork and Code do. That
property, plus six others below, is what the protocol routes on, and none of the seven mentions a
vendor.

Second, capability claims about live products go stale. Compliance and audit coverage for Cowork is
an area of active change: as of writing, one source describes Cowork activity as recently added to
Compliance API and audit log coverage, and an earlier source describes it as excluded from both,
with conversation history kept locally. The registry records that as `audit: "unknown"` with a
`verified_on` date rather than resolving it, because a confident wrong value is worse than an honest
gap. Every registry entry carries the same three evidence fields for the same reason.

## The capability vector

Seven vendor-independent predicates. Any surface from any vendor scores on all of them. The full
JSON definition is `schemas/event-base.json#/definitions/capability_profile`.

| Field | Values | What it decides |
|---|---|---|
| `interface` | `conversational`, `programmatic` | whether a caller owns the loop |
| `autonomy` | `none`, `redirectable`, `full` | multi-step execution between human turns |
| `human_presence` | `required`, `optional`, `absent` | whether anyone is watching |
| `workspace` | `none`, `session`, `local`, `remote` | where persistent state lives |
| `tool_execution` | `none`, `sandboxed`, `host` | whether execution reaches the host filesystem |
| `egress` | `local`, `operator-hosted`, `vendor-cloud` | where content goes when processed |
| `audit` | `none`, `local-only`, `vendor-attested`, `operator-attested`, `unknown` | who attests to a record |

`egress` is the join key for any sensitivity gate. A routing rule that must decide whether content
may reach a given faculty reads this field rather than depending on an operator remembering which
faculties are cloud-hosted.

`tool_execution` is the join key for a tool-call trust exclusion. A faculty with `none` cannot be
handed a task that writes to a repository, regardless of how capable it is at drafting.

## Deriving the regime

Three clauses, first match wins:

1. `interface` is `programmatic` and `autonomy` is `none`, then `programmatic-contractual`.
2. `human_presence` is `required`, then `interactive-synchronous`.
3. Otherwise, `autonomous-asynchronous`.

The rule reproduces every row of the capability matrix below, including the two counterintuitive
ones. `api-agent-sdk` falls through both early clauses and lands on `autonomous-asynchronous`,
which is where its behavior belongs even though its product family is "API." `api-raw` terminates
at clause 1. That the rule recovers all eight rows is the evidence that these are the right seven
predicates: a rule that failed on even one row would mean the vector is missing something.

## Surfaces and sub-roles

The surfaces below are Anthropic's, described here because they are the ones this protocol was
first built against. Their capability values live in `registry/anthropic.json`. Other vendors go in
their own registry file and need no prose section here.

### Chat (`anthropic:chat`)

Conversational loop. Human present for every turn. No autonomous execution between turns beyond
tool calls made and returned within a single turn. No persistent file workspace by default. Lowest
setup cost; best suited to planning, drafting, and judgment calls that benefit from a human staying
in the loop turn by turn.

### Cowork

Same underlying agentic engine as Code, retargeted at knowledge work: files, documents,
spreadsheets, browser. Desktop app.

- **`anthropic:cowork-interactive`**: human describes the outcome and stays present, able to
  redirect mid-task.
- **`anthropic:cowork-delegated`**: human describes the outcome and leaves; Cowork executes
  multi-step work autonomously and the human returns later to review. This sub-role is functionally
  closest to a Code headless run, but confined to knowledge-work tools rather than a code
  environment.

### Code

Agentic coding assistant, terminal or IDE.

- **`anthropic:code-interactive`**: human present, turn by turn, in a terminal or IDE session.
- **`anthropic:code-headless-routine`**: runs on vendor-managed cloud infrastructure. Scheduled,
  API-triggered, or event-triggered (for example, a GitHub event). The human's machine does not need
  to be on. No human present during execution.
- **`anthropic:code-local-routine`**: a desktop-scheduled task with the same unattended-execution
  profile as the headless routine, but requiring the local machine to stay on. Note that its
  `egress` is still `vendor-cloud`: running the scheduler locally does not keep the content local.

### API

Programmatic access, no chat UI.

- **`anthropic:api-raw`**: direct calls to the Messages API. Single request, single response. Any
  autonomy across multiple calls is built and owned by the calling application, not the API itself.
- **`anthropic:api-agent-sdk`**: the Agent SDK, which packages the same autonomous, multi-step,
  tool-using loop that powers Code into a library the calling application controls. Functionally
  closer to a headless routine than to `api-raw`, despite both falling under "API."

### Human

The human is a node in the graph, not only the mechanism that moves messages between other nodes.

Human agents carry `kind: "human"` and a `role`, and no `surface`. The two roles should not be
conflated.

**`role: "relay"`**: passive. Copies a message produced by one agent and pastes it into another
agent's surface, without editing its content or inserting judgment. A relay human's failure mode is
transcription drift: dropping a line, retyping instead of pasting, summarizing instead of forwarding
verbatim.

**`role: "participant"`**: active. Reads and contributes semantic content: makes a decision an LLM
agent flagged as a judgment call, overrides a plan, breaks a tie. A participant human's failure mode
is the inverse of the relay human's: silently editing content that should have been forwarded
intact, without flagging that an edit happened.

A single human can hold both roles across a run, but should not hold both roles for the same
message. If a human edits content while relaying it, that is a participant act, and the message log
should say so (see `protocol.md`, relay fidelity).

Earlier versions of this protocol expressed both roles as members of the `surface` enum, which made
the meaningless combination `kind: "llm"` with `surface: "human-relay"` a valid event. Splitting
`role` off fixed that.

## Capability matrix

Values are the current registry contents. The registry is authoritative; this table is a reading
aid and will drift.

| Surface | interface | autonomy | human_presence | workspace | tool_execution | egress | audit | Regime |
|---|---|---|---|---|---|---|---|---|
| `anthropic:chat` | conversational | none | required | session | sandboxed | vendor-cloud | vendor-attested | interactive-synchronous |
| `anthropic:cowork-interactive` | conversational | redirectable | required | local | host | vendor-cloud | unknown | interactive-synchronous |
| `anthropic:cowork-delegated` | conversational | full | absent | local | host | vendor-cloud | unknown | autonomous-asynchronous |
| `anthropic:code-interactive` | conversational | redirectable | required | local | host | vendor-cloud | vendor-attested | interactive-synchronous |
| `anthropic:code-headless-routine` | conversational | full | absent | remote | host | vendor-cloud | vendor-attested | autonomous-asynchronous |
| `anthropic:code-local-routine` | conversational | full | absent | local | host | vendor-cloud | vendor-attested | autonomous-asynchronous |
| `anthropic:api-raw` | programmatic | none | optional | none | none | vendor-cloud | operator-attested | programmatic-contractual |
| `anthropic:api-agent-sdk` | programmatic | full | absent | local | host | vendor-cloud | operator-attested | autonomous-asynchronous |

Human agents have no capability profile and no regime. They are typed by `kind` and `role`.

## Regime, dial adjustment, and skill activation

Each regime carries its own adjustments to `working-preferences` dials and its own default skill
activation. That mapping lives in the `surface-regimes` skill
(`skills/surface-regimes/SKILL.md`), not duplicated here, so the two cannot drift apart. The
`regime` field is the join key.
