# Agent Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

My Agent Skills collection: original skills I maintain, plus a curated selection of other authors' work with pinned references, selection reasons, and honest validation limits.

- **Use my skills:** the [installable catalog](#skill-catalog) below.
- **Explore other authors:** [curated upstream selection](docs/curated-skills.md), backed by [catalog.json](catalog.json).
- **Understand duplication and compatibility:** [skill audit](docs/skill-audit.md).
- **Grow the collection:** [maintenance and evaluation guide](docs/maintaining-the-collection.md).
- **Connect the lifecycle:** [proposed development workflow](docs/development-workflow.md), from requirements and ADRs to implementation and security/authorization review.
- **Track corrections:** [audit repairs](docs/skill-repairs.md) and [selected attributed patches](repairs/2026-09-05/README.md).

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

## Shared working rules

[`agent-instructions/`](agent-instructions/working-rules.md) holds general rules for working with an owner and for spending tokens well, learned from a real project. `python agent-instructions/install.py` writes them into `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md` between markers, keeps everything else in those files, and links this repository's skills for both agents.

## Skill catalog

| Skill | Use it for | Key output | Side effects | Status |
| --- | --- | --- | --- | --- |
| [`architecture-hygiene-audit`](skills/architecture-hygiene-audit/SKILL.md) | Whole-repository dead-code, dependency, structure, and SOLID/SoC/DRY/KISS/YAGNI review | Deterministic inventory, reconciled evidence ledger, calibrated findings, and a human report | Does not change the target source tree; may write audit artifacts outside it | Stable |
| [`token-usage-review`](skills/token-usage-review/SKILL.md) | Daily or after-batch review of where Claude Code and Codex tokens went, plus which model and effort to use for which job | Markdown report: value, context re-reading, subagent and model share, costliest runs, flags, lines changed; [model and effort guide](skills/token-usage-review/references/model-and-effort.md) | Read-only; reads local transcripts and Git history | Stable |
| [`process-model-review`](skills/process-model-review/SKILL.md) | Audit documented business processes for coverage, clarity, coherence, system mapping, controls and KPIs against reference models (APQC, SCOR, ITIL) and the systems' real data | Findings per process with severity, a coverage matrix and a top-five summary | Read-only on the processes under review | Stable |
| [`polish-business-writing`](skills/polish-business-writing/SKILL.md) | Write or review Polish documents for a CFO, board or chief accountant: ERP concepts, functional comparisons, "today vs. new system" walkthroughs with screenshots | A document built on the CFO template, checked against the style checklist and the Odoo-to-accounting [terminology table](skills/polish-business-writing/references/terminology.md) | None; writing guidance only | Stable |
| [`itil-ticket-handling`](skills/itil-ticket-handling/SKILL.md) | Handle an employee's ticket about an internal system the ITIL 4 way: log, classify, clarify (at most 3 questions), diagnose, change, verify on production, resolve, confirm with the requester, close | Internal notes, requester messages and stage changes on the ticket; [ITIL essentials](skills/itil-ticket-handling/references/itil-essentials.md) and an [Odoo Helpdesk adapter](skills/itil-ticket-handling/references/odoo-helpdesk.md) | Writes on the ticket only as the organisation's site profile allows; every other write and every release needs the owner's approval | Stable |
| [`keepassxc-agent-secrets`](skills/keepassxc-agent-secrets/SKILL.md) | Agents using secrets from a KeePassXC database: find, read in memory, store new logins, rotate, backups, failure cases, leak response | Credentials used without ever reaching chat, files or Git; a copy-paste [hand-off block](skills/keepassxc-agent-secrets/references/handoff.md) for any agent; [research and sources](skills/keepassxc-agent-secrets/references/research.md) | Reads secrets in memory through a local adapter; creating or rotating an entry needs the owner's approval in KeePassXC | Stable |

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
python scripts/orphan_check.py
python skills/architecture-hygiene-audit/scripts/validate_ledger.py \
  --inventory examples/architecture-hygiene-audit/inventory.json \
  --ledger examples/architecture-hygiene-audit/ledger.json
```

Behavioral evaluation evidence: [architecture-hygiene-audit](evals/architecture-hygiene-audit.md), [token-usage-review](evals/token-usage-review.md), [polish-business-writing](evals/polish-business-writing.md), [keepassxc-agent-secrets](evals/keepassxc-agent-secrets.md) and [itil-ticket-handling](evals/itil-ticket-handling.md). Design and primary-source rationale: research on the [audit skill](docs/research/architecture-hygiene-audit.md), the [development workflow](docs/research/development-workflow.md), [ITIL ticket handling](docs/research/itil-ticket-handling.md) and the [repository structure](docs/research/public-skills-repository-structure.md); designs for the [audit skill](docs/superpowers/specs/2026-08-25-architecture-hygiene-audit-design.md) and the [public repository](docs/superpowers/specs/2026-08-26-public-repository-design.md). Executed implementation plans live in Git history.

Every file is reachable from this README through links or named paths (each `skills/<name>/` is an entry point); `python scripts/orphan_check.py` fails on a file nothing reaches, `--tree` prints the tree, and settings live in `scripts/orphan_check.json`.

## Contributing and security

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before changing a skill's triggers, behavior, scripts, or output contract. Report ordinary defects through GitHub Issues. Report vulnerabilities privately according to [`SECURITY.md`](SECURITY.md).

This is an independently maintained collection, informed by the clear catalogs and validation culture of [Matt Pocock's skills](https://github.com/mattpocock/skills) and [Superpowers](https://github.com/obra/superpowers); it is not a fork of either project.

## License

Original repository material is MIT; see [`LICENSE`](LICENSE). Third-party derivative [repair patches](repairs/2026-09-05/README.md) retain their separately stated CC-BY-SA-4.0 license and attribution.
