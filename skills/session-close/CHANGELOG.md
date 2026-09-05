# CHANGELOG

## v3

Phase 3's dash sweep covered the em dash only, while the convention it enforces
bans an em dash and any punctuation substituting for the same grammatical
function. Measured on the maintainer's tree 2026-09-04: 100 files carried an em
dash and the check found them, 73 carried an en dash and the check reported clean
on every one. The skill that warns about a check looking like coverage contained
one.

The fix is a second command reported as a review prompt rather than a gate.
**Alternative considered and rejected:** widening the pattern to flag en dashes
outside digit pairs. Measured before adopting, and it flagged `Mar 15 - Aug 30`
and `Apr-Jun 2026` across 54 files. Those are ranges. A gate that is mostly false
positives gets ignored inside a week, which is the standing finding from the
register-metric work. Ranges and separators were not mechanically separable here,
so the human reads the hits.

## v2

Phase 1 item 6 gained two named cases, both found by missing them. A file moved between sensitivity tiers leaves stale paths in every document that referenced it, and a description of its contents is content wherever that description sits. A document whose framing was overtaken still reads correctly sentence by sentence while arguing a superseded position.

Also added: a sweep for references by name has to drive its own directory walk. A recursive grep that honors ignore files will skip the tier tree and report clean, which is the failure mode where a check looks like coverage.

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
