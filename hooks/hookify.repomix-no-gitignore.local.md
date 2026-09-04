---
name: repomix-no-gitignore
enabled: true
event: bash
action: block
tool_matcher: Bash
conditions:
  - field: command
    operator: regex_match
    pattern: (^|[;&|]\s*|\$\(\s*|\n\s*)(npx\s+)?repomix\b
  - field: command
    operator: contains
    pattern: --no-gitignore
---

**Blocked: `--no-gitignore` silently disables the second layer of defense.**

`db/.gitignore` is not only a Git file here. This tree is deliberately not a
repository, and the file exists primarily as the repomix deny-list. Passing
`--no-gitignore` removes the tier-boundary exclusions, the unfiled-material
exclusions, and every credential pattern, with no error and no visible change in
the command output.

**If this flag is genuinely needed**, mirror the deny-list first:

```
cp .gitignore .repomixignore
```

Then re-run, and check the resulting file list against the verification commands
in `system/repomix-procedure.md` before treating the pack as usable.

Note that the allow-list, not the deny-list, is the control actually doing the
work. Disabling the backstop is tolerable only while `--include` is still scoping
the run, and it is never safe on its own.
