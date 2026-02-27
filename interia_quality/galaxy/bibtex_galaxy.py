"""
bibtex_galaxy.py — InterIA BibTeX Galaxy Map (Transcendental Edition)

Builds a galaxy map of bibliographic references across a LaTeX project:

- Parse .bib files → extract entries, authors, years, keywords
- Parse .tex files → extract \\cite{...}
- Detect:
  - cited references
  - non-cited references
  - citations to missing bib entries (ghost references)
- Build co-citation matrix (how often two refs are cited together)
- Compute cosmic metrics:
  - citation density
  - co-citation clusters
  - BibTeX completeness score
"""

from __future__ import annotations

import json
from pathlib import Path
import re
from itertools import combinations
from typing import Dict, List, Any

CITE_PATTERN = re.compile(r"\\cite\{([^}]*)\}")
BIB_ENTRY_PATTERN = re.compile(r"@(\w+)\{([^,]+)," )
AUTHOR_PATTERN = re.compile(r"author\s*=\s*\{([^}]*)\}", re.IGNORECASE)
YEAR_PATTERN = re.compile(r"year\s*=\s*\{([^}]*)\}", re.IGNORECASE)
KEYWORD_PATTERN = re.compile(r"keywords?\s*=\s*\{([^}]*)\}", re.IGNORECASE)

def parse_bib_file(path: Path) -> Dict[str, Dict[str, Any]]:
    """Return a dict: key → metadata extracted from a .bib file."""
    content = path.read_text(encoding="utf-8", errors="ignore")
    entries = {}

    for match in BIB_ENTRY_PATTERN.finditer(content):
        entry_type = match.group(1)
        key = match.group(2)
        entries[key] = {
            "type": entry_type,
            "authors": [],
            "year": None,
            "keywords": [],
        }

    # Now find authors, year, keywords
    for key in entries:
        # crude slicing: find block starting at '@...{key,' until next '}'
        start = content.find(key + ",")
        if start == -1:
            continue
        end = content.find("}", start)
        block = content[start:end]

        auth_m = AUTHOR_PATTERN.search(block)
        if auth_m:
            authors = [a.strip() for a in auth_m.group(1).split(" and ")]
            entries[key]["authors"] = authors

        year_m = YEAR_PATTERN.search(block)
        if year_m:
            entries[key]["year"] = year_m.group(1).strip()

        kw_m = KEYWORD_PATTERN.search(block)
        if kw_m:
            kws = [k.strip() for k in kw_m.group(1).split(",")]
            entries[key]["keywords"] = kws

    return entries


def extract_citations_from_tex(path: Path) -> List[str]:
    """Extract all citation keys from a .tex file."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    keys = []
    for match in CITE_PATTERN.findall(text):
        # multiple keys inside \cite{a,b,c}
        keys.extend(k.strip() for k in match.split(",") if k.strip())
    return keys


def _collect_bib_entries(root: Path) -> Dict[str, Dict[str, Any]]:
    """Collect all BibTeX entries under the given project root."""
    bib_entries: Dict[str, Dict[str, Any]] = {}
    for bib_file in root.rglob("*.bib"):
        bib_entries.update(parse_bib_file(bib_file))
    return bib_entries


def _collect_citations_per_file(root: Path) -> Dict[str, List[str]]:
    """Collect all citation keys used in .tex files under the given root."""
    citations_per_file: Dict[str, List[str]] = {}
    for tex_file in root.rglob("*.tex"):
        rel = str(tex_file.relative_to(root))
        citations_per_file[rel] = extract_citations_from_tex(tex_file)
    return citations_per_file


def analyze_project(root: Path | None = None) -> Dict[str, Any]:
    """Build BibTeX galaxy metrics for a project tree.

    Aggregates BibTeX entries, citation usage, and co-citation statistics.
    """
    if root is None:
        root = Path(".")

    bib_entries = _collect_bib_entries(root)
    citations_per_file = _collect_citations_per_file(root)

    # Flatten list of all citations
    all_citations = [c for lst in citations_per_file.values() for c in lst]

    unique_citations = set(all_citations)
    defined_keys = set(bib_entries.keys())

    cited_and_defined = unique_citations & defined_keys
    cited_but_missing = unique_citations - defined_keys
    defined_but_not_cited = defined_keys - unique_citations

    # 3. Co-citation matrix
    cocite: Dict[str, Dict[str, int]] = {}
    for file, keys in citations_per_file.items():
        for a, b in combinations(sorted(set(keys)), 2):
            cocite.setdefault(a, {}).setdefault(b, 0)
            cocite[a][b] += 1
            # symmetry
            cocite.setdefault(b, {}).setdefault(a, 0)
            cocite[b][a] += 1

    # Simple cosmic metrics
    citation_density = len(all_citations) / max(1, len(citations_per_file))
    completeness = len(cited_and_defined) / max(1, len(unique_citations))

    result = {
        "bib_entries": bib_entries,
        "citations_per_file": citations_per_file,
        "unique_citations": sorted(unique_citations),
        "cited_and_defined": sorted(cited_and_defined),
        "cited_but_missing": sorted(cited_but_missing),
        "defined_but_not_cited": sorted(defined_but_not_cited),
        "citation_density": round(citation_density, 3),
        "completeness_score": round(completeness, 3),
        "co_citation": cocite,
    }

    return result


def save_galaxy(galaxy: Dict[str, Any], path="bib_galaxy.json") -> None:
    """Save bib_galaxy.json for BibTeX galaxy."""
    Path(path).write_text(json.dumps(galaxy, indent=2), encoding="utf-8")


def main():
    """Main function BibTeX galaxy builder."""
    root = Path(".").resolve()
    galaxy = analyze_project(root)
    save_galaxy(galaxy)
    print("💫 BibTeX galaxy saved to bib_galaxy.json")

    print("\n📊 Summary:")
    print(f" - Citation density:   {galaxy['citation_density']}")
    print(f" - Completeness score: {galaxy['completeness_score']}")
    print(f" - Total bib entries:  {len(galaxy['bib_entries'])}")
    print(f" - Total cited keys:   {len(galaxy['unique_citations'])}")
    print(f" - Missing references: {len(galaxy['cited_but_missing'])}")

    if galaxy["cited_but_missing"]:
        print("⚠️  Missing keys:", ", ".join(galaxy["cited_but_missing"]))

    if galaxy["defined_but_not_cited"]:
        print("ℹ️  Unused entries:", ", ".join(galaxy["defined_but_not_cited"][:10]),
              "..." if len(galaxy["defined_but_not_cited"]) > 10 else "")

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
