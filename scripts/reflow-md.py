#!/usr/bin/env python3
"""Unwrap hard-wrapped Markdown paragraphs to one line each.

Markdown collapses single newlines, so a hard wrap changes nothing about how a
document renders. What it does change is that the author's column width gets
baked into the file, and every reader inherits it: at 200% zoom, in a narrow
split, or through a screen reader. Unwrapping lets the text reflow to whatever
the reader actually has.

Paragraphs and list items are joined to a single line. Everything that depends
on its own line structure is left exactly as found:

  - fenced code blocks (``` and ~~~), including the fence lines
  - YAML front matter
  - ATX headings, and setext headings with their underline
  - tables
  - blockquotes
  - horizontal rules
  - HTML blocks
  - blank lines, which separate blocks

Known limits, stated rather than discovered later: indented (four-space) code
blocks are not detected, because they are ambiguous with list continuations, so
a document using them should be checked by eye. Hard line breaks made with two
trailing spaces are preserved as line breaks rather than joined.

Usage:
    reflow-md.py FILE...            rewrite in place
    reflow-md.py --check FILE...    report what would change, write nothing
    reflow-md.py --selftest         run the fixture, write nothing, exit nonzero on failure

The fixture is reflow-md.test.md next to this script, with the expected result
in reflow-md.expected.md. It covers every block type the reflow has to leave
alone. Two bugs were caught by it that the token-stream check above could not
see, because that check normalizes whitespace: a nested list item losing its
indentation, and a hard break losing the two trailing spaces that create it.
Both changed the rendered document while preserving every word. Run --selftest
after any change here.

Every rewrite is verified before it is written: the whitespace-normalized token
stream must be identical before and after. A file that fails verification is
left untouched and reported. Standard library only.
"""

import argparse
import difflib
import os
import re
import sys

FENCE = re.compile(r'^(\s*)(`{3,}|~{3,})')
LIST = re.compile(r'^(\s*)([-*+]\s+|\d+[.)]\s+)')
SETEXT = re.compile(r'^\s*(=+|-{2,})\s*$')
HRULE = re.compile(r'^\s*([-*_])(\s*\1){2,}\s*$')
TABLE = re.compile(r'^\s*\|')
QUOTE = re.compile(r'^\s*>')
HTML = re.compile(r'^\s*<')
HEADING = re.compile(r'^\s*#{1,6}\s')


def reflow(text):
    lines = text.split('\n')
    out, buf = [], []

    def joined(parts):
        # Keep the first line's indentation: a nested list item that loses it
        # gets promoted to top level, which changes the document.
        head = parts[0]
        indent = head[:len(head) - len(head.lstrip())]
        return indent + ' '.join(p.strip() for p in parts if p.strip())

    def flush():
        if buf:
            out.append(joined(buf))
            buf.clear()

    fence_close = None      # closing marker while inside a fenced block
    in_front = False
    in_list = False

    for i, line in enumerate(lines):
        # YAML front matter, only when it opens on the very first line
        if i == 0 and line.strip() == '---':
            in_front = True
            out.append(line)
            continue
        if in_front:
            out.append(line)
            if line.strip() == '---':
                in_front = False
            continue

        # fenced code: copy verbatim until the matching closer
        if fence_close is not None:
            out.append(line)
            if line.strip().startswith(fence_close):
                fence_close = None
            continue
        m = FENCE.match(line)
        if m:
            flush()
            in_list = False
            fence_close = m.group(2)[0] * 3
            out.append(line)
            continue

        if line.strip() == '':
            flush()
            in_list = False
            out.append('')
            continue

        # a setext underline belongs to the line above it
        if SETEXT.match(line) and buf and not in_list:
            tail = buf.pop()
            flush()
            out.append(tail.strip())
            out.append(line)
            continue

        if (HEADING.match(line) or HRULE.match(line) or TABLE.match(line)
                or QUOTE.match(line) or HTML.match(line)):
            flush()
            in_list = False
            out.append(line)
            continue

        if LIST.match(line):
            flush()
            in_list = True
            buf.append(line.rstrip())
            continue

        # A hard break (two trailing spaces) ends the joined line. The two
        # spaces are what cause the break, so they have to survive the join.
        if line.endswith('  '):
            buf.append(line)
            out.append(joined(buf) + '  ')
            buf.clear()
            continue

        # indented continuation of the current list item
        if in_list and line.startswith('  '):
            buf.append(line)
            continue

        if in_list:
            flush()
            in_list = False

        buf.append(line)

    flush()
    result = re.sub(r'\n{3,}', '\n\n', '\n'.join(out))
    return result.rstrip('\n') + '\n'


def tokens(text):
    """Whitespace-normalized token stream, for verifying nothing was lost."""
    return text.split()


def selftest():
    """Reflow the fixture and compare against the expected result.

    Never writes. Also checks idempotence: reflowing an already-unwrapped
    document must be a no-op, or repeated runs would keep changing the file.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    fixture = os.path.join(here, 'reflow-md.test.md')
    expected_path = os.path.join(here, 'reflow-md.expected.md')

    try:
        with open(fixture, encoding='utf-8') as fh:
            src = fh.read()
        with open(expected_path, encoding='utf-8') as fh:
            expected = fh.read()
    except OSError as err:
        print(f'selftest: cannot read fixture: {err}', file=sys.stderr)
        return 1

    ok = True

    got = reflow(src)
    if got != expected:
        ok = False
        print('FAIL  fixture output does not match expected:', file=sys.stderr)
        for line in difflib.unified_diff(
                expected.split('\n'), got.split('\n'),
                fromfile='expected', tofile='got', lineterm=''):
            print('  ' + line, file=sys.stderr)
    else:
        print('pass  fixture reflows to the expected output')

    if reflow(expected) != expected:
        ok = False
        print('FAIL  not idempotent: reflowing the expected output changed it',
              file=sys.stderr)
    else:
        print('pass  idempotent on already-unwrapped input')

    if tokens(src) != tokens(got):
        ok = False
        print('FAIL  token stream changed', file=sys.stderr)
    else:
        print('pass  token stream unchanged')

    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('files', nargs='*', metavar='FILE')
    ap.add_argument('--check', '-n', action='store_true',
                    help='report changes without writing')
    ap.add_argument('--selftest', action='store_true',
                    help='run the bundled fixture and exit')
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    if not args.files:
        ap.error('no files given')

    failed = False
    for path in args.files:
        try:
            with open(path, encoding='utf-8') as fh:
                before = fh.read()
        except OSError as err:
            print(f'error  {path}: {err}', file=sys.stderr)
            failed = True
            continue

        after = reflow(before)

        if tokens(before) != tokens(after):
            print(f'FAILED {path}: token stream changed, not written',
                  file=sys.stderr)
            failed = True
            continue

        if before == after:
            print(f'ok     {path} (already unwrapped)')
            continue

        n_before, n_after = len(before.split('\n')), len(after.split('\n'))
        if args.check:
            print(f'would  {path}: {n_before} -> {n_after} lines')
            continue

        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(after)
        print(f'wrote  {path}: {n_before} -> {n_after} lines')

    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
