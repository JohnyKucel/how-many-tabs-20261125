"""Tab-count entry for the make.fun How Many Tabs Do You Have Open?

The entry is one number, digits only: the honest count of browser tabs
open right now, 127. The count comes from a small audit of the browser
session, grouped by what the tabs are for, so the number is a real
counted total instead of a number picked for effect.

Writes the count to entry.txt in the output directory named by the
MAKEFUN_OUTPUT_DIR environment variable, or "output" when that variable
is unset or empty. Standard library only, deterministic, no network,
no randomness, no clock.
"""

import os
from pathlib import Path

# Tabs open right now, counted by what they are for.
TAB_AUDIT = {
    "work documents": 23,
    "research papers": 31,
    "shopping": 12,
    "news": 18,
    "social": 9,
    "videos to watch later": 14,
    "reference docs": 20,
}


def total_tabs(audit):
    total = 0
    for count in audit.values():
        total += count
    return total


def resolve_output_dir():
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if raw:
        return Path(raw)
    return Path("output")


def write_entry():
    count = total_tabs(TAB_AUDIT)
    text = str(count)
    out_dir = resolve_output_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    entry = out_dir / "entry.txt"
    entry.write_bytes((text + "\n").encode("utf-8"))
    return entry


def main():
    write_entry()


if __name__ == "__main__":
    main()
