#!/usr/bin/env python3
from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"


ROOT_INDEX = """<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8" />
    <meta http-equiv="refresh" content="0; url=./app/" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>浅草寺 · 启签</title>
    <script>
      window.location.replace("./app/");
    </script>
  </head>
  <body>
    <p>正在前往 <a href="./app/">浅草寺 · 启签</a>。</p>
  </body>
</html>
"""


def main() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)

    DIST.mkdir(parents=True)

    shutil.copytree(ROOT / "app", DIST / "app")
    shutil.copytree(ROOT / "data", DIST / "data")

    (DIST / "index.html").write_text(ROOT_INDEX, encoding="utf-8")
    (DIST / ".nojekyll").write_text("", encoding="utf-8")

    print(f"Built static site at {DIST}")


if __name__ == "__main__":
    main()
