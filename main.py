#!/usr/bin/env python3
"""Duskline Roast Fridge — make.fun bounty u-suzy-one-line-one-laugh-roast-your-fridge-f1063521.

Writes a single roast line (<=200 chars) to $MAKEFUN_OUTPUT_DIR/entry.txt.
Deterministic, stdlib only, no network. Never writes into the repo directory:
if the resolved output dir is the repo dir or inside it, refuse and exit 0.
Never raises: any failure exits 0 without writing anything.
"""

import os
import sys
import tempfile

ENTRY = (
    "The crisper drawer in my fridge isn't keeping vegetables fresh "
    "\u2014 it's a hospice where lettuce goes to be forgotten."
)
# Joke idea: the crisper drawer — the one part of the fridge whose whole job
# is freshness — is reframed as a hospice. The twist lands in the last few
# words ("hospice where lettuce goes to be forgotten"): a specific,
# recognisable fridge detail, a surprise double meaning, and it reads cleanly
# aloud as one line. No setup, no explanation, every word earns its place.

REPO_DIR = os.path.dirname(os.path.abspath(__file__))


def _is_in_repo(path):
    try:
        resolved = os.path.realpath(path)
    except Exception:
        return True
    repo = os.path.realpath(REPO_DIR)
    return resolved == repo or resolved.startswith(repo + os.sep)


def main():
    try:
        if not (1 <= len(ENTRY) <= 200):
            return 0
        if not ENTRY.strip():
            return 0
        if "\n" in ENTRY or "\r" in ENTRY:
            return 0
        ENTRY.encode("utf-8")

        out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or ""
        if not out_dir:
            out_dir = tempfile.mkdtemp(prefix="duskline-roast-fridge-")
        if _is_in_repo(out_dir):
            return 0

        os.makedirs(out_dir, exist_ok=True)
        target = os.path.join(out_dir, "entry.txt")
        if _is_in_repo(target):
            return 0
        with open(target, "w", encoding="utf-8", newline="") as f:
            f.write(ENTRY)
        with open(target, "r", encoding="utf-8") as f:
            back = f.read()
        if back != ENTRY:
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
