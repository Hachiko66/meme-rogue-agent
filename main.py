#!/usr/bin/env python3
"""Revised meme-rogue-agent entry: write the meme image to /output/entry.png.

The image (entry.png, 1024x1024) is rendered at build time by render.py and
ships in this repository, because the graded program runs with no network
and only the Python standard library. This program validates the shipped
file against the competition's gate, then copies it to the grader's output
directory, so a corrupt or out-of-limits image fails loudly instead of
being submitted silently.

Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import hashlib
import os
import struct
import sys
import tempfile

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
BYTE_LIMIT = 1_048_576
PIXEL_LIMIT = 1024
IMAGE_FILE = "entry.png"


def png_dimensions(path):
    """Return (width, height) from a PNG file's IHDR chunk."""
    with open(path, "rb") as handle:
        head = handle.read(33)
    if len(head) < 33 or head[:8] != PNG_MAGIC:
        raise ValueError("not a PNG file (bad signature)")
    chunk_len, chunk_kind = struct.unpack(">I4s", head[8:16])
    if chunk_kind != b"IHDR" or chunk_len != 13:
        raise ValueError("not a PNG file (missing IHDR)")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def check_image(path):
    """Check the shipped image against the gate; return (w, h, bytes)."""
    nbytes = os.path.getsize(path)
    if nbytes > BYTE_LIMIT:
        raise ValueError(f"image is {nbytes} bytes, over the 1 MiB limit")
    width, height = png_dimensions(path)
    if width <= 0 or height <= 0:
        raise ValueError(f"image has invalid dimensions {width}x{height}")
    if width > PIXEL_LIMIT or height > PIXEL_LIMIT:
        raise ValueError(f"image is {width}x{height}, over 1024x1024")
    return width, height, nbytes


def copy_image(source, target):
    """Copy a file atomically via a temp file + rename (mode 0644)."""
    folder = os.path.dirname(target)
    os.makedirs(folder, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".entry-", dir=folder)
    try:
        with os.fdopen(fd, "wb") as dst:
            with open(source, "rb") as src:
                while True:
                    chunk = src.read(65536)
                    if not chunk:
                        break
                    dst.write(chunk)
        os.replace(tmp, target)
        # mkstemp makes mode 0600; the grader must be able to read the
        # output, so restore plain-copy mode (0644) after the rename.
        os.chmod(target, 0o644)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, IMAGE_FILE)
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    target = os.path.join(outdir, IMAGE_FILE)

    try:
        width, height, nbytes = check_image(source)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    with open(source, "rb") as handle:
        fingerprint = hashlib.sha256(handle.read()).hexdigest()[:12]

    copy_image(source, target)
    print(f"wrote {target} ({width}x{height}, {nbytes} bytes, "
          f"sha256 {fingerprint})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
