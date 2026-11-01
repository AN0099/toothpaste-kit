# verify: the verification container

Runs the third-party checkers on a tree without installing them on the host. The tree is mounted
read-only and copied to a scratch directory inside the container, and checks run with no network.
How to run it is in [`containers/README.md`](../README.md).

## Tools

Each version is exact, and each download is checked against a sha256 in the
[`Containerfile`](Containerfile) or [`requirements.txt`](requirements.txt). The build also checks
that each tool reports the version pinned for it.

| Tool | Version | How it is installed | Where the version came from |
|---|---|---|---|
| python | 3.13-slim, by digest | The base image | The v0 image |
| libmagic1, git, xz-utils | The base image's Debian packages | `apt-get` | reuse's file-type detection, as on the CI runner; xz-utils unpacks shellcheck |
| reuse | 6.2.0 | pip, by hash, built from its sdist (no python 3.13 wheel) with poetry-core 2.5.0 from [`build-requirements.txt`](build-requirements.txt) | `.github/workflows/compliance.yml` |
| CodeQL CLI | 2.27.2 | The CodeQL bundle, by digest | The newest bundle at least 14 days old on 2026-10-31; the default setup runs whatever GitHub picks, usually the newest |
| codeql/python-queries, codeql/actions-queries | The versions in the 2.27.2 bundle | The CodeQL bundle | The bundle; the build writes the resolved packs to `/opt/codeql-packs.txt` |
| yamllint | 1.38.0 | pip, by hash | The newest release at least 14 days old on 2026-10-31 |
| shellcheck | 0.11.0 | Release binary, by digest | The newest release at least 14 days old on 2026-10-31 |
| actionlint | 1.7.12 | Release binary, by digest | The newest release at least 14 days old on 2026-10-31 |
| check-jsonschema | 0.38.2 | pip, by hash | The newest release at least 14 days old on 2026-10-31 |
| CUE | 0.17.1 | Release binary, by digest | The newest release at least 14 days old on 2026-10-31 |

Only reuse has a version CI also pins. The others are chosen here: the newest release that has
been out at least 14 days, so a compromised release has time to be found before it is pinned. The
Python packages' own dependencies are pinned the same way in `requirements.txt`, resolved from files
uploaded before the cutoff. A new version is a change to this table, the Containerfile and its
digest together.

## CodeQL settings

`codeql-scan` analyses with `--threat-model=local`, because the repository's default setup counts
command-line arguments and files as untrusted input. Without it, the local run misses the
`py/path-injection` alerts that CI then reports. It gives CodeQL a 4 GB heap (`--ram=4096`), which the
Python analysis of this tree needs to finish.

## The `.git` file

A git worktree has a `.git` file pointing outside the mount, so `git` fails inside the container
and any check that calls it fails falsely. `verify` replaces that file in the copy with a fresh
`git init`. The source tree is never changed.

## Not yet

- The image is built for linux/amd64 only.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
