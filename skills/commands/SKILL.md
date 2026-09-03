---
name: commands
description: Gateway and index for the project command vocabulary. Routes to individual command definitions and handles the HELP command directly.
---
# Scope
This skill provides a discoverability index for the seventeen commands defined in the project command vocabulary. It lists each command with a one-line summary and directs execution to the appropriate dedicated skill file for the sixteen commands that have them. The HELP command is resolved directly within this skill.
# Command Index
- AUDIT [scope]: targeted diagnostic pass. Report errors, gaps, and unverified claims. Do not fix; await instruction.
- COMPLETE: finalize now with available context, no further checkpointing.
- EXPAND: add depth to the last response without restating it.
- EXPORT: recap of session decisions and open threads, pipe-delimited numbered lines (EVENT_00N | CATEGORY | Detail). Append-only across a session. When marking an old entry CLOSED, preserve its original text verbatim rather than rewriting it.
- FLAG [content]: treat as load-bearing; surface conflicts before overriding later.
- FREEZE [content]: treat as fixed; don't revise without flagging conflict first.
- HELP: list active commands.
- MAN [command]: full definition of one command.
- OVERRIDE: drop an active pushback thread on one point.
- PROCEED: current stage is good, advance without recap.
- RESET: restate current task, active preferences, and current position.
- RETRACT [content]: treat specified content as unsaid going forward.
- RETRY: redo the last response in compliance, no acknowledgment of the miss.
- REVIEW: re-examine a suspected error in a prior response, explain and revise.
- SCOPE: read-only recap of decisions, facts, and progress so far.
- SCORE: straight compliance check of the last response against active rules.
- SOCRATIC: toggle. Stress-test the stated position for internal contradictions and assumptions; no outside counterarguments.
# Routing
Sixteen of the seventeen commands route to their own dedicated file under this directory (for example, commands/AUDIT.md). Those files contain the full behavioral rules, edge cases, and execution logic for their respective commands.
The HELP command does not have a dedicated file. Its function is to list active commands, which is the exact purpose of this gateway skill. When HELP is invoked, this skill command index is the output.
# Cross-References
- working-preferences: The source of truth for the command vocabulary and standing behavior rules.
- skill-creation: Governs how new skills, including the individual command files, are structured and added.
- skill-discovery: Determines whether a recurring need justifies a new skill.
