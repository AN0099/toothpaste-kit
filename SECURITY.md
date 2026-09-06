# Security

## What counts as a vulnerability here

This repository ships documents, JSON schemas, two scripts, and example hook rules. It runs no
service and holds no user data, so the usual web-application categories mostly do not apply.

What does apply:

- **A gate that fails open.** `redaction-gate` and the hook rules exist to stop content from
  crossing a boundary. A pattern that silently misses a case it claims to catch is the highest
  severity defect this project can have, because the failure is invisible to the person relying on
  it. The v2.1 fix to `redaction-gate` is the worked example: the published skill was weaker than
  its own documentation for a period, and anyone running it had less protection than they believed.
- **A skill or hook that leaks.** A rule whose body, error text, or example quotes material it was
  meant to keep out.
- **A script defect with a destructive path.** `scripts/` writes to files. A bug that corrupts input
  rather than refusing it belongs here.
- **A protocol defect that defeats auditability.** A schema or rule change that makes a relay hop
  untraceable, or that lets an edited payload pass as an unedited one.

Out of scope: the behavior of any model vendor's product, the models themselves, and anything about
a deployment that this repository does not describe.

## Reporting

Use GitHub's private vulnerability reporting on this repository: the Security tab, then "Report a
vulnerability." That channel is private to the maintainer and does not create a public issue.

If private reporting is unavailable to you, or you would rather not use GitHub, email
`an0099+security@proton.me`. It reaches the same person. It is a fallback rather than the preferred
channel, so send enough to establish that a defect exists and expect the detail to move into a
private advisory.

Do not open a public issue for anything in the first category above. A pattern gap is directly
actionable by anyone who reads it, and this project has no release channel through which to ship a
fix ahead of disclosure.

Include what you were doing, what you expected the control to do, and what it did instead. A
reproduction that a maintainer can run is worth more than a description.

## What to expect

An initial response within seven days. This is a small project without a paid on-call rotation, and
a promise it can keep is worth more than one it cannot.

If a report is accepted, the fix and an explanation of what was wrong go into the affected file's
`CHANGELOG.md`, because a later editor needs to know why a pattern is shaped the way it is.
Reporters are credited unless they ask not to be.

## Supported versions

`main` only. This project has no version numbering scheme yet, so there is no earlier release to
patch. See `docs/project-state.md`.

## What this project does not promise

The hook rules and the gates are pattern-based. Every pattern-based control has ways around it, and
each rule's own body says so. They raise the cost of a mistake and they do not constitute a
boundary. Treat them as instrumentation rather than as enforcement.
