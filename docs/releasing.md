# Versioning and releases

**One version for the whole kit, semantic versioning, cut as
an annotated git tag.** This unblocks three things that were all waiting on the
same absence: an OpenSSF Best Practices Badge, which requires unique version
numbering and per-release notes; a Zenodo DOI, which needs a tagged release; and
a vulnerability report, which needs a version to be reported against.

## The scheme

`MAJOR.MINOR.PATCH`, applied to the repository as a whole.

- **MAJOR**: a breaking change to something another project can depend on. The
  orchestration message schema, a skill's frontmatter `name`, or the removal of
  a skill.
- **MINOR**: a new skill, a new orchestration field that is optional, a new
  gate, or any addition that leaves existing usage working.
- **PATCH**: corrections, wording, and fixes that change no interface.

**Skills keep their own `CHANGELOG.md`.** Those stay the place design reasoning
lives, and they are the detail behind a release rather than a competing version
number. A skill does not carry its own version string. The reason is that skills
here reference each other by name and are loaded as a set, so a reader needs to
know which set they have, not a list of independent numbers.

**Pre-1.0 means the interfaces still move.** While MAJOR is 0, a MINOR bump may
break something, which is what 0.x is for. `README.md` says pre-alpha and that
stays true until the schema stops changing.

## What a release is

A tag, release notes, and nothing else. There is no build artifact, no package
and no installer, because the kit is documents and two scripts. `scripts/link-skills.sh`
is how it gets used, and it reads the tree it sits in.

## Cadence

**A release review every two weeks, on a Tuesday, and a release only when the
review admits one.** Counted from 0.3.0 on Tuesday 2026-09-29, so the next
review is Tuesday 2026-10-13.

- **The Friday before is the cutoff.** No new scope enters the release. The
  release notes, citation fields and redaction result are assembled, and the
  maintainer decides to go to Monday's review, defer, split the scope, or
  abandon it. The weekend is buffer, never planned work.
- **Monday is the final review** of the exact commit that will be tagged.
- **Tuesday, late morning, is the release**: tag, GitHub release, Zenodo.
  Wednesday to Friday are for watching it and correcting it.

**A release is not owed because the date arrived.** Each published release mints
a permanent Zenodo version DOI, so a review that finds nothing coherent to
archive defers. **A PATCH release may land between reviews** only for a
material defect in a published release: a broken primary workflow, a security
or safety correction, or wrong citation, licence or DOI metadata.

Two weeks suits a pre-alpha project with one maintainer, where momentum
matters more than ceremony. The cadence is itself reviewed as the project
matures; a four-week cycle is the expected next step once there are more
contributors to coordinate.

## Cutting one

Every step below is the maintainer's. An agent may prepare the edits and stage
them; it does not commit, tag or push, and `GOVERNANCE.md` says why.

1. **Gates pass on the commit being tagged.**

   ```sh
   ./scripts/gates.sh --selftest
   ```

2. **Write the release notes** as a dated section at the top of the repository
   `CHANGELOG.md`, under the version number. Added, Changed, Fixed, Removed.
   Draw on the per-skill `CHANGELOG.md` files for detail rather than repeating
   them wholesale.

3. **Set `version` and `date-released` in `CITATION.cff` in the tree that gets
   tagged.** They go in on the release branch before the merge, so the merge
   commit the tag points at carries them. For example:

   ```yaml
   version: 0.2.0
   date-released: 2026-09-26
   ```

   The date also heads the release's `CHANGELOG.md` section. If the tag is cut
   on a different day, change both before the release commit.

   `identifiers` lists only the concept DOI and does not change per release.
   Add the previous release's version DOI to "Where releases stand" below, in
   this same release branch (step 7 says why it waits until now).

4. **Check `SECURITY.md`'s "Supported versions".** Since 0.1.0 it says the
   latest release and `main`, which is the honest answer for a one-maintainer
   project. Change it only if that stops being true.

5. **Tag, annotated and signed.** A signing SSH key is registered on the
   account, so the tag is signed rather than merely annotated:

   ```sh
   git tag -s v0.2.0 -m "toothpaste-kit 0.2.0"
   git push origin v0.2.0
   ```

   GitHub marks the tag Verified when the key is registered as a **signing**
   key, which is a separate setting from the same key as an authentication key.
   Local verification of a signed tag needs an allowed signers file:

   ```sh
   git config gpg.format ssh
   git config user.signingkey ~/.ssh/<key>.pub
   git config gpg.ssh.allowedSignersFile ~/.ssh/allowed_signers
   git tag -v v0.2.0
   ```

   Without `allowedSignersFile`, `git tag -v` reports that it cannot check the
   signature, which is not the same as a bad signature.

   **Expect exactly one commit per release that does not verify locally, and
   expect it to be the merge.** Merging through the web interface produces a
   merge commit carrying GitHub's signature rather than the maintainer's, which
   is what satisfies `required_signatures` without a signing key configured on
   the merge step. `git log --format=%G?` reports `E` on it, meaning an unknown
   signer, while the API reports `verified=true`. Both are correct and they are
   about different signers: the maintainer's authorship survives in the signed
   commits inside the merge, and the merge commit attests only that an
   authenticated account with permission performed it. The trust anchor for that
   one commit is the forge. This is written down so the result is expected
   rather than rediscovered, the same reason a check states its coverage before
   its clean result is trusted.

6. **Create the GitHub release** from that tag, pasting the `CHANGELOG.md`
   section as the body. Publish it rather than saving a draft: the Zenodo
   webhook fires on a published release.

7. **Record the version DOI in the next release, not in a pull request of its
   own.** The Zenodo integration is enabled, and it mints from the GitHub
   release webhook in step 6, so the DOI does not exist until that step
   completes. It issues a concept DOI covering every version, which always
   resolves to the newest, and a per-version DOI. Cite the concept DOI: it is
   the only DOI in `CITATION.cff`, so that file is right the moment the tag is
   cut and needs no change after it. The version DOI is found on the Zenodo
   record until the next release branch writes it under
   "Where releases stand" (step 3). The release branch also adds its own line
   there, since it merges on the day the tag is cut.

8. **Release badges in `README.md`.** Added at 0.1.0; a later release leaves
   them as they are. Four, on the badge line after the `gates` and licence
   badges:

   - the Zenodo concept DOI badge, linking to the concept DOI
   - the Software Heritage archive badge, linking to the archived origin
   - the OpenSSF Best Practices badge, once the questionnaire is submitted
   - the latest release badge, linking to the releases page

   Each badge is wrapped in a link, and each carries alt text that names what
   it indicates rather than its current value, because the image is served by
   a third party and its value changes while the alt text does not. A badge
   whose subject has no row in `docs/security-posture.md` does not belong in
   the README.

## Where releases stand

- **0.1.0, cut 2026-09-19.** The first release: a signed tag, a GitHub
  release, a Zenodo concept DOI and a version DOI. The concept DOI is in
  `CITATION.cff`; the 0.1.0 version DOI is `10.5281/zenodo.22850482`.
  `0.1.0` rather than `0.0.1` because the kit was already a working set of
  eleven skills and a protocol, not a sketch.
- **0.2.0, cut 2026-09-26.** MINOR, because it adds three skills and changes
  the question format in `working-preferences`, a change a MINOR bump may make
  while MAJOR is 0. The 0.2.0 version DOI is `10.5281/zenodo.22978591`. From
  0.3.0 on, `CITATION.cff` lists only the concept DOI, and each version DOI is
  recorded here by the release after it.
- **0.3.0, cut 2026-09-29.** MINOR, because it adds one skill, `daily-review`.
  It also starts the two-week cadence above, which replaces releasing whenever
  something outside the kit came to depend on a change, and moves version DOIs
  out of `CITATION.cff`.
