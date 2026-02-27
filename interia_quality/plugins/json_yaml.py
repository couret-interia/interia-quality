"""JSON/YAML lint plugin."""
from pathlib import Path
import json

try:
    import yaml  # type: ignore
except Exception:
    yaml = None


def run():
    """
    Validate JSON and YAML files in the project.

    - JSON files are checked using the Python standard library.
    - YAML files are validated only if PyYAML is installed.
    """
    issues = []
    root = Path(".")
    for p in root.rglob("*.json"):
        try:
            json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            issues.append(f"JSON error in {p}: {e}")
    for ext in ("*.yml", "*.yaml"):
        for p in root.rglob(ext):
            if yaml is None:
                issues.append(f"YAML not checked (PyYAML missing): {p}")
                continue
            try:
                yaml.safe_load(p.read_text(encoding="utf-8"))
            except Exception as e:
                issues.append(f"YAML error in {p}: {e}")
    return {"ok": not issues, "issues": issues}
