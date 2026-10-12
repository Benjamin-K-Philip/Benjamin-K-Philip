"""Recolour github-profile-summary-cards 'algolia' SVGs into a custom Tron theme.

Usage: python3 tronify.py <src_dir> <dst_dir>
"""
import pathlib
import re
import sys

CYAN = "#00E5FF"   # titles, icons, graph line, border
TEXT = "#A8F3FF"   # body text and axis labels
BG = "#000000"     # pure black grid

# algolia colour -> Tron colour
PALETTE = {
    "#050f2c": BG,
    "#00aeff": CYAN,
    "#2dde98": CYAN,
    "#ffffff": TEXT,
}

GLOW = (
    '<defs><filter id="tron-glow" x="-20%" y="-20%" width="140%" height="140%">'
    '<feGaussianBlur stdDeviation="2.5" result="b"/>'
    '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>'
    "</filter></defs>"
)


def tronify(svg: str) -> str:
    # 1. swap palette (case-insensitive)
    svg = re.sub(
        r"#[0-9a-fA-F]{6}\b",
        lambda m: PALETTE.get(m.group(0).lower(), m.group(0)),
        svg,
    )
    # 2. visible neon border on the card background rect
    svg = re.sub(
        r'(<rect x="1" y="1"[^>]*?)stroke="#000000"([^>]*?)stroke-opacity="0"',
        rf'\1stroke="{CYAN}"\2stroke-opacity="0.9"',
        svg,
        count=1,
    )
    # 3. light-trail graph: translucent fill, bright glowing edge
    svg = re.sub(
        rf'stroke="{CYAN}" fill="{CYAN}" opacity="1"',
        rf'stroke="{CYAN}" stroke-width="2" fill="{CYAN}" fill-opacity="0.18" '
        rf'opacity="1" filter="url(#tron-glow)"',
        svg,
    )
    # 4. glow on the title
    svg = svg.replace(
        f"font-size: 22px; fill: {CYAN};",
        f"font-size: 22px; fill: {CYAN}; filter: url(#tron-glow);",
    )
    # 5. inject the glow filter definition right after the opening <svg ...>
    if "tron-glow" in svg and 'id="tron-glow"' not in svg:
        svg = re.sub(r"(<svg[^>]*>)", r"\1" + GLOW, svg, count=1)
    return svg


def main() -> None:
    src, dst = map(pathlib.Path, sys.argv[1:3])
    dst.mkdir(parents=True, exist_ok=True)
    for f in sorted(src.glob("*.svg")):
        (dst / f.name).write_text(tronify(f.read_text()))
        print("tronified", f.name)


if __name__ == "__main__":
    main()
