# Spec: Producing Digests from AI Platform Export Data (Vendor-Agnostic)

Purpose: a repeatable procedure for turning AI platform data-export JSON (conversation, project, memory and reflection exports, from Claude, ChatGPT, Gemini or any other vendor, including ones not yet seen) into dense, accurate, machine-readable digest documents suitable for an agent handoff chain. It documents a method already used in practice, generalized enough to repeat on a new export without re-deriving it from scratch.

The procedure (§2) doesn't change across vendors. What changes is how you locate each abstract concept (§1) inside an unfamiliar JSON shape; Step 0 does that mapping. Claude's export shapes are given in §1 as a worked mapping example.

Without an export, or for a fast first pass before one: [CONVERSATION-EXTRACTION-PACKET.md](CONVERSATION-EXTRACTION-PACKET.md) is a prompt pasted into the conversation itself, which extracts findings on that conversation's own tokens. It is a triage layer, not a substitute: the full export stays the ground truth for anything load-bearing.

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

### Worked mapping example: Claude's four export shapes

Claude's data export is the shape this method was first built on. Each file maps onto the model above as follows; use it as a template for writing the Step 0 mapping for another vendor.

**Project export** (`{project_uuid}.json`), the *container*:
```json
{uuid, name, description, is_private, is_starter_project, prompt_template,
 created_at, updated_at, creator, docs: [{uuid, filename, content}, ...]}
```
`docs` is the project's knowledge base (static reference files, not conversation). Content is plain text/markdown/JSON-as-string. **No conversation content lives here.** Two different projects can carry byte-identical doc content if the human copy-pasted a doc set between projects/accounts: check for this before assuming two projects are independent (string-compare doc content, not just filenames).

**Conversation export** (`conversations.json`), the *threads*:
```json
[{uuid, name, summary, created_at, updated_at, account,
  chat_messages: [{sender, content: [...], attachments: [...], files: [...]}, ...]}, ...]
```
A flat list of conversations, each already linear (no tree to linearize). Per message (*turn*), `sender` is the role field and `content` is a list of typed blocks (*content segments*):
- `text`: prose, human or assistant. **This is almost always the highest-value content.**
- `thinking`: hidden reasoning. Often present as a block with empty/redacted `text` in exports; do not assume it's readable.
- `tool_use` (`{name, input}`): a tool call. `input` can contain full file bodies (`file_text`, long strings) that can dwarf everything else in the export by volume.
- `tool_result` (`{content}`): the return value of a tool call. Same volume risk as `tool_use`.
- `attachment` (on the message, not a content-block type): `{file_name, file_size, extracted_content}`. `extracted_content` can be an entire uploaded document's full text.

`summary` (top-level, per conversation) is a vendor-generated abstractive summary (*derived analytics*), usually several paragraphs, present on most but not all conversations (some very short or oddly-terminated ones have an empty string). **Read every summary before deciding whether to open the full transcript**: for many conversations the summary is sufficient and a full read is wasted effort.

**Memory export** (account-level, filename is an account UUID), the *persistent memory store*:
```json
{conversations_memory: "<markdown-ish prose, account-wide>",
 project_memories: {"<project_uuid>": "<markdown-ish prose, scoped to that project>", ...},
 memory_files: [{path, content, updated_at}, ...],
 account_uuid}
```
`conversations_memory` and each `project_memories` entry are vendor-synthesized narrative summaries (headed sections like "Work context," "Current state," "Key learnings"), not raw fact lists. `memory_files` are structured-memory documents (frontmatter plus `[stated]`-tagged bullets); these are higher-fidelity than the prose summaries and should be preferred where both exist and conflict.

**Reflections export** (also account-level), *derived analytics*:
```json
{account_uuid, reflections: [{period, content: {hero_title, hero_body, stats,
  topics: [...], about_your_time: [...], expanding_your_skills: [...],
  worth_thinking_about: [...]}, created_at, updated_at}, ...], feedback: [...]}
```
Monthly/periodic vendor-generated retrospectives. Low information density per byte but occasionally surfaces a real behavioral pattern (a self-correction habit, a recurring theme) worth one line in a digest. Don't over-invest here; skim once.

---

## 2. Procedure

### Step 0: Schema discovery
Before Step 1 can run, map the export's actual field names onto §1's abstract model. Do this once per vendor/export shape, then reuse the mapping:
1. Load each file, print top-level type/keys/lengths: same as before, format-agnostic.
2. Locate the thread boundary: what field or nesting level separates one conversation from another. Confirm whether threads are flat arrays or trees needing linearization (check for `parent`/`children`/`mapping`-style keys: a strong tree signal).
3. Locate the turn boundary and its role field: what marks a user turn vs. an assistant turn, and what timestamp field is attached.
4. Locate the content-segment discriminator: what field or field-pattern distinguishes prose from tool calls from attachments from hidden reasoning within a turn. This is the field most likely to differ sharply by vendor (some flatten everything into one `content` string per turn (no segment typing at all, in which case tool calls and prose are already merged and Step 4 of the procedure below can't separate them cleanly) note this limitation rather than pretending a clean split exists), others use a typed-block list like Claude's.
5. Locate the container concept, if any, and whether it's a separate export file, a field on each thread, or absent entirely.
6. Locate the persistent-memory equivalent, if any: this is the layer most likely to not exist at all for a given vendor; don't assume it does.
7. Note volume risk: which content-segment type(s) carry the large embedded payloads (full file bodies, full search/tool results) that need condensing in Step 4 of the procedure. This is near-universal (some segment type always carries this risk), but which one varies. It also varies *within* one vendor across different exports of the same account or product: two exports from the same vendor have surfaced different segment-type sets in practice (one carrying only prose turns, another additionally carrying search-result and file-attachment segments); re-run this check per export, don't assume the last export from a given vendor tells you what this one contains.
8. Scan for embedded, human-requested recap turns (a point in a thread where the human asked for an "in excruciating detail" / "summarize so another LLM can pick this up" turn. These are distinct from Step 0's vendor-generated summary field (which is metadata attached outside the thread); this is content *inside* the thread, written by the assistant at the human's request, and when present it is usually the single most efficient extraction path through a large file) read it before deciding whether the surrounding raw turns need a full pass at all.

Write this mapping down explicitly (even just as a short comment block) before proceeding: it's what lets Steps 1–9 below run unchanged regardless of vendor, with every field name treated as a variable resolved by this mapping rather than a fixed name.

### Step 1: Inventory pass
For every uploaded file, load it and print: top-level type, keys, and (for lists) length. Do this before reading any content. Goal: confirm the shape Step 0 mapped, and roughly how big each part is (character/byte counts per section). This takes one `python3 -c` call per file in practice and should always come first: never assume shape from filename or file extension alone.

### Step 2: Scope the actual ask
Determine, explicitly, before extracting anything:
- Which containers/accounts are in scope. A thread export may contain threads belonging to several unrelated containers or none at all (personal one-offs).
- What the digest is *for*: a handoff to another agent instance, a provenance trail, an incident record. This determines what counts as signal. A handoff digest wants current state and open items; a provenance digest wants chronology and origin; an incident record wants the failure narrative verbatim-adjacent.
- What's already known/already documented elsewhere (existing docs, a prior digest). Never re-derive what's already been captured: cross-reference it and spend the token budget on what's missing.

### Step 3: Triage without full reads
For thread exports: print `{id, title, created→updated, turn_count}` for every thread, plus the per-thread summary field where the mapping found one (Claude: `summary`). If no vendor summary exists at all, triage by turn count and a peek at the first turn's prose instead. Use this table to sort threads into: clearly relevant (read fully or deeply), clearly irrelevant (skip, note existence only if the digest is meant to be exhaustive), and ambiguous (peek at the first 1–2 turns' prose to disambiguate; this is cheap and usually resolves it).

For container exports: list the reference files by name and size; read every file if the digest's job is to distill the set (small, bounded), or skim descriptions if the digest's job is narrower.

For memory exports: read the account-scope and relevant container-scope narrative in full: they're short enough that triage doesn't apply. Skim structured memory files by path/description, read the ones matching your scope.

### Step 4: Condense before reading in depth
Conditional on what Step 0.7 found, not a reflexive pass. For any thread you're reading deeply, strip the low-signal-per-byte content **before** loading it into context, don't just read around it:
- Keep prose segments in full.
- Keep tool calls and results as a one-line marker (tool name plus the most identifying argument, e.g. a file path: truncate any string argument over ~150 chars) rather than full payload. The fact that a tool ran, and on what, is usually what matters; the full file body it wrote almost never is.
- Drop attachment extracted text to a marker (`[ATTACHMENT: name, size: content omitted]`) unless the digest's specific job is to recover attachment content.
- Drop hidden-reasoning segments entirely unless you have a specific reason to believe they contain non-redacted reasoning worth reading (check one sample first: if the text is empty across several, they all are).

Write the condensed form to a scratch file per thread. This routinely cuts raw export volume by 5–20x with negligible loss of narrative content, and makes the difference between a corpus you can actually read versus one you can only sample.

An export can turn out to carry no heavy payload at all (pure prose, no tool or attachment segments), in which case condensation has nothing to do and the raw export is already reading-ready; don't spend a step stripping an export that doesn't need it. If the export has no segment typing at all (a flat content string per turn, per Step 0.4), condensing means truncating embedded code blocks/file dumps by pattern (e.g. long fenced blocks) rather than by segment type: the goal is the same, the mechanism adapts. Where Step 0.8 found embedded recap turns, condensation can also mean triaging by those recaps first and only condensing the raw turns a recap doesn't adequately cover.

### Step 5: Targeted extraction on top of condensed transcripts
Once condensed, `grep` for the specific things the digest needs before reading serially start-to-finish: incident/postmortem keywords, proper nouns from the doc set (role names, project names, file names), decision-marker language ("locked," "confirmed," "decided," "reversed"), correction-marker language ("actually," "that's wrong," the human's own name for a standing rule). Read the surrounding context of each hit. This is far more time-efficient than sequential reading for anything over ~50 turns, and in practice is where most of the highest-value narrative material gets found (the actual dialogue behind an incident, a correction, a reversal).

Reserve sequential reading for threads short enough to read whole (under roughly 30 condensed turns) or for the specific stretch right before an export cuts off, since end-of-thread content is disproportionately likely to be unresolved/time-sensitive and won't show up as a keyword hit for anything you already know to look for.

### Step 6: Reconstruct chronology across sources
Requires a usable timestamp field per thread/turn, confirmed in Step 0.3. Once you have candidate material from multiple threads/containers, order it by timestamp, not by source file or upload order. Cross-account or cross-container work is often interleaved (work-account and personal-account sessions running in the same week, sometimes referencing shared state). A chronological spine is usually worth writing out explicitly as its own section: it's cheap to produce once you have timestamps and is often the single most useful piece of orientation for whoever reads the digest next.

### Step 7: Cross-reference, don't restate
Before writing anything into the digest, check whether it's already captured in a doc the reader already has. If it is, cite it by name and move on. If the export shows something that **contradicts or postdates** an existing doc, that is the highest-priority content in the whole digest. Lead with it, flag it explicitly as time-sensitive or unresolved, and do not bury it under routine material.

This check earns its place. In practice the most consequential finding a digest ever produced was a storage-durability claim that the export contradicted, and it surfaced only because new material was read against the standing ground-truth claim in an existing document rather than in isolation.

### Step 8: Write with these priorities, in this order
1. Anything unresolved, time-sensitive, or contradicting existing docs.
2. The actual process/narrative behind standing rules and incidents: not just that a rule exists, but the failure that produced it, in enough detail that the pattern is recognizable if it starts recurring.
3. Current state (roster, task status, decisions): but only the parts not already covered by an existing doc.
4. Provenance/origin material: where something came from, when it's not obvious from current state alone.
5. Low-value-but-complete inventory (e.g., listing every thread even the irrelevant ones by name): last, brief, and only if completeness itself has value for the reader.

For provenance/origin digests specifically: a strong structural resemblance noticed across sources (the same hierarchy, naming pattern, or design reused later for an unrelated purpose) is a high-value observation, but state it as an observed pattern ("this later structure is isomorphic to this earlier one") rather than an asserted causal fact ("this became that") unless a source explicitly says so. The strength of the resemblance doesn't convert it into a confirmed claim, and the digest should let the reader tell the difference.

### Step 9: Format conventions that made these digests usable
- Dense bullets and short paragraphs over prose narrative; tables for anything enumerable (roster, task status, hardware).
- Verbatim quotes used sparingly and only where exact wording carries meaning a paraphrase would lose (a rule's precise scope, a diagnostic phrase the human coined): not as decoration.
- Every non-obvious claim traceable to its source (thread title/id, doc filename) so the reader can go verify if needed, without demanding they open the raw export to do so.
- State uncertainty plainly rather than resolving it with a guess: "this wasn't fully determinable from the export, worth asking directly" is a correct and complete sentence in a digest; a confident wrong reconstruction is not recoverable the same way.
- A closing section that states explicitly what this digest adds beyond documents the reader already has: orients them on why they're reading it, not just what's in it.

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

## 4. Known failure modes to avoid

- **Treating a vendor-generated summary as ground truth without spot-checking.** It's usually accurate but is itself an LLM output; for anything load-bearing in the digest, verify against the condensed transcript rather than citing the summary alone.
- **Reading in upload/file order instead of timestamp order.** Produces digests that read as a list of documents rather than a story, and can invert cause and effect across sources.
- **Over-reading.** Not every thread needs a deep pass. Triage (Step 3) exists specifically to prevent burning the whole effort budget on low-relevance threads before reaching the ones that matter.
- **Silently resolving ambiguity in the source data.** If two records plausibly describe the same event/entity but can't be confirmed identical (e.g., two similarly-named, similarly-timed threads across two accounts), say so in the digest instead of picking one interpretation and presenting it as settled.
- **Letting tool payload volume drive what gets read.** A single large tool call, tool result or attachment can be 90% of a thread's raw size and 0% of its narrative value. Condense first (Step 4); size in the raw export is not a proxy for importance.
- **New for the multi-vendor case:** assuming a schema-discovery mapping made for one vendor's export applies unchanged to another vendor, or to a new version of the same vendor's export format: re-run Step 0 whenever the source shape is new, even if it looks superficially similar to one seen before (this includes re-checking segment-type sets per §2 Step 0.7, since two exports from the same vendor have already been observed to differ).
- Asserting a resemblance between an early source and a later one as confirmed provenance rather than an observed pattern (see §2 Step 8's addition): a strong isomorphism is worth leading with, but only ever as itself, not dressed up as a stated fact from either source.
- Re-summarizing a block of repeated, re-pasted context as if it were new information in a later thread, inflating the apparent size of the delta a session actually contributed.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
