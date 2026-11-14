# Choosing a model and an effort level

Prices are Anthropic list prices per million tokens (checked 2026-11-14). On a subscription you don't pay these directly, but they show what eats your limits.

| Model | Input | Re-read from cache | Output | Relative to Opus |
| --- | ---: | ---: | ---: | ---: |
| Fable 5.2 | $8 | $0.20 | $40 | 2× |
| Opus 5.5 | $4 | $0.20 | $20 | 1× |
| Sonnet 5.5 | $2 | $0.10 | $10 | ½ |
| Haiku 5.5 | $0.10 | ~$0.01 | $0.50 | 1⁄40 |

## The rule that matters most

**Cost ≈ steps × context per step × price.** Every step re-reads the whole conversation. A 300k-token context on Opus costs about $0.06 per step just to re-read, so a 500-step run costs about $30 before any work is written. Picking a cheaper model halves or quarters that. Keeping runs short and contexts small cuts it by 5–10×.

## Which model for which job

| Job | Model | Effort | Why |
| --- | --- | --- | --- |
| Planning, brief writing, reviewing a result against its brief | Opus 5.5 | medium | Judgement matters, but the session should stay short |
| Implementing a slice (new feature, data model, integration) | Opus 5.5 | medium; high if the first attempt failed | Best code per token; high pays off only on hard problems |
| Architecture, data-migration design, production-touching change, security review | Opus 5.5 | high | A mistake costs more than the tokens |
| Stuck after two attempts on Opus at high | Fable 5.2 | high | Twice the price; use it to unblock, not by default |
| Mechanical edits: renames, link fixes, doc rewrites, branch clean-up, gate runs | Sonnet 5.5 | low or medium | Half the price; no deep reasoning needed |
| Review of one diff (not the whole repo) | Sonnet 5.5 | medium | Reads the change, reports a few findings |
| Searching, reading, "where is X", log reading | Haiku 5.5 (or the Explore agent) | low | 40× cheaper than Opus; the answer is a location, not a design |
| Daily token report | Sonnet 5.5 or Haiku 5.5 | low | The script does the counting; the model only summarises |

## Effort levels

- **low:** short answers, few tool calls. For searches, summaries and mechanical edits.
- **medium:** the default on Opus 5.5 and Haiku 5.5. Right for most coding.
- **high:** more thinking and checking. For hard bugs, design, migrations and security.
- **xhigh / max:** rarely worth it. Use only for one hard question when correctness matters far more than cost, never for a long agent run.

Raise effort only after a lower level visibly failed. Judge by cost per finished task: a cheap run that needs a redo isn't cheap.

## How to set them in Claude Code

- Session model and effort: the model picker in the app, or `/model` and `/effort` in a terminal session.
- Subagents: pass `model` (`haiku`, `sonnet`, `opus`) when spawning; agent files take `model:` and `effort:` in their frontmatter.
- Codex: `model` and `model_reasoning_effort` in `~/.codex/config.toml`, or per run with `-c`.
