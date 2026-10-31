# Prompts catalog

This kit's reusable prompts are its skills. Each entry below names a skill directory under
`skills/`, links to its `SKILL.md`, and gives the `description` field from that file's
frontmatter, copied without change. The commands are listed with their brevity codes in the
`commands` skill, which the entry for it links to.

## commands

[`skills/commands/SKILL.md`](../../skills/commands/SKILL.md)

Index of the twenty-seven project commands with brevity codes and one-line summaries; resolves HELP and MAN. Does not hold the behavioral rules; working-preferences is the source of truth for each command.

## daily-dashboard

[`skills/daily-dashboard/SKILL.md`](../../skills/daily-dashboard/SKILL.md)

Open a working day; verify carry-over against the trees, then show project state, ranked todos, roadmap and pending decisions. Mirror of session-close, which writes what this reads; does not capture residue or start the work.

## daily-review

[`skills/daily-review/SKILL.md`](../../skills/daily-review/SKILL.md)

Daily pass over the task board; empty the Inbox, check priorities, carry Doing forward, offer Verify for close, order Next and pick the Most Important Task. The person decides every move. Does not replace daily-dashboard, the state view.

## document-standards

[`skills/document-standards/SKILL.md`](../../skills/document-standards/SKILL.md)

Writing and quality standards for any standalone document; dials, Content Read, pre-flight checklist, full anti-slop reference. Not for chat replies (see working-preferences) or technical document-type presets (see technical-documents).

## jot

[`skills/jot/SKILL.md`](../../skills/jot/SKILL.md)

Agent-callable micro-capture at a clean boundary; appends one short marked entry of decisions, corrections and findings to the day's capture file. Costs about one reply. Does not replace or satisfy session-log or session-close.

## merge-proxy

[`skills/merge-proxy/SKILL.md`](../../skills/merge-proxy/SKILL.md)

Session-scoped, invoked by a person only. The agent merges into a trunk and pushes on an internal or absent remote, after stating the full plan and getting explicit approval. Never applies to a public or internet remote, including GitHub.

## monthly-review

[`skills/monthly-review/SKILL.md`](../../skills/monthly-review/SKILL.md)

Monthly pass over the task board; adopt or reject Someday/Maybe items, recheck long-stalled Waiting tasks, choose archive candidates. The person decides every move. Run after that week's weekly-review, which it does not replace.

## orient

[`skills/orient/SKILL.md`](../../skills/orient/SKILL.md)

Re-establish where things stand before acting; run the reorient tool, then check what moved, record-versus-tree drift and broken assumptions. Use after compaction, handoff or return. Not daily-dashboard, which opens a day and ranks work.

## redaction-gate

[`skills/redaction-gate/SKILL.md`](../../skills/redaction-gate/SKILL.md)

Pre-publish redaction pass before content crosses a sensitivity tier outward (vendor API call, Git commit, repomix pack, cross-account handoff). Checks candidate output against the local restricted corpus.

## session-close

[`skills/session-close/SKILL.md`](../../skills/session-close/SKILL.md)

Run the end-of-session capture procedure for this PKD. Sweeps the session for reasoning, decisions, and near misses that exist nowhere on disk, then updates the six files that must stay current. Invoke before ending any working session.

## session-log

[`skills/session-log/SKILL.md`](../../skills/session-log/SKILL.md)

Mid-session capture before compaction or handoff while work is unfinished; one append-only pass of decisions, corrections, questions and findings, no verification or standing-file updates. Does not replace or satisfy session-close.

## skill-creation

[`skills/skill-creation/SKILL.md`](../../skills/skill-creation/SKILL.md)

How to add a skill once the decision is made; naming, section shape, sizing, integration and pre-publish checklists. Not whether a need deserves a skill (see skill-discovery) or prose quality checks (see document-standards).

## skill-discovery

[`skills/skill-discovery/SKILL.md`](../../skills/skill-discovery/SKILL.md)

How a recurring need is judged worth a skill, and how an existing skill is located. Not what a skill does once triggered (its own description) or how to structure a new skill file (see skill-creation).

## surface-regimes

[`skills/surface-regimes/SKILL.md`](../../skills/surface-regimes/SKILL.md)

Detect the session's regime (interactive, autonomous or programmatic) from its capabilities and adjust working-preferences and document rules. Trigger on Cowork, Routine, headless, Agent SDK, raw API, CLI/IDE agents or a regime field.

## technical-documents

[`skills/technical-documents/SKILL.md`](../../skills/technical-documents/SKILL.md)

Document-type presets and vocabulary for technical documents (runbooks, postmortems, ADRs, READMEs, handoffs, SOPs) for network admin and DevOps readers. Extends document-standards; does not redefine its dials, checklist or anti-slop references.

## touch

[`skills/touch/SKILL.md`](../../skills/touch/SKILL.md)

Agent-callable single-fact update to a standing file right after the work it records; one queue status, flag or state line, plus a ledger line. Never moves, resolves, rewrites or runs checks. Does not replace or satisfy session-close.

## weekly-review

[`skills/weekly-review/SKILL.md`](../../skills/weekly-review/SKILL.md)

Weekly pass over the task board; chase Waiting blockers, name carried Doing tasks, read Done against plan, schedule one important non-urgent task. The person decides every move. Run after a daily-review, which it does not replace.

## working-preferences

[`skills/working-preferences/SKILL.md`](../../skills/working-preferences/SKILL.md)

Standing behavioral defaults, register, prohibitions, correction protocol and command vocabulary. Load for sustained interaction, judgment calls or multi-step work. Not for technical document standards (see document-standards).

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
