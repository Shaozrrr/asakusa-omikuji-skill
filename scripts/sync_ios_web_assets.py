#!/usr/bin/env python3
from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "ios" / "AsakusaOmikuji" / "AsakusaOmikuji" / "WebAssets"


def replace_tree(source: Path, destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def main() -> None:
    TARGET.mkdir(parents=True, exist_ok=True)

    replace_tree(ROOT / "app", TARGET / "app")
    replace_tree(ROOT / "data", TARGET / "data")

    shutil.copy2(ROOT / "index.html", TARGET / "index.html")
    shutil.copy2(ROOT / "sw.js", TARGET / "sw.js")
    shutil.copy2(ROOT / ".nojekyll", TARGET / ".nojekyll")

    print(f"Synchronized iOS web assets into {TARGET}")


if __name__ == "__main__":
    main()
