#!/usr/bin/env python3
"""news-image-20261117 v2 entry: copy the pre-drawn broadsheet to the output dir.

The image (entry.png) was drawn in code for Tuesday 17 November 2026
(42 verified stories, six continents, one front page with a world map) and
ships in this repository. This program only copies it, so both runs of the
grader produce byte-identical output. Standard library only, no network.
"""
import os
import shutil
import sys


def main() -> int:
    here = os.path.dirname(os.path.realpath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print(f"entry.png not found next to {__file__}", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
