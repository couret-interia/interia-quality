"""
Markdown refactor scanner for InterIA Quality v4.

Detects:
- forbidden tokens like TODO or WIP
- headings that are very long
"""

from pathlib import Path

FORBIDDEN_TOKENS = ["TODO:", "WIP", "???"]
MAX_HEADING_LENGTH = 80

def scan_md_file(path: Path):
    """
    Analyse a Markdown file and extract refactor suggestions:

    - forbidden tokens (TODO:, WIP, ???)
    - excessively long headings

    Returns a list of suggestion dictionaries.
    """
    text = path.read_text(encoding="utf-8", errors="ignore")
    suggestions = []
    lines = text.splitlines()

    for i, line in enumerate(lines, start=1):
        # Forbidden tokens
        for token in FORBIDDEN_TOKENS:
            if token in line:
                suggestions.append({
                    "type": "forbidden_token",
                    "file": str(path),
                    "line": i,
                    "message": f"Found token '{token}'",
                    "action": "remove_or_resolve",
                    "snippet": str(line),
                })

        # Long headings
        if line.startswith("#") and len(line) > MAX_HEADING_LENGTH:
            suggestions.append({
                "type": "long_heading",
                "file": str(path),
                "line": i,
                "message": (
                    f"Heading longer than {MAX_HEADING_LENGTH} characters."
                ),
                "action": "shorten_heading",
                "snippet": str(line),
            })

    return suggestions


def scan_project(root: Path | None = None):
    """
    Recursively scan all Markdown files under the given root
    and aggregate refactor suggestions for the entire project.
    """
    if root is None:
        root = Path(".")

    all_suggestions: list[dict] = []
    for md_file in root.rglob("*.md"):
        all_suggestions.extend(scan_md_file(md_file))

    return all_suggestions
