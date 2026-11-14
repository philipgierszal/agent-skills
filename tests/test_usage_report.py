from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "skills" / "token-usage-review" / "scripts" / "usage_report.py"


def load():
    spec = importlib.util.spec_from_file_location("usage_report", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class UsageReportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.m = load()

    def test_classify_tools_and_commands(self) -> None:
        c = self.m.classify
        self.assertEqual(c("Read"), "read")
        self.assertEqual(c("Edit"), "write")
        self.assertEqual(c("Agent"), "delegate")
        self.assertEqual(c("Bash", "git log --oneline -5"), "read")
        self.assertEqual(c("Bash", "git commit -m x"), "write")
        self.assertEqual(c("Bash", "python -m pytest tests"), "verify")
        self.assertEqual(c("Bash", "docker compose up -d"), "run")

    def test_price_prefers_the_most_specific_model(self) -> None:
        self.assertEqual(self.m.price("claude-opus-5-5"), (4.0, 20.0, 0.20))
        self.assertEqual(self.m.price("claude-haiku-5-5"), (0.10, 0.50, 0.01))
        self.assertEqual(self.m.price("claude-sonnet-4-6"), (3.0, 15.0, 0.30))

    def test_cost_counts_cache_writes_at_a_quarter_above_input(self) -> None:
        cost = self.m.cost_usd("claude-opus-5-5", 1_000_000, 1_000_000, 1_000_000, 1_000_000)
        self.assertAlmostEqual(cost, 4.0 + 5.0 + 0.20 + 20.0)


if __name__ == "__main__":
    unittest.main()
