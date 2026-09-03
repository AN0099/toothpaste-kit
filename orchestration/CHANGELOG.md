# Changelog

Decision log for this orchestration system's own design. One entry per structural choice, with the reasoning, so a later editor does not silently undo a decision made for a reason that isn't obvious from the artifact alone.

**Scope: hybrid, custom protocol layered on real surface constraints.** Rejected a pure custom taxonomy, which would drift from the actual capability differences it needs to route around, and rejected pure documentation-of-product-behavior, too narrow on its own since the goal is a coordination protocol rather than a product comparison. The taxonomy is grounded in searched, current material rather than training-data recall, since product surface behavior changes faster than a model's knowledge cutoff.

**Deliverable shape: multi-file.** Matches the three-tier pattern already established in this project's skills repo. Chosen explicitly over single-file after a pro/con comparison; single-file was the safer default under `document-standards`' own split-threshold rule, but multi-file was chosen deliberately for this system rather than by default.

**Relay mechanism: human-readable header wrapping a JSON payload.** Neither pure JSON, illegible to a human relay without tooling, nor pure prose, not machine-parseable and reintroducing the ambiguity the schema exists to remove, satisfied both the human-relay and LLM-agent audiences at once.

**Taxonomy granularity: sub-roles included where constraints materially differ.** A flat four-surface taxonomy was considered and rejected. `code-interactive` and `code-headless-routine` differ on human presence, machine-on requirement, and audit timing in ways that change what the protocol should assume; collapsing them into one "Code" row would have hidden load-bearing distinctions.

**Human is a typed node (`human-relay` / `human-participant`), not a plain relay.** Added after recognizing that treating the human as an undifferentiated automation layer erases the distinction between transcription and judgment, which is exactly the failure mode, silent edits during relay, most likely to produce undetectable drift in a multi-agent thread.

**Regime and skill-activation mapping promoted out of this project into `skills/surface-regimes/SKILL.md`.** The taxonomy's surface/regime distinction is useful beyond this orchestration protocol; it governs which `working-preferences` mechanics and dial baselines apply in any solo session on any surface, not only in relay threads. Kept a single source of truth (the skill) rather than duplicating the mechanic and activation tables here; `taxonomy.md` carries only the `regime` column as a join key.

**`regime` and `active_skills` added to `agent_ref` in `schemas/event-base.json` and to `templates/relay-message.md`.** Both are derived from `surface` via the skill's lookup tables, not typed freely, so a relay message states its regime and active skills explicitly for any receiving agent that doesn't have `surface-regimes` loaded, while still being checkable against that skill's own definitions when it is.
