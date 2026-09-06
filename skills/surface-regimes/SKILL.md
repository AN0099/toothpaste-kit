---
name: surface-regimes
description: Detects which of three behavioral regimes the current session runs under, interactive-synchronous, autonomous-asynchronous, or programmatic-contractual, and adjusts working-preferences dials and mechanics, and document-standards/technical-documents applicability, accordingly. Regime is derived from a session's capability profile rather than from a vendor's product name, so it holds on any vendor's surface. Applies to any single session on any agent surface, not only multi-agent relay threads. Trigger on any mention of Cowork, Routine, headless, Agent SDK, raw API call, a CLI or IDE coding agent from any vendor, or an explicit regime, capability, or surface field in a relay or handoff message.
---

# Purpose

`working-preferences` states mechanics (Q1-3, propose-before-generating, dial baselines) as if one register fits every session. It does not, because "a human is present and can respond before the next step" is true in a chat window and false in a Routine running unattended. This skill states which mechanics apply, and at what dial setting, based on which of three regimes the current session actually runs under. It does not replace `working-preferences`; it sets the dial before that skill's task-specific override applies.

Regime is a property of what a session can do. Product names are a label on top of that property, so the same three regimes hold whether a session runs on Anthropic's surfaces, another vendor's, or a locally hosted model.

# Regime Detection

1. If a `capability` profile is present in context, for example on an agent reference in a relay message or handoff note from the multi-agent orchestration protocol, derive the regime from it using the rule below. Authoritative, skip inference.
2. If a stated `regime` is present without a capability profile, use it. If both are present and disagree, the capability profile governs and the mismatch is worth surfacing rather than silently resolving.
3. If only a `surface` identifier is present, resolve it against `orchestration/registry/` to get its capability profile, then derive.
4. Otherwise infer from session context: which interface is described in the system prompt or surrounding tooling (a chat window, a desktop agent app, a terminal or IDE coding agent, or an API call with no chat UI), whether a human can plausibly respond before the next step executes, whether the output is consumed by a program as a data contract rather than read by a person.
5. If inference is ambiguous, default to interactive-synchronous. This is the safe default: it keeps every confirmation gate and dial baseline active rather than silently assuming no human is present.

## The derivation rule

Three clauses, first match wins:

1. `interface` is `programmatic` and `autonomy` is `none`, then **programmatic-contractual**.
2. `human_presence` is `required`, then **interactive-synchronous**.
3. Otherwise, **autonomous-asynchronous**.

The full capability vector and the evidence that this rule reproduces every row of the surface taxonomy it was extracted from live in `orchestration/taxonomy.md`. Treat `human_presence: optional` as `required` for gating purposes until a human's absence is actually confirmed, per step 5's default.

# Three Regimes

**Interactive-synchronous.** A human is present for the current exchange and can respond before the next step happens. Chat, an interactive desktop agent session, an interactive terminal or IDE coding session.

**Autonomous-asynchronous.** No human present during execution. Output is reviewed after the fact, if at all. A delegated desktop agent run, a scheduled or event-triggered headless routine, a local unattended routine, an agent SDK loop owned by a calling application.

**Programmatic-contractual.** A single request and response with no chat UI, called by another program. Output is a data contract, not prose for a human reader, unless the caller's request explicitly asks for prose.

# Mechanic Adjustments by Regime

| Mechanic | Interactive-synchronous | Autonomous-asynchronous | Programmatic-contractual |
|---|---|---|---|
| Q1-3 follow-up questions | Applies as stated in `working-preferences` | Suppressed; nothing present reads them mid-run | N/A, no prose output |
| Propose-before-generating | Applies as stated | Converted to a logged decision in the handoff note, not a pause | N/A |
| Dialog before large builds | Applies as stated | Front-loaded into the initiating request's parameters; no mid-run dialog is possible | Calibration lives in the request schema itself |
| AUTONOMY dial | Stated baseline, roughly 3 by default | Defaults to 8-10; overridable by an explicit instruction in the initiating request | Caller controls via request parameters |
| RIGOR dial | Stated baseline | Defaults to baseline +1 to +2; overridable by an explicit instruction in the initiating request | Caller-defined |
| Register, anti-slop rules | Applies as stated | Applies to any prose meant for later human review, handoff notes and deliverables | Doesn't apply to the contract itself; applies only if the caller separately requests prose |
| Command vocabulary | Applies as stated | Usable only by a human reviewing after the fact, not during the run | N/A |

# Skill Activation by Regime

Both document skills always load together when producing a technical document. `technical-documents`' own trigger conditions (declared audience, document type, netadmin/DevOps/DevSecOps register) decide preset priority, not which surface the session runs on. `document-standards` is never fully displaced; it supplies the dial mechanism, Content Read step, pre-flight checklist, and generic presets that `technical-documents` extends rather than replaces.

| Regime | Skills active by default | Note |
|---|---|---|
| Interactive-synchronous | `working-preferences`; `document-standards` when producing a standalone document; `technical-documents` alongside it when a technical audience or type is declared or evident | Baseline case |
| Autonomous-asynchronous | `working-preferences` under autonomous-asynchronous mechanics; `document-standards` and `technical-documents` together whenever the deliverable is technical | Decisions logged, not gated |
| Programmatic-contractual | None by default | Register rules don't apply to a bare data contract; they apply to any prose the caller separately requests |

## Capability modifiers within a regime

Regime sets the mechanics. Two capability fields shift the dials further inside a regime, and neither is a reason to change regime.

- **`tool_execution: host` with `workspace: local` or `remote`.** The session is acting on a real tree rather than producing text about one. Dials shift denser and more technical, and the stale-dependency check in `working-preferences` becomes live rather than advisory.
- **`interface: programmatic` with `autonomy: full`.** The domain comes from the calling application's request parameters. Preset priority is still decided by `technical-documents`' own trigger conditions rather than by the caller's declared domain alone.

# Relationship to Other Skills

This skill does not claim authority over `working-preferences`, `document-standards`, or `technical-documents`. It sets which of their stated mechanics are live for the current regime and where a dial starts before that session's task-specific override applies. Those three remain the source of truth for what the mechanics themselves are.

# Multi-Agent Relay Use

Inside the orchestration protocol's relay and handoff templates, an agent reference carries a required `capability` profile and the `regime` derived from it. The `regime` field is stated explicitly on the wire so a receiving agent without this skill loaded still sees it, and it is derived rather than typed freely so it cannot drift from the derivation rule above.

`active_skills` is operator-side configuration. It names whatever behavioral configuration a given agent has loaded, in whatever form its vendor provides. An empty array is valid and expected for a vendor with no skill mechanism, and an empty array is not evidence that an agent is unconfigured.

A receiving agent that has this skill loaded can recompute the regime from the stated `capability` and compare it against the stated `regime`. A mismatch is worth surfacing, not silently trusting either side.

# Failure-Mode Note

AUTONOMY and RIGOR default high under autonomous-asynchronous because a stated baseline of 3 with no human present to answer a confirmation gate produces a stall, not caution, a gate nobody can answer is not a safety mechanism. The default is not forced: an explicit instruction in the initiating request can override it downward (for example, a Routine intentionally run at low autonomy with a human reviewing every logged decision before the next step proceeds). What is not available is the silent case, an unstated baseline of 3 with nobody present to raise it when the gate stalls. Forcing with no override erased legitimate low-autonomy Routine designs; the corrected version keeps the safe default while leaving room for a deliberate, stated choice to run otherwise.
