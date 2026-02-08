#!/usr/bin/env python3
"""Herramienta sencilla para reconstruir código desde fragmentos."""
from __future__ import annotations

import argparse
from typing import Iterable, List, Sequence

MARKER_PREFIXES = ("<<<", ">>>", "===")


def clean_fragment(fragment: str) -> List[str]:
    lines = []
    for raw_line in fragment.splitlines():
        if raw_line.strip().startswith(MARKER_PREFIXES):
            continue
        lines.append(raw_line.rstrip())
    return lines


def reconstruct_code(fragments: Iterable[str], keep_duplicates: bool = False) -> str:
    output: List[str] = []
    seen = set()
    for fragment in fragments:
        for line in clean_fragment(fragment):
            if keep_duplicates:
                output.append(line)
                continue
            if line in seen:
                continue
            seen.add(line)
            output.append(line)
    if not output:
        return ""
    return "\n".join(output) + "\n"


def load_fragments(paths: Sequence[str]) -> List[str]:
    if not paths:
        return ["".join(iter_input())]
    return [read_file(path) for path in paths]


def iter_input() -> Iterable[str]:
    try:
        while True:
            chunk = input()
            yield chunk + "\n"
    except EOFError:
        return


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Reconstruye código desde fragmentos evitando líneas duplicadas.",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Archivos con fragmentos. Si se omite, se lee desde stdin.",
    )
    parser.add_argument(
        "--keep-duplicates",
        action="store_true",
        help="Conservar líneas duplicadas al reconstruir.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    fragments = load_fragments(args.paths)
    reconstructed = reconstruct_code(fragments, keep_duplicates=args.keep_duplicates)
    print(reconstructed, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
