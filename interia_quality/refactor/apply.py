"""
Apply safe refactor suggestions from refactor_plan.json.

For now:
- add a minimal docstring template for functions without docstring.
"""

import json
from pathlib import Path

def apply_docstring_suggestions(plan: dict):
    """
    Apply basic refactor actions related to missing docstrings.

    Currently, this inserts a minimal TODO docstring template in functions
    flagged as missing a docstring.
    """
    for item in plan.get("python", []):
        if item.get("type") != "missing_docstring":
            continue

        file_path = Path(item["file"])
        if not file_path.exists():
            continue

        src = file_path.read_text(encoding="utf-8")
        lines = src.splitlines()

        # On insère la docstring juste après la ligne de définition.
        fun_start = item["lines"][0]
        # Attention : ce heuristique est volontairement simple.
        insert_at = fun_start  # ligne après "def ..."

        # On regarde la ligne de définition pour récupérer l'indentation réelle
        def_line = lines[insert_at - 1]
        base_indent = len(def_line) - len(def_line.lstrip(" "))
        indent = " " * (base_indent + 4)

        name = file_path.name
        if name.endswith(".py"):
            name = name[:-3]
        doc_line = f'{indent}"""TODO: add docstring. ({name}.{item["function"]})"""'
        lines.insert(insert_at, doc_line)

        file_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"✨ Added docstring template in {file_path} (function {item['function']})")


def main():
    """
    CLI entry to apply safe refactor actions defined in refactor_plan.json.
    """
    plan_path = Path("refactor_plan.json")
    if not plan_path.exists():
        print("❌ refactor_plan.json not found. Run `refactor-plan` first.")
        return 1
    try:
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise FileNotFoundError(
            f"{plan_path} JSON decoding failed: {e}."
        )

    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    apply_docstring_suggestions(plan)
    print("✅ Basic refactor actions applied (docstring templates).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
