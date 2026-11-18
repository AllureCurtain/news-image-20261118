#!/usr/bin/env python3
"""news-image-20261118 entrypoint.

Copies the front-page image (news.png, a newspaper-style summary of
Wednesday 18 November 2026's world news) to /output/entry.png.

Deterministic, standard library only, no network: the same bytes are
written on every run.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "news.png")


def main():
    if not os.path.isfile(SRC):
        print(f"missing image: {SRC}", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dest)
    # The copy must be exact: same size as the source image.
    if os.path.getsize(dest) != os.path.getsize(SRC):
        print("copy size mismatch", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
