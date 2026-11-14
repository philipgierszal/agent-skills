#!/usr/bin/env python3
"""Summarise where coding-agent tokens went in a time window.

Reads local Claude Code transcripts (~/.claude/projects/**/*.jsonl) and Codex
session logs (~/.codex/sessions/**/*.jsonl), and optionally the Git history of
the repositories you name. Prints a Markdown report to stdout. Read-only.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import re
import statistics
import subprocess
from pathlib import Path

# USD per million tokens: (input, output, cache read). Cache write = 1.25 x input.
PRICES = {
    "fable-5-2": (8.0, 40.0, 0.20),
    "fable-5": (10.0, 50.0, 1.0),
    "opus-5-5": (4.0, 20.0, 0.20),
    "opus": (5.0, 25.0, 0.50),
    "sonnet-5-5": (2.0, 10.0, 0.10),
    "sonnet": (3.0, 15.0, 0.30),
    "haiku-5-5": (0.10, 0.50, 0.01),
    "haiku": (1.0, 5.0, 0.10),
}
READ_TOOLS = {"Read", "Grep", "Glob", "WebFetch", "WebSearch", "NotebookRead"}
WRITE_TOOLS = {"Edit", "Write", "NotebookEdit", "apply_patch"}
READ_CMD = re.compile(
    r"^\s*(cd [^&;]+(&&|;)\s*)?(cat|sed -n|head|tail|grep|rg|ls|find|wc|type|Get-Content|Select-String|Get-ChildItem"
    r"|git (log|show|diff|status|grep|ls-files|ls-tree|branch|rev-parse))\b"
)
WRITE_CMD = re.compile(
    r"git (commit|push|merge|rm|add)\b|sed -i|cat > |Set-Content|Out-File|Add-Content|write_text|\*\*\* (Update|Add) File"
)
TEST_CMD = re.compile(r"pytest|unittest|check\.py|run_local_gate|--test-enable|ruff|npm (run )?test")


def price(model: str) -> tuple[float, float, float]:
    for key, value in PRICES.items():
        if key in model:
            return value
    return PRICES["opus"]


def cost_usd(model: str, fresh: int, cache_write: int, cache_read: int, out: int) -> float:
    pin, pout, pread = price(model)
    return (fresh * pin + cache_write * pin * 1.25 + cache_read * pread + out * pout) / 1e6


def classify(tool: str, command: str = "") -> str:
    """Return read, write, verify, run, delegate or other for one tool call."""
    if tool in READ_TOOLS or "Browser" in tool or "chrome" in tool:
        return "read"
    if tool in WRITE_TOOLS:
        return "write"
    if tool in ("Agent", "Task", "spawn_agent"):
        return "delegate"
    if tool in ("Bash", "PowerShell", "shell", "exec_command", "shell_command") or command:
        if WRITE_CMD.search(command):
            return "write"
        if TEST_CMD.search(command):
            return "verify"
        if READ_CMD.search(command):
            return "read"
        return "run"
    return "other"


def parse_time(value: str) -> dt.datetime | None:
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None


def claude_transcripts(root: Path, since: dt.datetime, match: str) -> list[dict]:
    runs = []
    for path in root.rglob("*.jsonl"):
        if match and match.lower() not in str(path).lower():
            continue
        if dt.datetime.fromtimestamp(path.stat().st_mtime, dt.timezone.utc) < since:
            continue
        is_sub = "subagents" in path.parts
        run = dict(file=path, sub=is_sub, model="", steps=0, fresh=0, cw=0, cr=0, out=0,
                   contexts=[], calls=collections.Counter(), label="", usd=0.0)
        seen = set()
        for line in path.open(encoding="utf-8", errors="replace"):
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            if entry.get("type") == "user" and not run["label"]:
                content = entry.get("message", {}).get("content")
                text = content if isinstance(content, str) else " ".join(
                    c.get("text", "") for c in content or [] if isinstance(c, dict))
                text = re.sub(r"<([\w-]+)[^>]*>.*?</\1>", " ", text, flags=re.S)
                lines = [t.strip() for t in text.splitlines() if t.strip() and not t.strip().startswith("<")]
                run["label"] = lines[0][:80] if lines else ""
            if entry.get("type") != "assistant":
                continue
            when = parse_time(entry.get("timestamp", ""))
            if not when or when < since:
                continue
            msg = entry.get("message", {})
            for block in msg.get("content") or []:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    command = str((block.get("input") or {}).get("command", ""))
                    run["calls"][classify(block.get("name", ""), command)] += 1
            usage, mid = msg.get("usage"), msg.get("id")
            if not usage or mid in seen:
                continue
            seen.add(mid)
            run["model"] = msg.get("model", run["model"])
            fresh, cw = usage.get("input_tokens", 0), usage.get("cache_creation_input_tokens", 0)
            cr, out = usage.get("cache_read_input_tokens", 0), usage.get("output_tokens", 0)
            run["steps"] += 1
            run["fresh"] += fresh
            run["cw"] += cw
            run["cr"] += cr
            run["out"] += out
            run["contexts"].append(fresh + cw + cr)
            run["usd"] += cost_usd(run["model"], fresh, cw, cr, out)
        meta = path.with_suffix(".meta.json")
        if meta.exists():
            try:
                run["label"] = json.loads(meta.read_text(encoding="utf-8")).get("description") or run["label"]
            except (json.JSONDecodeError, OSError):
                pass
        if run["steps"]:
            runs.append(run)
    return runs


def codex_sessions(root: Path, since: dt.datetime) -> dict:
    total = collections.Counter()
    for path in root.rglob("*.jsonl"):
        if dt.datetime.fromtimestamp(path.stat().st_mtime, dt.timezone.utc) < since:
            continue
        last = None
        for line in path.open(encoding="utf-8", errors="replace"):
            if '"token_count"' in line:
                try:
                    last = json.loads(line)["payload"].get("info", {}).get("total_token_usage") or last
                except (json.JSONDecodeError, KeyError, AttributeError):
                    pass
            elif '"function_call"' in line or '"custom_tool_call"' in line:
                try:
                    payload = json.loads(line)["payload"]
                except (json.JSONDecodeError, KeyError):
                    continue
                text = str(payload.get("input") or payload.get("arguments") or "")
                total["call_" + classify(payload.get("name", ""), text)] += 1
        if last:
            total["sessions"] += 1
            for key in ("input_tokens", "cached_input_tokens", "output_tokens"):
                total[key] += last.get(key, 0)
    return total


def git_lines(repo: Path, since: dt.datetime) -> collections.Counter:
    out = subprocess.run(
        ["git", "-C", str(repo), "log", "--no-merges", f"--since={since.isoformat()}",
         "--numstat", "--format="], capture_output=True, text=True, check=False).stdout
    lines = collections.Counter()
    for row in out.splitlines():
        parts = row.split("\t")
        if len(parts) != 3 or not parts[0].isdigit():
            continue
        name = parts[2].lower()
        kind = "tests" if "test" in name else "docs" if name.endswith((".md", ".rst", ".txt")) else "code"
        lines[kind + "+"] += int(parts[0])
        lines[kind + "-"] += int(parts[1])
    return lines


def m(n: float) -> str:
    return f"{n / 1e6:,.1f}M"


def report(args: argparse.Namespace) -> str:
    since = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=args.hours)
    runs = claude_transcripts(Path(args.claude_root).expanduser(), since, args.match)
    out = [f"# Token usage, last {args.hours} h (since {since:%Y-%m-%d %H:%M} UTC)", ""]
    usd = sum(r["usd"] for r in runs)
    cr = sum(r["cr"] for r in runs)
    if runs:
        read_cost = sum(r["cr"] * price(r["model"])[2] for r in runs) / 1e6
        out_cost = sum(r["out"] * price(r["model"])[1] for r in runs) / 1e6
        sub_cost = sum(r["usd"] for r in runs if r["sub"])
        calls = sum((r["calls"] for r in runs), collections.Counter())
        out += ["## Claude", "",
                f"- {len(runs)} transcripts, {sum(r['steps'] for r in runs):,} steps, list-price value **${usd:,.0f}**.",
                f"- Re-reading context: {m(cr)} tokens = {read_cost / usd:.0%} of value; writing output "
                f"{m(sum(r['out'] for r in runs))} = {out_cost / usd:.0%}.",
                f"- Subagents: {sub_cost / usd:.0%} of value.",
                f"- Tool calls: read {calls['read']}, write {calls['write']}, run {calls['run']}, "
                f"verify {calls['verify']}, delegate {calls['delegate']} "
                f"(read:write {calls['read'] / max(1, calls['write']):.1f}:1).", ""]
        by_model = collections.Counter()
        for r in runs:
            by_model[(r["model"] or "?") + (" (subagent)" if r["sub"] else "")] += r["usd"]
        out += ["| Model | Share |", "| --- | ---: |"]
        out += [f"| {k} | {v / usd:.0%} |" for k, v in by_model.most_common(6)] + [""]
        out += ["### Most expensive runs", "", "| Run | Model | Steps | Median context | Read:write | Value |",
                "| --- | --- | ---: | ---: | ---: | ---: |"]
        for r in sorted(runs, key=lambda r: -r["usd"])[: args.top]:
            ratio = r["calls"]["read"] / max(1, r["calls"]["write"])
            label = (("sub: " if r["sub"] else "") + (r["label"] or r["file"].stem)).replace("|", "/")[:60]
            out.append(f"| {label} | {r['model'].replace('claude-', '')} | {r['steps']} | "
                       f"{statistics.median(r['contexts']) / 1e3:,.0f}k | {ratio:.1f} | ${r['usd']:,.0f} |")
        flags = []
        for r in runs:
            name = (r["label"] or r["file"].stem)[:50]
            if r["steps"] > args.max_steps:
                flags.append(f"`{name}` ran {r['steps']} steps (limit {args.max_steps}): split it.")
            if statistics.median(r["contexts"]) > args.max_context:
                flags.append(f"`{name}` carried a median {statistics.median(r['contexts']) / 1e3:,.0f}k context: "
                             "start fresh sessions with a short brief.")
            if r["sub"] and ("opus" in r["model"] or "fable" in r["model"]) and \
                    r["calls"]["write"] == 0 and r["calls"]["read"] >= 10:
                flags.append(f"`{name}` only read, on {r['model']}: use Haiku or Sonnet for searches.")
            if r["fresh"] + r["cw"] + r["cr"] > args.budget * 1e6:
                flags.append(f"`{name}` used {m(r['fresh'] + r['cw'] + r['cr'])} input, over the "
                             f"{args.budget:.0f}M budget.")
        out += ["", "### Flags", ""] + ([f"- {f}" for f in flags[:15]] or ["- None."]) + [""]
    else:
        out += ["## Claude", "", "No transcripts in this window.", ""]
    if not args.no_codex:
        cx = codex_sessions(Path(args.codex_root).expanduser(), since)
        if cx["sessions"]:
            out += ["## Codex", "",
                    f"- {cx['sessions']} sessions, input {m(cx['input_tokens'])} "
                    f"({cx['cached_input_tokens'] / max(1, cx['input_tokens']):.0%} cached), "
                    f"output {m(cx['output_tokens'])}.",
                    f"- Tool calls: read {cx['call_read']}, write {cx['call_write']}, run {cx['call_run']} "
                    f"(read:write {cx['call_read'] / max(1, cx['call_write']):.1f}:1).", ""]
        else:
            out += ["## Codex", "", "No sessions in this window.", ""]
    if args.repo:
        out += ["## Lines changed on the checked-out branch (no merges)", "",
                "| Repository | Code +/- | Tests +/- | Docs +/- |", "| --- | ---: | ---: | ---: |"]
        added = 0
        for repo in args.repo:
            g = git_lines(Path(repo), since)
            added += g["code+"] + g["tests+"]
            out.append(f"| {Path(repo).name} | {g['code+']}/{g['code-']} | {g['tests+']}/{g['tests-']} | "
                       f"{g['docs+']}/{g['docs-']} |")
        if usd:
            out += ["", f"Code and test lines added per $100 of Claude value: {added / usd * 100:,.0f}.", ""]
    return "\n".join(out)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--hours", type=float, default=24, help="window length (default 24)")
    p.add_argument("--match", default="", help="only Claude transcripts whose path contains this text")
    p.add_argument("--repo", action="append", default=[], help="Git repository to count lines in (repeatable)")
    p.add_argument("--top", type=int, default=10)
    p.add_argument("--max-steps", type=int, default=100)
    p.add_argument("--max-context", type=int, default=200_000)
    p.add_argument("--budget", type=float, default=60, help="input-token budget per run, in millions")
    p.add_argument("--claude-root", default="~/.claude/projects")
    p.add_argument("--codex-root", default="~/.codex/sessions")
    p.add_argument("--no-codex", action="store_true")
    print(report(p.parse_args()))


if __name__ == "__main__":
    main()
