"""LaTeX plugin: run chktex if available."""
import shutil, subprocess
from pathlib import Path

def run():
    """
    Validate LaTeX files using chktex if available.

    If chktex is not found or no .tex file is present,
    the plugin reports success with informational notes.
    """
    if shutil.which("chktex") is None:
        return {"ok": True, "issues": ["chktex not found; LaTeX lint skipped."]}

    root = Path(".")
    tex_files = list(root.rglob("*.tex"))
    if not tex_files:
        return {"ok": True, "issues": ["No .tex files found; skipping LaTeX lint."]}

    issues = []
    for p in tex_files:
        cmd = ["chktex", "-q", "-n1", "-n2", "-n3", str(p)]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True)
        except Exception as e:
            issues.append(f"{p}: chktex failed to run: {e}")
            continue
        if res.returncode != 0 and res.stdout.strip():
            issues.append(f"{p}: {res.stdout.strip()}")
    return {"ok": not issues, "issues": issues}
