# Public Agent Skills Repository Design

Date: 2026-08-26
Status: Approved by repository policy for autonomous evidence-backed execution

## Purpose

Turn `philipgierszal/agent-skills` into a public, reusable Agent Skills catalog that a visitor can understand, install, validate, and contribute to without private context. The repository should borrow the strongest public-facing patterns from Matt Pocock's skills collection and Jesse Vincent's Superpowers project while remaining deliberately smaller than either.

The first public release continues to ship one stable skill, `architecture-hygiene-audit`. Its distinctive promise is evidence-first, repository-wide architecture and dead-code analysis with explicit coverage, uncertainty, and safety boundaries.

## Design Decision

Use a lightweight, standards-first catalog:

- keep each installable unit at `skills/<name>/SKILL.md`;
- put runtime scripts and progressively disclosed references beside the owning skill;
- keep tests, evaluations, examples, research, and maintainer documentation at repository root;
- make installation and first invocation the first actions in the README;
- publish contribution and security contracts before inviting external changes; and
- validate metadata, links, scripts, and a real example on Windows and Linux in CI.

This approach preserves the portable skill boundary shared by the Agent Skills specification, Matt Pocock's collection, and Superpowers without importing unrelated distribution infrastructure.

## Alternatives Considered

### Full multi-client plugin framework

Copy Superpowers-style plugin manifests, client adapters, hooks, bootstrap commands, release synchronization, and package metadata now. Rejected because the repository has one directly installable skill and no maintained plugin distribution. Those files would promise compatibility that has not been tested and create several version sources.

### README-only public launch

Change visibility and installation wording while leaving the rest of the repository untouched. Rejected because public users would have no contribution path, private security channel, continuous validation, or verified output example. The repository would be installable but not yet trustworthy or maintainable as a community project.

### Lightweight standards-first catalog

Adopt the portable layout, user-first README, verified example, deterministic CI, and community health files now; defer plugin and release machinery until a real distribution need appears. Selected because it gives users the useful parts of both reference repositories with the smallest honest maintenance surface.

## Public Information Architecture

The README flows from action to detail:

1. one-sentence outcome and validation/license badges;
2. a thirty-second public install command;
3. explicit and implicit first-use examples;
4. a compact skill catalog with status and side effects;
5. a link to a validator-backed example;
6. requirements, supported installation path, update, and removal;
7. contributor validation commands; and
8. links to contribution, security, research, and license documents.

The previous private-repository warning is removed. The explanation for not forking Matt Pocock's repository becomes a short attribution and design note rather than a major user-facing section.

## Repository Structure

```text
agent-skills/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug.yml
│   │   └── skill-proposal.yml
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/validate.yml
├── docs/
│   ├── research/
│   └── superpowers/
│       ├── plans/
│       └── specs/
├── evals/
├── examples/
│   └── architecture-hygiene-audit/
│       ├── README.md
│       ├── .architecture-hygiene.yml
│       ├── inventory.json
│       ├── ledger.json
│       └── report.md
├── skills/
│   └── architecture-hygiene-audit/
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       ├── references/
│       └── scripts/
├── tests/
│   ├── test_inventory.py
│   ├── test_skill_package.py
│   └── test_validate_ledger.py
├── AGENTS.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── SECURITY.md
└── requirements-dev.txt
```

No empty directories are added. `CHANGELOG.md`, category buckets, a setup/router skill, `.codex-plugin`, `.claude-plugin`, `package.json`, and Changesets remain deferred until the repository has a corresponding release or distribution problem.

## Skill Metadata and Compatibility

`SKILL.md` retains a name matching its directory and front-loads concrete audit triggers in the description. It adds:

```yaml
license: MIT
metadata:
  author: philipgierszal
  compatibility: Requires Git and Python 3.10+; designed for coding agents with shell access.
```

Python 3.10 is the true minimum because the bundled scripts use PEP 604 union syntax. The Agent Skills specification defines a top-level `compatibility` field, but the current Codex structural validator rejects that key while accepting string metadata. Until the validator converges with the specification, the same constraint is carried as `metadata.compatibility` and stated prominently in the README. The README describes the Agent Skills CLI route as supported and the Codex metadata as tested; it does not claim universal compatibility with every agent harness.

## Verified Example

The example is an intentionally small, illustrative audit artifact set. Its inventory and ledger share the same revision and digest and reconcile every path through the real bundled validator. It demonstrates:

- a production entry point;
- a probable-unused symbol whose uncertainty remains visible;
- an explicit architecture policy;
- machine-readable evidence; and
- a concise human report that distinguishes findings from proof of safe deletion.

The example is not represented as output from a real third-party project. A package test imports the validator and proves the example passes whenever the repository changes.

## Validation and CI

Local and continuous validation use only Git, supported Python versions, and pinned development dependencies:

```text
python -m unittest discover -s tests -v
python -m ruff check .
python -m compileall -q skills tests
python skills/architecture-hygiene-audit/scripts/validate_ledger.py \
  --inventory examples/architecture-hygiene-audit/inventory.json \
  --ledger examples/architecture-hygiene-audit/ledger.json
```

CI runs the same contract on Windows and Linux with Python 3.10 and a current Python 3 release. Third-party GitHub Actions are pinned to immutable commit hashes and receive only `contents: read` permission.

The package test enforces stable metadata, existing relative links, required public community files, and validator-backed example integrity. It avoids testing prose wording or internal implementation details.

## Contribution and Security Model

`CONTRIBUTING.md` allows small documentation fixes directly and asks contributors to discuss new skills or behavior changes first. It requires focused changes, deterministic and safe scripts, valid references, behavioral evidence for instruction changes, and provenance for copied material.

Issue forms separate reproducible defects from skill proposals. The pull-request template requests the problem, approach, validation, behavior evidence, documentation, and provenance without imposing a multi-harness process the project does not support.

`SECURITY.md` routes ordinary bugs to public issues and sensitive findings to GitHub's private vulnerability-reporting flow. Public visibility is not complete until that setting is enabled. A code of conduct is deferred until the maintainer publishes and can service a private enforcement contact.

## GitHub Publication

The repository becomes public with this description:

> Evidence-first Agent Skills for repository architecture, dead-code, and code-hygiene audits.

Topics:

- `agent-skills`
- `codex`
- `code-quality`
- `software-architecture`
- `dead-code`
- `static-analysis`

The default branch remains `main`. This change does not create a tag or release: those require a verified public clean-room install and successful remote CI first.

## Success Criteria

- An unauthenticated visitor can open the repository and install the named skill with the documented command.
- The README gives installation and first use before implementation history.
- Skill metadata truthfully names license and compatibility.
- A maintained example passes the bundled ledger validator.
- Unit tests, lint, bytecode compilation, structural skill validation, and CI configuration pass.
- Contributors have focused issue, pull-request, validation, and security guidance.
- GitHub visibility, description, topics, and private vulnerability reporting match this design.
- The committed local revision is the revision served by the public `main` branch.
