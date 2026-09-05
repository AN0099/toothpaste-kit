# Project State

Current status of toothpaste-kit. For what the project is and how to use it, start with
`README.md`.

Last updated 2026-09-04.

## Live

Nine skills in two classes.

Seven govern agent behavior and are in daily use: `working-preferences`, `document-standards`,
`technical-documents`, `surface-regimes`, `skill-creation`, `skill-discovery`, `commands`.

Two are human-invoked procedures, added 2026-09-03: `redaction-gate` and `session-close`. Both set
`disable-model-invocation`, which is the point in each case. A gate a model can invoke to satisfy
itself is not a gate, and an agent should not decide a session is over.

`hooks/` carries seven `hookify` rule examples, inert where they sit. `scripts/` carries
`link-skills.sh` and `reflow-md.py`, the latter with a fixture and `--selftest`. `link-skills.sh`
writes relative symlink targets where `ln -r` exists, so the links survive the tree being moved.

The orchestration protocol has run relay traffic across Claude, local models, and several vendor
surfaces. Message schemas and the role taxonomy are stable enough to build against.

## In progress

Two skill families are specced and not yet built:

- **reference-architecture**: governs how specific a technical document can be before it stops
  being safe to publish.
- **content-pipeline**: note-mining, public-writing register, and publishing workflow.

## Recent changes

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
  review.
- No drift detection for this repo's own documents. A checker exists in the maintainer's tree that
  records a source path and a content hash next to a claim and rehashes on demand, reporting whether
  a claim's source is current, moved, changed, or gone. It is deterministic, costs no tokens, and is
  not ready to ship here. The full-repo audit that found six inaccuracies below is the kind of pass
  it is meant to make unnecessary.
- No versioning scheme across the skill set. Individual skills carry their own `CHANGELOG.md`.
- Skill interfaces still change without deprecation notice.

## Open questions

- Whether `commands` should split, since the seventeen-command vocabulary has grown informal
  extensions that were never audited against the original set.
- Whether skills should declare version compatibility with each other, given how often they
  cross-reference by name.
- Whether the two closing-section names `skill-creation` permits are too narrow. `surface-regimes`
  closes with `# Failure-Mode Note` and `technical-documents` with `# Templates`. Both are more
  informative than the generic names the checklist allows, which suggests the rule needs widening
  rather than those two files needing renaming.
