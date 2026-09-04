---
name: em-dash-gate
enabled: true
event: file
action: block
tool_matcher: Write|Edit|MultiEdit
conditions:
  - field: content
    operator: regex_match
    pattern: \u2014
  - field: file_path
    operator: not_contains
    pattern: em-dash
  - field: file_path
    operator: not_contains
    pattern: banned-words
---

**Blocked: forbidden dash character in generated content.**

Carry this as a standing convention with no exceptions, gated mechanically
rather than by eye. The behavior that motivates a hard gate here: the character
propagates across agent tiers through unconscious style imitation from task
packets, without any agent deliberately choosing it. That is why eyeballing does
not hold and why the check has to be a gate.

**To clear this block**, rewrite the affected sentences. The character is almost
always doing one of four jobs, each with a plain replacement:

- Parenthetical aside, use a comma pair or parentheses
- Appositive or restatement, use a colon
- Abrupt turn or contrast, use a semicolon or split the sentence
- Range, use "to" or an en dash if genuinely numeric

Do not substitute a double hyphen. That reads as an escape from the rule rather
than as prose, and the register tell that accompanies this character is the
actual problem, not the glyph alone.

**Two filename patterns are deliberately exempt**: any file whose name contains
`em-dash`, and the `banned-words` reference. Both have to quote the character in
order to document it. The exemption exists because a gate whose own rule file
trips it gets ignored within a week. Add your own exemptions the same way, by
filename rather than by weakening the pattern.
