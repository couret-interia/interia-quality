"""
multiverse_gravity.py — InterIA Documentary Gravity v1

Compute "documentary gravity" between repositories based on:

- existing structural distance (distance_matrix)
- overlap of citation keys (BibTeX)
- overlap of LaTeX macros
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any, List, Set

def load_json(path: Path) -> Any:
    """Load JSON file from path"""
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise FileNotFoundError(
            f"{path} JSON decoding failed: {e}."
        )


def jaccard_overlap(a: Set[str], b: Set[str]) -> float:
    """overlap of citation keys (BibTeX)"""
    if not a and not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union > 0 else 0.0


def _collect_macro_keys(cosmos_repo):
    """Collect all macro names used in the LaTeX files for a repository."""
    macros: Set[str] = set()
    for fstats in cosmos_repo["latex"]["files"].values():
        macros |= set(fstats.get("macro_details", {}).keys())
    return macros


def _build_gravity_edge(a, b, cosmos_maps, matrix):
    """Compute gravity information for a pair of repositories."""
    cA = cosmos_maps[a]
    cB = cosmos_maps[b]

    # Structural distance
    d = matrix[a][b]

    # Citations overlap
    citesA = set(cA["bibtex"].get("unique_citations", []))
    citesB = set(cB["bibtex"].get("unique_citations", []))
    cit_overlap = jaccard_overlap(citesA, citesB)

    # Macros overlap (collect macro keys across LaTeX files)
    macrosA = _collect_macro_keys(cA)
    macrosB = _collect_macro_keys(cB)
    macro_overlap = jaccard_overlap(macrosA, macrosB)

    base_attraction = 1 / (1 + d)
    gravity = base_attraction * (1 + cit_overlap + macro_overlap)

    return {
        "a": a,
        "b": b,
        "distance": d,
        "citation_overlap": round(cit_overlap, 3),
        "macro_overlap": round(macro_overlap, 3),
        "gravity": round(gravity, 3),
    }


def compute_gravity():
    """Compute "documentary gravity" between repositories"""
    multiverse_path = Path("interia_multiverse_map.json")
    matrix_path = Path("interia_multiverse_matrix.json")

    if not multiverse_path.exists() or not matrix_path.exists():
        print("❌ interia_multiverse_map.json or interia_multiverse_matrix.json missing.")
        print("   Run multiverse-map first.")
        return 1

    multiverse = load_json(multiverse_path)
    matrix = load_json(matrix_path)

    cosmos_maps: Dict[str, Dict[str, Any]] = multiverse["cosmos_maps"]
    repos = list(cosmos_maps.keys())

    edges: List[Dict[str, Any]] = []

    for i, a in enumerate(repos):
        for b in repos[i + 1 :]:
            edges.append(_build_gravity_edge(a, b, cosmos_maps, matrix))

    out = {
        "repos": repos,
        "edges": edges,
    }

    Path("interia_multiverse_gravity.json").write_text(
        json.dumps(out, indent=2),
        encoding="utf-8",
    )
    print("🌌 Documentary gravity map saved to interia_multiverse_gravity.json")
    return 0


def main():
    """Main function of InterIA Documentary Gravity"""
    return compute_gravity()

if __name__ == "__main__":
    import sys
    sys.exit(main())
