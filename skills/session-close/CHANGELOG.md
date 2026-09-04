# CHANGELOG

## v1 (initial)

End-of-session capture. Sweeps a session for reasoning, decisions, near misses,
and corrections that exist nowhere on disk, then updates the documents that must
stay current.

The problem it solves is that anything living only in a session is gone when the
session ends, including a completion claim resting on a skill mount that does not
survive it. This existed as a prompt a human had to remember to type. The skill is
now the trigger.

Two things are deliberate.

**Phase 1 is not skippable on the grounds that nothing comes to mind.** The
prompt that motivated the skill found six unrecorded items on a session where the
honest first answer was "nothing." Categories are asked separately for that
reason.

**Phase 4 forbids self-certification.** The procedure reports what was recorded
and what was checked and stops there. A completion claim is not a fact until
someone other than the claimant checks it, and an agent auditing its own session
is the claimant.

`disable-model-invocation` is set so the human decides when a session ends,
rather than an agent deciding it has finished.
