# Changelog

Repo-level log. Records changes to what the kit contains. Design reasoning for an individual
skill lives in that skill's own `CHANGELOG.md`.

## Unreleased

### Added

- `.github/workflows/pages.yml`: deploys the kit blog to GitHub Pages at
  <https://kit.bridleworks.org/> on a push to `main` that changes the blog,
  after `blog.py --selftest` passes. The feed's channel link is now that
  address instead of the repository, and each item links to its post's
  page there, which `--selftest` checks with a planted wrong link.
- `scripts/blog.py` and `blog/`: the kit blog. `blog.py build OUT` turns
  `blog/posts/*.md` into static HTML pages, an index and an RSS 2.0
  `feed.xml`; `--selftest` runs the planted cases for both. Three posts, one
  per release from 0.3.0 to 0.5.0. `blog/README.md` indexes the directory and
  [The kit blog](docs/blog.md) is the guide.
- `scripts/cli_path.py`: one function, `under(root, arg)`, that keeps a
  command-line path argument inside a root directory, using `realpath` and a
  `startswith` on the root plus the separator. A path outside, through `..`,
  an absolute path or a symbolic link, exits 2 naming the argument and the
  root. `scripts/spdx-fragment.py` routes `--models` through it, taken from
  the repository root, so a `--models` path outside the repository now exits
  2. `scripts/gates.sh --selftest` runs the helper's selftest against a copy
  with the separator dropped.
- `containers/verify/`: a verification container that
  holds every third-party checker the kit's checks call, so no check is
  skipped and nothing is installed on the host: reuse 6.2.0, the CodeQL 2.27.2
  bundle with its python and actions query packs, yamllint 1.38.0, shellcheck
  0.11.0, actionlint 1.7.12, check-jsonschema 0.38.2 and CUE 0.17.1, each at an
  exact version and each download checked by sha256. `verify TREE CMD...` runs
  a command on a read-only copy of a tree with no network; `codeql TREE` runs
  the python and actions analyses and prints each alert as `file:line rule`.
  `containers/README.md` says how to run each image.
- `containers/starter/`: a container to try the kit without installing its
  dependencies on the host. `run [--network] [DIR [CMD...]]` starts it as the
  calling user, with the kit read-only at `/kit` and DIR read-write at
  `/workspace`, and no network unless `--network` is given. The image holds
  Python, git and Claude Code, each download pinned to its version and
  sha256, on the same base image digest as the verification container.
- `scripts/check-qblock` (pull request #62): checks a reply's closing question
  block against `skills/working-preferences/SKILL.md`, "Questions and
  Answers", with 30 planted cases in `tests/qblock-cases/` run from
  `scripts/gates.sh`.
- `scripts/schema-check.py` (pull request #67): validates every
  `orchestration/registry/*.json` file against its schema; the registry gate
  runs it.
- `scripts/link-skills.sh --dry-run` (pull request #66): prints the plan and
  writes nothing. Every run now prints its plan before writing.
- `scripts/spdx-fragment.py` (pull request #74): renders a commit range's
  `Assisted-by:` and `Agent-Effort:` trailers as one SPDX 3.0.1 JSON-LD
  document, with a CreationInfo, the kit package, one AIPackage per model, one
  Tool per tool version, their Agents and a `usesTool` relationship. Values the
  trailers cannot give come from `scripts/spdx-models.json`, shipped empty. A
  model with no entry still gets its AIPackage, with `ai_autonomyType` set to
  `noAssertion`, the file's other values left out and a warning on stderr; an
  entry missing a required key exits 2. The pull request template now points
  to the script, and `scripts/gates.sh` runs its selftest as gate 17.
- `scripts/sbom.py`: prints an SPDX 3.0.1 JSON-LD bill of materials for the
  tree, with every REUSE-covered file's copyright and licence and every
  workflow action by its pinned ref. It exits 1 on a file with no licence or
  copyright, a licence with no text under `LICENSES/`, or an action not pinned
  by commit SHA, except `actions/checkout@v7`, recorded in
  `docs/security-posture.md` row 3.7. `scripts/gates.sh` runs its selftest
  and then the script on the tree as gate 19.
- `security-insights.yml` (pull request #76): an OpenSSF Security Insights
  file at the kit root, following schema version 2.2.0, that describes the
  kit's security arrangements in a form tools read. `docs/security-posture.md`
  row 2.9 records where each value comes from.

- Review rounds (TK-081): three JSON schemas in `orchestration/schemas/round/`
  for a round's packet, the reviewer's report and the operator's decision;
  `scripts/round-check.py`, which validates a round directory against them and
  checks the invariants that span the records (a reviewer never verifies their
  own finding, the operator cites only reproduced findings, the reviewed
  revision matches the packet's), with `--repo` to check recorded commits and
  `--selftest`; a practice fixture in `examples/review-round/` with reviewer and
  verifier paths, an answer key and schema cases; and `docs/review-rounds.md`
  and `docs/review-rounds-quickstart.md`. `scripts/gates.sh` runs the selftest
  and the schema cases as gate 18.

### Changed

- `scripts/gates.sh` runs `scripts/blog.py --selftest` as gate 20, and
  `--selftest` plants a copy whose bad-character pattern matches nothing,
  which must fail. The blog builder's checks shipped with it but no gate
  ran them.
- `containers/verify/` and `containers/starter/` build for linux/amd64 and
  linux/arm64. Each download that differs by architecture has one pinned
  stage per architecture, chosen by `TARGETARCH`, and `requirements.txt`
  carries an aarch64 wheel hash beside each x86-64 one. A new workflow,
  `.github/workflows/containers.yml`, builds both images on a native runner
  for each architecture and runs the gates selftest inside each, plus
  compliance and a CodeQL scan in the verification image.
- `containers/verify/` moves to the CodeQL 2.27.3 bundle, the version GitHub's
  default setup runs. 2.27.2 missed a `py/xml-bomb` alert that 2.27.3 reports
  on the same tree. The image is now `localhost/kit-verify:v2`, so a host that
  built v1 builds the new one on its next run instead of reusing the old.
- `scripts/compliance.sh`: a check whose tool is not
  installed now fails the script, exit 1, and names the tool; `--allow-missing`
  reports it as not checked instead. `--require` is still accepted. The
  selftest shows both cases, and `scripts/gates.sh --selftest` checks them with
  nothing installed.
- Selftests for nine scripts, from mutation testing: `check-hooks.py`,
  `check-pr-body`, `compliance.sh`, `mdlint.py`, `reflow-md.py`, `reorient`,
  `round-check.py`, `spdx-fragment.py`, and the schema-check plants in
  `gates.sh`. Each new case kills a mutant the old selftest let through.
  `check-hooks.py` now reports a `pattern:` or `operator:` line that comes
  before any `- field:` as a finding, where it used to drop the line.
- `orchestration/ingestion/VENDOR-AGNOSTIC-DIGEST-SPEC.md` (pull request #60):
  one spec, its duplicate sections merged, with
  `CONVERSATION-EXTRACTION-PACKET.md` linked as a fast first pass.
- The branch-name hook (pull request #61) sees `push` behind quoted and
  separate-word global options, and lists the forms it still does not catch.
- The frontmatter gate (pull request #63) checks each skill `description` for
  length, one line, and the plain-scalar YAML rules; 17 descriptions are
  shortened to fit.
- Commits (pull request #68): provenance is recorded as `Assisted-by:` and
  `Agent-Effort:` trailers, every commit needs a `Signed-off-by:` line, and
  `scripts/check-pr-body` checks a pull request body against the template.
- The `pr-body`, `dco` and `commit-attribution` jobs (pull request #72) report
  under those names. All three reported as `check` before, so a required
  `check` was met by whichever ran; each can now be required on its own.

- The pull request template's "Drafted with an agent?" section is one box,
  ticked, or replaced by a "No." line. The unticked Yes or No box had
  counted as an open task, so every merged pull request showed one task
  left. `scripts/check-pr-body` now treats that box like any other.

### Fixed

- `scripts/gates.sh`: changes to the kit root, found from its own path
  rather than from git, before any gate runs. Run from another directory,
  `--selftest` had failed 9 plants with messages about the gates ("rejected
  its own clean fixture", "accepted a planted positive") rather than about the
  directory. The selftest adds a plant for it: two copies of the kit without
  `.git` are run from a third directory, and the one whose `cd` is removed
  must fail while the one as installed passes every gate.
- `README.md` and `docs/installing.md`: the README names the five scripts in
  `scripts/` it had left out, and says `repomix` is a separate tool that the
  counts check depends on. The installing guide creates the skills directory
  before copying into it, and says which hook rules work as shipped and which
  name paths you must edit first.
- `scripts/gates.sh --selftest` (pull request #70): counts its planted
  positives as they run, so the "all N planted positives fired" message can
  no longer drift from the code.
- `scripts/schema-check.py` (pull request #71): refuses any argument with
  exit 2. Before it, a mistyped flag such as `--selftest` ran a normal check
  and exited 0.
- `scripts/round-check.py --selftest`: counts its extra checks as they run, so
  the total reads 134 of 134 and can no longer drift from the code, as 133
  did. The `finding-id-unique` plant now differs from the finding it
  duplicates, and the report's ids are kept as a set, which removes a mutant
  the selftest could not tell apart.

### Skill revisions

- `orient` v4, `session-log` v4, `session-close` v7 (pull request #65): each
  points at the kit's shipped `examples/workspace/CLAUDE.md`, and `orient`
  names `scripts/` and `bin/` where a tree has no justfile.

## 0.5.0 (2026-10-27)

A MINOR release under `docs/releasing.md`. The licence moves to Apache 2.0, with REUSE
compliance and a Developer Certificate of Origin sign-off; the ACMM L2, L3 and L4 files arrive;
`scripts/gates.sh` goes from ten gates to fourteen; and branch and tag names get one rule. No
skill is added and no skill revision is BREAKING.

### Added

- `docs/document-layers.md`, exception 5: a filed reflection entry may be
  reformatted where no word changes (line wrapping or whitespace, or markup
  a new gate requires), and a markup change MUST NOT change what a line
  means; a change to any word needs a superseding entry. The maintainer's
  decision of 2026-10-20, made for ACMM compatibility.
- `docs/risk-tiers.md`, "Per-tool instruction files": every per-tool
  instruction file (`CLAUDE.md`, `.cursor/rules/agents.mdc`,
  `.github/copilot-instructions.md`) points at `AGENTS.md` and adds no rule.
  The maintainer's decision of 2026-10-20, made for ACMM compatibility.
- ACMM L3 measurement (pull request #44): `docs/metrics.md`, the pull request
  acceptance metric; `docs/review-rubric.md`, the review rubric;
  `.github/workflows/ci.yml`, the test matrix on Linux and macOS;
  `docs/quality.md`, the quality dashboard; `.claude/session-summary.md`, the
  session summary artifact. `scripts/reorient` now parses under bash 3.2.
- `docs/acmm.md`: an index of the ACMM levels, naming the file that meets
  each criterion and the pull request that added it.
- REUSE compliance: every file declares its copyright and licence, by an
  SPDX header or, for files that cannot hold one, in `REUSE.toml`; the
  licence text is also in `LICENSES/Apache-2.0.txt`. `scripts/compliance.sh`
  runs `reuse lint` with a planted-file selftest, and
  `.github/workflows/compliance.yml` runs it in CI with a pinned `reuse`.
  `scripts/gates.sh` still needs nothing installed.
- Branch and tag names: `scripts/check-branch-name` is the one definition of
  an allowed name, `<prefix>/<words>` from a fixed prefix list, 40 characters
  at most, and `v<major>.<minor>.<patch>` for tags. `.githooks/pre-push` runs
  it before a push, gate 13 selftests it and checks the ruleset's prefix list
  against it, the `branch-name` job in `gates.yml` checks a pull request's
  branch, and `.github/rulesets/` holds the forge rulesets for the
  maintainer to apply. `hooks/hookify.branch-name-guard.local.md` is the
  example agent rule: push only to an explicit destination, never skip the
  hooks; its cases are in `tests/branch-guard-cases.tsv`, run by the hooks
  gate. CONTRIBUTING.md, "Branch and tag names".
- `orchestration/rounds.md`: the rounds protocol, by which work is checked by
  a seat other than its author before it reaches the maintainer, with report
  and finding numbering and the major, minor and nit severity scale (pull
  request #53).
- `scripts/check-hooks.py`, gate 12: each rule in `hooks/` parses, and each
  blocking rule fires on its planted cases (pull request #51).
- `scripts/auto-qa-tuner.py`, run weekly by `.github/workflows/auto-qa.yml`:
  proposes a timeout for each job in `.github/auto-qa-tuning.json` from its
  last 100 runs, in the job summary, and never edits a workflow (pull
  request #52).
- `.github/workflows/ai-fix.yml`: an issue labelled `ai-fix` gets one fixed
  comment routing it to the maintainers. No agent runs in CI and no stored
  secret is used (pull request #48).
- ACMM L4 part a (pull request #45): `SECURITY-AI.md`, the AI security policy;
  `docs/risk-tiers.md`, change classification; `.github/labeler.yml` and its
  workflow, labelling pull requests by path; `.github/workflows/nightly.yml`,
  the gates selftest every night; and `docs/reflections/`, filed
  cross-session lessons.
- ACMM L2 (pull request #37): `CLAUDE.md`, `.github/copilot-instructions.md`
  and `.cursor/rules/agents.mdc` point at `AGENTS.md`;
  `docs/prompts/README.md` catalogs the skills; `docs/corrections.md` and an
  empty `corrections.jsonl` give the Correction Protocol's records a format.
- Contributor files (pull request #30): `AGENTS.md`, a pull request template,
  `.editorconfig`, and `tests/run` with `tests/README.md` as the test entry
  point. `scripts/link-skills.sh --selftest`, gate 11.
- `docs/glossary.md`, each term of art with the file that defines it (pull
  request #29), and `docs/concepts.md`, a concepts index (pull request #43).

### Changed

- `.githooks/commit-msg` also refuses `Assisted-by:` and `Agent-<name>:`
  trailers, and the `commit-attribution` workflow now runs that hook on each
  commit instead of a copy of its pattern, so the two cannot drift. Gate 14
  runs the hook against `tests/attribution-cases.tsv`.
- `scripts/gates.sh` stops with one message when `python3` is missing,
  instead of failing gate by gate.
- `docs/quickstart.md` step 1 says where to install Claude Code and that it
  needs an account.
- **Licence: Apache License 2.0 from this release.** `LICENSE` is the
  unmodified official text, and `CITATION.cff`, `README.md`, `GOVERNANCE.md`,
  `references.md`, `docs/security-posture.md` and `docs/project-state.md` name
  it. Releases 0.1.0 to 0.4.0 were published under MIT and stay under it: their
  tags and assets are not rewritten, and what MIT granted for them is not
  revoked. The copyright holder is named in `CITATION.cff` and `README.md`, and
  no NOTICE file is added.
- **Contributions need a Developer Certificate of Origin sign-off.**
  `CONTRIBUTING.md` gains a licence and sign-off section (inbound licence, the
  DCO, `git commit -s`, how to add a missing sign-off, and the pause when
  someone else may own the work), `GOVERNANCE.md` states the pause, and
  `.github/workflows/dco.yml` fails a pull request containing a commit with no
  sign-off for its author. No contributor licence agreement is asked.
- Four skills (`working-preferences`, `document-standards`, `technical-documents`,
  `surface-regimes`) each gain one line pointing to `skill-creation` for making a skill and
  `skill-discovery` for deciding whether a need justifies one, or locating one.
- `docs/security-posture.md` rows 3.7 and 4.4 state the rule for every
  workflow instead of a count, which had gone stale twice.
- `daily-review` step 5: the Most Important Task is the person's first task
  in Next, in the order the review proposes, the rule the lane board marks.
- `scripts/reorient` names what it skips: a path that is not a repository
  gets a line, MAIL says `none` when nothing is new, and TASK says
  `not checked` when `ps` is missing (pull requests #30 and #36).
- `session-log`'s description names what the capture records, the decisions,
  corrections, open questions and findings, where it said it writes the
  reasoning; `orient` and `session-close` describe it the same way (pull
  request #22).

### Skill revisions

- `daily-review` v3 to v4.
- `document-standards` v4 to v5.
- `orient` v2 to v3.
- `session-close` v5 to v6.
- `session-log` v2 to v3.
- `surface-regimes` v3 to v4.
- `technical-documents` v2 to v3.
- `working-preferences` v5 to v6.

## 0.4.0 (2026-10-13)

A MINOR release under `docs/releasing.md`: three new skills, three new scripts, each
with a gate, and the issue #11 fix, which carries one BREAKING skill change. The
`scripts/reorient` selftest rows for planted positives (pull request #20) were
added after the 2026-10-09 cutoff and change the selftest only.

### Added

- `skills/merge-proxy/`, a seventh procedure a person invokes. For the session
  it is invoked in, an agent may run and push a merge into a trunk on a
  repository whose remote is internal or absent, after explaining the whole
  plan and halting for approval of each merge. Never on a GitHub or other
  internet remote. The decision stays the person's; only the typing moves.
- `scripts/remote-level.sh`, the remote classifier `merge-proxy` runs first:
  `none`, `internal` or `external` from where a repository's remotes point,
  `external` whenever a host cannot be proven internal. A ninth gate runs its
  `--selftest`.
- `skills/weekly-review/`. A once-a-week pass over a task board's slower lanes:
  each Waiting blocker chased, carried work named by its count, the Done lane
  read back against each task's own verification, and one important task given
  a day, never a due date. It proposes and asks; it moves nothing the person
  did not answer.
- `skills/monthly-review/`. A once-a-month pass: each Someday/Maybe item
  adopted, kept or rejected, long-stalled Waiting work questioned, and the
  tool's archive candidates chosen by the person, leaving as reference or as
  trash. The only review that archives a task the board has been holding, and trash
  never satisfies a dependency (v2, after a second-party check of v1).
- `scripts/reorient`, the observing half of `skills/orient/`, which shipped
  without it. Paths come from the workspace's `CLAUDE.md` and manifest; mail is
  off unless `REORIENT_INBOX_REPO` is set. A tenth gate runs its `--selftest`
  on `examples/workspace/` and against planted positives, among them mail on a
  sibling branch, a flag filed below Resolved, and a runbook named like a
  capture. `orient` v2 names it.
- `docs/releasing.md` says how a skill is versioned and retired (MINOR, a new
  release rule that leaves existing usage working). Three new sections: Skill
  revisions, where a skill's `vN` lives only in its own `CHANGELOG.md` and each
  release names the skills whose revision moved; A skill's interface, six
  surfaces, including when a skill fires, and what counts as breaking, labeled
  BREAKING pre-1.0; and Deprecation, announced in one release and removable no
  earlier than the second after it, with experimental skills exempt while the
  kit is pre-alpha. Release notes gain a Deprecated heading.
- `docs/installing.md`, the installing guide: where each part of the kit goes
  among Claude Code's features, workspace-level against user-level skills and
  why a user-level copy shadows a workspace one, symlink or copy,
  `CLAUDE.local.md`, enabling the hooks through the `hookify` plugin, updating,
  removing, and how a workspace grows (a place for unsorted imports, a
  repository, tiers). Reported in issue #11.
- `examples/workspace/`: the workspace the quickstart copies. `CLAUDE.md`
  naming the provenance layer and the manifest, `index.md`, and stubs of the
  standing files under `.agents/`, each holding comments rather than content.
- An eighth gate, `scripts/check-workspace-stubs.py`: every stub in
  `examples/workspace/` is a file `docs/standing-documents.md` describes, every
  described file has a stub or a stated exemption, and the stub `index.md`
  lists every stub under `.agents/`. It has a planted positive in
  `scripts/gates.sh --selftest`.
- `docs/releasing.md` step 9 deletes the release branch once the release is
  published and the local `main` is pulled.

### Changed

- `README.md` and `docs/project-state.md` list eighteen skills, with
  `merge-proxy`, `weekly-review` and `monthly-review` among those a person
  invokes; `docs/project-state.md` and `CONTRIBUTING.md` describe ten gates,
  with `remote-level.sh` and `reorient` under `scripts/`.
- `docs/quickstart.md` is one path in six steps, from checking the
  prerequisites to a session log on disk, each step ending with what you should
  now see. It clones the kit, copies `examples/workspace/`,
  and installs the skills into the workspace with `scripts/link-skills.sh`. Alternatives, and
  the material on growing a workspace, moved to `docs/installing.md`. The
  quickstart no longer creates `intake/`; the guide says what it is for.
  Reported in issue #11.
- `README.md`: "Installing the skills" points to the quickstart and the
  installing guide instead of carrying its own `cp` command, the `hooks/`
  section says the rules need the `hookify` plugin, and a new `examples/`
  section describes the example workspace.
- `CONTRIBUTING.md` lists what `scripts/gates.sh` needs, and its em dash
  check no longer uses `grep -P`, which only GNU grep has.
- `docs/project-state.md` names the example workspace and gains an "In v0.4.0"
  section.
- `skills/daily-review/` v2: its Scope Pointer names `weekly-review` as
  shipped.
- `skills/daily-review/` v3 and `skills/weekly-review/` v2: the lanes table
  and Scope Pointer (daily) and the Scope Pointer (weekly) name
  `monthly-review` as shipped. No change to either procedure.
- Every `skills/*/CHANGELOG.md` relabeled to the shape `docs/releasing.md` now
  states (PATCH, no entry text changed): one integer `vN` per heading, unique,
  newest first, title `# CHANGELOG`. Renumbered: `document-standards` second
  `v2` to `v4 (was v2)`, `redaction-gate` `v2.1` to `v3 (was v2.1)`, and
  `daily-review` `v1.1` to `v2`. Reordered newest first: `document-standards`,
  `skill-creation`, `surface-regimes`, `technical-documents`,
  `working-preferences`.

### Fixed

- `scripts/gates.sh`: the em dash and private task ID gates searched `.git`,
  because `--exclude-dir` followed `--` and was read as a file name, and
  passed when `grep` could not run at all. Both now fail on a `grep` error,
  and the selftest runs the two gates themselves on a planted tree instead of
  a copy of their command line.
- **BREAKING** `skills/session-close/` v5: phase 1 writes provenance to the
  layer the tree's `CLAUDE.md` names instead of a path from the tree it was
  written in; the phase 3 dash sweeps no longer need GNU grep; and the memory
  store check is stated as the source tree's example, to be substituted, and
  reported as not applicable where a tree keeps no store. Reported in
  issue #11.
  Migration: name your provenance layer in your `CLAUDE.md`; where it names
  none, the skill now stops and asks instead of writing to
  `agents/claude/context/`. It skips the deprecation window as a safety fix:
  the old default could put session reasoning in a repository that later
  gains a public remote.
- `skills/session-log/` v2: it writes no em dash, headings included, so
  `session-close` no longer has to correct its captures. Reported in issue #11.

### Skill revisions

- `daily-review` v1 to v3.
- `merge-proxy` v1, new.
- `monthly-review` v2, new (v1 and v2 both in this release).
- `orient` v1 to v2.
- `session-close` v4 to v5, BREAKING.
- `session-log` v1 to v2.
- `weekly-review` v2, new (v1 and v2 both in this release).

## 0.3.0 (2026-09-29)

A MINOR release under `docs/releasing.md`: one new skill, and a release cadence.
Documentation and skill files only; no script changes.

### Added

- `skills/daily-review/`. A once-a-day pass over a task board's lanes: the
  Inbox clarified to empty, carried work counted, finished work offered for
  close, priority read as an Eisenhower quadrant, and the day's order proposed.
  It proposes and asks; it moves nothing the person did not answer. It assumes
  a lane-board tool and says what that tool must print.
- `docs/releasing.md` has a Cadence section: a release review every two weeks
  on a Tuesday, with a Friday cutoff and a Monday final review, and a release
  only when the review admits one.

### Changed

- `CITATION.cff` lists only the concept DOI, which is the one to cite. Each
  version DOI is recorded under "Where releases stand" in `docs/releasing.md`
  by the release after it, so a release no longer needs a follow-up pull
  request to record its DOI. Steps 3 and 7 of `docs/releasing.md` say so.
- `README.md` and `docs/project-state.md` list fifteen skills, with
  `daily-review` among those a person invokes.
- `docs/quickstart.md`: the example `CLAUDE.md` names the provenance layer and
  the file that lists the standing files, which the loop skills look for
  before writing.

## 0.2.0 (2026-09-26)

A MINOR release under `docs/releasing.md`: three new skills, and a changed
question format in `working-preferences`. Pre-1.0, so the format change is
allowed in a MINOR bump. Documentation and skill files only; no script changes.

### Added

- `orchestration/ROLES.md`. Operator, lead, aide and minions, defined as an
  axis of authority over a decision, separate from clearance, working surface
  and reach. Persona is stated to be a different thing, and is left unbuilt.
- `skills/orient/`. The judgement half of a reorientation. The mechanical half
  is delegated to whatever state tool the adopting tree has.
- `skills/jot/` and `skills/touch/`. Partial captures an agent may call at a
  clean boundary: `jot` records decisions, corrections and findings, and
  `touch` makes one fact-level update to a standing file.
- `docs/partial-captures.md`. The rules `jot` and `touch` share, including
  that neither satisfies `session-log` or `session-close`, and that each marks
  its entry so it cannot be mistaken for one.
- `docs/quickstart.md`, linked from `README.md`.

### Changed

- `working-preferences` v5. Adds Context Cadence, which sets when the agent
  reports context size and when it offers a compaction. **Replaces the NEXT
  block with Questions and Answers**: three labeled questions, each closing
  with the codes it accepts, answered as `f q1; 2 q2`. An adopter who relies
  on the NEXT block needs to update. Mirrored in `docs/interface-contract.md`,
  `docs/control-layers.md` and `skills/commands/`. Reasons are in the skill's
  own `CHANGELOG.md`.
- `session-close` now prefers a tool that judges each memory store by where it
  is and whether it holds data, over the path grep, which has passed while
  the declared store had never been written.
- `docs/project-state.md` has a section for this release, and task ids on each
  known gap.
- `docs/releasing.md` step 3 describes setting the citation fields in the tree
  that gets tagged, and steps 4, 7 and 8 no longer describe the first release
  as still to come. Step 5's examples name this release.
- `skill-creation` v2. The naming convention allows a single verb for a
  procedure an agent runs on its own at a clean boundary, which covers
  `orient`, `jot` and `touch`. A skill that governs a domain still takes a
  noun phrase.

### Fixed

- `README.md` and `docs/project-state.md` said eleven skills and listed only
  those. Both now list all fourteen in three classes, and the README tells an
  adopter to copy the whole `skills/` folder rather than a count.
- `orient`, `jot` and `touch` arrived without the `CHANGELOG.md` every other
  skill carries. Each now has a v1 entry giving the reasons for its shape.
- Three markdown findings from the gates: two code fences without a language,
  and one double blank line.

## 0.1.0 (2026-09-19)

First tagged release. Pre-1.0: the orchestration schema and skill interfaces
still move, and a MINOR bump may break something. `README.md` says pre-alpha and
that remains true.

The kit at this release is eleven skills, the orchestration protocol with its
two JSON schemas and a four-vendor registry, seven inert hook rule examples, and
four scripts. Most of it is not new at 0.1.0; the version exists because having
no release at all blocks the OpenSSF badge, a Zenodo DOI, and having a version
to report a vulnerability against.

### Added

- `GOVERNANCE.md`. One maintainer, stated as a governance model rather than left
  implicit, with bus factor one named as a known risk. Merges, tags and pushes
  are not delegated, and the document says why that boundary is the main control
  keeping review meaningful in a project where agents do much of the editing.
- `docs/releasing.md`. Repo-wide semantic versioning, cut as an annotated tag.
  Chosen over per-skill version strings because skills here reference each other
  by name and load as a set, so a reader needs to know which set they have. The
  absence of any release was blocking the OpenSSF badge, a Zenodo DOI, and
  having a version to report a vulnerability against.
- `docs/security-posture.md`. One row per control, with an evidence column that
  names a file or says the thing is absent. Organised by control area rather than
  by criterion ID until the criterion lists are transcribed from their published
  source, because inventing criterion IDs would produce a document that looks
  authoritative and cites nothing.
- `scripts/gates.sh` and `.github/workflows/gates.yml`. The seven mechanical
  gates `CONTRIBUTING.md` states as rules, now enforced. The gates live in the
  script and the workflow calls it, so a contributor's local run and CI are the
  same text rather than two copies that can drift.
- `scripts/gates.sh --selftest`, which plants a positive for each gate and
  confirms the gate fires before the real pass runs. A gate that has never
  returned a hit has not been shown capable of returning one.
- `.github/dependabot.yml`, github-actions only. The repository ships no package
  manifest, so the actions used by the two workflows are its entire declared
  dependency surface.
- `permissions: contents: read` on the new workflow.
- `scripts/mdlint.py`, a seventh gate. Eighteen markdown structure rules using
  markdownlint's own rule IDs, standard library only. markdownlint itself was
  rejected on the same grounds the CI design note rejected third party actions:
  `npx` fetches at run time, which is a supply chain surface attached to the
  thing meant to increase trust, and a package manifest is the other half of
  that cost in a repository that deliberately ships none. Four of the rules are
  accessibility rules mapped to WCAG techniques in `docs/document-accessibility.md`.
- `docs/document-accessibility.md`, the output-side companion that
  `docs/accessibility.md` section 8 listed as open. Technique IDs read from
  local W3C captures or from a supplied URL, never from recall, and the document
  says plainly that the project does not claim conformance.
- A Succession section in `GOVERNANCE.md`, naming what a successor needs and the
  state of each item. Nobody is listed as a maintainer without written consent.

### Changed

- `README.md` restructured around an index of descriptive anchor links, with the
  narrative moved into `philosophy.md`. One `h1`, no skipped heading levels.
- `philosophy.md` deduplicated. `## The name` was fully contained in the
  Toothpaste Repairman section and pointed at a README passage that had moved
  into the same file, so it was removed rather than rewritten. The author's own
  sections are unchanged, verified byte for byte against the committed original.
- Three mechanical rules in `CONTRIBUTING.md`, stated before they could block
  anyone: every `.json` parses, a registry entry is self-consistent, and every
  `SKILL.md` carries `name` and `description`. A blocking check that no document
  promises would reject a contributor under a rule they had no way to read.

### Fixed

- `docs/project-state.md` was twelve days stale. It called five committed
  documents uncommitted, and described the code of conduct's reporting contact as
  a placeholder when it is a real address.
- A typo in the `README.md` overview.

### Known

- **`scripts/mdlint.py` has a quadratic-time residual that is bounded per line
  and not per file.** Six `py/polynomial-redos` alerts are dismissed as
  `won't fix` rather than as false positives, because the patterns are real:
  four of them were independently reproduced on a second host at 15x to 16x
  scaling when the input quadruples, against a known-quadratic control at 11x.
  `MAX_LINE` caps analysis at 2000 characters and its guard precedes every
  affected call site, so a worst-case line costs roughly 29 ms. Nothing caps how
  many such lines one file may hold, so a hostile input makes the check slow
  rather than making it hang. `docs/security-posture.md` row 4.10 carries the
  full reasoning.

## 2026-09-06

### Added

- `SECURITY.md`, `CODE_OF_CONDUCT.md`, `CITATION.cff`, and `.github/ISSUE_TEMPLATE/` (a config plus
  defect, finding, and registry-addition forms). Drafted 2026-09-05 and completed 2026-09-06, having
  been blocked on decisions that were the maintainer's rather than on anything to write.
- `SECURITY.md` defines a vulnerability for a repository that ships no service, which is narrower
  and stranger than the usual list. The highest severity defect here is a gate that fails open,
  because that failure is invisible to the person relying on it. Private vulnerability reporting on
  GitHub is the primary channel, with an email fallback for people who cannot or will not use it.
- `CODE_OF_CONDUCT.md` names the reporting address and then says plainly that this project has one
  maintainer, that the address reaches that person, and that there is no independent body to
  escalate to. A reporter is asked to name a third party they would accept if the report concerns
  the maintainer. Implying a process that does not exist would be worse than the honest version.

### Changed

- `README.md` and `CONTRIBUTING.md` no longer say the kit is maintained by Bridle Works. Bridle
  Works is the project this kit belongs to and is not a formed entity, so it cannot maintain or hold
  anything. Both now name the person who does. This is the same correction made to `LICENSE` on
  2026-09-05, applied to the two places nothing had connected to it.

## 2026-09-05

### Added

- `skills/daily-dashboard/`, a third human-invoked procedure. It opens a working session the way
  `session-close` ends one: read the standing files, verify carry-over against every Git working
  tree rather than against the previous session's closing report, then present project state, a
  ranked todo list, the roadmap, and the decisions waiting on a person. It ends on numbered
  questions and starts no work.
- The pair is now a loop. `session-close` already assumed something would read back what it wrote,
  and nothing did; a start-of-day summary was being typed by hand as an ad hoc prompt each time,
  which is the same gap `session-close` itself was built to close. Reconstructed from the one
  recorded instance of that prompt rather than designed fresh, so the four-section shape and the
  todo ranking rule are the ones already in use.
- `disable-model-invocation` is set, matching the other two procedures. An agent should not decide
  that the working day has started any more than it should decide the session is over.

- `skills/session-log/`, a fourth human-invoked procedure and the cheap counterpart to
  `session-close`. It covers the compaction boundary: write the reasoning from the recent stretch
  to one append-only provenance file, in a single pass, and stop. No standing-file updates, no
  mechanical checks, no verification.
- Running `session-close` more often was the obvious alternative and does not survive its price.
  The skill is aimed at the one thing compaction destroys, which is why a file looks the way it
  does rather than what it says, and it states in its own text that it does not discharge
  `session-close`.

### Changed

- `skills/session-close/` to v4. It gained the closing `# Scope Pointer` section it had been
  shipping without since v1, now naming `daily-dashboard` as the half of the loop that reads back
  what it writes. Phase 3's memory containment check also gained a caveat: it greps `.mcp.json`,
  which is a declaration rather than the running server, so a server registered elsewhere leaves
  the check passing against a config that no longer governs it.
- Both were found by running this repo's own Integration Checklist while adding the new skill,
  which is what that checklist is for.

### Known gap

- Three skills still have no closing cross-reference section: `redaction-gate`, `surface-regimes`,
  and `technical-documents`. `skill-creation` requires one. Nothing in the repo checks, and the
  rule is currently enforced by whoever opens the checklist.

## 2026-09-04

### Added

- `scripts/reflow-md.py`, which unwraps hard-wrapped Markdown paragraphs to one line each. Markdown
  collapses single newlines, so a hard wrap changes nothing about how a document renders; what it
  changes is that the author's column width gets baked into the file and every reader inherits it,
  at 200% zoom, in a narrow split, or through a screen reader. Fenced code, front matter, tables,
  blockquotes, headings, and list indentation are left alone. `--check` is a dry run. Every rewrite
  verifies that the whitespace-normalized token stream is unchanged before writing, and a file that
  fails is left untouched.
- `scripts/reflow-md.test.md` and `scripts/reflow-md.expected.md`, run by `--selftest`, which also
  checks idempotence. The fixture earned its place immediately: it caught two bugs that the token
  check could not see, because that check normalizes whitespace. A nested list item was losing its
  indentation, which promotes it to top level, and a hard break was losing the two trailing spaces
  that create it. Both changed the rendered document while preserving every word.
- A "Why these filenames are here at all" section in `docs/standing-documents.md`. A filename either
  names a role or names a subject. A role name says what the file does for the system and every tree
  organized this way has one, so publishing it discloses nothing. A subject name is a fact about you
  before anyone reads a word, and gets treated as content.

### Changed

- `README.md`'s framing section rewritten. It now defines the centaur and reverse-centaur terms
  rather than assuming them, and rests the argument on determinism: the analogy was built for
  systems where the same input gives the same output, and a non-deterministic system has something
  it has no slot for. The accessibility consequence is stated as fitment rather than accommodation,
  since tack already varies by rider and horse and nobody calls a different bit an accommodation.
  The intro line dropped a slogan that only parsed after reading the section it summarized.
- `README.md`, `CONTRIBUTING.md`, and `docs/standing-documents.md` reflowed to one line per
  paragraph, matching the nine other prose files in the repo that were already soft-wrapped. The
  three had been the outliers. `CHANGELOG.md` and `docs/project-state.md` are left wrapped.
- `docs/standing-documents.md` opening reframed. It previously read as an apology for pointers that
  led nowhere, which stopped being true once the structure became something deliberately shared. Six
  table rows now carry real filenames instead of generic role descriptions.
- `skills/session-close/` to v2. Phase 1 item 6 gained two named cases, and the phase now says a
  reference sweep has to drive its own directory walk rather than trusting a recursive grep that may
  honor ignore files and report clean.

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

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
