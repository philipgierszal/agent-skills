#!/usr/bin/env python3
"""Create a deterministic inventory of files that belong to a Git worktree."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path


class InventoryError(RuntimeError):
    """Raised when a repository cannot be inventoried reliably."""


def _decode_path(value: bytes) -> str:
    return value.decode("utf-8", errors="surrogateescape")


def _run_git(repo: Path, *args: str, allow_failure: bool = False) -> bytes:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), *args],
            check=False,
            capture_output=True,
        )
    except OSError as error:
        raise InventoryError(f"Unable to execute Git: {error}") from error

    if result.returncode != 0 and not allow_failure:
        message = result.stderr.decode("utf-8", errors="replace").strip()
        raise InventoryError(message or f"Git command failed: {' '.join(args)}")
    return result.stdout if result.returncode == 0 else b""


def _repository_root(repo: Path) -> Path:
    if not repo.exists() or not repo.is_dir():
        raise InventoryError(f"Repository path is not a directory: {repo}")

    output = _run_git(repo, "rev-parse", "--show-toplevel", allow_failure=True)
    if not output:
        raise InventoryError(f"Path is not inside a Git worktree: {repo}")
    return Path(output.decode("utf-8", errors="surrogateescape").strip()).resolve()


def _nul_paths(output: bytes) -> list[str]:
    return [_decode_path(item) for item in output.split(b"\0") if item]


def _stage_entries(repo: Path) -> dict[str, list[dict[str, object]]]:
    entries: dict[str, list[dict[str, object]]] = {}
    for record in _run_git(repo, "ls-files", "--stage", "-z").split(b"\0"):
        if not record or b"\t" not in record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        fields = metadata.split()
        if len(fields) < 3:
            continue
        path = _decode_path(raw_path)
        entries.setdefault(path, []).append(
            {
                "mode": fields[0].decode("ascii", errors="replace"),
                "object": fields[1].decode("ascii", errors="replace"),
                "stage": int(fields[2]),
            }
        )
    for stages in entries.values():
        stages.sort(key=lambda entry: int(entry["stage"]))
    return entries


def _head_entries(repo: Path) -> dict[str, dict[str, str]]:
    entries: dict[str, dict[str, str]] = {}
    output = _run_git(repo, "ls-tree", "-r", "-z", "HEAD", allow_failure=True)
    for record in output.split(b"\0"):
        if not record or b"\t" not in record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        fields = metadata.split()
        if len(fields) < 3:
            continue
        entries[_decode_path(raw_path)] = {
            "mode": fields[0].decode("ascii", errors="replace"),
            "object": fields[2].decode("ascii", errors="replace"),
        }
    return entries


def _sha256(path: Path, kind: str) -> str | None:
    if kind in {"missing", "submodule"}:
        return None

    digest = hashlib.sha256()
    try:
        if kind == "symlink":
            digest.update(os.readlink(path).encode("utf-8", errors="surrogateescape"))
        else:
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
    except OSError as error:
        raise InventoryError(f"Cannot hash {path}: {error}") from error
    return digest.hexdigest()


def _submodule_state(path: Path) -> tuple[bool, str | None, bool | None]:
    git_marker = path / ".git"
    if not path.is_dir() or not (git_marker.is_file() or git_marker.is_dir()):
        return False, None, None

    head_output = _run_git(path, "rev-parse", "--verify", "HEAD", allow_failure=True)
    if not head_output:
        return False, None, None
    head = head_output.decode("ascii", errors="replace").rstrip("\r\n")
    dirty = bool(
        _run_git(
            path,
            "status",
            "--porcelain=v1",
            "-z",
            "--untracked-files=normal",
            allow_failure=True,
        )
    )
    return True, head, dirty


def build_inventory(repo: Path) -> dict[str, object]:
    """Return a stable inventory of tracked and non-ignored untracked paths."""

    root = _repository_root(repo.resolve())
    tracked = set(_nul_paths(_run_git(root, "ls-files", "--cached", "-z")))
    untracked = set(_nul_paths(_run_git(root, "ls-files", "--others", "--exclude-standard", "-z")))
    index_entries = _stage_entries(root)
    head_entries = _head_entries(root)
    paths = tracked | untracked | set(index_entries) | set(head_entries)

    files: list[dict[str, object]] = []
    for relative_path in sorted(paths):
        path = root / Path(relative_path)
        stages = index_entries.get(relative_path, [])
        stage_zero = next((entry for entry in stages if entry["stage"] == 0), None)
        head_entry = head_entries.get(relative_path)
        selected_entry = stage_zero or head_entry
        mode = selected_entry["mode"] if selected_entry else None
        git_object = selected_entry["object"] if selected_entry else None
        is_conflicted = any(entry["stage"] != 0 for entry in stages)
        exists = path.exists() or path.is_symlink()

        if is_conflicted:
            index_status = "conflicted"
        elif stage_zero:
            index_status = "tracked"
        else:
            index_status = "absent"
        worktree_status = "present" if exists else "missing"

        if not exists:
            kind = "missing"
            size_bytes = None
        elif mode == "160000":
            kind = "submodule"
            size_bytes = None
        elif path.is_symlink():
            kind = "symlink"
            try:
                size_bytes = path.lstat().st_size
            except OSError as error:
                raise InventoryError(f"Cannot inspect {path}: {error}") from error
        elif mode == "120000":
            kind = "symlink-materialized"
            try:
                size_bytes = path.stat().st_size
            except OSError as error:
                raise InventoryError(f"Cannot inspect {path}: {error}") from error
        else:
            kind = "file"
            try:
                size_bytes = path.stat().st_size
            except OSError as error:
                raise InventoryError(f"Cannot inspect {path}: {error}") from error

        if mode == "160000":
            submodule_initialized, submodule_head, submodule_dirty = _submodule_state(path)
        else:
            submodule_initialized, submodule_head, submodule_dirty = None, None, None

        files.append(
            {
                "path": relative_path,
                "tracked": relative_path in tracked,
                "tracked_at_head": relative_path in head_entries,
                "git_mode": mode,
                "git_object": git_object,
                "index_stages": stages,
                "index_status": index_status,
                "head_entry": head_entry,
                "worktree_status": worktree_status,
                "kind": kind,
                "size_bytes": size_bytes,
                "sha256": _sha256(path, kind),
                "submodule_initialized": submodule_initialized,
                "submodule_head": submodule_head,
                "submodule_dirty": submodule_dirty,
            }
        )

    revision_output = _run_git(root, "rev-parse", "HEAD", allow_failure=True)
    revision = revision_output.decode("ascii", errors="replace").strip() or None
    dirty = bool(_run_git(root, "status", "--porcelain=v1", "-z", "--untracked-files=normal"))
    inventory_digest = hashlib.sha256(
        json.dumps(files, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")
    ).hexdigest()

    return {
        "inventory_version": 1,
        "inventory_digest": inventory_digest,
        "path_encoding": "utf-8 with surrogateescape serialized as JSON escapes",
        "repository_root": root.as_posix(),
        "revision": revision,
        "dirty": dirty,
        "scope": "HEAD/index-tracked plus non-ignored untracked paths",
        "files": files,
    }


def write_inventory(repo: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(build_inventory(repo), indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd(), help="Path inside the Git worktree")
    parser.add_argument("--output", type=Path, required=True, help="Output JSON path")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        write_inventory(args.repo, args.output)
    except InventoryError as error:
        print(f"inventory error: {error}", file=sys.stderr)
        return 2
    print(f"Inventory written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
