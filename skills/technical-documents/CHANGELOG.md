# CHANGELOG

## v1 (split from document-standards)

This skill was split out of `document-standards` so that skill could apply universally to any generated document rather than being scoped to technical writing specifically. The netadmin, DevOps, and DevSecOps audience framing and the technical document-type presets (runbook, ADR, postmortem, on-call handoff, change-management, SOP) moved here unchanged. Everything else, the dial mechanism itself, the Content Read step, the pre-flight checklist, the scoring rubric, and the anti-slop references, stayed in `document-standards` and is inherited rather than duplicated.

## Data-recovery note

This file was never actually written to disk during initial build. Its intended content was trapped inside `SKILL.md` as leaked shell heredoc scaffolding (a `cat > CHANGELOG.md << FILEEOF` block written into the wrong file), silently corrupting `SKILL.md` with CRLF line endings and non-file content past its Templates section. Recovered and separated out during the RCA-remediation pass.

## v2 (RCA remediation, turn-7 postmortem)

Companion entry to `working-preferences` v2 and `document-standards` v3; see `working-preferences/CHANGELOG.md` for the full root-cause statement.

- **Finding 4:** When to Use. Added the mirrored half of the preset-priority rule: this file's presets win over `document-standards`' own presets whenever this file's trigger conditions (audience, document type) are met.
- **Templates:** added `postmortem-remediation.md`, the first populated entry in
  `references/templates/`, generalized from the same remediation audit that produced the findings
  above. This closes a tracked gap: the templates directory had been scaffolded empty, which the
  skill's own guidance warns against.
