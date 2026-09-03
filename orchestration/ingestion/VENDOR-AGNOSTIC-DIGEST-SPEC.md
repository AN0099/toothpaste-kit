# Spec: Producing Digests from AI Platform Export Data (Vendor-Agnostic)

Generalized from `CLAUDE-EXPORT-DIGEST-SPEC.md`. That spec assumes Claude's specific export shapes; this one keeps the same procedure but replaces every Claude-specific schema reference with an abstract data model plus a discovery step, so it holds for ChatGPT, Gemini, or any other vendor's export: including ones not yet seen.

The methodology (§2 in both documents) doesn't change across vendors. What changes is §1: how you locate each abstract concept inside an unfamiliar JSON shape. That mapping step is new in this document and is the actual generalization.

---

## 1. Abstract data model

Every AI chat platform export, regardless of vendor, is some serialization of these concepts. Not every export contains every layer: identify which are present before mapping fields.

**Thread.** A single conversation: an ordered sequence of turns. May be stored as a flat array (Claude) or as a tree of nodes with parent/child pointers where the "current" conversation is one root-to-leaf path (ChatGPT's `mapping` structure): if a tree, you must linearize it first by walking the active path, and note that a tree can contain abandoned branches (regenerated/edited responses) that a flat export discards; decide whether those branches are in scope before ignoring them.

**Turn/message.** One unit of exchange within a thread: a role/sender, a timestamp, and one or more content segments. Roles are typically some variant of user/human vs. assistant/model, sometimes with a distinct system/developer role.

**Content segment.** Within a turn, the actual payload, which is typically one of:
- *Prose*: the visible reply or user input. Always the highest-value segment type.
- *Hidden reasoning*: a chain-of-thought or "thinking" segment, which vendors increasingly redact, truncate, or omit from exports even when the feature was used live. Verify before relying on it.
- *Tool/function call*: a structured invocation with a name and arguments, which can embed arbitrarily large payloads (full file contents, full search results).
- *Tool/function result*: the return value of the above; same volume risk.
- *Attachment*: a user-supplied file, which may appear as a reference (filename only) or with full extracted text inline, depending on vendor and file type.

**Container.** A grouping unit above the level of a single thread: a "project," "workspace," "folder," or "GPT/persona" that bundles multiple threads together and may carry its own static reference material (uploaded knowledge files, custom instructions) independent of any single conversation.

**Persistent memory store.** Vendor-synthesized or user-curated durable facts that persist *across* threads, at either account scope or container scope. May be free-text narrative summaries, structured key-value/frontmatter files, or both at once (newer vendors increasingly do both: a narrative layer plus a structured file layer, with the structured layer being higher-fidelity when they disagree).

**Derived analytics.** Vendor-generated retrospectives or summaries that describe usage patterns rather than content: periodic reflections, per-thread abstractive summaries, usage stats. Not present on every vendor; low density, occasionally worth one line.

---

## 2. Procedure (unchanged in substance from the Claude-specific spec)

### Step 0: Schema discovery (new step, vendor-agnostic addition)
Before Step 1 of the Claude-specific procedure can run, map the export's actual field names onto §1's abstract model. Do this once per vendor/export shape, then reuse the mapping:
1. Load each file, print top-level type/keys/lengths: same as before, format-agnostic.
2. Locate the thread boundary: what field or nesting level separates one conversation from another. Confirm whether threads are flat arrays or trees needing linearization (check for `parent`/`children`/`mapping`-style keys: a strong tree signal).
3. Locate the turn boundary and its role field: what marks a user turn vs. an assistant turn, and what timestamp field is attached.
4. Locate the content-segment discriminator: what field or field-pattern distinguishes prose from tool calls from attachments from hidden reasoning within a turn. This is the field most likely to differ sharply by vendor (some flatten everything into one `content` string per turn (no segment typing at all, in which case tool calls and prose are already merged and Step 4 of the procedure below can't separate them cleanly) note this limitation rather than pretending a clean split exists), others use a typed-block list like Claude's.
5. Locate the container concept, if any, and whether it's a separate export file, a field on each thread, or absent entirely.
6. Locate the persistent-memory equivalent, if any: this is the layer most likely to not exist at all for a given vendor; don't assume it does.
7. Note volume risk: which content-segment type(s) carry the large embedded payloads (full file bodies, full search/tool results) that need condensing in Step 4 of the procedure. This is near-universal , some segment type always carries this risk, but which one varies.

Write this mapping down explicitly (even just as a short comment block) before proceeding: it's what lets Steps 1–9 below run unchanged regardless of vendor.

### Steps 1–9
Identical in substance to the Claude-specific spec's Steps 1–9, with every field name treated as a variable resolved by the Step 0 mapping rather than a fixed name:
1. **Inventory pass**: same, using the mapped fields.
2. **Scope the ask**: vendor-independent; unchanged.
3. **Triage without full reads** (same, using whatever per-thread summary field the mapping found (if any vendor summary exists at all) if not, triage by turn count and a peek at the first turn's prose instead).
4. **Condense before reading in depth** (same principle: keep prose in full, reduce tool-call/tool-result/attachment payloads to one-line markers, drop hidden-reasoning segments unless confirmed non-empty. If the export has no segment typing at all (a flat content string per turn, per §Step 0.4), condensing means truncating embedded code blocks/file dumps by pattern (e.g. long fenced blocks) rather than by segment type) the goal is the same, the mechanism adapts.
5. **Targeted extraction via grep on condensed transcripts**: vendor-independent once condensed.
6. **Reconstruct chronology across sources**: vendor-independent; requires a usable timestamp field per thread/turn, confirmed in Step 0.3.
7. **Cross-reference, don't restate**: vendor-independent.
8. **Write with priority order** (unresolved/contradicting first, process/narrative second, current state third, provenance fourth, inventory last). Vendor-independent.9. **Format conventions**: vendor-independent.

### Step 10: Vendor-specific caveats worth logging in the digest itself
When the digest draws on a non-Claude export, note in the digest's own preamble which schema-discovery decisions were made (e.g., "threads were linearized from a tree export; abandoned/regenerated branches were not included" or "no persistent-memory layer exists for this vendor, so no cross-check against standing memory was possible"); this is the vendor-agnostic equivalent of citing sources, and matters because a reader who knows Claude's export shape will otherwise wrongly assume the same guarantees hold.

---

## 3. Known vendor variations to anticipate

These aren't exhaustive and shouldn't be trusted over Step 0's live discovery on the actual file: treat them as hypotheses to check, not facts to assume.

- **Tree-structured exports.** Some vendors export the full edit/regeneration graph of a conversation rather than one linear thread, with a pointer to which leaf is "current." Linearization is mandatory before the rest of the procedure applies, and the discarded branches are a real (if usually low-value) source of "what was tried and abandoned": the same category of signal Step 8's priority-2 narrative material cares about, so don't discard them reflexively without checking.
- **No segment typing.** Some exports give one prose blob per turn with tool calls and results inlined as markdown/code rather than as distinct structured fields. Condensing (Step 4) has to work by pattern-matching (fenced code blocks, obvious file-dump shapes) instead of by field type.
- **No container concept.** A vendor may have no project/workspace grouping at all, in which case all scoping (Step 2) has to happen by conversation title/date/content rather than by a container ID.
- **No persistent-memory export.** Common for vendors without a standing cross-thread memory feature. Don't manufacture a memory-layer analysis where none exists; state plainly that this layer isn't available for this vendor rather than substituting thread-derived inference for it.
- **Per-turn attachments vs. per-thread attachments.** Some vendors attach uploaded files to the thread as a whole rather than to the specific turn that introduced them: check whether attachment order still lets you place a file at the right point in the narrative, or whether it can only be placed at thread granularity.
- **Timestamp granularity and timezone.** Confirm units (seconds vs. milliseconds vs. ISO string) and timezone before Step 6's chronological reconstruction: silently mixing granularities across vendors when merging multi-vendor exports into one chronology will silently misorder events.

---

## 4. Known failure modes to avoid (same list as the Claude-specific spec, still applies)

- Treating a vendor-generated summary as ground truth without spot-checking.
- Reading in upload/file order instead of timestamp order.
- Over-reading conversations that triage should have deprioritized.
- Silently resolving ambiguity in the source data instead of flagging it.
- Letting tool-payload volume drive what gets read instead of condensing first.
- **New for the multi-vendor case:** assuming a schema-discovery mapping made for one vendor's export applies unchanged to another vendor, or to a new version of the same vendor's export format: re-run Step 0 whenever the source shape is new, even if it looks superficially similar to one seen before.
