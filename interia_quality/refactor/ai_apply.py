"""
ai_apply.py

InterIA Quality v4 – AI Apply

Apply edits described in ai_response.json to the local files.

Each edit is expected to have the following structure:

{
  "file": "path/to/file.py",
  "kind": "python_function_refactor",
  "location": {"start_line": 10, "end_line": 42},
  "old_snippet": "the \"\\nold\" \n# code...",
  "new_snippet": "The \"\\nNew\" \n# code...",
  "rationale": "why this is better"
}

Safety rules:
- If ai_response.json is missing or malformed, no changes are applied.
- For each edit, if the current file contents do not match old_snippet
  at the given location, the edit is skipped with a warning.
- For each modified file, a backup copy is created once:
  <filename>.interia-ai-backup
"""

from __future__ import annotations

import re, json
from pathlib import Path
from typing import Any, Dict, List

AI_RESPONSE_PATH = Path("ai_response.json")

def load_ai_response() -> Dict[str, Any]:
    """Load ai_response.json or raise JSONDecodeError, FileNotFoundError if missing."""
    if not AI_RESPONSE_PATH.exists():
        raise FileNotFoundError(
            f"{AI_RESPONSE_PATH} not found. "
            "You must create it from an external AI using ai_request.json."
        )
    try:
        return json.loads(AI_RESPONSE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise FileNotFoundError(
            f"{AI_RESPONSE_PATH} JSON decoding failed: {e}. \n---\n"
            "💡 Load ai_response.json in 🔑 JSON Tool: http://127.0.0.1:8000/interia_quality/board/ai_preview.html#tools\n"
            "🧩 When AI say like full implementation of old snip or not provided, copy snippet line from request/plan to old_snippet in ai_response.json\n"
            "🧪 You must verify if the double quotes `\"` bein escaped like this: \n "
            "\"snippets\": \"\\\"\\\"\\\"docstr\\\"\\\"\\\"\\nsame=\\\"think\\\"\\n#in code.\","
        )


def _get_location_lines(edit: dict) -> list[int]:
    """Extract a [start_line, end_line] pair from an edit's location.

    The location may be a mapping with `start_line`/`end_line` keys or a
    string containing line numbers. The returned list is ordered so that the
    end line is always greater than or equal to the start line.
    """
    loc = edit.get("location") or {}
    lines = [0, 0]

    if isinstance(loc, dict):
        try:
            start = int(loc.get("start_line") or 0)
            end = int(loc.get("end_line") or 0)
        except (TypeError, ValueError):
            return lines
        if end < start:
            end = start
        return [start, end]

    if isinstance(loc, str):
        nums = [int(x) for x in re.findall(r'\d+', loc)]
        if len(nums) >= 2:
            lines = nums[:2]
            if lines[1] < lines[0]:
                lines[1] = lines[0]
            print(f"🔬 Snippet lines {lines} extracted from 'str' location: {loc}")
        return lines

    return lines


def _has_overlap(e1: Dict[str, Any], e2: Dict[str, Any]) -> bool:
    """Return true if Overlaps, false otherwise (_warn_overlaps helper)"""
    a1, b1 = _get_location_lines(e1)
    a2, b2 = _get_location_lines(e2)
    return not (b1 < a2 or b2 < a1)


def _warn_overlaps(path: Path, edits: List[Dict[str, Any]]) -> None:
    """Check Overlap edits and log when detected"""
    n = len(edits)
    for i in range(n):
        for j in range(i + 1, n):
            if _has_overlap(edits[i], edits[j]):
                print(f"⚠️  Overlapping edits detected in {path}: #{i} and #{j}")


def _print_diff_for_mismatch(file_path: Path, snips: list[str,str], loc_lines: list[int, int]) -> None:
    """Log a diff-style hint when the old snippet cannot be found.

    This keeps the main edit function smaller while preserving behaviour and
    diagnostic messages.
    """
    start_line, end_line = loc_lines
    old, window = snips
    # For idea : https://www.educative.io/answers/how-to-return-the-difference-of-two-strings-in-python
    # Inspired : https://stackoverflow.com/questions/46453075/python-getting-just-the-difference-between-strings#46453470
    splits = [set(old.strip().split("\n")), set(window.strip().split("\n"))]
    diffs = ["\n".join(splits[1].difference(splits[0])), "\n".join(splits[0].difference(splits[1]))]
    print(f"   ↳ Content mismatch in {file_path} at lines {start_line}-{end_line}.")
    if len(diffs[0]) < 618:
        print(
            f"🧩 Diff of line(s) in <old_snippet> ≌ <window code>:\n```\n{diffs[1]}\n```\n"
            f"👉 Diff of between <window code> and expected line(s) in <old_snippet>:\n```\n{diffs[0]}\n```\n"
            "💡 On snippet in ai preview page of portal, click on -🔨 Load Diff- Tool and click on -🔍- te see code editors, "
            "in -New Snippet (Diff B)-, click on -🔨 request- (or -🔨 plan-) button to compare with old ≌ snippet"
        )
    else:
        print(
            f"❓ Ancient 'ai_response' edit, experiment, old snippet? The difference is {len(diffs[0])} ≌ {len(diffs[1])} characters"
        )


def _build_line_offsets(lines):
    """Return a list with the character offset at the beginning of each line."""
    offsets = []
    pos = 0
    for line in lines:
        offsets.append(pos)
        pos += len(line)
    return offsets


def _compute_search_window(text: str, offsets: list, lines: str, loc_lines: list[int,int], margin: int):
    """Compute a search window around the requested line range.

    The window is defined by start, end location lines
    extended by ``margin`` lines on each side. It returns the substring of ``text``
    covered by this window together with the starting character index
    and the normalized start and end line numbers.
    """
    start_line, end_line = loc_lines
    start_line = max(start_line, 1)
    end_line = max(end_line, start_line)

    i0 = max(start_line - 1 - margin, 0)
    i1 = min(end_line - 1 + margin, len(lines) - 1)

    start_char = offsets[i0]
    end_char = offsets[i1] + len(lines[i1])

    window = text[start_char:end_char]
    return window, start_char, start_line, end_line


def _print_missing_snippet_warning(
    file_path: Path,
    loc_lines: list[int, int],
    old: str,
    window: str,
) -> None:
    """Log a warning and show a diff when the expected snippet cannot be found."""
    print(f"⚠️  <old_snippet> not in actual <full code> for edit in {file_path}, skipping.")
    if old.strip() and window.strip() != old.strip():
        snips = [old, window]
        _print_diff_for_mismatch(file_path, snips, loc_lines)


def _find_old_snippet_index(text: str, snips: list[str, str], loc_lines: list[int, int], file_path: Path) -> int:
    """
    Locate the absolute index of ``old`` (snips) in ``text`` source code.

    The function first searches within the approximate ``start_line``/``end_line`` i(loc_lines)
    window (with a small margin) and then falls back to a global search.
    Returns ``-1`` when the edit should be skipped (e.g. invalid location,
    empty content, or the snippet already appears as ``new`` in the file).
    """
    old, new = snips
    start_line, end_line = loc_lines
    # Indexes for Python lists (0-based)
    start_idx, end_idx = [start_line - 1, end_line]  # slice end is exclusive

    # Line breaks with \n preserved
    lines = text.splitlines(keepends=True)
    if not lines:
        print(f"⚠️  No text lines in {file_path}, skipping.")
        return -1

    # Location lines minimal checks
    if start_idx < 0 or end_idx > len(lines):
        print(f"⚠️  Invalid location [{start_line}, {end_line}] in {file_path}, skipping.")
        return -1

    # Offset table (character index at the beginning of each line)
    offsets = _build_line_offsets(lines)
    # A small margin around the announced area is tolerated.
    margin = 3
    window = _compute_search_window(text, offsets, lines, loc_lines, margin)
    window, start_char, start_line, end_line = window

    idx = window.find(old)
    if idx >= 0:
        # found in the local window
        edt_idx = window.find(new)
        if edt_idx >= 0:
            # new snippet found in the local window
            print(f"💚 Already edited, <new_snippet> in actual <window code> in {file_path}, skipping.")
            return -1

        abs_idx = start_char + idx
        return abs_idx

    # global fallback
    edt_idx = text.find(new)
    if edt_idx >= 0:
        # new snippet found in the local text
        print(f"🍀 Already edited, <new_snippet> in actual <full code> in {file_path}, skipping.")
        return -1

    abs_idx = text.find(old)
    if abs_idx < 0:
        _print_missing_snippet_warning(file_path, loc_lines, old, window)
        return -1

    return abs_idx


def _apply_single_edit(text: str, edit: Dict[str, Any], file_path: Path) -> tuple[str, bool]:
    """
    Apply a single edit to the full file contents.

    The edit is located using ``location.start_line`` / ``location.end_line``
    as an approximate range and, if needed, a global search for
    ``old_snippet``. Returns the updated text and a flag indicating whether
    the edit was applied.
    """
    location_lines = _get_location_lines(edit)
    if len(location_lines) < 2:
        print(f"⚠️  Missing edit location start & end line numbers to find code in {file_path}, skipping.")
        return text, False

    start_line, end_line = location_lines
    if start_line <= 0 or end_line <= 0:
        print(f"⚠️  Invalid or missing location for edit in {file_path}, skipping.")
        return text, False

    new = edit.get("new_snippet", "")
    if not new:
        print(f"⚠️  Edit without 'new_snippet' in {file_path}, skipping.")
        return text, False

    old = edit.get("old_snippet", "")
    if not old:
        print(f"⚠️  Edit without 'old_snippet' in {file_path}, skipping.")
        return text, False

    snips = [old, new]
    abs_idx = _find_old_snippet_index(text, snips, location_lines, file_path)
    if abs_idx < 0:
        return text, False

    before = text[:abs_idx]
    after = text[abs_idx + len(old):]
    new_text = before + new
    new_text += after
    return new_text, True


def _end_line(e: Dict[str, Any]) -> int:
    """Return the end line for an edit and normalise its location.

    When the `location` field is a string, this also updates the edit in
    place to use a structured mapping with `start_line` and `end_line`.

    - Helper for apply_edits_for_file to sort from bottom to top.
    - Only one Log message in _get_location_lines() by update object.
    """
    start, end = _get_location_lines(e)
    # Set missing keys
    loc = e.get("location")
    if isinstance(loc, str) or loc is None:
        e["location"] = {"start_line": start, "end_line": end}
    return end


def apply_edits_for_file(path: Path, file_edits: List[Dict[str, Any]]) -> bool:
    """
    Applies all edits for a given file.

    - Sorts edits by start_line in descending order.
    - Applies each edit to a buffer in memory.
    - Return true if edited, false otherwise.
    """
    if not path.exists():
        print(f"⚠️  File not found: {path}, skipping.")
        return False

    _warn_overlaps(path, file_edits)
    # Sort from bottom to top to avoid line shifts
    file_edits_sorted = sorted(file_edits, key=_end_line, reverse=True)

    edited = False
    text = path.read_text(encoding="utf-8")
    for edit in file_edits_sorted:
        kind = edit.get("kind", "⏼ edit placeholder (kind missing)")
        print(f"--- 🔹 Init Kind '{kind}' in {path} ---")
        rationale = edit.get("rationale", "")
        text, applied = _apply_single_edit(text, edit, path)
        if applied:
            edited = True
            print(f"✨ Applied '{kind}' in {path}")
        else:
            print(f"⚠️  Skipped '{kind}' in {path}")
        if rationale:
            print(f"   ↳ Rationale: {rationale}")

    if edited:
        path.write_text(text, encoding="utf-8")
    return edited


def apply_all_edits(data: Dict[str, Any]) -> None:
    """
    Apply all edits described in the AI response.

    Creates a single backup per file the first time it is modified.
    """
    edits: List[Dict[str, Any]] = data.get("edits", [])
    if not edits:
        print("ℹ️  No edits found in ai_response.json.")
        return

    modified_files: set[Path] = set()
    backups_done: set[Path] = set()

    # Group per file
    by_file: dict[Path, list[dict]] = {}
    for edit in edits:
        file_str = edit.get("file")
        if not file_str:
            print("⚠️  Edit without 'file' key field, skipping.")
            continue
        file_path = Path(file_str)
        by_file.setdefault(file_path, []).append(edit)

    for file_path, file_edits in by_file.items():
        print(f"\n--- 🔷 Init Edits for '{file_path}' ---")

        if not file_path.exists():
            print(f"⚠️  File not found: {file_path}, skipping.")
            continue

        original_text = file_path.read_text(encoding="utf-8")
        if apply_edits_for_file(file_path, file_edits):
            # Backup once per file
            if file_path not in backups_done and file_path.exists():
                backup_path = file_path.with_suffix(file_path.suffix + ".interia-ai-backup")
                backup_path.write_text(original_text, encoding="utf-8")
                backups_done.add(file_path)
                print(f"🗂  Backup created: {backup_path}")
            modified_files.add(file_path)

    if not modified_files:
        print("ℹ️  No edits were applied (all skipped).")
    else:
        print("\n✅ AI edits applied to the following files:")
        for f in sorted(modified_files):
            print(f" - {f}")


def main() -> int:
    """CLI entry to apply AI-suggested edits from ai_response.json."""
    try:
        data = load_ai_response()
    except FileNotFoundError as e:
        print(f"⚠️  {e}")
        return 1

    apply_all_edits(data)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
