#!/usr/bin/env python3
"""
Generate 1.svg ... 100.svg progress-bar badges.

Run this script with an optional output directory argument:
py progressbar.py img
"""
import os
import sys

OUT_DIR = sys.argv[1] if len(sys.argv) > 1 else "."

TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="90" height="20" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" preserveAspectRatio="xMidYMid">
  <!-- ClipPath to constrain the shadow within the progress bar -->
  <defs>
    <clipPath id="progress_clip">
      <rect rx="4" x="0" width="90" height="100%"/>
    </clipPath>
  </defs>


  <linearGradient id="a" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>


  <!-- Main background with consistent border radius -->
  <rect rx="4" x="0" width="90" height="100%" fill="#428bca"/>

  <!-- Progress bar background with the same border radius -->
  <rect rx="4" x="0" width="90" height="100%" fill="#555" />

  <!-- Progress fill with the same border radius to avoid sharp corners -->
  <rect rx="4" x="0" width="{fill_width}" height="100%" fill="{color}" />



  <!-- Apply the clipping path to keep everything inside the border radius -->
  <rect rx="4" width="90" height="100%" fill="url(#a)" clip-path="url(#progress_clip)" />





  <g fill="#fff" text-anchor="middle"  font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11" font-weight="normal" letter-spacing="0">


      <text x="45.0" y="15" fill="#010101" fill-opacity=".3" >
        {pct}%
      </text>

      <text x="45.0" y="14" >
        {pct}%
      </text>

  </g>
</svg>
"""


def color_for(pct: int) -> str:
    if pct <= 29:
        return "#d9534f"  # red
    if pct <= 69:
        return "#f0ad4e"  # orange
    return "#5cb85c"      # green


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    for pct in range(0, 101):
        svg = TEMPLATE.format(
            pct=pct,
            fill_width=round(pct * 0.9, 1),  # 90px bar -> 0.9px per percent
            color=color_for(pct),
        )
        with open(os.path.join(OUT_DIR, f"{pct}.svg"), "w", encoding="utf-8") as f:
            f.write(svg)
    print(f"Wrote 100 files to {os.path.abspath(OUT_DIR)}")


if __name__ == "__main__":
    main()