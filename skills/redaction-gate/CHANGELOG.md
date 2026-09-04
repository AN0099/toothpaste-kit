# CHANGELOG

## v1 (initial)

Pre-publish redaction pass, run before content crosses a sensitivity boundary
outward: a vendor API call, a commit into a Git working tree, a pack intended to
leave the machine, or a handoff to an agent on another account.

Two design choices carry the weight.

**The check corpus is derived at run time from the restricted material itself,
never hardcoded here.** A stored list of sensitive terms would be a sensitive
artifact sitting in an unprotected file, which is the problem the skill exists to
prevent, reintroduced by the skill.

**The gate reports and does not act.** It produces findings and a recommendation,
then hands the decision to a human. `disable-model-invocation` is set for the
same reason: a gate a model can invoke to satisfy itself is not a gate. The cost
is that the gate cannot fire automatically, including on paths where something
egresses without a tool call. That tradeoff is deliberate and is the known
limitation.

Step 4 carries a rule added after the first real run, which over-applied:
**propose a redaction only where the content is unnecessary.** Load-bearing
content is never quietly removed or genericized, however sensitive. Where a
finding is load-bearing the gate halts and warns with what removal would cost.
A redaction that silently breaks the document reports as a clean result while
destroying the thing being published.
