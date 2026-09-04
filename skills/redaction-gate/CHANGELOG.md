# CHANGELOG

## v2.1

Restored the Step 4 rule on load-bearing content, which was absent from the
published copy while present in the maintainer's live copy and described in this
file as though it shipped. The rule was lost during the pass that generalized the
skill for publication: a dated internal statistic in the same region was
correctly removed, and the rule went with it.

The rule that went missing is the rule against removing load-bearing content, and
its own worked example is a redaction pass over-applying. Adopters between v1 and
v2.1 had a gate weaker than the one it documents. Recorded rather than quietly
corrected, because a silent restore leaves no trace that the published and live
copies can diverge at all.

## v2

Step 3 gained a derived-values check. A corpus pass matches strings, so it cannot
see a value computed from restricted content rather than copied from it. The case
that prompted it: a documentation drift checker records a hash of a cited passage
inside the document that cites it, which puts a fingerprint of the cited material
wherever the citing document goes while none of that material's words travel with
it.

The check is syntactic and blocks any citation comment whose source path does not
resolve inside the outbound set. Building it the other way, as an index of known
digests to match against, would assemble a collection of fingerprints of
restricted material in an unprotected file. That is the same trap the run-time
corpus derivation in Step 2 avoids, arriving by a different route.

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
