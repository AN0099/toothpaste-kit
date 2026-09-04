# Changelog

Repo-level log. Records changes to what the kit contains. Design reasoning for an individual
skill lives in that skill's own `CHANGELOG.md`.

## 2026-09-03

### Added

- `skills/redaction-gate/` and `skills/session-close/`, bringing the library to nine. Both set
  `disable-model-invocation`, which makes them a different class from the other seven: procedures a
  person invokes rather than behavior an agent loads on its own. `README.md` now separates the two
  classes rather than listing nine rows under a heading that says the skills govern agent behavior.
- `hooks/`, seven `hookify` rules as examples rather than live configuration. They sit inert where
  they are and must be copied into a `.claude/` directory to do anything. Deliberately not placed in
  this repo's `.claude/`, since several assume a tiered directory scheme this repository does not
  have and would fire as false positives on contributors.
- `scripts/link-skills.sh`, an alternative to the README's `cp -r`. Symlinking means a `git pull`
  updates the installed skills instead of leaving a stale copy. Re-runnable, and it refuses to
  replace a real directory so a hand-edited local skill is never clobbered.
- `.github/workflows/commit-attribution.yml` and `.githooks/commit-msg`, rejecting AI attribution
  trailers in commit messages. `CONTRIBUTING.md` documents all three enforcement layers and is
  explicit that only the required status check binds: a client hook is opt-in per clone and
  `--no-verify` walks past it.
- `.claude/settings.json`, setting `attribution` to empty and disabling the session link, so Claude
  Code adds no trailer to begin with.
- `docs/standing-documents.md`. `redaction-gate` and `session-close` both reference files that are
  not in this repository, and the pointers previously led nowhere for anyone else. This describes
  the structure and how the pieces work, without any of their content: the two-layer split between
  provenance and human-facing documents, the role each standing file plays, and the sensitivity
  tiering the redaction procedure assumes.
- A "Hook rules" section in `CONTRIBUTING.md` covering how to add one: block versus warn, matching
  on command position rather than substrings, giving every rule a stated escape and stated limits,
  and testing against a true positive, a false positive, and the rule's own documentation.
- A "Why this exists" section in `README.md` and an "Operable by more than one kind of person"
  section in `philosophy.md`.

### Changed

- Skill count corrected from seven to nine in `README.md`, `docs/project-state.md`, and
  `skills/skill-discovery/SKILL.md`. The last is the one that mattered: it argues that discovery
  works without a routing file *given the family's current size*, so the number is load-bearing
  rather than decorative.

### Fixed

- `skills/commands/SKILL.md` described a routing mechanism that never existed. It sent readers to
  sixteen per-command files under `skills/commands/`, naming `commands/AUDIT.md` as the example.
  No such file has been in any commit. The section is gone and the skill now names
  `working-preferences` as the source of the definitions, which is where they have always been.
- Added `skills/commands/CHANGELOG.md`. It was the only skill without one, which
  `skills/skill-creation/SKILL.md`'s pre-publish checklist requires.
- Renamed `commands`' closing section from `# Cross-References` to `# Scope Pointer`, one of the
  two names that checklist permits.
- `README.md` pointed at `orchestration/request.json` and `orchestration/response.json` in three
  places. The 2026-09-02 reorganization moved both under `orchestration/schemas/` and was recorded
  as complete, but did not reach this file. Added the `event-base.json` row while correcting them.
- `skills/skill-discovery/SKILL.md` called the family six skills in two places. There are seven.
  The number is load-bearing there, since the gateway-threshold rule in the same file is evaluated
  against it.
- `skills/skill-creation/SKILL.md` cited `working-preferences` as roughly 140 lines against a
  150-line target. It is 149.

### Changed

- `skills/document-standards/SKILL.md` to v2. Removed two internal contradictions that made the
  skill unfollowable as written, and added a `# When Not to Generate Yet` section for the case
  where a request is too underspecified to generate against. All three were found by running the
  skill against live document tasks rather than by reading it. Reasoning is in that skill's own
  `CHANGELOG.md`.

### Removed

- An empty `skills/working-preferences/references/templates/` tree. It held no files, was named
  nowhere in that skill, and was untracked, so it existed on one disk and shipped to no one.

## 2026-09-02

### Changed

- Reorganized `orchestration/` into `schemas/` and `templates/` subdirectories. The documentation
  had described that layout for some time while the files sat flat, so seven references pointed at
  directories that did not exist.
- Rewrote `README.md` and `CONTRIBUTING.md`, and added `philosophy.md`. The previous versions
  pointed at several files this repo does not contain and carried operational detail that belongs
  outside a public repo.
- Rewrote the skill changelogs to be self-contained. Entries previously cited internal planning
  documents that ship with neither the repo nor any release, which left a reader with a citation
  they could not follow. The reasoning those citations carried is now stated inline.
- Generalized the worked examples in `orchestration/ROUTING-THRESHOLD.md`. The gate logic is
  unchanged. The examples no longer describe specific private engagements.
- Corrected `skills/skill-creation/SKILL.md`'s Integration Checklist, which instructed the reader
  to update two repo-level files that do not exist.
- Replaced dead absolute paths from a prior build environment with repo-relative ones.

### Removed

- The `lib-*` reference-library toolchain. It served a personal knowledge base rather than the
  kit, and now lives with that project.
- A root `changelog.md` that was a byte-identical copy of `skills/surface-regimes/CHANGELOG.md`.

### Added

- `LICENSE` (MIT).
- `philosophy.md`.
- This file.
