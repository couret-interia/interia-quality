"""
multiverse_3d.py — InterIA Multiverse 3D Generator

Converts the multiverse distance matrix + gravity map
into a 3D-ready JSON structure.
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, Tuple

def load_json(path: Path) -> Any:
    """Load JSON file from path, return None if missing."""
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise FileNotFoundError(
            f"{path} JSON decoding failed: {e}."
        )


def build_gravity_lookup(gravity_json: Dict[str, Any]) -> Dict[Tuple[str, str], float]:
    """Convert interia_multiverse_gravity.json into a {(a,b): gravity} dict."""
    lookup = {}
    if not gravity_json:
        return lookup
    for edge in gravity_json.get("edges", []):
        a = edge["a"]
        b = edge["b"]
        g = edge.get("gravity", 1.0)
        lookup[(a, b)] = g
        lookup[(b, a)] = g
    return lookup


def _load_repo_cci(name, multimap):
    """Load the optional cosmic coherence index (CCI) for a repository."""
    if not multimap or "repos" not in multimap or name not in multimap["repos"]:
        return None

    repo_root = Path(multimap["repos"][name])
    cosmos_path = repo_root / "cosmos_map.json"
    cosmos = load_json(cosmos_path)
    if cosmos is None:
        return None
    return cosmos.get("cosmic_coherence_index")


def _build_links_for_repo(name, repos, matrix, gravity_lookup):
    """Build link entries from one repository to all others."""
    links = []
    for other in repos:
        if other == name:
            continue

        link = {
            "target": other,
            "distance": matrix[name][other],
        }

        # Inject gravity if available
        g = gravity_lookup.get((name, other))
        if g is not None:
            link["gravity"] = g

        links.append(link)
    return links


def main() -> int:
    """Main function — InterIA Multiverse 3D Generator."""
    map_path     = Path("interia_multiverse_map.json")
    matrix_path  = Path("interia_multiverse_matrix.json")
    summary_path = Path("interia_multiverse_summary.json")
    gravity_path = Path("interia_multiverse_gravity.json")

    if not matrix_path.exists() or not summary_path.exists():
        print("❌ interia_multiverse_matrix.json or interia_multiverse_summary.json missing.")
        print("   Run `multiverse-map` first.")
        return 1

    multimap = load_json(map_path)
    matrix   = load_json(matrix_path)
    summary  = load_json(summary_path)
    gravity  = load_json(gravity_path)

    gravity_lookup = build_gravity_lookup(gravity) if gravity else {}

    nodes = []
    repos = list(matrix.keys())

    for name in repos:
        cci = _load_repo_cci(name, multimap)
        links = _build_links_for_repo(name, repos, matrix, gravity_lookup)

        entry = {
            "name": name,
            "score": summary["star_score"].get(name, 1.0),
            "cci": cci,
            "links": links,
        }
        nodes.append(entry)

    out = {"nodes": nodes}
    Path("interia_multiverse_3d.json").write_text(
        json.dumps(out, indent=2),
        encoding="utf-8",
    )
    print("🌠 interia_multiverse_3d.json generated.")

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
