# Governance

How decisions get made here. "One maintainer decides" is a
governance model and an unwritten one is indistinguishable from no model at all.

Last reviewed 2026-09-17.

## Who decides

**One maintainer.** Aidan Naveja, named in `LICENSE` and `CITATION.cff`. There is
no committee, no vote, and no independent body to escalate to. Saying otherwise
would describe a process that does not exist, which is worse than the honest
version for anyone deciding whether to depend on this project.

Copyright rests with the individual authors, currently that one person. Bridle
Works is the name of the project this kit belongs to and is not a formed entity,
so it holds nothing.

**Bus factor is one, and the succession plan below is explicit rather than
assumed.** See [Succession](#succession) below. Until a second maintainer
accepts, the fallback remains a fork: the licence permits it, every design
decision is recorded in a `CHANGELOG.md` beside the file it concerns, and
nothing here depends on infrastructure only the maintainer can reach.

## How a change lands

1. **Discussion first for anything that changes an interface.** A skill's
   frontmatter, the orchestration message schema, or a documented rule. Open an
   issue before the pull request, because the disagreement is the useful part and
   a finished branch makes it expensive to have.
2. **A pull request for everything else**, including maintainer changes, so the
   mechanical gates run against it.
3. **The gates must pass.** `scripts/gates.sh` is the same text CI runs. A gate
   failure is not advisory.
4. **The maintainer merges.** No self-merge rule applies, because with one
   maintainer a self-merge ban would stop all work rather than add review.

**A completion claim is verified by someone other than the person making it.**
That rule is in `CONTRIBUTING.md` and it governs review here too: the maintainer
reviewing their own agent's output is not verification, and a review that only
re-reads the diff is not verification either. Where a change claims a check
passes, the reviewer runs it.

## What is deliberately not delegated

- **Merges into the default branch.** A commit records what was done; a merge
  says this is now shared truth, which is a decision.
- **Tags and releases**, for the same reason, plus the fact that a tag is what
  other people pin to.
- **Anything that publishes**, including a push to this repository's remote.
  Automated agents contribute by editing and staging; a person commits and
  pushes.

That last one is not a style preference. This project is developed with AI
agents doing a large share of the editing, and the boundary between an agent
preparing a change and a person publishing it is the main control that keeps
review meaningful.

## Succession

Named as its own section because "bus factor" is a criterion a reviewer checks,
and because the honest answer to it today is one person.

**Status: a second maintainer is proposed and has not accepted.** Nobody is
named here as a maintainer until they have agreed in writing, because listing a
person as responsible for a project without their consent is a claim about them
rather than about the project. The proposal is recorded in the maintainer's own
notes; this document is updated when there is an acceptance to record.

**What a successor needs, listed so it can be prepared rather than discovered:**

| Needed | State today |
|---|---|
| Commit access to the repository | Held by one account |
| Ability to publish a release | Same account, and no signing key is configured yet |
| The private vulnerability reporting inbox | Reaches one person, per `SECURITY.md` |
| The conduct reporting address | Reaches the same person, per `CODE_OF_CONDUCT.md` |
| Knowledge of why the design is shaped this way | In `philosophy.md` and in a `CHANGELOG.md` beside each file |
| Knowledge of what is unfinished | In `docs/project-state.md` and `docs/security-posture.md` |

The last two rows are the reason this project writes reasoning down beside the
thing it concerns. A successor who inherits the files inherits the argument for
them, which is the part a handover usually loses.

**The gap that consent does not close:** the two reporting addresses route to
one person. A second maintainer who cannot receive a report about the first
maintainer is not an escalation path. `CODE_OF_CONDUCT.md` already asks a
reporter to name a third party they would accept, which is the interim answer
and not the permanent one.

## Becoming a maintainer

A sustained record of accepted contributions, agreement on the project's
judgment criterion (control fidelity, see `philosophy.md`), and the current
maintainer's decision. Then a written acceptance, then this document changes.

That order matters: the acceptance comes before the listing, not after.

## Changing this document

Same path as any other change, with one addition: a change to the decision
process is announced in `CHANGELOG.md` at the repository level, not only in a
commit message, because people depending on the project cannot be expected to
read commit history to discover that the rules moved.

## Security decisions

`SECURITY.md` owns the reporting channel and the response commitment.
Vulnerability triage is the maintainer's, and the one standing constraint is
that a gate that fails open is treated as the highest severity class this
project has, because that failure is invisible to whoever is relying on it.
