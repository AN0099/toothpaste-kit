# Containers

Images that hold what the kit needs, so nothing is installed on the host: one to try the kit, and
one that runs its checks with every tool they call, so that no check is skipped for a missing tool.
Each image has its own directory, with its Containerfile, its scripts and a README that lists every
tool in it, its version and where that version came from. The scripts need `podman`.

| Directory | Image | What it runs |
|---|---|---|
| [`starter/`](starter/README.md) | `localhost/kit-starter:v0` | Python, git and Claude Code, to try the quickstart without installing them; `containers/starter/run` starts it |
| [`verify/`](verify/README.md) | `localhost/kit-verify:v2` | The third-party checkers: reuse, CodeQL with its python and actions queries, yamllint, shellcheck, actionlint, check-jsonschema and CUE |

## Running `verify`

`containers/verify/verify TREE CMD...` runs `CMD` in the image on a copy of `TREE`. The tree is
mounted read-only and copied to a scratch directory inside the container, and the command runs
with no network. The image is built on first use; after editing the Containerfile, remove it with
`podman rmi localhost/kit-verify:v2` so the next run rebuilds it.

```sh
containers/verify/verify . ./scripts/compliance.sh --selftest
containers/verify/verify . ./scripts/gates.sh --selftest
containers/verify/verify . shellcheck scripts/compliance.sh
containers/verify/verify . actionlint
```

`containers/verify/codeql TREE` runs CodeQL's python and actions analyses on the tree with each
pack's default query suite, prints each alert as `file:line rule`, and exits 1 if there is any.

```sh
containers/verify/codeql .
```

## What they do not do

They run checks; they do not decide what a result means. A check that passes in the image passes
only for what the check covers, which each script's header states. The image does not reach the
network when a check runs, so a check that needs a service, such as the GitHub API, does not run
in it.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
