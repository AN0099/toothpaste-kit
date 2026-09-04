---
name: redaction-gate
description: Run the pre-publish redaction pass before content crosses a sensitivity tier boundary outward, such as a vendor API call, a Git commit, a repomix pack, or a handoff to an agent on another account. Checks candidate output against the local restricted corpus.
disable-model-invocation: true
---

# Redaction Gate

**Adapting this skill:** filenames below name roles in a document set rather than
literal paths. `docs/standing-documents.md` describes that set, what each file
does, and the tier scheme this procedure assumes. Read it once and the pointers
resolve; substitute your own filenames freely.

Run this before anything crosses a tier boundary outward. The governing rule in
`CLAUDE.md` is that the pass must actually run and actually be checked, never
assumed to have happened already, and that it applies even to Public-tier output
that was derived from higher-tier material.

Take one argument: the path or description of the candidate content. If none was
given, ask what is being published and where it is going before proceeding.

## Step 1: Establish direction and destination

Name the source tier and the destination explicitly. The gate applies to
outward movement. Common destinations, all of which count:

- A commit or push into any Git working tree
- A repomix pack intended to leave this machine
- A vendor API call, including a sub-agent running on a different account
- A document handed to a person outside the tier's audience
- Any published artifact or page

If the destination is inward (a vendor response arriving with something
sensitive in it), stop and say so. Whether this gate covers the inbound
direction is an open question in `agents/claude/lead-handoff.md`, not a settled
rule, and it is not this skill's job to settle it unilaterally.

## Step 2: Build the check corpus

Derive the match terms from the local restricted material, not from memory and
not from a list hardcoded in this file. A hardcoded list of sensitive terms
would itself be a sensitive artifact sitting in an unprotected location.

Read the restricted tier and the sensitive-material inventory, and assemble:

- Named entities: people, companies, working titles, product names
- Identifiers: account names, hostnames, network topology, device names
- Credential shapes: key prefixes, token formats, anything matching the
  credential patterns already enumerated in `.gitignore`
- Reasoning fragments: strategic rationale that is restricted regardless of
  whether any name appears alongside it

## Step 3: Check the candidate

Match the candidate content against the corpus. Report every hit with its
location and the tier of the material it matched.

Then apply the content-depth principle, which catches what a term match cannot.
Public and Internal carry almost nothing sensitive regardless of audience width,
because the concern there is optics rather than access. Confidential carries
operational behavior with entities abstracted into categories. Only Restricted
carries actual reasoning and real named entities.

So ask the question a term list cannot answer: **does this text reveal the
reasoning behind a decision, even with every name removed?** If yes, it is
Restricted content in disguise and moving it downward requires stripping the
reasoning, not just the names.

Check the register as well. The antithetical "X, not Y" construction and
self-narrating asides tend to arrive together with decision archaeology. Their
presence is a signal that provenance material has leaked into a human-facing
document.

## Step 4: Report and hand off the decision

Produce a findings list: each hit, its tier, and a specific proposed redaction.

Do not perform the outward action. Do not describe the content as cleared.
Confirmation authority for anything sensitive is shared with the human, not
held by any agent alone. Present the analysis and a recommendation, and let the
human make the call in dialogue.

If the pass found nothing, say that it found nothing and note what it could not
check. A clean result from a mechanical pass is not clearance to send. Credential
scanners in general miss a substantial share of what they are pointed at, so a
passing scan is one input to the decision rather than the decision itself.
