#!/usr/bin/env python3
"""make.fun entry for news-image-20261118.

Sum up 18 November 2026's world news in one image.

The program writes one image to /output/entry.png by copying the
image this repository holds (entry.png). That is the simplest
program the brief allows, and it keeps the entry deterministic:
no network, no randomness, no timestamps, so both runs write
the exact same bytes.

The image itself is a newspaper front page drawn for this bounty.
Its stories are all grounded in reporting from 18 November 2026:
the US strike on Iran's Qeshm Island and Iran's drone replies
against Bahrain and Kuwait; Ukraine's second-day strike on the
Kerch Bridge; Xi hosting Putin in Shenzhen ahead of Thursday's
trilateral summit with Trump; Mary Peltola winning Alaska and a
56-44 Democratic Senate; the Ebola outbreak in DR Congo more
than doubling; plus the Siberia plane crash, the Papua New
Guinea quake, Cyclone Xavier and Nvidia's record revenue.
See build_image.py for how entry.png was drawn, with sources.
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
TARGET = "/output/entry.png"


def main():
    if not os.path.isfile(SOURCE):
        print("entry.png is missing from the repository", file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(TARGET), exist_ok=True)
    shutil.copyfile(SOURCE, TARGET)
    # The brief requires both runs to write the same bytes: verify the
    # copy is byte-identical to the image this repository holds.
    with open(SOURCE, "rb") as f:
        source_hash = hashlib.sha256(f.read()).hexdigest()
    with open(TARGET, "rb") as f:
        target_hash = hashlib.sha256(f.read()).hexdigest()
    if source_hash != target_hash:
        print("copy mismatch: output differs from entry.png", file=sys.stderr)
        return 1
    size = os.path.getsize(TARGET)
    if size > 1024 * 1024:
        print("entry.png is over the 1 MiB limit", file=sys.stderr)
        return 1
    print("wrote", TARGET, size, "bytes, sha256", target_hash)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
