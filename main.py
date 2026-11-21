#!/usr/bin/env python3
"""make.fun entry for the competition news-image-20261121.

The entry itself is a fixed front-page image, entry.png beside this
file (a 1024x1024 JPEG, whatever the name says). This program copies
it, byte for byte, into $MAKEFUN_OUTPUT_DIR/entry.png, so the two
runs the grader makes always produce identical output. It draws
nothing, reads no clock, rolls no dice and touches no network.
The image is a 1024x1024 JPEG of 265818 bytes, dated
SATURDAY 21 NOVEMBER 2026 in its masthead.
"""

from pathlib import Path
import os
import shutil
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def output_dir() -> Path:
    """Where the grader wants the entry: $MAKEFUN_OUTPUT_DIR or /output."""
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")


def main() -> int:
    if not SOURCE.is_file():
        print("entry.png is missing beside main.py", file=sys.stderr)
        return 1
    dest_dir = output_dir()
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "entry.png"
    shutil.copyfile(SOURCE, dest)
    if dest.stat().st_size != SOURCE.stat().st_size:
        print("copied entry.png does not match the source size", file=sys.stderr)
        return 1
    print(f"entry.png written: {dest.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
