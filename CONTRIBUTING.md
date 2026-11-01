# Contributing

toothpaste-kit is one of the kits in Bridle Works, maintained by Aidan Naveja. This covers what to read first, the rules that apply to every change, and how to submit one.

## Start here

Read `README.md` for what the project does and `philosophy.md` for why it works the way it does. Changing a skill also means reading `skills/skill-creation/SKILL.md` first, since it defines the required structure and the checklist a skill passes before it counts as live.

## Rules that apply to every change

**No em dashes in AI-generated text.** This is a hard rule. If you drafted anything here with an agent, check the output mechanically before committing:

```sh
grep -rn "$(printf '\342\200\224')" .
```

**Verify completion claims before repeating them.** When an agent reports that it wrote a file, confirm the file exists and holds what it should. An agent auditing its own work does not satisfy this.

**Use public task IDs only.** This project runs two task queues. The public one uses `TK-` ids (`TK-014`). The private queue and its open items use a phase-and-number form and an OPEN-prefixed form, spelled out in the pattern below. Neither appears in this repo. An id in the private format is a signal that private context came with it, so check what else the sentence carries:

```sh
grep -rnE '\b(P[0-9]+-[0-9]+|OPEN_[0-9]+)\b' .
```

That check must return nothing. The two formats cannot collide, so a single grep catches drift.

**Raise findings instead of quietly resolving them.** If something looks wrong or inconsistent, say so in the issue or the pull request. A unilateral fix hides the disagreement that prompted it.

More rules, all mechanical and all enforced by the checks below:

**Every `.json` in the repo must parse.**

**A registry entry must be self-consistent.** Its `regime` must equal what its `capability` derives under the rule in `orchestration/taxonomy.md`, its `id` must sit under its file's `vendor` namespace, and `confidence: verified` requires a non-empty `sources` array.

**Every `skills/*/SKILL.md` must carry `name` and `description` in frontmatter.**

**Markdown structure is checked.** `scripts/mdlint.py` enforces nineteen rules using markdownlint's own rule IDs. Four of them are accessibility rules rather than tidiness: heading structure, image alt text, descriptive link text, and table column consistency. Run it on its own while editing:

```sh
scripts/mdlint.py path/to/file.md
```

It states its own coverage in its header, including the thirty-four markdownlint rules it does not implement and why.

**markdownlint itself runs in CI, and it is not the same check.** `scripts/mdlint.py` is this project's own reimplementation, so a clean result from it is a self-audit, and the standing rule here is that a completion claim is not fact until a party other than the one making it verifies it. The `markdownlint` job in `.github/workflows/gates.yml` runs the real tool against the same rule IDs for exactly that reason. Nothing is installed at your desk to make this work, and you are not expected to run it locally. If the two ever disagree, the defect is in `scripts/mdlint.py`: report the disagreement rather than editing the document to satisfy whichever one complained. Its configuration is in `.markdownlint-cli2.jsonc`.

## Run the checks the way CI runs them

You need a POSIX shell, `bash`, `git`, `python3`, `find`, and a `grep` with `-r` and `--exclude-dir`, which GNU `grep` has. Nothing else needs installing: the gates use only the Python standard library. A `grep` without those options makes the two search gates fail rather than pass.

```sh
./scripts/gates.sh --selftest
```

That is the same script `.github/workflows/gates.yml` runs, which is the point: a check whose local copy and CI copy are separate texts can drift apart, and you find out when a clean local run is rejected by CI. It covers the mechanical rules above, including the two greps quoted earlier in this document, and these besides. It runs `scripts/reflow-md.py --selftest`. The stubs in `examples/workspace/` must match the files `docs/standing-documents.md` describes, checked by `scripts/check-workspace-stubs.py`. It runs `scripts/remote-level.sh --selftest`, so the classifier `merge-proxy` relies on still gives all three answers; `scripts/reorient --selftest`, on `examples/workspace/` as a second tree and against planted positives; and `scripts/link-skills.sh --selftest`, which links the skills into a temporary directory and checks each link. It runs `scripts/check-hooks.py`, which checks the structure and patterns of the rules in `hooks/` and that the blocking ones fire on planted commands, the branch name guard's from `tests/branch-guard-cases.tsv`; `scripts/check-branch-name --selftest`, the branch and tag name rule below; and `.githooks/commit-msg` against the trailers in `tests/attribution-cases.tsv`. It runs the selftests of `scripts/check-qblock` against `tests/qblock-cases/`, of `scripts/check-pr-body`, of `scripts/spdx-fragment.py`, and of `scripts/sbom.py`, which then runs on the tree itself. The header of `scripts/gates.sh` lists what every gate covers.

`--selftest` first shows that each gate can fire, by planting a positive and confirming the gate catches it or by running the gate tool's own selftest, then runs the real pass. A gate that has never returned a hit has not been shown capable of returning one, so a clean result on its own is weak evidence.

**What these gates do not cover**, stated because a check that does not state its coverage is not a check: en dashes, which stay a review prompt because a range and a clause separator are not mechanically separable; prose quality; internal link validity; whether a skill's closing section is last; and whether any document's claims are true.

## Compliance checks

Checks that need a tool from outside this repository run from a separate script, so the gates above keep needing nothing installed:

```sh
./scripts/compliance.sh --selftest
```

Today it runs `reuse lint`, which checks that every file declares a copyright and a licence in the form the [REUSE specification](https://reuse.software/spec-3.3/) sets out. Install the linter with `pipx install reuse==6.2.0`, the version `.github/workflows/compliance.yml` pins. Without it, the script fails and names the missing tool; `--allow-missing` reports the check as not run instead, never as passed. CI installs it and fails on any missing declaration. To run the check without installing anything, use the verification container: `containers/verify/verify . ./scripts/compliance.sh --selftest`, described in [`containers/README.md`](containers/README.md).

## Skills

One directory per skill under `skills/`, containing `SKILL.md` and an optional `references/`. Frontmatter requires `name` and `description`.

The description decides when the skill loads, so it should state what the skill covers and what it does not, with a pointer to whichever skill handles the excluded part. Skills reference each other by name, so renaming one means updating every reference. Run `grep -rn '<old-name>' skills/` before you call it done.

## Orchestration

`orchestration/protocol.md` and the JSON schemas in `orchestration/schemas/` define the message contract between agents. Changing a field means changing the schema, the protocol document, and `taxonomy.md` together, since they are read by separate agents that will not notice a partial update.

## Branch and tag names

A branch name is public the moment it is pushed, and copies of public push events persist outside the forge, so deleting a branch does not take its name back. Choose every name; never push one a tool made up. The same holds for a tag, a pull request title, a commit subject and a file name: words from a request never become one unchosen. Only branch and tag names are checked mechanically.

- A branch is `main` or `<prefix>/<words>`: a prefix from the list in `scripts/check-branch-name`, a slash, then lowercase `a-z` and `0-9` joined by single hyphens or dots, 40 characters at most. `docs/fix-typo` and `release/0.5.0` pass.
- A tag is `v<major>.<minor>.<patch>`, as `docs/releasing.md` sets out.
- Names the forge suggests, such as `<user>-patch-1` or a branch titled from an issue, are refused. The Dependabot app is exempt: the branch ruleset lets it create any branch, and the `branch-name` job exempts it on its own `dependabot/` prefix only.

Check a name before you push it:

```sh
scripts/check-branch-name docs/fix-typo
```

`scripts/check-branch-name` is the one definition. `.githooks/pre-push` runs it before anything leaves your machine, enabled by the same `git config core.hooksPath .githooks` as the commit hook below; the `branch-name` job in `.github/workflows/gates.yml` runs it on a pull request's branch; and the rulesets in `.github/rulesets/`, once the maintainer has applied them, refuse at the forge a branch outside the allowed prefixes and a tag not starting `v`; case, characters and length are checked only by the hook and the job. The rulesets cannot call a script, so `branch-names.json` repeats the prefix list, and gate 13 fails if the two differ. An agent pushes only with an explicit destination, `git push origin HEAD:refs/heads/<prefix>/<words>`; `hooks/hookify.branch-name-guard.local.md` is the example rule that holds it to that.

## Commits and pull requests

Configure `user.email` before your first commit. Use the noreply address your forge provides, not a personal mailbox. An address in a public commit log is permanent, scraped quickly, and part of the commit hash, so correcting it later rewrites history.

One logical change per commit. Commit messages should say what changed and why. Keep generated output, index databases, and packed repository files out of the repo. `.gitignore` covers the known cases.

**Record which tool helped as provenance, never as attribution.** If an assistant drafted part of a commit, add one `Assisted-by:` trailer for each assistant whose model you know, and `Agent-Effort:` where the tool reports its effort level:

```text
Assisted-by: <model> via <tool>/<version>
Agent-Effort: low | medium | high | xhigh | max
```

For example, `Assisted-by: claude-opus-5-5 via claude-code/2.1.308`. Take each value from the tool itself, never from memory. If an agent's model is not on record, leave its trailer out and say so in the pull request's Provenance section; a partial trailer reads as the whole story. A reviewer uses provenance to decide how closely to read a change, and it is where a licence question about the change would start.

No `Co-Authored-By` line naming an AI, no session links, and no generated-with footers. A co-author line claims an authorship a tool cannot certify, and the `Signed-off-by:` line is yours alone (see "Licence and sign-off"). The hook checks the forms in `tests/attribution-cases.tsv`; any other line crediting a tool is a review item.

Three layers enforce this, and only the third binds:

1. If you use Claude Code, `.claude/settings.json` in this repo sets `attribution` to empty and disables the session link. Nothing to remember.
2. A `commit-msg` hook lives in `.githooks/`. Enable it once per clone:

   ```sh
   git config core.hooksPath .githooks
   ```

   Git does not transmit hooks on clone, so this is opt-in, and `--no-verify` walks past it. Treat it as a fast local failure rather than a guarantee. The same hook refuses a commit with no `Signed-off-by:` line for its author, so a missing `-s` fails on your machine rather than in the `dco` workflow.
3. The `commit-attribution` workflow runs the same `commit-msg` hook on every commit in a pull request, with its sign-off check off since the `dco` workflow holds that, so the two cannot disagree. It is the layer that binds: it is set as a required status check in the ruleset on `main`, as read from the rulesets API on 2026-10-30. On a fork, it binds only once that fork's maintainer sets the same; without that setting it reports a failure and blocks nothing. Where it is required, a branch that reaches review with a trailer in its history needs those messages rewritten and the branch force-pushed.

Human co-author trailers are fine and expected. The rule is about tools.

## Licence and sign-off

Contributions are licensed under the Apache License 2.0, the project's licence ([`LICENSE`](LICENSE)). No contributor licence agreement, copyright assignment or indemnity is asked of you.

Every file declares its copyright and licence. A new file carries an `SPDX-FileCopyrightText` and an `SPDX-License-Identifier` line, at the top in a comment, or at the end in an HTML comment for Markdown so the frontmatter and first heading stay first. A file that cannot hold a comment, such as JSON, is covered in [`REUSE.toml`](REUSE.toml) instead. `reuse annotate` writes the header for you; `./scripts/compliance.sh` checks it.

Sign off every commit. A sign-off certifies the [Developer Certificate of Origin](https://developercertificate.org/), version 1.1: that you have the right to submit the work under the project's licence.

```sh
git commit -s
```

`-s` adds a `Signed-off-by:` line with your `user.name` and `user.email`. It is your certification, not a cryptographic signature (that is `-S`), and not acceptance: a signed-off contribution is still reviewed, and may be declined. The `dco` workflow fails a pull request containing a commit with no `Signed-off-by:` line for its author's email. Bot accounts are exempt.

To add a missing sign-off, amend the last commit, or rebase every commit on the branch onto `main`, then force-push the branch:

```sh
git commit --amend -s --no-edit
git rebase --signoff main
```

**If someone other than you may own the work**, such as an employer or a client, say so in the pull request. Review pauses until that owner's authorization is documented, since your sign-off cannot stand in for it.

## Hook rules

`hooks/` holds `hookify` rules as examples. They are inert where they sit and do nothing until copied into a `.claude/` directory.

A rule is one `.local.md` file: YAML frontmatter defining the match, then a Markdown body that is shown to the agent when it fires. The body is the part that matters. A rule that blocks without explaining why gets worked around or disabled, so the body should name what tripped, why the rule exists, and what to do instead. Several rules here cite the specific failure that motivated them for that reason.

Adding one:

- `action: block` stops the tool call. `action: warn` lets it through and adds a notice. Reach for `warn` unless the thing being prevented is unrecoverable. The read notices here warn, because reading sensitive material is normal work and the thing worth catching is what happens afterward.
- Match on command position, not bare substrings, for anything matching shell commands. A rule that fires on a tool name inside a quoted heredoc makes writing documentation about that tool impossible.
- Give the rule a false-positive escape and say what it is. If a contributor cannot get legitimate work past a rule, they will disable it, and a disabled rule protects nothing.
- Exempt by filename, not by weakening the pattern. One rule here, `hookify.em-dash-gate.local.md`, exempts files that must quote the thing it forbids.
- State the rule's limits in its own body. Every pattern-based rule has ways around it. Saying so is what keeps it from being mistaken for a boundary.

Test a rule against three cases before adding it: something that must trip it, something legitimate that must not, and the rule's own documentation.

## What does not belong here

Operational and business material lives outside this repository entirely and is never committed to it. Anything that names a client, an internal process, or a person's private details is out of scope for this repo regardless of where you found it. If you cannot tell which side of that line something falls on, ask before pushing.

## What kind of writing goes in this repo

Docs here are written for a person with a task. State what a thing does, how to use it, and what it does not cover. Outside the exceptions below, skip the archaeology: which options were weighed, what a previous version got wrong, how the decision felt at the time.

That material is kept, in a separate provenance layer outside this repository. `docs/document-layers.md` states the rule and the tests for applying it. Three exceptions live here on purpose: a skill's `CHANGELOG.md` records why that skill is shaped the way it is, because a later editor needs it to avoid silently undoing a deliberate choice, the repository's `CHANGELOG.md` records what changed, and a reflection entry in `docs/reflections/` restates what one documentation row records, including a correction, in the fixed format of `docs/document-layers.md` exception 5. None is a session log.

Practical test before you commit a doc: could a contributor who has never spoken to the maintainers act on it? If a sentence only makes sense to someone who was in the room, it belongs in the provenance layer.

## Questions

Ask. A question costs less than a wrong assumption acted on.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
