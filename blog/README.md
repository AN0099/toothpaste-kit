# Blog

This directory holds the kit blog's posts. `scripts/blog.py` builds them into static HTML pages and
one RSS feed; nothing here is published. This page is the index for `blog/` and `blog/posts/`:
`blog.py` refuses any `.md` file in `posts/` whose name is not a post's, so `posts/` has no README
of its own. The full guide, from writing a post to building the site, is
[The kit blog](../docs/blog.md).

| Path | What it is | Read by |
|---|---|---|
| [`posts/`](posts/) | The posts, one Markdown file each, with its licence sidecar beside it | `blog.py build`, which reads it unless `--posts DIR` names another |
| `posts/YYYY-MM-DD-slug.md` | One post: a front block, then the body | `load_posts` in `blog.py` |
| `posts/YYYY-MM-DD-slug.md.license` | The post's `SPDX-FileCopyrightText` and `SPDX-License-Identifier` lines | Not `blog.py`, which reads only names ending `.md` |

The posts so far, each with its `.license` sidecar:

- [`posts/2026-09-29-v0.3.0.md`](posts/2026-09-29-v0.3.0.md): toothpaste-kit 0.3.0
- [`posts/2026-10-13-v0.4.0.md`](posts/2026-10-13-v0.4.0.md): toothpaste-kit 0.4.0
- [`posts/2026-10-27-v0.5.0.md`](posts/2026-10-27-v0.5.0.md): toothpaste-kit 0.5.0

## What a post must be

`load_posts` refuses a post, naming the file and, where it has one, the line, when any of these
fails:

- **The name** is `YYYY-MM-DD-slug.md`: a date, a dash, then a slug of letters, digits, dot, dash
  or underscore. The date in the name must equal the front block's `date`.
- **The front block** is the file's first line, `---`, then one `field: value` line per field,
  then a closing `---`. A value wrapped in matching single or double quotes has them removed.
  It has exactly three fields, each once and none empty:
  - `title`: the page's only level-1 heading, so the body starts at `##`.
  - `date`: `YYYY-MM-DD`.
  - `summary`: the one sentence shown under the title on the index page.
- **The body** uses only the Markdown subset listed at the top of `scripts/blog.py`: headings of
  levels 2 to 6, paragraphs, lists, fenced code blocks, links and inline code. HTML comments are
  dropped from the page; other constructs are refused.
- **No two posts** share both a date and a title.

## From post to page

```sh
python3 scripts/blog.py build OUT
```

writes into OUT one `<slug>.html` per post, where the slug is the file name without `.md`; an
`index.html` listing the posts newest first; a `style.css`; and a `feed.xml`. The feed is written
by `write_feed` in `blog.py`, from the same posts: RSS 2.0, each post's whole body in
`content:encoded`, its `guid` `tp-kit-blog:` and the slug, and its date in RFC 822 at midnight UTC.
`python3 scripts/blog.py --selftest` runs the planted cases for both, and `scripts/gates.sh` runs it
as gate 20.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
