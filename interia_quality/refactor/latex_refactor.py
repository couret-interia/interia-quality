"""
latex_refactor.py

InterIA Quality Pack v4 – LaTeX Refactor Scanner

Analyse .tex files and suggests small refactors:

- forbidden tokens (TODO, FIXME)
- very long lines
- too many consecutive blank lines
- section commands without nearby labels (heuristic)

This module does NOT modify files. It only returns structured suggestions.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Dict, Any

FORBIDDEN_TOKENS = ["TODO", "FIXME"]
MAX_LINE_LENGTH = 120
MAX_CONSEC_BLANK = 2
SECTION_COMMANDS = ["\section{", "\subsection{", "\subsubsection{"]

def _scan_line_for_forbidden_and_spacing(path: Path, line: str, line_no: int, blank_streak: int):
    """Scan a single LaTeX line and update spacing-related suggestions."""
    suggestions: List[Dict[str, Any]] = []
    stripped = line.strip()

    # Forbidden tokens
    for token in FORBIDDEN_TOKENS:
        if token in line:
            suggestions.append({
                "type": "forbidden_token",
                "file": str(path),
                "line": line_no,
                "message": f"Found token '{token}' in LaTeX file.",
                "action": "remove_or_resolve",
                "snippet": str(line),
            })

    # Very long lines (ignore pure comments)
    if len(line) > MAX_LINE_LENGTH and not stripped.startswith("%"):
        suggestions.append({
            "type": "long_line",
            "file": str(path),
            "line": line_no,
            "message": (
                f"Line length {len(line)} exceeds {MAX_LINE_LENGTH} characters."
            ),
            "action": "wrap_or_split",
            "snippet": str(line),
        })

    # Excessive blank lines
    if stripped == "":
        blank_streak += 1
        if blank_streak > MAX_CONSEC_BLANK:
            suggestions.append({
                "type": "excessive_blank_lines",
                "file": str(path),
                "line": line_no,
                "message": (
                    f"More than {MAX_CONSEC_BLANK} consecutive blank lines."
                ),
                "action": "reduce_blank_lines",
                "snippet": str(line),
            })
    else:
        blank_streak = 0

    return suggestions, blank_streak


def _scan_forbidden_tokens_and_spacing(path: Path, lines: List[str]) -> List[Dict[str, Any]]:
    """Detect forbidden tokens, very long lines and excessive blank lines."""
    suggestions: List[Dict[str, Any]] = []
    blank_streak = 0

    # Première passe : tokens interdits, lignes longues, blancs excessifs
    for i, line in enumerate(lines, start=1):
        line_suggestions, blank_streak = _scan_line_for_forbidden_and_spacing(
            path, line, i, blank_streak
        )
        suggestions.extend(line_suggestions)

    return suggestions


def _scan_sections_without_label(path: Path, lines: List[str]) -> List[Dict[str, Any]]:
    """Detect section commands that are missing nearby labels."""
    suggestions: List[Dict[str, Any]] = []

    # Deuxième passe : sections sans label à proximité (heuristique simple)
    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        if any(stripped.startswith(cmd) for cmd in SECTION_COMMANDS):
            # Cherche un label dans la ligne et les 3 suivantes
            has_label = False
            for j in range(i - 1, min(i + 3, len(lines))):
                if "\\label{" in lines[j]:
                    has_label = True
                    break
            if not has_label:
                suggestions.append({
                    "type": "section_without_label",
                    "file": str(path),
                    "line": i,
                    "message": "Section command without nearby \\label{...}.",
                    "action": "add_label",
                    "snippet": str(line),
                })

    return suggestions


def scan_tex_file(path: Path) -> List[Dict[str, Any]]:
    """
    Analyse a single .tex file and return refactor suggestions.

    Each suggestion is a dict with at least:
    - type
    - file
    - line / lines
    - message
    - action
    """
    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()

    suggestions: List[Dict[str, Any]] = []
    suggestions.extend(_scan_forbidden_tokens_and_spacing(path, lines))
    suggestions.extend(_scan_sections_without_label(path, lines))

    return suggestions


def scan_project(root: Path | None = None) -> List[Dict[str, Any]]:
    """
    Recursively scan all .tex files under the given root
    and aggregate LaTeX refactor suggestions for the whole project.
    """
    if root is None:
        root = Path(".")

    all_suggestions: List[Dict[str, Any]] = []

    for tex_file in root.rglob("*.tex"):
        all_suggestions.extend(scan_tex_file(tex_file))

    return all_suggestions
