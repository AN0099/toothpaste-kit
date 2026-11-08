#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2026 Aidan Naveja
#
# SPDX-License-Identifier: Apache-2.0

"""Fail a Markdown file that uses a BCP 14 keyword without saying so.

docs/document-layers.md states that MUST, SHOULD, MAY and their relatives
carry the force BCP 14 gives them only when written in capitals. A capital
keyword is therefore a requirement, and a reader can tell that only if the
file says its keywords are BCP 14. So a file that uses one must name BCP 14
outside code, as SECURITY-AI.md and docs/security-posture.md do, or be listed
in QUOTING, for a file that quotes keywords without stating requirements.

Coverage, stated because a check that does not state its coverage is not a
check: every *.md file under the root, outside .git, with fenced code blocks,
HTML comment blocks, inline code spans and inline HTML comments removed first,
so a keyword quoted as `MUST` is not a use and a statement a reader cannot see
does not count. They are read as CommonMark reads them. A fence opens at most
three spaces in, with no backtick in the rest of a backtick fence's line. A
comment block opens on a line starting <!-- and runs to the line holding -->.
Inside a paragraph, a backslash escapes the punctuation after it, a backtick
run opens a span only if a run of the same length closes it, and a comment
must close before the paragraph ends, all of which may run over lines; a
blank line, a quote or a list item ends the paragraph, and a heading ends the
lines before it. BCP 14 may
be wrapped over two lines. The keywords are the eleven of RFC 2119 as RFC
8174 reads them, in capitals and as whole words. It does NOT check files other
than Markdown (a comment in a workflow or a script is not read), whether a
keyword is used correctly, whether the BCP 14 statement is the full
boilerplate, or whether a lowercase "must" was meant as a requirement.
Indented code blocks, fences inside a blockquote or a list item, link
destinations, the content of <pre> and <code> elements and MAY as the month
are read as prose, so a keyword in one is reported although it is not a use.
Three silent misses remain, each hiding text a renderer shows. A paragraph's
lines are joined without reading tables or lazy continuation lines, so a span
or comment that opens in one table row and closes in a later one hides the
rows between. A span or comment that opens in a heading, or before a setext
underline, a thematic break or an item nested four or more spaces in, and
closes on a later line hides the lines between. Text after --> on a line that
holds a whole comment block is not read.

Usage: scripts/bcp14-check.py              check the tree
       scripts/bcp14-check.py --selftest   plant each case, then check the tree
"""

import os
import re
import sys
import tempfile

# Files that quote the keywords without stating a requirement. Empty: every
# file that uses one today names BCP 14. A file goes here only when naming
# BCP 14 in it would be false.
QUOTING = ()

KEYWORD = re.compile(
    r'\b(MUST NOT|MUST|REQUIRED|SHALL NOT|SHALL|SHOULD NOT|SHOULD|'
    r'NOT RECOMMENDED|RECOMMENDED|MAY|OPTIONAL)\b')
STATEMENT = re.compile(r'\bBCP\s+14\b')
FENCE = re.compile(r'^ {0,3}(`{3,}|~{3,})(.*)$')
COMMENT_BLOCK = re.compile(r'^ {0,3}<!--')
# A line that starts a block of its own, so a span or comment opened before
# it cannot run into it: a heading, a quote, a list item. A numbered line
# other than 1 continues a paragraph, as CommonMark reads it ("BCP" then
# "14." wrapped), and starts an item only in a run that is already a list.
BLOCK_START = re.compile(r'^ {0,3}(#{1,6}(\s|$)|>|[-+*](\s|$)|1[.)](\s|$))')
LIST_ITEM = re.compile(r'^ {0,3}([-+*]|[0-9]{1,9}[.)])(\s|$)')
PUNCT = set('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')


def blank_out(s):
    """Keep only the line breaks of removed text, so line numbers hold."""
    return '\n' * s.count('\n')


def closing_run(text, run, start):
    """Return where a backtick run of exactly len(run) starts, or -1."""
    k = start
    while True:
        k = text.find(run, k)
        if k < 0:
            return -1
        end = k + len(run)
        if text[k - 1] != '`' and (end == len(text) or text[end] != '`'):
            return k
        while end < len(text) and text[end] == '`':
            end += 1
        k = end


def strip_inline(text):
    """Remove code spans and HTML comments from one run of prose, left to
    right as CommonMark reads them: a backslash escapes the punctuation after
    it, a backtick run opens a span only if a run of the same length closes
    it, and a comment opened in the run must close inside it."""
    out, i = [], 0
    while i < len(text):
        if text[i] == '\\' and text[i + 1:i + 2] in PUNCT:
            out.append(text[i:i + 2])
            i += 2
        elif text[i] == '`':
            j = i
            while j < len(text) and text[j] == '`':
                j += 1
            k = closing_run(text, text[i:j], j)
            if k < 0:
                out.append(text[i:j])
                i = j
            else:
                out.append(blank_out(text[i:k]))
                i = k + j - i
        elif text.startswith('<!--', i):
            if text.startswith('<!-->', i):
                end = i + 5
            elif text.startswith('<!--->', i):
                end = i + 6
            else:
                k = text.find('-->', i + 4)
                end = k + 3 if k >= 0 else -1
            if end < 0:
                out.append('<!--')
                i += 4
            else:
                out.append(blank_out(text[i:end]))
                i = end
        else:
            out.append(text[i])
            i += 1
    return ''.join(out)


def prose_blocks(text):
    """Yield (first line number, text) for each run of prose lines outside
    fenced code and HTML comment blocks, with code spans and comments removed
    and line breaks kept."""
    fence, comment, runs, run = None, False, [], None
    for n, line in enumerate(text.splitlines(), 1):
        if fence is not None:
            close = FENCE.match(line)
            if (close and close.group(1)[0] == fence[0]
                    and len(close.group(1)) >= len(fence)
                    and close.group(2).strip() == ''):
                fence = None
            continue
        if comment:
            comment = '-->' not in line
            continue
        m = FENCE.match(line)
        if m and not (m.group(1)[0] == '`' and '`' in m.group(2)):
            fence, run = m.group(1), None
            continue
        if COMMENT_BLOCK.match(line):
            # A comment block ends on the line holding -->, which may be
            # the line it opens on; the whole line belongs to the block.
            comment, run = '-->' not in line, None
            continue
        if not line.strip():
            run = None
            continue
        if (run is None or BLOCK_START.match(line)
                or (LIST_ITEM.match(line) and LIST_ITEM.match(run[1][0]))):
            run = [n, []]
            runs.append(run)
        run[1].append(line)
    for first, lines in runs:
        yield first, strip_inline('\n'.join(lines))


def check_file(path):
    """Return the (line, keyword) uses in a file that never names BCP 14."""
    with open(path, encoding='utf-8') as f:
        text = f.read()
    uses, named = [], False
    for first, block in prose_blocks(text):
        if STATEMENT.search(block):
            named = True
        for offset, line in enumerate(block.split('\n')):
            uses.extend((first + offset, m.group(1)) for m in KEYWORD.finditer(line))
    return [] if named else uses


def check_tree(root, quoting=QUOTING):
    """Return 'file:line keyword' for each unstated use under root."""
    hits = []
    for top, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d != '.git')
        for name in sorted(files):
            if not name.endswith('.md'):
                continue
            path = os.path.join(top, name)
            rel = os.path.relpath(path, root)
            if rel in quoting:
                continue
            hits.extend(f'{rel}:{n} {kw}' for n, kw in check_file(path))
    return hits


def selftest():
    """Plant each case in a scratch tree; return the number of failures."""
    cases = [
        # (file text, quoting list, want a hit)
        ('A reader MUST check.\n', (), True),
        ('A reader MUST NOT check.\n', (), True),
        ('It is OPTIONAL.\n', (), True),
        ('Keywords are BCP 14.\n\nA reader MUST check.\n', (), False),
        ('A reader MUST check.\n\nKeywords are BCP 14.\n', (), False),
        ('Both criteria are `MUST`.\n', (), False),
        ('```\nA reader MUST check.\n```\n', (), False),
        ('~~~~\nA reader MUST check.\n~~~~\n', (), False),
        ('A reader must check.\n', (), False),
        ('MUSTER and MAYBE are words.\n', (), False),
        ('A reader MUST check.\n', ('a.md',), False),
        # BCP 14 named only inside code does not count as naming it.
        ('`BCP 14`\n\nA reader MUST check.\n', (), True),
        ('```\nBCP 14\n```\nA reader MUST check.\n', (), True),
        # An unclosed fence hides the rest, as Markdown renders it.
        ('```\nA reader MUST check.\n', (), False),
        # A fence closes only on a run as long as the opener, at most three
        # spaces in.
        ('````\n```\nA reader MUST check.\n````\n', (), False),
        ('```\n    ```\nA reader MUST check.\n', (), False),
        # Not fences: a span at the start of a line, and a tab before one.
        ('```x``` is a span.\n\nA reader MUST check.\n', (), True),
        ('\t```\n\nA reader MUST check.\n', (), True),
        # BCP 14 named only in an HTML comment does not count; a keyword
        # inside one is not a use.
        ('<!-- BCP 14 -->\n\nA reader MUST check.\n', (), True),
        ('<!--\nBCP 14\n-->\nA reader MUST check.\n', (), True),
        ('<!-- A reader MUST check. -->\n', (), False),
        ('Text <!--\nA reader MUST check.\n--> more.\n', (), False),
        # Not comments: unclosed in its run, indented code, inside a span,
        # escaped, and a comment opened in one paragraph or list item that
        # does not close there.
        ('Compare a <!-- b.\nA reader MUST check.\n', (), True),
        ('Text.\n\n    <!-- example\n\nA reader MUST check.\n', (), True),
        ('See `a <!--\nb` here.\nA reader MUST check.\n', (), True),
        ('Literal \\<!-- text.\n\nA reader MUST check.\n', (), True),
        ('a <!-- b\n\nA reader MUST check.\n\n--> c\n', (), True),
        ('- a <!-- b\n- A reader MUST check. -->\n', (), True),
        ('1. a <!-- b\n2. A reader MUST check. -->\n', (), True),
        # A comment ends at its first -->, even inside backticks, and the
        # two empty comments end where they open.
        ('<!-- see `-->` end\n\nA reader MUST check.\n', (), True),
        ('<!-->\nA reader MUST check.\n', (), True),
        ('<!--->\nA reader MUST check.\n', (), True),
        ('Text <!--> A reader MUST check. -->\n', (), True),
        ('Text <!---> A reader MUST check. -->\n', (), True),
        # A run closes only on a run of its own length, so a single
        # backtick is literal here and the double run is the span.
        ('`a`` MUST `` b\n', (), False),
        # Escaped backticks and an unbalanced run open no span.
        ('\\`MUST\\`\n', (), True),
        ('``MUST`\n', (), True),
        # A span over two lines is code; BCP 14 wrapped over two lines is
        # named.
        ('The word `MUST\nNOT` is quoted.\n', (), False),
        ('Keywords are BCP\n14.\n\nA reader MUST check.\n', (), False),
    ]
    failed = 0
    for i, (text, quoting, want) in enumerate(cases, 1):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, 'a.md'), 'w', encoding='utf-8') as f:
                f.write(text)
            got = bool(check_tree(d, quoting))
        if got == want:
            print(f'PLANT ok    case {i}: {"hit" if want else "no hit"}')
        else:
            print(f'PLANT FAIL  case {i}: wanted {"a hit" if want else "no hit"}, got the other')
            failed += 1
    # A keyword in a file that is not Markdown is outside the coverage.
    with tempfile.TemporaryDirectory() as d:
        with open(os.path.join(d, 'a.yml'), 'w', encoding='utf-8') as f:
            f.write('# a value MUST be exact\n')
        os.mkdir(os.path.join(d, '.git'))
        with open(os.path.join(d, '.git', 'a.md'), 'w', encoding='utf-8') as f:
            f.write('A reader MUST check.\n')
        if check_tree(d):
            print('PLANT FAIL  a .yml file or a file in .git was read')
            failed += 1
        else:
            print('PLANT ok    a .yml file and a file in .git are not read')
    return failed


def main(argv):
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
    if argv not in ([], ['--selftest']):
        print('usage: scripts/bcp14-check.py [--selftest]', file=sys.stderr)
        return 2
    if argv and selftest():
        print('bcp14-check: selftest FAILED')
        return 1
    hits = check_tree(root)
    for h in hits:
        print(h)
    if hits:
        print('bcp14-check: the files above use a BCP 14 keyword and never name BCP 14.'
              ' Name it, lowercase the word, or list a quoting file in QUOTING.')
        return 1
    print('bcp14-check: every file using a BCP 14 keyword names it')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
