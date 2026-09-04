---
name: restricted-egress-guard
enabled: true
event: bash
action: block
tool_matcher: Bash
conditions:
  - field: command
    operator: regex_match
    pattern: (CLASSIFIED|intake/unsorted|YOUR-SENSITIVE-INVENTORY|\.env|id_rsa|id_ed25519|\.pem)
  - field: command
    operator: regex_match
    pattern: (^|[;&|]\s*|\$\(\s*|\n\s*)(curl|wget|scp|rsync|ssh|nc|netcat|gh|repomix|base64|tar|zip|xdg-open|mail|sendmail|git\s+(add|commit|push|remote))\b
---

**Blocked: a command referencing tier-restricted material also carries an egress verb.**

This rule exists because of a near miss in which an existing control was sound
and simply did not cover the surface in use. A packing tool invoked without
scoping reached material that every other layer was designed to exclude. The
lesson generalizes past that one tool: a control that covers one path is not a
control over the class.

**Physical isolation is the primary control.** The `.gitignore` entry is the
backstop, and this hook is a third layer that catches the case where a command
reaches around both.

**If this fired on legitimate work**, the options in order of preference:

1. Operate on a redacted copy staged outside the tier tree, not on the original
2. Narrow the command so it does not name a restricted path at all
3. Split the command, do the read and the transmit as separate steps, so the
   redaction gate has somewhere to sit between them

**If you actually intend to move this content outward**, that is a joint
decision with the human, not a unilateral one. `agents/claude/lead-handoff.md`
is explicit that confirmation authority for anything sensitive is shared. Run
`/redaction-gate`, present the result, and let the human make the call.

**Scope of the match.** The egress verb must appear in command position: at the
start of the command, after a `;`, `|`, or `&&`, inside a substitution, or at
the start of a line. Merely naming one of these tools inside a quoted heredoc or
a comment does not trip the rule, which is what makes it possible to write
documentation about these paths without fighting the gate.

Command-position matching is a deliberate tradeoff and it has limits, as any
pattern-based rule does. Treat this as a third layer behind physical isolation
and the deny-list rather than as a boundary that stands on its own, and size your
confidence accordingly. Report a recurring false positive rather than disabling
the rule.
