"""
Python refactor scanner for InterIA Quality v4.

This module does NOT modify files.
It only produces structured suggestions about code quality,
including functions that are too long, too many arguments,
and missing docstrings.
"""

import ast, json
from pathlib import Path

MAX_FUNCTION_LINES = 50
MAX_ARGS = 5

def docstring_lines_length(node):
    """
    Return the docstring lines length (if present).

    Args:
        node (ast.FunctionDef): The function node to analyze.

    Returns:
        length of docstring lines.
    """

    docstring_lines = 0

    if (
        node.body
        and isinstance(node.body[0], ast.Expr)
        and hasattr(node.body[0], "value")
        and isinstance(node.body[0].value, (ast.Str, ast.Constant))
    ):
        docstring_node = node.body[0]
        ds_start = docstring_node.lineno
        ds_end = getattr(docstring_node, "end_lineno", docstring_node.lineno)
        docstring_lines = ds_end - ds_start + 1

    return docstring_lines


def get_snippet(node, start_line, end_line, file_path):
    """Return a text snippet for the given 1-based line range from file_path.

    If the requested range is invalid, returns False and logs a warning.
    """

    text = file_path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines(keepends=True)

    # Indexes for Python lists (0-based)
    start_idx = start_line - 1
    end_idx = end_line     # slice end is exclusive

    if start_idx < 0 or end_idx > len(lines):
        print(f"⚠️  Invalid location [{start_line}, {end_line}] in {file_path}, skipping.")
        return False

    return "".join(lines[start_idx:end_idx])


def extract_function_suggestions(node, path):
    """
    Analyze a single AST function node and generate suggestions.

    Checks function length, argument count, and presence of a docstring.
    Docstring lines are not counted toward the function length.

    Args:
        node (ast.FunctionDef): The function node to analyze.
        path (Path): Path to the Python file.

    Returns:
        list of dict: Refactor suggestions related to this function.
    """
    suggestions = []
    name = node.name
    start = node.lineno
    end = getattr(node, "end_lineno", node.lineno)
    length = end - start + 1 - docstring_lines_length(node)
    arg_count = len(node.args.args)

    if length > MAX_FUNCTION_LINES:
        suggestions.append({
            "type": "long_function",
            "file": str(path),
            "function": name,
            "lines": [start, end],
            "message": (
                f"Function '{name}' is {length} lines long "
                f"(>{MAX_FUNCTION_LINES} without docstring)."
            ),
            "action": "consider_split",
            "snippet": get_snippet(node, start, end, path),
        })

    if arg_count > MAX_ARGS:
        suggestions.append({
            "type": "too_many_args",
            "file": str(path),
            "function": name,
            "lines": [start, end],
            "args": arg_count,
            "message": (
                f"Function '{name}' has {arg_count} parameters "
                f"(>{MAX_ARGS})."
            ),
            "action": "introduce_dataclass_or_context",
            "snippet": get_snippet(node, start, end, path),
        })

    if ast.get_docstring(node) is None:
        suggestions.append({
            "type": "missing_docstring",
            "file": str(path),
            "function": name,
            "lines": [start, end], # Full snip. One line: use start, start
            "message": f"Function '{name}' has no docstring.",
            "action": "add_docstring",
            "snippet": get_snippet(node, start, end, path), # start, start
        })

    return suggestions


def analyze_file_functions(tree, path):
    """
    Traverse an AST tree and collect refactor suggestions for each function.

    Args:
        tree (ast.Module): The parsed AST of the file.
        path (Path): Path to the Python file.

    Returns:
        list of dict: All refactor suggestions from the file.
    """
    suggestions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            suggestions.extend(extract_function_suggestions(node, path))
    return suggestions


def scan_file(path: Path):
    """
    Analyze a single Python file and return refactor suggestions.

    Suggestions include long functions, too many arguments, and missing docstrings.

    Args:
        path (Path): The path to the Python file.

    Returns:
        list of dict: All suggestions for refactoring the file.
    """
    src = path.read_text(encoding="utf-8")
    tree = ast.parse(src)
    return analyze_file_functions(tree, path)


def find_python_files(root: Path):
    """
    Recursively yield all Python files starting from the given root.

    Args:
        root (Path): Root directory to scan.

    Yields:
        Path: Path object for each Python *.py file found.
    """
    return root.rglob("*.py")


def scan_project(root: Path | None = None):
    """
    Recursively scan all Python files under the given root and aggregate
    refactor suggestions for the whole project.

    Args:
        root (Path or None): Project root directory. Defaults to current directory.

    Returns:
        list of dict: Aggregated list of suggestions for the entire project.
    """
    if root is None:
        root = Path(".")
    all_suggestions = []
    for py_file in find_python_files(root):
        all_suggestions.extend(scan_file(py_file))
    return all_suggestions
