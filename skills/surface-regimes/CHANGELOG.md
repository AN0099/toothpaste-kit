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
