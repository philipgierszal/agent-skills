from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "agent-instructions" / "install.py"


def load():
    spec = importlib.util.spec_from_file_location("agent_instructions_install", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class WithBlockTests(unittest.TestCase):
    def setUp(self) -> None:
        self.m = load()

    def test_appends_block_and_keeps_own_text(self) -> None:
        out = self.m.with_block("# Mine\n\nkeep me\n", "rules v1")
        self.assertIn("keep me", out)
        self.assertIn("rules v1", out)
        self.assertTrue(out.index("keep me") < out.index(self.m.START))

    def test_rerun_replaces_only_the_block(self) -> None:
        once = self.m.with_block("# Mine\n", "rules v1")
        twice = self.m.with_block(once + "\nafter\n", "rules v2")
        self.assertNotIn("rules v1", twice)
        self.assertIn("rules v2", twice)
        self.assertIn("after", twice)
        self.assertEqual(twice.count(self.m.START), 1)

    def test_empty_file_gets_only_the_block(self) -> None:
        self.assertTrue(self.m.with_block("", "x").startswith(self.m.START))


if __name__ == "__main__":
    unittest.main()
