"""
interia_menu.py

InterIA Quality Pack v4 – Interactive menu helper

Small interactive menu to run common quality/refactor/AI tasks
via `make` in the current repository.

Usage:
    cd my_repo
    python /path/to/interia_quality_pack_v4/interia_menu.py
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from interia_quality.version import NAME, CODENAME

QUALITY_NAME = NAME + " " + CODENAME

TARGETS = [
    ("Quality + Refactor Plan",        "quality-all"),
    ("Quality only",                   "quality"),
    ("Build refactor plan",            "refactor-plan"),
    ("Apply refactor (safe)",          "refactor-apply"),
    ("Build AI request",               "ai-request"),
    ("Build AI prompt + open",         "ai-prompt"),
    ("Preview AI edits (HTML)",        "ai-preview"),
    ("Apply AI edits",                 "ai-apply"),
    ("LaTeX Galaxy (HTML)",            "latex-galaxy-html"),
    ("BibTeX Galaxy (HTML)",           "bib-galaxy-html"),
    ("Cosmos Map (HTML)",              "cosmos-map"),
    ("Cosmos Timeline (HTML)",         "cosmos-timeline-html"),
    ("Multiverse 3D (HTML)",           "multiverse-3d-html"),
    ("Multiverse Bridges",             "multiverse-thematic-bridges"),
    ("Stop local server",              "ai-stop"),
]


def run_make(target: str) -> None:
    """Try to run command with make."""
    print(f"\n▶ Running: make {target}\n")
    try:
        subprocess.run(["make", target], check=False)
    except FileNotFoundError:
        print("❌ 'make' command not found. Please install make on your system.")


def menu_loop() -> None:
    """Show menu options."""
    print("🌌 " + QUALITY_NAME + " – Interactive Menu Helper")
    print(f"📂 Current repo: {Path('.').resolve()}")

    while True:
        print("\n❓ Choose an action:")
        for i, (label, target) in enumerate(TARGETS, start=1):
            print(f"  {i}. {label}  [make {target}]")
        print("  0. Quit")

        choice = input("\nYour choice: ").strip()
        if not choice.isdigit():
            print("⚠️  Please enter a number.\n")
            continue

        n = int(choice)
        if n == 0:
            print("👋 Bye.")
            break

        if 1 <= n <= len(TARGETS):
            label, target = TARGETS[n - 1]
            run_make(target)
        else:
            print("⚠️  Invalid choice.\n")


def main() -> int:
    """Main function."""
    menu_loop()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
