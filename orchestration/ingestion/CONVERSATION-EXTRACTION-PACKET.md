# Conversation Extraction Packet (portable, vendor-agnostic)

## How to use this

Paste the fenced block below as the next message in the conversation you want to extract from, on whatever vendor's chat interface still holds that conversation in context. It runs entirely on the tokens of that conversation, not yours. If the model replies with a `continuation_marker` line instead of a `manifest` line, reply `continue` and keep doing that until you get a `manifest` with `"coverage": "full"`.

If it still produces a fenced code block despite rule 7 below (some models default to this reflexively for anything JSON-shaped), tell it directly to repost without fencing, plain inline text, before you trust the length of what you got.

This is deliberately vendor-agnostic and doesn't reference this project's own conventions by name, since the extracting model will never have them and different vendors behave differently under the same instructions. The mapping back to this project happens on your end afterward, not inside the prompt:

- `grounding: "quoted"` items are your closest thing to Verified/Derived-grounded once you spot-check the quote against the real export, `paraphrased_only` starts at Derived-candidate, `uncertain` starts at Unknown, same as any other faculty's output.
- Each `item` line becomes a candidate finding when you compile these into a permanent reference doc; FM-style numbering happens at that compilation step, not here, this packet doesn't know about that scheme.
- This is the fast, low-resource first pass. The full JSON export is still the ground truth for anything load-bearing enough to need it, this packet gets you a triage layer over old threads without spending your own tokens re-reading them.

---

## The packet (copy everything in the fenced block)

```
You are extracting everything of value from this conversation's own context into a dense, machine-readable log for external processing. This is a mechanical extraction task, not a summary, critique, or improvement of the conversation. Follow this exactly.

GOAL
Produce one JSON object per line (JSONL, not a single nested blob) for every distinct piece of value in this conversation: decisions or conclusions reached, facts or preferences I stated about myself or my work, artifacts or code produced, threads left open or unresolved, corrections or reversals that happened mid-conversation, and anything you yourself flagged as uncertain at the time. If something doesn't fit those six, use "other" rather than forcing a fit or dropping it.

HARD RULES
1. One distinct item per line. Do not merge multiple separate facts or decisions into one item to save space or finish faster. Completeness matters more than brevity of your response.
2. Every item needs an evidence_quote: a short exact substring copied verbatim from earlier in this conversation, character-for-character, no added ellipses, no paraphrasing inside the quote itself, under ~25 words. If you cannot produce a genuine exact substring, set evidence_quote to null and grounding to "paraphrased_only", do not fabricate a quote to fill the field.
3. Never guess or reconstruct a detail you're not actually finding in the conversation. If you don't know something (a date, a scope, whether something was resolved), say so with null or "unknown", don't fill it in plausibly.
4. If you notice signs this conversation spans a model change, a memory gap, or an internal contradiction (referencing something as settled that was never actually discussed, inconsistent self-description, etc.), emit a context_discontinuity item for it. This is itself valuable information, not a flaw to hide.
5. Do not compress your effort to finish in one reply. If you're running low on room before you've covered the whole conversation, stop at a clean point and emit a continuation_marker line instead of rushing or thinning out the remaining items. You will be told to continue.
6. End every reply (whether you finished or are continuing) with exactly one manifest line.
7. Do not put your output inside a fenced code block. Code blocks on some platforms silently truncate past a size limit, which would corrupt this extraction without either of us knowing. Output the JSONL lines as plain inline text in your reply, one JSON object per line, no fencing around them. If your platform has a persistent document/canvas feature with no such size limit, you may use that instead of a normal chat reply, but never a fenced code block for this specifically.

SCHEMA (one JSON object per line, in this order of appearance)

Optional, once, first line if you can populate any of it:
{"type": "session_metadata", "approximate_topic": string or null, "apparent_date_range": string or null, "model_or_version_mentions": [array of any AI model/version names mentioned in the conversation itself] or [], "notes": string or null}

Repeated, one per distinct item:
{"type": "item", "category": "decision" | "stated_fact_or_preference" | "artifact" | "open_thread" | "correction_or_reversal" | "self_flagged_uncertainty" | "other", "summary": "dense, information-preserving description, machine-readable priority, plain language", "evidence_quote": "exact verbatim substring" or null, "grounding": "quoted" | "paraphrased_only" | "uncertain", "approx_location": "best-effort description of where in the conversation this came from, no fabricated indices", "superseded_by": "short description of what later overrode this, if anything" or null, "tags": [short free-text keywords] or []}

As-needed:
{"type": "context_discontinuity", "description": string, "approx_location": string}

Only if stopping before full coverage:
{"type": "continuation_marker", "status": "incomplete", "last_covered": "description of the last point in the conversation you reached", "reason": string}

Exactly one, last line of every reply:
{"type": "manifest", "items_emitted_this_pass": integer, "coverage": "full" | "partial", "remaining_estimate": string or null, "pass_number": integer}

Begin now. Work through the entire visible conversation history in order. Do not ask me clarifying questions first, if something is ambiguous, extract it as best you can and mark grounding accordingly.
```
