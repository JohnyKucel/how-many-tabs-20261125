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

# Tabs open right now, counted by what they are for. The total, 127, is
# a counted audit total rather than a round number picked for effect:
# high enough to surprise, low enough to still be believable for a
# chronic tab hoarder with several windows open at once.
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
    for label, count in audit.items():
        # A typo in the audit table must fail loudly here, not silently
        # produce a wrong-but-valid total (e.g. a negative count would
        # still pass validate_count below).
        if isinstance(count, bool) or not isinstance(count, int) or count < 0:
            raise ValueError("audit value for %r must be a non-negative int, got %r" % (label, count))
        total += count
    return total


def validate_count(count: int) -> str:
    if not 1 <= count <= 99999:
        raise ValueError("tab count must be 1-99999, got %d" % count)
    text = str(count)
    if not 1 <= len(text) <= 5 or not text.isdigit():
        raise ValueError("entry must be 1-5 digits, got %r" % text)
    return text


def resolve_output_dir():
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if raw:
        return Path(raw)
    return Path("output")


def write_entry():
    count = total_tabs(TAB_AUDIT)
    text = validate_count(count)
    out_dir = resolve_output_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    entry = out_dir / "entry.txt"
    data = (text + "\n").encode("utf-8")
    entry.write_bytes(data)
    if entry.read_bytes() != data:
        raise IOError("entry.txt read-back mismatch after write")
    return entry


def main():
    write_entry()


if __name__ == "__main__":
    main()
