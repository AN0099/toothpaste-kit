#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2026 Aidan Naveja
#
# SPDX-License-Identifier: Apache-2.0

"""Keep a command-line path argument inside a root directory.

usage: scripts/cli_path.py --selftest

A script that opens a path its user passed on the command line imports this
module and routes the argument through under(root, arg) before it opens
anything. under() joins arg to root, resolves symbolic links and `..` with
os.path.realpath, and returns the resolved path when it is realpath(root)
itself or lies below it. Any other path, whether through `..`, an absolute
path elsewhere or a symbolic link pointing out of root, prints
`cli_path: <arg> is outside <root>` to stderr and exits 2.

The check is a realpath followed by a plain startswith on realpath(root) plus
the path separator, then a separate equality test for root itself, written
out here rather than as Path.resolve() and is_relative_to or one combined
test, because that is the form CodeQL's Python analysis recognises as a path
check. The separator is what keeps a sibling such as `<root>-old`
out.

A script imports it by putting its own directory first on sys.path:

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from cli_path import under

--selftest checks a path inside, `..` escaping, an absolute path outside, a
symbolic link pointing outside, a sibling whose name starts with root's, and
root itself, then prints `cli_path selftest: N of N passed` and exits 1 on
any failure. Standard library only.
"""

import os
import sys

USAGE = "usage: scripts/cli_path.py --selftest"


def under(root, arg):
    """Return realpath(root/arg) if it is root or below it; else exit 2."""
    real_root = os.path.realpath(root)
    path = os.path.realpath(os.path.join(root, arg))
    # Two tests, not one `or`: CodeQL recognises only a plain startswith on
    # the value that is returned, so a combined guard, or a startswith on a
    # value other than `path`, leaves the path unchecked in its analysis.
    # Keep this shape.
    if path.startswith(real_root + os.sep):
        return path
    if path == real_root:
        return real_root
    print(f"cli_path: {arg} is outside {root}", file=sys.stderr)
    sys.exit(2)


def selftest():
    import contextlib
    import io
    import tempfile

    passed = 0
    total = 0
    with tempfile.TemporaryDirectory() as d:
        root = os.path.join(d, "root")
        os.makedirs(os.path.join(root, "sub"))
        os.makedirs(os.path.join(d, "root-old"))
        os.symlink(d, os.path.join(root, "out-link"))
        os.symlink(os.path.join(root, "sub"), os.path.join(root, "in-link"))
        real_root = os.path.realpath(root)

        def call(arg):
            err = io.StringIO()
            try:
                with contextlib.redirect_stderr(err):
                    return 0, under(root, arg), err.getvalue()
            except SystemExit as e:
                return e.code, None, err.getvalue()

        inside = [
            ("a path inside", "sub/f.json", os.path.join(real_root, "sub", "f.json")),
            ("a path inside through ..", "sub/../sub", os.path.join(real_root, "sub")),
            ("root itself", ".", real_root),
            ("root itself, as an empty argument", "", real_root),
            ("an absolute path inside", os.path.join(root, "sub"), os.path.join(real_root, "sub")),
            ("a symbolic link pointing inside", "in-link", os.path.join(real_root, "sub")),
        ]
        for name, arg, want in inside:
            code, got, err = call(arg)
            ok = code == 0 and got == want and err == ""
            total += 1
            passed += ok
            print(f"{'ok  ' if ok else 'FAIL'}  {name}: {arg!r}"
                  + ("" if ok else f" gave exit {code}, {got!r}, stderr {err!r}"))

        outside = [
            ("an escape through ..", "../root-old"),
            ("an escape through .. from below", "sub/../../x"),
            ("an absolute path outside", os.path.join(d, "root-old")),
            ("an absolute path outside, /", "/"),
            ("a symbolic link pointing outside", "out-link"),
            ("a path through a symbolic link pointing outside", "out-link/root-old"),
            ("a sibling whose name starts with root's", "../root-old/f"),
            ("the parent of root", ".."),
        ]
        for name, arg in outside:
            code, got, err = call(arg)
            want = f"cli_path: {arg} is outside {root}\n"
            ok = code == 2 and got is None and err == want
            total += 1
            passed += ok
            print(f"{'ok  ' if ok else 'FAIL'}  {name}: {arg!r}"
                  + ("" if ok else f" gave exit {code}, {got!r}, stderr {err!r}"))

    print(f"cli_path selftest: {passed} of {total} passed")
    return 0 if passed == total else 1


def main(argv):
    if argv == ["--selftest"]:
        return selftest()
    print(USAGE, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
