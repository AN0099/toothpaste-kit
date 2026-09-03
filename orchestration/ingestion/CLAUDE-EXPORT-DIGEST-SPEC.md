# Spec: Producing Digests from Claude Export Data

Purpose: a repeatable procedure for turning Claude data-export JSON (project exports, conversation exports, memory exports, reflection exports) into dense, accurate, machine-readable digest documents suitable for an agent handoff chain. This spec documents a method already used in practice, generalized enough to repeat on a new export without re-deriving it from scratch.

---

## 1. Input inventory: the four Claude export shapes

Before doing anything else, identify which of these you have. They are structurally distinct and require different handling.

### 1.1 Project export (`{project_uuid}.json`)
```
{uuid, name, description, is_private, is_starter_project, prompt_template,
 created_at, updated_at, creator, docs: [{uuid, filename, content}, ...]}
```
`docs` is the project's knowledge base (static reference files, not conversation. Content is plain text/markdown/JSON-as-string. **No conversation content lives here.** Two different projects can carry byte-identical doc content if the human copy-pasted a doc set between projects/accounts) check for this before assuming two projects are independent (string-compare doc content, not just filenames).

### 1.2 Conversation export (`conversations.json`)
```
[{uuid, name, summary, created_at, updated_at, account,
  chat_messages: [{sender, content: [...], attachments: [...], files: [...]}, ...]}, ...]
```
A flat list of conversations, each already linear (no tree/branching to resolve: unlike some other vendors, see §2 of the generic spec). Per message, `content` is a list of typed blocks:
- `text`: the actual prose, human or assistant. **This is almost always the highest-value content.**
- `thinking`: extended-thinking content. Often present as a block with empty/redacted `text` in exports; do not assume it's readable.
- `tool_use` (`{name, input}`. `input` can contain full file bodies (`file_text`, long strings)) these can dwarf everything else in the export by volume.
- `tool_result`: `{content}`, the return value of a tool call. Same volume risk as `tool_use`.
- `attachment` (on the message, not a content-block type): `{file_name, file_size, extracted_content}`. `extracted_content` can be an entire uploaded document's full text.

`summary` (top-level, per conversation) is a vendor-generated abstractive summary of that conversation, usually several paragraphs, present on most but not all conversations (some (very short, or oddly-terminated ones) have an empty string. **Read every summary before deciding whether to open the full transcript**) for many conversations the summary is sufficient and a full read is wasted effort.

### 1.3 Memory export (account-level, filename is an account UUID)
```
{conversations_memory: "<markdown-ish prose, account-wide>",
 project_memories: {"<project_uuid>": "<markdown-ish prose, scoped to that project>", ...},
 memory_files: [{path, content, updated_at}, ...],
 account_uuid}
```
`conversations_memory` and each `project_memories` entry are vendor-synthesized narrative summaries (headed sections like "Work context," "Current state," "Key learnings"), not raw fact lists. `memory_files` are the newer structured-memory-filesystem documents (frontmatter + `[stated]`-tagged bullets, matching the format Claude itself now writes to under the persistent-memory system); these are higher-fidelity than the prose summaries and should be preferred where both exist and conflict.

### 1.4 Reflections export (also account-level)
```
{account_uuid, reflections: [{period, content: {hero_title, hero_body, stats,
  topics: [...], about_your_time: [...], expanding_your_skills: [...],
  worth_thinking_about: [...]}, created_at, updated_at}, ...], feedback: [...]}
```
Monthly/periodic vendor-generated retrospectives. Low information density per byte but occasionally surfaces a real behavioral pattern (a self-correction habit, a recurring theme) worth one line in a digest. Don't over-invest here; skim once.

---

## 2. Procedure

### Step 1. Inventory passFor every uploaded file, load it and print: top-level type, keys, and (for lists) length. Do this before reading any content. Goal: identify which of the four shapes in §1 you're holding, and roughly how big each part is (character/byte counts per section). This took one `python3 -c` call per file in practice and should always come first: never assume shape from filename or file extension alone.

### Step 2: Scope the actual ask
Determine, explicitly, before extracting anything:
- Which project(s)/account(s) are in scope. A conversations.json may contain conversations belonging to several unrelated projects or none at all (personal one-offs).
- What the digest is *for*: a handoff to another agent instance, a provenance trail, an incident record. This determines what counts as signal. A handoff digest wants current state and open items; a provenance digest wants chronology and origin; an incident record wants the failure narrative verbatim-adjacent.
- What's already known/already documented elsewhere (existing docs, a prior digest). Never re-derive what's already been captured: cross-reference it and spend the token budget on what's missing.

### Step 3: Triage without full reads
For conversation exports: print `{uuid, name, created_at→updated_at, message_count}` for every conversation, plus the `summary` field where present. Use this table to sort conversations into: clearly relevant (read fully or deeply), clearly irrelevant (skip, note existence only if the digest is meant to be exhaustive), and ambiguous (peek at the first 1–2 messages' `text` blocks to disambiguate; this is cheap and usually resolves it).

For project exports: list `docs[].filename` and size; read every doc if the digest's job is to distill the doc set (small, bounded), or skim descriptions if the digest's job is narrower.

For memory exports: read `conversations_memory` and the relevant `project_memories` entry in full: they're short enough that triage doesn't apply. Skim `memory_files` paths/descriptions, read the ones matching your scope.

### Step 4: Condense before reading in depth
For any conversation you're reading deeply, strip the low-signal-per-byte content **before** loading it into context, don't just read around it:
- Keep `text` blocks in full.
- Keep `tool_use`/`tool_result` as a one-line marker (tool name + the most identifying argument, e.g. a file path: truncate any string argument over ~150 chars) rather than full payload. The fact that a tool ran, and on what, is usually what matters; the full file body it wrote almost never is.
- Drop `attachment.extracted_content` to a marker (`[ATTACHMENT: name, size: content omitted]`) unless the digest's specific job is to recover attachment content.
- Drop `thinking` blocks entirely unless you have a specific reason to believe they contain non-redacted reasoning worth reading (check one sample first: if `text` is empty across several thinking blocks, they all are).

Write the condensed form to a scratch file per conversation. This routinely cuts raw export volume by 5–20x with negligible loss of narrative content, and makes the difference between a corpus you can actually read versus one you can only sample.

### Step 5: Targeted extraction on top of condensed transcripts
Once condensed, `grep` for the specific things the digest needs before reading serially start-to-finish: incident/postmortem keywords, proper nouns from the doc set (role names, project names, file names), decision-marker language ("locked," "confirmed," "decided," "reversed"), correction-marker language ("actually," "that's wrong," the human's own name for a standing rule). Read the surrounding context of each hit. This is far more time-efficient than sequential reading for anything over ~50 messages, and in practice is where most of the highest-value narrative material gets found (the actual dialogue behind an incident, a correction, a reversal).

Reserve genuinely sequential reading for conversations short enough to read whole (under roughly 30 condensed messages) or for the specific stretch right before an export cuts off, since end-of-thread content is disproportionately likely to be unresolved/time-sensitive and won't show up as a keyword hit for anything you already know to look for.

### Step 6: Reconstruct chronology across sources
Once you have candidate material from multiple conversations/projects, order it by timestamp, not by source file or upload order. Cross-account or cross-project work is often genuinely interleaved (the tpkit case: work-account and personal-account sessions ran in the same week, sometimes referencing shared state). A chronological spine is usually worth writing out explicitly as its own section: it's cheap to produce once you have timestamps and is often the single most useful piece of orientation for whoever reads the digest next.

### Step 7: Cross-reference, don't restate
Before writing anything into the digest, check whether it's already captured in a doc the reader already has. If it is, cite it by name and move on. If the export shows something that **contradicts or postdates** an existing doc, that is the highest-priority content in the whole digest. Lead with it, flag it explicitly as time-sensitive or unresolved, and do not bury it under routine material.

This check earns its place. In practice the most consequential finding a digest ever produced was a storage-durability claim that the export contradicted, and it surfaced only because new material was read against the standing ground-truth claim in an existing document rather than in isolation.

### Step 8: Write with these priorities, in this order
1. Anything unresolved, time-sensitive, or contradicting existing docs.
2. The actual process/narrative behind standing rules and incidents: not just that a rule exists, but the failure that produced it, in enough detail that the pattern is recognizable if it starts recurring.
3. Current state (roster, task status, decisions): but only the parts not already covered by an existing doc.
4. Provenance/origin material: where something came from, when it's not obvious from current state alone.
5. Low-value-but-complete inventory (e.g., listing every conversation even the irrelevant ones by name): last, brief, and only if completeness itself has value for the reader.

### Step 9: Format conventions that made these digests usable
- Dense bullets and short paragraphs over prose narrative; tables for anything enumerable (roster, task status, hardware).
- Verbatim quotes used sparingly and only where exact wording carries meaning a paraphrase would lose (a rule's precise scope, a diagnostic phrase the human coined): not as decoration.
- Every non-obvious claim traceable to its source (conversation name/uuid, doc filename) so the reader can go verify if needed, without demanding they open the raw export to do so.
- State uncertainty plainly rather than resolving it with a guess: "this wasn't fully determinable from the export, worth asking directly" is a correct and complete sentence in a digest; a confident wrong reconstruction is not recoverable the same way.
- A closing section that states explicitly what this digest adds beyond documents the reader already has: orients them on why they're reading it, not just what's in it.

---

## 3. Known failure modes to avoid

- **Treating a vendor-generated `summary` as ground truth without spot-checking.** It's usually accurate but is itself an LLM output; for anything load-bearing in the digest, verify against the condensed transcript rather than citing the summary alone.
- **Reading in upload/file order instead of timestamp order.** Produces digests that read as a list of documents rather than a story, and can invert cause and effect across sources.
- **Over-reading.** Not every conversation needs a deep pass. Triage (Step 3) exists specifically to prevent burning the whole effort budget on low-relevance threads before reaching the ones that matter.
- **Silently resolving ambiguity in the source data.** If two records plausibly describe the same event/entity but can't be confirmed identical (e.g., two similarly-named, similarly-timed conversations across two accounts), say so in the digest instead of picking one interpretation and presenting it as settled.
- **Letting tool payload volume drive what gets read.** A single large `tool_use`/`tool_result`/attachment block can be 90% of a conversation's raw size and 0% of its narrative value. Condense first (Step 4); size in the raw export is not a proxy for importance.
