#!/usr/bin/env python3
"""
interia_install.py

InterIA Quality Pack v4 – Initializer

This script installs the InterIA Quality Pack into a target repository.

What it does:
- Copies the `interia_quality/` package to the target root
- Copies quality READMEs (if present)
- Adds / appends Makefile targets for quality + refactor assist

Usage:
    python interia_install.py            # installs into current directory
    python interia_install.py path/to/repo
    python interia_install.py path/to/repo --force
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from interia_quality.version import NAME, CODENAME

QUALITY_NAME    = NAME + " " + CODENAME
QUALITY_MARKER  = "# >>> " + QUALITY_NAME
QUALITY_SNIPPET = QUALITY_MARKER + "\n\n" + Path('./Makefile').read_text() + "\n\n" + QUALITY_MARKER

def copy_tree(src: Path, dst: Path, force: bool = False) -> None:
    """Copy tree on src if not on dst, --force param clean dst before copying."""
    if dst.exists():
        if not force:
            print(f"⚠️  Destination {dst} already exists. Use --force to overwrite.")
            return
        print(f"🧹 Removing existing {dst} (force).")
        shutil.rmtree(dst)
    print(f"📁 Copying {src} → {dst}")
    shutil.copytree(src, dst)


def copy_file_if_missing(src: Path, dst: Path) -> None:
    """Copy file on src if missing on dst."""
    if not src.exists():
        return
    if dst.exists():
        print(f"ℹ️  File {dst} already exists, skipping.")
        return
    print(f"📄 Copying {src} → {dst}")
    shutil.copy2(src, dst)


def ensure_makefile(target_root: Path) -> Path:
    """Create Makefile or return target_root Makefile."""
    makefile = target_root / "Makefile"
    if not makefile.exists():
        print(f"🧾 No Makefile found in {target_root}, creating a new one.")
        makefile.write_text("", encoding="utf-8")
    return makefile


def patch_makefile(makefile: Path) -> None:
    """Attempt to patch (add) Makefile pack into target Makefile."""
    text = makefile.read_text(encoding="utf-8")
    marker = QUALITY_MARKER
    if marker in text:
        print("ℹ️  Makefile already contains InterIA Quality targets, skipping patch.")
        return
    print(f"🧷 Patching Makefile: adding InterIA Quality targets to {makefile}")
    with makefile.open("a", encoding="utf-8") as f:
        if text and not text.endswith("\n"):
            f.write("\n")
        f.write("\n" + QUALITY_SNIPPET + "\n")


def copy_package(script_dir, src_pkg, target_root, args) -> None:
    """Copying pack into target_root."""
    print(f"🚀 InterIA – installing Quality Pack into {target_root}")

    # Copy package
    dst_pkg = target_root / "interia_quality"
    copy_tree(src_pkg, dst_pkg, force=args.force)

    # Copy helper HTML + docs if present
    copy_file_if_missing(script_dir / "interia_menu.py", target_root / "interia_menu.py")
    copy_file_if_missing(script_dir / "interia_doctor.py", target_root / "interia_doctor.py")

    # Quality docs (recommended)
    copy_file_if_missing(
        script_dir / "README_interia_quality.md",
        target_root / "README_interia_quality.md",
    )
    copy_file_if_missing(
        script_dir / "README_interia_quality_quickstart.md",
        target_root / "README_interia_quality_quickstart.md",
    )
    copy_file_if_missing(
        script_dir / "AI_TOUR.md",
        target_root / "AI_TOUR.md",
    )
    copy_file_if_missing(
        script_dir / "AI_BRIDGE.md",
        target_root / "AI_BRIDGE.md",
    )

    # Makefile patch
    makefile = ensure_makefile(target_root)
    patch_makefile(makefile)


def main() -> int:
    """Main logic to add pack into target."""
    parser = argparse.ArgumentParser(
        description="Install " + QUALITY_NAME + " into a target repository."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Target repository root (default: current directory).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing interia_quality/ directory if present.",
    )
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    src_pkg = script_dir / "interia_quality"

    if not src_pkg.exists():
        print(f"❌ Cannot find interia_quality/ in {script_dir}")
        return 1

    target_root = Path(args.target).resolve()
    if not target_root.exists():
        print(f"❌ Target path {target_root} does not exist.")
        return 1

    copy_package(script_dir, src_pkg, target_root, args)

    print("\n✅ " + QUALITY_NAME + " installed.")
    print("   You can now run in the target repo:")
    print("   - make quality-all   (or make if is 1st in Makefile)")
    print("   - make ai-request    (or make ai-prompt)")
    print("   - make ai-preview")
    print("   - make ai-apply")
    print("   - make quality-help (Show utilities of all quality make commands)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
