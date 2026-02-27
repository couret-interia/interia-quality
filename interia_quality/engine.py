#!/usr/bin/env python3
"""
 ╔═════════════════════════════════╗
 ║    INTERIA QUALITY PACK — v4    ║
 ║      « ✨ Cosmic Edition »      ║
 ╚═════════════════════════════════╝
Loads all plugins under interia_quality.plugins and runs them.
Produces a JSON report (quality_report.json).
"""
import importlib
import json
import pkgutil
import sys
from pathlib import Path

def load_plugins():
    """Load all quality plugins from the interia_quality.plugins package."""
    import interia_quality.plugins as plugins_pkg
    plugins = []
    for module in pkgutil.iter_modules(plugins_pkg.__path__):
        mod = importlib.import_module(f"interia_quality.plugins.{module.name}")
        if hasattr(mod, "run"):
            plugins.append(mod)
    return plugins


def run_all():
    """Run all loaded quality plugins and collect their results in a dict."""
    report = {}
    for plugin in load_plugins():
        name = plugin.__name__.split(".")[-1]
        try:
            result = plugin.run()
        except Exception as e:
            result = {"ok": False, "issues": [f"Plugin error: {e}"]}
        report[name] = result
    return report


def save_report(report, path: str = "quality_report.json"):
    """Save the aggregated quality report as a JSON file at the given path."""
    Path(path).write_text(json.dumps(report, indent=2), encoding="utf-8")
    return path


def main():
    """Entry point: run all plugins and save the report."""
    report = run_all()
    save_report(report)
    failed = any(not v.get("ok", False) for v in report.values())
    if failed:
        print("❌ InterIA Quality Pack v4: some checks failed. See quality_report.json.")
    else:
        print("✨ InterIA Quality Pack v4: all checks passed.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
