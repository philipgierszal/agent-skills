# Evidence Model

Use this model while constructing `ledger.json`. It separates repository coverage from semantic certainty.

## Nodes and roots

Model files, symbols, packages/modules, build targets, commands, configuration keys, assets, generated artifacts, runtime registries, and external/public contracts. Keep two root sets:

- `production`: shipped applications, library exports, services, CLIs, jobs, migrations, deploy/startup hooks, and required assets;
- `full-repository`: production plus tests, examples, fixtures, stories, benchmarks, documentation checks, and developer tooling.

Attach variant predicates to roots and relations: application/package, platform, architecture, feature/build flags, optional extras, and environment-specific configuration.

## Typed relations

Each file ledger row has a `relations` array. A relation contains:

- `kind`: import, call, re-export, inheritance, implementation, registration, reflection/string lookup, manifest/config/script/build/deploy reference, convention/glob discovery, generated-from/generates, template/asset/schema/migration reference, or another precise kind;
- `target`: repository path, fully qualified symbol, external identifier, or pattern;
- `target_type`: `file`, `symbol`, `external`, or `pattern`;
- `evidence`: source locations, analyzer artifacts, configuration locations, or runtime observations;
- `confidence`: `direct`, `declared`, `inferred`, or `observed`;
- `scopes`: production, test, development, build, deployment, and/or named variants.

Use `target_type: external` for ignored/generated/runtime targets absent from the inventory. A file with no outgoing relation still gets `relations: []`; its role and no-relation disposition need evidence.

## Finding classes

| Class | Evidence threshold | Default action |
| --- | --- | --- |
| `confirmed-unreachable` | Semantic/control-flow proof for all declared targets and variants; no unresolved dynamic channel | CI candidate; removal still needs authorization and verification. |
| `high-confidence-unused` | Native analyzer and evidence graph agree; roots/manifests reconciled; dynamic preflight closed | Review for removal; never auto-delete. |
| `probable-unused` | No discovered incoming path, but dynamic, external, or variant uncertainty remains | Runtime/manual validation. |
| `orphan-path` | No relation, root, provenance, or declared retention role | Investigate ownership and lifecycle. |
| `architecture-violation` | An observed edge violates a versioned, unambiguous policy rule | Gate when policy mapping and exception evaluation are deterministic. |
| `design-smell` | SOLID/SoC/DRY/KISS/YAGNI or complexity concern with file-level evidence | Human design review. |
| `unknown-or-exempt` | Tool failure, unsupported syntax, generated/vendor policy, exception, or incomplete roots/variants | Keep visible; never count as clean. |

Every finding needs a file or fully qualified symbol `subject`, source `location`, summary, evidence, counter-evidence checked, confidence rationale, action, and optional policy rule. Runtime non-observation is negative evidence only.

## Confidence promotion gate

Before promoting to `confirmed-unreachable` or `high-confidence-unused`, close every applicable channel:

1. computed imports/includes and string-based symbol lookup;
2. reflection, serialization, ORM/schema mapping, and dependency injection;
3. routes, events, queues, commands, schedules, registries, decorators, and annotations;
4. framework discovery by path, naming, glob, metadata, or package entry point;
5. package exports, external consumers, native/FFI calls, and generated bindings;
6. config, environment flags, build scripts, CI, containers, deployment descriptors, hooks, and service managers;
7. generators and required generated output;
8. templates, HTML, CSS, schemas, migrations, localization, media, and assets;
9. production versus test/example/story/benchmark reachability; and
10. declared application, platform, architecture, feature, and build variants.

An unresolved item belongs in `unresolved_dynamic_references` and prevents a high-certainty class.

## Design-principle evidence

- **SoC/SRP:** identify distinct reasons to change and knowledge scattered across files; do not infer responsibility from class count.
- **DRY:** find duplicated knowledge or business rules, not merely similar tokens. Similar code with separate domain ownership may be correct.
- **OCP/DIP/ISP/LSP:** inspect known variation, dependency direction, client needs, and behavioral contracts. Do not demand abstractions without real seams or adapters.
- **KISS:** compare complexity against required behavior and constraints, not line count alone.
- **YAGNI:** identify speculative capability or extension points with no current consumer while preserving refactoring that improves locality.

These create `design-smell` findings unless repository policy translates a specific manifestation into a deterministic rule.
