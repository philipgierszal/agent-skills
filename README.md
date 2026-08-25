# Philip's Agent Skills

Reusable custom skills for Codex and compatible Agent Skills clients.

## Included skill

### `architecture-hygiene-audit`

Performs exhaustive, read-only repository audits for:

- dead-code candidates, unused methods/exports, orphaned files, and unreachable modules;
- file, symbol, configuration, build, deployment, generation, and framework relationships;
- dependency cycles and explicit architecture-rule violations; and
- evidence-backed SOLID, separation-of-concerns, DRY, KISS, and YAGNI design concerns.

The skill creates a deterministic Git inventory and requires an exactly reconciled per-file ledger. It uses ecosystem-native analyzers as evidence, checks dynamic and convention-driven relationships, and refuses to equate an analyzer warning with safe deletion.

Audit mode does not delete, rewrite, move, suppress, or automatically remediate source code.

## Install

Install with the Agent Skills CLI:

```bash
npx skills@latest add philipgierszal/agent-skills --skill architecture-hygiene-audit
```

The repository is initially private, so GitHub authentication with repository access is required.

For a local checkout, copy `skills/architecture-hygiene-audit` into your personal Codex skills directory as `~/.codex/skills/architecture-hygiene-audit`. Restart or begin a new Codex turn so the skill catalog refreshes.

## Use

Invoke it explicitly:

```text
$architecture-hygiene-audit Audit this repository for dead code, orphaned files, unused methods, dependency violations, and architecture design smells.
```

Its discovery metadata also allows automatic invocation for exhaustive repository architecture and code-hygiene audit requests.

The report distinguishes:

- `confirmed-unreachable`
- `high-confidence-unused`
- `probable-unused`
- `orphan-path`
- `architecture-violation`
- `design-smell`
- `unknown-or-exempt`

The strongest clean conclusion it permits is scoped: “No known findings within the documented roots, variants, tools, and dynamic-behavior model.”

## Develop and verify

Requirements: Python 3.9+ and Git.

```bash
python -m unittest discover -s tests -v
python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/architecture-hygiene-audit
```

The evaluation record at [`evals/architecture-hygiene-audit.md`](evals/architecture-hygiene-audit.md) documents RED baseline gaps, GREEN behavioral results, and the refactor prompted by an observed failure. Primary-source research is at [`docs/research/architecture-hygiene-audit.md`](docs/research/architecture-hygiene-audit.md).

## Why this is not a Matt Pocock fork

[Matt Pocock's skills](https://github.com/mattpocock/skills) are a broad, composable engineering workflow collection. This repository contains independently maintained personal skills with their own scope, tests, release history, and installation path. A fork would be appropriate only if the intent were to modify and continuously merge Matt's complete distribution.

## License

MIT. See [`LICENSE`](LICENSE).
