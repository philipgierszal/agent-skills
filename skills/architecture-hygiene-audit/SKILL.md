---
name: architecture-hygiene-audit
description: Use when asked to audit an entire repository for dead code, orphaned files, unused methods or exports, dependency cycles, architecture-rule violations, repository structure problems, or SOLID, separation-of-concerns, DRY, KISS, and YAGNI concerns.
---

# Architecture Hygiene Audit

Audit the whole repository without changing its source. Every conclusion must name its scope, evidence, counter-evidence, and uncertainty.

Every invocation—including a focused SOLID, DRY, dependency-rule, or repository-structure audit—must retain the inventory/ledger scope proof and state the relevant roots, variants, and limitations. Do not answer only the design question and imply the repository was exhaustively audited.

## Non-negotiable contract

- Account for every Git-tracked and non-ignored untracked path. Never silently sample.
- Analyze first-party text/source content; classify generated, vendored, binary, fixture, documentation, configuration, deployment, and standalone paths with provenance.
- Model production/shipped roots separately from full-repository roots.
- Treat configuration, build, CI, deployment, framework conventions, generation, and external/public contracts as real relations.
- Use parser/compiler/ecosystem-native analyzers. Text search corroborates string-driven edges; it does not prove reachability.
- A tool finding is a candidate, not permission to delete. Audit mode may write reports and temporary artifacts only.
- Call something an architecture violation only when a versioned repository rule defines it. SOLID, SoC, DRY, KISS, and YAGNI are advisory lenses otherwise.

## Workflow

### 1. Freeze scope and create the inventory

Resolve this skill's directory as `SKILL_ROOT`. Resolve the target Git root and record revision, branch, dirty state, submodules, and workspaces. Create the audit output outside the repository (OS temp by default) before generating any artifacts.

Run:

```bash
python "<SKILL_ROOT>/scripts/inventory.py" --repo "<repo>" --output "<audit-dir>/inventory.json"
```

The inventory covers the union of HEAD, every index stage, and non-ignored untracked paths. It models index conflict separately from worktree presence, preserves staged/unstaged deletions, distinguishes submodules, real symlinks, and platforms that materialize Git symlinks as regular files, and safely serializes legal non-UTF-8 POSIX path bytes. Initialized submodule revision and dirty state participate in the `inventory_digest` that binds the ledger to inventoried content. Inspect ignored paths only when manifests, builds, deployments, runtime configuration, or repository policy make them relevant; record those as explicit external/ignored scope additions. Record `.git`, caches, dependency stores, and unrelated build output as scope exclusions rather than pretending they were reviewed.

### 2. Discover intent, roots, and variants

Read manifests, lockfiles, package exports, architecture documents, ADRs, runbooks, scripts, containers, CI, deployment descriptors, generators, and framework configuration before judging reachability.

Create:

- a production/shipped root set;
- a full-repository root set including tests, examples, fixtures, stories, benchmarks, and developer tools; and
- a declared variant matrix covering applications, packages, platforms, architectures, feature flags, build tags, optional extras, and environment-specific configuration.

Missing variants remain visible limitations. Tests keeping code alive do not prove production reachability.

### 3. Select native analyzer adapters

Read [references/adapter-selection.md](references/adapter-selection.md). Prefer already-configured project commands and tools. Record every command, version, configuration, exit status, raw artifact, target, and known blind spot. If authoritative tooling is unavailable, downgrade confidence; do not emulate compiler semantics with regular expressions.

### 4. Build and reconcile the evidence graph

Read [references/evidence-model.md](references/evidence-model.md). For every inventory path, create exactly one ledger row with its role, review status, reachability, evidence, typed outgoing relations, dynamic-reference gaps, and findings. A zero-relation path needs an `orphan-path`, `unknown-or-exempt`, standalone/provenance explanation, or evidence-backed no-finding disposition.

For source files, reconcile analyzer symbols and findings for classes, functions, methods, exports, callbacks, fixtures, hooks, overrides, and generated interfaces. Findings name a file or fully qualified symbol and source location.

Complete the dynamic-behavior preflight before promoting any unused candidate: reflection, computed imports, string lookup, serialization, dependency injection, registries, decorators/annotations, framework discovery, package/public consumers, native calls, config/scripts/build/CI/deploy roots, generation, templates/assets/schemas/migrations, test-only use, and every declared variant.

### 5. Evaluate architecture policy and design lenses

Read [references/architecture-policy.md](references/architecture-policy.md). Evaluate observed edges against explicit rules and exception scopes. When no policy exists, label inferred boundaries and possible rules as proposals—not violations.

Use SOLID, separation of concerns, DRY, KISS, and YAGNI to explain file-level `design-smell` evidence. Do not score classes against slogans, force abstraction to remove syntactic duplication, or introduce speculative seams.

### 6. Produce and validate the audit

Read [references/report-contract.md](references/report-contract.md). Preserve `inventory.json`, `ledger.json`, raw analyzer output, and a human-readable report. Validate the ledger:

```bash
python "<SKILL_ROOT>/scripts/validate_ledger.py" --inventory "<audit-dir>/inventory.json" --ledger "<audit-dir>/ledger.json"
```

The audit is not exhaustive unless the validator reports exact path reconciliation. Batching a large repository is allowed; sampling or silently truncating the ledger is not.

## Completion gate

Before reporting completion, confirm:

- inventory and ledger revisions and `inventory_digest` match;
- every inventory path appears exactly once;
- every relation has a ledger-wide unique ID, type, target, evidence, confidence, scopes, and variants;
- every analyzer finding has a disposition;
- production and full-repository roots and analyzed variants are named;
- failed tools, unsupported syntax, dynamic channels, external consumers, and missing variants remain visible with affected scopes and variants;
- high-certainty findings name analyzed scopes/variants, contain substantive counter-evidence checks, and overlap no unresolved dynamic channel;
- every architecture violation cites a policy rule and applicable observed relation IDs whose scopes and variants cover the finding; and
- the target source tree was not changed.

Use calibrated language: **“No known findings within the documented roots, variants, tools, and dynamic-behavior model.”** Never claim universal absence of dead code.

## Common mistakes

| Shortcut | Required correction |
| --- | --- |
| “The analyzer says unused, so delete it.” | Treat output as evidence; complete roots, variants, and dynamic preflight first. |
| “No text reference means unreachable.” | Use semantic tools and inspect configuration/convention edges. |
| “Config files do not count as code relations.” | Model build, runtime, CI, deployment, and registry references. |
| “Every file was reviewed” without reconciliation. | Generate the inventory and pass the ledger validator. |
| “DRY means every duplicate must be abstracted.” | Ask whether it is duplicated knowledge and changes for the same reason. |
| “This is only an architecture question, so inventory can wait.” | Keep the inventory/ledger proof, roots, variants, and limitations even in a focused report. |
| “Deadline means sample the hot spots.” | Batch the full scope or report the audit incomplete. |

Remediation is a separate, explicitly authorized change. Remove one dependency-closed candidate at a time and re-run builds, tests, type checks, linters, packaging, startup, policy checks, and affected variants.
