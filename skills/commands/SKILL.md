---
name: commands
description: Gateway and index for the project command vocabulary. Lists all seventeen commands with one-line summaries and resolves HELP and MAN directly. Does not hold the behavioral rules themselves; those live in working-preferences, which is the source of truth for what each command does.
---
# Scope
Discoverability index for the seventeen commands in the project command vocabulary. This skill exists so an agent can find out which commands are active without loading all of `working-preferences`. HELP and MAN resolve here. Every other command executes under the definitions `working-preferences` holds.
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
# Resolution
HELP outputs the Command Index above. That index is the complete list of active commands, which is what HELP asks for.
MAN [command] outputs the index entry for the named command. For FREEZE, FLAG, and RETRACT, read `working-preferences`' `# Session-State Semantics` section first and include what it says. Those three change what the session treats as ground truth, and the one-line index entry understates that.
Commands do not have dedicated files. Depth on any command belongs in `working-preferences` alongside the rest of its definition, so that a reader who has the vocabulary also has the rules that govern it.
# Scope Pointer
- `working-preferences`: source of truth for the command vocabulary, session-state semantics, and standing behavior rules. Anything this index summarizes is defined there in full.
- `skill-creation`: structure and checklists for adding a skill.
- `skill-discovery`: whether a recurring need justifies a new skill.
