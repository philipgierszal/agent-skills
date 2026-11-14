---
name: token-usage-review
description: Use when asked where coding-agent tokens went, to run a daily or after-batch token review, to compare Claude Code and Codex usage, or to choose which model and effort level to use for a kind of work.
license: MIT
metadata:
  author: philipgierszal
  compatibility: Requires Git and Python 3.10+; reads local Claude Code transcripts (~/.claude/projects) and Codex session logs (~/.codex/sessions).
---

# Token Usage Review

Find out where the tokens went, what came out of them, and what to change next time. Read-only: the script never edits transcripts or repositories.

## 1. Run the report

```bash
python <skill-dir>/scripts/usage_report.py --hours 24 --repo <repo> [--repo <repo> ...]
```

- `--hours` sets the window (24 for a daily review; the length of the batch otherwise).
- `--match <text>` keeps only Claude transcripts whose path contains the text, such as a project name.
- `--repo` counts code, test and doc lines on each repository's checked-out branch, so tokens can be set against output.
- `--max-steps`, `--max-context` and `--budget` set the flag thresholds (defaults 100 steps, 200k context, 60M input tokens per run).

It prints Markdown: list-price value, the share spent re-reading context, subagent share, model mix, the most expensive runs, flags, Codex totals and lines changed.

## 2. Read it

Look at these, in order:

1. **Long runs.** Flagged runs over the step limit cost the most, because each step re-reads the whole context. Name the task and say how it should have been split.
2. **Big contexts.** A median above 200k means the session dragged a long history. One fresh session per task with a short brief fixes it.
3. **Expensive model on cheap work.** A subagent on Opus or Fable that only read files should have been Haiku or Sonnet. See [model and effort](references/model-and-effort.md).
4. **Read:write ratio.** Above 3:1 usually means re-reading the same files or auditing instead of building.
5. **Output.** Compare lines added with value spent. Deleted lines show churn; note what was thrown away and why.

Treat the numbers as estimates: list prices, not the bill, and line counts include formatting.

## 3. Report and learn

Write five to ten lines: total value, the top two or three causes with run names, and one or two concrete changes for the next batch. When the same cause shows up in two reports in a row, propose a one-line change to the project's agent instructions; don't edit them without the owner's yes.

Save the report where the owner asked (for example a dated file in a local reports folder). Never put transcript content, secrets or personal data in a repository.
