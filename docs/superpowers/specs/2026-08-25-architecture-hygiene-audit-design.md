# Architecture Hygiene Audit Skill Design

Date: 2026-08-25
Status: Approved by repository policy for autonomous evidence-backed execution

## Purpose

Create a reusable Codex skill named `architecture-hygiene-audit` for exhaustive, read-only repository audits. It must account for every repository path, analyze file and symbol relationships using ecosystem-native tools, find dead-code candidates and architectural violations without overstating certainty, and distinguish enforceable rules from SOLID/SoC/DRY/KISS/YAGNI design judgments.

The skill will live in a standalone personal skills repository, `philipgierszal/agent-skills`, rather than a fork of `mattpocock/skills`. A fork would couple unrelated custom work to Matt Pocock's complete distribution and upstream history. The standalone repository keeps ownership, releases, tests, and installation independent while allowing proper attribution where ideas are reused.

## Scope

The first release contains one skill and its supporting research, evaluation fixtures, deterministic scripts, and tests. Audit mode is read-only: it may write reports and temporary analysis artifacts, but it must not delete, move, rewrite, suppress, or automatically remediate repository code. Remediation and CI configuration require a separate explicit request.

“Exhaustive” means every Git-tracked file and every non-ignored untracked file receives exactly one ledger entry. Ignored paths are included only when referenced by a manifest, build/deploy mechanism, or repository policy. Dependency stores, caches, and `.git` internals remain explicit scope exclusions. The audit can prove inventory and disposition coverage, not omniscient knowledge of every runtime relationship.

## Repository Structure

```text
agent-skills/
├── README.md
├── LICENSE
├── docs/
│   ├── research/architecture-hygiene-audit.md
│   └── superpowers/specs/2026-08-25-architecture-hygiene-audit-design.md
├── evals/architecture-hygiene-audit.md
├── skills/architecture-hygiene-audit/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── references/
│   │   ├── adapter-selection.md
│   │   ├── architecture-policy.md
│   │   ├── evidence-model.md
│   │   └── report-contract.md
│   └── scripts/
│       ├── inventory.py
│       └── validate_ledger.py
└── tests/
    ├── test_inventory.py
    └── test_validate_ledger.py
```

## Skill Architecture

`SKILL.md` is a concise orchestrator. It defines the scope contract, audit phases, safety boundary, confidence rules, and report completion gate. Detailed schemas and ecosystem-specific guidance are progressively disclosed through one-level references.

`inventory.py` creates a deterministic, NUL-safe JSON inventory from Git. It inventories the union of HEAD, all index stages, and non-ignored untracked files, so staged/unstaged deletions and merge conflicts stay visible. Each path records HEAD/index identity, index state, independent worktree presence, kind, size, and content hash where applicable; submodules, real symlinks, and platform-materialized Git symlinks are distinct. Initialized submodule HEAD and dirty state participate in a canonical digest that detects worktree, index, and submodule drift even when superproject HEAD is unchanged. Surrogate-escaped POSIX path bytes are emitted as safe JSON escapes. The helper fails clearly outside a Git worktree.

`validate_ledger.py` validates the completed machine-readable ledger against the inventory. It rejects revision or inventory-digest drift, missing, duplicate, or unexpected paths, invalid dispositions, empty evidence, ledger-wide duplicate relation IDs, architecture references whose relation scopes/variants do not cover the finding, and high-certainty claims whose affected scope/variant overlaps an unresolved channel. Its purpose is coverage and evidence-contract proof, not semantic dead-code detection.

The agent remains responsible for discovering root sets and build variants, choosing native analyzers, interpreting their output, reviewing dynamic channels, constructing typed relations, and writing findings. It must downgrade confidence when tooling or runtime evidence is incomplete rather than imitate a compiler with text search.

## Audit Data Flow

1. Freeze the audited Git revision and record repository state.
2. Generate the inventory before writing audit artifacts into the target repository.
3. Read repository intent: manifests, architecture documentation, ADRs, runbooks, build/deploy definitions, and policy.
4. Discover production and full-repository roots plus supported variant matrices.
5. Select and run ecosystem-native analyzers; preserve commands, versions, configuration, failures, and raw artifacts.
6. Normalize direct, inferred, dynamic, configuration, build, deployment, generation, and convention-based relations into the evidence ledger.
7. Reconcile every inventory path with one disposition and analyze every tool finding.
8. Evaluate only explicit versioned architecture rules as violations. Record SOLID/SoC/DRY/KISS/YAGNI observations as advisory design smells unless a repository rule makes them deterministic.
9. Validate the ledger and produce the human-readable report, limitations, unresolved dynamic channels, and variant gaps.

## Evidence and Decisions

Findings use separate classes: `confirmed-unreachable`, `high-confidence-unused`, `probable-unused`, `orphan-path`, `architecture-violation`, `design-smell`, and `unknown-or-exempt`. Every finding includes evidence, counter-evidence checks, scope/variant applicability, confidence rationale, and a safe next action.

No single analyzer result or absence from runtime coverage proves code is dead. Before raising confidence, the audit checks computed imports, reflection, serialization, dependency injection, routes/events/queues, registries, framework discovery, package exports, public consumers, native calls, build and deployment configuration, CI, generators, templates/assets/migrations, test-only reachability, and supported variants.

Deletion eligibility is advisory only. An actual deletion requires separate authorization and a dependency-closed removal with build, test, type, lint, packaging, startup, architecture, and relevant variant verification.

## Architecture Enforcement

The skill reads an optional versioned `.architecture-hygiene.yml` policy. Policy concepts include named modules/layers, path mappings, root declarations, allowed and forbidden dependency directions, cycle rules, classifications, variant matrices, retained standalone artifacts, and expiring exceptions.

When no policy exists, inferred boundaries are proposals rather than violations. Continuous CI may gate deterministic policy violations and scope-complete high-certainty results; probable findings and design smells remain advisory. Legacy adoption should baseline existing violations and fail on regressions rather than force unsafe bulk cleanup.

## Failure Handling

- Outside a Git repository: stop and report the required precondition.
- Dirty repository: preserve present, deleted, conflicted, staged, unstaged, and untracked path states in the inventory; do not modify source files.
- Analyzer unavailable or failing: record the failure and downgrade affected findings.
- Unsupported syntax or ecosystem: retain paths as reviewed/unknown, never as clean.
- Incomplete roots, variants, or dynamic behavior: expose the gap and block a “zero dead code” claim.
- Ledger mismatch: the audit is incomplete and cannot be reported as exhaustive.
- Oversized repositories: batch analysis while retaining a single inventory and final reconciliation; do not silently sample.

## Testing Strategy

Skill behavior follows RED-GREEN-REFACTOR. Baseline scenarios cover a dynamic TypeScript monorepo, a Python plugin system, and conflicting architecture-principle demands. The same scenarios are repeated with the skill, checking for inventory proof, root/variant modeling, dynamic-reference handling, calibrated confidence, read-only behavior, and separation of deterministic rules from design judgment.

Script tests use Python's standard library and temporary Git repositories. Tests are written and observed failing before implementation. Structural validation uses Codex's `quick_validate.py`. Final verification includes unit tests, script smoke tests on this repository, ledger reconciliation, skill validation, installation-copy comparison, clean Git status, and remote commit verification.

## Success Criteria

- The skill is discoverable automatically for exhaustive architecture/dead-code audits and explicitly through `$architecture-hygiene-audit`.
- Every supported audit produces a deterministic inventory and a reconciled per-file ledger.
- Unsupported or dynamic cases remain visible as uncertainty; the skill never promises universal absence of dead code.
- Architecture violations require explicit policy; design principles remain contextual review lenses.
- Audit mode never changes target source code.
- The skill and scripts pass behavioral, structural, and unit validation.
- The verified skill is installed in the personal Codex skill directory and pushed to `philipgierszal/agent-skills`.
