#!/usr/bin/env python3
"""Serve the 20 November 2026 world-news front page: copy entry.png to $MAKEFUN_OUTPUT_DIR.

The image is drawn offline at 4x supersample with Pillow and downscaled to
1024x1024, so the committed PNG is the deterministic artifact this program
serves. Stories are real events of Friday 20 November 2026 with outlet
attributions.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SRC, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
