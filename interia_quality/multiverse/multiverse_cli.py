"""
multiverse_cli.py — Print ASCII heatmap of the multiverse distance matrix.
"""

from __future__ import annotations

import json
from pathlib import Path

def main():
    """ Main function of multiverse_cli.py — Print ASCII heatmap of the multiverse distance matrix."""
    matrix_path = Path("interia_multiverse_matrix.json")
    if not matrix_path.exists():
        print("❌ interia_multiverse_matrix.json missing.")
        return 1
    try:
        matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise FileNotFoundError(
            f"{matrix_path} JSON decoding failed: {e}."
        )
    names = list(matrix.keys())

    print("🌌 InterIA Multiverse Distance Matrix\n")
    header = "        " + " ".join(f"{n[:6]:>6}" for n in names)
    print(header)
    print("        " + "-" * (7 * len(names)))

    for a in names:
        row = f"{a[:6]:>6} |"
        for b in names:
            d = matrix[a][b]
            # turn distance into heat symbol
            if d == 0:
                sym = "·"
            elif d < 1:
                sym = "░"
            elif d < 3:
                sym = "▒"
            else:
                sym = "▓"
            row += f"   {sym}  "
        print(row)

    print("\nLegend: · identical — ░ close — ▒ medium — ▓ distant")

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
