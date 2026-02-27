"""
version.py

InterIA Quality Pack v4 – Version Info
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

def _load_version_data() -> Dict[str, Any]:
    """
    Load version.json from the package root.

    Returns a dict with keys like name, version, build_date, etc.
    """
    # On part du dossier contenant ce fichier
    here = Path(__file__).resolve().parent
    # version.json est supposé être à la racine du pack, un niveau au-dessus
    version_path = here.parent / "version.json"
    if not version_path.exists():
        # Fallback: valeurs minimales en dur
        return {
            "name": "InterIA Quality Pack",
            "version": "4.0.0",
            "codename": "Cosmic v4",
            "build_date": "UNKNOWN",
        }
    try:
        return json.loads(version_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise FileNotFoundError(
            f"{version_path} JSON decoding failed: {e}."
        )

_VERSION_DATA = _load_version_data()

NAME: str = _VERSION_DATA.get("name", "InterIA Quality Pack")
VERSION: str = _VERSION_DATA.get("version", "4.0.0")
CODENAME: str = _VERSION_DATA.get("codename", "Cosmic v4")
BUILD_DATE: str = _VERSION_DATA.get("build_date", "UNKNOWN")

def as_string() -> str:
    """Return a single-line version string."""
    return f"{NAME} {VERSION} ({CODENAME}, built {BUILD_DATE})"
