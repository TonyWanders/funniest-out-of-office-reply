#!/usr/bin/env python3
"""Write one funny one-line out-of-office reply to the output target.

Standard library only, deterministic: the same line every run.
Usage: python3 main.py [output_path]
The output path defaults to $OUTPUT_PATH, then /output/entry.txt.
"""

import os
import sys

ENTRY = "I am away from my desk, my inbox, and my will to answer either."

MIN_ENTRY_LENGTH = 1
MAX_ENTRY_LENGTH = 160
DEFAULT_OUTPUT_PATH = "/output/entry.txt"


def validate_entry(text: str) -> str:
    """Enforce the 1-160 character gate on the entry line.

    Raises ValueError when the entry is empty or too long, so a bad
    entry fails loudly instead of being written out silently.
    """
    if not MIN_ENTRY_LENGTH <= len(text) <= MAX_ENTRY_LENGTH:
        raise ValueError(
            f"entry must be {MIN_ENTRY_LENGTH}-{MAX_ENTRY_LENGTH} characters, "
            f"got {len(text)}"
        )
    return text


def resolve_output_path(argv: list[str]) -> str:
    """Pick the output target: argv[1], then $OUTPUT_PATH, then the default."""
    if len(argv) > 1:
        return argv[1]
    return os.environ.get("OUTPUT_PATH") or DEFAULT_OUTPUT_PATH


def write_entry(target: str, text: str) -> None:
    """Write the validated entry to the target, with a trailing newline."""
    parent = os.path.dirname(target)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(target, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text + "\n")


def main() -> int:
    target = resolve_output_path(sys.argv)
    write_entry(target, validate_entry(ENTRY))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
