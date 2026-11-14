# token-usage-review: evaluation record

## 2026-11-14, first real run

- Ran `usage_report.py` over a 24-hour and a 120-hour window of one workstation's Claude Code transcripts (about 160 transcripts, 15,800 steps) and its Codex logs, with line counts from four repositories.
- Run time under 3 seconds. Totals matched an earlier one-off analysis of the same transcripts within a few percent. The remaining gap comes from Opus 5.5's cache-read price ($0.20, 5% of input) replacing the earlier flat 10% weight.
- The flags named the runs a human review had already singled out: long slice subagents, a main session over 300 steps, and read-only subagents on Opus.
- Limits: list prices, not the bill; Haiku 5.5's cache-read price is estimated; line counts include formatting and generated files; Codex sessions are counted by file modification time.

Unit tests (`tests/test_usage_report.py`) cover only the pure functions: tool classification, price lookup and cost. Parsing is checked by running the script on real logs, not on invented transcripts.
