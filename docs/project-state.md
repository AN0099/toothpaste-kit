# Project State

Current status of toothpaste-kit. For what the project is and how to use it, start with
`README.md`.

Last updated 2026-09-02.

## Live

Seven skills, all in daily use:

`working-preferences`, `document-standards`, `technical-documents`, `surface-regimes`,
`skill-creation`, `skill-discovery`, `commands`.

The orchestration protocol has run relay traffic across Claude, local models, and several vendor
surfaces. Message schemas and the role taxonomy are stable enough to build against.

## In progress

Two skill families are specced and not yet built:

- **reference-architecture**: governs how specific a technical document can be before it stops
  being safe to publish.
- **content-pipeline**: note-mining, public-writing register, and publishing workflow.

## Recent changes

- The `lib-*` reference-library toolchain moved out of this repo. It served the maintainer's
  personal knowledge base rather than the kit, and now lives alongside that.
- `README.md`, `CONTRIBUTING.md`, and `philosophy.md` were rewritten. The old versions carried
  operational detail that belonged elsewhere and pointed at files this repo does not contain.

## Known gaps

- No test suite. Skills are validated by use and review.
- No versioning scheme across the skill set. Individual skills carry their own `CHANGELOG.md`.
- Skill interfaces still change without deprecation notice.

## Open questions

- Whether `commands` should split, since the seventeen-command vocabulary has grown informal
  extensions that were never audited against the original set.
- Whether skills should declare version compatibility with each other, given how often they
  cross-reference by name.
