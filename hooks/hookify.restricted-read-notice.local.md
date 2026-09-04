---
name: restricted-read-notice
enabled: true
event: all
action: warn
tool_matcher: Read|Write|Edit|MultiEdit|NotebookEdit
conditions:
  - field: file_path
    operator: regex_match
    pattern: (CLASSIFIED/0[34]-|intake/unsorted|YOUR-SENSITIVE-INVENTORY)
---

**Notice: tier-restricted material is entering session context.**

This is not a block. Reading this material is normal and expected work. The
warning exists because of what becomes true immediately afterward.

**What changed:** anything you write for the rest of this session may now be
derived from Confidential or Restricted content, including summaries, commit
messages, and documents that look entirely innocuous. `CLAUDE.md` states the
pre-publish redaction gate applies even to Public-tier output that was derived
from Confidential or Restricted material.

**Before any of the following, run `/redaction-gate` first:**

- Writing into `projects/toothpaste-kit/` or any other Git working tree
- Any `git add`, `git commit`, or `git push`
- Any repomix pack intended to leave this machine
- Any content handed to a vendor API, including a sub-agent on another account

**Content-depth reminder** from `CLASSIFIED/OPSEC.md`: Confidential carries
operational behavior with entities abstracted into categories. Only Restricted
carries actual reasoning and named entities. Moving a fact downward in tier
means stripping the reasoning and the names, not just deleting a paragraph.

Note that the inbound direction of this gate is still an open question in
`agents/claude/lead-handoff.md`, not a resolved rule.
