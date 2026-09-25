# Toothpaste Kit: `tp-kit`

A skill library, an agent relay protocol, and a set of mechanical gates for
running multi-agent work with a person in charge of it. Judged on control
fidelity rather than capability: legible state, cheap correction, a reliable
halt.

**Status: work in progress, pre-alpha.** The skills are in daily use and the
interfaces still change.

[![gates workflow status](https://github.com/AN0099/toothpaste-kit/actions/workflows/gates.yml/badge.svg?branch=main)](https://github.com/AN0099/toothpaste-kit/actions/workflows/gates.yml) [![licence: MIT](https://img.shields.io/badge/licence-MIT-blue.svg)](LICENSE) [![concept DOI, resolves to the newest version](https://zenodo.org/badge/DOI/10.5281/zenodo.22850481.svg)](https://doi.org/10.5281/zenodo.22850481) [![latest tagged release](https://img.shields.io/github/v/release/AN0099/toothpaste-kit?label=release)](https://github.com/AN0099/toothpaste-kit/releases) [![Software Heritage archive status](https://archive.softwareheritage.org/badge/origin/https%3A%2F%2Fgithub.com%2FAN0099%2Ftoothpaste-kit/)](https://archive.softwareheritage.org/browse/origin/https%3A%2F%2Fgithub.com%2FAN0099%2Ftoothpaste-kit/) [![OpenSSF Best Practices level](https://www.bestpractices.dev/projects/14726/badge)](https://www.bestpractices.dev/projects/14726)

**Accessibility is a requirement here, not an afterthought.** The documents this
repository ships are authored against
[WCAG techniques for Markdown, with the technique IDs stated](docs/document-accessibility.md),
and `scripts/mdlint.py` enforces the mechanically checkable half of them. The
other side, [the accessibility of the interface this work is done through](docs/accessibility.md),
is documented with it.

A Bridle Works project, maintained by Aidan Naveja.

## Index

Where to go, by what you came for.

- [What this kit is](#what-this-kit-is), if you want the one-paragraph version
- [What is here](#what-is-here), a directory-by-directory tour of the repository
- [Installing the skills](#installing-the-skills), the fastest path to using it
- [Using the orchestration protocol](#using-the-orchestration-protocol), for relaying work between agents
- [Packing this repo for an LLM](#packing-this-repo-for-an-llm), to paste the whole thing into a model
- [Contributing](#contributing), including the lowest-friction first contribution
- [Project documents](#project-documents), governance, security, releases and accessibility
- [Why this exists](#why-this-exists), the reasoning behind every choice above
- [License and citation](#license-and-citation)

## What this kit is

This is documentation for both the user and the agent. It holds an information
corpus, a skill library, a vendor-independent capability taxonomy, a message
schema for relaying work between agents and humans across surfaces, and a
routing rule that gates dispatch on content sensitivity.

It is currently designed around a local Claude Code instance as the lead
orchestrator. Most of it is Agent Skills compatible, plain shell and Python
scripts, and Markdown, so it stays portable across vendors. A modular,
vendor-agnostic framework is on the roadmap.

## What is here

### `skills/`

Eleven skills, in two classes.

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

Four are procedures a person invokes. All four set `disable-model-invocation`, so an agent cannot trigger them. That is the point in each case: a gate a model can invoke to satisfy itself is not a gate, and an agent should not decide on its own that a session is over or that a working day has started.

| Skill | Runs |
|---|---|
| `redaction-gate` | Before content crosses a sensitivity boundary outward. Reports findings, hands the decision to a person |
| `session-close` | At the end of a working session. Captures reasoning that exists nowhere on disk, then updates the standing documents |
| `daily-dashboard` | At the start of a working session. Reads those documents back, verifies carry-over against the working trees, and ends on questions |
| `session-log` | Mid-session, before context is compacted. Captures the reasoning from the recent stretch to one append-only file, and nothing else |

### `docs/`

`docs/standing-documents.md` describes the document structure that `redaction-gate`, `session-close`, and `daily-dashboard` assume: what each standing file does, how they work together, and the sensitivity tiering the redaction procedure depends on. Read it if a skill's pointers look like they lead nowhere.

`docs/project-state.md` is where the kit itself stands.

### `hooks/`

Seven `hookify` rules, as examples rather than live configuration. Copy the ones you want into your own `.claude/` directory; they do nothing where they sit.

Two block (a forbidden character in generated content, and a packing command without an allow-list). The rest warn on reads that pull sensitive material into context, so a later publish step knows the session is derived from it. They assume a tiered directory scheme; adapt the patterns before enabling them.

### `scripts/`

`link-skills.sh` symlinks `skills/` into your Claude skills directory instead of copying, so `git pull` updates them in place. Targets are relative where `ln -r` exists, so the links survive the tree being moved, and absolute otherwise; the script reports which it used.

`reflow-md.py` unwraps hard-wrapped Markdown paragraphs to one line each. Markdown collapses single newlines, so a hard wrap changes nothing about how a document renders; what it does change is that the author's column width gets baked into the file and every reader inherits it. Fenced code, tables, front matter, headings, blockquotes, and list indentation are left alone. Use `--check` for a dry run. `--selftest` runs the bundled fixture in `reflow-md.test.md` against `reflow-md.expected.md` and exits nonzero on failure; run it after any change to the script.

### `orchestration/`

The protocol for passing work between agents on different surfaces.

| File | Holds |
|---|---|
| `orchestration/protocol.md` | The relay protocol itself |
| `orchestration/taxonomy.md` | Role and surface definitions |
| `orchestration/schemas/request.json` | Request message schema |
| `orchestration/schemas/response.json` | Response message schema |
| `orchestration/schemas/event-base.json` | Shared event envelope |
| `orchestration/ingestion/` | Specs for turning vendor data exports into machine-readable digests |

## Installing the skills

Copy the directories under `skills/` into your Claude skills directory:

```sh
cp -r skills/* ~/.claude/skills/
```

Each skill is one `SKILL.md` and a `CHANGELOG.md`, plus an optional `references/`. They cross-reference each other by name, so copy all eleven or expect broken pointers.

To symlink instead of copy, so that a `git pull` updates them in place:

```sh
scripts/link-skills.sh
```

Skills load on their frontmatter `description`. Read `skills/skill-discovery/SKILL.md` for how that resolution works.

## Using the orchestration protocol

`orchestration/protocol.md` defines the message flow. `orchestration/schemas/request.json` and `orchestration/schemas/response.json` are the schemas a participating agent reads and writes. `taxonomy.md` maps surfaces to behavioral regimes and is the join key for the `surface-regimes` skill.

## Packing this repo for an LLM

`repomix` collapses the whole repo into one file suitable for pasting into a model:

```sh
repomix --output repomix-output.xml
```

Check that the pack covers the tracked tree. The two counts should match:

```sh
git ls-files | wc -l
grep -c '<file path=' repomix-output.xml
```

The output is gitignored on purpose. It is a near-complete copy of the repository, so committing it roughly doubles clone size and produces a full-file diff on every change, and it goes stale silently. `repomix --remote` builds one straight from the GitHub URL without a clone.

## Contributing

Read `CONTRIBUTING.md`. It covers the rules that apply to every change, the structure a skill has to follow, and how this repo handles commit attribution.

The lowest-friction first contribution is a surface descriptor in `orchestration/registry/`. It adds support for a vendor this project does not cover yet, cannot break anyone else's traffic, and needs no knowledge of the rest of the protocol. `orchestration/registry/README.md` has the format.

`CODE_OF_CONDUCT.md` applies in every project space. `SECURITY.md` says what counts as a vulnerability in a repository that ships no service, which is narrower and stranger than the usual list; read it before filing a public issue about a gate.

## Project documents

| Document | What it answers |
|---|---|
| [Quickstart](docs/quickstart.md) | The shortest path from nothing to a working loop |
| [Governance](GOVERNANCE.md) | Who decides, how a change lands, and what is never delegated |
| [Contribution guide](CONTRIBUTING.md) | The rules every change passes, and the script that enforces them |
| [Security policy](SECURITY.md) | What counts as a vulnerability here, and how to report one privately |
| [Security posture](docs/security-posture.md) | Every control, its state, and the evidence for each |
| [Versioning and releases](docs/releasing.md) | The version scheme and the steps to cut a release |
| [Code of conduct](CODE_OF_CONDUCT.md) | Expected conduct, and who a report reaches |
| [Project state](docs/project-state.md) | Where the kit itself stands right now |
| [Standing documents](docs/standing-documents.md) | The document structure the procedure skills assume |
| [Interface accessibility](docs/accessibility.md) | Accessibility of the interface the work is done through |
| [Document accessibility](docs/document-accessibility.md) | WCAG techniques applied to the Markdown this repository ships |
| [Document layers](docs/document-layers.md) | How a requirement is marked, and what belongs in this repository at all |
| [References and prior work](references.md) | Every external standard this kit depends on or borrows from |

## Why this exists

The reasoning, the two images this project thinks in, and what it refuses to
optimise for are in [the philosophy document](philosophy.md).

## License and citation

MIT. See [the licence](LICENSE).

[`CITATION.cff`](CITATION.cff) carries citation metadata for anyone referencing
this work.
