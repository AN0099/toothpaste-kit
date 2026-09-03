# Handoff Note Template

Fill this out before ending a turn, a session, or handing a thread to a different agent, human or LLM. This is the state-handoff artifact referenced in `protocol.md`.

```
## Handoff: <thread_id>

**From:** <agent_id> (<surface>)
**To:** <agent_id, or "next agent, unspecified"> (<surface, if known>)
**As of:** <timestamp>

### Completed this turn
- <what got done, specific enough that the next agent does not have to re-derive it>

### Next
- <what the next agent should do first, and why it's next>

### Watch out for
- <anything non-obvious: a gotcha, an assumption made, a place where the next agent might otherwise repeat work already ruled out>

### How to verify current state
- <a concrete check: a command, a file to read, a test to run>
```

This mirrors the session-handoff pattern already in use elsewhere in this project: good handoff notes name what was completed, what's next with enough specificity to act on, and how to verify current state. This version generalizes it to apply between any two agents in this system, not only between two sessions of the same tool.
