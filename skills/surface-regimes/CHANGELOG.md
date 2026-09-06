# Changelog

## v1 (initial generation)

Originated inside the agent-orchestration project (see `orchestration/`) as a taxonomy of surfaces for triggering skills by context. Promoted to a standalone skill rather than left as project documentation, on the stated requirement that it govern solo sessions on any surface, not only multi-agent relay threads.

### Why a forced dial shift instead of a stated baseline under autonomous-asynchronous

A confirmation gate with no human present to answer it doesn't degrade gracefully into caution; it stalls. AUTONOMY and RIGOR were forced rather than merely recommended for that regime because the alternative isn't safer, it's non-functional. Superseded in v2, see below, the forcing was itself the design mistake; the underlying stall problem is real and stays solved by a strong default, not by removing the override.

### Open question, not yet resolved

Whether `working-preferences`' own Scope Pointer section should cross-reference this skill the way it references `document-standards`. Not added unilaterally since it edits a file this skill doesn't own; flagged for the user to decide. Resolved in v2.

## v2 (corrections applied)

**Data-recovery note:** this skill's SKILL.md and this CHANGELOG.md existed only as chat output from a prior session; the files were never actually written to the skills directory. Recovered from the user's own saved copy of that session's output, not re-derived. The corrections below were confirmed by the user in the original session but were never applied to any surviving copy of the file; applied now for the first time, not re-applied.

- **AUTONOMY dial row:** changed from "Forced to 8-10 regardless of stated baseline" to "Defaults to 8-10; overridable by an explicit instruction in the initiating request." The forced version blocked legitimate low-autonomy Routine designs with no escape hatch; user called this a design mistake.
- **RIGOR dial row:** same correction, forced language replaced with default-with-override.
- **Failure-Mode Note:** rewritten to argue for a hard default with an explicit override clause, rather than for the forced version it previously defended.
- **Skill Activation by Regime table:** rebuilt across every row. Previously framed `technical-documents` as replacing `document-standards` on Code, Cowork-delegated, and Agent SDK surfaces. Corrected: both document skills always load together when producing a technical document; `technical-documents`' own trigger conditions (not surface) decide which preset takes priority. User stated the surface-based framing was incorrect.
- **Open question closed:** `working-preferences`' Scope Pointer section now cross-references this skill (see `working-preferences/CHANGELOG.md`).

## v3 (decoupled from vendor product names)

Follows the 2026-09-05 schema inversion in `orchestration/`, which made a seven-field `capability`
profile required and normative on every agent reference and demoted `surface` to a registry label.
This skill was the last document still treating the product name as authoritative.

- **Regime now derives from capability, not from surface.** The Regime Detection section gained the
  three-clause derivation rule and a precedence order: capability profile first, stated regime
  second, surface identifier resolved through the registry third, inference fourth, and the
  interactive-synchronous default last. Where a stated regime and a capability profile disagree,
  capability governs. The old step 1 treated `regime` and `surface` as equally authoritative, which
  was fine while one vendor's enum was the only vocabulary and is wrong now that a surface is a
  label resolved elsewhere.
- **Skill Activation table re-keyed from surface to regime.** It had seven rows named after one
  vendor's products, so a session on any other vendor's surface had no row at all. It now has three
  rows, one per regime. No activation decision changed for any of the seven original rows.
- **Per-surface nuance preserved as capability modifiers.** Re-keying would otherwise have dropped
  two real distinctions the old table carried: that a session acting on a real tree runs denser and
  more technical, and that an SDK caller's declared domain does not by itself decide preset
  priority. Both are now stated as capability conditions (`tool_execution: host`, and
  `interface: programmatic` with `autonomy: full`) rather than as product names.
- **`active_skills` widened.** It was described as looked up from this skill's own activation table,
  which only made sense for a vendor with this skill mechanism. It is now operator-side
  configuration in whatever form a vendor provides, and an empty array is explicitly valid rather
  than a sign of a misconfigured agent.
- **Frontmatter description no longer enumerates one vendor's products** as the definition of each
  regime, and no longer scopes the skill to "any Claude surface." Every trigger term from v2 is
  retained, with a CLI or IDE coding agent from any vendor and an explicit `capability` field added.
- **Failure-Mode Note carried forward verbatim.** It patches an observed failure and is load-bearing
  under the repo-wide convention against paraphrasing such rules for elegance.

Not changed: the Mechanic Adjustments table, which was already keyed on regime and needed nothing.
