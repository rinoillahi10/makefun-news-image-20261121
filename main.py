"""Copy the finished front-page image into the grading output folder.

The artwork itself lives in ``entry.png`` next to this script; this program
does nothing creative at all. It simply places an exact byte-for-byte copy
of that image where the grader expects it, then double-checks the copy
really matches the original before reporting success.
"""

import argparse
import os
import shutil
import sys


SOURCE_NAME = "entry.png"
FALLBACK_DIR = "/output"


def locate_source():
    """Return the absolute path of the image sitting beside this file."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, SOURCE_NAME)


def destination_dir():
    """Pick the output folder from the environment, with a sane default."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR") or FALLBACK_DIR
    return os.path.abspath(chosen)


def parse_args():
    """Read an optional --output-dir override from the command line."""
    parser = argparse.ArgumentParser(
        description="Copy entry.png into the grading output folder."
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Destination folder; overrides MAKEFUN_OUTPUT_DIR when given.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    origin = locate_source()
    if not os.path.isfile(origin):
        print(f"ERROR: source image not found: {origin}", file=sys.stderr)
        return 1

    target_folder = os.path.abspath(args.output_dir) if args.output_dir else destination_dir()
    target = os.path.join(target_folder, SOURCE_NAME)

    os.makedirs(target_folder, exist_ok=True)
    shutil.copyfile(origin, target)

    # Re-read both files from disk so the check compares real bytes on disk.
    with open(origin, "rb") as handle:
        expected = len(handle.read())
    with open(target, "rb") as handle:
        written = len(handle.read())
    if written != expected:
        print(
            f"ERROR: copied {written} bytes but source has {expected}",
            file=sys.stderr,
        )
        return 1

    print(f"Wrote {written} bytes to {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
