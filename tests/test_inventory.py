from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

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
        capture_output=True,
    )


class InventoryTests(unittest.TestCase):
    def test_path_decoder_preserves_backslash_bytes(self) -> None:
        inventory = load_inventory_module()
        self.assertEqual(inventory._decode_path(b"module\\name.py"), "module\\name.py")

    def test_writer_serializes_surrogateescaped_path_bytes(self) -> None:
        inventory = load_inventory_module()

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "inventory.json"
            decoded_name = "invalid-\udcff.py"
            payload = {"inventory_version": 1, "files": [{"path": decoded_name}]}
            with mock.patch.object(inventory, "build_inventory", return_value=payload):
                inventory.write_inventory(Path(directory), output)

            restored = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(restored["files"][0]["path"], decoded_name)

    @unittest.skipIf(os.name == "nt", "Windows filenames cannot contain backslashes")
    def test_distinguishes_posix_backslash_name_from_directory_separator(self) -> None:
        inventory = load_inventory_module()

        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            run_git(repo, "init", "-b", "main")
            run_git(repo, "config", "user.name", "Audit Test")
            run_git(repo, "config", "user.email", "audit@example.test")
            (repo / "a").mkdir()
            (repo / "a\\b.txt").write_text("backslash\n", encoding="utf-8")
            (repo / "a" / "b.txt").write_text("separator\n", encoding="utf-8")
            run_git(repo, "add", "--all")
            run_git(repo, "commit", "-m", "fixture")

            paths = {entry["path"] for entry in inventory.build_inventory(repo)["files"]}
            self.assertEqual(paths, {"a\\b.txt", "a/b.txt"})

    @unittest.skipIf(os.name == "nt", "Windows filenames must be valid Unicode")
    def test_serializes_non_utf8_posix_path_bytes(self) -> None:
        inventory = load_inventory_module()

        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "repo"
            repo.mkdir()
            run_git(repo, "init", "-b", "main")
            run_git(repo, "config", "user.name", "Audit Test")
            run_git(repo, "config", "user.email", "audit@example.test")
            decoded_name = os.fsdecode(b"invalid-\xff.py")
            (repo / decoded_name).write_bytes(b"print('ok')\n")
            run_git(repo, "add", decoded_name)
            run_git(repo, "commit", "-m", "non-utf8 fixture")
            output = Path(directory) / "inventory.json"

            inventory.write_inventory(repo, output)
            payload = json.loads(output.read_text(encoding="utf-8"))

            self.assertEqual(payload["files"][0]["path"], decoded_name)

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

    def test_inventory_digest_changes_when_content_changes_at_same_revision(self) -> None:
        inventory = load_inventory_module()

        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            run_git(repo, "init", "-b", "main")
            run_git(repo, "config", "user.name", "Audit Test")
            run_git(repo, "config", "user.email", "audit@example.test")
            path = repo / "same-size.txt"
            path.write_text("one\n", encoding="utf-8")
            run_git(repo, "add", "same-size.txt")
            run_git(repo, "commit", "-m", "fixture")

            before = inventory.build_inventory(repo)
            path.write_text("two\n", encoding="utf-8")
            after = inventory.build_inventory(repo)

            self.assertEqual(before["revision"], after["revision"])
            self.assertNotEqual(before["inventory_digest"], after["inventory_digest"])

    def test_represents_staged_and_unstaged_deleted_tracked_paths(self) -> None:
        inventory = load_inventory_module()

        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            run_git(repo, "init", "-b", "main")
            run_git(repo, "config", "user.name", "Audit Test")
            run_git(repo, "config", "user.email", "audit@example.test")
            (repo / "staged.txt").write_text("staged\n", encoding="utf-8")
            (repo / "unstaged.txt").write_text("unstaged\n", encoding="utf-8")
            run_git(repo, "add", "staged.txt", "unstaged.txt")
            run_git(repo, "commit", "-m", "fixture")

            (repo / "unstaged.txt").unlink()
            run_git(repo, "rm", "staged.txt")

            files = {
                entry["path"]: entry for entry in inventory.build_inventory(repo)["files"]
            }
            self.assertEqual(set(files), {"staged.txt", "unstaged.txt"})
            self.assertEqual(files["staged.txt"]["worktree_status"], "missing")
            self.assertEqual(files["unstaged.txt"]["worktree_status"], "missing")
            self.assertFalse(files["staged.txt"]["tracked"])
            self.assertTrue(files["unstaged.txt"]["tracked"])
            self.assertTrue(files["staged.txt"]["tracked_at_head"])
            self.assertTrue(files["unstaged.txt"]["tracked_at_head"])
            self.assertTrue(files["staged.txt"]["git_object"])
            self.assertTrue(files["unstaged.txt"]["git_object"])
            self.assertIsNone(files["staged.txt"]["sha256"])
            self.assertIsNone(files["unstaged.txt"]["sha256"])

    def test_represents_unmerged_index_stages(self) -> None:
        inventory = load_inventory_module()

        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            run_git(repo, "init", "-b", "main")
            run_git(repo, "config", "user.name", "Audit Test")
            run_git(repo, "config", "user.email", "audit@example.test")
            path = repo / "conflict.txt"
            path.write_text("base\n", encoding="utf-8")
            run_git(repo, "add", "conflict.txt")
            run_git(repo, "commit", "-m", "base")
            run_git(repo, "checkout", "-b", "side")
            path.write_text("side\n", encoding="utf-8")
            run_git(repo, "commit", "-am", "side")
            run_git(repo, "checkout", "main")
            path.write_text("main\n", encoding="utf-8")
            run_git(repo, "commit", "-am", "main")
            merge = subprocess.run(
                ["git", "-C", str(repo), "merge", "side"],
                check=False,
                capture_output=True,
            )
            self.assertNotEqual(merge.returncode, 0)

            entry = next(
                item
                for item in inventory.build_inventory(repo)["files"]
                if item["path"] == "conflict.txt"
            )
            self.assertEqual(entry["index_status"], "conflicted")
            self.assertEqual(entry["worktree_status"], "present")
            self.assertEqual(
                {stage["stage"] for stage in entry["index_stages"]},
                {1, 2, 3},
            )

            path.unlink()
            missing_entry = next(
                item
                for item in inventory.build_inventory(repo)["files"]
                if item["path"] == "conflict.txt"
            )
            self.assertEqual(missing_entry["index_status"], "conflicted")
            self.assertEqual(missing_entry["worktree_status"], "missing")
            self.assertEqual(missing_entry["kind"], "missing")
            self.assertIsNone(missing_entry["size_bytes"])
            self.assertIsNone(missing_entry["sha256"])

    def test_hashes_git_symlink_materialized_as_regular_file(self) -> None:
        inventory = load_inventory_module()

        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            run_git(repo, "init", "-b", "main")
            run_git(repo, "config", "user.name", "Audit Test")
            run_git(repo, "config", "user.email", "audit@example.test")
            (repo / "link").write_text("target.txt", encoding="utf-8")
            blob = subprocess.run(
                ["git", "-C", str(repo), "hash-object", "-w", "--stdin"],
                input=b"target.txt",
                check=True,
                capture_output=True,
            ).stdout.decode("ascii").strip()
            run_git(repo, "update-index", "--add", "--cacheinfo", "120000", blob, "link")
            run_git(repo, "commit", "-m", "symlink fixture")

            entry = inventory.build_inventory(repo)["files"][0]
            self.assertEqual(entry["git_mode"], "120000")
            self.assertEqual(entry["kind"], "symlink-materialized")
            self.assertEqual(entry["worktree_status"], "present")
            self.assertEqual(entry["sha256"], hashlib.sha256(b"target.txt").hexdigest())

    def test_hashes_actual_symlink_target_without_following_it(self) -> None:
        inventory = load_inventory_module()

        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            run_git(repo, "init", "-b", "main")
            run_git(repo, "config", "user.name", "Audit Test")
            run_git(repo, "config", "user.email", "audit@example.test")
            (repo / "target.txt").write_text("secret target contents\n", encoding="utf-8")
            try:
                os.symlink("target.txt", repo / "link")
            except OSError as error:
                self.skipTest(f"OS symlink creation unavailable: {error}")
            run_git(repo, "add", "target.txt", "link")
            run_git(repo, "commit", "-m", "symlink fixture")

            entry = next(
                item for item in inventory.build_inventory(repo)["files"] if item["path"] == "link"
            )
            self.assertEqual(entry["kind"], "symlink")
            self.assertEqual(entry["sha256"], hashlib.sha256(b"target.txt").hexdigest())

    def test_represents_present_gitlink_as_submodule(self) -> None:
        inventory = load_inventory_module()

        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            run_git(repo, "init", "-b", "main")
            run_git(repo, "config", "user.name", "Audit Test")
            run_git(repo, "config", "user.email", "audit@example.test")
            (repo / "root.txt").write_text("root\n", encoding="utf-8")
            run_git(repo, "add", "root.txt")
            run_git(repo, "commit", "-m", "root")
            head = subprocess.run(
                ["git", "-C", str(repo), "rev-parse", "HEAD"],
                check=True,
                capture_output=True,
            ).stdout.decode("ascii").strip()
            run_git(
                repo,
                "update-index",
                "--add",
                "--cacheinfo",
                "160000",
                head,
                "vendor/module",
            )
            run_git(repo, "commit", "-m", "gitlink fixture")
            (repo / "vendor" / "module").mkdir(parents=True)

            entry = next(
                item
                for item in inventory.build_inventory(repo)["files"]
                if item["path"] == "vendor/module"
            )
            self.assertEqual(entry["kind"], "submodule")
            self.assertEqual(entry["git_mode"], "160000")
            self.assertIsNone(entry["sha256"])

    def test_inventory_digest_captures_initialized_submodule_drift(self) -> None:
        inventory = load_inventory_module()

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            child = root / "child"
            repo = root / "super"
            child.mkdir()
            repo.mkdir()
            run_git(child, "init", "-b", "main")
            run_git(child, "config", "user.name", "Audit Test")
            run_git(child, "config", "user.email", "audit@example.test")
            (child / "lib.txt").write_text("clean\n", encoding="utf-8")
            run_git(child, "add", "lib.txt")
            run_git(child, "commit", "-m", "child fixture")
            run_git(repo, "init", "-b", "main")
            run_git(repo, "config", "user.name", "Audit Test")
            run_git(repo, "config", "user.email", "audit@example.test")
            run_git(
                repo,
                "-c",
                "protocol.file.allow=always",
                "submodule",
                "add",
                str(child),
                "vendor/module",
            )
            run_git(repo, "commit", "-m", "super fixture")

            before = inventory.build_inventory(repo)
            (repo / "vendor" / "module" / "lib.txt").write_text(
                "dirty\n", encoding="utf-8"
            )
            after = inventory.build_inventory(repo)
            before_entry = next(
                item for item in before["files"] if item["path"] == "vendor/module"
            )
            after_entry = next(
                item for item in after["files"] if item["path"] == "vendor/module"
            )

            self.assertEqual(before["revision"], after["revision"])
            self.assertFalse(before_entry["submodule_dirty"])
            self.assertTrue(after_entry["submodule_dirty"])
            self.assertEqual(before_entry["submodule_head"], after_entry["submodule_head"])
            self.assertNotEqual(before["inventory_digest"], after["inventory_digest"])

    def test_rejects_non_git_directory(self) -> None:
        inventory = load_inventory_module()

        with (
            tempfile.TemporaryDirectory() as directory,
            self.assertRaisesRegex(inventory.InventoryError, "Git worktree"),
        ):
            inventory.build_inventory(Path(directory))


if __name__ == "__main__":
    unittest.main()
