"""Text style plugin: UTF-8, LF, no trailing spaces on selected extensions."""
from pathlib import Path

TEXT_EXT = {".md", ".py", ".tex", ".txt", ".yml", ".yaml", ".json", ".css", ".html", ".js"}
IGNORED_DIRS = {'.git', '.github', '__pycache__', '.venv', 'venv', 'archives'}

def is_text(path: Path):
    """
    Return True if the given file path has an extension considered a text file.

    Only files matching the TEXT_EXT set are processed for style checks.
    """
    return path.suffix in TEXT_EXT


def run():
    """
    Perform text-style checks on selected file types:

    UTF-8 decoding, trailing spaces and line endings (LF only)

    Returns a dict with 'ok' and 'issues' keys.
    """
    root = Path(".")
    trailing = []
    crlf = []
    unreadable = []

    for p in root.rglob("*"):
        if not p.is_file():
            continue
        parts = p.relative_to(root).parts
        if parts and parts[0] in IGNORED_DIRS:
            continue
        if not is_text(p):
            continue
        try:
            data = p.read_bytes()
        except Exception as e:
            unreadable.append(f"{p}: cannot read bytes: {e}")
            continue
        try:
            text = data.decode("utf-8")
        except Exception as e:
            unreadable.append(f"{p}: not valid UTF-8: {e}")
            continue

        lines = text.splitlines(keepends=True)
        for i, line in enumerate(lines, start=1):
            if line.endswith("\r\n"):
                crlf.append(f"{p}:{i}")
            if line.rstrip("\n\r") != line.rstrip("\n\r ").rstrip("\n\r"):
                trailing.append(f"{p}:{i}")

    issues = []
    if unreadable:
        issues.append("Unreadable or non-UTF-8 files:")
        issues.extend(unreadable)
    if crlf:
        issues.append("Files with CRLF line endings:")
        issues.extend(crlf)
    if trailing:
        issues.append("Lines with trailing spaces:")
        issues.extend(trailing)
    return {"ok": not issues, "issues": issues}
