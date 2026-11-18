#!/usr/bin/env python3
"""Build the workshop overlay from the exact source in the installed image."""

import ast
import hashlib
import pathlib
import sys

EXPECTED_SHA256 = "e7f21a189bf9863a0a0b1d756cdcb0e28eaa1b2c932168923ca0b6229996344f"


def main():
    source_path, output_path = map(pathlib.Path, sys.argv[1:])
    source = source_path.read_text()
    digest = hashlib.sha256(source.encode()).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(
            f"Unexpected upstream agent source SHA-256: {digest}; inspect before adapting overlay"
        )
    tree = ast.parse(source)
    cls = next(
        n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "GenericAgent"
    )
    method = next(
        n
        for n in cls.body
        if isinstance(n, ast.AsyncFunctionDef) and n.name == "_execute_structured"
    )
    lines = source.splitlines(keepends=True)
    original = "".join(lines[method.lineno - 1 : method.end_lineno])
    original = original.replace(
        "async def _execute_structured(", "async def _execute_structured_native(", 1
    )
    replacement = (
        pathlib.Path(__file__).with_name("structured_method.py.txt").read_text()
    )
    result = (
        "".join(lines[: method.lineno - 1])
        + replacement
        + "\n\n"
        + original
        + "".join(lines[method.end_lineno :])
    )
    ast.parse(result)
    output_path.write_text(result)
    print(
        f"Overlay built from {digest}; SHA-256 {hashlib.sha256(result.encode()).hexdigest()}"
    )


if __name__ == "__main__":
    main()
