#!/usr/bin/env python3
from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"


def main() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)

    DIST.mkdir(parents=True)

    shutil.copytree(ROOT / "app", DIST / "app")
    shutil.copytree(ROOT / "data", DIST / "data")
    shutil.copy2(ROOT / "index.html", DIST / "index.html")
    shutil.copy2(ROOT / ".nojekyll", DIST / ".nojekyll")
    shutil.copy2(ROOT / "sw.js", DIST / "sw.js")

    print(f"Built static site at {DIST}")


if __name__ == "__main__":
    main()
