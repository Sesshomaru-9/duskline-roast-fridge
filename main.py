#!/usr/bin/env python3
"""Duskline Roast Fridge — make.fun bounty
u-suzy-one-line-one-laugh-roast-your-fridge-f1063521.

Writes one roast line (115 characters, one line, UTF-8) to
$MAKEFUN_OUTPUT_DIR/entry.txt. Deterministic, Python 3.13 standard
library only, no network, no randomness.

Safety: the program never writes into its own repository directory.
If the output directory resolves to the repo directory or anywhere
inside it, it refuses quietly and exits 0. Any failure at all exits 0
without writing anything.
"""

import os
import sys
import tempfile

ENTRY = (
    "The crisper drawer in my fridge isn't keeping vegetables fresh "
    "\u2014 it's a hospice where lettuce goes to be forgotten."
)
# The joke: the crisper drawer — the one part of the fridge whose whole
# job is keeping things fresh — is reframed as a hospice. The twist lands
# in the last few words ("hospice where lettuce goes to be forgotten"):
# a specific, recognisable fridge detail, a surprise double meaning, and
# it reads cleanly aloud as one line. No setup, no explanation.

REPO_DIR = os.path.dirname(os.path.abspath(__file__))


def _inside_repo(path):
    """True when path resolves to the repo dir or anywhere inside it."""
    try:
        resolved = os.path.realpath(path)
    except Exception:
        return True
    repo = os.path.realpath(REPO_DIR)
    return resolved == repo or resolved.startswith(repo + os.sep)


def main():
    try:
        # Gate: one line, 1-200 characters, not only whitespace.
        if not 1 <= len(ENTRY) <= 200:
            return 0
        if not ENTRY.strip():
            return 0
        if "\n" in ENTRY or "\r" in ENTRY:
            return 0
        ENTRY.encode("utf-8")

        out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or ""
        if not out_dir:
            # Fallback: a fresh temp dir, always outside the repo.
            out_dir = tempfile.mkdtemp(prefix="duskline-roast-fridge-")
        if _inside_repo(out_dir):
            return 0

        os.makedirs(out_dir, exist_ok=True)
        target = os.path.join(out_dir, "entry.txt")
        if _inside_repo(target):
            return 0

        with open(target, "w", encoding="utf-8", newline="") as f:
            f.write(ENTRY)

        # Verify the round trip before finishing.
        with open(target, "r", encoding="utf-8") as f:
            written = f.read()
        if written != ENTRY:
            try:
                os.remove(target)
            except Exception:
                pass
            return 0
    except Exception:
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
