"""Orphan-file ratchet: every repository file must be reachable from
the entry points (README.md by default) through references, so the README is a tree
that reaches every file. One identical copy per repository; settings live under the
"orphans" key of scripts/code_health.json or scripts/orphans.json (first one found):

    "orphans": {"roots": [...], "leaves": [...], "module_roots": ["src"],
                "allowed": ["path or glob", ...]}

A reference is a Markdown link, a path written in any text file (relative to the file
or to the repository root, globs included), a unique file name with an extension, or
a Python import. A directory reference reaches only the directory's README.md
(index.md, SKILL.md); name the files of a directory that has none. A reached module
also reaches its packages' __init__.py.
"roots" are entry points: files found by convention (pytest, Alembic, git, tools).
"leaves" (tests) reach only what they import: a test that reads a document does not
index it, so documents stay reachable from the README tree.

    python scripts/orphans.py           # gate; run by the repo check
    python scripts/orphans.py --tree    # print the reference tree from the roots
"""

from __future__ import annotations

import argparse
import ast
import fnmatch
import json
import posixpath
import re
import subprocess
import sys
from collections import defaultdict, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SETTINGS = [ROOT / "scripts" / name for name in ("code_health.json", "orphans.json")]
TOKEN = re.compile(r"[\w.*\-/]+")
TEXT_LIMIT = 2_000_000
INDEXES = ("README.md", "index.md", "SKILL.md")


def repository_files() -> list[str]:
    """Tracked and untracked non-ignored files: a new orphan fails before commit."""
    command = ("git", "ls-files", "-z", "--cached", "--others", "--exclude-standard")
    output = subprocess.run(  # noqa: S603 - local Git argv; never a shell
        command,
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout.decode("utf-8")
    return sorted({p for p in output.split("\0") if p and (ROOT / p).is_file()})


def read_text(path: str) -> str | None:
    data = (ROOT / path).read_bytes()
    if len(data) > TEXT_LIMIT or b"\0" in data[:4096]:
        return None
    return data.decode("utf-8", errors="replace")


class Index:
    """Lookups from a written reference to repository files."""

    def __init__(self, files: list[str], leaves: list[str]) -> None:
        self.files = set(files)
        self.leaves = leaves
        names: dict[str, list[str]] = defaultdict(list)
        for path in files:
            names[posixpath.basename(path)].append(path)
        self.unique = {n: p[0] for n, p in names.items() if len(p) == 1 and "." in n}
        self.directories = {posixpath.dirname(p) for p in files} | {
            d for p in files for d in parents(p)
        }

    def directory(self, path: str) -> list[str]:
        index = [f"{path}/{name}" for name in INDEXES if f"{path}/{name}" in self.files]
        return index[:1]

    def resolve(self, token: str, base: str) -> list[str]:
        token = token.strip(",:;'\"`)(").rstrip(".").removeprefix("./")
        if not token.strip("*/-") or token.startswith("//"):
            return []
        if "*" in token and ("/" not in token or "**" in token):
            return []  # a bare or recursive glob names no particular file
        found: list[str] = []
        for start in {base, ""}:
            candidate = posixpath.normpath(posixpath.join(start, token.lstrip("/")))
            found += self.match(candidate)
        if not found and token in self.unique:
            found.append(self.unique[token])
        return found

    def match(self, candidate: str) -> list[str]:
        if candidate.startswith("..") or candidate == ".":
            return []
        if "*" in candidate:
            pattern = re.compile(re.escape(candidate).replace(r"\*", "[^/]*") + "$")
            return [f for f in self.files if pattern.match(f)]
        if candidate in self.files:
            return [candidate]
        if candidate.rstrip("/") in self.directories:
            return self.directory(candidate.rstrip("/"))
        return []


def parents(path: str) -> list[str]:
    parts = path.split("/")[:-1]
    return ["/".join(parts[: i + 1]) for i in range(len(parts))]


def module_files(index: Index, module_roots: list[str]) -> dict[str, str]:
    """Dotted module name -> file, from the top level and from each module root."""
    modules: dict[str, str] = {}
    for path in sorted(index.files):
        if not path.endswith(".py"):
            continue
        dotted = path.removesuffix(".py").removesuffix("/__init__").replace("/", ".")
        modules[dotted] = path
        for root in module_roots:
            if dotted.startswith(f"{root}."):
                modules.setdefault(dotted.removeprefix(f"{root}."), path)
    return modules


def python_imports(path: str, text: str, modules: dict[str, str]) -> list[str]:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return []
    package = path.removesuffix(".py").replace("/", ".").rsplit(".", 1)[0]
    found: list[str] = []
    for node in ast.walk(tree):
        names: list[str] = []
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            base = package.rsplit(".", node.level - 1)[0] if node.level else ""
            module = ".".join(p for p in (base, node.module or "") if p)
            names = [module] + [f"{module}.{alias.name}" for alias in node.names]
        for name in names:
            name = name.removeprefix("odoo.addons.")  # Odoo add-on import path
            if name in modules:
                found.append(modules[name])
    return found


def references(path: str, index: Index, modules: dict[str, str]) -> set[str]:
    text = read_text(path)
    if text is None:
        return set()
    base = posixpath.dirname(path)
    found: set[str] = set()
    if not matches(path, index.leaves):
        found = {f for token in TOKEN.findall(text) for f in index.resolve(token, base)}
    if path.endswith(".py"):
        found.update(python_imports(path, text, modules))
    for target in [t for t in found if t.endswith(".py")]:
        found.update(f"{directory}/__init__.py" for directory in parents(target))
    return (found & index.files) - {path}


def walk(
    roots: list[str], index: Index, modules: dict[str, str]
) -> dict[str, str | None]:
    """Breadth-first reach from the roots; value is the file that first reached it."""
    reached: dict[str, str | None] = dict.fromkeys(roots)
    queue = deque(roots)
    while queue:
        path = queue.popleft()
        for target in sorted(references(path, index, modules)):
            if target not in reached:
                reached[target] = path
                queue.append(target)
    return reached


def matches(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatchcase(path, pattern) for pattern in patterns)


def print_tree(reached: dict[str, str | None]) -> None:
    children: dict[str | None, list[str]] = defaultdict(list)
    for path, parent in reached.items():
        children[parent].append(path)
    stack = [(path, 0) for path in sorted(children[None], reverse=True)]
    while stack:
        path, depth = stack.pop()
        print("  " * depth + path)
        stack.extend((c, depth + 1) for c in sorted(children[path], reverse=True))


def load_settings() -> dict[str, list[str]]:
    """The "orphans" object of the first settings file that has one."""
    for path in SETTINGS:
        if path.is_file():
            data = json.loads(path.read_text(encoding="utf-8"))
            if "orphans" in data:
                return dict(data["orphans"])
    return {}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tree", action="store_true", help="print the reference tree")
    args = parser.parse_args()
    settings = load_settings()
    files = repository_files()
    roots = [f for f in files if matches(f, settings.get("roots", ["README.md"]))]
    index = Index(files, settings.get("leaves", []))
    modules = module_files(index, settings.get("module_roots", ["src"]))
    reached = walk(roots, index, modules)
    if args.tree:
        print_tree(reached)
    allowed = settings.get("allowed", [])
    orphans = [f for f in files if f not in reached and not matches(f, allowed)]
    for path in orphans:
        print(f"orphan: {path} - link it from a document that is reached, or delete it")
    print(
        f"orphans: {len(files)} files, {len(reached)} reached, {len(orphans)} orphans"
    )
    return 1 if orphans else 0


if __name__ == "__main__":
    sys.exit(main())
