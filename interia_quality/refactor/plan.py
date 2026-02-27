"""
Build a refactor plan for Python and Markdown files.

Creates a refactor_plan.json file with a structured summary.
"""

import json
from pathlib import Path

from . import python_refactor, markdown_refactor, latex_refactor

def build_plan(root: Path | None = None):
    """
    Build a combined refactor plan for the project (Python + Markdown + LaTeX)
    and write it to refactor_plan.json.
    """
    if root is None:
        root = Path(".")

    plan = {
        "python": python_refactor.scan_project(root),
        "markdown": markdown_refactor.scan_project(root),
        "latex": latex_refactor.scan_project(root),
    }

    Path("refactor_plan.json").write_text(
        json.dumps(plan, indent=2),
        encoding="utf-8",
    )
    return plan


def write_human_readable_md(plan: dict):
    """
    Write a human-friendly summary of the refactor plan to refactor_plan.md.

    This file acts as a “mirror” of places where the project can improve.
    """
    Path("refactor_plan.md").write_text(
        """# 🌌 InterIA — Refactor Plan

<details><summary><b>🇫🇷 Français</b> — cliquer pour déployer</summary>

> *“Ce fichier est un miroir des endroits où le projet peut devenir plus clair,
> plus lisible, plus généreux pour le prochain contributeur.”*

Ce document accompagne `refactor_plan.json`, qui liste les propositions de refactorisation
générées par InterIA Quality Pack v4.

</details>

<details open><summary><b>🇬🇧 English</b> — click to collapse</summary>

> *“This file is a mirror of the places where the project can become clearer,
> more readable, and more generous for the next contributor.”*

This document accompanies `refactor_plan.json`, which collects the improvement
suggestions produced by InterIA Quality Pack v4.

</details>

## Résumé des suggestions / Summary of suggestions

- Python : {} items
- Markdown : {} items
- LaTeX : {} items

💡 Pour les détails consultez / For details consult [`refactor_plan.json`](refactor_plan.json).
""".format(
            len(plan["python"]),
            len(plan["markdown"]),
            len(plan["latex"])
        ),
        encoding="utf-8"
    )


def main():
    """CLI entry to build the refactor plan and the human-readable summary."""
    plan = build_plan()
    write_human_readable_md(plan)
    print("📜 Refactor plan written to refactor_plan.json and refactor_plan.md")
    print(f"Total suggestions: {sum(len(v) for v in plan.values())}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
