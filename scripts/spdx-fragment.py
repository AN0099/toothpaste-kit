#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2026 Aidan Naveja
#
# SPDX-License-Identifier: Apache-2.0

"""Build an SPDX 3.0.1 JSON-LD fragment describing who assisted a commit range.

usage: scripts/spdx-fragment.py [--models PATH] <base>..<head>
       scripts/spdx-fragment.py --selftest

Reads every commit in <base>..<head> with `git log`, taking the `Assisted-by:`
and `Agent-Effort:` trailers (see CONTRIBUTING.md). One `Agent-Effort:` in a
commit applies to every model that commit's `Assisted-by:` trailers name.
Prints one JSON-LD document to stdout: a CreationInfo, a software_Package for
the kit, one Agent for the head commit's author plus one more for each
distinct supplier named in the models file, one ai_AIPackage per distinct
model, one Tool per distinct tool, and one Relationship of type usesTool from
the kit package to every AIPackage and Tool. Every element other than
CreationInfo carries a `creationInfo` reference back to it, and CreationInfo's
`createdBy` names the author Agent: a merge made on the hosting site has the
site as its committer, so the author is the person who made it.

The values the trailers cannot give (suppliedBy, downloadLocation, releaseTime,
packageVersion, autonomyType) come from the file at --models PATH (default
scripts/spdx-models.json), a JSON object keyed by model name. The file is read
only when the range names a model; then every entry in it is checked, whether
or not the range names that entry, before any output is printed: a file or
entry that is not an object, a missing key, a suppliedBy, downloadLocation or
packageVersion that is not a string, a releaseTime that is not a string
matching DateTime.html's pattern, or an autonomyType that is not "yes" or "no"
each exit 2, as does a file that is not UTF-8, not JSON, or past the JSON
parser's limits (an integer over 4300 digits, nesting too deep). A model
this run names but the file lacks exits 2 the same way, naming the model and
the file.

A range with no Assisted-by trailer prints the CreationInfo, the kit package
and the author Agent only, and exits 0. The range must be exactly
<base>..<head>, two dots; a three-dot range or any other form exits 2 with the
usage line. An Assisted-by value not of the form "<model> via <tool>/<version>"
exits 2, naming the commit and the value.

Standard library only.
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

DEFAULT_MODELS_PATH = "scripts/spdx-models.json"
CONTEXT_URL = "https://spdx.org/rdf/3.0.1/spdx-context.jsonld"
PACKAGE_NAME = "toothpaste-kit"
CREATION_INFO_ID = "_:creationinfo"
USAGE = (
    "usage: scripts/spdx-fragment.py [--models PATH] <base>..<head>\n"
    "       scripts/spdx-fragment.py --selftest"
)

FIELD_SEP = "\x1f"
VALUE_SEP = "\x1d"

REQUIRED_MODEL_KEYS = [
    "suppliedBy", "downloadLocation", "releaseTime", "packageVersion",
    "autonomyType",
]

# \Z, not $: $ also matches before a trailing newline.
RELEASE_TIME_RE = re.compile(r"^\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ\Z")
ASSISTED_BY_RE = re.compile(r"^(.+) via ([^/]+)/(.+)$")
DOT_RUN_RE = re.compile(r"\.\.+")


class BadRange(Exception):
    pass


class NoModelEntry(Exception):
    def __init__(self, model, models_path):
        super().__init__(f"spdx-fragment: no entry for {model} in {models_path}")


class ModelsValidationError(Exception):
    pass


class MalformedAssistedBy(Exception):
    def __init__(self, commit_hash, value):
        super().__init__(
            f"spdx-fragment: {commit_hash} has a malformed Assisted-by: {value}")


class GitError(Exception):
    pass


def git_output(cwd, args):
    result = subprocess.run(
        ["git"] + args, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        raise GitError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout


def to_utc_z(iso_str):
    dt = datetime.fromisoformat(iso_str)
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def iter_commits(cwd, range_arg):
    fmt = FIELD_SEP.join([
        "%H", "%cI",
        f"%(trailers:key=Assisted-by,valueonly,separator={VALUE_SEP})",
        f"%(trailers:key=Agent-Effort,valueonly,separator={VALUE_SEP})",
    ])
    # --reverse: oldest first, so a later commit's Agent-Effort for a model
    # overrides an earlier one, not the other way round.
    out = git_output(cwd, ["log", "--reverse", f"--format={fmt}", range_arg])
    # Split on "\n" only, not str.splitlines(): VALUE_SEP (\x1d, Group
    # Separator) is one of the control characters splitlines() also treats
    # as a line break, which would tear a multi-value trailers field apart.
    for line in out.split("\n"):
        if not line:
            continue
        commit_hash, ci, assisted, effort = line.split(FIELD_SEP)
        names = [v for v in assisted.split(VALUE_SEP) if v]
        yield commit_hash, ci, names, (effort or None)


def load_models(models_path):
    try:
        with open(models_path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError, RecursionError) as e:
        raise GitError(f"cannot read {models_path}: {e}")


def validate_models(models, models_path):
    if not isinstance(models, dict):
        raise ModelsValidationError(
            f"spdx-fragment: {models_path} is not a JSON object")
    for model in models:
        entry = models[model]
        if not isinstance(entry, dict):
            raise ModelsValidationError(
                f"spdx-fragment: {model} in {models_path} is not a JSON object")
        for key in REQUIRED_MODEL_KEYS:
            if key not in entry:
                raise ModelsValidationError(
                    f"spdx-fragment: {model} in {models_path} lacks {key}")
        for key in ("suppliedBy", "downloadLocation", "packageVersion"):
            if not isinstance(entry[key], str):
                raise ModelsValidationError(
                    f"spdx-fragment: {model} {key} is not a string")
        if not isinstance(entry["releaseTime"], str) or not RELEASE_TIME_RE.match(entry["releaseTime"]):
            raise ModelsValidationError(
                f"spdx-fragment: {model} releaseTime is not YYYY-MM-DDTHH:MM:SSZ")
        if entry["autonomyType"] not in ("yes", "no"):
            raise ModelsValidationError(
                f"spdx-fragment: {model} autonomyType is not yes or no")


def is_valid_range(s):
    runs = DOT_RUN_RE.findall(s)
    return (
        len(runs) == 1 and runs[0] == ".."
        and not s.startswith("..") and not s.endswith("..")
    )


def build_graph(cwd, range_arg, models_path):
    base, sep, head_ref = range_arg.partition("..")
    if not sep or not base or not head_ref:
        raise BadRange(range_arg)

    head_hash = git_output(cwd, ["rev-parse", "--verify", head_ref]).strip()
    head_ci = git_output(cwd, ["log", "-1", "--format=%cI", head_hash]).strip()
    created = to_utc_z(head_ci)
    author_name = git_output(
        cwd, ["log", "-1", "--format=%an", head_hash]).strip()

    model_order = []
    tool_order = []
    effort_by_model = {}
    for commit_hash, _ci, names, effort in iter_commits(cwd, range_arg):
        for raw in names:
            if not ASSISTED_BY_RE.match(raw):
                raise MalformedAssistedBy(commit_hash, raw)
            model, _via, tool_id = raw.partition(" via ")
            if model not in model_order:
                model_order.append(model)
            if tool_id and tool_id not in tool_order:
                tool_order.append(tool_id)
            if effort:
                effort_by_model[model] = effort

    agent_n = 1
    author_agent_id = f"urn:toothpaste-kit:{head_hash}:agent-{agent_n}"
    agent_n += 1

    graph = [{
        "type": "CreationInfo",
        "@id": CREATION_INFO_ID,
        "specVersion": "3.0.1",
        "created": created,
        "createdBy": [author_agent_id],
    }]

    package_id = f"urn:toothpaste-kit:{head_hash}:package-1"
    graph.append({
        "type": "software_Package",
        "spdxId": package_id,
        "creationInfo": CREATION_INFO_ID,
        "name": PACKAGE_NAME,
        "software_packageVersion": head_hash,
    })

    graph.append({
        "type": "Agent",
        "spdxId": author_agent_id,
        "creationInfo": CREATION_INFO_ID,
        "name": author_name,
    })

    if not model_order:
        return graph

    models = load_models(models_path)
    validate_models(models, models_path)

    for model in model_order:
        if model not in models:
            raise NoModelEntry(model, models_path)

    supplier_agent_id = {}
    for model in model_order:
        supplier = models[model]["suppliedBy"]
        if supplier not in supplier_agent_id:
            aid = f"urn:toothpaste-kit:{head_hash}:agent-{agent_n}"
            agent_n += 1
            supplier_agent_id[supplier] = aid
            graph.append({
                "type": "Agent",
                "spdxId": aid,
                "creationInfo": CREATION_INFO_ID,
                "name": supplier,
            })

    aipackage_ids = []
    for i, model in enumerate(model_order, start=1):
        entry = models[model]
        supplier = entry["suppliedBy"]
        node = {
            "type": "ai_AIPackage",
            "spdxId": f"urn:toothpaste-kit:{head_hash}:aipackage-{i}",
            "creationInfo": CREATION_INFO_ID,
            "name": model,
            "ai_autonomyType": entry["autonomyType"],
            "software_primaryPurpose": "model",
            "suppliedBy": supplier_agent_id[supplier],
            "software_downloadLocation": entry["downloadLocation"],
            "releaseTime": entry["releaseTime"],
            "software_packageVersion": entry["packageVersion"],
        }
        if model in effort_by_model:
            node["ai_hyperparameter"] = [
                {"key": "agent-effort", "value": effort_by_model[model]}
            ]
        graph.append(node)
        aipackage_ids.append(node["spdxId"])

    tool_ids = []
    for i, tool_id in enumerate(tool_order, start=1):
        node_id = f"urn:toothpaste-kit:{head_hash}:tool-{i}"
        graph.append({
            "type": "Tool",
            "spdxId": node_id,
            "creationInfo": CREATION_INFO_ID,
            "name": tool_id,
        })
        tool_ids.append(node_id)

    graph.append({
        "type": "Relationship",
        "spdxId": f"urn:toothpaste-kit:{head_hash}:relationship-1",
        "creationInfo": CREATION_INFO_ID,
        "relationshipType": "usesTool",
        "from": package_id,
        "to": aipackage_ids + tool_ids,
    })

    return graph


def parse_args(argv):
    models_path = DEFAULT_MODELS_PATH
    rest = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--models":
            if i + 1 >= len(argv):
                return None
            models_path = argv[i + 1]
            i += 2
            continue
        rest.append(a)
        i += 1
    if len(rest) != 1 or rest[0].startswith("-") or not is_valid_range(rest[0]):
        return None
    return models_path, rest[0]


def run(argv, cwd):
    """Execute the command; return (exit_code, stdout_text, stderr_lines)."""
    parsed = parse_args(argv)
    if parsed is None:
        return 2, "", [USAGE]
    models_path, range_arg = parsed
    try:
        graph = build_graph(cwd, range_arg, models_path)
    except (NoModelEntry, ModelsValidationError, MalformedAssistedBy) as e:
        return 2, "", [str(e)]
    except BadRange:
        return 2, "", [USAGE]
    except GitError as e:
        return 2, "", [f"spdx-fragment: {e}"]
    doc = {"@context": CONTEXT_URL, "@graph": graph}
    return 0, json.dumps(doc, indent=2) + "\n", []


def selftest():
    import tempfile

    ok = True
    n = 0

    def git(cwd, *args):
        subprocess.run(["git"] + list(args), cwd=cwd, check=True,
                        capture_output=True, text=True)

    def commit(cwd, path, text, message, date, author="T"):
        with open(os.path.join(cwd, path), "a") as f:
            f.write(text)
        git(cwd, "add", path)
        env_commit(cwd, message, date, author)

    def env_commit(cwd, message, date, author="T"):
        env = dict(os.environ)
        env["GIT_COMMITTER_DATE"] = date
        env["GIT_AUTHOR_DATE"] = date
        env["GIT_AUTHOR_NAME"] = author
        env["GIT_AUTHOR_EMAIL"] = "t@example.com"
        env["GIT_COMMITTER_NAME"] = "Hosting Site"  # differs from the author, as in a web merge
        env["GIT_COMMITTER_EMAIL"] = "site@example.com"
        subprocess.run(
            ["git", "commit", "-q", "-m", message], cwd=cwd, check=True,
            capture_output=True, text=True, env=env)

    with tempfile.TemporaryDirectory() as d:
        git(d, "init", "-q")
        git(d, "config", "user.email", "t@example.com")
        git(d, "config", "user.name", "T")
        commit(d, "f", "a\n", "root\n\nno trailers here", "2026-01-01T00:00:00+00:00")
        c0 = git_output(d, ["rev-parse", "HEAD"]).strip()
        commit(
            d, "f", "b\n",
            "add feature\n\n"
            "Assisted-by: model-a via tool-x/1.0.0\n"
            "Agent-Effort: high\n",
            "2026-01-02T03:04:05-07:00",
        )
        c1 = git_output(d, ["rev-parse", "HEAD"]).strip()
        commit(d, "f", "m\n", "middle\n\nno trailers here either",
               "2026-01-02T03:30:00-07:00")
        c2 = git_output(d, ["rev-parse", "HEAD"]).strip()
        commit(
            d, "f", "c\n",
            "add another\n\n"
            "Assisted-by: model-b via tool-y/2.0.0\n",
            "2026-01-02T04:00:00-07:00",
            author="Head Author",  # the range's head: not the base's author, not user.name
        )
        c3 = git_output(d, ["rev-parse", "HEAD"]).strip()
        commit(
            d, "f", "x\n",
            "bad trailer\n\nAssisted-by: just-a-model-no-via\n",
            "2026-01-02T04:30:00-07:00",
        )
        c4 = git_output(d, ["rev-parse", "HEAD"]).strip()
        commit(
            d, "f", "y\n",
            "two models\n\n"
            "Assisted-by: model-a via tool-x/1.0.0\n"
            "Assisted-by: model-c via tool-z/3.0.0\n"
            "Agent-Effort: medium\n",
            "2026-01-02T05:00:00-07:00",
        )
        c5 = git_output(d, ["rev-parse", "HEAD"]).strip()

        models_path = os.path.join(d, "models.json")
        with open(models_path, "w") as f:
            json.dump({
                "model-a": {
                    "suppliedBy": "vendor-a",
                    "downloadLocation": "https://example.com/model-a",
                    "releaseTime": "2025-12-01T00:00:00Z",
                    "packageVersion": "1.0",
                    "autonomyType": "no",
                },
                "model-b": {
                    "suppliedBy": "vendor-b",
                    "downloadLocation": "https://example.com/model-b",
                    "releaseTime": "2025-12-02T00:00:00Z",
                    "packageVersion": "2.0",
                    "autonomyType": "no",
                },
                "model-c": {
                    "suppliedBy": "vendor-a",
                    "downloadLocation": "https://example.com/model-c",
                    "releaseTime": "2025-12-03T00:00:00Z",
                    "packageVersion": "3.0",
                    "autonomyType": "no",
                },
            }, f)

        range_full = f"{c0}..{c3}"

        # --- graph shape: two models, two suppliers, two tools, one relationship ---
        code, out, errs = run(["--models", models_path, range_full], d)
        doc = json.loads(out) if code == 0 else None
        types = [n_["type"] for n_ in doc["@graph"]] if doc else []
        want = ["CreationInfo", "software_Package", "Agent", "Agent", "Agent",
                "ai_AIPackage", "ai_AIPackage", "Tool", "Tool", "Relationship"]
        graph_ok = (code == 0 and not errs and types == want)
        n += 1
        print(f"{'ok  ' if graph_ok else 'FAIL'}  graph shape: expected "
              f"{want}, got {types}" if not graph_ok else "ok    graph shape")
        ok = ok and graph_ok

        rel = next((x for x in doc["@graph"] if x["type"] == "Relationship"), None) if doc else None
        pkg = next((x for x in doc["@graph"] if x["type"] == "software_Package"), None) if doc else None
        aipkgs = [x for x in doc["@graph"] if x["type"] == "ai_AIPackage"] if doc else []
        tools = [x for x in doc["@graph"] if x["type"] == "Tool"] if doc else []
        rel_ok = bool(
            rel and pkg
            and rel["relationshipType"] == "usesTool"
            and rel["from"] == pkg["spdxId"]
            and set(rel["to"]) == {x["spdxId"] for x in aipkgs + tools}
        )
        n += 1
        print(f"{'ok  ' if rel_ok else 'FAIL'}  one usesTool relationship, kit package to every AIPackage and Tool")
        ok = ok and rel_ok

        effort_ok = bool(
            aipkgs
            and any(x.get("ai_hyperparameter") == [{"key": "agent-effort", "value": "high"}]
                    for x in aipkgs if x["name"] == "model-a")
            and any("ai_hyperparameter" not in x for x in aipkgs if x["name"] == "model-b")
        )
        n += 1
        print(f"{'ok  ' if effort_ok else 'FAIL'}  agent-effort hyperparameter only on the model named with one")
        ok = ok and effort_ok

        head_fields_ok = bool(
            pkg and pkg["software_packageVersion"] == c3
            and doc["@graph"][0]["created"] == "2026-01-02T11:00:00Z"
        )
        n += 1
        print(f"{'ok  ' if head_fields_ok else 'FAIL'}  head hash and UTC created time")
        ok = ok and head_fields_ok

        creation_info_ok = bool(
            doc and doc["@graph"][0]["@id"] == CREATION_INFO_ID
            and doc["@graph"][0]["createdBy"]
            and all(x.get("creationInfo") == CREATION_INFO_ID
                    for x in doc["@graph"] if x["type"] != "CreationInfo")
        )
        n += 1
        print(f"{'ok  ' if creation_info_ok else 'FAIL'}  every element but CreationInfo carries creationInfo, and CreationInfo has an @id")
        ok = ok and creation_info_ok

        creator = doc["@graph"][0]["createdBy"][0] if doc else None
        author_ok = any(x["type"] == "Agent" and x["spdxId"] == creator and x["name"] == "Head Author"
                        for x in doc["@graph"]) if doc else False
        n += 1
        print(f"{'ok  ' if author_ok else 'FAIL'}  createdBy names the author, not a differing committer")
        ok = ok and author_ok

        model_a = next((x for x in aipkgs if x["name"] == "model-a"), None) if aipkgs else None
        field_names_ok = bool(
            model_a
            and "software_downloadLocation" in model_a and "downloadLocation" not in model_a
            and "software_packageVersion" in model_a and "packageVersion" not in model_a
            and "releaseTime" in model_a and "suppliedBy" in model_a
        )
        n += 1
        print(f"{'ok  ' if field_names_ok else 'FAIL'}  AIPackage: downloadLocation and packageVersion carry the software_ prefix, releaseTime and suppliedBy stay bare"
              if field_names_ok else
              f"FAIL  AIPackage field names: got {model_a}")
        ok = ok and field_names_ok

        agents = [x for x in doc["@graph"] if x["type"] == "Agent"] if doc else []
        agent_ids = {x["spdxId"] for x in agents}
        supplied_by_ok = bool(
            model_a and model_a["suppliedBy"] in agent_ids
            and model_a["suppliedBy"] != "vendor-a"
            and any(x["name"] == "vendor-a" and x["spdxId"] == model_a["suppliedBy"] for x in agents)
        )
        n += 1
        print(f"{'ok  ' if supplied_by_ok else 'FAIL'}  AIPackage.suppliedBy is a reference to an Agent, not the bare supplier name"
              if supplied_by_ok else
              f"FAIL  AIPackage.suppliedBy: got {model_a['suppliedBy'] if model_a else None}, agents={agents}")
        ok = ok and supplied_by_ok

        # --- autonomyType comes from the models file, not a hard-coded value ---
        yes_models = os.path.join(d, "yes-autonomy-models.json")
        with open(yes_models, "w") as f:
            json.dump({"model-a": {
                "suppliedBy": "vendor-a",
                "downloadLocation": "https://example.com/model-a",
                "releaseTime": "2025-12-01T00:00:00Z",
                "packageVersion": "1.0",
                "autonomyType": "yes",
            }}, f)
        code, out, errs = run(["--models", yes_models, f"{c0}..{c1}"], d)
        doc_yes = json.loads(out) if code == 0 else None
        yes_aipkgs = [x for x in doc_yes["@graph"] if x["type"] == "ai_AIPackage"] if doc_yes else []
        autonomy_from_file_ok = bool(
            code == 0 and not errs and len(yes_aipkgs) == 1
            and yes_aipkgs[0]["ai_autonomyType"] == "yes"
        )
        n += 1
        print(f"{'ok  ' if autonomy_from_file_ok else 'FAIL'}  ai_autonomyType comes from the models file, not hard-coded"
              if autonomy_from_file_ok else
              f"FAIL  ai_autonomyType: code={code} errs={errs} aipkgs={yes_aipkgs}")
        ok = ok and autonomy_from_file_ok

        # --- missing model entry: exits 2, names the model and the file ---
        bad_models = os.path.join(d, "bad-models.json")
        with open(bad_models, "w") as f:
            json.dump({"model-a": {
                "suppliedBy": "vendor-a",
                "downloadLocation": "https://example.com/model-a",
                "releaseTime": "2025-12-01T00:00:00Z",
                "packageVersion": "1.0",
                "autonomyType": "no",
            }}, f)
        code, out, errs = run(["--models", bad_models, range_full], d)
        missing_ok = (code == 2 and not out
                      and errs == [f"spdx-fragment: no entry for model-b in {bad_models}"])
        n += 1
        print(f"{'ok  ' if missing_ok else 'FAIL'}  missing model entry: got code={code} errs={errs}"
              if not missing_ok else "ok    missing model entry exits 2 and names it")
        ok = ok and missing_ok

        # --- a models entry lacking a required key ---
        lacking_key = os.path.join(d, "lacking-key-models.json")
        with open(lacking_key, "w") as f:
            json.dump({
                "model-a": {
                    "suppliedBy": "vendor-a",
                    "releaseTime": "2025-12-01T00:00:00Z",
                    "packageVersion": "1.0",
                    "autonomyType": "no",
                },
                "model-b": {
                    "suppliedBy": "vendor-b",
                    "downloadLocation": "https://example.com/model-b",
                    "releaseTime": "2025-12-02T00:00:00Z",
                    "packageVersion": "2.0",
                    "autonomyType": "no",
                },
            }, f)
        code, out, errs = run(["--models", lacking_key, range_full], d)
        lacking_key_ok = (code == 2 and not out
                           and errs == [f"spdx-fragment: model-a in {lacking_key} lacks downloadLocation"])
        n += 1
        print(f"{'ok  ' if lacking_key_ok else 'FAIL'}  models entry lacking a key: got code={code} errs={errs}"
              if not lacking_key_ok else "ok    models entry lacking a key exits 2 and names the key")
        ok = ok and lacking_key_ok

        # --- a bad releaseTime ---
        bad_release = os.path.join(d, "bad-release-models.json")
        with open(bad_release, "w") as f:
            json.dump({
                "model-a": {
                    "suppliedBy": "vendor-a",
                    "downloadLocation": "https://example.com/model-a",
                    "releaseTime": "not-a-date",
                    "packageVersion": "1.0",
                    "autonomyType": "no",
                },
                "model-b": {
                    "suppliedBy": "vendor-b",
                    "downloadLocation": "https://example.com/model-b",
                    "releaseTime": "2025-12-02T00:00:00Z",
                    "packageVersion": "2.0",
                    "autonomyType": "no",
                },
            }, f)
        code, out, errs = run(["--models", bad_release, range_full], d)
        bad_release_ok = (code == 2 and not out
                           and errs == ["spdx-fragment: model-a releaseTime is not YYYY-MM-DDTHH:MM:SSZ"])
        n += 1
        print(f"{'ok  ' if bad_release_ok else 'FAIL'}  bad releaseTime: got code={code} errs={errs}"
              if not bad_release_ok else "ok    bad releaseTime exits 2")
        ok = ok and bad_release_ok

        # A valid model-b beside each bad model-a below, so a case that stops catching
        # its fault exits 0 or raises, never 2 by falling through to "no entry for model-b".
        valid_b = {
            "suppliedBy": "vendor-b",
            "downloadLocation": "https://example.com/model-b",
            "releaseTime": "2025-12-02T00:00:00Z",
            "packageVersion": "2.0",
            "autonomyType": "no",
        }

        # --- a releaseTime that is not a string ---
        nonstr_release = os.path.join(d, "nonstr-release-models.json")
        with open(nonstr_release, "w") as f:
            json.dump({
                "model-a": {
                    "suppliedBy": "vendor-a",
                    "downloadLocation": "https://example.com/model-a",
                    "releaseTime": 5,
                    "packageVersion": "1.0",
                    "autonomyType": "no",
                },
                "model-b": valid_b,
            }, f)
        code, out, errs = run(["--models", nonstr_release, range_full], d)
        nonstr_release_ok = (code == 2 and not out
                             and errs == ["spdx-fragment: model-a releaseTime is not YYYY-MM-DDTHH:MM:SSZ"])
        n += 1
        print(f"{'ok  ' if nonstr_release_ok else 'FAIL'}  non-string releaseTime: got code={code} errs={errs}"
              if not nonstr_release_ok else "ok    non-string releaseTime exits 2")
        ok = ok and nonstr_release_ok

        # --- a models file that is not a JSON object ---
        list_models = os.path.join(d, "list-models.json")
        with open(list_models, "w") as f:
            json.dump(["model-a"], f)
        code, out, errs = run(["--models", list_models, range_full], d)
        list_models_ok = (code == 2 and not out
                          and errs == [f"spdx-fragment: {list_models} is not a JSON object"])
        n += 1
        print(f"{'ok  ' if list_models_ok else 'FAIL'}  models file not an object: got code={code} errs={errs}"
              if not list_models_ok else "ok    models file that is not an object exits 2")
        ok = ok and list_models_ok

        # --- a releaseTime with a trailing newline ---
        nl_release = os.path.join(d, "nl-release-models.json")
        with open(nl_release, "w") as f:
            json.dump({
                "model-a": {
                    "suppliedBy": "vendor-a",
                    "downloadLocation": "https://example.com/model-a",
                    "releaseTime": "2025-12-01T00:00:00Z\n",
                    "packageVersion": "1.0",
                    "autonomyType": "no",
                },
                "model-b": valid_b,
            }, f)
        code, out, errs = run(["--models", nl_release, range_full], d)
        nl_release_ok = (code == 2 and not out
                         and errs == ["spdx-fragment: model-a releaseTime is not YYYY-MM-DDTHH:MM:SSZ"])
        n += 1
        print(f"{'ok  ' if nl_release_ok else 'FAIL'}  releaseTime with a trailing newline: got code={code} errs={errs}"
              if not nl_release_ok else "ok    releaseTime with a trailing newline exits 2")
        ok = ok and nl_release_ok

        # --- suppliedBy, downloadLocation or packageVersion not a string ---
        for key, value in (("suppliedBy", ["vendor-a"]),
                           ("downloadLocation", {"url": "https://example.com/model-a"}),
                           ("packageVersion", 1)):
            entry = {
                "suppliedBy": "vendor-a",
                "downloadLocation": "https://example.com/model-a",
                "releaseTime": "2025-12-01T00:00:00Z",
                "packageVersion": "1.0",
                "autonomyType": "no",
            }
            entry[key] = value
            nonstr = os.path.join(d, f"nonstr-{key}-models.json")
            with open(nonstr, "w") as f:
                json.dump({"model-a": entry, "model-b": valid_b}, f)
            code, out, errs = run(["--models", nonstr, range_full], d)
            nonstr_ok = (code == 2 and not out
                         and errs == [f"spdx-fragment: model-a {key} is not a string"])
            n += 1
            print(f"{'ok  ' if nonstr_ok else 'FAIL'}  non-string {key}: got code={code} errs={errs}"
                  if not nonstr_ok else f"ok    non-string {key} exits 2")
            ok = ok and nonstr_ok

        # --- a models file that is not UTF-8 ---
        latin1_models = os.path.join(d, "latin1-models.json")
        with open(latin1_models, "wb") as f:
            f.write(b'{"model-a": {"suppliedBy": "vend\xe9"}}')
        code, out, errs = run(["--models", latin1_models, range_full], d)
        latin1_ok = (code == 2 and not out and len(errs) == 1
                     and errs[0].startswith(f"spdx-fragment: cannot read {latin1_models}: "))
        n += 1
        print(f"{'ok  ' if latin1_ok else 'FAIL'}  models file not UTF-8: got code={code} errs={errs}"
              if not latin1_ok else "ok    models file that is not UTF-8 exits 2")
        ok = ok and latin1_ok

        # --- JSON the parser itself refuses: an int past Python's digit limit, deep nesting ---
        for label, text in (("integer over 4300 digits", '{"model-a": ' + "9" * 5000 + "}"),
                            ("nesting 1,000,000 deep", '{"a":' * 1000000)):
            deep_models = os.path.join(d, "parser-limit-models.json")
            with open(deep_models, "w") as f:
                f.write(text)
            code, out, errs = run(["--models", deep_models, range_full], d)
            parse_ok = (code == 2 and not out and len(errs) == 1
                        and errs[0].startswith(f"spdx-fragment: cannot read {deep_models}: "))
            n += 1
            print(f"{'ok  ' if parse_ok else 'FAIL'}  {label}: got code={code} errs={errs[-1:]}"
                  if not parse_ok else f"ok    models file with {label} exits 2")
            ok = ok and parse_ok

        # --- a bad autonomyType ---
        bad_autonomy = os.path.join(d, "bad-autonomy-models.json")
        with open(bad_autonomy, "w") as f:
            json.dump({
                "model-a": {
                    "suppliedBy": "vendor-a",
                    "downloadLocation": "https://example.com/model-a",
                    "releaseTime": "2025-12-01T00:00:00Z",
                    "packageVersion": "1.0",
                    "autonomyType": "maybe",
                },
                "model-b": {
                    "suppliedBy": "vendor-b",
                    "downloadLocation": "https://example.com/model-b",
                    "releaseTime": "2025-12-02T00:00:00Z",
                    "packageVersion": "2.0",
                    "autonomyType": "no",
                },
            }, f)
        code, out, errs = run(["--models", bad_autonomy, range_full], d)
        bad_autonomy_ok = (code == 2 and not out
                            and errs == ["spdx-fragment: model-a autonomyType is not yes or no"])
        n += 1
        print(f"{'ok  ' if bad_autonomy_ok else 'FAIL'}  bad autonomyType: got code={code} errs={errs}"
              if not bad_autonomy_ok else "ok    bad autonomyType exits 2")
        ok = ok and bad_autonomy_ok

        # --- no trailers in range: a real, non-empty range, never base..base ---
        no_trailer_range = f"{c1}..{c2}"
        code, out, errs = run(["--models", models_path, no_trailer_range], d)
        doc2 = json.loads(out) if code == 0 else None
        no_trailer_ok = bool(
            code == 0 and not errs and doc2
            and [x["type"] for x in doc2["@graph"]] == ["CreationInfo", "software_Package", "Agent"]
        )
        n += 1
        print(f"{'ok  ' if no_trailer_ok else 'FAIL'}  no trailers in range: code={code} types="
              f"{[x['type'] for x in doc2['@graph']] if doc2 else None}"
              if not no_trailer_ok else "ok    no trailers in a real range: CreationInfo, kit package and author Agent only, exit 0")
        ok = ok and no_trailer_ok

        # --- models file is never loaded when no model is named ---
        # Point at a path that cannot accidentally exist (unlike the real
        # DEFAULT_MODELS_PATH, which resolves against the process's actual
        # cwd, not the tempdir, and happens to hit the real shipped file
        # there): if build_graph loads it anyway, open() fails and this
        # becomes exit 2 instead of 0.
        bogus_models_path = os.path.join(d, "does-not-exist.json")
        code, out, errs = run(["--models", bogus_models_path, no_trailer_range], d)
        never_loaded_ok = (code == 0 and not errs)
        n += 1
        print(f"{'ok  ' if never_loaded_ok else 'FAIL'}  no model named: the default models file (which does not exist here) is never opened"
              if never_loaded_ok else
              f"FAIL  models file loaded with no model named: code={code} errs={errs}")
        ok = ok and never_loaded_ok

        # --- a malformed Assisted-by trailer ---
        code, out, errs = run(["--models", models_path, f"{c3}..{c4}"], d)
        malformed_ok = (code == 2 and not out
                         and errs == [f"spdx-fragment: {c4} has a malformed Assisted-by: just-a-model-no-via"])
        n += 1
        print(f"{'ok  ' if malformed_ok else 'FAIL'}  malformed Assisted-by: got code={code} errs={errs}"
              if not malformed_ok else "ok    malformed Assisted-by exits 2 and names the commit")
        ok = ok and malformed_ok

        # --- one Agent-Effort applied to two models named in one commit ---
        code, out, errs = run(["--models", models_path, f"{c4}..{c5}"], d)
        doc3 = json.loads(out) if code == 0 else None
        two_model_aipkgs = [x for x in doc3["@graph"] if x["type"] == "ai_AIPackage"] if doc3 else []
        shared_effort_ok = bool(
            code == 0 and not errs and len(two_model_aipkgs) == 2
            and all(x.get("ai_hyperparameter") == [{"key": "agent-effort", "value": "medium"}]
                    for x in two_model_aipkgs)
        )
        n += 1
        print(f"{'ok  ' if shared_effort_ok else 'FAIL'}  one Agent-Effort applied to both models named in one commit"
              if shared_effort_ok else
              f"FAIL  one Agent-Effort applied to both models named in one commit: code={code} errs={errs}")
        ok = ok and shared_effort_ok

        # --- bad arguments: exit 2 with the usage line ---
        for name, argv in [
            ("no arguments", []),
            ("not a range", ["notarange"]),
            ("too many arguments", [range_full, "extra"]),
            ("--models with no value", ["--models"]),
            ("a flag instead of a range", ["--bogus"]),
            ("a three-dot range", [f"{c0}...{c3}"]),
            ("more than one two-dot range", [f"{c0}..{c1}..{c3}"]),
        ]:
            code, out, errs = run(argv, d)
            case_ok = (code == 2 and not out and errs == [USAGE])
            n += 1
            print(f"{'ok  ' if case_ok else 'FAIL'}  bad argument ({name}): code={code} errs={errs}"
                  if not case_ok else f"ok    bad argument ({name}) exits 2 with usage")
            ok = ok and case_ok

    print(f"selftest: {n} cases passed" if ok else "selftest: FAILED")
    return 0 if ok else 1


def main(argv):
    if argv == ["--selftest"]:
        return selftest()
    code, out, errs = run(argv, os.getcwd())
    if out:
        sys.stdout.write(out)
    for e in errs:
        print(e, file=sys.stderr)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
