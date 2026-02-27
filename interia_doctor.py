#!/usr/bin/env python3
"""
interia_doctor.py

InterIA Quality Pack v4 – Doctor

Run a series of simple diagnostics on a target repository
to check whether the InterIA Quality Pack is properly installed
and how far the workflow has been used (reports, plans, AI files).

Usage:
    python interia_doctor.py           # diagnose current directory
    python interia_doctor.py path/to/repo
"""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path
from typing import List, Tuple
from interia_quality.version import NAME, CODENAME

QUALITY_NAME = NAME + " " + CODENAME

def check_python_version() -> Tuple[bool, str]:
    """Check minimal version to use Quality Pack"""
    v = sys.version_info
    ok = (v.major, v.minor) >= (3, 8)
    msg = f"Python {v.major}.{v.minor}.{v.micro}"
    if not ok:
        msg += " (❌ Python 3.8+ recommended)"
    return ok, msg


def check_package_import(target_root: Path) -> Tuple[bool, str]:
    """Try to import interia_quality with PYTHONPATH pointed to target_root."""
    sys.path.insert(0, str(target_root))
    try:
        importlib.import_module("interia_quality")
    except Exception as e:
        return False, f"Cannot import 'interia_quality': {e!r}"
    finally:
        # on laisse sys.path modifié, ce n'est pas dramatique pour un script unique
        pass
    return True, "Package 'interia_quality' importable."


def check_version_module(target_root: Path) -> Tuple[bool, str]:
    """Return if module interia_quality.version exist"""
    sys.path.insert(0, str(target_root))
    try:
        version_mod = importlib.import_module("interia_quality.version")
        version_str = getattr(version_mod, "as_string", lambda: "unknown version")()
        return True, f"Version module OK: {version_str}"
    except Exception as e:
        return False, f"Cannot import 'interia_quality.version': {e!r}"


def check_file_exists(root: Path, rel: str) -> Tuple[bool, str]:
    """Verify if file exists on path"""
    path = root / rel
    if path.exists():
        return True, f"Found: {rel}"
    return False, f"Missing: {rel}"


def latex_galaxy_map(root: Path):
    """Launch InterIA Doctor LaTeX galaxy map."""
    from interia_quality.doctor import latex_galaxy

    galaxy = latex_galaxy.analyze_project(root)
    files = galaxy.get("files", {})
    if files:
        print("\n🌌 LaTeX Galaxy (summary):")
        latex_galaxy.print_heatmap(galaxy)
        print("   (full data in latex_galaxy.json if you run `make latex-galaxy`)")
    else:
        print("\n🌌 LaTeX Galaxy: no .tex files detected.")


def latex_refactor_quality(root: Path):
    """Launch InterIA Quality LaTeX Refactor."""
    from interia_quality.refactor import latex_refactor

    latex_issues = latex_refactor.scan_project(root)
    if latex_issues:
        print("\n🪐 LaTeX Doctor:")
        print(f"⚠️  {len(latex_issues)} issue(s) detected in LaTeX files:")
        for issue in latex_issues[:10]:  # prevent flood
            print(f"   - {issue['file']} [{issue.get('type')}] line {issue.get('line')}: {issue.get('message')}")
        if len(latex_issues) > 10:
            print(f"   … and {len(latex_issues) - 10} more.")
    else: # 🪐 LaTeX Doctor: No LaTeX issues detected. All constellations aligned ✨
        print("\n🪐 No LaTeX issues detected.\n\n        *       .\n   .            ▪︎\n          *          *\n      .         ✶        .\n ✦ All constellations aligned ✦\n")


def _parse_target_root() -> Path:
    """Parse CLI arguments and return the resolved target root path."""
    parser = argparse.ArgumentParser(
        description="Run diagnostics for " + QUALITY_NAME + " on a target repository."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Target repository root (default: current directory).",
    )
    args = parser.parse_args()
    return Path(args.target).resolve()


def _collect_core_checks(target_root: Path) -> List[Tuple[bool, str]]:
    """Run core installation checks for the given target root."""
    results: List[Tuple[bool, str]] = []
    results.append(check_python_version())
    results.append(check_package_import(target_root))
    results.append(check_version_module(target_root))
    for rel in [
        "Makefile",
        "interia_quality",
        "version.json",
        "quality_report.json",
        "refactor_plan.json",
        "ai_request.json",
        "ai_response.json",
    ]:
        ok, msg = check_file_exists(target_root, rel)
        results.append((ok, msg))
    return results


def _print_diagnostics(target_root: Path, results: List[Tuple[bool, str]]) -> None:
    """Display diagnostics and typical next steps."""
    print("\n🔎 Diagnostics:")

    latex_refactor_quality(target_root)
    latex_galaxy_map(target_root)

    for ok, msg in results:
        prefix = "✅" if ok else "⚠️"
        print(f" {prefix} {msg}")
    if all(ok for ok, _ in results[:3]):  # Python + package + version
        print("\n✨ Core InterIA Quality Pack appears to be installed correctly.")
    else:
        print("\n⚠️ Some core checks failed. Please review the warnings above.")

    print("\n💡 Typical next steps:")
    print("  - Run `make`           for quality & refactor plan")
    print("  - Run `make ai-request` to build the AI request")
    print("  - Run `make ai-preview` to inspect AI proposals")
    print("  - Run `make ai-apply`  to apply them (safely)")


def main() -> int:
    """Launch InterIA Doctor diagnostics from the command line."""
    target_root = _parse_target_root()
    print(f"🧭 InterIA Doctor – target: {target_root}")

    if not target_root.exists():
        print(f"❌ Target path does not exist: {target_root}")
        return 1

    results = _collect_core_checks(target_root)
    _print_diagnostics(target_root, results)

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
