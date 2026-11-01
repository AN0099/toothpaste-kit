#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2026 Aidan Naveja
#
# SPDX-License-Identifier: Apache-2.0

"""Build the kit blog: static HTML pages from blog/posts/*.md.

Experimental. The layout and the front block may change.

A post is a Markdown file whose name starts with its date
(2026-10-13-v0.4.0.md) and opens with a front block of exactly three fields:

    ---
    title: What 0.4.0 changed
    date: 2026-10-13
    summary: One sentence for the index.
    ---

The converter handles the Markdown subset the kit's own docs use, and nothing
more. Anything outside it is refused with the file and line, rather than
passed through or guessed at, because a page that renders differently from
what its author read is a silent error. Supported:

  - ATX headings, levels 2 to 6 (the title is the page's only h1, and comes
    from the front block)
  - paragraphs
  - unordered (- or *) and ordered (1.) lists, nested by indentation
  - fenced code blocks (```), with an optional language word
  - inline links [text](url), with an http, https, mailto or relative url
  - inline code `x`
  - HTML comments, dropped from the output (a post's SPDX lines go in its
    .license sidecar, as blog/README.md says, not in a comment)

Refused, among others: emphasis, images, raw HTML, blockquotes, tables,
horizontal rules, setext headings, indented code blocks, reference links.

Output: OUT/<slug>.html for each post, OUT/index.html newest first, and
OUT/style.css. Plain semantic HTML, no scripts. If a write_feed(posts, out_dir)
function is defined in this file, build calls it as well; without one the
pages are built alone. Nothing is published: the script writes files into OUT
and stops.

Usage:
    blog.py build OUT [--posts DIR]   build the site into OUT (default posts: blog/posts)
    blog.py release-post VERSION      draft blog/posts/<date>-v<VERSION>.md from CHANGELOG.md
    blog.py --selftest                run the planted cases, exit nonzero on failure
"""

import argparse
import datetime
import html
import os
import re
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(ROOT, 'blog', 'posts')
SITE_TITLE = 'tp-kit blog'
FRONT_FIELDS = ('title', 'date', 'summary')
NAME_RE = re.compile(r'^(\d{4}-\d{2}-\d{2})-[A-Za-z0-9._-]+\.md$')

STYLE = """\
:root { color-scheme: light dark; --fg: #1a1a1a; --bg: #fdfdfc; --muted: #595959; --rule: #d6d6d6; --link: #0b57a4; }
@media (prefers-color-scheme: dark) {
  :root { --fg: #e8e8e6; --bg: #161616; --muted: #b0b0ab; --rule: #3a3a3a; --link: #8cb9f0; }
}
body { margin: 0 auto; max-width: 42rem; padding: 1.5rem 1rem 3rem; font: 1.0625rem/1.6 system-ui, sans-serif; color: var(--fg); background: var(--bg); }
a { color: var(--link); }
header { border-bottom: 1px solid var(--rule); margin-bottom: 1.5rem; }
time, .summary { color: var(--muted); }
pre { overflow-x: auto; padding: 0.75rem; border: 1px solid var(--rule); }
code { font-family: ui-monospace, monospace; font-size: 0.95em; }
ol.posts { list-style: none; padding: 0; }
ol.posts li { margin-bottom: 1.25rem; }
"""


class BlogError(Exception):
    """One or more posts were refused; args[0] is the list of messages."""


# ---------------------------------------------------------------- front block

def parse_front(path, lines):
    """Return (fields, index of the first body line). Raises BlogError."""
    errs = []
    if not lines or lines[0].strip() != '---':
        raise BlogError([f'{path}:1: no front block: the file must start with a --- line'])
    fields = {}
    end = None
    for i in range(1, len(lines)):
        line = lines[i]
        if line.strip() == '---':
            end = i
            break
        # One quantifier per span, so a long line cannot backtrack; strip()
        # drops the spaces that \s*(.*?)\s*$ used to.
        m = re.match(r'^([a-z]+):(.*)$', line)
        if not m:
            errs.append(f'{path}:{i + 1}: front block line is not "field: value"')
            continue
        key, val = m.group(1), m.group(2).strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in '"\'':
            val = val[1:-1]
        if key not in FRONT_FIELDS:
            errs.append(f'{path}:{i + 1}: unknown front field {key!r}; the fields are {", ".join(FRONT_FIELDS)}')
        elif key in fields:
            errs.append(f'{path}:{i + 1}: front field {key!r} given twice')
        elif not val:
            errs.append(f'{path}:{i + 1}: front field {key!r} is empty')
        else:
            fields[key] = (val, i + 1)
    if end is None:
        raise BlogError(errs + [f'{path}:1: front block has no closing --- line'])
    for key in FRONT_FIELDS:
        if key not in fields and not any(f'{key!r}' in e for e in errs):
            errs.append(f'{path}:1: missing front field {key!r}')
    if 'date' in fields:
        val, ln = fields['date']
        try:
            fields['date'] = (datetime.date.fromisoformat(val), ln)
        except ValueError:
            errs.append(f'{path}:{ln}: date {val!r} is not YYYY-MM-DD')
            del fields['date']
    if errs:
        raise BlogError(errs)
    return {k: v for k, (v, _) in fields.items()}, end + 1


# ------------------------------------------------------------------ converter

def refuse(path, ln, what):
    return f'{path}:{ln}: unsupported construct: {what}'


def inline(path, ln, text, errs):
    """Convert one line's inline markup. Appends refusals to errs."""
    parts = text.split('`')
    if len(parts) % 2 == 0:
        errs.append(refuse(path, ln, 'unclosed inline code (`)'))
        return html.escape(text)
    out = []
    for n, part in enumerate(parts):
        if n % 2:
            out.append(f'<code>{html.escape(part)}</code>')
            continue
        if '![' in part:
            errs.append(refuse(path, ln, 'image (![...])'))
        pos = 0
        for m in re.finditer(r'\[([^\[\]]+)\]\(([^()\s]+)\)', part):
            out.append(inline_text(path, ln, part[pos:m.start()], errs))
            url = m.group(2)
            if re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:', url) and not re.match(r'^(https?|mailto):', url):
                errs.append(refuse(path, ln, f'link scheme in {url!r}; only http, https, mailto or relative'))
            out.append(f'<a href="{html.escape(url)}">{inline_text(path, ln, m.group(1), errs)}</a>')
            pos = m.end()
        out.append(inline_text(path, ln, part[pos:], errs))
    return ''.join(out)


INLINE_REFUSED = [
    (re.compile(r'\]\[|\]\(|^\[[^\]]*\]:'), 'reference or malformed link'),
    (re.compile(r'<[A-Za-z/!?]'), 'raw HTML or autolink (<...>)'),
    (re.compile(r'\*'), 'emphasis (*)'),
    (re.compile(r'(^|\W)_|_($|\W)'), 'emphasis (_)'),
]


def inline_text(path, ln, text, errs):
    for pat, what in INLINE_REFUSED:
        if pat.search(text):
            errs.append(refuse(path, ln, what))
    return html.escape(text, quote=False)


BLOCK_REFUSED = [
    (re.compile(r'^\s*>'), 'blockquote (>)'),
    (re.compile(r'^\s*\|'), 'table (|)'),
    (re.compile(r'^\s*([-*_])(\s*\1){2,}\s*$'), 'horizontal rule'),
    (re.compile(r'^\s*(=+|-+)\s*$'), 'setext heading underline'),
    (re.compile(r'^\s*~~~'), 'fenced code with ~~~; use ```'),
    (re.compile(r'^#{1,6}[^#\s]'), 'heading without a space after #'),
    (re.compile(r'^\s*<(?!!--)'), 'raw HTML block'),
]
# Neither pattern has two quantifiers that can match the same characters
# side by side ([^ ] and the literal space end each run of spaces), so
# neither can backtrack on a long line. The spaces after a
# marker and a heading's closing #s are cut in code instead: heading_text and
# the lstrip on an item's text.
HEADING_RE = re.compile(r'^(#{1,6})( +)([^ ].*)?$')
ITEM_RE = re.compile(r'^( *)([-*]|\d+\.) (.*)$')


def heading_text(m):
    """A HEADING_RE match's text without the closing run of # and the
    spaces around it, as (.+?)\\s*#*\\s*$ read it, or None when there is no
    text. The text is the shortest non-empty start of the rest whose tail is
    spaces, #s, spaces; with nothing after the spaces, one space is the text."""
    rest = m.group(3)
    if not rest:
        return ' ' if len(m.group(2)) > 1 else None
    cut = len(rest.rstrip().rstrip('#').rstrip())
    return rest[:max(cut, 1)]


def convert(path, lines, first_ln=1):
    """Convert body lines to HTML. Raises BlogError listing every refusal."""
    errs = []
    out = []
    para = []          # (ln, text) lines of the open paragraph
    lists = []         # stack of [indent, tag, item lines]
    i = 0

    def close_para():
        if para:
            out.append('<p>' + ' '.join(inline(path, ln, t, errs) for ln, t in para) + '</p>')
            para.clear()

    def close_item():
        if lists and lists[-1][2]:
            out.append('<li>' + ' '.join(inline(path, ln, t, errs) for ln, t in lists[-1][2]))
            lists[-1][2] = []
            return True
        return False

    def close_lists(to_indent=-1):
        while lists and lists[-1][0] > to_indent:
            if close_item():
                out.append('</li>')
            out.append(f'</{lists.pop()[1]}>')
            if lists:
                out.append('</li>')

    while i < len(lines):
        ln = first_ln + i
        line = lines[i].rstrip('\n').rstrip()
        i += 1
        if not line:
            close_para()
            close_lists()
            continue
        if line.lstrip().startswith('<!--'):
            close_para()
            close_lists()
            j = i - 1
            while '-->' not in lines[j]:
                j += 1
                if j >= len(lines):
                    errs.append(f'{path}:{ln}: HTML comment is not closed')
                    break
            i = j + 1
            continue
        if line.startswith('```'):
            close_para()
            close_lists()
            lang = line[3:].strip()
            if lang and not re.match(r'^[A-Za-z0-9_+-]+$', lang):
                errs.append(refuse(path, ln, f'code fence info {lang!r}; one language word only'))
            body = []
            while i < len(lines) and lines[i].rstrip() != '```':
                body.append(lines[i].rstrip('\n'))
                i += 1
            if i >= len(lines):
                errs.append(f'{path}:{ln}: code block is not closed')
            i += 1
            cls = f' class="language-{html.escape(lang)}"' if lang else ''
            out.append(f'<pre><code{cls}>' + html.escape('\n'.join(body)) + '</code></pre>')
            continue
        refused = next((what for pat, what in BLOCK_REFUSED if pat.search(line)), None)
        if refused:
            errs.append(refuse(path, ln, refused))
            continue
        m = HEADING_RE.match(line)
        text = heading_text(m) if m else None
        if text is not None:
            close_para()
            close_lists()
            level = len(m.group(1))
            if level == 1:
                errs.append(refuse(path, ln, 'level-1 heading; the title comes from the front block'))
                continue
            out.append(f'<h{level}>{inline(path, ln, text, errs)}</h{level}>')
            continue
        m = ITEM_RE.match(line)
        if m and not para:
            indent, tag = len(m.group(1)), 'ul' if m.group(2) in '-*' else 'ol'
            if not lists or indent > lists[-1][0]:
                if not lists and indent:
                    errs.append(refuse(path, ln, 'indented list with no parent item'))
                if lists:
                    if not lists[-1][2]:
                        errs.append(refuse(path, ln, 'nested list with no parent item'))
                    close_item()
                lists.append([indent, tag, []])
                out.append(f'<{tag}>')
            else:
                close_lists(indent)
                if lists and lists[-1][0] != indent:
                    errs.append(refuse(path, ln, 'list item indentation matches no open list'))
                if close_item():
                    out.append('</li>')
                if lists and lists[-1][1] != tag:
                    errs.append(refuse(path, ln, 'list changes between - and 1. at one level'))
            lists[-1][2].append((ln, m.group(3).lstrip(' ')))
            continue
        if lists:
            if line.startswith(' ') and lists[-1][2]:
                lists[-1][2].append((ln, line.strip()))
                continue
            close_lists()
        if line.startswith('    '):
            errs.append(refuse(path, ln, 'indented code block; use ```'))
            continue
        para.append((ln, line.strip()))
    close_para()
    close_lists()
    if errs:
        raise BlogError(errs)
    return '\n'.join(out) + '\n'


# ---------------------------------------------------------------- posts, pages

def load_posts(posts_dir):
    """Read every post in posts_dir. Returns dicts, newest first, with the keys
    title, date (datetime.date), summary, slug and html. Raises BlogError
    listing every refusal in every post."""
    if not os.path.isdir(posts_dir):
        raise BlogError([f'{posts_dir}: no posts directory'])
    errs = []
    posts = []
    for name in sorted(os.listdir(posts_dir)):
        if not name.endswith('.md'):
            continue
        path = os.path.join(posts_dir, name)
        m = NAME_RE.match(name)
        if not m:
            errs.append(f'{path}: name must be YYYY-MM-DD-slug.md, with letters, digits, dot, dash or underscore')
            continue
        with open(path, encoding='utf-8') as f:
            lines = f.read().split('\n')
        try:
            front, body_at = parse_front(path, lines)
            if str(front['date']) != m.group(1):
                raise BlogError([f'{path}: name starts with {m.group(1)} but the front date is {front["date"]}'])
            body = convert(path, lines[body_at:], body_at + 1)
        except BlogError as e:
            errs.extend(e.args[0])
            continue
        posts.append(dict(front, slug=name[:-3], html=body, path=path))
    seen = {}
    for p in posts:
        key = (p['date'], p['title'])
        if key in seen:
            errs.append(f'{p["path"]}: same date and title as {seen[key]}')
        else:
            seen[key] = p['path']
    if errs:
        raise BlogError(errs)
    posts.sort(key=lambda p: (p['date'], p['slug']), reverse=True)
    for p in posts:
        del p['path']
    return posts


def page(title, main):
    feed = ''
    if 'write_feed' in globals():
        feed = f'\n<link rel="alternate" type="application/rss+xml" title="{SITE_TITLE}" href="feed.xml">'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="style.css">{feed}
</head>
<body>
<header><p><a href="index.html">{SITE_TITLE}</a></p></header>
<main>
{main}</main>
</body>
</html>
"""


def build(out_dir, posts_dir=POSTS_DIR):
    posts = load_posts(posts_dir)
    os.makedirs(out_dir, exist_ok=True)
    for p in posts:
        d = p['date'].isoformat()
        main = (f'<article>\n<h1>{html.escape(p["title"])}</h1>\n'
                f'<p><time datetime="{d}">{d}</time></p>\n{p["html"]}</article>\n')
        with open(os.path.join(out_dir, p['slug'] + '.html'), 'w', encoding='utf-8') as f:
            f.write(page(f'{p["title"]} - {SITE_TITLE}', main))
    items = ''.join(
        f'<li><a href="{html.escape(p["slug"])}.html">{html.escape(p["title"])}</a>'
        f' <time datetime="{p["date"]}">{p["date"]}</time>'
        f'<p class="summary">{html.escape(p["summary"])}</p></li>\n' for p in posts)
    index = f'<h1>{SITE_TITLE}</h1>\n' + (f'<ol class="posts">\n{items}</ol>\n' if posts else '<p>No posts yet.</p>\n')
    with open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(page(SITE_TITLE, index))
    with open(os.path.join(out_dir, 'style.css'), 'w', encoding='utf-8') as f:
        f.write(STYLE)
    if 'write_feed' in globals():
        globals()['write_feed'](posts, out_dir)
    return posts


# ------------------------------------------------------------------- selftest

# REUSE-IgnoreStart
GOOD = """---
title: A good post
date: 2026-10-13
summary: Every supported construct once.
---

## What changed

A paragraph with `inline <code>` and a [link](https://example.org/a?b=1&c=2)
that wraps onto a second line.

- one
- two, with [a relative link](../docs/quickstart.md)
  continued
  - nested
- three

1. first
2. second

```sh
echo "<kept>" && exit 0
```

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
"""
# REUSE-IgnoreEnd

GOOD_HTML = """<h2>What changed</h2>
<p>A paragraph with <code>inline &lt;code&gt;</code> and a <a href="https://example.org/a?b=1&amp;c=2">link</a> that wraps onto a second line.</p>
<ul>
<li>one
</li>
<li>two, with <a href="../docs/quickstart.md">a relative link</a> continued
<ul>
<li>nested
</li>
</ul>
</li>
<li>three
</li>
</ul>
<ol>
<li>first
</li>
<li>second
</li>
</ol>
<pre><code class="language-sh">echo &quot;&lt;kept&gt;&quot; &amp;&amp; exit 0</code></pre>
"""


def front(title='T', date='2026-10-14', summary='S', body='Text.\n'):
    lines = ['---']
    for k, v in (('title', title), ('date', date), ('summary', summary)):
        if v is not None:
            lines.append(f'{k}: {v}')
    return '\n'.join(lines) + '\n---\n\n' + body


# Each planted case: name, {file name: text}, a fragment the error must hold.
# The three the design note names come first; REQUIRED fails the selftest if
# any of them is ever dropped from this list.
PLANTED = [
    ('unsupported construct', {'2026-10-14-t.md': front(body='| a | b |\n')}, '2026-10-14-t.md:7: unsupported construct: table'),
    ('missing front field', {'2026-10-14-t.md': front(summary=None)}, "missing front field 'summary'"),
    ('duplicate date and title', {'2026-10-14-a.md': front(), '2026-10-14-b.md': front()}, 'same date and title as'),
    ('emphasis', {'2026-10-14-t.md': front(body='Some **bold** text.\n')}, 'unsupported construct: emphasis (*)'),
    ('underscore emphasis', {'2026-10-14-t.md': front(body='Some _slanted_ text.\n')}, 'unsupported construct: emphasis (_)'),
    ('image', {'2026-10-14-t.md': front(body='![alt](a.png)\n')}, 'unsupported construct: image'),
    ('raw HTML', {'2026-10-14-t.md': front(body='<div>x</div>\n')}, 'unsupported construct: raw HTML block'),
    ('inline HTML', {'2026-10-14-t.md': front(body='a <b>b</b>\n')}, 'unsupported construct: raw HTML'),
    ('blockquote', {'2026-10-14-t.md': front(body='> quoted\n')}, 'unsupported construct: blockquote'),
    ('horizontal rule', {'2026-10-14-t.md': front(body='a\n\n***\n')}, 'unsupported construct: horizontal rule'),
    ('level-1 heading', {'2026-10-14-t.md': front(body='# Title again\n')}, 'level-1 heading'),
    ('script link', {'2026-10-14-t.md': front(body='[x](javascript:alert)\n')}, 'link scheme'),
    ('unclosed code', {'2026-10-14-t.md': front(body='a `b\n')}, 'unclosed inline code'),
    ('unclosed fence', {'2026-10-14-t.md': front(body='```\ncode\n')}, 'code block is not closed'),
    ('unknown front field', {'2026-10-14-t.md': front() .replace('summary: S', 'summary: S\nauthor: X')}, "unknown front field 'author'"),
    ('bad date', {'2026-10-14-t.md': front(date='14 October 2026')}, 'is not YYYY-MM-DD'),
    ('name and date differ', {'2026-10-14-t.md': front(date='2026-10-15')}, 'but the front date is 2026-10-15'),
    ('no front block', {'2026-10-14-t.md': 'Text.\n'}, 'no front block'),
    ('bad name', {'news.md': front()}, 'name must be YYYY-MM-DD-slug.md'),
]
REQUIRED = ('unsupported construct', 'missing front field', 'duplicate date and title')


def selftest():
    fails = []

    def check(ok, what):
        print(('PASS ' if ok else 'FAIL ') + what)
        if not ok:
            fails.append(what)

    names = [c[0] for c in PLANTED]
    check(all(r in names for r in REQUIRED), 'the three planted cases the design note names are all present')
    with tempfile.TemporaryDirectory() as tmp:
        posts = os.path.join(tmp, 'posts')
        os.mkdir(posts)
        with open(os.path.join(posts, '2026-10-13-good.md'), 'w') as f:
            f.write(GOOD)
        with open(os.path.join(posts, '2026-10-20-later.md'), 'w') as f:
            f.write(front(title='Later & newer', date='2026-10-20'))
        got = load_posts(posts)
        check([p['slug'] for p in got] == ['2026-10-20-later', '2026-10-13-good'], 'load_posts returns newest first')
        check(set(got[0]) == {'title', 'date', 'summary', 'slug', 'html'}, 'each post has exactly the agreed keys')
        check(got[1]['date'] == datetime.date(2026, 10, 13), 'date is a datetime.date')
        check(got[1]['html'] == GOOD_HTML, 'every supported construct converts to the expected HTML')
        if got[1]['html'] != GOOD_HTML:
            print(got[1]['html'])
        out = os.path.join(tmp, 'out')
        called = []
        globals()['write_feed'] = lambda ps, d: called.append((len(ps), d))
        try:
            build(out, posts)
        finally:
            del globals()['write_feed']
        check(called == [(2, out)], 'build calls write_feed(posts, out_dir) when it is defined')
        check(sorted(os.listdir(out)) == ['2026-10-13-good.html', '2026-10-20-later.html', 'index.html', 'style.css'],
              'build writes one page per post, the index and the stylesheet')
        index = open(os.path.join(out, 'index.html')).read()
        check(index.index('Later &amp; newer') < index.index('A good post'), 'the index lists newest first, escaped')
        out2 = os.path.join(tmp, 'out2')
        build(out2, posts)
        pages = ''.join(open(os.path.join(out2, n)).read() for n in os.listdir(out2) if n.endswith('.html'))
        check('<script' not in pages and 'feed.xml' not in pages, 'without write_feed: no script and no feed link')
        check(pages.count('<h1>') == 3, 'each page has one h1')
    for name, files, want in PLANTED:
        with tempfile.TemporaryDirectory() as tmp:
            for fn, text in files.items():
                with open(os.path.join(tmp, fn), 'w') as f:
                    f.write(text)
            try:
                load_posts(tmp)
                msg = ''
            except BlogError as e:
                msg = '\n'.join(e.args[0])
            check(want in msg, f'planted {name} is refused' + ('' if want in msg else f' (got: {msg or "no error"})'))
    # Each rewritten pattern on a long line built to make the old one
    # backtrack: each must finish well under a second and read as before.
    import time

    def quick(label, run):
        t0 = time.perf_counter()
        got = run()
        took = time.perf_counter() - t0
        check(took < 1.0, f'{label}, in {took:.3f} s')
        return got

    # pad T pad T, not pad T pad: the old \s*(.*?)\s*$ was linear on the
    # second and took 4 s on this one.
    pad = ' \t' * 20000
    fields, _ = quick('a front line of 40000 spaces and tabs, T, 40000 more and T',
                      lambda: parse_front('p', ['---', 'title: ' + pad + 'T' + pad + 'T', 'date: 2026-10-14',
                                                'summary: S', '---']))
    check(fields.get('title') == 'T' + pad + 'T', 'the padding around a front value is dropped')
    html_out = quick('a heading of 20000 " # " runs before its last word',
                     lambda: convert('p', ['## a' + ' # ' * 20000 + 'b']))
    check(html_out.startswith('<h2>a #') and html_out.endswith(' b</h2>\n'), 'that heading keeps its #s inside the text')
    html_out = quick('a heading of 100000 spaces before its last letter',
                     lambda: convert('p', ['## a' + ' ' * 100000 + 'b']))
    check(html_out == '<h2>a' + ' ' * 100000 + 'b</h2>\n', 'that heading keeps its spaces')
    # convert's lines never hold a newline; this times the pattern on one anyway.
    quick('HEADING_RE on 100000 spaces then a newline', lambda: HEADING_RE.match('# ' + ' ' * 100000 + '\nx'))
    check(convert('p', ['## Title ## ']) == '<h2>Title</h2>\n', 'a heading drops its closing #s')
    html_out = quick('a list item with 100000 spaces after its marker',
                     lambda: convert('p', ['- ' + ' ' * 100000 + 'x']))
    check(html_out == '<ul>\n<li>x\n</li>\n</ul>\n', 'the spaces after an item marker are dropped')
    # As with HEADING_RE: the old ' +(.*)$' took 6 s here, though convert never passes a newline.
    quick('ITEM_RE on 50000 spaces then a newline', lambda: ITEM_RE.match('- ' + ' ' * 50000 + '\nx'))
    with tempfile.TemporaryDirectory() as tmp:
        cl = os.path.join(tmp, 'CHANGELOG.md')
        with open(cl, 'w', encoding='utf-8') as f:
            # REUSE-IgnoreStart
            f.write('<!--\nSPDX-FileCopyrightText: x\n' * 20000 + '<!--' + ' \n' * 50000)
            # REUSE-IgnoreEnd
        check(quick('20000 unclosed SPDX comment starts', lambda: spdx_comment(cl)) == '',
              'an SPDX comment that is never closed is not taken')
        with open(cl, 'w', encoding='utf-8') as f:
            f.write('<!--x' * 200000)
        check(quick('200000 comment starts that are not an SPDX comment', lambda: spdx_comment(cl)) == '',
              'a file with no SPDX comment gives none')
    print(f'blog selftest: {len(fails)} failure(s)')
    return 1 if fails else 0


# ------------------------------------------------- feed and release posts (B)
#
# Part B: write_feed, which build calls when it is defined, and the
# release-post subcommand. Nothing above this line is changed by part B.

import email.utils
import xml.etree.ElementTree as ET

# The channel link: the address .github/workflows/pages.yml deploys to.
SITE_URL = 'https://kit.bridleworks.org/'
FEED_DESCRIPTION = 'Changes to the toothpaste kit, each post with its full text.'
CONTENT_NS = 'http://purl.org/rss/1.0/modules/content/'
# A post's guid is its slug under this prefix: stable across builds and
# hosts, and changed only by renaming the post's file.
GUID_PREFIX = 'tp-kit-blog:'


def post_url(slug):
    """A post's page on the site: the item link a feed reader opens."""
    return f'{SITE_URL}{slug}.html'
# Characters XML 1.0 cannot carry at all, even escaped.
XML_BAD_CHAR = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f\ufffe\uffff]')
RFC822_RE = re.compile(r'^(Mon|Tue|Wed|Thu|Fri|Sat|Sun), \d{2} '
                       r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{4} '
                       r'\d{2}:\d{2}:\d{2} (GMT|[+-]\d{4})$')


def rfc822(day):
    """A post's date as RFC 822, at midnight UTC: the posts carry no time."""
    return email.utils.format_datetime(
        datetime.datetime(day.year, day.month, day.day, tzinfo=datetime.timezone.utc), usegmt=True)


def feed_xml(posts):
    """RSS 2.0 for posts (newest first), each item with its whole body in
    content:encoded. Raises BlogError for text XML cannot carry."""
    bad = [f'{p["slug"]}: {k} holds a character XML 1.0 cannot carry'
           for p in posts for k in ('title', 'summary', 'html') if XML_BAD_CHAR.search(p[k])]
    if bad:
        raise BlogError(bad)
    ET.register_namespace('content', CONTENT_NS)
    rss = ET.Element('rss', version='2.0')
    channel = ET.SubElement(rss, 'channel')
    for tag, text in (('title', SITE_TITLE), ('link', SITE_URL),
                      ('description', FEED_DESCRIPTION), ('language', 'en')):
        ET.SubElement(channel, tag).text = text
    if posts:
        # The newest post's date, not the clock: the same posts give the same feed.
        ET.SubElement(channel, 'lastBuildDate').text = rfc822(max(p['date'] for p in posts))
    for p in posts:
        item = ET.SubElement(channel, 'item')
        ET.SubElement(item, 'title').text = p['title']
        ET.SubElement(item, 'link').text = post_url(p['slug'])
        ET.SubElement(item, 'description').text = p['summary']
        ET.SubElement(item, 'pubDate').text = rfc822(p['date'])
        ET.SubElement(item, 'guid', isPermaLink='false').text = GUID_PREFIX + p['slug']
        ET.SubElement(item, f'{{{CONTENT_NS}}}encoded').text = p['html']
    ET.indent(rss)
    return '<?xml version="1.0" encoding="utf-8"?>\n' + ET.tostring(rss, encoding='unicode') + '\n'


def write_feed(posts, out_dir):
    """Write OUT/feed.xml. build calls this after the pages are written."""
    with open(os.path.join(out_dir, 'feed.xml'), 'w', encoding='utf-8') as f:
        f.write(feed_xml(posts))


def feed_problems(text, posts):
    """What is wrong with a feed for these posts: well-formed XML, the RSS 2.0
    required elements (rss version, channel title, link and description; an
    item's title or description), and this blog's own promises (one item
    per post in order, a link to the post's page, a unique guid, an RFC
    822 pubDate on the post's date, the whole body in content:encoded). Empty when nothing is.
    A feed with a DOCTYPE is refused before parsing, so no entity it
    declares is ever expanded; this blog's feed never carries one."""
    if '<!DOCTYPE' in text:
        return ['a DOCTYPE is refused, so no entity can be expanded']
    try:
        root = ET.fromstring(text)
    except ET.ParseError as e:
        return [f'not well-formed XML: {e}']
    probs = []
    if root.tag != 'rss' or root.get('version') != '2.0':
        probs.append('the root is not <rss version="2.0">')
    channel = root.find('channel')
    if channel is None:
        return probs + ['no channel element']
    for tag in ('title', 'link', 'description'):
        if not (channel.findtext(tag) or '').strip():
            probs.append(f'the channel has no {tag}')
    items = channel.findall('item')
    if len(items) != len(posts):
        probs.append(f'{len(items)} items for {len(posts)} posts')
    guids = []
    for n, (item, p) in enumerate(zip(items, posts), 1):
        if p['title'] != item.findtext('title'):
            probs.append(f'item {n} is not the post {p["slug"]} (posts go newest first)')
        if not ((item.findtext('title') or '').strip() or (item.findtext('description') or '').strip()):
            probs.append(f'item {n} has neither title nor description')
        if item.findtext('link') != post_url(p['slug']):
            probs.append(f'item {n} link is not the page of {p["slug"]}')
        guid = (item.findtext('guid') or '').strip()
        if not guid:
            probs.append(f'item {n} has no guid')
        guids.append(guid)
        date = item.findtext('pubDate') or ''
        if not RFC822_RE.match(date):
            probs.append(f'item {n} pubDate {date!r} is not RFC 822')
        elif email.utils.parsedate_to_datetime(date).date() != p['date']:
            probs.append(f'item {n} pubDate {date!r} is not the post date {p["date"]}')
        if item.findtext(f'{{{CONTENT_NS}}}encoded') != p['html']:
            probs.append(f'item {n} content:encoded is not the whole post body')
    if len(set(g for g in guids if g)) != len([g for g in guids if g]):
        probs.append('two items share a guid')
    return probs


# A released version's CHANGELOG heading: "## 0.4.0 (2026-10-13)".
RELEASE_HEAD = re.compile(r'^## (\S+) \((\d{4}-\d{2}-\d{2})\)\s*$')
CHANGELOG = os.path.join(ROOT, 'CHANGELOG.md')


def changelog_section(changelog, version):
    """(date, section lines) for version, without its heading and up to the
    next ## heading or the file's closing comment."""
    if version.lower() == 'unreleased':
        raise BlogError([f'{changelog}: Unreleased has no date yet; release-post drafts a released version'])
    with open(changelog, encoding='utf-8') as f:
        lines = f.read().split('\n')
    for i, line in enumerate(lines):
        m = RELEASE_HEAD.match(line)
        if m and m.group(1) == version:
            body = []
            for later in lines[i + 1:]:
                if later.startswith('## ') or later.startswith('<!--'):
                    break
                body.append(later)
            while body and not body[0].strip():
                body.pop(0)
            while body and not body[-1].strip():
                body.pop()
            return m.group(2), body
    raise BlogError([f'{changelog}: no "## {version} (YYYY-MM-DD)" section'])


def spdx_comment(changelog):
    """The CHANGELOG's closing SPDX comment, so the draft carries the same header."""
    with open(changelog, encoding='utf-8') as f:
        text = f.read()
    # The first <!-- followed by whitespace that ends in a newline, then the
    # tag at the start of that line, up to the next -->, found in one pass: the
    # regex this replaces, <!--\s*\n...:.*?-->, could take quadratic time on
    # many unclosed starts. Each whitespace run is walked once, since the next
    # <!-- is searched for from where the walk began and cannot be whitespace.
    # REUSE-IgnoreStart
    tag = 'SPDX-FileCopyrightText:'
    # REUSE-IgnoreEnd
    start = text.find('<!--')
    while start != -1:
        after = start + 4
        at = after
        while at < len(text) and text[at].isspace():
            at += 1
        if at > after and text[at - 1] == '\n' and text.startswith(tag, at):
            end = text.find('-->', at + len(tag))
            return text[start:end + 3] if end != -1 else ''
        start = text.find('<!--', after)
    return ''


def draft_text(version, date, section, spdx):
    """The draft post: a front block marked DRAFT, a comment saying where it
    came from, and the section with its headings raised one level, since a
    post's body starts at ##."""
    body, fence = [], False
    for line in section:
        if line.startswith('```'):
            fence = not fence
        if not fence and re.match(r'^#{3,6} ', line):
            line = line[1:]
        body.append(line)
    return '\n'.join([
        '---',
        f'title: DRAFT: Release {version}',
        f'date: {date}',
        f'summary: DRAFT: one sentence on what {version} changed, for the index.',
        '---',
        '',
        '<!--',
        f'Drafted by scripts/blog.py release-post from CHANGELOG.md, section {version}.',
        'Edit before building: write the title and summary, cut what a reader does not',
        'need, and keep every claim traceable to a file in the tree at this date.',
        '-->',
        '',
        f'The CHANGELOG entry for {version}, dated {date}:',
        '',
    ] + body + ([''] + [spdx] if spdx else []) + [''])


def release_post(version, changelog=CHANGELOG, posts_dir=POSTS_DIR):
    """Write the draft for version into posts_dir. Returns (path, refusals):
    the converter's refusals of the draft, for the person to edit. Raises
    BlogError, writing nothing, when there is no section or the post exists."""
    version = version[1:] if re.match(r'^v\d', version) else version
    if not re.match(r'^[A-Za-z0-9._-]+$', version):
        raise BlogError([f'version {version!r} has a character a post name cannot hold'])
    date, section = changelog_section(changelog, version)
    path = os.path.join(posts_dir, f'{date}-v{version}.md')
    if os.path.exists(path):
        raise BlogError([f'{path}: already exists; release-post never overwrites a post'])
    text = draft_text(version, date, section, spdx_comment(changelog))
    os.makedirs(posts_dir, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    lines = text.split('\n')
    try:
        _front, body_at = parse_front(path, lines)
        convert(path, lines[body_at:], body_at + 1)
        refusals = []
    except BlogError as e:
        refusals = e.args[0]
    return path, refusals


# Feeds feed_problems must refuse, each made from a good feed by one change:
# (name, (old, new) applied once to the good feed's text, fragment wanted).
FEED_PLANTED = [
    ('not well-formed', ('</channel>', '</chanel>'), 'not well-formed XML'),
    ('wrong rss version', ('version="2.0"', 'version="0.91"'), 'not <rss version="2.0">'),
    ('no channel title', ('<title>tp-kit blog</title>', ''), 'the channel has no title'),
    ('no channel link', (f'<link>{SITE_URL}</link>', ''), 'the channel has no link'),
    ('no channel description', (f'<description>{FEED_DESCRIPTION}</description>', ''), 'the channel has no description'),
    ('pubDate not RFC 822', ('<pubDate>Tue, 20 Oct 2026 00:00:00 GMT</pubDate>', '<pubDate>2026-10-20</pubDate>'),
     'is not RFC 822'),
    ('pubDate on another day', ('<pubDate>Tue, 20 Oct 2026 00:00:00 GMT</pubDate>',
                                '<pubDate>Wed, 21 Oct 2026 00:00:00 GMT</pubDate>'), 'is not the post date'),
    ('item link to another post', (f'<link>{post_url("2026-10-20-later")}</link>',
                                   f'<link>{post_url("2026-10-13-good")}</link>'), 'link is not the page of'),
    ('no guid', (f'<guid isPermaLink="false">{GUID_PREFIX}2026-10-20-later</guid>', ''), 'has no guid'),
    ('duplicate guid', (f'{GUID_PREFIX}2026-10-20-later<', f'{GUID_PREFIX}2026-10-13-good<'), 'share a guid'),
    ('body cut short', ('&lt;h2&gt;What changed&lt;/h2&gt;\n', ''), 'not the whole post body'),
    ('item without title or description',
     (f'<title>Later &amp; newer</title>\n      <link>{post_url("2026-10-20-later")}</link>\n'
      '      <description>S</description>', f'<link>{post_url("2026-10-20-later")}</link>'),
     'neither title nor description'),
]
FEED_REQUIRED = ('not well-formed', 'wrong rss version', 'no channel title', 'no channel link',
                 'no channel description', 'pubDate not RFC 822', 'pubDate on another day', 'item link to another post', 'no guid',
                 'duplicate guid', 'body cut short', 'item without title or description')

# REUSE-IgnoreStart
CHANGELOG_SAMPLE = """# Changelog

## Unreleased

### Added

- Not yet.

## 1.2.0 (2026-10-27)

Released with a `tool`.

### Added

- `scripts/x.py`: does x.

### Fixed

- A crash in [y](docs/y.md).

## 1.1.0 (2026-10-13)

### Added

- Older.

<!--
SPDX-FileCopyrightText: 2026 Someone

SPDX-License-Identifier: Apache-2.0
-->
"""
# REUSE-IgnoreEnd


def feed_selftest():
    """Part B's checks: the feed for the two-post sample, the planted
    feeds, and release-post. Returns the failures."""
    fails = []

    def check(ok, what):
        print(('PASS ' if ok else 'FAIL ') + what)
        if not ok:
            fails.append(what)

    names = [c[0] for c in FEED_PLANTED]
    check(all(r in names for r in FEED_REQUIRED), 'the planted feeds for each required check are all present')
    with tempfile.TemporaryDirectory() as tmp:
        posts = os.path.join(tmp, 'posts')
        os.mkdir(posts)
        with open(os.path.join(posts, '2026-10-13-good.md'), 'w') as f:
            f.write(GOOD)
        with open(os.path.join(posts, '2026-10-20-later.md'), 'w') as f:
            f.write(front(title='Later & newer', date='2026-10-20'))
        out = os.path.join(tmp, 'out')
        got = build(out, posts)
        check('feed.xml' in os.listdir(out), 'build writes feed.xml')
        text = open(os.path.join(out, 'feed.xml'), encoding='utf-8').read()
        probs = feed_problems(text, got)
        check(not probs, 'the two-post feed parses and has every required element'
              + ('' if not probs else f' (got: {probs})'))
        index = open(os.path.join(out, 'index.html')).read()
        check('href="feed.xml"' in index, 'the pages link the feed')
        check(rfc822(datetime.date(2026, 10, 20)) == 'Tue, 20 Oct 2026 00:00:00 GMT', 'dates are RFC 822 at midnight GMT')
        out2 = os.path.join(tmp, 'out2')
        build(out2, posts)
        check(open(os.path.join(out2, 'feed.xml'), encoding='utf-8').read() == text,
              'the same posts give the same feed, byte for byte')
        check(not feed_problems(feed_xml([]), []), 'no posts give a valid empty feed')
        try:
            feed_xml([dict(got[0], title='bad \x01')])
            msg = ''
        except BlogError as e:
            msg = '\n'.join(e.args[0])
        check('cannot carry' in msg, 'a control character XML cannot carry is refused')
        for name, (old, new), want in FEED_PLANTED:
            ok_once = text.count(old) == 1
            probs = feed_problems(text.replace(old, new), got) if ok_once else []
            hit = any(want in p for p in probs)
            check(ok_once and hit, f'planted feed {name} is refused'
                  + ('' if hit else f' (old text found {text.count(old)} time(s); got: {probs})'))

        cl = os.path.join(tmp, 'CHANGELOG.md')
        with open(cl, 'w') as f:
            f.write(CHANGELOG_SAMPLE)
        drafts = os.path.join(tmp, 'drafts')
        path, refusals = release_post('v1.2.0', cl, drafts)
        check(os.path.basename(path) == '2026-10-27-v1.2.0.md', 'release-post names the draft with the release date first')
        check(not refusals, 'the draft converts' + ('' if not refusals else f' (got: {refusals})'))
        draft = open(path).read()
        check('## Added' in draft and '## Fixed' in draft and '### ' not in draft,
              'the section headings are raised one level')
        check('Older.' not in draft and 'Not yet.' not in draft, 'only the version asked for is drafted')
        # REUSE-IgnoreStart
        check('SPDX-License-Identifier: Apache-2.0' in draft, 'the draft carries the SPDX header')
        # REUSE-IgnoreEnd
        drafted = load_posts(drafts)
        check(len(drafted) == 1 and drafted[0]['title'].startswith('DRAFT'), 'the draft loads as a post marked DRAFT')
        for label, version, want in (('the existing draft is not overwritten', '1.2.0', 'already exists'),
                                     ('a missing version is refused', '9.9.9', 'no "## 9.9.9'),
                                     ('Unreleased is refused', 'Unreleased', 'has no date yet'),
                                     ('a version with a slash is refused', '1/2', 'cannot hold')):
            try:
                release_post(version, cl, drafts)
                msg = ''
            except BlogError as e:
                msg = '\n'.join(e.args[0])
            check(want in msg, label + ('' if want in msg else f' (got: {msg or "no error"})'))
    bomb = ('<?xml version="1.0"?><!DOCTYPE rss [<!ENTITY a "' + 'a' * 1000 + '">'
            + ''.join(f'<!ENTITY a{i} "' + '&a;' * 10 + '">' for i in range(5))
            + ']><rss version="2.0"><channel>&a4;</channel></rss>')
    check(feed_problems(bomb, []) == ['a DOCTYPE is refused, so no entity can be expanded'],
          'a feed with a DOCTYPE is refused before it is parsed')
    bad = [chr(c) for c in list(range(0x00, 0x09)) + [0x0b, 0x0c] + list(range(0x0e, 0x20))] + ['\ufffe', '\uffff']
    good_chars = ['\t', '\n', '\r', ' ', '~', '\ud7ff', '\ue000', '\ufffd']
    check(all(XML_BAD_CHAR.search(c) for c in bad) and not any(XML_BAD_CHAR.search(c) for c in good_chars),
          'XML_BAD_CHAR holds exactly the characters XML 1.0 cannot carry, U+FFFE and U+FFFF included')
    import time
    t0 = time.perf_counter()
    XML_BAD_CHAR.search('a' * 1000000)
    took = time.perf_counter() - t0
    check(took < 1.0, f'XML_BAD_CHAR on a clean 1000000-character text, in {took:.3f} s')
    return fails


def selftest_all():
    """Part A's selftest, then part B's. Part A's swaps write_feed for a
    stub and deletes it, so the real one is put back before part B runs."""
    real = write_feed
    try:
        code = selftest()
    finally:
        globals()['write_feed'] = real
    fails = feed_selftest()
    print(f'feed selftest: {len(fails)} failure(s)')
    return 1 if code or fails else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--selftest', action='store_true', help='run the planted cases')
    sub = ap.add_subparsers(dest='cmd')
    b = sub.add_parser('build', help='build the site into OUT')
    b.add_argument('out')
    b.add_argument('--posts', default=POSTS_DIR, help='posts directory (default: blog/posts)')
    r = sub.add_parser('release-post', help="draft a post from VERSION's CHANGELOG section")
    r.add_argument('version', metavar='VERSION')
    args = ap.parse_args()
    if args.selftest:
        return selftest_all()
    if args.cmd == 'release-post':
        try:
            path, refusals = release_post(args.version)
        except BlogError as e:
            for msg in e.args[0]:
                print(msg, file=sys.stderr)
            return 1
        print(f'blog: drafted {path}; edit it before building')
        for msg in refusals:
            print(f'blog: the converter refuses, edit this: {msg}', file=sys.stderr)
        return 0
    if args.cmd == 'build':
        try:
            posts = build(args.out, args.posts)
        except BlogError as e:
            for msg in e.args[0]:
                print(msg, file=sys.stderr)
            return 1
        print(f'blog: {len(posts)} post(s) built into {args.out}')
        return 0
    ap.print_usage(sys.stderr)
    return 2


if __name__ == '__main__':
    sys.exit(main())
