# -*- coding: utf-8 -*-

"""Convert Chinese full-width punctuation to English half-width punctuation."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .impl import process

_BOM = "\ufeff"


def _restore_trailing_newline(old_text: str, new_text: str) -> str:
    """Re-attach the trailing newline that :func:`.impl.process` strips off.

    ``process()`` is built on ``str.splitlines()``, which drops the final line
    terminator. That is harmless for text in / text out, but rewriting a file
    must not silently delete its last newline.
    """
    if old_text.endswith("\n") and not new_text.endswith("\n"):
        return new_text + "\n"
    return new_text


def _count_changed_lines(old_text: str, new_text: str) -> int:
    """Count how many lines differ between the two versions."""
    old_lines = old_text.splitlines()
    new_lines = new_text.splitlines()
    n = 0
    for i in range(max(len(old_lines), len(new_lines))):
        old_line = old_lines[i] if i < len(old_lines) else None
        new_line = new_lines[i] if i < len(new_lines) else None
        if old_line != new_line:
            n += 1
    return n


def _main_text(text: str | None = None) -> int:
    """Convert a chunk of text and write the result to stdout.

    When ``text`` is ``None`` the input is read from stdin, so the command can
    be used as a pipe filter.

    Returns an exit code: 0 on success, 1 on failure.
    """
    if text is None:
        text = sys.stdin.read()
    print(process(text))
    return 0


def _main_file(path: Path, dry_run: bool = False) -> int:
    """Convert a UTF-8 encoded text file in place.

    The file must be valid UTF-8; anything else is rejected instead of being
    guessed at. Line endings are normalized to ``\\n``, and a trailing newline
    is preserved if the original had one.

    Returns an exit code: 0 on success, 1 on failure.
    """
    if not path.exists():
        print(f"ERROR: {path} not found", file=sys.stderr)
        return 1
    if not path.is_file():
        print(f"ERROR: {path} is not a file", file=sys.stderr)
        return 1

    try:
        old_text = path.read_bytes().decode("utf-8")
    except UnicodeDecodeError as e:
        print(f"ERROR: {path} is not valid UTF-8: {e}", file=sys.stderr)
        return 1

    # A byte order mark is not content, keep it out of the conversion and
    # put it back afterwards so the file's encoding form is unchanged.
    bom, body = (_BOM, old_text[1:]) if old_text.startswith(_BOM) else ("", old_text)
    new_text = bom + _restore_trailing_newline(body, process(body))

    if new_text == old_text:
        print(f"{path}: no change")
        return 0

    n = _count_changed_lines(old_text, new_text)
    if dry_run:
        print(f"{path}: {n} line(s) would change (dry run, nothing written)")
        return 0

    path.write_bytes(new_text.encode("utf-8"))
    print(f"{path}: {n} line(s) changed")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="c2ep",
        description=(
            "Convert Chinese full-width punctuation to English half-width "
            "punctuation, and add spaces between Chinese and English."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_text = subparsers.add_parser(
        "text",
        help="convert text and print the result to stdout",
        description=(
            "Convert text and print the result to stdout. "
            "Reads from stdin when --text is omitted."
        ),
    )
    parser_text.add_argument(
        "--text",
        type=str,
        default=None,
        help="the text to convert; read from stdin if not given",
    )

    parser_file = subparsers.add_parser(
        "file",
        help="convert a UTF-8 text file in place",
        description=(
            "Convert a UTF-8 encoded text file in place. "
            "Files that are not valid UTF-8 are rejected."
        ),
    )
    parser_file.add_argument(
        "--path",
        type=Path,
        required=True,
        help="path to the file to convert in place",
    )
    parser_file.add_argument(
        "--dry_run",
        action="store_true",
        help="report what would change without writing the file",
    )

    args = parser.parse_args(argv)
    if args.command == "text":
        return _main_text(text=args.text)
    else:
        return _main_file(path=args.path, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
