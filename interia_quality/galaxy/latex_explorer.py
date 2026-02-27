"""
latex_explorer.py — InterIA Galaxy Explorer (CLI core)

Reads latex_galaxy.json, computes global metrics,
and prints a cosmic summary.

Also generates latex_galaxy_summary.json for the HTML explorer.
"""

from __future__ import annotations
import json
from pathlib import Path

def load_galaxy(path="latex_galaxy.json"):
    """Load and return latex_galaxy.json."""
    p = Path(path)
    if not p.exists():
        print("❌ latex_galaxy.json not found. Run `latex-galaxy` first.")
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise FileNotFoundError(
            f"{p} JSON decoding failed: {e}."
        )


def _compute_galaxy_summary(files):
    """Compute aggregate LaTeX galaxy metrics from a files mapping."""
    N = len(files)

    scores = [d["score"] for d in files.values()]
    avg_score = sum(scores) / N

    label_density = sum(d["label_density"] for d in files.values()) / N
    macro_ratio = sum(d["macro_usage_ratio"] for d in files.values()) / N
    cite_density = sum(d["citation_density"] for d in files.values()) / N

    galaxy_score = (
        0.5 * label_density +
        0.3 * macro_ratio +
        0.2 * cite_density
    )

    return {
        "total_files": N,
        "avg_score": round(avg_score, 3),
        "avg_label_density": round(label_density, 3),
        "avg_macro_ratio": round(macro_ratio, 3),
        "avg_cite_density": round(cite_density, 3),
        "galaxy_score": round(galaxy_score, 3),
    }


def _print_galaxy_summary(summary):
    """Pretty-print the galaxy summary to stdout."""
    print("\n🌌 InterIA Galaxy Summary")
    print("-------------------------")
    print(f"Files: {summary['total_files']}")
    print(f"Average score:       {summary['avg_score']}")
    print(f"Label density:       {summary['avg_label_density']}")
    print(f"Macro usage ratio:   {summary['avg_macro_ratio']}")
    print(f"Citation density:    {summary['avg_cite_density']}")
    print(f"Galaxy score (global): {summary['galaxy_score']}")

    # Fun cosmic interpretation
    if summary["galaxy_score"] == 0:
        print("\n🪐 Galaxy dormant: no labels, no macros, no citations yet.")
    elif summary["galaxy_score"] < 0.3:
        print("\n✨ Proto-galactic stage: structure exists but anchors missing.")
    elif summary["galaxy_score"] < 0.6:
        print("\n🌠 Galactic bloom: labels and structure forming beautifully.")
    else:
        print("\n🌟 Advanced galaxy: excellent documentation structure!")


def main():
    """Entry point for the InterIA LaTeX Galaxy Explorer CLI.

    Reads latex_galaxy.json, computes global documentation metrics,
    prints a cosmic summary, and writes latex_galaxy_summary.json
    for the HTML explorer.
    """
    data = load_galaxy()
    if not data:
        return 1

    files = data["files"]
    if not files:
        print("🌑 Galaxy empty: no LaTeX files.")
        return 0

    summary = _compute_galaxy_summary(files)

    Path("latex_galaxy_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    _print_galaxy_summary(summary)

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
