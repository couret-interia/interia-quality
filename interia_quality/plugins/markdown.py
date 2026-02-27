"""Markdown fence safety plugin (lightweight)."""
from pathlib import Path

# Patterns can be customized per-repo; here they are disabled by default.
DANGEROUS_PATTERNS = []  # e.g. ["``` `", "` ``` `"]

def run():
    """
    Markdown fence safety check (lightweight).

    If DANGEROUS_PATTERNS is non-empty, the plugin scans Markdown files
    for inline fence sequences that may break rendering.
    """
    issues = []
    if not DANGEROUS_PATTERNS:
        return {"ok": True, "issues": []}
    for p in Path(".").rglob("*.md"):
        text = p.read_text(encoding="utf-8", errors="ignore")
        for pat in DANGEROUS_PATTERNS:
            if pat in text:
                issues.append(f"{p}: contains pattern {pat!r}")
    return {"ok": not issues, "issues": issues}
