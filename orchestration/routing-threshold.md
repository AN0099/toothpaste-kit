# Routing Threshold: Local vs. Vendor Decision Rule

Status: adopted. Standing convention governing Claude-tier faculty-dispatch decisions.

## Scope

This rule governs a decision one level below the lead's task assignment. The lead's task assignment gives work to the lead, a worker, or the operator only; it does not dispatch to vendor faculties directly. This rule is what a Claude-tier agent applies *after* receiving an assigned task, to decide how to execute it: directly, through a drafting model, through a broader-cluster faculty (chatgpt/gemini/deepseek/perplexity), or through a local model once active. It serves the adopted vendor-agnostic architecture principle by making that choice mechanical rather than case-by-case.

Four gates, checked in order. The first gate that produces a terminal answer ends the check; later gates are not consulted once a hard stop fires.

## Gate 0: Sensitivity

**Question:** Does the task read, generate from, or reference Restricted-tier or unredacted Confidential-tier content?

What lands in those tiers is defined by your own sensitivity framework. Typical members: credentials and tokens, anything naming a private individual, and any internal document set held deliberately outside the public repository.

- **Yes, not yet redacted** → no vendor faculty under any circumstance (qwen/chatgpt/gemini/deepseek/perplexity all excluded, redacted or not is irrelevant at this branch since nothing has been redacted yet). Route to the dispatching Claude-tier agent's own direct work, or a local model once active and once its separate storage-persistence clearance is confirmed. If the task's capability need exceeds what that leaves available, do not force a workaround: flag to the operator for a scoped, separately-redacted extract instead.
- **Yes, already passed the pre-publish redaction gate** (checked against the local Restricted corpus, not assumed) → proceed to Gate 1, but the redacted extract is the entire artifact a vendor faculty ever sees. Original content and file paths do not enter that conversation.
- **No** (Public/Internal, or Confidential with no planned external egress) → proceed to Gate 1 unrestricted.

This gate is the redaction pre-publish gate's enforcement point inside the routing decision itself, not a separate check bolted on after routing.

## Gate 1: Capability requirement

**Question:** Does the task need something no local or Claude-tier-native option currently provides?

Checked in this order; first match wins:

1. **Live or current external data** (prices, news, real-time verification) → Perplexity. Give it a single bounded ask (question, expected artifact, source targets, stop condition), not an open research list, per its operating-mode constraint. Trivial lookups go to the dispatching agent's own web_search instead, to preserve Perplexity's quota for cases where a shallow wrong answer would be costly.
2. **Large-document first-pass distillation or Google-ecosystem integration** → Gemini.
3. **Structured-output/tool-integration transformation** outside the agent's own tool access → ChatGPT.
4. **Tool-call execution or file-write against the live repo** → the Claude-tier agent itself (the lead or a worker), never a faculty. No faculty currently holds tool-call trust: drafting models have no tool-call layer by design (markdown output, moved by human relay). This is a standing exclusion, not a per-task judgment.
5. **None of the above** (pure generation, drafting, or formalization from context already on hand) → proceed to Gate 2.

## Gate 2: Cost/tier assignment

Reached only for pure-generation tasks that cleared Gate 1 without a special capability need.

**Question:** Is a local model active?

- **Inactive (current state):** route to a drafting model when the generation volume is worth the round-trip; route to the agent's own direct generation when it isn't. That size threshold is a separate open question and this rule does not resolve it.
- **Active:** route standard generation to the local model first (no quota cost); a smaller local model only for lightweight structured-output fallback. Reserve the drafting model for cases where local's output has already shown insufficient quality for the task at hand.

Whether a local model is dispatched only through the lead, or by workers directly, is each installation's decision.

## Gate 3: Trust-label assignment

Applies regardless of which gate terminated the routing decision. The dispatching Claude-tier agent personally verifies faculty output before using or forwarding it, never accepting a faculty's self-report as verification, then labels it:

| Faculty | Default label | Verified upgrade path |
|---|---|---|
| Drafting model | Unknown on receipt | Derived-grounded once independently checked against ground truth (file existence, factual claim); Derived-candidate if plausible but unchecked |
| deepseek | Derived-candidate, always | None. Context size does not imply grounding, per its own faculty note. |
| perplexity | Derived-grounded (cites sources) | Any signed or token-bearing URL in the output is a credential-handling flag independent of its trust label; strip before storing, don't just cite around it. |
| chatgpt / gemini | Derived-candidate until checked | Derived-grounded once independently checked |
| Local model (once active) | Same tiering as a drafting model | Locality changes sensitivity/egress eligibility, not trust. Being local earns no automatic trust bump. |
| Verified | Reserved for content the dispatching agent confirmed directly | Never assigned on a faculty's self-report alone |

Output that reaches the lead or the operator inherits the weakest unverified label anywhere in its chain.

## Worked examples

### A task needing live web data
Gate 0: no Restricted or Confidential content, no redaction trip. Gate 1 rule 1: the task needs current prices and availability, which change daily. Bounded ask: one question, the expected artifact, named source pages, and a stop condition.
Gate 3: Derived-grounded by default. Any presigned or token-bearing URL in the response is stripped as a credential before it touches a file, regardless of the citation's trust label.
Route: Perplexity, one bounded ask, Derived-grounded pending the credential-URL check, reviewed before anything irreversible depends on it.

### A task with restricted input
Gate 0: the task reads unredacted Restricted-tier content, a hard stop. No vendor faculty at all, since no redaction pass has happened and this branch does not care whether one is possible. Route to the dispatching Claude-tier agent's own direct work, or to a local model once active and once its separate storage-persistence clearance is confirmed, which is a different question from tier.
Gate 3: no faculty involved, so no trust-inheritance question. The agent's own authorship carries the label it assigns directly.
Route: Claude-tier only.

## Confidence

**Internal consistency: high.** Every terminal branch in every gate names exactly one route, the gates are checked in a fixed order, and no branch can produce two conflicting answers for the same task as described.

**Match to actual practice: untested.** The rule formalizes routing that would otherwise be decided case by case. Treat it as prescriptive, not as a validated model of past practice.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
