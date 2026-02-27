"""Versioning plugin: detect -vX.Y patterns in file/dir names."""
import os, re, fnmatch
from pathlib import Path

PAT_SUFFIX = re.compile(r"-v[0-9]+(\.[0-9]+)*")
PAT_PREFIX = re.compile(r"^v[0-9]+(\.[0-9]+)*-")
IGNORED_DIRS = {'.git', '.github', '__pycache__', '.venv', 'venv', 'archives'}

def load_allowlist(path: str = ".interia_versioning_allowlist"):
    """
    Load versioning allowlist patterns from the given file, if it exists.

    Each non-empty, non-comment line is treated as a glob pattern.
    """
    if not os.path.exists(path):
        return []
    patterns = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            patterns.append(line)
    return patterns


def is_allowed(rel_path: str, allow_patterns):
    """Return True if the given relative path matches at least one allowlist pattern."""
    return any(fnmatch.fnmatch(rel_path, pat) for pat in allow_patterns)


def run():
    """
    Check file and directory names for forbidden version-like patterns.

    Returns a dict with 'ok' and 'issues' keys to be consumed by the engine.
    """
    root = Path(".").resolve()
    allow = load_allowlist()
    violations = []

    for current_dir, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(current_dir, root)
        parts = rel_dir.split(os.sep)
        if parts[0] in IGNORED_DIRS:
            dirnames[:] = []
            continue

        for d in list(dirnames):
            rel_path = os.path.join(rel_dir, d) if rel_dir != "." else d
            if is_allowed(rel_path, allow):
                continue
            if PAT_SUFFIX.search(d) or PAT_PREFIX.search(d):
                violations.append(f"dir: {rel_path}")

        for fname in filenames:
            rel_path = os.path.join(rel_dir, fname) if rel_dir != "." else fname
            if is_allowed(rel_path, allow):
                continue
            if PAT_SUFFIX.search(fname) or PAT_PREFIX.search(fname):
                violations.append(f"file: {rel_path}")

    return {"ok": not violations, "issues": violations}
