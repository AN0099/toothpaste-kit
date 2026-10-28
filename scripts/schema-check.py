#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2026 Aidan Naveja
#
# SPDX-License-Identifier: Apache-2.0

"""Validate orchestration/registry/*.json against surface-descriptor.schema.json.

Standard library only, no dependency and no vendored validator. This is not a
general JSON Schema engine: it implements exactly the keywords that
orchestration/registry/surface-descriptor.schema.json and the
orchestration/schemas/event-base.json definition it references actually use.
Before validating anything, it walks both schema documents in full and fails,
naming the keyword, on any key it does not recognize, so a schema edit that
adds a keyword this file does not implement cannot pass silently; it has to
fail here first.

Keywords implemented: type, required, properties, pattern, items, $ref,
enum, format (date, date-time, uri). $schema, $id, title, description and
definitions are recognized as structure or annotations, not applied to an
instance.

No CLI arguments. Run from the repository root, as scripts/gates.sh does.
"""

import glob
import json
import os
import re
import sys
from datetime import datetime
from urllib.parse import urlparse

SCHEMA_PATH = "orchestration/registry/surface-descriptor.schema.json"
REGISTRY_DIR = "orchestration/registry"

KNOWN_KEYWORDS = {
    "$schema", "$id", "title", "description", "definitions",
    "type", "required", "properties", "pattern", "items", "$ref",
    "enum", "format",
}

_schema_cache = {}


def load_json(path):
    with open(path) as f:
        return json.load(f)


def load_schema_file(path):
    path = os.path.normpath(path)
    if path not in _schema_cache:
        _schema_cache[path] = load_json(path)
    return _schema_cache[path]


def check_keywords(node, errors):
    """Walk a schema document and fail on any keyword not implemented below,
    everywhere a nested schema can appear: properties, definitions, items."""
    if not isinstance(node, dict):
        return
    for key, value in node.items():
        if key not in KNOWN_KEYWORDS:
            errors.append(f"unimplemented JSON Schema keyword: {key}")
            continue
        if key in ("properties", "definitions") and isinstance(value, dict):
            for subschema in value.values():
                check_keywords(subschema, errors)
        elif key == "items":
            check_keywords(value, errors)


def resolve_ref(ref, current_file):
    if "#" in ref:
        file_part, pointer_part = ref.split("#", 1)
    else:
        file_part, pointer_part = ref, ""
    target_file = (
        os.path.normpath(os.path.join(os.path.dirname(current_file), file_part))
        if file_part else current_file
    )
    node = load_schema_file(target_file)
    for part in pointer_part.strip("/").split("/"):
        if part == "":
            continue
        node = node[part.replace("~1", "/").replace("~0", "~")]
    return node, target_file


def check_type(instance, expected, path, errors):
    for t in expected if isinstance(expected, list) else [expected]:
        if t == "object" and isinstance(instance, dict):
            return
        if t == "array" and isinstance(instance, list):
            return
        if t == "string" and isinstance(instance, str):
            return
        if t == "boolean" and isinstance(instance, bool):
            return
        if t == "integer" and isinstance(instance, int) and not isinstance(instance, bool):
            return
        if t == "number" and isinstance(instance, (int, float)) and not isinstance(instance, bool):
            return
        if t == "null" and instance is None:
            return
    errors.append(f"{path}: expected type {expected!r}, got {type(instance).__name__}")


def check_format(instance, fmt, path, errors):
    if not isinstance(instance, str):
        return
    if fmt == "date":
        try:
            datetime.strptime(instance, "%Y-%m-%d")
        except ValueError:
            errors.append(f"{path}: {instance!r} is not a valid date (YYYY-MM-DD)")
    elif fmt == "date-time":
        try:
            datetime.fromisoformat(instance.replace("Z", "+00:00"))
        except ValueError:
            errors.append(f"{path}: {instance!r} is not a valid date-time")
    elif fmt == "uri":
        parsed = urlparse(instance)
        if not parsed.scheme or not parsed.netloc:
            errors.append(f"{path}: {instance!r} is not a valid uri")
    else:
        errors.append(f"{path}: unimplemented format value: {fmt}")


def validate(instance, schema, current_file, path, errors):
    if "$ref" in schema:
        subschema, ref_file = resolve_ref(schema["$ref"], current_file)
        validate(instance, subschema, ref_file, path, errors)
        return

    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: {instance!r} is not one of {schema['enum']}")
        return

    if "type" in schema:
        check_type(instance, schema["type"], path, errors)

    if "pattern" in schema and isinstance(instance, str):
        if re.search(schema["pattern"], instance) is None:
            errors.append(f"{path}: {instance!r} does not match pattern {schema['pattern']!r}")

    if "format" in schema:
        check_format(instance, schema["format"], path, errors)

    if "required" in schema and isinstance(instance, dict):
        for name in schema["required"]:
            if name not in instance:
                errors.append(f"{path}: missing required field {name!r}")

    if "properties" in schema and isinstance(instance, dict):
        for name, subschema in schema["properties"].items():
            if name in instance:
                validate(instance[name], subschema, current_file, f"{path}.{name}", errors)

    if "items" in schema and isinstance(instance, list):
        for i, item in enumerate(instance):
            validate(item, schema["items"], current_file, f"{path}[{i}]", errors)


def main():
    errors = []

    schema_doc = load_schema_file(SCHEMA_PATH)
    check_keywords(schema_doc, errors)
    event_base_path = os.path.normpath(
        os.path.join(os.path.dirname(SCHEMA_PATH), "../schemas/event-base.json")
    )
    check_keywords(load_schema_file(event_base_path), errors)

    if errors:
        for e in errors:
            print(f"::error::{e}")
        return 2

    files = sorted(
        p for p in glob.glob(f"{REGISTRY_DIR}/*.json")
        if os.path.normpath(p) != os.path.normpath(SCHEMA_PATH)
    )
    for path in files:
        validate(load_json(path), schema_doc, SCHEMA_PATH, path, errors)
    print(f"  schema-checked {len(files)} registry files against {SCHEMA_PATH}")

    if errors:
        for e in errors:
            print(f"::error::{e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
