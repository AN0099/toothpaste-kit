---
name: commands
description: Gateway and index for the project command vocabulary. Lists all twenty-seven commands with their brevity codes and one-line summaries, and resolves HELP and MAN directly. Does not hold the behavioral rules themselves; those live in working-preferences, which is the source of truth for what each command does.
---
# Scope
Discoverability index for the twenty-seven commands in the project command vocabulary, with the brevity code for each. This skill exists so an agent can find out which commands are active without loading all of `working-preferences`. HELP and MAN resolve here. Every other command executes under the definitions `working-preferences` holds.
# Command Index
Code in parentheses. A code is a code only when it is the entire message, or paired with a question label (`f q1`); see `working-preferences` Questions and Answers.
- ATOMIC (`jd`): toggle. Nothing is applied until every part is done and checked; a failure reverts the whole set.
- AUDIT [scope] (`dl`): targeted diagnostic pass. Report errors, gaps, and unverified claims. Do not fix; await instruction.
- COMPLETE (`fl`): finalize now with available context, no further checkpointing.
- CONFIRM (`f`): yes to the thing proposed. Answers a proposal; PROCEED advances a stage.
- DECLINE (`d`): no to the thing proposed. Rejects that one option without stopping the work.
- DEEPEN [target] (`j`): add depth. With a target, that element only; with none, the whole last response.
- EXPORT (`sfj`): recap of session decisions and open threads, pipe-delimited numbered lines (EVENT_00N | CATEGORY | Detail). Append-only across a session. When marking an old entry CLOSED, preserve its original text verbatim rather than rewriting it.
- FLAG [content] (`k`): treat as load-bearing; surface conflicts before overriding later.
- FREEZE [content] (`sdj`): treat as fixed; don't revise without flagging conflict first.
- HELP (`l`): list active commands.
- MAN [command] (`kd`): full definition of one command.
- MEASURE (`fj`): stop reasoning about it and go count it.
- NUDGE (`sl`): toggle the teaching register.
- OVERRIDE (`dfj`): drop an active pushback thread on one point.
- PARK (`ls`): move it to a register; do not do it now.
- PROCEED (`fk`): current stage is good, advance without recap.
- QUEUE (`kf`): do not run it; log it for a runner.
- RESET (`js`): restate current task, active preferences, and current position.
- RETRACT [content] (`sdk`): treat specified content as unsaid going forward.
- RETRY (`sfk`): redo the last response in compliance, no acknowledgment of the miss.
- REVIEW (`s`): re-examine a suspected error in a prior response, explain and revise.
- SCOPE (`sk`): read-only recap of decisions, facts, and progress so far.
- SCORE (`sj`): straight compliance check of the last response against active rules.
- SOCRATIC (`dfk`): toggle. Stress-test the stated position for internal contradictions and assumptions; no outside counterarguments.
- SOURCE [claim] (`lf`): show the evidence for that specific claim.
- STAGE (`jf`): edit and stage, never commit. The commit-triage case of QUEUE.
- WHY (`dj`): rationale only, without expanding the whole response.
# Resolution
HELP outputs the Command Index above. That index is the complete list of active commands, which is what HELP asks for.
MAN [command] outputs the index entry for the named command. For FREEZE, FLAG, RETRACT and ATOMIC, read `working-preferences`' `# Session-State Semantics` section first and include what it says. Those four change what the session treats as ground truth or how work is applied, and the one-line index entry understates that.
Commands do not have dedicated files. Depth on any command belongs in `working-preferences` alongside the rest of its definition, so that a reader who has the vocabulary also has the rules that govern it.
# Scope Pointer
- `working-preferences`: source of truth for the command vocabulary, the brevity code table, session-state semantics, and standing behavior rules. Anything this index summarizes is defined there in full.
- `skill-creation`: structure and checklists for adding a skill.
- `skill-discovery`: whether a recurring need justifies a new skill.
