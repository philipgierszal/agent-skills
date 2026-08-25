from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import unittest
from pathlib import Path
from urllib.parse import unquote

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "architecture-hygiene-audit"
EXAMPLE = ROOT / "examples" / "architecture-hygiene-audit"
VALIDATOR = SKILL / "scripts" / "validate_ledger.py"
MARKDOWN_LINK = re.compile(r"\[[^]]*\]\(([^)]+)\)")


def load_validator_module():
    spec = importlib.util.spec_from_file_location(
        "architecture_hygiene_validator",
        VALIDATOR,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load validator module at {VALIDATOR}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", maxsplit=2)
    if len(parts) != 3 or parts[0].strip():
        raise AssertionError(f"{path} must start with YAML frontmatter")

    value = yaml.safe_load(parts[1])
    if not isinstance(value, dict):
        raise TypeError(f"{path} frontmatter must be a mapping")
    return value


class SkillPackageTests(unittest.TestCase):
    def test_shebang_scripts_are_executable_in_git(self) -> None:
        scripts = sorted((SKILL / "scripts").glob("*.py"))
        self.assertTrue(scripts)

        for script in scripts:
            relative = script.relative_to(ROOT).as_posix()
            result = subprocess.run(
                ["git", "ls-files", "--stage", "--", relative],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            mode = result.stdout.split(maxsplit=1)[0]

            with self.subTest(script=relative):
                self.assertTrue(script.read_text(encoding="utf-8").startswith("#!"))
                self.assertEqual("100755", mode)

    def test_dev_requirements_pin_yaml_parser(self) -> None:
        requirements = (ROOT / "requirements-dev.txt").read_text(encoding="utf-8").splitlines()

        self.assertIn("PyYAML==6.0.3", requirements)

    def test_stable_skills_have_codex_compatible_metadata(self) -> None:
        skill_files = sorted((ROOT / "skills").glob("*/SKILL.md"))
        self.assertTrue(skill_files)

        for skill_file in skill_files:
            frontmatter = load_frontmatter(skill_file)
            metadata = frontmatter.get("metadata")

            with self.subTest(skill=skill_file.parent.name):
                self.assertEqual(skill_file.parent.name, frontmatter.get("name"))
                self.assertIsInstance(frontmatter.get("description"), str)
                self.assertTrue(str(frontmatter.get("description", "")).strip())
                self.assertEqual("MIT", frontmatter.get("license"))
                self.assertNotIn("compatibility", frontmatter)
                self.assertIsInstance(metadata, dict)
                if not isinstance(metadata, dict):
                    self.fail("metadata must be a mapping")
                self.assertEqual("philipgierszal", metadata.get("author"))
                self.assertRegex(
                    str(metadata.get("compatibility", "")),
                    r"Git.*Python 3\.10\+",
                )

    def test_skill_markdown_relative_links_resolve(self) -> None:
        markdown_files = sorted(SKILL.rglob("*.md"))
        self.assertTrue(markdown_files)

        for markdown_file in markdown_files:
            text = markdown_file.read_text(encoding="utf-8")
            for match in MARKDOWN_LINK.finditer(text):
                raw_target = match.group(1).strip().split(maxsplit=1)[0].strip("<>")
                if raw_target.startswith(("#", "https://", "http://", "mailto:")):
                    continue
                target = unquote(raw_target.split("#", maxsplit=1)[0])
                with self.subTest(source=markdown_file, target=target):
                    self.assertTrue((markdown_file.parent / target).exists())

    def test_public_community_files_exist(self) -> None:
        for relative in (
            "AGENTS.md",
            "CONTRIBUTING.md",
            "SECURITY.md",
            ".github/ISSUE_TEMPLATE/bug.yml",
            ".github/ISSUE_TEMPLATE/skill-proposal.yml",
            ".github/PULL_REQUEST_TEMPLATE.md",
            ".github/workflows/validate.yml",
        ):
            with self.subTest(path=relative):
                self.assertTrue((ROOT / relative).is_file(), relative)

    def test_example_is_reconciled_by_bundled_validator(self) -> None:
        required = (
            "README.md",
            ".architecture-hygiene.yml",
            "inventory.json",
            "ledger.json",
            "report.md",
        )
        for filename in required:
            self.assertTrue((EXAMPLE / filename).is_file(), filename)

        inventory = json.loads((EXAMPLE / "inventory.json").read_text(encoding="utf-8"))
        ledger = json.loads((EXAMPLE / "ledger.json").read_text(encoding="utf-8"))

        load_validator_module().validate(inventory, ledger)


if __name__ == "__main__":
    unittest.main()
