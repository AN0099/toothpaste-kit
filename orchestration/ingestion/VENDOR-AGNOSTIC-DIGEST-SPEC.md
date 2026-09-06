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
7. Note volume risk: which content-segment type(s) carry the large embedded payloads (full file bodies, full search/tool results) that need condensing in Step 4 of the procedure. This is near-universal (some segment type always carries this risk), but which one varies. It also varies *within* one vendor across different exports of the same account or product: two exports from the same vendor have surfaced different segment-type sets in practice (one carrying only prose turns, another additionally carrying search-result and file-attachment segments); re-run this check per export, don't assume the last export from a given vendor tells you what this one contains.
8. Scan for embedded, human-requested recap turns (a point in a thread where the human asked for an "in excruciating detail" / "summarize so another LLM can pick this up" turn. These are distinct from Step 0's vendor-generated summary field (which is metadata attached outside the thread); this is content *inside* the thread, written by the assistant at the human's request, and when present it is usually the single most efficient extraction path through a large file) read it before deciding whether the surrounding raw turns need a full pass at all.

Write this mapping down explicitly (even just as a short comment block) before proceeding: it's what lets Steps 1–9 below run unchanged regardless of vendor.

### Steps 1–9
Identical in substance to the Claude-specific spec's Steps 1–9, with every field name treated as a variable resolved by the Step 0 mapping rather than a fixed name:
1. **Inventory pass**: same, using the mapped fields.
2. **Scope the ask**: vendor-independent; unchanged.
3. **Triage without full reads** (same, using whatever per-thread summary field the mapping found (if any vendor summary exists at all) if not, triage by turn count and a peek at the first turn's prose instead).
4. **Condense before reading in depth**: conditional on what Step 0.7 found, not a reflexive pass: same principle where it applies: keep prose in full, reduce tool-call/tool-result/attachment payloads to one-line markers, drop hidden-reasoning segments unless confirmed non-empty, but an export can turn out to carry no heavy payload at all (pure REQUEST/RESPONSE prose, no tool or attachment segments), in which case condensation has nothing to do and the raw export is already reading-ready; don't spend a step stripping an export that doesn't need it. If the export has no segment typing at all (a flat content string per turn, per §Step 0.4), condensing means truncating embedded code blocks/file dumps by pattern (e.g. long fenced blocks) rather than by segment type: the goal is the same, the mechanism adapts. Where Step 0.8 found embedded recap turns, condensation can also mean triaging by those recaps first and only condensing the raw turns a recap doesn't adequately cover.
5. **Targeted extraction via grep on condensed transcripts**: vendor-independent once condensed.
6. **Reconstruct chronology across sources**: vendor-independent; requires a usable timestamp field per thread/turn, confirmed in Step 0.3.
7. **Cross-reference, don't restate**: vendor-independent.
8. **Write with priority order** (unresolved/contradicting first, process/narrative second, current state third, provenance fourth, inventory last) (vendor-independent. One addition for provenance/origin digests specifically: a strong structural resemblance noticed across sources (the same hierarchy, naming pattern, or design reused later for an unrelated purpose) is a genuinely high-value observation, but state it as an observed pattern ("this later structure is isomorphic to this earlier one") rather than an asserted causal fact ("this became that") unless a source explicitly says so) the strength of the resemblance doesn't convert it into a confirmed claim, and the digest should let the reader tell the difference.
9. **Format conventions**: vendor-independent.

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
- **Repeated context re-injection across threads.** Some users re-paste an entire prior thread's output (or a vendor-generated recap of it, per Step 0.8) as the opening turn of a new thread, to carry context forward manually. Recognize the repeated block on sight (it will match near-verbatim) and don't re-extract it a second time as if it were new content in the later thread: treat the later thread's *new* turns, past the repeated block, as the actual delta.
- **Cross-vendor content reuse.** A turn that opens with language like "here's what another model said" or is explicitly labeled as authored for a different product is a real provenance signal, not noise: it means the same content or instruction set is circulating across more than one vendor, which matters for a provenance digest specifically (it tells you the true origin may sit in a different export than the one you're reading) and is worth surfacing rather than silently normalizing away.

---

## 4. Known failure modes to avoid (same list as the Claude-specific spec, still applies)

- Treating a vendor-generated summary as ground truth without spot-checking.
- Reading in upload/file order instead of timestamp order.
- Over-reading conversations that triage should have deprioritized.
- Silently resolving ambiguity in the source data instead of flagging it.
- Letting tool-payload volume drive what gets read instead of condensing first.
- **New for the multi-vendor case:** assuming a schema-discovery mapping made for one vendor's export applies unchanged to another vendor, or to a new version of the same vendor's export format: re-run Step 0 whenever the source shape is new, even if it looks superficially similar to one seen before (this includes re-checking segment-type sets per §2 Step 0.7, since two exports from the same vendor have already been observed to differ).
- Asserting a resemblance between an early source and a later one as confirmed provenance rather than an observed pattern (see §2 Step 8's addition): a strong isomorphism is worth leading with, but only ever as itself, not dressed up as a stated fact from either source.
- Re-summarizing a block of repeated, re-pasted context as if it were new information in a later thread, inflating the apparent size of the delta a session actually contributed.
