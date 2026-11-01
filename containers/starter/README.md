# Starter container

Try the kit without installing its dependencies on your machine. The image holds what the
[quickstart](../../docs/quickstart.md) and the scripts the README and
[installing guide](../../docs/installing.md) tell you to run need: Python, git, the shell tools
the scripts call, and Claude Code. Your files stay on your machine: the kit is mounted read-only,
and the directory you name is mounted read-write as the workspace.

## Build and run

You need [Podman](https://podman.io/) on the host, nothing else. From your clone of the kit:

```sh
containers/starter/run ~/tpkit-try
```

The first run builds the image, `localhost/kit-starter:v0`. After editing the `Containerfile`,
remove the image with `podman rmi localhost/kit-starter:v0` and the next run builds it again.

`run` starts a shell in the container as your own user (`--userns=keep-id`), so files you make
are owned by you on the host:

| Inside | On the host |
|---|---|
| `/kit`, read-only | The kit clone `run` lives in |
| `/workspace`, read-write, the starting directory | The directory you name, or the current one if you name none |

The directory must exist and must be outside the kit; `run` refuses one inside it. With a command
after the directory, `run` runs that instead of a shell:

```sh
containers/starter/run ~/tpkit-try sh -c 'cd /kit && ./scripts/gates.sh --selftest'
```

The kit's scripts run from the kit root, `/kit`, so a command that runs one changes there first.

**There is no network** unless you pass `--network` first. The kit's scripts need none. Claude
Code does, to sign in and to work:

```sh
containers/starter/run --network ~/tpkit-try
```

## The quickstart inside the container

Step 2, the clone, is already done: the kit is `/kit`. Steps 3 and 4 become:

```sh
cp -R /kit/examples/workspace /workspace/tpkit-workspace
cd /kit && ./scripts/link-skills.sh /workspace/tpkit-workspace/.claude/skills
```

Step 5 needs `--network`; start `claude` in `/workspace/tpkit-workspace`.

The skill links point at `/kit/skills`, so they resolve inside the container and not on the host.
To use the workspace from Claude Code on the host later, copy the skills in instead of linking
them, as the installing guide's "Symlink or copy" section describes.

## What it holds and why

| Part | Why |
|---|---|
| Python 3.13, the base image, pinned by digest | The `.py` scripts and `check-qblock` and `check-pr-body` run on `python3`, standard library only. The same base as the verification container |
| git | Quickstart step 1 runs `git --version`; `gates.sh`, `remote-level.sh`, `reorient` and `spdx-fragment.py` read a repository |
| `sh`, `bash`, GNU `grep`, `find`, `sed`, `awk`, `sort`, `mktemp`, `ln -r` | Called by the shell scripts; all are in the base image's Debian already, so nothing is added for them |
| Node.js 22.12.0 and Claude Code 2.1.304, with its `linux-x64` platform package | Quickstart steps 1 and 5 run `claude` |

Each download in the `Containerfile` names its exact version and its sha256, and the build fails
on a hash that does not match.

## What it does not do

- It does not keep your Claude Code sign-in or settings. The home directory is inside the
  container and goes when it exits, so each run signs in again.
- It does not hold the tools `scripts/compliance.sh` needs, such as `reuse`, or the linters CI
  runs. The verification container is for those.
- It does not run `repomix`, which the README describes as a separate tool needing Node.js and
  network.
- It does not work on a kit that is a git worktree: the worktree's `.git` file points outside the
  mount, so git fails inside. Use a plain clone, as the quickstart makes.
- It does not relabel files for SELinux. `run` starts the container with SELinux separation turned
  off for it (`--security-opt label=disable`), because a relabel rewrites the labels of the
  workspace directory and everything under it on the host, and that directory may be your home.
- It is for x86-64 only for now. The Node.js download and Claude Code's platform package are both
  pinned for `linux-x64`, and the image installs the platform package from that pinned file with no
  registry access, so on another architecture the build has nothing to install.
- The Containerfile installs the platform package before the main package, and that order must
  stay: the main package's install step copies the `claude` binary out of the platform package,
  and if it runs first it finds nothing and leaves a stub, so `claude` does not run.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
