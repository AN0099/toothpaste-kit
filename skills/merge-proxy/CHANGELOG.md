# CHANGELOG

## v1 (initial)

A session-scoped grant that lets an agent run and push a merge into a trunk on a repository whose
remote is internal or absent, after explaining the exact plan and halting for approval. It exists
for anyone whose hands are the constraint, for any reason: the person decides, the agent types.

Five things are deliberate.

**Only a person can open it.** `disable-model-invocation` is set, so an agent cannot grant itself
the exception. Invoking the skill is the grant, and nothing said in the conversation is.

**External remotes are excluded outright, not gated.** A repository with any remote on GitHub or
another internet host is out of scope whatever else it has, and `scripts/remote-level.sh` defaults
to `external` when it cannot prove a remote internal. A wrong `internal` publishes; a wrong
`external` is a refusal a person overrides in a second.

**Each merge needs its own approval, and the grant never persists.** A grant that outlives
its session becomes a standing loosening nobody decided.

**The explanation checklist is the control.** A short confirmation is safe only when the plan it
confirms was stated completely, so step 3 lists what must be said, and anything left out is not
covered by the approval.

**Trial merges run in sequence.** Each is simulated against the result of the one before, because a
parallel pre-check can report every merge clean while the second one, applied after the first,
conflicts.
