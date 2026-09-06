# Surface Registry

A surface descriptor answers one question: what can this vendor's product actually do. The
orchestration protocol reads the answer, never the product name.

`schemas/event-base.json` requires `capability` and `regime` on every agent reference. `surface` is
a label that resolves here. That ordering is deliberate: capability is what every routing and
gating decision consults, and product names are the part that changes without warning.

## Files

- `surface-descriptor.schema.json` validates every vendor file in this directory.
- `anthropic.json`, `openai.json`, `google.json`, `local.json`: one file per vendor namespace.
  Three of those are empty and waiting for someone who uses them.

## Adding a surface

Open a pull request that adds one entry to the vendor file, or adds a new vendor file. A new file
needs a `vendor` namespace and a `surfaces` array, nothing else.

Every entry carries seven capability fields, a derived regime, and its own evidence:

```json
{
  "id": "vendor:surface-name",
  "display_name": "Human-readable name",
  "capability": {
    "interface": "conversational | programmatic",
    "autonomy": "none | redirectable | full",
    "human_presence": "required | optional | absent",
    "workspace": "none | session | local | remote",
    "tool_execution": "none | sandboxed | host",
    "egress": "local | operator-hosted | vendor-cloud",
    "audit": "none | local-only | vendor-attested | operator-attested | unknown"
  },
  "regime": "derived, see below",
  "confidence": "verified | derived | unverified",
  "verified_on": "YYYY-MM-DD",
  "sources": ["https://..."],
  "notes": "Which fields are shaky, and why."
}
```

## Deriving `regime`

Three clauses, first match wins:

1. `interface` is `programmatic` and `autonomy` is `none`, then `programmatic-contractual`.
2. `human_presence` is `required`, then `interactive-synchronous`.
3. Otherwise, `autonomous-asynchronous`.

The rule is stated in full in `../taxonomy.md`, which also shows it reproducing every row of the
capability matrix it was extracted from. Record the result in the entry anyway, so a checker can
compare the stated regime against the derivation and catch an entry that drifted.

## Evidence fields are not optional decoration

`confidence`, `verified_on`, and `sources` exist because a registry describing products that ship
weekly is a collection of claims about the past unless each claim carries its own date.

- `verified` means every capability field was checked against a cited source on `verified_on`.
  `sources` must be non-empty.
- `derived` means the fields were inferred from observed product behavior with no citation
  recorded. An empty `sources` array is permitted.
- `unverified` means the entry was imported and not checked.

Use `unknown` for an `audit` value you cannot establish. An honest `unknown` is more useful than a
confident guess, and `anthropic:cowork-interactive` carries one today for exactly that reason.

## What does not belong here

An operator's own roster of models, endpoints, and quotas is local configuration. This registry
describes what a product can do, and says nothing about which products any particular operator has
access to.
