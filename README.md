# Toothpaste Kit: `tp-kit`

A skill library, an agent relay protocol, and a set of mechanical gates for running multi-agent work with a person in charge of it. Judged on control fidelity rather than capability: legible state, cheap correction, a reliable halt.

**Status: work in progress, pre-alpha.** The skills are in daily use and the interfaces still change.

[![gates workflow status](https://github.com/AN0099/toothpaste-kit/actions/workflows/gates.yml/badge.svg?branch=main)](https://github.com/AN0099/toothpaste-kit/actions/workflows/gates.yml) [![licence: Apache 2.0](https://img.shields.io/badge/licence-Apache%202.0-blue.svg)](LICENSE) [![concept DOI, resolves to the newest version](https://zenodo.org/badge/DOI/10.5281/zenodo.22850481.svg)](https://doi.org/10.5281/zenodo.22850481) [![latest tagged release](https://img.shields.io/github/v/release/AN0099/toothpaste-kit?label=release)](https://github.com/AN0099/toothpaste-kit/releases) [![Software Heritage archive status](https://archive.softwareheritage.org/badge/origin/https%3A%2F%2Fgithub.com%2FAN0099%2Ftoothpaste-kit/)](https://archive.softwareheritage.org/browse/origin/https%3A%2F%2Fgithub.com%2FAN0099%2Ftoothpaste-kit/) [![OpenSSF Best Practices level](https://www.bestpractices.dev/projects/14726/badge)](https://www.bestpractices.dev/projects/14726) [![REUSE status](https://api.reuse.software/badge/github.com/AN0099/toothpaste-kit)](https://api.reuse.software/info/github.com/AN0099/toothpaste-kit)

**Accessibility is a requirement here, not an afterthought.** The documents this repository ships are authored against [WCAG techniques for Markdown, with the technique IDs stated](docs/document-accessibility.md), and `scripts/mdlint.py` enforces the mechanically checkable half of them. The other side, [the accessibility of the interface this work is done through](docs/accessibility.md), is documented with it.

A Bridle Works project, maintained by Aidan Naveja.

## Index

Where to go, by what you came for.

- [What this kit is](#what-this-kit-is), if you want the one-paragraph version
- [What is here](#what-is-here), a directory-by-directory tour of the repository
  - [`skills/`](#skills), the eighteen skills in three classes
  - [`docs/`](#docs), the documents the skills assume
  - [`examples/`](#examples), the workspace the quickstart copies and a practice review round
  - [`hooks/`](#hooks), example rules for the `hookify` plugin
  - [`scripts/`](#scripts), the gates and the tools they run
  - [`orchestration/`](#orchestration), the relay protocol and its schemas
- [Installing the skills](#installing-the-skills), the fastest path to using it
- [Using the orchestration protocol](#using-the-orchestration-protocol), for relaying work between agents
- [Packing this repo for an LLM](#packing-this-repo-for-an-llm), to paste the whole thing into a model, or ask DeepWiki instead
- [Contributing](#contributing), including the lowest-friction first contribution
- [Project documents](#project-documents), governance, security, releases, accessibility and the changelog
- [Why this exists](#why-this-exists), the reasoning behind every choice above
- [License and citation](#license-and-citation)

## What this kit is

This is documentation for both the user and the agent. It holds an information corpus, a skill library, a vendor-independent capability taxonomy, a message schema for relaying work between agents and humans across surfaces, and a routing rule that gates dispatch on content sensitivity.

It is currently designed around a local Claude Code instance as the lead orchestrator. Most of it is Agent Skills compatible, plain shell and Python scripts, and Markdown, so it stays portable across vendors. A modular, vendor-agnostic framework is on the roadmap.

## What is here

### `skills/`

Eighteen skills, in three classes.

Seven govern agent behavior continuously. An agent loads them on its own when the frontmatter `description` matches what it is doing.

| Skill | Covers |
|---|---|
| `working-preferences` | Standing defaults, register, correction protocol, command vocabulary |
| `document-standards` | Writing standards for generated documents, with formality, density, and audience dials |
| `technical-documents` | Presets for runbooks, postmortems, ADRs, and handoff notes aimed at ops readers |
| `surface-regimes` | Detects whether a session is interactive, autonomous, or programmatic, and sets dials to match |
| `skill-creation` | Naming, required structure, and checklists for adding a skill |
| `skill-discovery` | Whether a recurring need is worth a skill, and finding one that already exists |
| `commands` | Index for the twenty-seven-command vocabulary, with brevity codes |

Eight are procedures a person invokes. All eight set `disable-model-invocation`, so an agent cannot trigger them. That is the point in each case: a gate a model can invoke to satisfy itself is not a gate, and an agent should not decide on its own that a session is over or that a working day has started.

| Skill | Runs |
|---|---|
| `redaction-gate` | Before content crosses a sensitivity boundary outward. Reports findings, hands the decision to a person |
| `session-close` | At the end of a working session. Captures reasoning that exists nowhere on disk, then updates the standing documents |
| `daily-dashboard` | At the start of a working session. Reads those documents back, verifies carry-over against the working trees, and ends on questions |
| `daily-review` | Once a day, before the first task is pulled. Proposes moves across the task board's lanes and ends on questions; assumes a lane-board tool |
| `weekly-review` | Once a week, after a daily review. Chases Waiting's blockers, names carried work by its count, reads the Done lane back, and schedules one important task; ends on questions |
| `monthly-review` | Once a month, after a weekly review. Adopts or rejects each Someday item, asks whether long-stalled Waiting work is still committed, and lets the person choose which archive candidates leave the board; ends on questions |
| `session-log` | Mid-session, before context is compacted. Records the decisions, corrections, open questions and findings from the recent stretch to one append-only file, and nothing else |
| `merge-proxy` | When a person wants the agent to type a merge they have decided. For that session, on a repository whose remote is internal or absent, the agent may run and push a trunk merge after explaining the full plan and halting for approval of each one. Never on a GitHub or other internet remote |

Three are procedures an agent may run on its own at a clean boundary. None sets `disable-model-invocation`, because each one reads or records and none decides anything. None of them satisfies `session-log` or `session-close`.

| Skill | Runs |
|---|---|
| `orient` | After a compaction or a handoff, or before acting on a summary. Runs the tree's own state tool, then asks what moved and where the record disagrees with the tree |
| `jot` | After a stretch of work. Appends one short, marked entry of decisions, corrections and findings to the day's capture file |
| `touch` | Right after the work it records. Makes one fact-level update to a standing file, and leaves a marked line in the day's capture file |

### `docs/`

`docs/standing-documents.md` describes the document structure that `redaction-gate`, `session-close`, and `daily-dashboard` assume: what each standing file does, how they work together, and the sensitivity tiering the redaction procedure depends on. Read it if a skill's pointers look like they lead nowhere.

`docs/project-state.md` is where the kit itself stands.

### `examples/`

`examples/workspace/` is the workspace the quickstart copies: a `CLAUDE.md` naming where the other files are, the manifest `index.md`, and stubs of the standing files under `.agents/`. The stubs hold comments saying what goes in each, and point at `docs/standing-documents.md` rather than restating it. A gate checks that each stub matches a file that document describes.

`examples/review-round/` is a practice [review round](docs/review-rounds.md): a small synthetic project with a proposed change that carries a known defect, the material for the reviewer and the verifier in separate directories, an answer key, and the schema test cases that gate 18 runs. [`examples/README.md`](examples/README.md) indexes both examples, and each directory in the review round has its own README.

### `hooks/`

Eight rules for the `hookify` plugin, as examples rather than live configuration. They need the plugin installed, and do nothing where they sit; [the installing guide](docs/installing.md#hooks) says how to enable them.

Five block: a forbidden character in generated content, a packing command without an allow-list, a packing command that turns off `.gitignore`, a push without an explicit destination branch or one that skips the git hooks, and a command naming restricted material that also carries an egress verb. The other three warn on reads that pull sensitive material into context, so a later publish step knows the session is derived from it. They assume a tiered directory scheme; adapt the patterns before enabling them.

### `scripts/`

`gates.sh` is the mechanical gates, one implementation run both by CI and by hand before a push; `./scripts/gates.sh --selftest` also proves each gate can fail against a planted positive. Its header states what each gate covers. `compliance.sh` holds the checks that need an installed tool, REUSE among them, so a fresh clone can still run every gate in `gates.sh` with only the tools [`CONTRIBUTING.md` lists](CONTRIBUTING.md#run-the-checks-the-way-ci-runs-them), and nothing installed.

The gates call these, and each runs on its own as well:

- `mdlint.py`: Markdown structure checks under markdownlint's rule IDs, standard library only
- `check-branch-name`: the one definition of an allowed branch or tag name, used by the pre-push hook, a gate and CI
- `check-hooks.py`: checks the rules in `hooks/` and shows each blocking one can fire
- `check-workspace-stubs.py`: checks `examples/workspace/` against `docs/standing-documents.md`
- `schema-check.py`: validates `orchestration/registry/*.json` against its schema
- `check-qblock`: checks a reply's closing question block against `working-preferences`
- `check-pr-body`: checks a pull request body against `.github/pull_request_template.md`; CI also runs it on each pull request
- `cli_path.py`: keeps a path given on a script's command line inside a root directory; `spdx-fragment.py` uses it for `--models`
- `spdx-fragment.py`: builds an SPDX fragment of who assisted a commit range from its `Assisted-by:` trailers, taking per-model values from `spdx-models.json`
- `remote-level.sh`: classifies a repository by where its remotes point, as none, internal or external, and treats any host it cannot prove internal as external
- `reorient`: prints where a workspace stands in one screen, for the start of a session and after a compaction; the observing half of the `orient` skill
- `round-check.py`: validates review-round documents against their schemas in `orchestration/schemas/round/`

`auto-qa-tuner.py` proposes CI job timeouts from the repository's own run history.

`link-skills.sh` symlinks `skills/` into your Claude skills directory instead of copying, so `git pull` updates them in place. Targets are relative where `ln -r` exists, so the links survive the tree being moved, and absolute otherwise; the script reports which it used.

`reflow-md.py` unwraps hard-wrapped Markdown paragraphs to one line each. Markdown collapses single newlines, so a hard wrap changes nothing about how a document renders; what it does change is that the author's column width gets baked into the file and every reader inherits it. Fenced code, tables, front matter, headings, blockquotes, and list indentation are left alone. Use `--check` for a dry run. `--selftest` runs the bundled fixture in `reflow-md.test.md` against `reflow-md.expected.md` and exits nonzero on failure; run it after any change to the script.

`remote-level.sh PATH` prints a repository's level from where its remotes point: `none`, `internal` (a path or a private address) or `external` (anything else, GitHub included). A host it cannot prove internal is `external`. `merge-proxy` runs it as its first step. `--selftest` proves all three answers on scratch repositories, and a gate runs it.

`reorient [ROOT]` is the observing half of the `orient` skill: one screen of a workspace's state, git per repository, the newest capture and its partials, queues, flags and standing files found through the manifest, ending in a COVERAGE block. It reads its paths from the workspace's `CLAUDE.md` and manifest, so it names no desk. Mail is read only when `REORIENT_INBOX_REPO` is set. `--selftest` runs it on `examples/workspace/` and against planted positives, and a gate runs it.

### `orchestration/`

The protocol for passing work between agents on different surfaces.

| File | Holds |
|---|---|
| `orchestration/README.md` | What the system is for, and where to start |
| `orchestration/protocol.md` | The relay protocol itself |
| `orchestration/taxonomy.md` | Role and surface definitions |
| `orchestration/ROLES.md` | The operator, lead, aide and minion roles |
| `orchestration/rounds.md` | Rounds: delegated work, checked and decided |
| `orchestration/ROUTING-THRESHOLD.md` | When work goes to a local model and when to a vendor |
| `orchestration/CHANGELOG.md` | The decision log for the protocol's own design |
| `orchestration/schemas/request.json` | Request message schema |
| `orchestration/schemas/response.json` | Response message schema |
| `orchestration/schemas/event-base.json` | Shared event envelope |
| `orchestration/ingestion/` | Specs for turning vendor data exports into machine-readable digests |
| `orchestration/registry/` | One surface descriptor per vendor, and the schema they follow |
| `orchestration/templates/` | Templates for a relay message and a handoff note |

## Installing the skills

First time: follow the [quickstart](docs/quickstart.md). It is one path, six steps, ending with a session log on disk.

Otherwise, [the installing guide](docs/installing.md) covers workspace-level and user-level installs, symlink or copy, the `hookify` plugin the hooks need, updating and removing.

## Using the orchestration protocol

`orchestration/protocol.md` defines the message flow. `orchestration/schemas/request.json` and `orchestration/schemas/response.json` are the schemas a participating agent reads and writes. `orchestration/taxonomy.md` maps surfaces to behavioral regimes and is the join key for the `surface-regimes` skill.

## Packing this repo for an LLM

`repomix` collapses the whole repo into one file suitable for pasting into a model. It is a separate tool, not shipped with the kit; it runs from npm, as `npx repomix` or installed globally, so it needs Node.js:

```sh
repomix --output repomix-output.xml
```

Check that the pack covers the tracked tree. This reads the pack the step above writes, so it needs `repomix` first; without a global install, run that step as `npx repomix --output repomix-output.xml`. The two counts should match:

```sh
git ls-files | wc -l
grep -c '<file path=' repomix-output.xml
```

The output is gitignored on purpose. It is a near-complete copy of the repository, so committing it roughly doubles clone size and produces a full-file diff on every change, and it goes stale silently. `repomix --remote` builds one straight from the GitHub URL without a clone.

To ask questions of the repository without packing it, [DeepWiki](https://deepwiki.com/AN0099/toothpaste-kit) keeps a generated index of it.

## Contributing

Read `CONTRIBUTING.md`. It covers the rules that apply to every change, the structure a skill has to follow, how a commit is signed off, and how it records which tool helped.

The lowest-friction first contribution is a surface descriptor in `orchestration/registry/`. It adds support for a vendor this project does not cover yet, cannot break anyone else's traffic, and needs no knowledge of the rest of the protocol. `orchestration/registry/README.md` has the format.

`CODE_OF_CONDUCT.md` applies in every project space. `SECURITY.md` says what counts as a vulnerability in a repository that ships no service, which is narrower and stranger than the usual list; read it before filing a public issue about a gate.

## Project documents

| Document | What it answers |
|---|---|
| [Quickstart](docs/quickstart.md) | The shortest path from nothing to a working loop |
| [Installing](docs/installing.md) | Where each part goes, the alternatives, updating and removing, and what comes next |
| [Governance](GOVERNANCE.md) | Who decides, how a change lands, and what is never delegated |
| [Contribution guide](CONTRIBUTING.md) | The rules every change passes, and the script that enforces them |
| [Security policy](SECURITY.md) | What counts as a vulnerability here, and how to report one privately |
| [Security for AI agents](SECURITY-AI.md) | What an AI agent may and may not do in this repository |
| [Agent instructions](AGENTS.md) | Where a coding agent working here finds each rule |
| [Security posture](docs/security-posture.md) | Every control, its state, and the evidence for each |
| [Versioning and releases](docs/releasing.md) | The version scheme and the steps to cut a release |
| [Changelog](CHANGELOG.md) | What each release changed, and what has merged since the last one |
| [The kit blog](docs/blog.md) | Writing a post and building the blog's pages and feed |
| [Code of conduct](CODE_OF_CONDUCT.md) | Expected conduct, and who a report reaches |
| [Project state](docs/project-state.md) | Where the kit itself stands right now |
| [Standing documents](docs/standing-documents.md) | The document structure the procedure skills assume |
| [Glossary](docs/glossary.md) | What each term of art here means, and which file defines it |
| [Concepts](docs/concepts.md) | Each idea a contributor needs, with every file that carries it |
| [Interface accessibility](docs/accessibility.md) | Accessibility of the interface the work is done through |
| [Document accessibility](docs/document-accessibility.md) | WCAG techniques applied to the Markdown this repository ships |
| [Review rounds](docs/review-rounds.md) | How a change is reviewed, its findings verified by someone else, and the operator decides; [steps](docs/review-rounds-quickstart.md) |
| [Control layers](docs/control-layers.md) | How automation, gates and the human divide responsibility |
| [Risk tiers](docs/risk-tiers.md) | Which changes need which review |
| [Document layers](docs/document-layers.md) | How a requirement is marked, and what belongs in this repository at all |
| [References and prior work](references.md) | Every external standard this kit depends on or borrows from |

## Why this exists

The reasoning, the two images this project thinks in, and what it refuses to optimise for are in [the philosophy document](philosophy.md).

## License and citation

Apache License 2.0, from release 0.5.0. See [the licence](LICENSE). Releases 0.1.0 to 0.4.0 were published under MIT and stay under it.

Copyright 2026 Aidan Naveja. Contributions are accepted under the same licence, each commit signed off under the Developer Certificate of Origin; see [`CONTRIBUTING.md`](CONTRIBUTING.md#licence-and-sign-off).

[`CITATION.cff`](CITATION.cff) carries citation metadata for anyone referencing this work.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0 -->
