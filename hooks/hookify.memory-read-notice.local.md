---
name: memory-read-notice
enabled: true
event: all
action: warn
tool_matcher: mcp__memory__read_graph|mcp__memory__search_nodes|mcp__memory__open_nodes
conditions:
  - field: reason
    operator: regex_match
    pattern: ^
---

**Notice: this read loads Restricted-tier content into session context.**

The memory store lives inside the restricted tier, at
`CLASSIFIED/04-restricted/memory/`. That placement is what clears it
to persist named entities and decision reasoning: containment inside the tier is
the clearance, so persistence creates no storage violation independent of
egress. The cost of that clearance is that **every memory read is a Restricted
read**, including a search that returns a single node.

This is not a block. Reading memory is the point of having it.

**What is now true:** anything you write for the rest of this session may be
derived from Restricted material. The pre-publish redaction gate applies even to
Public-tier output derived from higher-tier material.

**Run `/redaction-gate` before** writing into any Git working tree, staging or
committing, packing for transport, or handing content to a vendor API or an
agent on another account.

**A search is not a filter.** Retrieving one node does not narrow what is now in
context, because the surrounding graph informs how that node reads. Treat the
whole session as contaminated from this point, not just the returned subset.

Full rules in `system/agent-memory-procedure.md`.
