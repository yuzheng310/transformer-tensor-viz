#!/usr/bin/env python3
"""Lint fragile TikZ connector and macro patterns used by this skill."""

from __future__ import annotations

import re
import sys
from pathlib import Path


DRAW_RE = re.compile(r"\\draw\s*\[([^\]]*)\]\s*(.*?);", re.DOTALL)
ARITY_RE = re.compile(r"\\newcommand\s*\{[^}]+\}\s*\[(\d+)\]")
CONNECTOR_STYLE_RE = re.compile(
    r"(?<![\w-])(?:tt\s+flow|tt\s+share|tt\s+collective|flow|share|collective)(?![\w-])"
)
NAMED_ANCHOR = r"\([A-Za-z][A-Za-z0-9_-]*(?:\.[A-Za-z][A-Za-z0-9 _-]*)?\)"
START_RE = re.compile(rf"^\s*{NAMED_ANCHOR}")
END_RE = re.compile(rf"{NAMED_ANCHOR}\s*$")
TARGET_RE = re.compile(rf"({NAMED_ANCHOR})\s*$")


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def lint(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    for match in ARITY_RE.finditer(text):
        arity = int(match.group(1))
        if arity > 9:
            errors.append(
                f"{path}:{line_number(text, match.start())}: TeX macro declares {arity} parameters; maximum is 9"
            )

    for match in DRAW_RE.finditer(text):
        styles, route = match.groups()
        if not CONNECTOR_STYLE_RE.search(styles):
            continue
        line = line_number(text, match.start())
        compact = " ".join(route.split())
        if not START_RE.search(route):
            errors.append(
                f"{path}:{line}: connector source must be a named node anchor, got: {compact[:100]}"
            )
        if not END_RE.search(route):
            errors.append(
                f"{path}:{line}: connector target must be a named node anchor, got: {compact[-100:]}"
            )
            continue
        target = TARGET_RE.search(route)
        if target and ("-symbol" in target.group(1) or "-shape" in target.group(1)):
            errors.append(
                f"{path}:{line}: connector must not terminate on a tensor label node: {target.group(1)}"
            )

    return errors


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: lint_tikz_connectors.py DIAGRAM.tex [DIAGRAM.tex ...]", file=sys.stderr)
        return 2

    errors: list[str] = []
    for raw_path in argv[1:]:
        path = Path(raw_path)
        if not path.is_file():
            errors.append(f"{path}: file not found")
            continue
        errors.extend(lint(path))

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"TikZ connector lint passed for {len(argv) - 1} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
