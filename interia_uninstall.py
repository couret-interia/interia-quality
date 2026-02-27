#!/usr/bin/env python3
"""
interia_uninstall.py

InterIA Quality Pack v4 – Uninstaller

Safely removes the InterIA Quality Pack from a target repository.

What it removes:
- The `interia_quality/` package
- Helper JSON files (`ai_request.json`, `quality_report.json`)
- InterIA Quality documentation files
- The Quality Pack v4 snippet in the target Makefile (between markers)

Usage:
    python interia_uninstall.py
    python interia_uninstall.py path/to/repo
    python interia_uninstall.py path/to/repo --yes
"""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
from interia_quality.version import NAME, CODENAME

QUALITY_NAME = NAME + " " + CODENAME
QUALITY_MARKER = "# >>> " + QUALITY_NAME

# ------------------------------------------------------------
# Files list
# ------------------------------------------------------------
FILES_TO_REMOVE = [
    "interia_menu.py",
    "interia_doctor.py",
    "quality_report.json",
    "interia_multiverse_3d.json",
    "interia_multiverse_map.json",
    "interia_multiverse_summary.json",
    "interia_multiverse_matrix.json",
    "interia_multiverse_gravity.json",
    "interia_multiverse_bridges.json",
    "cosmos_map.json",
    "cosmos_map_summary.json",
    "bib_galaxy.json",
    "bib_galaxy_summary.json",
    "latex_galaxy.json",
    "latex_galaxy_summary.json",
    "refactor_plan.md",
    "refactor_plan.json",
    "README_interia_quality.md",
    "README_interia_quality_quickstart.md",
    "AI_TOUR.md",
    "AI_BRIDGE.md",
    "ai_prompt.txt",
    "ai_request.json",
    "ai_response.json",
]

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def remove_tree(path: Path) -> None:
    """Remove a directory tree if it exists."""
    if path.exists() and path.is_dir():
        print(f"🧹 Removing directory: {path}")
        shutil.rmtree(path)
    else:
        print(f"ℹ️  Directory not found (skip): {path}")


def remove_file(path: Path) -> None:
    """Remove a file if it exists."""
    if path.exists() and path.is_file():
        print(f"🧺 Removing file: {path}")
        path.unlink()
    else:
        print(f"ℹ️  File not found (skip): {path}")


def patch_makefile_remove_snippet(makefile: Path) -> None:
    """Remove the InterIA Quality snippet from the Makefile, if present."""
    if not makefile.exists():
        print(f"ℹ️  No Makefile found at {makefile}, nothing to patch.")
        return

    text = makefile.read_text(encoding="utf-8")
    marker = QUALITY_MARKER

    first = text.find(marker)
    if first == -1:
        print("ℹ️  Makefile does not contain the InterIA Quality snippet, skipping patch.")
        return

    second = text.find(marker, first + len(marker))
    if second == -1:
        print("⚠️  Only one QUALITY_MARKER found — snippet removal may be incomplete. "
              "Skipping for safety.")
        return

    # Remove text between the two markers (inclusive)
    before = text[:first]
    after = text[second + len(marker):]

    new_text = before.rstrip() + "\n\n" + after.lstrip()
    makefile.write_text(new_text, encoding="utf-8")

    print(f"🧷 Makefile patched: removed InterIA Quality snippet → {makefile}")

# ------------------------------------------------------------
# Core logic
# ------------------------------------------------------------

def uninstall(target_root: Path, args) -> int:
    """Show affected items and uninstall them if user confirms."""
    print(f"🧭 InterIA uninstall — target: {target_root}")

    # Directories
    items_to_remove = [
        target_root / "interia_quality",
        target_root / "cosmos_history",
    ]

    # Files
    for name in FILES_TO_REMOVE:
      items_to_remove.append(target_root / name)

    print("\nThe following items will be removed:")
    for p in items_to_remove:
        print(f" - {p}")

    makefile = target_root / "Makefile"
    print(f" - Makefile patch (remove {QUALITY_NAME} snippet): {makefile}")

    # Confirmation
    if not args.yes:
        ans = input("\nProceed with uninstall? [y/N] ").strip().lower()
        if ans not in ("y", "yes"):
            print("❎ Uninstall cancelled.")
            return 0

    # Remove items
    remove_tree(items_to_remove[0])
    remove_tree(items_to_remove[1])
    for p in items_to_remove[2:]:
        remove_file(p)

    # Patch Makefile
    patch_makefile_remove_snippet(makefile)

    print(f"\n✅ {QUALITY_NAME} successfully uninstalled from {target_root}.")
    return 0

# ------------------------------------------------------------
# Entry point
# ------------------------------------------------------------

def main() -> int:
    """Uninstall InterIA Quality Pack v4 from a target repository."""
    parser = argparse.ArgumentParser(
        description="Uninstall " + QUALITY_NAME + " from a target repository."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Target repository root (default: current directory).",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Do not ask for confirmation.",
    )
    args = parser.parse_args()

    target_root = Path(args.target).resolve()
    if not target_root.exists():
        print(f"❌ Target path does not exist: {target_root}")
        return 1

    return uninstall(target_root, args)

if __name__ == "__main__":
    raise SystemExit(main())
