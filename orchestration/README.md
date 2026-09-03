# Agent Orchestration System

## Purpose

A protocol for coordinating work across Claude's four product surfaces (chat, Cowork, Code, API) and human participants, treating both LLM instances and humans as addressable nodes in a single orchestration graph. The human acts as the relay layer between agent instances that cannot otherwise reach each other directly: a chat window has no channel to another chat window, and a human closes that gap by copying output from one and pasting it into another.

## When to use this

Use this system when a task benefits from splitting across surfaces with different capability profiles (for example: planning in chat, autonomous multi-step execution in Cowork or Code, machine-triggered execution via Routines or the API), and no single surface or session can hold the whole task.

Do not use this system for tasks a single session already handles well. The relay overhead (formatting, pasting, tracking thread state) costs more than it saves below a certain task complexity. There is no fixed threshold; apply judgment, the same way `document-standards`' three-tier split only triggers on real usage pressure rather than on a schedule.

## File index

- `taxonomy.md`: agent role definitions across the four surfaces, their sub-roles, and the two human roles (relay vs. participant), plus a capability matrix.
- `protocol.md`: the relay mechanism (human-readable header wrapping a JSON payload), turn-taking rules, and state handoff rules.
- `schemas/`: JSON Schema definitions for events exchanged between agents (`event-base.json`, `request.json`, `response.json`).
- `templates/relay-message.md`: the literal template a human copies, fills, and pastes to move a message from one agent's surface to another.
- `templates/handoff-note.md`: the template for closing out one agent's turn and briefing whichever agent picks up next.
- `ROUTING-THRESHOLD.md`: the rule for deciding whether a task runs locally, on a Claude-tier agent, or through a vendor faculty.
- `ingestion/`: specs for turning vendor data exports into machine-readable digests.
- `CHANGELOG.md`: the decision log for this system's own design choices.

## Quick start

1. Identify the agents in the run and assign each an `agent_id`, `kind` (`llm` or `human`), and `surface` (see `taxonomy.md`).
2. Open one surface per LLM agent: a chat window, a Cowork session, a Code session, or an API-driven process.
3. For each message that needs to cross a surface boundary, the sending agent (or the human, on the LLM's behalf, if the LLM cannot produce the format directly) fills `templates/relay-message.md`.
4. The human, acting as relay, pastes the filled template into the receiving agent's surface. A relay human's job is to move the payload intact, not to edit its content.
5. At the end of a run or a session boundary, whoever is finishing their turn fills `templates/handoff-note.md` so the next agent, human or LLM, can resume without re-deriving context.

## Relationship to the existing skills repo

This system is a peer to `working-preferences`, `document-standards`, and `technical-documents`, not a replacement. Those skills govern how a single Claude instance writes and behaves. This system governs how multiple instances, and humans, coordinate across a task that spans more than one of them.
