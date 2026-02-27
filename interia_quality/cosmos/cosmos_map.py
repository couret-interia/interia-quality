"""
cosmos_map.py — InterIA COSMOS MAP v1
-------------------------------------

Unifies all analysis layers into a single cosmic JSON:

- Python structure (functions, docstrings)
- Markdown structure (headings, tokens)
- LaTeX structure (sections, labels, macros, citations)
- BibTeX structure (bib entries, missing refs, co-citation graph)

Outputs:
- cosmos_map.json        (full dataset)
- cosmos_map_summary.json (global metrics)
"""

from __future__ import annotations

import json
from pathlib import Path

# Existing modules from your suite
from interia_quality.refactor import python_refactor, markdown_refactor
from interia_quality.doctor import latex_galaxy
from interia_quality.galaxy import bibtex_galaxy

def analyze_python(root: Path):
    """Returns Python-centric metrics."""
    items = python_refactor.scan_project(root)
    return {
        "issues": items,
        "count": len(items),
    }


def analyze_markdown(root: Path):
    """Returns Markdown-centric metrics."""
    items = markdown_refactor.scan_project(root)
    return {
        "issues": items,
        "count": len(items),
    }


def analyze_latex(root: Path):
    """Returns LaTeX galaxy metrics."""
    galaxy = latex_galaxy.analyze_project(root)
    return {
        "files": galaxy["files"],
        "aggregates": galaxy["aggregates"],
        "count_files": galaxy["aggregates"]["total_files"],
    }


def analyze_bibtex(root: Path):
    """Returns BibTeX galaxy metrics."""
    galaxy = bibtex_galaxy.analyze_project(root)
    return {
        "bib_entries": galaxy["bib_entries"],
        "unique_citations": galaxy["unique_citations"],
        "missing_refs": galaxy["cited_but_missing"],
        "unused_refs": galaxy["defined_but_not_cited"],
        "citation_density": galaxy["citation_density"],
        "completeness": galaxy["completeness_score"],
    }


def compute_cosmic_coherence(py, md, latex, bib):
    """Compute global coherence index."""
    # python: fewer issues = better → invert
    python_score = 1.0 if py["count"] == 0 else max(0.0, 1 - py["count"] / 50)

    markdown_score = 1.0 if md["count"] == 0 else max(0.0, 1 - md["count"] / 50)

    latex_files = latex["count_files"]
    latex_labels = latex["aggregates"]["total_labels"]
    latex_score = 0 if latex_files == 0 else min(1.0, latex_labels / (latex_files * 3))

    bib_score = bib["completeness"]

    return round(
        0.4 * python_score
      + 0.1 * markdown_score
      + 0.3 * latex_score
      + 0.2 * bib_score,
      3
    )


def main():
    """Main cosmos map function."""
    root = Path(".").resolve()

    py_data = analyze_python(root)
    md_data = analyze_markdown(root)
    latex_data = analyze_latex(root)
    bib_data = analyze_bibtex(root)

    cci = compute_cosmic_coherence(py_data, md_data, latex_data, bib_data)

    cosmos = {
        "root": str(root),
        "python": py_data,
        "markdown": md_data,
        "latex": latex_data,
        "bibtex": bib_data,
        "cosmic_coherence_index": cci,
    }

    Path("cosmos_map.json").write_text(
        json.dumps(cosmos, indent=2),
        encoding="utf-8",
    )

    # Summary
    summary = {
        "cosmic_coherence_index": cci,
        "python_issues": py_data["count"],
        "markdown_issues": md_data["count"],
        "latex_files": latex_data["count_files"],
        "latex_labels": latex_data["aggregates"]["total_labels"],
        "bibtex_completeness": bib_data["completeness"],
    }

    Path("cosmos_map_summary.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )

    print("\n🌌 COSMOS MAP generated:")
    print(" - cosmos_map.json")
    print(" - cosmos_map_summary.json")
    print(f"✨ Cosmic Coherence Index (CCI): {cci}")

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
