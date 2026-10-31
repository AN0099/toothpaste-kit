# Changelog

Decision log for this orchestration system's own design. One entry per structural choice, with the reasoning, so a later editor does not silently undo a decision made for a reason that isn't obvious from the artifact alone.

**Scope: hybrid, custom protocol layered on real surface constraints.** Rejected a pure custom taxonomy, which would drift from the actual capability differences it needs to route around, and rejected pure documentation-of-product-behavior, too narrow on its own since the goal is a coordination protocol rather than a product comparison. The taxonomy is grounded in searched, current material rather than training-data recall, since product surface behavior changes faster than a model's knowledge cutoff.

**Deliverable shape: multi-file.** Matches the three-tier pattern already established in this project's skills repo. Chosen explicitly over single-file after a pro/con comparison; single-file was the safer default under `document-standards`' own split-threshold rule, but multi-file was chosen deliberately for this system rather than by default.

**Relay mechanism: human-readable header wrapping a JSON payload.** Neither pure JSON, illegible to a human relay without tooling, nor pure prose, not machine-parseable and reintroducing the ambiguity the schema exists to remove, satisfied both the human-relay and LLM-agent audiences at once.

**Taxonomy granularity: sub-roles included where constraints materially differ.** A flat four-surface taxonomy was considered and rejected. `code-interactive` and `code-headless-routine` differ on human presence, machine-on requirement, and audit timing in ways that change what the protocol should assume; collapsing them into one "Code" row would have hidden load-bearing distinctions.

**Human is a typed node (`human-relay` / `human-participant`), not a plain relay.** Added after recognizing that treating the human as an undifferentiated automation layer erases the distinction between transcription and judgment, which is exactly the failure mode, silent edits during relay, most likely to produce undetectable drift in a multi-agent thread.

**Regime and skill-activation mapping promoted out of this project into `skills/surface-regimes/SKILL.md`.** The taxonomy's surface/regime distinction is useful beyond this orchestration protocol; it governs which `working-preferences` mechanics and dial baselines apply in any solo session on any surface, not only in relay threads. Kept a single source of truth (the skill) rather than duplicating the mechanic and activation tables here; `taxonomy.md` carries only the `regime` column as a join key.

**`regime` and `active_skills` added to `agent_ref` in `schemas/event-base.json` and to `templates/relay-message.md`.** Both are derived from `surface` via the skill's lookup tables, not typed freely, so a relay message states its regime and active skills explicitly for any receiving agent that doesn't have `surface-regimes` loaded, while still being checkable against that skill's own definitions when it is.

**Capability inverted above product name; surfaces moved to a registry.** `agent_ref` previously
required `surface`, a closed enum of one vendor's ten product names, and treated `regime` as an
optional field derived from it. That made the portable concept subordinate to the vendor-specific
one, and a session on any other vendor's product could not be expressed as a valid event at all.
The order is now reversed: a seven-field `capability` profile and the `regime` derived from it are
required and normative, and `surface` is an optional namespaced string resolved against
`registry/`. Four of the seven fields are the columns the old capability matrix already had.
The three additions (`interface`, `tool_execution`, `egress`) exist because the routing rule was
already consulting all three informally, `egress` most consequentially: a sensitivity gate that
must know whether content leaves the operator's boundary was reading an operator's memory rather
than a field. The three-clause derivation rule was checked against all eight rows of the existing
matrix and reproduces every one, which is the evidence that the vector is complete rather than
merely plausible.

**Human role split out of the surface enum.** `human-relay` and `human-participant` were members of
the `surface` enum while `kind` separately carried `llm | human`, so `kind: "llm"` with
`surface: "human-relay"` validated and meant nothing. Human agents now carry `kind: "human"` and a
`role` of `relay` or `participant`, and no surface.

**Registry entries carry evidence and an expiry date.** Every descriptor requires `confidence`,
`verified_on`, and `sources`. `taxonomy.md` already did this in prose for one surface, telling the
reader to treat the Cowork audit claim as derived and go check the docs. Requiring the fields turns
a paragraph one author wrote into a property the whole registry has, and makes the registry
sweepable by a staleness checker rather than only readable. `unknown` is a legitimate value for
`audit` and is used where the evidence conflicts.

**`ingestion/CLAUDE-EXPORT-DIGEST-SPEC.md` merged into `ingestion/VENDOR-AGNOSTIC-DIGEST-SPEC.md` (0.6.0).** The vendor-agnostic spec pointed at the Claude spec for its Steps 1 to 9 and failure list, so it could not stand alone. Both now live in one file, with Claude's export shapes kept as a worked mapping example.

**A review round is three records, and the verifier is a different role from the reviewer.** A round's packet, the reviewer's report and the operator's decision are separate files with separate schemas, so each is written by the role that owns it and none can be edited to agree with another after the fact. The reviewer's findings stay unverified in the report; a role other than the reviewer reproduces them in the decision, and the operator cites only reproduced findings. Rejected: one combined record, which lets the reviewer fill in their own verification, and checks within each schema alone, which cannot compare a value across records; those comparisons are in `scripts/round-check.py`.

**Round records allow all four roles of `ROLES.md`, `minion` included.** The TK-081 handoff's `actorModel.vocabulary` lists three roles, `operator`, `lead` and `aide`, and names `ROLES.md` as its source; `ROLES.md` defines four. The round schemas and `scripts/round-check.py` follow the source, so a round that a minion takes part in can be recorded, and a role `ROLES.md` defines is never rejected. The cost is that `minion` can be named as a round's reviewer or verifier, which the handoff's list does not foresee; the independence rule (verifier role differs from reviewer role) applies to it as to any other role.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
