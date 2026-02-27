"""
multiverse_map.py — InterIA Multiverse Topology v1

Given several repositories, build a multiverse-level analysis:

- Load each repo's cosmos_map.json
- Compute pairwise "cosmic distance"
- Identify clusters of similarity
- Produce:
    interia_multiverse_map.json
    interia_multiverse_matrix.json
    interia_multiverse_summary.json
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Any
import math

def load_cosmos(path: Path) -> Dict[str, Any]:
    """Load cosmos_map.json from path"""
    cosmos_file = path / "cosmos_map.json"
    if not cosmos_file.exists():
        return None
    try:
        return json.loads(cosmos_file.read_text(encoding="utf-8"))
    except:
        return None


def cosmic_distance(c1: Dict[str, Any], c2: Dict[str, Any]) -> float:
    """
    Compute a symmetric distance between two cosmos maps.
    Lower = more similar.
    """

    # Python layer
    py1, py2 = len(c1["python"]["issues"]), len(c2["python"]["issues"])
    d_py = abs(py1 - py2)

    # Markdown
    md1, md2 = len(c1["markdown"]["issues"]), len(c2["markdown"]["issues"])
    d_md = abs(md1 - md2)

    # LaTeX
    l1 = c1["latex"]["aggregates"]["total_labels"]
    l2 = c2["latex"]["aggregates"]["total_labels"]
    d_latex = abs(l1 - l2)

    # BibTeX completeness
    b1 = c1["bibtex"]["completeness"]
    b2 = c2["bibtex"]["completeness"]
    d_bib = abs(b1 - b2)

    # Cosmic Coherence Index
    cci1 = c1["cosmic_coherence_index"]
    cci2 = c2["cosmic_coherence_index"]
    d_cci = abs(cci1 - cci2)

    # Weighted sum → distance
    return round(
        0.3 * d_py +
        0.2 * d_md +
        0.3 * d_latex +
        0.1 * d_bib +
        0.1 * d_cci,
        3
    )


def build_multiverse(repo_paths: List[str]) -> Dict[str, Any]:
    """Load all cosmos, Pairwise distances, Build a “star score” for each repo."""
    repos = {}
    cosmos_maps = {}

    # Load all cosmos
    for p in repo_paths:
        root = Path(p).resolve()
        name = root.name
        cosmos = load_cosmos(root)
        if cosmos:
            repos[name] = str(root)
            cosmos_maps[name] = cosmos

    # Pairwise distances
    names = list(cosmos_maps.keys())
    matrix = {a: {} for a in names}

    for i, a in enumerate(names):
        for b in names[i:]:
            if a == b:
                matrix[a][b] = 0.0
            else:
                d = cosmic_distance(cosmos_maps[a], cosmos_maps[b])
                matrix[a][b] = d
                matrix[b][a] = d

    # Build a “star score” for each repo (sum of inverse distances)
    star_score = {}
    for a in names:
        inv_sum = 0
        for b in names:
            d = matrix[a][b]
            inv_sum += 1 / (1 + d)
        star_score[a] = round(inv_sum, 3)

    return {
        "repos": repos,
        "cosmos_maps": cosmos_maps,
        "distance_matrix": matrix,
        "star_score": star_score,
    }


def main():
    """Main InterIA Multiverse Map Generator"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m interia_quality.multiverse.multiverse_map repo1 repo2 [...]")
        return 1

    repo_paths = sys.argv[1:]
    multiverse = build_multiverse(repo_paths)

    Path("interia_multiverse_map.json").write_text(
        json.dumps(multiverse, indent=2), encoding="utf-8"
    )

    Path("interia_multiverse_matrix.json").write_text(
        json.dumps(multiverse["distance_matrix"], indent=2), encoding="utf-8"
    )

    summary = {
        "repos": list(multiverse["repos"]),
        "star_score": multiverse["star_score"],
    }

    Path("interia_multiverse_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    print("🌌 Multiverse map generated:")
    print(" - interia_multiverse_map.json")
    print(" - interia_multiverse_matrix.json")
    print(" - interia_multiverse_summary.json")

    print("\n✨ Star Scores:")
    for name, s in multiverse["star_score"].items():
        print(f" - {name}: {s}")

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
