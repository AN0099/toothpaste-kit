# toothpaste-kit

**[CURRENT WORK IN PROGRESS // PRE-ALPHA]**

A skill library and agent relay protocol for working with Claude. Judged on control fidelity: legible state, cheap correction, a reliable halt.

Maintained by Bridle Works.

## Why this exists

The "centaur" analogy of automation theory imagines a human-machine collaboration where a person uses technology as a powerful, tireless assistant to execute tasks while retaining ultimate control over judgment and decision-making: a human orchestrator directing an automated agent, each unable to complete the work without the other. The reverse-centaur inverts the roles. An automated orchestrator directs a human agent, the person in the loop only because the machine has no fleshy appendages of its own to do the work.

The analogy holds best with deterministic automated systems, computers and machines where the same input produces the same output every time and 1 + 1 is always 2. Such systems have no will of their own to negotiate with. Applied to a non-deterministic system the centaur gets portrayed as one organism, and it will not be one until human and machine are literally fused. More accurately, what you have is a rider and a horse: two wills, one of them in charge, joined by riding tack.

The tack is the interface. A rider does not think the horse forward. They apply pressure through equipment, the horse interprets it, and the result depends almost entirely on the quality of that equipment and the operator's skill. The horse acts non-deterministically, and retraining it is not on the table, so tack and skill are the only levers left for improving how reliably it does what was asked. When the tack is bad, even a skilled rider ends up going where the horse chose to go, which is the failure this repository exists to prevent.

Model capability improves or degrades without us and is somebody else's product. What is here is tack: the skills, protocols, and gates through which a person's intent reaches a capable system, and through which that system's state comes back legible. Every piece of it is judged on control fidelity rather than capability: can you tell where you are going, correct early, and stop.

One consequence shapes what gets accepted here. An interface is only an interface for the people who can operate it. Reins you cannot feel are not reins.

This is not a separate concern bolted onto the design. Tack already comes in many forms because riders and horses vary, and nobody treats a different bit or a different saddle as an accommodation; it is the same equipment fitted to the hands actually holding it. An interface that assumes one input method, one output channel, or one kind of attention has not been fitted to anyone. It has been fitted to an average that does not exist.

The practical result is the one every curb cut demonstrates. Fitting the interface to the widest range of operators produces something better for all of them.

## What is here

### `skills/`

Nine skills, in two classes.

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

Two are procedures a person invokes. Both set `disable-model-invocation`, so an agent cannot trigger them. That is the point in each case: a gate a model can invoke to satisfy itself is not a gate, and an agent should not decide that a session is over.

| Skill | Runs |
|---|---|
| `redaction-gate` | Before content crosses a sensitivity boundary outward. Reports findings, hands the decision to a person |
| `session-close` | At the end of a working session. Captures reasoning that exists nowhere on disk, then updates the standing documents |

### `docs/`

`docs/standing-documents.md` describes the document structure that `redaction-gate` and `session-close` assume: what each standing file does, how they work together, and the sensitivity tiering the redaction procedure depends on. Read it if either skill's pointers look like they lead nowhere.

`docs/project-state.md` is where the kit itself stands.

### `hooks/`

Seven `hookify` rules, as examples rather than live configuration. Copy the ones you want into your own `.claude/` directory; they do nothing where they sit.

Two block (a forbidden character in generated content, and a packing command without an allow-list). The rest warn on reads that pull sensitive material into context, so a later publish step knows the session is derived from it. They assume a tiered directory scheme; adapt the patterns before enabling them.

### `scripts/`

`link-skills.sh` symlinks `skills/` into your Claude skills directory instead of copying, so `git pull` updates them in place.

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

## Status

Early. The skills are in daily use and the interfaces still change. The orchestration protocol has run across Claude, local models, and several vendor surfaces.

## Philosophy

See `philosophy.md`.

## License

MIT. See `LICENSE`.
