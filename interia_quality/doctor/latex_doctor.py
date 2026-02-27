"""
latex_doctor.py

InterIA Quality Pack v4 – LaTeX Doctor (Cosmic Edition)

Run diagnostic checks on all .tex files in a repository.

Checks performed:
- Forbidden tokens: TODO, FIXME, ???
- Very long lines (>120 chars)
- Sections without \label{...}
- Figures/environments without labels (\label{...})
- Equations without labels
- Excessive blank lines
- Unused macros (simple heuristic)
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import List, Dict, Any

FORBIDDEN_TOKENS = ["TODO", "FIXME", "???"]
MAX_LINE_LENGTH = 120
MAX_CONSEC_BLANK = 2

SECTION_CMDS = [
    r"\\section{",
    r"\\subsection{",
    r"\\subsubsection{"
]

ENVIRONMENTS_REQUIRING_LABEL = [
    r"\\begin{figure}",
    r"\\begin{table}",
    r"\\begin{equation}",
    r"\\begin{align}"
]

MACRO_DEF_PAT = re.compile(r"\\newcommand{\\(\w+)}")
MACRO_USE_PAT = r"\\{}"  # formatted via .format

def _scan_layout_issues(path: Path, lines: List[str]) -> List[Dict[str, Any]]:
    """Check forbidden tokens, long lines and blank lines."""
    suggestions: List[Dict[str, Any]] = []
    blank_streak = 0

    # 1) Forbidden tokens, long lines, blank lines
    for i, line in enumerate(lines, start=1):
        stripped = line.strip()

        # Forbidden tokens
        for token in FORBIDDEN_TOKENS:
            if token in line and not stripped.startswith("%"):
                suggestions.append({
                    "type": "forbidden_token",
                    "file": str(path),
                    "line": i,
                    "message": f"Found token '{token}'",
                    "advice": "Resolve or remove this token."
                })

        # Long lines (ignore pure comments)
        if len(line) > MAX_LINE_LENGTH and not stripped.startswith("%"):
            suggestions.append({
                "type": "long_line",
                "file": str(path),
                "line": i,
                "message": f"Line exceeds {MAX_LINE_LENGTH} characters.",
                "advice": "Wrap or split this line."
            })

        # Excessive blank lines
        if stripped == "":
            blank_streak += 1
            if blank_streak > MAX_CONSEC_BLANK:
                suggestions.append({
                    "type": "excessive_blank_lines",
                    "file": str(path),
                    "line": i,
                    "message": "More than 2 consecutive blank lines.",
                    "advice": "Reduce blank lines to improve readability."
                })
        else:
            blank_streak = 0

    return suggestions


def _scan_sections_without_labels(path: Path, lines: List[str]) -> List[Dict[str, Any]]:
    """Detect section commands that are missing nearby labels."""
    suggestions: List[Dict[str, Any]] = []

    # 2) Sections without labels (small heuristic)
    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        if any(stripped.startswith(cmd) for cmd in SECTION_CMDS):
            # search for label in line and next 5 lines
            has_label = False
            for j in range(i - 1, min(i + 5, len(lines))):
                if "\\label{" in lines[j]:
                    has_label = True
                    break
            if not has_label:
                suggestions.append({
                    "type": "section_without_label",
                    "file": str(path),
                    "line": i,
                    "message": "Section command without nearby \\label{}.",
                    "advice": "Add a label for cross-referencing."
                })

    return suggestions


def _scan_environments_without_labels(path: Path, lines: List[str]) -> List[Dict[str, Any]]:
    """Detect figures, tables and equations without labels."""
    suggestions: List[Dict[str, Any]] = []

    # 3) Figures / tables / equations without labels
    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        if any(stripped.startswith(env) for env in ENVIRONMENTS_REQUIRING_LABEL):
            # search for label inside environment
            found_label = False
            for j in range(i - 1, min(i + 8, len(lines))):
                if "\\label{" in lines[j]:
                    found_label = True
                    break
            if not found_label:
                suggestions.append({
                    "type": "environment_without_label",
                    "file": str(path),
                    "line": i,
                    "message": f"Environment at line {i} missing \\label{{}}.",
                    "advice": "Add a label inside this environment."
                })

    return suggestions


def _scan_unused_macros(path: Path, text: str) -> List[Dict[str, Any]]:
    """Detect macros that are defined but never used."""
    suggestions: List[Dict[str, Any]] = []

    # 4) Unused macros (very simple heuristic)
    macros = MACRO_DEF_PAT.findall(text)
    for macro in macros:
        pattern = MACRO_USE_PAT.format(macro)
        if not re.search(pattern, text):
            suggestions.append({
                "type": "unused_macro",
                "file": str(path),
                "line": None,
                "message": f"Macro \{macro} defined but not used.",
                "advice": "Remove unused macro if not needed."
            })

    return suggestions


def scan_tex_file(path: Path) -> List[Dict[str, Any]]:
    """Scan a single .tex file and return a list of issues."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()

    suggestions: List[Dict[str, Any]] = []
    suggestions.extend(_scan_layout_issues(path, lines))
    suggestions.extend(_scan_sections_without_labels(path, lines))
    suggestions.extend(_scan_environments_without_labels(path, lines))
    suggestions.extend(_scan_unused_macros(path, text))

    return suggestions


def scan_project(root: Path | None = None) -> List[Dict[str, Any]]:
    """
    Recursively scan all .tex files under root and return all issues found.
    """
    if root is None:
        root = Path(".")

    all_issues: List[Dict[str, Any]] = []

    for tex_file in root.rglob("*.tex"):
        all_issues.extend(scan_tex_file(tex_file))

    return all_issues
