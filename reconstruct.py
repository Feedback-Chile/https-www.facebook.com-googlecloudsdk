#!/usr/bin/env python3
"""Herramienta sencilla para reconstruir código desde fragmentos."""
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from typing import Iterable, List, Sequence

MARKER_PREFIXES = ("<<<", ">>>", "===")
PROMPT_PATTERN = re.compile(r"^[\w.-]+[>#]\s*")


@dataclass(frozen=True)
class CleanOptions:
    strip_prompts: bool = False
    strip_prefixes: Sequence[str] = ()
    drop_empty: bool = False


def normalize_line(raw_line: str, options: CleanOptions) -> str:
    line = raw_line
    if options.strip_prompts:
        line = PROMPT_PATTERN.sub("", line)
    for prefix in options.strip_prefixes:
        if line.startswith(prefix):
            line = line[len(prefix) :]
    return line.rstrip()


def clean_fragment(fragment: str, options: CleanOptions) -> List[str]:
    lines = []
    for raw_line in fragment.splitlines():
        if raw_line.strip().startswith(MARKER_PREFIXES):
            continue
        normalized = normalize_line(raw_line, options)
        if options.drop_empty and not normalized:
            continue
        lines.append(normalized)
    return lines


def reconstruct_code(
    fragments: Iterable[str],
    *,
    dedupe: bool = False,
    options: CleanOptions | None = None,
) -> str:
    if options is None:
        options = CleanOptions()
    output: List[str] = []
    seen = set()
    for fragment in fragments:
        for line in clean_fragment(fragment, options):
            if not dedupe:
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
        description="Reconstruye código desde fragmentos.",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Archivos con fragmentos. Si se omite, se lee desde stdin.",
    )
    dedupe_group = parser.add_mutually_exclusive_group()
    dedupe_group.add_argument(
        "--dedupe",
        action="store_true",
        help="Eliminar líneas duplicadas al reconstruir.",
    )
    dedupe_group.add_argument(
        "--keep-duplicates",
        action="store_true",
        help="Conservar líneas duplicadas (comportamiento por defecto).",
    )
    parser.add_argument(
        "--strip-prompts",
        action="store_true",
        help="Quitar prefijos de prompt comunes (por ejemplo switch#).",
    )
    parser.add_argument(
        "--strip-prefix",
        action="append",
        default=[],
        help="Prefijo exacto a eliminar (se puede repetir).",
    )
    parser.add_argument(
        "--drop-empty",
        action="store_true",
        help="Eliminar líneas vacías después de la limpieza.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    fragments = load_fragments(args.paths)
    options = CleanOptions(
        strip_prompts=args.strip_prompts,
        strip_prefixes=tuple(args.strip_prefix),
        drop_empty=args.drop_empty,
    )
    reconstructed = reconstruct_code(
        fragments,
        dedupe=args.dedupe,
        options=options,
    )
    print(reconstructed, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
