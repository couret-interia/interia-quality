"""Astro-format plugin: placeholder for InterIA-specific tokens (TODO/WIP)."""
from pathlib import Path

FORBIDDEN_TOKENS = ["TODO:", "WIP", "???"]

def run():
    """
    Scan Markdown files for InterIA-specific forbidden tokens
    such as TODO:, WIP or ???.

    Returns a dict with 'ok' and 'issues' keys.
    """
    issues = []
    for p in Path(".").rglob("*.md"):
        text = p.read_text(encoding="utf-8", errors="ignore")
        for token in FORBIDDEN_TOKENS:
            if token in text:
                issues.append(f"{p}: contains token '{token}'")
    return {"ok": not issues, "issues": issues}
