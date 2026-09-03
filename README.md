# toothpaste-kit

**[CURRENT WORK IN PROGRESS // PRE-ALPHA]**

A skill library and agent relay protocol for working with Claude.

Maintained by Bridle Works.

## What is here

### `skills/`

Seven skills that govern agent behavior.

| Skill | Covers |
|---|---|
| `working-preferences` | Standing defaults, register, correction protocol, command vocabulary |
| `document-standards` | Writing standards for generated documents, with formality, density, and audience dials |
| `technical-documents` | Presets for runbooks, postmortems, ADRs, and handoff notes aimed at ops readers |
| `surface-regimes` | Detects whether a session is interactive, autonomous, or programmatic, and sets dials to match |
| `skill-creation` | Naming, required structure, and checklists for adding a skill |
| `skill-discovery` | Whether a recurring need is worth a skill, and finding one that already exists |
| `commands` | Index for the seventeen-command vocabulary |

### `orchestration/`

The protocol for passing work between agents on different surfaces.

| File | Holds |
|---|---|
| `orchestration/protocol.md` | The relay protocol itself |
| `orchestration/taxonomy.md` | Role and surface definitions |
| `orchestration/request.json` | Request message schema |
| `orchestration/response.json` | Response message schema |
| `orchestration/ingestion/` | Specs for turning vendor data exports into machine-readable digests |

## Installing the skills

Copy the directories under `skills/` into your Claude skills directory:

```
cp -r skills/* ~/.claude/skills/
```

Each skill is one `SKILL.md` plus an optional `references/`. They cross-reference each other by name, so copy all seven or expect broken pointers.

Skills load on their frontmatter `description`. Read `skills/skill-discovery/SKILL.md` for how that resolution works.

## Using the orchestration protocol

`orchestration/protocol.md` defines the message flow. `request.json` and `response.json` are the schemas a participating agent reads and writes. `taxonomy.md` maps surfaces to behavioral regimes and is the join key for the `surface-regimes` skill.

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

The output is gitignored on purpose. It is a near-complete copy of the repository, so committing it
roughly doubles clone size and produces a full-file diff on every change, and it goes stale
silently. `repomix --remote` builds one straight from the GitHub URL without a clone.

## Status

Early. The skills are in daily use and the interfaces still change. The orchestration protocol has run across Claude, local models, and several vendor surfaces.

## Philosophy

See `philosophy.md`.

## License

MIT. See `LICENSE`.
