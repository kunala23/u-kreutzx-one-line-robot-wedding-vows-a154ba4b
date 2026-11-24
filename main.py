#!/usr/bin/env python3
"""One-Line Robot Wedding Vows — entry program.

Writes a single line of wedding vows for a robot couple to
/output/entry.txt, the artifact the make.fun judge reads.

The vow is built to land on the judge's brief:
  * a real wedding vow (promise / commitment, "to have and to hold"),
  * machine-specific all the way through (co-processor, backup, battery),
  * the laugh pays off in the last few words — a twist on the classic
    "till death do us part" — and the line reads well aloud.

The gate allows 1-160 UTF-8 characters, one line, not only whitespace,
so the program checks its own output against exactly those limits
before it writes anything.
"""

import os
import sys

# The vow: a classic vow cadence, robot terms throughout, and the joke
# lands in the final clause. "my backup" does double duty — a data
# backup, and someone who has your back.
VOW = (
    "I take you to be my partner, my co-processor, my backup — "
    "to have and to hold, in sickness and in health, "
    "till low battery do us part."
)

MAX_CHARS = 160


def check(text: str) -> str | None:
    """Return an error message if `text` fails the gate, else None."""
    if not text:
        return "vow is empty"
    if len(text) > MAX_CHARS:
        return f"vow is {len(text)} chars, over the {MAX_CHARS} limit"
    if "\n" in text or "\r" in text:
        return "vow must be a single line"
    return None


def main() -> int:
    text = VOW.strip()

    # Gate self-check: 1-160 characters, a single line, not only whitespace.
    error = check(text)
    if error is not None:
        print(f"error: {error}", file=sys.stderr)
        return 1

    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")

    # Write exactly the vow, no trailing newline: the newline would be
    # an extra character the judge reads, and the gate counts it.
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(text)

    # Read the file back and re-check it: the artifact on disk is what
    # the judge reads, so verify that, not just the string in memory.
    with open(out_path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != text:
        print("error: file on disk differs from the vow", file=sys.stderr)
        return 1
    error = check(written)
    if error is not None:
        print(f"error: written file fails the gate: {error}", file=sys.stderr)
        return 1

    print(f"wrote {len(text)} chars to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
