# Schema test cases

Documents checked one at a time against one round schema each, from
[`orchestration/schemas/round/`](../../../orchestration/schemas/round/README.md).

- `cases.json`: the list the runner reads. Each case names a `file`, the `schema` it is checked
  against, whether it should `pass` or `fail`, and the `matrixRow` it covers in the validation
  matrix, the table under [What a schema decides, and what the validator decides](../../../orchestration/schemas/round/README.md#what-a-schema-decides-and-what-the-validator-decides).
  A case for a rule outside the matrix has `matrixRow` null and says why in `reason`. A file not
  listed in `cases.json` is not run.
- `valid/`: complete rounds that must pass, one directory per matrix row.
- `invalid/`: documents that must fail, one directory per rule they break, named for the rule.

A case here shows only what one document's schema can see. Rules that compare one record with
another, such as a decision citing a finding nobody reproduced, are the validator's, and the matrix
marks them "Not decidable" for the schema; `--selftest` covers those. Run the cases with:

```sh
python3 scripts/round-check.py --cases examples/review-round/schema-cases
```

To add a case, add its file under `valid/` or `invalid/` and its entry to `cases.json`.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
