# Project State

Current status of toothpaste-kit. For what the project is and how to use it, start with
`README.md`.

Last updated 2026-09-05.

## Live

Eleven skills in two classes.

Seven govern agent behavior and are in daily use: `working-preferences`, `document-standards`,
`technical-documents`, `surface-regimes`, `skill-creation`, `skill-discovery`, `commands`.

Four are human-invoked procedures: `redaction-gate` and `session-close`, added 2026-09-03, and
`daily-dashboard` and `session-log`, added 2026-09-05. All four set `disable-model-invocation`, which is the point in
each case. A gate a model can invoke to satisfy itself is not a gate, and an agent should not decide
on its own that a session is over or that a working day has started.

`hooks/` carries seven `hookify` rule examples, inert where they sit. `scripts/` carries
`link-skills.sh` and `reflow-md.py`, the latter with a fixture and `--selftest`. `link-skills.sh`
writes relative symlink targets where `ln -r` exists, so the links survive the tree being moved.

The orchestration protocol has run relay traffic across Claude, local models, and several vendor
surfaces. The message schema was inverted on 2026-09-05 so that a seven-field capability profile is
required and normative and a product name is a label resolved through `orchestration/registry/`.
Existing relay traffic stays wire-valid, since the eight Anthropic surface strings are unchanged and
became the seed entries of `registry/anthropic.json`. Build against `capability` rather than against
`surface`.

## In progress

Two skill families are specced and not yet built:

- **reference-architecture**: governs how specific a technical document can be before it stops
  being safe to publish.
- **content-pipeline**: note-mining, public-writing register, and publishing workflow.

## Recent changes

- The orchestration event schema now requires a `capability` profile and the `regime` derived from
  it, and treats `surface` as an optional namespaced string resolved against a new `registry/`
  directory. Human agents carry `kind` and a `role` of `relay` or `participant`, which retires the
  two human members of the old surface enum and with them the meaningless combination `kind: llm`
  with `surface: human-relay`. Every registry entry carries `confidence`, `verified_on`, and
  `sources`, so a capability claim about a product that ships weekly has its own expiry date.
  `anthropic.json` holds eight surfaces; `openai.json`, `google.json`, and `local.json` are empty and
  are the intended first-contribution surface. Reasoning in `orchestration/CHANGELOG.md`.
- `surface-regimes` went to v3, deriving regime from the capability profile and re-keying its
  activation table from seven product-name rows to three regime rows. No activation decision changed
  for any of the seven original rows. The Failure-Mode Note carried forward verbatim.
- `orchestration/ingestion/` lost a duplicate. `VENDOR-AGNOSTIC-DIGEST-SPEC-UPGRADE.md` was a strict
  superset of its base file and was folded into it, which also picked up a typo fix and a run-on
  that had swallowed a heading.
- Five repository documents are drafted and **uncommitted**: `SECURITY.md`, `CODE_OF_CONDUCT.md`,
  `CITATION.cff`, `.github/ISSUE_TEMPLATE/` (four files), and a `README.md` Contributing section.
  The code of conduct carries a deliberate placeholder for its reporting contact. See
  `.agents/claude/threads-flagged.md`.

- `redaction-gate` went to v2.1, carrying a fix and a feature. The fix restores a Step 4 rule that
  was present in the maintainer's working copy and described in the CHANGELOG while being absent
  from the published skill: a redaction is proposed only where the content is unnecessary, and a
  load-bearing finding halts and warns instead. It was dropped by the pass that generalized the
  skill for publication, alongside a dated internal statistic that was correctly removed. Anyone
  running the published skill before v2.1 had a gate weaker than its own documentation. The feature
  is a Step 3 derived-values check: a corpus pass matches strings, so it cannot see a value computed
  from restricted content rather than copied out of it, and the check is syntactic rather than an
  index of known digests, since building that index would assemble the thing it exists to control.
- The two procedure skills are no longer maintained as separate local copies. `session-close` and
  `redaction-gate` were real directories in the maintainer's skills folder, diverging from the
  published versions; both are now symlinks like the other seven, so this repo is the single source
  for all nine. The `redaction-gate` defect above was found by diffing those copies while retiring
  them, which is the only reason it surfaced.
- `session-close` now names `CLAUDE.md` as the place a tree should say where its standing-files list
  lives. The generic instruction told the reader to substitute their own list and never said where
  the list should be recorded, which left the pointer nowhere once the tree-specific copy was gone.

- Published. The repository was deleted and recreated to clear AI attribution trailers from three
  commits, since force-pushed commits stay reachable on GitHub by SHA. Three enforcement layers are
  built: `.claude/settings.json` suppressing the trailers at source, an opt-in `commit-msg` hook,
  and a `commit-attribution` workflow. The first two are bypassable by anyone who has not opted in.
  The third binds only while it is set as a required status check in a ruleset on the default
  branch. Whether that ruleset is configured on this repository is unverified as of 2026-09-04.
  See `CONTRIBUTING.md`.
- `docs/standing-documents.md` added, describing the document set `redaction-gate` and
  `session-close` assume. Structure and mechanics are shared; contents are not.
- `README.md`'s framing section rewritten around determinism rather than around fusion being
  impossible, and the accessibility consequence stated as fitment rather than accommodation.

- A full-repo audit found six inaccuracies and fixed them. The largest: `commands` routed to
  sixteen per-command files that never existed in any commit. `README.md` still pointed at the
  pre-reorganization schema paths. `skill-discovery` counted the family as six skills.
- `document-standards` went to v2. Two instructions in it could not be followed as written, and a
  third case, a request too underspecified to generate against, had no rule at all. Found by
  running the skill against live document tasks. See that skill's `CHANGELOG.md`.
- The `lib-*` reference-library toolchain moved out of this repo. It served the maintainer's
  personal knowledge base rather than the kit, and now lives alongside that.
- `README.md`, `CONTRIBUTING.md`, and `philosophy.md` were rewritten. The old versions carried
  operational detail that belonged elsewhere and pointed at files this repo does not contain.

## Known gaps

- No test suite in this repo. An eval harness covering `document-standards` exists in the
  maintainer's own tree and is not ready to ship here. Skills are otherwise validated by use and
  review. A six-gate CI workflow is specced and verified against the tree but not installed; it
  would close the more embarrassing half of this gap, which is that `CONTRIBUTING.md` documents two
  mechanical checks and nothing enforces either. See
  `.agents/claude/context/design-note-ci-gates.md`.
- No drift detection for this repo's own documents. A checker exists in the maintainer's tree that
  records a source path and a content hash next to a claim and rehashes on demand, reporting whether
  a claim's source is current, moved, changed, or gone. It is deterministic, costs no tokens, and is
  not ready to ship here. The full-repo audit that found six inaccuracies below is the kind of pass
  it is meant to make unnecessary.
- No versioning scheme across the skill set. Individual skills carry their own `CHANGELOG.md`. This
  now blocks two other things: an OpenSSF Best Practices Badge, which requires unique version
  numbering and per-release notes, and a Zenodo DOI, which needs a tagged release. `CITATION.cff`
  ships with `version` and `date-released` commented out for the same reason.
- Skill interfaces still change without deprecation notice.

## Open questions

- Whether `orchestration/registry/` stays JSON or moves to YAML. It was authored as JSON for
  consistency with `schemas/`, without weighing that against the declarative-configuration
  conventions the target audience works in. Needs dev-2.
- Which entity holds the copyright. The committed `LICENSE` names Bridle Works and the working tree
  names an individual; the change predates the 2026-09-05 session.

- Whether `commands` should split, since the seventeen-command vocabulary has grown informal
  extensions that were never audited against the original set.
- Whether skills should declare version compatibility with each other, given how often they
  cross-reference by name.
- Whether the two closing-section names `skill-creation` permits are too narrow. `surface-regimes`
  closes with `# Failure-Mode Note` and `technical-documents` with `# Templates`. Both are more
  informative than the generic names the checklist allows, which suggests the rule needs widening
  rather than those two files needing renaming.
