---
name: repomix-allowlist
enabled: true
event: bash
action: block
tool_matcher: Bash
conditions:
  - field: command
    operator: regex_match
    pattern: (^|[;&|]\s*|\$\(\s*|\n\s*)(npx\s+)?repomix\b
  - field: command
    operator: not_contains
    pattern: --include
---

**Blocked: repomix invoked without an `--include` allow-list.**

In a personal knowledge tree the great majority of files must never be packed.
Under a deny-list alone, anything
new lands inside the pack by default and stays there until a human notices. The
allow-list inverts that: new material is outside until someone deliberately adds
it. Skipping this step is the exact failure that motivated the rule.

**The shape of the correct command**, run from the tree root. Substitute the
directories that are actually publishable in your tree:

```
repomix --include "*.md,<dir-a>/**,<dir-b>/**" --output repomix-output.xml
```

Quote the `--include` value. Unquoted, the shell expands `*.md` against the
working directory before repomix sees it.

**Verify every run, do not assume:**

```
grep -c '<file path=' repomix-output.xml
```

Compare the count against what your allow-list should admit. A count far above
that means the include list was not applied and the run swept the unfiled and
reference trees. Then run a path-inspection pass over the output, listing every
packed path and checking it against your tier boundaries. It must return nothing
from an excluded tree.

**Two things that are not gates.** Repomix's bundled secret scanner is a
tripwire rather than a boundary: treat a clean security check as information, not
as clearance to send. And the scanner writes a findings report alongside the
pack. That report enumerates locations of interest, so treat it at the same
sensitivity as the material it describes and remove it once read.
