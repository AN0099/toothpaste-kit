# Routing Threshold: Local vs. Vendor Decision Rule

Status: adopted, confirmed by human_gate. Standing convention as of this document, governing Claude-tier faculty-dispatch decisions from here forward.

## Scope

This rule governs a decision one level below the task queue. The task queue assigns work to lead, claude-1, claude-2, or human_gate only (`assignment_rule`); it does not dispatch to vendor faculties directly. This rule is what a Claude-tier agent applies *after* receiving a queue task, to decide how to execute it: directly, through its paired qwen, through a broader-cluster faculty (chatgpt/gemini/deepseek/perplexity), or through local-1a/1b once active. It serves the adopted vendor-agnostic architecture principle by making that choice mechanical rather than case-by-case.

Four gates, checked in order. The first gate that produces a terminal answer ends the check; later gates are not consulted once a hard stop fires.

## Gate 0: Sensitivity

**Question:** Does the task read, generate from, or reference Restricted-tier or unredacted Confidential-tier content?

What lands in those tiers is defined by your own sensitivity framework. Typical members: credentials and tokens, anything naming a private individual, and any internal document set held deliberately outside the public repository.

- **Yes, not yet redacted** → no vendor faculty under any circumstance (qwen/chatgpt/gemini/deepseek/perplexity all excluded, redacted or not is irrelevant at this branch since nothing has been redacted yet). Route to the dispatching Claude-tier agent's own direct work, or local-1a/1b once active and once its separate storage-persistence clearance is confirmed. If the task's capability need exceeds what that leaves available, do not force a workaround: flag to human_gate for a scoped, separately-redacted extract instead.
- **Yes, already passed the pre-publish redaction gate** (checked against the local Restricted corpus, not assumed) → proceed to Gate 1, but the redacted extract is the entire artifact a vendor faculty ever sees. Original content and file paths do not enter that conversation.
- **No** (Public/Internal, or Confidential with no planned external egress) → proceed to Gate 1 unrestricted.

This gate is the redaction pre-publish gate's enforcement point inside the routing decision itself, not a separate check bolted on after routing.

## Gate 1: Capability requirement

**Question:** Does the task need something no local or Claude-tier-native option currently provides?

Checked in this order; first match wins:

1. **Live or current external data** (prices, news, real-time verification) → Perplexity. Give it a single bounded ask (question, expected artifact, source targets, stop condition), not an open research list, per its operating-mode constraint. Trivial lookups go to the dispatching agent's own web_search instead, to preserve Perplexity's quota (Pro 3/day, Research 1/month) for cases where a shallow wrong answer would be costly.
2. **Large-document first-pass distillation or Google-ecosystem integration** → Gemini.
3. **Structured-output/tool-integration transformation** outside the agent's own tool access → ChatGPT.
4. **Tool-call execution or file-write against the live repo** → the Claude-tier agent itself (lead/claude-1/claude-2), never a faculty. No faculty currently holds tool-call trust: qwen-coder was retired specifically over fabricated tool-call claims, and qwen-1/qwen-2 have no tool-call layer by design (markdown output, moved by human relay). This is a standing exclusion, not a per-task judgment.
5. **None of the above** (pure generation, drafting, or formalization from context already on hand) → proceed to Gate 2.

## Gate 2: Cost/tier assignment

Reached only for pure-generation tasks that cleared Gate 1 without a special capability need.

**Question:** Is local-1a/1b active?

- **Inactive (current state):** route to the dispatching agent's paired qwen (qwen-1/qwen-2) when the generation volume is worth the round-trip; route to the agent's own direct generation when it isn't. That size threshold is a separate open question (the flagged scope-creep discussion) and this rule does not resolve it.
- **Active:** route standard generation to local-1a first (no quota cost); local-1b only for lightweight structured-output fallback. Reserve qwen-1/2 for cases where local's output has already shown insufficient quality for the task at hand.

**Open item this gate surfaces:** local-1a/1b appear only under `lead_cluster` in the faculties structure, not under `claude-1_cluster` or `claude-2_cluster`. Until confirmed otherwise, this rule treats local dispatch as lead-mediated only, claude-1/claude-2 route local-eligible work up through lead rather than assuming direct access to it. This needs a human decision, not an assumption baked silently into the rule.

## Gate 3: Trust-label assignment

Applies regardless of which gate terminated the routing decision. The dispatching Claude-tier agent personally verifies faculty output before using or forwarding it (nervous-system rule), then labels it:

| Faculty | Default label | Verified upgrade path |
|---|---|---|
| qwen-L/1/2 | Unknown on receipt | Derived-grounded once independently checked against ground truth (file existence, factual claim); Derived-candidate if plausible but unchecked |
| deepseek | Derived-candidate, always | None. Context size does not imply grounding, per its own faculty note. |
| perplexity | Derived-grounded (cites sources) | Any signed or token-bearing URL in the output is a credential-handling flag independent of its trust label, per the presigned-S3-URL incident; strip before storing, don't just cite around it. |
| chatgpt / gemini | Derived-candidate until checked | Derived-grounded once independently checked |
| local-1a/1b (once active) | Same tiering as qwen | Locality changes sensitivity/egress eligibility, not trust. Being local earns no automatic trust bump. |
| Verified | Reserved for content the dispatching agent confirmed directly | Never assigned on a faculty's self-report alone |

Output that reaches lead or human_gate inherits the weakest unverified label anywhere in its chain, per the trust-labeling paragraph.

## Worked examples

**Formalizing four existing commands into skill files**
Gate 0: public project documentation, no Restricted/Confidential content, pass. Gate 1: no live-data, distillation, structured-transform, or tool-call-specific need beyond the file-write claude-2 already owns, falls through. Gate 2: local-1a/1b inactive, so draft generation routes to qwen-2; the file-write itself stays with claude-2 per Gate 1's standing tool-call exclusion, not delegated to qwen-2 regardless of Gate 2's outcome. Gate 3: qwen-2's draft starts Unknown, becomes Derived-grounded once claude-2 confirms the four files match the already-informal behavior the task describes.
Route: qwen-2 drafts → claude-2 verifies and writes → Derived-grounded.

**Hardware sourcing pass needing current vendor prices and stock**
Gate 0: no Restricted or Confidential content, no redaction trip. Gate 1 rule 1: an explicit need for prices and availability that change daily, across four candidate part families, where stale figures have already caused rework. This is what Perplexity quota exists for. Bounded ask: one in-stock SKU and current price per family, sources limited to named vendor pages, stop condition is all four resolved or explicitly marked unavailable.
Gate 3: Derived-grounded by default. Any presigned or token-bearing URL in the response is stripped as a credential before it touches a file, regardless of the citation's trust label. A cited source can still carry a secret in its query string.
Route: Perplexity, one bounded ask, Derived-grounded pending the credential-URL check, reviewed before anything irreversible depends on it.

**Drafting against a Restricted-tier document set held outside the repository**
Gate 0: the Restricted case by definition, unredacted, hard stop. No vendor faculty at all, since no redaction pass has happened and this branch does not care whether one is possible. Route to the dispatching Claude-tier agent's own direct drafting, or to a local model once active and once the separate storage-persistence question is cleared, which is a different question from tier and is not answered by the model merely running locally.
Gate 3: no faculty involved, so no trust-inheritance question. The agent's own authorship carries the label it assigns directly.
Route: Claude-tier only. Local eligibility is blocked on an unresolved clearance rather than on this rule.

## Confidence

**Internal consistency: high.** Every terminal branch in every gate names exactly one route, the gates are checked in a fixed order, and no branch can produce two conflicting answers for the same task as described.

**Match to actual practice so far: low-to-moderate.** The routing that has actually happened has been described as case-by-case (Perplexity for research, qwen/local-1a for generation, decided per task), which this rule formalizes but does not simply describe. In at least one respect the rule is corrective rather than descriptive: Gate 1's standing tool-call exclusion reflects the qwen-coder retirement, a rule this strict was not in force at the time that incident happened. Treat this draft as prescriptive going forward, not as a validated model of the roster's history.

## Open follow-ups (non-blocking)

Adoption covers the rule as written; these two items were flagged during drafting and remain open, tracked separately rather than assumed:

1. Whether local-1a/1b dispatch is lead-mediated only or open to claude-1/claude-2 directly (Gate 2). Until resolved, this rule's lead-mediated-only reading stands as the operating default.
2. Whether the storage-persistence axis of the OPSEC tier system is cleared for local-1a/1b, which currently blocks any local routing for Restricted-tier content (Gate 0, third example). Until resolved, Restricted-tier work stays Claude-tier-only, local-1a/1b are not eligible for it regardless of activation status.

Resolving either does not require reopening this document, both are implementation facts this rule already knows how to apply once answered.
