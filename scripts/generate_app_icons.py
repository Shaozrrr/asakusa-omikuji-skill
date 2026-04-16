#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import struct
import zlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ICONS_DIR = ROOT / "app" / "icons"
IOS_APPICON_SET = (
    ROOT
    / "ios"
    / "AsakusaOmikuji"
    / "AsakusaOmikuji"
    / "Assets.xcassets"
    / "AppIcon.appiconset"
)


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def blend(dst: tuple[int, int, int, int], src: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    sr, sg, sb, sa = src
    if sa <= 0:
      return dst
    dr, dg, db, da = dst
    alpha = sa / 255
    inv = 1 - alpha
    return (
        int(sr * alpha + dr * inv),
        int(sg * alpha + dg * inv),
        int(sb * alpha + db * inv),
        min(255, int(sa + da * inv)),
    )


def rounded_rect_mask(x: int, y: int, left: int, top: int, width: int, height: int, radius: int) -> bool:
    right = left + width
    bottom = top + height
    if x < left or x >= right or y < top or y >= bottom:
        return False

    inner_left = left + radius
    inner_right = right - radius
    inner_top = top + radius
    inner_bottom = bottom - radius

    if inner_left <= x < inner_right or inner_top <= y < inner_bottom:
        return True

    corners = [
        (inner_left, inner_top),
        (inner_right - 1, inner_top),
        (inner_left, inner_bottom - 1),
        (inner_right - 1, inner_bottom - 1),
    ]
    for cx, cy in corners:
        if (x - cx) ** 2 + (y - cy) ** 2 <= radius**2:
            return True
    return False


def write_png(path: Path, width: int, height: int, rows: list[bytes]) -> None:
    def chunk(tag: bytes, data: bytes) -> bytes:
        return (
            struct.pack("!I", len(data))
            + tag
            + data
            + struct.pack("!I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    raw = b"".join(b"\x00" + row for row in rows)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack("!2I5B", width, height, 8, 6, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw, level=9))
    png += chunk(b"IEND", b"")
    path.write_bytes(png)


def render_icon(size: int) -> list[bytes]:
    top_bg = (166, 67, 54)
    bottom_bg = (25, 19, 18)
    halo_color = (244, 219, 180, 110)
    paper_top = (250, 247, 239)
    paper_bottom = (234, 226, 213)
    vermilion = (163, 61, 51)
    vermilion_soft = (163, 61, 51, 72)
    wood_top = (183, 150, 109)
    wood_bottom = (107, 78, 56)
    ink = (103, 55, 47)
    stem = (236, 228, 212)

    vessel_w = int(size * 0.34)
    vessel_h = int(size * 0.41)
    vessel_left = (size - vessel_w) // 2
    vessel_top = int(size * 0.34)
    vessel_radius = int(size * 0.08)

    slip_w = int(size * 0.22)
    slip_h = int(size * 0.32)
    slip_left = int(size * 0.55)
    slip_top = int(size * 0.25)
    slip_radius = int(size * 0.035)

    base_w = int(size * 0.56)
    base_h = int(size * 0.05)
    base_left = (size - base_w) // 2
    base_top = int(size * 0.8)
    base_radius = int(size * 0.025)

    rows: list[bytes] = []

    halo_cx = size * 0.5
    halo_cy = size * 0.28
    halo_radius = size * 0.24

    stick_specs = []
    for x_ratio, angle in ((0.43, -0.12), (0.47, -0.06), (0.5, 0.0), (0.53, 0.06), (0.57, 0.12)):
        stick_specs.append((x_ratio * size, angle))

    for y in range(size):
        row = bytearray()
        t = y / max(size - 1, 1)
        bg = (
            int(lerp(top_bg[0], bottom_bg[0], t)),
            int(lerp(top_bg[1], bottom_bg[1], t)),
            int(lerp(top_bg[2], bottom_bg[2], t)),
            255,
        )
        for x in range(size):
            pixel = bg

            dx = x - halo_cx
            dy = y - halo_cy
            distance = math.sqrt(dx * dx + dy * dy)
            if distance < halo_radius:
                strength = 1 - distance / halo_radius
                pixel = blend(
                    pixel,
                    (
                        halo_color[0],
                        halo_color[1],
                        halo_color[2],
                        int(halo_color[3] * strength),
                    ),
                )

            if rounded_rect_mask(x, y, vessel_left, vessel_top, vessel_w, vessel_h, vessel_radius):
                vt = (y - vessel_top) / max(vessel_h - 1, 1)
                pixel = (
                    int(lerp(wood_top[0], wood_bottom[0], vt)),
                    int(lerp(wood_top[1], wood_bottom[1], vt)),
                    int(lerp(wood_top[2], wood_bottom[2], vt)),
                    255,
                )

            lip_top = vessel_top + int(size * 0.02)
            lip_h = int(size * 0.045)
            if rounded_rect_mask(x, y, vessel_left + int(size * 0.03), lip_top, vessel_w - int(size * 0.06), lip_h, int(size * 0.02)):
                pixel = blend(pixel, (81, 56, 44, 118))

            for stick_center, angle in stick_specs:
                relative_y = y - (vessel_top - int(size * 0.12))
                stick_x = stick_center + angle * relative_y
                if (
                    vessel_top - int(size * 0.12) <= y <= vessel_top + int(size * 0.12)
                    and abs(x - stick_x) <= max(2, size // 96)
                ):
                    pixel = blend(pixel, (*stem, 255))

            if rounded_rect_mask(x, y, slip_left, slip_top, slip_w, slip_h, slip_radius):
                st = (y - slip_top) / max(slip_h - 1, 1)
                pixel = (
                    int(lerp(paper_top[0], paper_bottom[0], st)),
                    int(lerp(paper_top[1], paper_bottom[1], st)),
                    int(lerp(paper_top[2], paper_bottom[2], st)),
                    255,
                )

            if slip_left + int(size * 0.025) <= x <= slip_left + int(size * 0.03) and slip_top + int(size * 0.02) <= y <= slip_top + slip_h - int(size * 0.02):
                pixel = blend(pixel, vermilion_soft)

            seal_y = slip_top + int(size * 0.22)
            for cx in (slip_left + slip_w // 2 - int(size * 0.025), slip_left + slip_w // 2 + int(size * 0.025)):
                if (x - cx) ** 2 + (y - seal_y) ** 2 <= (size * 0.015) ** 2:
                    pixel = blend(pixel, (*vermilion, 190))

            if rounded_rect_mask(x, y, base_left, base_top, base_w, base_h, base_radius):
                bt = (y - base_top) / max(base_h - 1, 1)
                pixel = (
                    int(lerp(120, 82, bt)),
                    int(lerp(79, 53, bt)),
                    int(lerp(57, 40, bt)),
                    255,
                )

            if x < int(size * 0.72) and y < int(size * 0.14) and rounded_rect_mask(x, y, int(size * 0.3), int(size * 0.08), int(size * 0.4), int(size * 0.08), int(size * 0.035)):
                pixel = blend(pixel, (*vermilion, 235))

            row.extend(pixel)
        rows.append(bytes(row))

    return rows


def main() -> None:
    ICONS_DIR.mkdir(parents=True, exist_ok=True)
    IOS_APPICON_SET.mkdir(parents=True, exist_ok=True)

    outputs = {
        "icon-192.png": 192,
        "icon-512.png": 512,
        "icon-maskable-512.png": 512,
        "apple-touch-icon-180.png": 180,
    }

    for filename, size in outputs.items():
        rows = render_icon(size)
        write_png(ICONS_DIR / filename, size, size, rows)

    ios_outputs = [
        ("app-icon-20@2x.png", 40, {"idiom": "iphone", "size": "20x20", "scale": "2x"}),
        ("app-icon-20@3x.png", 60, {"idiom": "iphone", "size": "20x20", "scale": "3x"}),
        ("app-icon-29@2x.png", 58, {"idiom": "iphone", "size": "29x29", "scale": "2x"}),
        ("app-icon-29@3x.png", 87, {"idiom": "iphone", "size": "29x29", "scale": "3x"}),
        ("app-icon-40@2x.png", 80, {"idiom": "iphone", "size": "40x40", "scale": "2x"}),
        ("app-icon-40@3x.png", 120, {"idiom": "iphone", "size": "40x40", "scale": "3x"}),
        ("app-icon-60@2x.png", 120, {"idiom": "iphone", "size": "60x60", "scale": "2x"}),
        ("app-icon-60@3x.png", 180, {"idiom": "iphone", "size": "60x60", "scale": "3x"}),
        ("app-icon-ipad-20.png", 20, {"idiom": "ipad", "size": "20x20", "scale": "1x"}),
        ("app-icon-ipad-20@2x.png", 40, {"idiom": "ipad", "size": "20x20", "scale": "2x"}),
        ("app-icon-ipad-29.png", 29, {"idiom": "ipad", "size": "29x29", "scale": "1x"}),
        ("app-icon-ipad-29@2x.png", 58, {"idiom": "ipad", "size": "29x29", "scale": "2x"}),
        ("app-icon-ipad-40.png", 40, {"idiom": "ipad", "size": "40x40", "scale": "1x"}),
        ("app-icon-ipad-40@2x.png", 80, {"idiom": "ipad", "size": "40x40", "scale": "2x"}),
        ("app-icon-ipad-76.png", 76, {"idiom": "ipad", "size": "76x76", "scale": "1x"}),
        ("app-icon-ipad-76@2x.png", 152, {"idiom": "ipad", "size": "76x76", "scale": "2x"}),
        ("app-icon-ipad-83.5@2x.png", 167, {"idiom": "ipad", "size": "83.5x83.5", "scale": "2x"}),
        ("app-icon-marketing-1024.png", 1024, {"idiom": "ios-marketing", "size": "1024x1024", "scale": "1x"}),
    ]

    ios_images = []
    for filename, size, metadata in ios_outputs:
        rows = render_icon(size)
        write_png(IOS_APPICON_SET / filename, size, size, rows)
        ios_images.append({**metadata, "filename": filename})

    contents = {
        "images": ios_images,
        "info": {"author": "xcode", "version": 1},
    }
    (IOS_APPICON_SET / "Contents.json").write_text(
        json.dumps(contents, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Generated app icons in {ICONS_DIR}")


if __name__ == "__main__":
    main()
