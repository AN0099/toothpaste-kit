#!/usr/bin/env python3
"""Markdown structure checks for this repository.

Rule IDs and semantics are markdownlint's, read from a local capture of its
published rules document, so that swapping this for the real tool later is a
drop-in rather than a translation. Nothing is installed to run this: it is
standard library only.

Mirrors markdownlint 0.41.1, which has 53 rules. That count agrees across two
independent local sources, the published rules document and the library's own
per-rule documentation, so it is not one reading. 19 rules are implemented and
34 are listed as not implemented below, which accounts for all 53. A coverage
statement that does not add up to its whole field is the defect this file is
most concerned with, so the arithmetic is stated rather than implied.

Four rules have parameters whose defaults differ from the behaviour here, and
each is aligned in the CI configuration rather than left to diverge: MD009
br_spaces 0 rather than 2, MD010 code_blocks false, MD012 maximum 1, and
MD059's prohibited_texts extended from four entries to thirteen.

Why not markdownlint itself. The CI design note for this repository rejected
third party actions on the grounds that a gate workflow pulling unvetted code
from a registry is a supply chain surface attached to the thing meant to
increase trust. `npx markdownlint-cli2` fetches at run time and has that exact
shape, and adding a package manifest to a repository that deliberately ships
none is the other half of the same cost. So this implements a chosen subset.

COVERAGE. This is the part that matters, because a checker that does not say
what it covers is not a check.

Implemented, 19 rules:
  MD001 heading levels increment by one
  MD009 trailing spaces
  MD010 hard tabs
  MD011 reversed link syntax
  MD012 multiple consecutive blank lines
  MD018 no space after hash in an ATX heading
  MD019 multiple spaces after hash in an ATX heading
  MD023 headings start at the beginning of the line
  MD025 multiple top level headings in one document
  MD034 bare URL used
  MD036 emphasis used instead of a heading
  MD040 fenced code blocks have a language
  MD041 first line is a top level heading
  MD042 no empty links
  MD045 images have alternate text
  MD047 file ends with a single newline
  MD051 link fragments resolve to a heading in the same file
  MD056 table column count is consistent
  MD059 link text is descriptive

NOT implemented, and deliberately: MD003, MD004, MD005, MD007, MD013, MD014,
MD020, MD021, MD022, MD024, MD026, MD027, MD028, MD029, MD030, MD031, MD032,
MD033, MD035, MD037, MD038, MD039, MD043, MD044, MD046, MD048, MD049, MD050,
MD052, MD053, MD054, MD055, MD058, MD060. Most are style choices this
repository has not made. MD013 line length is owned by scripts/reflow-md.py,
which takes the opposite position on purpose. MD024 would fire on every
CHANGELOG, which repeats "Added" by design.

Four of the implemented rules exist here for accessibility rather than tidiness,
and each maps to a WCAG technique in docs/document-accessibility.md:
  MD001, MD025, MD041 -> G141, H42, G88, F25   heading structure and title
  MD045               -> G100, G82             text alternative for an image
  MD059, MD034        -> G91, H30, F84         link purpose from the link text
  MD056               -> H51, F91              table markup and headers

Five scoping rules, none of which loosens a rule, and each with a paired
positive in --selftest so that a rule not firing is distinguishable from a rule
that is broken:
  YAML frontmatter is removed before any rule runs. It is metadata, not markup,
  so a colon or a tab inside it is not a markdown defect. Reported line numbers
  stay absolute, so they point at the real line in the file.
  A title or name key in the frontmatter satisfies MD041, which is
  markdownlint's own front_matter_title option with a wider regex, since the
  skill and hook formats carry name rather than title.
  MD025 does not apply under skills/. A skill file uses one h1 per section and
  skill-creation's Required Sections rule depends on that shape. It applies
  everywhere else.
  Inline code spans are not parsed as markup, so documentation that quotes a
  bad pattern is not reported as an instance of it. MD056 is the deliberate
  exception: GFM splits a table row on every pipe, including one inside a code
  span, which is why the escaped form is required there and why MD056 has to
  read the raw line. An escaped pipe is cell content and is not counted.
  reflow-md's two fixture files are skipped by name. Their exact bytes are the
  thing under test, and editing them is the checker breaking the check.

Usage:
  scripts/mdlint.py [PATH ...]      check these files, or the whole repo
  scripts/mdlint.py --selftest      prove each rule fires, then check the repo
"""

import os
import re
import sys

# MD059: link text that says nothing on its own. F84 in WCAG terms.
VAGUE = {
    "here", "click here", "this", "this page", "link", "more", "read more",
    "learn more", "see more", "details", "info", "this link", "see here",
}

HEADING = re.compile(r'^(#{1,6})(\s*)(.*?)\s*$')
FENCE = re.compile(r'^(\s*)(`{3,}|~{3,})\s*(\S+)?')
IMAGE = re.compile(r'!\[([^\]]*)\]\(([^)]*)\)')
LINK = re.compile(r'(?<!!)\[([^\]]*)\]\(([^)]+)\)')
BARE_URL = re.compile(r'(?<![(<\[`])\bhttps?://[^\s<>)\]`"]+')
CODE_SPAN = re.compile(r'`[^`]*`')
# MD056 counts table cells, and in GFM a backslash-escaped pipe is cell content
# rather than a cell separator. markdownlint 0.41.1 gets this for free: lib/md056.mjs
# counts micromark tableData, tableHeader and tableDelimiter tokens rather than
# characters. This script reads lines, so the escape is removed before counting.
ESCAPED_PIPE = re.compile(r'(?<!\\)\\\|')
# MD011, reversed link syntax. The published rule states that Markdown Extra
# footnotes, (example)[^1], do not trigger it, so a destination beginning with
# a caret is excluded.
REVERSED_LINK = re.compile(r'(^|[^\\])\(([^()]+)\)\[([^\]^][^\]]*)\](?!\()')
FRONTMATTER_OPEN = re.compile(r'\A---\s*$')
FRONTMATTER_CLOSE = re.compile(r'^(---|\.\.\.)\s*$')
# markdownlint's MD041 has a front_matter_title option, a regex whose match
# in the frontmatter satisfies the rule. Its default is title only. Both the
# skill format and the hook format here carry name instead, so the pattern
# accepts either. This is markdownlint's mechanism with a wider regex, not a
# local exemption.
FRONTMATTER_TITLE = re.compile(r'^\s*(title|name)\s*[:=]')
EMPTY_LINK = re.compile(r'(?<!!)\[([^\]]*)\]\(\s*\)')
EMPH_ONLY = re.compile(r'^\s*(\*\*|__)(.+?)\1\s*$')
# markdownlint's MD036 does not fire when the emphasized text ends in
# punctuation, because that reads as a sentence or a lead-in to a list
# rather than as a heading. Mine fired on both and produced six false
# positives on this repository's own bold lead-ins.
MD036_PUNCT = '.,;:!?'
# A list marker is the character followed by a space. Testing for the
# bare character excluded every line of bold text, which is what made
# MD036 unable to fire on its own plant.
LIST_MARKER = re.compile(r'^\s*([-*+]\s|\d+[.)]\s|>|\|)')


def anchor(text):
    """GitHub's heading-to-anchor transform, close enough for MD051."""
    t = text.lower()
    t = re.sub(r'`([^`]*)`', r'\1', t)
    t = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', t)
    t = re.sub(r'[^\w\s-]', '', t)
    return re.sub(r'\s+', '-', t.strip())


def check(path, text):
    out = []
    def bad(line, rule, msg):
        out.append((path, line, rule, msg))

    lines = text.split('\n')
    if text and not text.endswith('\n'):
        bad(len(lines), 'MD047', 'file does not end with a newline')
    elif text.endswith('\n\n'):
        bad(len(lines), 'MD047', 'file ends with more than one newline')

    # Frontmatter is metadata, not markup. Its lines are removed from the body
    # before any rule runs, so a colon, a long line or an indented key inside it
    # is never read as markdown. Numbering stays absolute: body_start is the
    # count of frontmatter lines, and every reported line is a real line in the
    # file on disk.
    body_start = 0
    fm_has_title = False
    if lines and FRONTMATTER_OPEN.match(lines[0]):
        for j in range(1, len(lines)):
            if FRONTMATTER_CLOSE.match(lines[j]):
                body_start = j + 1
                break
        else:
            # An unterminated opener is not frontmatter. Lint the whole file.
            body_start = 0
        if body_start:
            fm_has_title = any(FRONTMATTER_TITLE.match(raw)
                               for raw in lines[1:body_start - 1])

    body = lines[body_start:]

    # MD025 asks for one top level heading per document. A skill file uses one
    # per section, and skills/skill-creation/SKILL.md's Required Sections rule
    # depends on that shape, so the rule does not apply under skills/. Stated
    # here and in COVERAGE above rather than left implicit.
    norm_path = path.replace('\\', '/').lstrip('./')
    md025_applies = not norm_path.startswith('skills/')

    in_fence = False
    fence_mark = None
    prev_level = 0
    seen_h1 = False
    first_content_seen = False
    headings = []
    blanks = 0

    for i, raw in enumerate(body, body_start + 1):
        fm = FENCE.match(raw)
        if fm and (not in_fence or raw.strip().startswith(fence_mark)):
            if not in_fence:
                in_fence, fence_mark = True, fm.group(2)[0] * 3
                if not fm.group(3):
                    bad(i, 'MD040', 'fenced code block has no language')
            else:
                in_fence, fence_mark = False, None
            # A fence line is content, so it breaks a run of blank lines. Not
            # resetting here counted the blank before a code block and the
            # blank after it as consecutive, which produced twenty-seven false
            # MD012 findings the moment the rule was tightened to markdownlint's
            # default of one.
            blanks = 0
            continue
        if in_fence:
            blanks = 0
            continue

        if raw.strip() == '':
            blanks += 1
            # markdownlint's MD012 default is maximum 1, so the second blank
            # line in a row is the violation. Verified against the rule's
            # published parameter list, not assumed.
            if blanks == 2:
                bad(i, 'MD012', 'more than one consecutive blank line')
            continue
        blanks = 0

        if raw != raw.rstrip():
            bad(i, 'MD009', 'trailing spaces')
        if '\t' in raw:
            bad(i, 'MD010', 'hard tab')

        stripped = raw.lstrip()
        if stripped.startswith('#') and raw[:len(raw) - len(stripped)]:
            bad(i, 'MD023', 'heading does not start at the beginning of the line')

        m = HEADING.match(raw)
        if m:
            level, gap, title = len(m.group(1)), m.group(2), m.group(3)
            if gap == '':
                bad(i, 'MD018', 'no space after hash')
            elif len(gap) > 1:
                bad(i, 'MD019', 'more than one space after hash')
            if level == 1:
                if seen_h1 and md025_applies:
                    bad(i, 'MD025', 'more than one top level heading')
                seen_h1 = True
            if not first_content_seen and level != 1 and not fm_has_title:
                bad(i, 'MD041', 'first content line is not a top level heading')
            if prev_level and level > prev_level + 1:
                bad(i, 'MD001', f'heading jumps from h{prev_level} to h{level}')
            prev_level = level
            headings.append(anchor(title))
            first_content_seen = True
            continue

        if not first_content_seen:
            if not fm_has_title:
                bad(i, 'MD041', 'first content line is not a top level heading')
            first_content_seen = True

        em = EMPH_ONLY.match(raw)
        if (em and len(em.group(2)) < 60 and not LIST_MARKER.match(raw)
                and em.group(2).rstrip()[-1:] not in MD036_PUNCT):
            bad(i, 'MD036', 'emphasis used on its own line instead of a heading')

        raw_nc = CODE_SPAN.sub(lambda m: ' ' * len(m.group(0)), raw)

        for alt, src in IMAGE.findall(raw_nc):
            if not alt.strip():
                bad(i, 'MD045', f'image has no alt text: {src[:40]}')

        for txt in EMPTY_LINK.findall(raw_nc):
            bad(i, 'MD042', f'empty link: [{txt[:30]}]')

        for txt, dest in LINK.findall(raw_nc):
            clean = re.sub(r'[`*_]', '', txt).strip().lower().rstrip('.,;:!?')
            if clean in VAGUE:
                bad(i, 'MD059', f'link text is not descriptive: "{txt[:30]}"')
            elif clean.startswith('http'):
                bad(i, 'MD059', 'link text is a URL rather than a description')

        for u in BARE_URL.findall(raw_nc):
            bad(i, 'MD034', f'bare URL: {u[:50]}')

        for _pre, txt, dest in REVERSED_LINK.findall(raw_nc):
            if txt.endswith('\\') or dest.endswith('\\'):
                continue
            bad(i, 'MD011', f'reversed link syntax: ({txt[:24]})[{dest[:24]}]')

    # MD056, table column count, and MD051, fragments, need the whole document.
    # The body only, and numbered from its real position, for the same reason as
    # the loop above: a pipe or a bracket inside frontmatter is not markup.
    rows, start = [], 0
    for i, raw in enumerate(body, body_start + 1):
        if raw.strip().startswith('|') and raw.strip().endswith('|'):
            if not rows:
                start = i
            rows.append((i, ESCAPED_PIPE.sub('', raw.strip()).count('|') - 1))
        else:
            if len(rows) >= 2:
                width = rows[0][1]
                for ln, w in rows:
                    if w != width:
                        bad(ln, 'MD056', f'table row has {w} cells, header has {width}')
            rows = []
    if len(rows) >= 2:
        width = rows[0][1]
        for ln, w in rows:
            if w != width:
                bad(ln, 'MD056', f'table row has {w} cells, header has {width}')

    for i, raw in enumerate(lines, 1):
        for _txt, dest in LINK.findall(raw):
            if dest.startswith('#') and anchor(dest[1:]) not in headings:
                bad(i, 'MD051', f'link fragment does not resolve: {dest}')

    return out


# Fixtures are excluded because their exact bytes are the thing under test.
# A bulk fix of MD040 and MD009 across the tree edited reflow-md's fixture
# pair and broke its selftest, which is the checker damaging the check.
SKIP = ('scripts/reflow-md.test.md', 'scripts/reflow-md.expected.md')


def gather(paths):
    files = []
    for p in paths:
        if os.path.isdir(p):
            for root, dirs, names in os.walk(p):
                dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules')]
                files += [os.path.join(root, n) for n in names if n.endswith('.md')]
        elif p.endswith('.md'):
            files.append(p)
    return sorted(f for f in files if not f.replace('./', '').endswith(SKIP))


def run(paths):
    findings = []
    files = gather(paths)
    for f in files:
        with open(f, encoding='utf-8') as fh:
            findings += check(f, fh.read())
    for path, line, rule, msg in findings:
        print(f'{path}:{line}: {rule} {msg}')
    print(f'\nmdlint: {len(files)} file(s), {len(findings)} finding(s)')
    return 1 if findings else 0


def selftest():
    """Every rule gets a planted positive. A rule that has never fired has not
    been shown capable of firing, and a clean run over a clean tree proves
    nothing about the rule."""
    cases = {
        'MD001': "# T\n\n### Skipped\n",
        'MD009': "# T\n\ntrailing   \n",
        'MD010': "# T\n\nhas\ttab\n",
        'MD011': "# T\n\n(reversed)[https://example.com]\n",
        'MD012': "# T\n\n\n\ntext\n",
        'MD018': "# T\n\n##Nospace\n",
        'MD019': "# T\n\n##  Twospaces\n",
        'MD023': "# T\n\n  ## Indented\n",
        'MD025': "# T\n\n# Second\n",
        'MD034': "# T\n\nsee https://example.com now\n",
        'MD036': "# T\n\n**Looks like a heading**\n",  # no trailing punctuation
        'MD040': "# T\n\n```\ncode\n```\n",
        'MD041': "Not a heading first\n",
        'MD042': "# T\n\n[text]()\n",
        'MD045': "# T\n\n![](img.png)\n",
        'MD047': "# T\n\nno newline",
        'MD051': "# T\n\n[go](#nope)\n",
        'MD056': "# T\n\n| a | b |\n|---|---|\n| 1 |\n",
        'MD059': "# T\n\n[here](x.md)\n",
    }
    ok = True
    for rule, body in cases.items():
        hits = {r for _p, _l, r, _m in check('<plant>', body)}
        if rule in hits:
            print(f'PLANT ok    {rule} fires on a planted positive')
        else:
            print(f'PLANT FAIL  {rule} did not fire (saw: {sorted(hits) or "nothing"})')
            ok = False
    # The frontmatter and path behaviour needs its own checks, because each one
    # is a rule NOT firing, and a rule that does not fire is indistinguishable
    # from a rule that is broken unless the same input is also shown to fire
    # without the exemption.

    # Frontmatter is not markdown. Every defect below is inside it.
    dirty_fm = ("---\nname: x\ndescription: see https://example.com\t  \n---\n"
                "\n# Title\n\nClean body.\n")
    fm_hits = {r for _p, _l, r, _m in check('docs/x.md', dirty_fm)}
    # The paired positive: the identical defects in the body DO fire, which is
    # what makes the clean result above mean something.
    dirty_body = "# Title\n\nsee https://example.com\t  \n"
    body_hits = {r for _p, _l, r, _m in check('docs/x.md', dirty_body)}
    if not fm_hits and {'MD009', 'MD010', 'MD034'} <= body_hits:
        print('EXEMPT ok   frontmatter is not linted, and the same bytes in the '
              'body still fire MD009, MD010 and MD034')
    else:
        print(f'EXEMPT FAIL frontmatter {sorted(fm_hits)}, body {sorted(body_hits)}')
        ok = False

    # MD056 counts cells, not pipe characters. An escaped pipe is content, so
    # the correctly escaped row must not fire; the same row with a real extra
    # cell must. Without the second half, a rule that never fires would pass.
    escaped = "# T\n\n| a | b |\n|---|---|\n| x \\| y | 2 |\n"
    extra = "# T\n\n| a | b |\n|---|---|\n| x | y | 2 |\n"
    e = {r for _p, _l, r, _m in check('docs/x.md', escaped)}
    x = {r for _p, _l, r, _m in check('docs/x.md', extra)}
    if 'MD056' not in e and 'MD056' in x:
        print('EXEMPT ok   MD056 treats an escaped pipe as content and still '
              'fires on a real extra cell')
    else:
        print(f'EXEMPT FAIL MD056 escaped {sorted(e)}, extra cell {sorted(x)}')
        ok = False

    # A title key in the frontmatter satisfies MD041, per markdownlint's
    # front_matter_title option. Without the key the same body fires it.
    with_name = "---\nname: x\n---\n\n## Section\n\nText.\n"
    without = "---\nother: x\n---\n\n## Section\n\nText.\n"
    a = {r for _p, _l, r, _m in check('docs/x.md', with_name)}
    b = {r for _p, _l, r, _m in check('docs/x.md', without)}
    if 'MD041' not in a and 'MD041' in b:
        print('EXEMPT ok   a name key satisfies MD041, and its absence fires it')
    else:
        print(f'EXEMPT FAIL MD041 with name {sorted(a)}, without {sorted(b)}')
        ok = False

    # MD025 is scoped by path, so the same content must pass under skills/ and
    # fail outside it. One of these alone proves nothing.
    two_h1 = "---\nname: x\n---\n\n# One\n\n# Two\n"
    inside = {r for _p, _l, r, _m in check('skills/x/SKILL.md', two_h1)}
    outside = {r for _p, _l, r, _m in check('docs/x.md', two_h1)}
    if 'MD025' not in inside and 'MD025' in outside:
        print('EXEMPT ok   MD025 is off under skills/ and on outside it')
    else:
        print(f'EXEMPT FAIL MD025 inside {sorted(inside)}, outside {sorted(outside)}')
        ok = False

    # A blank line, a fenced block, then another blank line is not two
    # consecutive blank lines. Paired with a real pair so the clean result is
    # not just the rule being broken.
    across = "# T\n\n```json\n{}\n```\n\nText.\n"
    real = "# T\n\n\nText.\n"
    a = {r for _p, _l, r, _m in check('docs/x.md', across)}
    b = {r for _p, _l, r, _m in check('docs/x.md', real)}
    if 'MD012' not in a and 'MD012' in b:
        print('EXEMPT ok   MD012 counts real consecutive blanks, not blanks '
              'separated by a fence')
    else:
        print(f'EXEMPT FAIL MD012 across a fence {sorted(a)}, real pair {sorted(b)}')
        ok = False

    # MD011 must not fire on Markdown Extra footnotes, which the published rule
    # states explicitly. Paired with a real reversal so the clean result means
    # something.
    fn = {r for _p, _l, r, _m in check('docs/x.md', "# T\n\nFor (example)[^1]\n")}
    rv = {r for _p, _l, r, _m in check('docs/x.md', "# T\n\n(bad)[https://x.com]\n")}
    if 'MD011' not in fn and 'MD011' in rv:
        print('EXEMPT ok   MD011 skips a footnote and fires on a real reversal')
    else:
        print(f'EXEMPT FAIL MD011 footnote {sorted(fn)}, reversal {sorted(rv)}')
        ok = False

    # Line numbers stay absolute. The defect is on line 7 of the file, and
    # reporting line 3 would send a reader to the frontmatter.
    offset = "---\nname: x\nkind: y\n---\n\n# Title\n\nhas\ttab\n"
    nums = [l for _p, l, r, _m in check('docs/x.md', offset) if r == 'MD010']
    if nums == [8]:
        print('EXEMPT ok   a body line number is the real file line, not an offset')
    else:
        print(f'EXEMPT FAIL MD010 reported at {nums}, expected [8]')
        ok = False

    clean = "# Title\n\nA paragraph.\n\n## Section\n\nMore text, see [the guide](g.md).\n"
    hits = check('<control>', clean)
    if hits:
        print(f'CONTROL FAIL  clean input produced {hits}')
        ok = False
    else:
        print('CONTROL ok  clean input produces nothing')
    if not ok:
        print('\nselftest: a rule could not be shown to fire. Do not trust a clean run.')
        return 1
    print('\nselftest: all rules fired on their plants. Now the real run.')
    return 0


if __name__ == '__main__':
    args = sys.argv[1:]
    if args and args[0] == '--selftest':
        rc = selftest()
        sys.exit(rc or run(args[1:] or ['.']))
    sys.exit(run(args or ['.']))
