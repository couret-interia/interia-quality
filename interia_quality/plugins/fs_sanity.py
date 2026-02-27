"""Filesystem sanity plugin: duplicates within same directory, forbidden chars."""
import os
from collections import defaultdict
from pathlib import Path

FORBIDDEN_CHARS = set('<>:"\\|?*')
IGNORED_DIRS = {'.git', '.github', '__pycache__', '.venv', 'venv', 'archives'}

def find_forbidden_names(name, rel_path):
    """
    Returns the path if the filename or directory name contains forbidden characters.

    Args:
        name (str): The name of the file or directory to check.
        rel_path (str): The relative path to the file or directory.

    Returns:
        str or None: The relative path if forbidden characters are detected, otherwise None.
    """
    if any(c in name for c in FORBIDDEN_CHARS):
        return rel_path
    return None


def should_ignore(parts):
    """
    Checks if the current directory should be skipped from analysis.

    Args:
        parts (list of str): Segments of the current directory path.

    Returns:
        bool: True if the directory should be ignored, False otherwise.
    """
    return parts[0] in IGNORED_DIRS if parts else False


def walk_filesystem(root):
    """
    Explores the directory tree from the provided root and gathers naming information.

    Args:
        root (Path): The root directory to start the scan.

    Returns:
        tuple:
            - dict of original names found by directory,
            - dict of lowercase names by directory,
            - list of paths containing forbidden characters.
    """
    per_dir_names = {}
    per_dir_lower_names = {}
    forbidden = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root)
        parts = rel_dir.split(os.sep)
        if should_ignore(parts):
            dirnames[:] = []
            continue
        names = per_dir_names.setdefault(rel_dir, defaultdict(list))
        lower = per_dir_lower_names.setdefault(rel_dir, defaultdict(list))
        for name in dirnames + filenames:
            rel_path = os.path.join(rel_dir, name) if rel_dir != "." else name
            names[name].append(rel_path)
            lower[name.lower()].append(rel_path)
            f = find_forbidden_names(name, rel_path)
            if f:
                forbidden.append(f)
    return per_dir_names, per_dir_lower_names, forbidden


def find_duplicates(per_dir_names):
    """
    Identifies duplicate filenames or directory names within the same directory.

    Args:
        per_dir_names (dict): Mapping of names to paths for each directory.

    Returns:
        dict: Duplicates organized by directory, where a name maps to more than one path.
    """
    dup = {rel_dir: {name: paths for name, paths in names.items() if len(paths) > 1}
           for rel_dir, names in per_dir_names.items()}
    return {k: v for k, v in dup.items() if v}


def find_case_collisions(per_dir_lower_names):
    """
    Finds case-only collisions where filenames differ only by letter casing.

    Args:
        per_dir_lower_names (dict): Mapping of lowercased names to paths in each directory.

    Returns:
        dict: Case collision details grouped by directory.
    """
    result = {}
    for rel_dir, lower in per_dir_lower_names.items():
        for lname, paths in lower.items():
            if len(paths) > 1 and len(set(paths)) > 1:
                result.setdefault(rel_dir, {})[lname] = paths
    return result


def build_issues(forbidden, dup, case_collisions):
    """
    Constructs a descriptive list of all detected filesystem issues.

    Args:
        forbidden (list): Paths containing forbidden characters.
        dup (dict): Directory-wise duplicate names.
        case_collisions (dict): Directory-wise case-only name collisions.

    Returns:
        list: Formatted problem descriptions as strings.
    """
    issues = []
    if forbidden:
        issues.append("Paths with forbidden characters (Windows/macOS sensitive):")
        issues.extend(sorted(forbidden))
    if dup:
        issues.append("Duplicate names within the same directory:")
        for rel_dir, name_dict in dup.items():
            for name, paths in name_dict.items():
                issues.append(f"{rel_dir or '.'}: {name} -> {paths}")
    if case_collisions:
        issues.append("Case-only filename collisions within the same directory:")
        for rel_dir, name_dict in case_collisions.items():
            for lname, paths in name_dict.items():
                issues.append(f"{rel_dir or '.'}: {lname} -> {paths}")
    return issues


def run():
    """
    Check for filesystem issues within each directory:

    - forbidden characters in filenames
    - duplicate filenames in the same directory
    - case-only collisions (dangerous for case-insensitive filesystems)

    Returns a dict with 'ok' and 'issues' keys.
    """
    root = Path(".")
    per_dir_names, per_dir_lower_names, forbidden = walk_filesystem(root)
    dup = find_duplicates(per_dir_names)
    case_collisions = find_case_collisions(per_dir_lower_names)
    issues = build_issues(forbidden, dup, case_collisions)
    return {"ok": not issues, "issues": issues}
