# References and prior work

Every external standard, specification and published practice this repository
depends on or borrows from, and what in here depends on it.

Split into normative and informative per
[RFC 7322](https://www.rfc-editor.org/info/rfc7322) section 4.8.6, where
**normative** means essential to implementing or understanding this
repository's content, and **informative** means additional information. That
split, and the requirement to cite BCP 14 when using its keywords, come from
RFC 7322 itself. `docs/document-layers.md` states how they are applied.

Local captures are not distributed with this repository. Where an entry names
one, the citation carries enough to retrieve the document independently.

## Normative references

### IETF

- **[BCP 14]** Bradner, S., "Key words for use in RFCs to Indicate Requirement
  Levels", BCP 14, RFC 2119, March 1997,
  <https://www.rfc-editor.org/info/bcp14>. BCP 14 also comprises RFC 8174,
  which clarifies that the keywords carry their defined meaning only in
  capitals. **Used by:** every document in this repository that states a
  requirement.

### W3C

- **[WCAG20-TECHS]** "Techniques for WCAG 2.0", W3C.
  <https://www.w3.org/TR/WCAG20-TECHS/>. **Used by:**
  `docs/document-accessibility.md`, for the G, H and F technique IDs.
- **[WCAG21-TECHS]** "Techniques for WCAG 2.1", W3C.
  <https://www.w3.org/WAI/WCAG21/Techniques/>. The living index. 2.0 and 2.1
  are different documents and a technique is not always revised between them,
  so both are cited where both exist. **Used by:**
  `docs/document-accessibility.md`.

### GitHub

- **[GFM]** "GitHub Flavored Markdown Spec". The dialect this repository's
  Markdown is rendered as, which is what makes WCAG apply to a README at all.
  **Used by:** `scripts/mdlint.py`, `scripts/reflow-md.py`.
- **[MDL]** "markdownlint Rules", markdownlint 0.41.1. The 53 rule IDs,
  semantics and parameter defaults. **Used by:** `scripts/mdlint.py`, which
  implements 19 of the 53 under the same IDs, and
  `.markdownlint-cli2.jsonc`, which runs the real tool over the same set.

### Other

- **[SEMVER]** "Semantic Versioning 2.0.0". <https://semver.org/>. **Used by:**
  `docs/releasing.md`, which applies one version to the whole kit.
- **[CFF]** "Citation File Format", version 1.2.0. **Used by:** `CITATION.cff`,
  which declares `cff-version: 1.2.0`.
- **[MIT]** The MIT License. **Used by:** `LICENSE`.

## Informative references

### IETF

- **[RFC 7322]** Flanagan, H. and S. Ginoza, "RFC Style Guide", RFC 7322,
  September 2014, <https://www.rfc-editor.org/info/rfc7322>. Source of the
  normative and informative reference split, the requirements-language section
  placement, and the precedent that a document may decline BCP 14 provided it
  says so. **Used by:** `docs/document-layers.md`.

### W3C

- **[WCAG-CONFORMANCE]** "Understanding Conformance", W3C WAI.
  <https://www.w3.org/WAI/WCAG21/Understanding/conformance>. Why this
  repository documents technique use and does not claim a conformance level.
- **[WCAG22-TECHS-INTRO]** "Understanding Techniques for WCAG 2.2 Success
  Criteria", W3C WAI. Techniques are sufficient or advisory, never required,
  which is the distinction `docs/document-accessibility.md` relies on.

### OpenSSF

- **[OSPS-BASELINE]** "Open Source Project Security Baseline", OpenSSF.
  <https://baseline.openssf.org/>. A target, not a claim.
- **[OSPS-BADGE]** "OpenSSF Best Practices Badge". <https://www.bestpractices.dev/>.
  A target, not a claim. **Referenced by:** `docs/security-posture.md`, whose
  tables are organised by control area because the criterion lists for both of
  these have not been transcribed from their published source.

### Other

- **[COVENANT]** "Contributor Covenant", version 2.1.
  <https://www.contributor-covenant.org/>. **Referenced by:**
  `CODE_OF_CONDUCT.md`, which is adapted from it in substance rather than
  reproduced.
- **[ZENODO]** Zenodo, CERN. <https://zenodo.org/>. Mints the DOI from a
  GitHub release webhook, and issues a concept DOI covering all versions
  alongside a per-version DOI. **Referenced by:** `docs/releasing.md`.

## Prior work, not yet integrated

Read and intended as the basis for future work. Nothing in this repository
depends on them yet, and listing them here is not a claim that it does.

### Semantic web

- **[OWL2-PRIMER]** "OWL 2 Web Ontology Language Primer (Second Edition)", W3C.
- **[OWL2-QUICKREF]** "OWL 2 Web Ontology Language Quick Reference Guide
  (Second Edition)", W3C.
- **[RDF12-PRIMER]** "RDF 1.2 Primer", W3C.
- **[SKOS-PRIMER]** "SKOS Simple Knowledge Organization System Primer", W3C.
- **[SKOS-REF]** "SKOS Simple Knowledge Organization System Reference", W3C.
  The likely nearest fit for `orchestration/registry/`, which is a controlled
  vocabulary with broader and narrower relations rather than a logic requiring
  inference.
- **[JSON-LD]** "JSON-LD", W3C. The interoperability path for services that
  consume JSON rather than RDF, which is what `orchestration/registry/` and
  `orchestration/schemas/` currently are.
- **[SW-FAQ]** "W3C Semantic Web FAQ", W3C.

### Data publishing

- **[DWBP]** "Data on the Web Best Practices", W3C.
- **[HTML-DATA]** "HTML Data Guide", W3C.

## What is deliberately not here

Design reasoning, decision history and the record of how any of the above came
to be adopted. That material is provenance and lives outside this repository,
per `docs/document-layers.md`.
