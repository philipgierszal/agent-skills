"""Orphan ratchet: every file must be reachable from the repository's tree (Z-571).

One identical copy per repository, like scripts/code_health.py; settings under the
"orphans" key of scripts/code_health.json (or scripts/orphan_check.json):
"roots" (entry points, globs; default README.md and AGENTS.md), "leaves" (files that
are reached but reach nothing, e.g. tests), "module_roots" (import roots such as
"src") and "not_sources" (files that list every file and prove nothing).

A file is reachable when a reachable file names it: a Markdown link, a path in text
or code (repository-relative, relative to the naming file, an add-on path such as
``/optiguard_crm/static/...``, or a glob such as ``scripts/test_*.py``), a Python
import, or an add-on manifest entry. A bare file name counts when no other file has
that name, except in data files (CSV, JSON). A glob's ``*`` stays inside one folder;
``**`` crosses folders. A folder link reaches its README.md (index.md, SKILL.md,
__manifest__.py). A manifest reaches what Odoo loads by convention: ``__init__.py``,
``hooks.py``, ``tests/__init__.py``, ``migrations/``, ``i18n/`` and
``static/description/``. A Python file reaches its sibling ``test_<name>.py`` and,
when reached, its packages' ``__init__.py``.

Usage: ``python scripts/orphan_check.py`` fails on an orphan missing from
``scripts/orphan_baseline.json`` (absent = empty); ``--write-baseline`` rewrites it,
which may only shrink unless ``CHECK_ALLOW_ORPHAN_BASELINE=1``; ``--tree`` prints the
tree. Untracked, non-ignored files count too, so a new file needs its home first.
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import posixpath
import re
import subprocess
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SETTINGS = ("scripts/code_health.json", "scripts/orphan_check.json")
BASELINE = "scripts/orphan_baseline.json"
OVERRIDE = "CHECK_ALLOW_ORPHAN_BASELINE"
DEFAULTS: dict[str, list[str]] = {
    "roots": ["README.md", "AGENTS.md"],
    "leaves": [],
    "module_roots": [],
    "not_sources": [
        ".gitattributes",
        ".editorconfig",
        "scripts/code_health_baseline.json",
        BASELINE,
    ],
}
TOKEN = re.compile(
    r"[\w./*\-]*[\w*]\.[\w*][\w*\-]*|addons/\w+|[\w.\-]+/[\w./*\-]+"
    r"|\w+(?:-\w+)+|\.\w[\w.\-]*"
)
INDEXES = ("__manifest__.py", "README.md", "index.md", "SKILL.md")
CONVENTION_DIRS = ("i18n/", "static/description/", "migrations/")
CONVENTION_FILES = ("__init__.py", "hooks.py", "tests/__init__.py")
DATA_SUFFIXES = (".csv", ".json", ".jsonl")
TEXT_LIMIT = 2_000_000


def repository_files(root: Path) -> list[str]:
    """Tracked and untracked non-ignored files; outside Git, every file but .git."""
    command = ["git", "-c", "core.quotePath=false", "ls-files", "-z", "--cached"]
    command += ["--others", "--exclude-standard"]
    result = subprocess.run(command, cwd=root, capture_output=True, check=False)  # noqa: S603
    if result.returncode != 0:
        paths = (p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file())
        return sorted(
            p for p in paths if not {".git", "node_modules"} & set(p.split("/"))
        )
    names = result.stdout.decode("utf-8", errors="replace").split("\0")
    return sorted(p for p in names if p and (root / p).is_file())


def load_settings(root: Path) -> dict[str, list[str]]:
    for name in SETTINGS:
        path = root / name
        if path.is_file():
            data = json.loads(path.read_text(encoding="utf-8"))
            if "orphans" in data:
                return {**DEFAULTS, **dict(data["orphans"])}
    return dict(DEFAULTS)


def glob_regex(pattern: str) -> re.Pattern[str]:
    """``*`` matches inside one folder, ``**`` across folders; case-sensitive."""
    pieces = {"**/": "(?:.*/)?", "**": ".*", "*": "[^/]*"}
    parts = re.split(r"(\*\*/?|\*)", pattern)
    return re.compile("".join(pieces.get(p, re.escape(p)) for p in parts) + r"\Z")


def matches(path: str, patterns: list[str]) -> bool:
    return any(glob_regex(pattern).match(path) for pattern in patterns)


class Index:
    """Lookups from a path-like token to repository files."""

    def __init__(self, files: list[str], settings: dict[str, list[str]]) -> None:
        self.files = set(files)
        self.settings = settings
        self.by_name: dict[str, list[str]] = {}
        for path in files:
            self.by_name.setdefault(posixpath.basename(path), []).append(path)
        self.addon_paths = {
            path.split("/")[-2]: posixpath.dirname(posixpath.dirname(path))
            for path in files
            if path.endswith("/__manifest__.py")
        }

    def candidates(self, token: str, folder: str) -> list[str]:
        token = token.strip("`'\"()").rstrip(".,;:")
        while token.startswith("./"):
            token = token[2:]
        token = token.lstrip("/")
        options = [token, posixpath.normpath(posixpath.join(folder, token))]
        head = token.split("/", 1)[0]
        if head in self.addon_paths:
            options.append(posixpath.join(self.addon_paths[head], token))
        return options

    def resolve(self, token: str, folder: str, bare: bool = True) -> set[str]:
        found: set[str] = set()
        for option in self.candidates(token, folder):
            found |= self.match(option)
        if bare and not found and "/" not in token and "*" not in token:
            paths = self.by_name.get(token, [])
            found |= set(paths) if len(paths) == 1 else set()
        return found

    def match(self, option: str) -> set[str]:
        if option.startswith("..") or option in ("", "."):
            return set()
        if "*" in option:
            pattern = glob_regex(option)
            return {path for path in self.files if pattern.match(path)}
        if option in self.files:
            return {option}
        prefix = option.rstrip("/") + "/"
        index = [prefix + name for name in INDEXES if prefix + name in self.files]
        return set(index[:1])


def python_imports(path: str, text: str, index: Index) -> set[str]:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return set()
    bases = [posixpath.dirname(path), "", *index.settings["module_roots"]]
    found: set[str] = set()
    for node in ast.walk(tree):
        for module in imported_modules(node, posixpath.dirname(path)):
            for option in module_options(module, bases, index):
                if option in index.files:
                    found.add(option)
    return found


def module_options(module: str, bases: list[str], index: Index) -> list[str]:
    """``odoo.addons.<name>`` is the add-on folder; others sit next to the importer
    or under the repository root or a module root."""
    if module.startswith("/"):  # relative import, already a path
        stems = [module[1:]]
    elif module.startswith("odoo/addons/"):
        name = module.removeprefix("odoo/addons/")
        stems = [posixpath.join(index.addon_paths.get(name.split("/")[0], ""), name)]
    else:
        stems = [posixpath.join(base, module) for base in bases]
    return [f"{stem}{end}" for stem in stems for end in (".py", "/__init__.py")]


def imported_modules(node: ast.AST, folder: str) -> list[str]:
    if isinstance(node, ast.Import):
        return [alias.name.replace(".", "/") for alias in node.names]
    if not isinstance(node, ast.ImportFrom):
        return []
    stem = (node.module or "").replace(".", "/")
    if node.level == 0:
        package = stem
    else:
        base = folder
        for _ in range(node.level - 1):
            base = posixpath.dirname(base)
        package = "/" + (posixpath.join(base, stem) if stem else base)
    return [package] + [posixpath.join(package, alias.name) for alias in node.names]


def conventions(path: str, index: Index) -> set[str]:
    """Edges Odoo, Python packages or the test runner add without naming the file."""
    found: set[str] = set()
    folder = posixpath.dirname(path)
    if path.endswith("/__manifest__.py"):
        for convention in CONVENTION_DIRS:
            found |= {p for p in index.files if p.startswith(f"{folder}/{convention}")}
        found |= {f"{folder}/{name}" for name in CONVENTION_FILES}
    if path.endswith(".py"):
        name = posixpath.basename(path)
        if not name.startswith("test_"):
            found.add(posixpath.join(folder, "test_" + name))
        parts = path.split("/")[:-1]
        found |= {"/".join(parts[: i + 1]) + "/__init__.py" for i in range(len(parts))}
    return found & index.files


def read_text(root: Path, path: str) -> str | None:
    data = (root / path).read_bytes()
    if len(data) > TEXT_LIMIT or b"\0" in data[:4096]:
        return None
    return data.decode("utf-8", errors="replace")


def edges(root: Path, path: str, index: Index) -> set[str]:
    found = conventions(path, index)
    settings = index.settings
    if matches(path, settings["not_sources"]) or matches(path, settings["leaves"]):
        return found - {path}
    text = read_text(root, path)
    if text is None:
        return found - {path}
    folder = posixpath.dirname(path)
    bare = not path.endswith(DATA_SUFFIXES)
    for token in set(TOKEN.findall(text)):
        if "*" not in token or ("/" in token and token.strip("*/")):
            found |= index.resolve(token, folder, bare)
    if path.endswith(".py"):
        found |= python_imports(path, text, index)
    found.discard(path)
    return found


def reach(root: Path, files: list[str]) -> dict[str, str | None]:
    """Breadth-first reach from the roots; value is the file that first reached it."""
    index = Index(files, load_settings(root))
    roots = [path for path in files if matches(path, index.settings["roots"])]
    reached: dict[str, str | None] = dict.fromkeys(roots)
    queue = deque(roots)
    while queue:
        path = queue.popleft()
        for target in sorted(edges(root, path, index)):
            if target not in reached:
                reached[target] = path
                queue.append(target)
    return reached


def orphans(root: Path = ROOT) -> list[str]:
    files = repository_files(root)
    reached = reach(root, files)
    return [path for path in files if path not in reached]


def load_baseline(root: Path) -> list[str]:
    path = root / BASELINE
    if not path.exists():
        return []
    return list(json.loads(path.read_text(encoding="utf-8"))["orphans"])


def write_baseline(root: Path, current: list[str]) -> int:
    grown = sorted(set(current) - set(load_baseline(root)))
    if grown and os.environ.get(OVERRIDE) != "1":
        print(f"orphan baseline would grow by {grown}; set {OVERRIDE}=1 if approved")
        return 1
    text = json.dumps({"orphans": current}, indent=1) + "\n"
    (root / BASELINE).write_text(text, encoding="utf-8")
    print(f"orphan baseline: {len(current)} file(s)")
    return 0


def print_tree(reached: dict[str, str | None]) -> None:
    children: dict[str | None, list[str]] = {}
    for path, parent in reached.items():
        children.setdefault(parent, []).append(path)
    stack = [(path, 0) for path in sorted(children.get(None, []), reverse=True)]
    while stack:
        path, depth = stack.pop()
        print("  " * depth + path)
        later = sorted(children.get(path, []), reverse=True)
        stack.extend((child, depth + 1) for child in later)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--write-baseline", action="store_true")
    parser.add_argument("--list", action="store_true", help="print every orphan")
    parser.add_argument("--tree", action="store_true", help="print the tree")
    arguments = parser.parse_args()
    if arguments.tree:
        print_tree(reach(ROOT, repository_files(ROOT)))
    current = orphans()
    if arguments.list:
        print("\n".join(current))
    if arguments.write_baseline:
        return write_baseline(ROOT, current)
    baseline = load_baseline(ROOT)
    new = sorted(set(current) - set(baseline))
    for path in new:
        print(f"{path}: orphan; link it from the README tree or delete it")
    fixed = sorted(set(baseline) - set(current))
    if fixed:
        print(f"orphan baseline can shrink by {len(fixed)}: run --write-baseline")
    print(f"orphans: {len(current)} ({len(new)} new, baseline {len(baseline)})")
    return 1 if new else 0


if __name__ == "__main__":
    sys.exit(main())
