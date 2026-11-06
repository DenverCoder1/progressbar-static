#!/usr/bin/env python3
"""
Generate 0.svg ... 100.svg progress-bar badges in four styles.

Output layout (under the optional base directory argument, default "."):
    img/          flat
    square/       square
    plastic/      plastic
    for-the-badge/ for-the-badge

Usage:
    py progressbar.py [base_dir]
"""

import os
import sys

BASE_DIR = sys.argv[1] if len(sys.argv) > 1 else "."

HEADER = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="90" height="{height}" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" preserveAspectRatio="xMidYMid">
  <!-- ClipPath to constrain the shadow within the progress bar -->
  <defs>
    <clipPath id="progress_clip">
      <rect rx="{rx}" x="0" width="90" height="100%"/>
    </clipPath>
  </defs>
"""

GRADIENT_A = """
  <linearGradient id="a" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
"""

BARS = """
  <!-- Main background with consistent border radius -->
  <rect rx="{rx}" x="0" width="90" height="100%" fill="{main_bg}"/>

  <!-- Progress bar background with the same border radius -->
  <rect rx="{rx}" x="0" width="90" height="100%" fill="{track}" />

  <!-- Progress fill with the same border radius to avoid sharp corners -->
  <rect rx="{rx}" x="0" width="{{fill_width}}" height="100%" fill="{{color}}" />

  <!-- Apply the clipping path to keep everything inside the border radius -->
{overlay}"""

OVERLAY = """
  <!-- Subtle top-to-bottom shading, clipped to the rounded bar -->
  <rect rx="{rx}" width="90" height="100%" fill="url(#a)" clip-path="url(#progress_clip)" />
"""

PLASTIC_GLOSS = """
  <!-- Gloss for progress bar -->
  <linearGradient id="progress_gloss" x1="0" y1="0" x2="0" y2="0.6">
    <stop offset="0%" stop-color="rgba(255,255,255,0.85)" />
    <stop offset="60%" stop-color="rgba(255,255,255,0)" />
  </linearGradient>
  <rect x="0" y="0" width="90" height="12" fill="url(#progress_gloss)" clip-path="url(#progress_clip)" />

  <!-- Shadow for progress bar -->
  <linearGradient id="progress_shadow" x1="0" y1="0.6" x2="0" y2="1">
    <stop offset="0%" stop-color="rgba(0,0,0,0)" />
    <stop offset="100%" stop-color="rgba(0,0,0,0.2)" />
  </linearGradient>
  <rect x="0" y="9" width="89" height="11" fill="url(#progress_shadow)" clip-path="url(#progress_clip)" />
"""

TEXT_SHADOWED = """
  <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11" font-weight="normal" letter-spacing="0">
    <text x="45.0" y="15" fill="#010101" fill-opacity=".3" >
      {pct}%
    </text>
    <text x="45.0" y="14" >
      {pct}%
    </text>
  </g>
</svg>
"""

TEXT_PLAIN = """
  <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11" font-weight="normal" letter-spacing="0">
    <text x="45.0" y="14" >
      {pct}%
    </text>
  </g>
</svg>
"""

TEXT_BADGE = """
  <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="10" font-weight="bold" letter-spacing="2">
    <text x="45.0" y="18" >
      {pct}%
    </text>
  </g>
</svg>
"""


def build(height, rx, main_bg, track, gradient, gloss, text):
    return (
        HEADER.format(height=height, rx=rx)
        + (GRADIENT_A if gradient else "")
        + BARS.format(
            rx=rx,
            main_bg=main_bg,
            track=track,
            overlay=OVERLAY.format(rx=rx) if gradient else "",
        )
        + gloss
        + text
    )


# name -> (directory, template, (red, orange, green))
STYLES = {
    "flat": (
        "img",
        build(20, 4, "#428bca", "#555", True, "", TEXT_SHADOWED),
        ("#d9534f", "#f0ad4e", "#5cb85c"),
    ),
    "square": (
        "square",
        build(20, 0, "#555", "#555", True, "", TEXT_PLAIN),
        ("#e05d44", "#fe7d37", "#97CA00"),
    ),
    "plastic": (
        "plastic",
        build(20, 5, "#555", "#ECEFF1", True, PLASTIC_GLOSS, TEXT_SHADOWED),
        ("#e05d44", "#fe7d37", "#91bc13"),
    ),
    "for-the-badge": (
        "for-the-badge",
        build(28, 0, "#555", "#555", False, "", TEXT_BADGE),
        ("#e05d44", "#fe7d37", "#97ca00"),
    ),
}


def color_for(pct: int, palette) -> str:
    red, orange, green = palette
    if pct <= 29:
        return red
    if pct <= 69:
        return orange
    return green


def main() -> None:
    for name, (subdir, template, palette) in STYLES.items():
        out_dir = os.path.join(BASE_DIR, subdir)
        os.makedirs(out_dir, exist_ok=True)
        for pct in range(0, 101):
            svg = template.format(
                pct=pct,
                fill_width=round(pct * 0.9, 1),  # 90px bar -> 0.9px per percent
                color=color_for(pct, palette),
            )
            with open(os.path.join(out_dir, f"{pct}.svg"), "w", encoding="utf-8") as f:
                f.write(svg)
        print(f"{name}: wrote 101 files to {os.path.abspath(out_dir)}")


if __name__ == "__main__":
    main()
