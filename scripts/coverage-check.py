#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2026 Aidan Naveja
#
# SPDX-License-Identifier: Apache-2.0

"""Hold each script's test coverage at a floor.

The gates selftest is this repository's test suite: most scripts carry their
own selftest, and `scripts/gates.sh --selftest` runs them. This runs that
suite under coverage.py and compares each script's statement coverage with its
floor in `.coverage-thresholds.json`. It fails when a script measures under its
floor, when a script the suite ran has no floor, or when a floor names a script
nothing ran, so a new script cannot arrive untested and a selftest cannot be
dropped unseen.

Usage: scripts/coverage-check.py             measure and compare
       scripts/coverage-check.py --selftest  the comparison against planted cases

Needs coverage.py and its startup hook, which the verification image installs
(containers/verify/); run it there, from a copy of the tree, as
.github/workflows/containers.yml does. Every python3 process the suite starts
records coverage through the hook while COVERAGE_PROCESS_START is set. The
selftests run copies of the tree, so each copy's scripts/ is mapped back to
this one's. A floor is a whole percentage, the measurement truncated, so the
two architectures' measurements need not agree past the decimal point.

Does not measure: shell scripts, which coverage.py cannot read, and whether a
covered line is checked by anything, which only mutation testing shows. A
planted copy that runs a script's own selftest counts toward that script, since
copies are mapped back by path, so a floor catches a selftest dropped from the
suite with its plant, and not one replaced while its plant still runs.
"""

import json
import os
import subprocess
import sys
import tempfile

THRESHOLDS = ".coverage-thresholds.json"


def load(text):
    """Return {script: floor} from the thresholds file's text, or raise ValueError."""
    data = json.loads(text)
    if not isinstance(data, dict) or not isinstance(data.get("scripts"), dict):
        raise ValueError('expected an object with a "scripts" object')
    floors = data["scripts"]
    for name, floor in floors.items():
        if not name.startswith("scripts/"):
            raise ValueError("%s: not under scripts/" % name)
        if type(floor) is not int or not 0 <= floor <= 100:
            raise ValueError("%s: floor must be a whole number from 0 to 100" % name)
    return floors


def compare(floors, measured):
    """Return one line per problem; none means every floor holds."""
    problems = []
    for name, floor in sorted(floors.items()):
        if name not in measured:
            problems.append("%s: has a floor of %d%% but the suite never ran it" % (name, floor))
        elif int(measured[name]) < floor:
            problems.append("%s: %.1f%% is under its floor of %d%%" % (name, measured[name], floor))
    for name in sorted(set(measured) - set(floors)):
        problems.append("%s: measured %.1f%% and has no floor" % (name, measured[name]))
    return problems


def measure(root):
    """Run the gates selftest under coverage; return {script: percent}."""
    import coverage

    tmp = tempfile.mkdtemp(prefix="coverage-check-")
    rc = os.path.join(tmp, "coveragerc")
    with open(rc, "w") as f:
        f.write("[run]\nparallel = True\ndata_file = %s\ninclude = */scripts/*\n"
                "[paths]\nsource =\n    %s\n    */scripts/\n"
                % (os.path.join(tmp, ".coverage"), os.path.join(root, "scripts")))
    env = dict(os.environ, COVERAGE_PROCESS_START=rc)
    run = subprocess.run(["./scripts/gates.sh", "--selftest"], cwd=root, env=env,
                         stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    if run.returncode != 0:
        sys.exit("coverage-check: gates.sh --selftest exit %d; run it alone to see why"
                 % run.returncode)
    cov = coverage.Coverage(config_file=rc)
    cov.combine()
    if not cov.get_data().measured_files():
        sys.exit("coverage-check: no coverage recorded; is the startup hook installed?")
    measured = {}
    for path in cov.get_data().measured_files():
        _, statements, _, missing, _ = cov.analysis2(path)
        if statements:
            name = os.path.relpath(path, root)
            measured[name] = 100.0 * (len(statements) - len(missing)) / len(statements)
    return measured


def selftest():
    fails = 0

    def check(name, got, want):
        nonlocal fails
        ok = got == want
        print("%s %s" % ("PASS" if ok else "FAIL", name))
        if not ok:
            print("  got %r, want %r" % (got, want))
            fails += 1

    floors = {"scripts/a.py": 90, "scripts/b": 50}
    check("every floor met is clean", compare(floors, {"scripts/a.py": 95.0, "scripts/b": 50.0}), [])
    check("a measurement at the floor plus a fraction is clean",
          compare(floors, {"scripts/a.py": 90.9, "scripts/b": 50.0}), [])
    check("a script under its floor fails", len(compare(floors, {"scripts/a.py": 89.9, "scripts/b": 60.0})), 1)
    check("a script with no floor fails", len(compare(floors, {"scripts/a.py": 95.0, "scripts/b": 60.0,
                                                              "scripts/c.py": 10.0})), 1)
    check("a floor nothing ran fails", len(compare(floors, {"scripts/a.py": 95.0})), 1)
    check("a well-formed file loads", load('{"scripts": {"scripts/a.py": 90}}'), {"scripts/a.py": 90})
    for name, text in [("a floor over 100 is refused", '{"scripts": {"scripts/a.py": 101}}'),
                       ("a fractional floor is refused", '{"scripts": {"scripts/a.py": 90.5}}'),
                       ("a boolean floor is refused", '{"scripts": {"scripts/a.py": true}}'),
                       ("a path outside scripts/ is refused", '{"scripts": {"a.py": 90}}'),
                       ("a file with no scripts object is refused", '{"a.py": 90}')]:
        try:
            load(text)
            got = "loaded"
        except ValueError:
            got = "refused"
        check(name, got, "refused")
    with open(THRESHOLDS) as f:
        try:
            load(f.read())
            got = "loaded"
        except ValueError as e:
            got = str(e)
    check("this repository's thresholds file loads", got, "loaded")
    print("FAILS: %d" % fails)
    return 1 if fails else 0


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root)
    if sys.argv[1:] == ["--selftest"]:
        return selftest()
    if sys.argv[1:]:
        sys.exit(__doc__)
    with open(THRESHOLDS) as f:
        floors = load(f.read())
    measured = measure(root)
    for name in sorted(measured):
        print("%-36s %5.1f%%  floor %s" % (name, measured[name], floors.get(name, "none")))
    problems = compare(floors, measured)
    for p in problems:
        print("FAIL " + p)
    if problems:
        return 1
    print("coverage-check: %d scripts at or over their floors" % len(floors))
    return 0


if __name__ == "__main__":
    sys.exit(main())
