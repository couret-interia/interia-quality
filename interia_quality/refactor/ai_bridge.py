"""
ai_bridge.py

InterIA Quality v4 – AI Bridge

This module defines the JSON contract between the Quality Pack and
an external AI (LLM, custom tool, etc.).

It does NOT make any network calls.
It simply:
- builds an ai_request.json file from refactor_plan.json
- loads ai_response.json if present
- summarizes the AI's proposals

The external AI is supposed to:
- read ai_request.json
- produce ai_response.json in the expected format
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

AI_REQUEST_PATH = Path("ai_request.json")
AI_RESPONSE_PATH = Path("ai_response.json")
REF_PLAN_PATH = Path("refactor_plan.json")
AI_PROMPT_PATH = Path("ai_prompt.txt")
# Prompt template FR/EN with included JSON
PROMPT = r"""
You are helping with an internal tool called "InterIA Quality Pack v4".

It generates refactor suggestions for a project (Python + Markdown + LaTeX),
and packages them in a JSON file called `ai_request.json`.

Below is the full content of ai_request.json:

```json
{}
```

---

Your task:

1. Read the `suggestions` field carefully (Python + Markdown + LaTeX).
2. For a subset of the most relevant suggestions, propose concrete edits:

- For Python:
  - improved function docstrings
  - smaller functions (split long ones)
  - clearer names if really needed

- For Markdown:
  - shorter, clearer headings
  - replacement of TODO / WIP tokens with more neutral text

3. Do NOT change the semantics of the code.
4. Return a JSON object with the following structure:

```json
{{
  "project": "{}",
  "edits": [
    {{
      "file": "path/to/file.py",
      "kind": "python_function_refactor",
      "location": {{ "start_line": 10, "end_line": 42 }},
      "old_snippet": "the \"\\nold\" \n# code...",
      "new_snippet": "The \"\\nNew\" \n# code...",
      "rationale": "short explanation of why this is clearer or better"
    }}
  ]
}}
```


Important constraints for the JSON edits:

- For each edit, ALWAYS fill:
  - "file": path to the file (relative to the project root),
  - "kind": a short string describing the type of edit,
  - "location": {{ "start_line": int, "end_line": int }} with 1-based line numbers,
  - "old_snippet": exact copy of the current code/text in that region,
  - "new_snippet": the modified code/text,
  - "rationale": short explanation (1–3 lines).

- "start_line" / "end_line" are approximate and mainly used as hints.
  The tool applies edits using the exact content of "old_snippet".

- If you propose several edits in the same file:
  - DO NOT create overlapping regions (they should not touch or intersect).
  - You may output them in any order; the tool will apply them from bottom
    to top inside each file to avoid line-shift issues.


Important:

- Output ONLY this JSON object (in bloc code), nothing else.
- Keep `new_snippet` as close as possible to the original (minimal but useful edits).
- If unsure, you may omit a change instead of guessing.
"""


def build_ai_prompt(project_name: str = Path.cwd().name) -> bool:
    """
    Build ai_prompt.txt from ai_request.json.

    This file can be copy-pasted directly into an external LLM.
    """
    if not AI_REQUEST_PATH.exists():
        payload = build_ai_payload(project_name=project_name)
        if not payload:
            # build_ai_payload has already printed a warning
            return False
    try:
        payload = json.loads(AI_REQUEST_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"⚠️  {AI_REQUEST_PATH} exists but is not valid JSON: {e}")
        print("   Tip: open it in your editor or JSON viewer, fix, then rerun `interia-quality ai-prompt`.")
        return False

    prompt = PROMPT.format(json.dumps(payload, indent=2), payload.get("project", project_name))
    AI_PROMPT_PATH.write_text(prompt, encoding="utf-8")
    print(f"📝  AI prompt written to {AI_PROMPT_PATH}")
    print("You can now open this file and copy/paste it into your LLM of choice.")
    return True


def build_ai_payload(project_name: str = Path.cwd().name) -> Dict[str, Any]:
    """
    Build ai_request.json from refactor_plan.json.

    Returns the payload dict on success, or False if refactor_plan.json is missing.
    """
    if not REF_PLAN_PATH.exists():
        print(f'⚠️  "{REF_PLAN_PATH}" not found. Run `refactor-plan` first.')
        return False
    try:
        plan = json.loads(REF_PLAN_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(
            f"{REF_PLAN_PATH} exists but JSON decoding failed: {e}. "
            "Did you manually edit it? Try rebuilding it with `interia-quality refactor-plan`."
        )

    payload: Dict[str, Any] = {
        "project": project_name,
        "version": "v4",
        "context": {
            "description": "InterIA Quality Pack v4 refactor suggestions for Python, Markdown and LaTeX.",
            "note": (
                "You are asked to propose concrete refactorings: better function names, "
                "smaller functions, improved docstrings, clearer section headings, etc., "
                "without changing semantics."
            ),
        },
        "suggestions": plan,
        "instructions": (
            "For each suggestion, propose a concrete edit. Prefer minimal, readable changes. "
            "Return a JSON object with a top-level 'edits' list, where each edit has at least: "
            "file, kind, location with {'start_line': int, 'end_line': int}, old_snippet, "
            "new_snippet, and rationale. "
            "Use 1-based line numbers, and ensure that, for a given file, edit regions do not "
            "touch or overlap. You may output edits in any order; the tool will apply them from "
            "the bottom of the file to the top to avoid line-shift issues."
        ),
    }

    AI_REQUEST_PATH.write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )

    return payload


def main_build() -> int:
    """CLI entry to build ai_request.json from refactor_plan.json."""
    try:
        payload = build_ai_payload()
    except ValueError as e:
        print(f"❌  {e}")
        return 1

    if not payload:
        print(f"❌  Error to write AI request")
        return 1
    print(f"📤  AI request written to {AI_REQUEST_PATH}")
    print("You can now feed this JSON to an external AI system.")
    return 0


def main_summary() -> int:
    """CLI entry to summarize ai_response.json."""
    from .ai_apply import load_ai_response

    try:
        data = load_ai_response()
    except FileNotFoundError as e:
        print(f"⚠️  {e}")
        return 1

    edits = data.get("edits", [])
    print(f"🔍  AI response loaded. Total edits proposed: {len(edits)}")

    if not edits:
        print("No edits in response.")
        return 0

    by_file: dict[str, int] = {}
    for edit in edits:
        f = edit.get("file", "UNKNOWN")
        by_file[f] = by_file.get(f, 0) + 1

    print("\nEdits per file:")
    for f, count in sorted(by_file.items()):
        print(f" - {f}: {count} edit(s)")
    return 0


def main_prompt() -> int:
    """CLI entry to build ai_prompt.txt."""
    ok = build_ai_prompt()
    return 0 if ok else 1

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "build":
        raise SystemExit(main_build())
    elif len(sys.argv) > 1 and sys.argv[1] == "summary":
        raise SystemExit(main_summary())
    elif len(sys.argv) > 1 and sys.argv[1] == "prompt":
        raise SystemExit(main_prompt())
    else:
        print("Usage: python -m interia_quality.refactor.ai_bridge [build|summary|prompt]")
        raise SystemExit(1)
