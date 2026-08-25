#!/usr/bin/env python3
"""Create a deterministic inventory of files that belong to a Git worktree."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Sequence


class InventoryError(RuntimeError):
    """Raised when a repository cannot be inventoried reliably."""


def _decode_path(value: bytes) -> str:
    return value.decode("utf-8", errors="surrogateescape")


def _run_git(repo: Path, *args: str, allow_failure: bool = False) -> bytes:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), *args],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
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


def _stage_modes(repo: Path) -> dict[str, str]:
    modes: dict[str, str] = {}
    for record in _run_git(repo, "ls-files", "--stage", "-z").split(b"\0"):
        if not record or b"\t" not in record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        fields = metadata.split()
        if fields:
            modes[_decode_path(raw_path)] = fields[0].decode("ascii", errors="replace")
    return modes


def _sha256(path: Path, kind: str) -> str | None:
    if kind == "submodule":
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


def build_inventory(repo: Path) -> dict[str, object]:
    """Return a stable inventory of tracked and non-ignored untracked paths."""

    root = _repository_root(repo.resolve())
    tracked = set(_nul_paths(_run_git(root, "ls-files", "--cached", "-z")))
    paths = _nul_paths(
        _run_git(root, "ls-files", "--cached", "--others", "--exclude-standard", "-z")
    )
    modes = _stage_modes(root)

    files: list[dict[str, object]] = []
    for relative_path in sorted(set(paths)):
        path = root / Path(relative_path)
        mode = modes.get(relative_path)
        if mode == "160000":
            kind = "submodule"
            size_bytes = None
        elif mode == "120000" or path.is_symlink():
            kind = "symlink"
            try:
                size_bytes = path.lstat().st_size
            except OSError as error:
                raise InventoryError(f"Cannot inspect {path}: {error}") from error
        else:
            kind = "file"
            try:
                size_bytes = path.stat().st_size
            except OSError as error:
                raise InventoryError(f"Cannot inspect {path}: {error}") from error

        files.append(
            {
                "path": relative_path,
                "tracked": relative_path in tracked,
                "git_mode": mode,
                "kind": kind,
                "size_bytes": size_bytes,
                "sha256": _sha256(path, kind),
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
        "repository_root": root.as_posix(),
        "revision": revision,
        "dirty": dirty,
        "scope": "git-tracked plus non-ignored untracked paths",
        "files": files,
    }


def write_inventory(repo: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(build_inventory(repo), indent=2, ensure_ascii=False) + "\n",
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
