"""
latex_galaxy.py

InterIA Quality Pack v4 – LaTeX Galaxy Map

Build a "galaxy map" of LaTeX structure across a repository:

- Sections & subsections
- Labels
- Macro definitions & usage
- Citation keys and counts
- Simple density indicators (labels per section, macro usage ratio, citation density)

Outputs:
- latex_galaxy.json  (structured data)
- ASCII-style heatmap in the console
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any, List
import re

SECTION_LEVELS = {
    "\\section{": "section",
    "\\subsection{": "subsection",
    "\\subsubsection{": "subsubsection",
}

LABEL_PATTERN = re.compile(r"\\label{")
MACRO_DEF_PATTERN = re.compile(r"\\newcommand{\\(\w+)}")
MACRO_USE_TEMPLATE = r"\\{}"
CITE_PATTERN = re.compile(r"\\cite\{([^}]*)\}")

def _count_structure_and_labels(text: str):
    """Return (sections, subsections, subsubsections, labels) for the LaTeX text."""
    sections = 0
    subsections = 0
    subsubsections = 0
    labels = len(LABEL_PATTERN.findall(text))

    for token, level in SECTION_LEVELS.items():
        count = text.count(token)
        if level == "section":
            sections += count
        elif level == "subsection":
            subsections += count
        elif level == "subsubsection":
            subsubsections += count

    return sections, subsections, subsubsections, labels


def _analyze_macros(text: str):
    """Return (macros_defined, macros_used_total, macro_details) for the text."""
    macros = MACRO_DEF_PATTERN.findall(text)
    macro_details: Dict[str, int] = {}
    macros_used_total = 0

    for macro in macros:
        pattern = MACRO_USE_TEMPLATE.format(macro)
        occurrences = len(re.findall(pattern, text)) - 1  # subtract definition itself
        if occurrences < 0:
            occurrences = 0
        macro_details[macro] = occurrences
        macros_used_total += occurrences

    macros_defined = len(macros)
    return macros_defined, macros_used_total, macro_details


def _collect_citation_statistics(text: str):
    """Return (citations_total, citations_unique, citation_keys) for the text."""
    citation_keys: List[str] = []
    for match in CITE_PATTERN.findall(text):
        # \cite{key1,key2} => split on comma
        keys = [k.strip() for k in match.split(",") if k.strip()]
        citation_keys.extend(keys)

    citations_total = len(citation_keys)
    citations_unique = len(set(citation_keys))
    return citations_total, citations_unique, citation_keys


def analyze_tex_file(path: Path) -> Dict[str, Any]:
    """
    Analyse a single LaTeX file and compute galaxy statistics.

    Returns a dict with keys:
    - sections, subsections, subsubsections
    - labels
    - macros_defined, macros_used_total, macro_details
    - citations_total, citations_unique, citation_keys
    - label_density, macro_usage_ratio, citation_density
    - score: rough combined indicator
    """
    text = path.read_text(encoding="utf-8", errors="ignore")

    sections, subsections, subsubsections, labels = _count_structure_and_labels(text)
    macros_defined, macros_used_total, macro_details = _analyze_macros(text)
    citations_total, citations_unique, citation_keys = _collect_citation_statistics(text)

    total_struct = sections + subsections + subsubsections
    label_density = labels / total_struct if total_struct > 0 else 0.0
    macro_usage_ratio = (
        (macros_used_total / macros_defined) if macros_defined > 0 else 0.0
    )
    citation_density = (
        (citations_total / total_struct) if total_struct > 0 else 0.0
    )

    score = label_density + 0.3 * macro_usage_ratio + 0.2 * citation_density

    return {
        "sections": sections,
        "subsections": subsections,
        "subsubsections": subsubsections,
        "labels": labels,
        "macros_defined": macros_defined,
        "macros_used_total": macros_used_total,
        "macro_details": macro_details,
        "citations_total": citations_total,
        "citations_unique": citations_unique,
        "citation_keys": sorted(set(citation_keys)),
        "label_density": round(label_density, 3),
        "macro_usage_ratio": round(macro_usage_ratio, 3),
        "citation_density": round(citation_density, 3),
        "score": round(score, 3),
    }


def analyze_project(root: Path | None = None) -> Dict[str, Any]:
    """
    Build the galaxy map for all .tex files under root
    and return a dict mapping file -> stats and global aggregates.
    """
    if root is None:
        root = Path(".")

    files_stats: Dict[str, Any] = {}
    for tex_file in root.rglob("*.tex"):
        rel = tex_file.relative_to(root)
        files_stats[str(rel)] = analyze_tex_file(tex_file)

    agg = {
        "total_files": len(files_stats),
        "total_sections": sum(d["sections"] for d in files_stats.values()),
        "total_subsections": sum(d["subsections"] for d in files_stats.values()),
        "total_subsubsections": sum(d["subsubsections"] for d in files_stats.values()),
        "total_labels": sum(d["labels"] for d in files_stats.values()),
        "total_macros_defined": sum(d["macros_defined"] for d in files_stats.values()),
        "total_macros_used": sum(d["macros_used_total"] for d in files_stats.values()),
        "total_citations": sum(d["citations_total"] for d in files_stats.values()),
        "total_citations_unique": len(
            set(k for d in files_stats.values() for k in d["citation_keys"])
        ),
    }

    galaxy = {
        "root": str(root),
        "files": files_stats,
        "aggregates": agg,
    }
    return galaxy


def save_galaxy(galaxy: Dict[str, Any], path: Path = Path("latex_galaxy.json")) -> None:
    """Save the galaxy map to a JSON file."""
    path.write_text(json.dumps(galaxy, indent=2), encoding="utf-8")


def print_heatmap(galaxy: Dict[str, Any]) -> None:
    """
    Print a small ASCII heatmap-like summary of LaTeX files:

    - each file gets a bar scaled by score
    - label_density, macro_usage_ratio, citation_density printed next to it
    """
    files = galaxy.get("files", {})
    if not files:
        print("ℹ️  No .tex files found – galaxy is empty.")
        return

    print("🌌 LaTeX Galaxy Map\n")
    max_score = max(d["score"] for d in files.values()) or 1.0

    for fname, stats in sorted(files.items(), key=lambda kv: kv[1]["score"], reverse=True):
        score = stats["score"]
        density = stats["label_density"]
        macro_ratio = stats["macro_usage_ratio"]
        cite_density = stats["citation_density"]

        bar_len = int((score / max_score) * 30)
        if bar_len < 1:
            bar_len = 1

        bar = "█" * bar_len
        print(
            f"{fname:40} | {bar}  "
            f"(score={score:.3f}, labels/struct={density:.3f}, "
            f"macros={macro_ratio:.3f}, cites={cite_density:.3f})"
        )


def main() -> int:
    """Main function : Build a "galaxy map" of LaTeX structure across a repository:

    - Sections & subsections
    - Labels
    - Macro definitions & usage
    - Citation keys and counts
    - Simple density indicators (labels per section, macro usage ratio, citation density)

    Outputs:
    - latex_galaxy.json  (structured data)
    - ASCII-style heatmap in the console
    """

    root = Path(".").resolve()
    galaxy = analyze_project(root)
    save_galaxy(galaxy)
    print_heatmap(galaxy)
    print("\n🧾 Galaxy data saved to latex_galaxy.json")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
