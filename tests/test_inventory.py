from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "architecture-hygiene-audit" / "scripts" / "inventory.py"


def load_inventory_module():
    spec = importlib.util.spec_from_file_location("architecture_hygiene_inventory", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load inventory module at {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


class InventoryTests(unittest.TestCase):
    def test_inventories_tracked_and_nonignored_untracked_paths(self) -> None:
        inventory = load_inventory_module()

        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            run_git(repo, "init", "-b", "main")
            run_git(repo, "config", "user.name", "Audit Test")
            run_git(repo, "config", "user.email", "audit@example.test")

            (repo / "docs").mkdir()
            (repo / "src").mkdir()
            (repo / "build").mkdir()
            (repo / "docs" / "żółć note.md").write_text("evidence\n", encoding="utf-8")
            (repo / "src" / "main file.py").write_text("print('main')\n", encoding="utf-8")
            (repo / ".gitignore").write_text("build/\n", encoding="utf-8")
            run_git(repo, "add", "docs/żółć note.md", "src/main file.py", ".gitignore")
            run_git(repo, "commit", "-m", "fixture")

            (repo / "src" / "untracked.py").write_text("VALUE = 1\n", encoding="utf-8")
            (repo / "build" / "ignored.py").write_text("ignored = True\n", encoding="utf-8")

            result = inventory.build_inventory(repo)
            paths = [entry["path"] for entry in result["files"]]

            self.assertEqual(
                paths,
                sorted([".gitignore", "docs/żółć note.md", "src/main file.py", "src/untracked.py"]),
            )
            self.assertNotIn("build/ignored.py", paths)
            self.assertEqual(result["inventory_version"], 1)
            self.assertTrue(result["revision"])
            self.assertTrue(result["dirty"])
            self.assertTrue(all(entry["sha256"] for entry in result["files"]))
            self.assertEqual(
                {entry["path"]: entry["tracked"] for entry in result["files"]},
                {
                    ".gitignore": True,
                    "docs/żółć note.md": True,
                    "src/main file.py": True,
                    "src/untracked.py": False,
                },
            )

    def test_inventory_is_stable_across_repeated_runs(self) -> None:
        inventory = load_inventory_module()

        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            run_git(repo, "init", "-b", "main")
            run_git(repo, "config", "user.name", "Audit Test")
            run_git(repo, "config", "user.email", "audit@example.test")
            (repo / "a.txt").write_text("same\n", encoding="utf-8")
            run_git(repo, "add", "a.txt")
            run_git(repo, "commit", "-m", "fixture")

            self.assertEqual(inventory.build_inventory(repo), inventory.build_inventory(repo))

    def test_rejects_non_git_directory(self) -> None:
        inventory = load_inventory_module()

        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(inventory.InventoryError, "Git worktree"):
                inventory.build_inventory(Path(directory))


if __name__ == "__main__":
    unittest.main()
