# Concepts

A map from each idea a contributor needs to the documents that carry it. Each
idea gets one sentence, then every file that carries it, deepest first. Terms
with an entry in the [glossary](glossary.md) are linked there and not defined
again.

## Checking work

- **Nobody certifies their own work.** A completion claim counts as fact only after a different party has run the check. Deepest first: [the interaction manual](interaction-manual.md#4-nobody-self-certifies), [control layers](control-layers.md#where-the-human-sits), [the aide role](../orchestration/roles.md#aide), [the security posture checks](security-posture.md#4-automated-checks), [contributing](../CONTRIBUTING.md#rules-that-apply-to-every-change), [governance](../GOVERNANCE.md#how-a-change-lands), [the verify lane](../skills/daily-review/SKILL.md#the-lanes). Glossary: [verified](glossary.md#v), [verify lane](glossary.md#v).
- **A check must be shown able to fail.** A clean result means nothing until the same check has caught an input built to trip it. Deepest first: [the gate script](../scripts/gates.sh), [contributing](../CONTRIBUTING.md#run-the-checks-the-way-ci-runs-them), [the tests page](../tests/README.md), [the example workspace rules](../examples/workspace/CLAUDE.md), [the interaction manual](interaction-manual.md#4-nobody-self-certifies). Glossary: [planted positive](glossary.md#p), [selftest](glossary.md#s), [coverage line](glossary.md#c).
- **Local and CI run one script.** Two copies of a check drift apart, so the desk and the pipeline share the same text. Deepest first: [the gate script](../scripts/gates.sh), [contributing](../CONTRIBUTING.md#run-the-checks-the-way-ci-runs-them), [the security posture](security-posture.md#4-automated-checks). Glossary: [gate](glossary.md#g).
- **Orientation goes stale, so re-read before acting.** A reading taken earlier in a session is not the present state, and acting on it is fast and wrong. Deepest first: [control layers on tempo](control-layers.md#tempo-the-ooda-loop), [the orient skill](../skills/orient/SKILL.md), [the interaction manual](interaction-manual.md#4-nobody-self-certifies). Glossary: [OODA loop](glossary.md#o).

## Writing and documents

- **Two layers, never mixed in one file.** Reasoning and history live in one layer and results in another, so each reader gets the file they came for. Deepest first: [document layers](document-layers.md#documentation-and-provenance), [standing documents](standing-documents.md#the-organizing-principle), [the interaction manual](interaction-manual.md#9-two-layers-never-mixed), [contributing](../CONTRIBUTING.md#what-kind-of-writing-goes-in-this-repo), [the example workspace rules](../examples/workspace/CLAUDE.md). Glossary: [documentation](glossary.md#d), [provenance](glossary.md#p), [human-facing](glossary.md#h).
- **Rules are checked by machine where a machine can.** The em dash ban is enforced by a gate, and its known gap is stated beside it. Deepest first: [the gate script](../scripts/gates.sh), [the em dash hook rule](../hooks/hookify.em-dash-gate.local.md), [contributing](../CONTRIBUTING.md#rules-that-apply-to-every-change), [the session-close skill](../skills/session-close/SKILL.md).
- **Partial records never pose as full ones.** A short capture is marked so a later reader cannot mistake a pile of them for a completed close. Deepest first: [partial captures](partial-captures.md#a-partial-capture-never-reads-as-a-full-one), [the jot skill](../skills/jot/SKILL.md), [the touch skill](../skills/touch/SKILL.md). Glossary: [partial capture](glossary.md#p).

## Authority and containment

- **A repository's remote sets what an agent may do, and a person merges.** The classifier reads where remotes point and the answer bounds the agent, with trunk merges reserved to a person. Deepest first: [the level script](../scripts/remote-level.sh), [the merge-proxy skill](../skills/merge-proxy/SKILL.md), [growing the workspace](installing.md#growing-the-workspace), [the README scripts section](../README.md#scripts), [governance](../GOVERNANCE.md#how-a-change-lands). Glossary: [level](glossary.md#l), [trunk](glossary.md#t), [merge-proxy](glossary.md#m).
- **Physical separation beats a filter.** The strongest control is a layout in which the failure cannot be reached, with pattern-based guards kept only as backstops. Deepest first: [control layers](control-layers.md#1-inherent-design-make-the-failure-impossible), [standing documents on tiers](standing-documents.md#sensitivity-tiering), [the egress guard hook rule](../hooks/hookify.restricted-egress-guard.local.md). Glossary: [inherent design](glossary.md#i), [containment](glossary.md#c), [sensitivity tier](glossary.md#s).
- **Automate what fails by inattention, keep a person on what fails by novelty.** The split follows the failure mode and not the importance of the task. Carried by [control layers](control-layers.md#where-the-human-sits) alone. Glossary: [alarm](glossary.md#a), [interlock](glossary.md#i).
- **A dependency's origin depends on the zone it runs in.** Code a contributor executes at their desk has a stricter source rule than code that runs only in CI. Deepest first: [the security posture on dependencies](security-posture.md#7-where-a-dependency-is-allowed-to-come-from), [the workflow gates](../.github/workflows/gates.yml), [the mdlint header](../scripts/mdlint.py).

## Interaction design

- **Design the interface around which hands do the work.** Input conventions are chosen against stated physical constraints, and the assumption of two hands is made visible. Deepest first: [accessibility](accessibility.md#5-keystroke-volume), [the interface contract](interface-contract.md#3-the-brevity-code-and-the-constraint-that-shaped-it), [the interaction manual](interaction-manual.md#6-price-the-input), [the merge-proxy skill](../skills/merge-proxy/SKILL.md). Glossary: [brevity code](glossary.md#b), [answer grammar](glossary.md#a).

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
