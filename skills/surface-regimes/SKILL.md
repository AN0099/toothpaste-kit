---
name: surface-regimes
description: Detects which of three behavioral regimes the current session runs under, interactive-synchronous (chat, Cowork interactive, Code interactive), autonomous-asynchronous (Cowork delegated, Code headless or local Routine, Agent SDK), or programmatic-contractual (raw Messages API, no chat UI), and adjusts working-preferences dials and mechanics, and document-standards/technical-documents applicability, accordingly. Applies to any single session on any Claude surface, not only multi-agent relay threads. Trigger on any mention of Cowork, Routine, headless, Agent SDK, raw API call, or an explicit regime or surface field in a relay or handoff message.
---

# Purpose

`working-preferences` states mechanics (Q1-3, propose-before-generating, dial baselines) as if one register fits every session. It does not, because "a human is present and can respond before the next step" is true in a chat window and false in a Code Routine running unattended. This skill states which mechanics apply, and at what dial setting, based on which of three regimes the current session actually runs under. It does not replace `working-preferences`; it sets the dial before that skill's task-specific override applies.

# Regime Detection

1. If an explicit `regime` or `surface` field is present in context, for example in a relay message or handoff note from the multi-agent orchestration protocol, use that value. Authoritative, skip inference.
2. Otherwise infer from session context: which interface is described in the system prompt or surrounding tooling (Claude.ai chat, Cowork desktop app, Claude Code terminal or IDE, or an API call with no chat UI), whether a human can plausibly respond before the next step executes, whether the output is consumed by a program as a data contract rather than read by a person.
3. If inference is ambiguous, default to interactive-synchronous. This is the safe default: it keeps every confirmation gate and dial baseline active rather than silently assuming no human is present.

# Three Regimes

**Interactive-synchronous.** Chat, Cowork interactive, Code interactive. A human is present for the current exchange and can respond before the next step happens.

**Autonomous-asynchronous.** Cowork delegated, Code headless Routine, Code local Routine, Agent SDK. No human present during execution. Output is reviewed after the fact, if at all.

**Programmatic-contractual.** Raw Messages API, no chat UI, called by another program. Output is a data contract, not prose for a human reader, unless the caller's request explicitly asks for prose.

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

| Surface | Skills active by default | Note |
|---|---|---|
| chat | `working-preferences`, `document-standards` if producing a standalone document, `technical-documents` alongside it if a technical audience/type is declared or evident | Baseline case |
| Cowork interactive | Same skill set as chat, `working-preferences` with AUTONOMY raised toward the interactive baseline shifted by task | Same skills, shifted dials |
| Cowork delegated | `working-preferences` under autonomous-asynchronous mechanics; `document-standards` plus `technical-documents` together whenever the deliverable is technical | Decisions logged, not gated |
| Code interactive | `working-preferences` with dials shifted denser and more technical; `document-standards` and `technical-documents` load together, `technical-documents`' trigger conditions decide preset priority | Not "technical-documents becomes primary over document-standards"; both load |
| Code headless or local Routine | `working-preferences` under autonomous-asynchronous mechanics; `document-standards` and `technical-documents` together under the same priority rule as above | |
| Raw API | None by default | Register rules don't apply to a bare data contract |
| Agent SDK | `working-preferences` under autonomous-asynchronous mechanics; `document-standards` and `technical-documents` together, `technical-documents`' trigger conditions (not the caller's declared domain alone) deciding preset priority | Domain set by the caller's request parameters, but priority is still trigger-condition-based, not surface-based |

# Relationship to Other Skills

This skill does not claim authority over `working-preferences`, `document-standards`, or `technical-documents`. It sets which of their stated mechanics are live for the current regime and where a dial starts before that session's task-specific override applies. Those three remain the source of truth for what the mechanics themselves are.

# Multi-Agent Relay Use

Inside the orchestration protocol's relay and handoff templates, the `regime` and `active_skills` fields on an agent are derived from that agent's `surface` value using the tables above, not set by hand, so they cannot drift from this skill's own definitions. A receiving agent that has this skill loaded can cross-check a stated `active_skills` value against its own inference from `surface`; a mismatch is worth surfacing, not silently trusting either side.

# Failure-Mode Note

AUTONOMY and RIGOR default high under autonomous-asynchronous because a stated baseline of 3 with no human present to answer a confirmation gate produces a stall, not caution, a gate nobody can answer is not a safety mechanism. The default is not forced: an explicit instruction in the initiating request can override it downward (for example, a Routine intentionally run at low autonomy with a human reviewing every logged decision before the next step proceeds). What is not available is the silent case, an unstated baseline of 3 with nobody present to raise it when the gate stalls. Forcing with no override erased legitimate low-autonomy Routine designs; the corrected version keeps the safe default while leaving room for a deliberate, stated choice to run otherwise.
