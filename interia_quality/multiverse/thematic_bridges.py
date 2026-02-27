"""
thematic_bridges.py — InterIA Thematic & Code Bridges

Compute thematic resonance and code bridges between repositories:

- thematic overlap via BibTeX keywords + citation keys
- code overlap via Python imports
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any, Set, List
import re

IMPORT_PATTERN = re.compile(r"^(from\s+(\S+)\s+import|import\s+(\S+))", re.MULTILINE)

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


def jaccard(a: Set[str], b: Set[str]) -> float:
    """overlap of citation keys (BibTeX)"""
    if not a and not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union > 0 else 0.0


def extract_python_imports(repo_root: Path) -> Set[str]:
    """Naive scan of .py files to extract imported modules."""
    modules: Set[str] = set()
    for py in repo_root.rglob("*.py"):
        text = py.read_text(encoding="utf-8", errors="ignore")
        for match in IMPORT_PATTERN.finditer(text):
            # group(2) for 'from x import', group(3) for 'import x'
            mod = match.group(2) or match.group(3)
            if mod:
                modules.add(mod.split(".")[0])
    return modules


def _compute_repo_themes(cosmos):
    """Extract thematic information (citations, keywords, macros) for a repo."""
    bib = cosmos["bibtex"]
    latex = cosmos["latex"]

    citation_keys = set(bib.get("unique_citations", []))

    bib_entries = bib.get("bib_entries", {})
    keywords: Set[str] = set()
    for info in bib_entries.values():
        for kw in info.get("keywords", []):
            keywords.add(kw.lower())

    latex_macros: Set[str] = set()
    for fstats in latex["files"].values():
        latex_macros |= set(fstats.get("macro_details", {}).keys())

    return {
        "citation_keys": citation_keys,
        "keywords": keywords,
        "macros": latex_macros,
    }


def _build_bridge_edge(a, b, themes, code_imports):
    """Compute thematic and code-based bridge strength between two repos."""
    ta = themes[a]
    tb = themes[b]

    cite_overlap = jaccard(ta["citation_keys"], tb["citation_keys"])
    kw_overlap = jaccard(ta["keywords"], tb["keywords"])
    macro_overlap = jaccard(ta["macros"], tb["macros"])

    code_overlap = jaccard(code_imports[a], code_imports[b])

    if any([cite_overlap, kw_overlap, macro_overlap]):
        theme_overlap = (cite_overlap + kw_overlap + macro_overlap) / 3
    else:
        theme_overlap = 0.0

    bridge_strength = 0.6 * theme_overlap + 0.4 * code_overlap

    return {
        "a": a,
        "b": b,
        "theme_overlap": round(theme_overlap, 3),
        "code_overlap": round(code_overlap, 3),
        "bridge_strength": round(bridge_strength, 3),
    }


def thematic_and_code_bridges(multiverse_map: Dict[str, Any]) -> Dict[str, Any]:
    """Compute thematic & code bridges between all repos."""

    repos: Dict[str, str] = multiverse_map["repos"]
    cosmos_maps: Dict[str, Any] = multiverse_map["cosmos_maps"]

    repo_names = list(repos.keys())

    # Precompute per-repo sets
    themes: Dict[str, Dict[str, Set[str]]] = {}
    code_imports: Dict[str, Set[str]] = {}

    for name in repo_names:
        root = Path(repos[name])
        cosmos = cosmos_maps[name]

        themes[name] = _compute_repo_themes(cosmos)
        code_imports[name] = extract_python_imports(root)

    # Now compute bridges between repos
    edges: List[Dict[str, Any]] = []

    for i, a in enumerate(repo_names):
        for b in repo_names[i + 1 :]:
            edges.append(_build_bridge_edge(a, b, themes, code_imports))

    return {
        "repos": repos,
        "edges": edges,
    }


def main():
    """Main function of InterIA Thematic & Code Bridges"""
    multiverse_path = Path("interia_multiverse_map.json")
    if not multiverse_path.exists():
        print("❌ interia_multiverse_map.json missing. Run multiverse-map first.")
        return 1

    multiverse_map = load_json(multiverse_path)
    bridges = thematic_and_code_bridges(multiverse_map)

    Path("interia_multiverse_bridges.json").write_text(
        json.dumps(bridges, indent=2),
        encoding="utf-8"
    )

    print("✨ Thematic & code bridges saved to interia_multiverse_bridges.json")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
