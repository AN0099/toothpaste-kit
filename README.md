# Toothpaste Kit: tp-kit`

**[CURRENT WORK IN PROGRESS // PRE-ALPHA]**

A Bridle Works project. Maintained by Aidan Naveja.

This is a set of documentation both for the user and the agent; an information corpus, a skill library, and agent relay protocol for working with multiple agents. Currently it is designed with Claude being the lead orchestrator in mind, but vendor-agnostic and vendor-specific variants are on the roadmap.

## Why this exists and Who it's for

### Toothpaste Repairman: Automation Engineering

In the 2005 film-adaption of Charlie and the Chocolate Factory, Mr. Bucket screws caps onto toothpaste
tubes until the factory buys a machine that does it faster, and he is let go. He ends the story
hired back to repair the machine that replaced him. That second job is the one this repository is
about. It is harder than the first in every way that matters. Capping tubes needed his hands.
Repairing the capper needs him to understand what the machine is doing and to notice when it stops
doing it, which is the one part of the work the machine cannot take over, because the job is
knowing whether the machine is working.

Everything here is built for the repairman rather than for someone operating a finished product. A
repairman is judged on whether the machine runs, not on how impressive it looks while running, and
that is why this project measures itself on control fidelity instead of capability: legible state,
cheap correction, a reliable halt. It is also why so much of what is here is checks that fail
loudly rather than features that succeed quietly. Nobody keeps a repairman who cannot tell when the
machine is broken, and a check that reports clean because it was never wired up is worse than no
check at all, since it spends the attention that would have found the fault.

### Riding Tack: User Interface & Experience

The "centaur" analogy of automation theory imagines a human-machine collaboration where a person uses technology as a powerful, tireless assistant to execute tasks while retaining ultimate control over judgment and decision-making: a human orchestrator directing an automated agent, each unable to complete the work without the other. The reverse-centaur inverts the roles. An automated orchestrator directs a human agent, the person in the loop only because the machine has no fleshy appendages of its own to do the work.

The analogy holds best with deterministic automated systems, computers and machines where the same input produces the same output every time and 1 + 1 is always 2. Such systems have no will of their own to negotiate with. Applied to a non-deterministic system the centaur gets portrayed as one organism, and it will not be one until human and machine are literally fused. More accurately, what you have is a rider and a horse: two wills, one of them in charge, joined by riding tack.

The tack is the interface. A rider does not think the horse forward. They apply pressure through equipment, the horse interprets it, and the result depends almost entirely on the quality of that equipment and the operator's skill. The horse acts non-deterministically, and retraining it is not on the table, so tack and skill are the only levers left for improving how reliably it does what was asked. When the tack is bad, even a skilled rider ends up going where the horse chose to go, which is the failure this repository exists to prevent.

Model capability improves or degrades without us and is somebody else's product. What is here is tack: the skills, protocols, and gates through which a person's intent reaches a capable system, and through which that system's state comes back legible. Every piece of it is judged on control fidelity rather than capability: can you tell where you are going, correct early, and stop.

One consequence shapes what gets accepted here. An interface is only an interface for the people who can operate it. Reins you cannot feel are not reins.

This is not a separate concern bolted onto the design. Tack already comes in many forms because riders and horses vary, and nobody treats a different bit or a different saddle as an accommodation; it is the same equipment fitted to the hands actually holding it. An interface that assumes one input method, one output channel, or one kind of attention has not been fitted to anyone. It has been fitted to an average that does not exist.

The practical result is the one every curb cut demonstrates. Fitting the interface to the widest range of operators produces something better for all of them.

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
| `commands` | Index for the seventeen-command vocabulary |

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

```
cp -r skills/* ~/.claude/skills/
```

Each skill is one `SKILL.md` and a `CHANGELOG.md`, plus an optional `references/`. They cross-reference each other by name, so copy all nine or expect broken pointers.

To symlink instead of copy, so that a `git pull` updates them in place:

```
scripts/link-skills.sh
```

Skills load on their frontmatter `description`. Read `skills/skill-discovery/SKILL.md` for how that resolution works.

## Using the orchestration protocol

`orchestration/protocol.md` defines the message flow. `orchestration/schemas/request.json` and `orchestration/schemas/response.json` are the schemas a participating agent reads and writes. `taxonomy.md` maps surfaces to behavioral regimes and is the join key for the `surface-regimes` skill.

## Packing this repo for an LLM

`repomix` collapses the whole repo into one file suitable for pasting into a model:

```
repomix --output repomix-output.xml
```

Check that the pack covers the tracked tree. The two counts should match:

```
git ls-files | wc -l
grep -c '<file path=' repomix-output.xml
```

The output is gitignored on purpose. It is a near-complete copy of the repository, so committing it roughly doubles clone size and produces a full-file diff on every change, and it goes stale silently. `repomix --remote` builds one straight from the GitHub URL without a clone.

## Contributing

Read `CONTRIBUTING.md`. It covers the rules that apply to every change, the structure a skill has to follow, and how this repo handles commit attribution.

The lowest-friction first contribution is a surface descriptor in `orchestration/registry/`. It adds support for a vendor this project does not cover yet, cannot break anyone else's traffic, and needs no knowledge of the rest of the protocol. `orchestration/registry/README.md` has the format.

`CODE_OF_CONDUCT.md` applies in every project space. `SECURITY.md` says what counts as a vulnerability in a repository that ships no service, which is narrower and stranger than the usual list; read it before filing a public issue about a gate.

## Status

Early. The skills are in daily use and the interfaces still change. The orchestration protocol has run across Claude, local models, and several vendor surfaces.

## Philosophy

See `philosophy.md`.

## License

MIT. See `LICENSE`.

`CITATION.cff` carries citation metadata for anyone referencing this work. It has no version or DOI yet; both get added at the first tagged release.
