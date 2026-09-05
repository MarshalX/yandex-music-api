#!/usr/bin/env python3
"""Generate deterministic AppIcon assets and original lossless demo tones."""

from __future__ import annotations

import argparse
import json
import math
import struct
import wave
from pathlib import Path

from PIL import Image


ICON_SPECS = [
    ("iphone", "20x20", "2x", 40),
    ("iphone", "20x20", "3x", 60),
    ("iphone", "29x29", "2x", 58),
    ("iphone", "29x29", "3x", 87),
    ("iphone", "40x40", "2x", 80),
    ("iphone", "40x40", "3x", 120),
    ("iphone", "60x60", "2x", 120),
    ("iphone", "60x60", "3x", 180),
    ("ipad", "20x20", "1x", 20),
    ("ipad", "20x20", "2x", 40),
    ("ipad", "29x29", "1x", 29),
    ("ipad", "29x29", "2x", 58),
    ("ipad", "40x40", "1x", 40),
    ("ipad", "40x40", "2x", 80),
    ("ipad", "76x76", "1x", 76),
    ("ipad", "76x76", "2x", 152),
    ("ipad", "83.5x83.5", "2x", 167),
    ("ios-marketing", "1024x1024", "1x", 1024),
]

TRACKS = {
    "northern-lights": (220.00, 277.18, 329.63),
    "glass-river": (196.00, 246.94, 293.66),
    "midnight-maple": (174.61, 220.00, 261.63),
    "soft-static": (146.83, 185.00, 220.00),
}


def generate_icons(source_path: Path, asset_root: Path) -> None:
    app_icon = asset_root / "AppIcon.appiconset"
    app_icon.mkdir(parents=True, exist_ok=True)
    with Image.open(source_path) as opened:
        rgba = opened.convert("RGBA")
        canvas = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
        canvas.alpha_composite(rgba)
        source = canvas.convert("RGB")
        images = []
        for idiom, size, scale, pixels in ICON_SPECS:
            filename = f"AppIcon-{idiom}-{size.replace('.', '_')}@{scale}.png"
            source.resize((pixels, pixels), Image.Resampling.LANCZOS).save(
                app_icon / filename,
                format="PNG",
                optimize=True,
            )
            images.append({"filename": filename, "idiom": idiom, "scale": scale, "size": size})
    (app_icon / "Contents.json").write_text(
        json.dumps({"images": images, "info": {"author": "xcode", "version": 1}}, indent=2),
        encoding="utf-8",
    )
    accent = asset_root / "AccentColor.colorset"
    accent.mkdir(parents=True, exist_ok=True)
    (accent / "Contents.json").write_text(
        json.dumps(
            {
                "colors": [
                    {
                        "color": {
                            "color-space": "srgb",
                            "components": {"alpha": "1.000", "blue": "0.290", "green": "0.120", "red": "0.980"},
                        },
                        "idiom": "universal",
                    }
                ],
                "info": {"author": "xcode", "version": 1},
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (asset_root / "Contents.json").write_text(
        json.dumps({"info": {"author": "xcode", "version": 1}}, indent=2),
        encoding="utf-8",
    )


def generate_tone(path: Path, frequencies: tuple[float, ...], seconds: float = 18.0, sample_rate: int = 44_100) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame_count = int(seconds * sample_rate)
    with wave.open(str(path), "wb") as target:
        target.setnchannels(1)
        target.setsampwidth(2)
        target.setframerate(sample_rate)
        block = bytearray()
        for index in range(frame_count):
            time = index / sample_rate
            fade = min(1.0, time / 1.5, (seconds - time) / 1.5)
            pulse = 0.78 + 0.22 * math.sin(2 * math.pi * 0.08 * time)
            value = sum(math.sin(2 * math.pi * frequency * time + position * 0.55) for position, frequency in enumerate(frequencies))
            value /= len(frequencies)
            sample = int(max(-1, min(1, value * fade * pulse * 0.24)) * 32767)
            block.extend(struct.pack("<h", sample))
            if len(block) >= 64 * 1024:
                target.writeframesraw(block)
                block.clear()
        if block:
            target.writeframesraw(block)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--icon", required=True, type=Path)
    parser.add_argument("--resources", required=True, type=Path)
    args = parser.parse_args()
    asset_root = args.resources / "Assets.xcassets"
    asset_root.mkdir(parents=True, exist_ok=True)
    generate_icons(args.icon, asset_root)
    for name, frequencies in TRACKS.items():
        generate_tone(args.resources / "DemoAudio" / f"{name}.wav", frequencies)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
