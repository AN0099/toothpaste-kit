# The kit blog: writing a post and building the site

The kit's blog is built only from what the repository already holds: release notes, CHANGELOG
entries and posts written about real changes. `scripts/blog.py` turns the posts in `blog/posts/`
into static HTML pages and one RSS feed carrying each post's whole text. It publishes nothing: it
writes files into a build directory and stops. The layout and the front block are experimental, and
nothing on this page is frozen.

## A post

A post is one Markdown file in `blog/posts/`, with a licence sidecar beside it.

- **The name** starts with the post's date: `2026-09-29-v0.3.0.md`.
- **The front block** opens the file and holds three fields, and nothing else about a post is
  required:

  ```markdown
  ---
  title: toothpaste-kit 0.3.0
  date: 2026-09-29
  summary: One new skill, daily-review, and a two-week release cadence; no script changed.
  ---
  ```

- **The body** uses only the Markdown the kit's own docs use: headings, paragraphs, lists, code
  blocks, links and inline code. The converter refuses anything else, HTML included, and names the
  file and line.
- **The licence** goes in a sidecar, `2026-09-29-v0.3.0.md.license`, holding the
  `SPDX-FileCopyrightText` and `SPDX-License-Identifier` lines. The converter drops HTML comments
  from the page, so a post could carry the trailing SPDX comment other docs end with instead; the
  posts here use the sidecar.

## What a post may say

Every claim in a post traces to a file in the tree at the commit the post is dated, the same rule
the kit's docs follow. A post that cannot point at its source is not written. End each post with a
Sources section naming the files and sections it comes from, such as the "0.4.0 (2026-10-13)"
section of `CHANGELOG.md`.

A release post says only what that release's CHANGELOG section holds. Choosing which entries to
tell is the writer's; adding to them is not.

## Writing a release post

1. Draft the post from the release's CHANGELOG section:

   ```sh
   python3 scripts/blog.py release-post 0.6.0
   ```

   The draft is for a person to edit. Check each sentence against the section before you keep it.

2. Add the licence sidecar, then check the post's Markdown:

   ```sh
   python3 scripts/mdlint.py blog/posts/2026-11-10-v0.6.0.md
   ```

   You should now see `mdlint: 1 file(s), 0 finding(s)`.

## Building the site

1. Check that the script works on this machine:

   ```sh
   python3 scripts/blog.py --selftest
   ```

   It exits 0 when every planted case behaves: an unsupported construct, a missing front field, a
   duplicate date and title, and a feed that is not well-formed or lacks an RSS 2.0 required
   element.

2. Build into a directory outside the tree:

   ```sh
   python3 scripts/blog.py build /tmp/kit-blog
   ```

   You should now see one page per post, an index page newest first, one stylesheet and
   `feed.xml`. The feed is RSS 2.0, with each post's full body in `content:encoded`, a stable
   `guid` per post and dates in RFC 822.

## What it does not do

It does not host or publish the site. A Pages site, a domain or a workflow that deploys are the
maintainer's decision, and the build directory is the deliverable.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
