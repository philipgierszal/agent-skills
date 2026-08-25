# Research: exhaustive architecture and code-hygiene audit skill

Date: 2026-08-25

## Executive recommendation

Build the skill as a technology-agnostic **orchestrator**, not as a universal dead-code detector. It should:

1. create a deterministic inventory and a row for every in-scope repository path;
2. discover all runtime, build, test, packaging, deployment, generation, and framework entrypoints;
3. select ecosystem-native analyzers and normalize their evidence into a typed graph;
4. evaluate explicit, versioned architecture rules separately from design heuristics; and
5. classify findings by proof strength and unresolved dynamic behavior.

This separation is essential. Static tools reason from a model and a root set, not from every possible production execution. Knip, for example, defines an unused file as a project file not reachable from configured entry files, while its own documentation lists computed imports, generated files, missing framework plugins, auto-imports, config references, and unsupported script or file formats as common sources of surprising results ([Knip issue-resolution guide](https://knip.dev/guides/handling-issues)). Go's official `deadcode` tool likewise limits a result to one `GOOS`/`GOARCH`/build-tag configuration and explicitly warns that a reported function is not automatically safe to delete ([Go `deadcode` documentation](https://pkg.go.dev/golang.org/x/tools/cmd/deadcode)).

## Define “exhaustive” as a verifiable contract

### 1. Inventory every first-party path

Use Git as the primary boundary: tracked files plus non-ignored untracked files. `git ls-files --cached --others --exclude-standard -z` provides this distinction and NUL-safe path handling; active submodules need explicit treatment because recursive support is limited to cached/stage modes ([Git `ls-files` documentation](https://git-scm.com/docs/git-ls-files)). Include ignored paths only when a manifest, build step, deployment definition, or user policy declares them relevant. Do not silently descend into dependency caches, virtual environments, or build output.

Produce an inventory ledger with one row per path and reconcile `ledger_count == inventory_count`. Every row should record:

- path, workspace/module, file kind, language, and ownership boundary;
- tracked/untracked/submodule/symlink status;
- first-party, generated, vendored, binary, fixture, test, documentation, configuration, or deployment classification;
- content-reviewed, tool-reviewed, metadata-only, or explicitly excluded status and rationale;
- production/test/development entrypoint membership;
- incoming/outgoing edges and unresolved-reference flags; and
- findings or “reviewed, no finding.”

“Every file” should therefore mean every repository path is accounted for. First-party text and source files receive content analysis; binaries, vendored trees, and generated artifacts receive provenance and reference analysis unless policy explicitly expands their scope.

### 2. Discover roots before judging reachability

Treat entrypoint discovery as a required phase. Collect roots from:

- package and workspace manifests, library exports, binaries, CLIs, and service mains;
- build files, task runners, shell scripts, containers, service managers, and deployment manifests;
- CI workflows, scheduled jobs, migrations, seeds, one-off operations, and hooks;
- framework configuration, route/event/command registries, dependency-injection containers, plugins, decorators/annotations, and naming conventions;
- code-generation inputs and generated outputs;
- tests, examples, fixtures, stories, benchmarks, and development tools; and
- templates, HTML, stylesheets, schemas, localization, media, and assets that reference code or each other.

Keep at least two root sets: **production/shipped** and **full repository**. Tests can keep production code alive even when both the test and code are deletable; Knip therefore provides a separate production mode and states that it complements rather than replaces the full run ([Knip production mode](https://knip.dev/features/production-mode)). Go's `deadcode -test` similarly adds test executables as roots and uses the difference to reveal test-only use or possible public-API coverage gaps ([Go `deadcode` documentation](https://pkg.go.dev/golang.org/x/tools/cmd/deadcode)).

For conditional builds, record and run a declared variant matrix: operating systems, architectures, feature flags, build tags, environment-dependent configs, package targets, and deployable applications. A result is only valid for the variants actually analyzed.

### 3. Build a typed evidence graph

Normalize tool output and repository inspection into nodes (files, symbols, packages, modules, targets, assets) and typed edges:

- import/re-export/include/package dependency;
- call, field access, type reference, inheritance, interface implementation;
- registration, reflection/string lookup, serialization, dependency injection;
- manifest/configuration/script/build/deploy reference;
- framework convention or glob discovery;
- generated-from/generates;
- template/asset/schema/migration reference; and
- test-only or development-only reachability.

Preserve provenance on every edge: tool, command, version, configuration, source location, and whether the edge is direct, inferred, or manually declared. Raw text search is useful corroboration for string-driven systems, but it is not a substitute for parser/compiler-aware analysis.

## Use language-native analyzers as adapters

No single tool covers all languages and runtime conventions. The skill should detect ecosystems and existing project tooling, then run the narrowest authoritative analyzers available.

| Ecosystem example | What the primary tool demonstrates | Limitation the skill must preserve |
| --- | --- | --- |
| JavaScript/TypeScript — Knip | Graph traversal from fine-grained entrypoints; unused files, exports, dependencies; framework plugins and script/config discovery ([entry-file documentation](https://knip.dev/explanations/entry-files)) | Computed import specifiers, missing/incomplete plugins, auto-imports, generated sources, uncommon formats, and conditional config can hide real edges ([issue-resolution guide](https://knip.dev/guides/handling-issues)). |
| Python — Vulture | AST-based defined-vs-used and unreachable-code analysis with per-item confidence and whitelists ([Vulture source repository](https://github.com/jendrikseipp/vulture)) | Python implicit calls and dynamic lookup can create false positives; the analysis records names without full scope sensitivity. Decorator ignores/whitelists are part of the supported model, not proof that code is dead. |
| Go — `golang.org/x/tools/cmd/deadcode` | Whole-program RTA from `main`/`init`, optional test roots, dynamic calls, runtime types, reflection-aware conservatism, and “why live” paths ([official command docs](https://pkg.go.dev/golang.org/x/tools/cmd/deadcode)) | Results are build-configuration-specific; `//go:linkname` can create false positives; generated and marker-interface methods are excluded by default; interface conformance can retain an otherwise unreachable method. |
| JVM architecture — ArchUnit | Bytecode-derived class/package dependencies with executable rules for layers, onion architecture, slices, cycles, modules, and allowed APIs ([ArchUnit user guide](https://www.archunit.org/userguide/html/000_Index.html)) | Imported-class coverage determines what can be checked; missing classes may be stubs, and tests/import filters change scope. It enforces declared rules; it does not infer business intent. |

The adapter contract should capture analyzer availability, exact command, version, build variant, exit status, parsed findings, and known blind spots. If a suitable analyzer is unavailable, downgrade confidence rather than imitating compiler semantics with regular expressions.

## Evidence and confidence model

Do not use a single `dead` label. Use scope-bound classes:

| Class | Required evidence | Default action |
| --- | --- | --- |
| `confirmed-unreachable` | Language/control-flow proof within a stated target and complete declared variant set; no unresolved dynamic channel | CI-blocking candidate; deletion still requires change authorization and verification. |
| `high-confidence-unused` | Ecosystem analyzer and graph agree; roots and manifests reconciled; no dynamic/framework/config signal found | Review for removal; never auto-delete in audit mode. |
| `probable-unused` | No discovered incoming path, but reflection, computed loading, environment conditions, external consumers, or variant coverage remains possible | Manual/runtime validation required. |
| `orphan-path` | Inventory path has no graph edge, root role, provenance role, or declared retention reason | Investigate ownership/provenance; binaries and docs may be intentionally standalone. |
| `architecture-violation` | A concrete dependency edge violates a versioned policy rule | Safe to gate when the policy and path mapping are unambiguous. |
| `design-smell` | SOLID/SoC/DRY/KISS/YAGNI or complexity judgment with file-level evidence | Advisory; require human design review. |
| `unknown-or-exempt` | Analyzer failure, unsupported syntax, generated/vendor policy, explicit exception, or incomplete root discovery | Report visibly; never count as clean. |

Confidence must be explained, not merely scored. Vulture's own 60–100% categories and `getattr` example show why a numeric estimate without dynamic-context evidence can mislead ([Vulture README](https://github.com/jendrikseipp/vulture/blob/main/README.md)). Runtime coverage can raise confidence that code is live, but non-execution only describes the observed run: official .NET documentation defines coverage as code run by unit tests ([Microsoft code-coverage guide](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-code-coverage)). It cannot prove that an unobserved production path is dead.

## Mandatory false-positive preflight

Before promoting an unused candidate, search and document each applicable channel:

1. computed imports/includes and string-based symbol lookup;
2. reflection, serialization/deserialization, ORM/schema mapping, and dependency injection;
3. routes, events, queues, commands, cron/scheduled jobs, plugin registries, decorators, and annotations;
4. framework auto-discovery by path, naming convention, glob, or metadata;
5. package exports, external/public library consumers, native/FFI/assembly calls, and generated bindings;
6. config, environment flags, build scripts, CI, containers, deployment descriptors, hooks, and service managers;
7. generated code that must exist before analysis and source maps back to inputs;
8. templates, HTML, CSS, schemas, migrations, localization, and asset references;
9. production versus test/example/story/benchmark-only use; and
10. every declared platform, architecture, feature, and build-tag variant.

Computed specifiers are a concrete blind spot in Knip; its recommended resolution is to declare the target as an entrypoint. Its docs also require some generated files to exist before analysis and recommend framework plugins or explicit entry patterns for auto-imported files ([Knip issue-resolution guide](https://knip.dev/guides/handling-issues)). Go RTA is deliberately conservative around reflection, treating exported methods of runtime types as reachable even though reflective edges are absent from its call graph ([Go RTA documentation](https://pkg.go.dev/golang.org/x/tools/go/callgraph/rta)). These are good cross-language precedents for retaining uncertainty explicitly.

## Enforce architecture through explicit policy, not slogans

Store repository-specific rules in a versioned policy (for example, `.architecture-hygiene.yml`) containing:

- named modules/layers and path/package mappings;
- public API/entrypoint declarations;
- allowed and forbidden dependency directions and edge types;
- cycle rules and module-isolation rules;
- production/test/generated/vendor classifications and variant matrix;
- retained standalone artifacts;
- exceptions with rule ID, precise scope, owner, rationale, creation date, and expiry/review date.

Architecture violations require an explicit rule. When no policy exists, the skill may infer candidate boundaries from manifests, namespaces, directories, ADRs, and dependency clusters, but it must label them **proposed**, not violated. ArchUnit provides the right conceptual model: declare package-to-layer mappings, allowed dependencies, cycle/module rules, then check observed edges; it also supports frozen/baselined violations for legacy adoption ([layers, slices, and modules](https://www.archunit.org/userguide/html/000_Index.html), [freezing configuration](https://www.archunit.org/userguide/html/000_Index.html#_configuration_2)).

Treat design principles as advisory lenses:

- **Separation of concerns** asks the reviewer to isolate aspects so they can be reasoned about independently; Dijkstra's original discussion is contextual, not a directory formula ([EWD447](https://www.cs.utexas.edu/~EWD/transcriptions/EWD04xx/EWD447.html)).
- **DRY** concerns a single authoritative representation of knowledge, not merely similar syntax; duplicate-looking code can represent different knowledge and premature abstraction can be harmful ([The Pragmatic Programmer extract](https://media.pragprog.com/titles/tpp20/dry.pdf)).
- **YAGNI** targets presumptive capability and abstraction, while explicitly not forbidding refactoring that keeps code malleable ([Martin Fowler's YAGNI](https://martinfowler.com/bliki/Yagni.html)).
- **KISS and SOLID** require contextual judgments about complexity, responsibilities, substitution, interfaces, and dependency direction. KISS originated as a broad engineering maxim rather than a software metric ([Lockheed Martin on Kelly Johnson](https://www.lockheedmartin.com/en-us/news/features/history/johnson.html)); Martin's primary SOLID material describes module/class design outcomes, not a universal folder layout ([Robert C. Martin's SOLID outline](https://cleancoder.com/files/solid.md)). Convert only repository-approved manifestations into deterministic rules. A code smell is an indicator requiring deeper inspection, not inherently a defect ([Martin Fowler on code smells](https://martinfowler.com/bliki/CodeSmell.html)).

This avoids contradictory enforcement: aggressive deduplication can violate KISS/YAGNI, while “one class, one responsibility” metrics can fragment cohesive modules.

## Skill and report design implications

Keep `SKILL.md` focused on the orchestration contract and move analyzer guidance and schemas into one-level references. Agent Skills load metadata first, then the entire skill body, then referenced resources on demand; the specification recommends keeping the body under 500 lines and using scripts for deterministic work ([Agent Skills specification](https://agentskills.io/specification)). OpenAI likewise recommends clear trigger words in `description`, imperative inputs/outputs, and scripts only where deterministic behavior or external tooling is needed ([OpenAI Codex skill guidance](https://developers.openai.com/codex/skills)).

Recommended skill contents:

- `SKILL.md`: scope contract, phases, confidence rules, safety/non-mutation rule, and report contract;
- `scripts/inventory.*`: deterministic NUL-safe inventory and ledger reconciliation with machine-readable JSON;
- `scripts/normalize-results.*`: optional normalization of analyzer outputs without pretending to parse unsupported languages;
- `references/evidence-model.md`: node/edge and confidence schema;
- `references/adapter-selection.md`: ecosystem detection, official analyzer commands, and blind spots;
- `references/architecture-policy.md`: policy schema, exception lifecycle, and CI adoption.

The final audit must contain:

1. scope and inventory reconciliation, including every excluded/metadata-only path;
2. discovered entrypoints, root sets, workspaces, and build variants;
3. tool versions, commands, configurations, failures, and blind spots;
4. module/dependency/cycle summary and explicit policy evaluation;
5. findings with evidence paths, counter-evidence checks, confidence class, and remediation;
6. a machine-readable file ledger; and
7. a limitations section listing unresolved dynamic channels and untested variants.

Audit mode should be read-only. Deletion belongs to a separately authorized remediation mode that removes one dependency-closed cluster at a time and reruns builds, tests, type checks, linters, packaging, architecture tests, and relevant variant checks. Continuous CI should gate only deterministic policy violations and scope-complete high-certainty findings; baseline legacy violations and fail on new ones, while keeping probable/design findings advisory.
