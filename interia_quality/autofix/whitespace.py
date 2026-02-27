"""Autofix: remove trailing spaces and normalize EOL to LF."""
from pathlib import Path

TEXT_EXT = {".md", ".py", ".tex", ".txt", ".css", ".html", ".js"}

def run():
    """
    Apply non-destructive automatic fixes:

    - remove trailing spaces
    - convert CRLF to LF
    - preserve all other formatting

    Only applies to text-based file extensions.
    """
    for p in Path(".").rglob("*"):
        if not p.is_file():
            continue
        if p.suffix not in TEXT_EXT:
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        text = text.replace("\r\n", "\n")
        fixed = "\n".join(line.rstrip() for line in text.split("\n"))
        if fixed != text:
            p.write_text(fixed, encoding="utf-8")
