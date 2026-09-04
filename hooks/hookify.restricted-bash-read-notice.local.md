---
name: restricted-bash-read-notice
enabled: true
event: bash
action: warn
tool_matcher: Bash
conditions:
  - field: command
    operator: regex_match
    pattern: (^|[;&|]\s*|\$\(\s*|\n\s*)(cat|head|tail|less|more|sed|awk|grep|rg|jq|wc|cp|mv|open)\b
  - field: command
    operator: regex_match
    pattern: (CLASSIFIED/0[34]-|intake/unsorted|YOUR-SENSITIVE-INVENTORY)
---

**Notice: tier-restricted material is entering session context via a shell command.**

This is the companion to `restricted-read-notice`, which only sees the `Read`
tool. Shell reads are the more common path in practice, and without this rule
the notice would almost never fire in a session that works through `cat`, `sed`,
and `grep`.

Not a block. Reading this material is normal work. What matters is what becomes
true immediately afterward.

**Anything you write for the rest of this session may now be derived from
Confidential or Restricted content**, including summaries, commit messages, and
documents that look entirely innocuous. The pre-publish redaction gate applies
even to Public-tier output derived from higher-tier material.

**Run `/redaction-gate` before** writing into any Git working tree, staging or
committing, packing for transport, or handing content to a vendor API or an
agent on another account.

**Content-depth reminder**: Confidential carries operational behavior with
entities abstracted into categories. Only Restricted carries actual reasoning
and named entities. Moving a fact downward means stripping the reasoning and the
names, not only deleting a paragraph.
