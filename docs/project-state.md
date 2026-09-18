# Project State

Current status of toothpaste-kit. For what the project is and how to use it, start with
`README.md`.

Last updated 2026-09-18.

## Live

Eleven skills in two classes.

Seven govern agent behavior and are in daily use: `working-preferences`, `document-standards`,
`technical-documents`, `surface-regimes`, `skill-creation`, `skill-discovery`, `commands`.

Four are human-invoked procedures: `redaction-gate`, `session-close`,
`daily-dashboard` and `session-log`. All four set `disable-model-invocation`, which is the point in
each case. A gate a model can invoke to satisfy itself is not a gate, and an agent should not decide
on its own that a session is over or that a working day has started.

`hooks/` carries seven `hookify` rule examples, inert where they sit. `scripts/` carries
`link-skills.sh` and `reflow-md.py`, the latter with a fixture and `--selftest`. `link-skills.sh`
writes relative symlink targets where `ln -r` exists, so the links survive the tree being moved.

The orchestration protocol has run relay traffic across Claude, local models, and several vendor
surfaces. The message schema requires a seven-field capability profile as the normative part, and
treats a product name as a label resolved through `orchestration/registry/`.
Existing relay traffic stays wire-valid, since the eight Anthropic surface strings are unchanged and
became the seed entries of `registry/anthropic.json`. Build against `capability` rather than against
`surface`.

## In progress

Two skill families are specced and not yet built:

- **reference-architecture**: governs how specific a technical document can be before it stops
  being safe to publish.
- **content-pipeline**: note-mining, public-writing register, and publishing workflow.

## Recent changes

- **0.1.0 release preparation.** `docs/releasing.md` added, holding the versioning scheme and a
  signed-tag procedure that separates a GitHub signing key from an authentication key.
  `docs/security-posture.md` added as the authoritative per-row posture record, and it owns the
  section stating what the README's badges claim and what they do not. `GOVERNANCE.md`,
  `.github/dependabot.yml` and the `gates.yml` workflow added. `README.md` gained a badge line and
  an accessibility paragraph directly below it, so a reader meets the evidence before the claims.
- `scripts/mdlint.py` no longer diverges from markdownlint on MD056. It counted raw pipe
  characters, so a correctly escaped GFM cell read as an extra column and following the rule could
  not make a file clean. markdownlint 0.41.1 counts micromark table tokens instead, which was read
  out of its `lib/md056.mjs` rather than recalled. An escaped pipe is now removed before counting,
  with a paired selftest that also proves the rule still fires on a real extra cell. Found by
  second-party review.
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
- `SECURITY.md`, `CODE_OF_CONDUCT.md`, `CITATION.cff`, `.github/ISSUE_TEMPLATE/` (four files) and
  the `README.md` Contributing section are **committed**. The code of conduct's reporting contact
  is a real address.

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
  branch. Whether that ruleset is configured on this repository is unverified.
  `docs/security-posture.md` owns that row. See also `CONTRIBUTING.md`.
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

- No test suite in this repo. An eval harness covering `document-standards` exists and is not
  ready to ship here. Skills are otherwise validated by use and
  review. The CI half of this gap is closed: `gates.yml` is installed and runs seven mechanical
  gates plus a second-party markdown lint, so the checks `CONTRIBUTING.md` documents are now
  enforced rather than merely documented.
- No drift detection for this repo's own documents. A checker exists that records a source path
  and a content hash next to a claim and rehashes on demand, reporting whether
  a claim's source is current, moved, changed, or gone. It is deterministic, costs no tokens, and is
  not ready to ship here. The full-repo audit that found six inaccuracies below is the kind of pass
  it is meant to make unnecessary.
- No release yet, though the scheme for one now exists. `docs/releasing.md` holds it, the
  repo-level `CHANGELOG.md` carries a `0.1.0` section, and `CITATION.cff` carries `version` and
  `date-released`. What is still absent is the tag, and with it the Zenodo DOI and the OpenSSF
  Best Practices Badge, both of which need a release to point at; the `identifiers` block in
  `CITATION.cff` stays commented until Zenodo mints the DOI. **This is still the critical path for
  the security posture work below**, because a repository with no release has no release notes, no
  signed artifact and no version to report a vulnerability against. The one remaining
  prerequisite is branch protection on the default branch, which is a host setting rather than a
  file and so belongs to the maintainer.
- No versioning scheme *across* the skill set. Individual skills still carry their own
  `CHANGELOG.md`, and the repo-level version does not imply a version for any single skill.
- Skill interfaces still change without deprecation notice.

## Security posture, and what is actually in place

**Nothing here is claimed as achieved.** Each row states what exists in the tree today, checked
rather than recalled.

| Expected by a reviewer | In this repository today |
|---|---|
| License | `LICENSE`, present, names the individual copyright holder |
| Security policy | `SECURITY.md`, present. No coordinated-disclosure timeline stated |
| Code of conduct | `CODE_OF_CONDUCT.md`, present, with a real reporting address and no escalation body, stated plainly |
| Contribution guide | `CONTRIBUTING.md`, present. Documents two mechanical checks that nothing enforces |
| Citation metadata | `CITATION.cff`, present, `version` and `date-released` commented out |
| Issue templates | Four under `.github/ISSUE_TEMPLATE/` |
| Governance and roles | **Absent.** No `GOVERNANCE.md`, no stated decision process, one maintainer |
| Automated checks in CI | **Two workflows**, `commit-attribution.yml` and `gates.yml`. The latter runs seven mechanical gates plus a second-party markdown lint |
| Versioning and releases | **Absent.** No tags, no releases, no release notes |
| Dependency management | **Absent.** No `dependabot.yml`. The repository ships no package manifest, which is why |
| Static analysis | **Absent.** The tree is Markdown, shell and one Python script; nothing scans the shell or the Python |
| Signed commits or releases | **Not configured in this repository** |
| Branch protection | Not verifiable from the tree. It is a host setting and belongs in a written record |

**`docs/security-posture.md` is authoritative for this table** and carries an evidence column per
row; `docs/releasing.md` holds the versioning scheme. The shorter table here is kept because it is
the record of what was true when the work started.

The first three absences are the ones a reader will notice, and the ordering above is not a plan.
The plan, once the target tier is fixed, belongs in its own document with one row per criterion and
a pointer to the evidence, because a posture claim without per-criterion evidence is the same
unverifiable clean result this project's own conventions reject.

## Open questions

- Whether `orchestration/registry/` stays JSON or moves to YAML. It was authored as JSON for
  consistency with `schemas/`, without weighing that against the declarative-configuration
  conventions the target audience works in. Needs dev-2.
- **Copyright holder: settled.** Bridle Works is the name of this project and is not a formed
  entity, so it cannot hold a copyright. Copyright rests with the individual authors, currently one
  person, and `LICENSE` names that person. Forming Bridle Works later and moving the copyright to
  it would require a written assignment from every individual holder, which is a formality today
  and a collection problem once outside contributors land.

- Whether `commands` should split, since the twenty-seven-command vocabulary has grown informal
  extensions that were never audited against the original set.
- Whether skills should declare version compatibility with each other, given how often they
  cross-reference by name.
- Whether the two closing-section names `skill-creation` permits are too narrow. `surface-regimes`
  closes with `# Failure-Mode Note` and `technical-documents` with `# Templates`. Both are more
  informative than the generic names the checklist allows, which suggests the rule needs widening
  rather than those two files needing renaming.
