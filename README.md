# Agent Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

My Agent Skills collection: original skills I maintain, plus a curated selection of other authors' work with pinned references, selection reasons, and honest validation limits.

- **Use my skills:** the [installable catalog](#skill-catalog) below.
- **Explore other authors:** [curated upstream selection](docs/curated-skills.md), backed by [catalog.json](catalog.json).
- **Understand duplication and compatibility:** [skill audit](docs/skill-audit.md).
- **Grow the collection:** [maintenance and evaluation guide](docs/maintaining-the-collection.md).

Upstream references are bookmarks, not bundled installations or claims of authorship. Installing this repository installs only its own `skills/` packages. Each upstream retains its own license.

## Install in 30 seconds

Install the architecture audit skill into the current project:

```bash
npx skills@latest add philipgierszal/agent-skills --skill architecture-hygiene-audit
```

To make it available to Codex in every project:

```bash
npx skills@latest add philipgierszal/agent-skills \
  --skill architecture-hygiene-audit \
  --global \
  --agent codex
```

Preview the repository's available skills without installing:

```bash
npx skills@latest add philipgierszal/agent-skills --list
```

## First use

Invoke the skill explicitly:

```text
$architecture-hygiene-audit Audit this repository for dead code, orphaned files, unused methods, dependency violations, and architecture design smells.
```

It can also be selected implicitly for requests such as:

```text
Audit every file in this repository. Map file and symbol relationships, then identify dead ends, orphaned files, unused exports, dependency cycles, and violations of our documented architecture rules.
```

## Skill catalog

| Skill | Use it for | Key output | Side effects | Status |
| --- | --- | --- | --- | --- |
| [`architecture-hygiene-audit`](skills/architecture-hygiene-audit/SKILL.md) | Whole-repository dead-code, dependency, structure, and SOLID/SoC/DRY/KISS/YAGNI review | Deterministic inventory, reconciled evidence ledger, calibrated findings, and a human report | Does not change the target source tree; may write audit artifacts outside it | Stable |

## What the audit proves

The skill inventories every Git-tracked and non-ignored untracked path, separates production reachability from test/tool reachability, records typed relationships, checks dynamic and convention-driven channels, and requires exactly one evidence-ledger entry per path.

Findings use calibrated classes:

- `confirmed-unreachable`
- `high-confidence-unused`
- `probable-unused`
- `orphan-path`
- `architecture-violation`
- `design-smell`
- `unknown-or-exempt`

An analyzer warning is evidence, not permission to delete. Architecture violations require a versioned repository rule; SOLID, separation of concerns, DRY, KISS, and YAGNI remain contextual design lenses otherwise.

See the [validator-backed example](examples/architecture-hygiene-audit/README.md) for a policy, inventory, reconciled ledger, and report.

## Requirements and compatibility

- Git, for repository inventory and revision binding.
- Python 3.10 or newer, for the bundled deterministic scripts.
- Node.js/npm only when installing through `npx skills`.
- A coding agent with shell access.

The skill follows the portable [Agent Skills specification](https://agentskills.io/specification) and includes Codex display/invocation metadata. Codex is the currently tested client; portability of the skill directory does not imply that every agent harness has been integration-tested.

## Update or remove

```bash
npx skills update architecture-hygiene-audit
npx skills remove architecture-hygiene-audit
```

Add `--global` when maintaining a global installation.

## Develop and validate

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python -m ruff check .
python -m compileall -q skills tests
python skills/architecture-hygiene-audit/scripts/validate_ledger.py \
  --inventory examples/architecture-hygiene-audit/inventory.json \
  --ledger examples/architecture-hygiene-audit/ledger.json
```

Behavioral evaluation evidence lives in [`evals/`](evals/). The design and primary-source rationale live in [`docs/research/`](docs/research/) and [`docs/superpowers/specs/`](docs/superpowers/specs/).

## Contributing and security

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before changing a skill's triggers, behavior, scripts, or output contract. Report ordinary defects through GitHub Issues. Report vulnerabilities privately according to [`SECURITY.md`](SECURITY.md).

This is an independently maintained collection, informed by the clear catalogs and validation culture of [Matt Pocock's skills](https://github.com/mattpocock/skills) and [Superpowers](https://github.com/obra/superpowers); it is not a fork of either project.

## License

MIT. See [`LICENSE`](LICENSE).
