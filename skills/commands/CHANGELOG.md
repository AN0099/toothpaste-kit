# CHANGELOG

## v2

Removed a Routing section that described a mechanism this repository never contained. It stated
that sixteen of the seventeen commands resolved to dedicated files under `skills/commands/`, and
gave `commands/AUDIT.md` as the worked example. No such file has existed in any commit. An agent
following that instruction was sent to read a path that does not resolve.

Two fixes were available: write the sixteen files, or delete the claim and name the place the
definitions actually live. This build takes the second. `working-preferences` already carries the
full command vocabulary and the session-state semantics for FREEZE, FLAG, and RETRACT, so the
sixteen files would have duplicated it, and a duplicated definition drifts from its original
without anything detecting the drift.

The consequence worth preserving: if a command needs more depth than an index line, that depth
belongs in `working-preferences` next to the rest of its definition. Adding per-command files
under this directory would reintroduce the split this entry closes.

Also renamed the closing section from `# Cross-References` to `# Scope Pointer`. That is one of the
two heading names `skill-creation` permits in a closing position, and this file used a third.

## v1 (initial generation)

Index of the seventeen-command vocabulary, built so an agent can see which commands are active
without loading `working-preferences` in full. Shipped without a `CHANGELOG.md`, which
`skill-creation`'s pre-publish checklist requires of every skill. This file closes that gap
retroactively; the v1 entry is reconstructed from the file as shipped rather than from a record
kept at the time.
