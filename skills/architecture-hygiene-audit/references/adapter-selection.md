# Analyzer Adapter Selection

Choose tools after discovering ecosystems, workspaces, roots, and variants. Prefer repository-pinned commands and existing configuration; consult each installed tool's `--help` rather than assuming current flags. Do not install packages, edit configuration, or generate source without authorization. Record unavailable analyzers as coverage gaps.

## Adapter contract

For every analyzer invocation record:

- ecosystem, workspace/target, root set, and variant;
- exact command, executable/package version, configuration, working directory, and environment inputs;
- exit status, stdout/stderr, raw output path, and parse/normalization method;
- findings and graph edges with source locations; and
- documented blind spots plus repository-specific dynamic channels.

Tool output is evidence, not the final finding class. Reconcile it against manifests, conventions, runtime/configuration edges, and external contracts.

## Routing examples

| Evidence detected | Preferred adapter | Required caveat |
| --- | --- | --- |
| JavaScript/TypeScript manifests and an existing Knip setup | Run configured Knip full-repository and production analyses; also run project type/lint/build checks | Entry files define reachability. Computed imports, missing framework plugins, auto-imports, generated files, config references, and uncommon formats can hide edges. See [Knip entry files](https://knip.dev/explanations/entry-files), [production mode](https://knip.dev/features/production-mode), and [issue handling](https://knip.dev/guides/handling-issues). |
| Python packages or applications with Vulture available | Run Vulture across declared packages and relevant variants; preserve confidence and whitelist/config behavior | Dynamic lookup, decorators, implicit protocol calls, entry points, fixtures, and framework registration cause false positives. See the [Vulture repository](https://github.com/jendrikseipp/vulture). |
| Go modules with executable roots | Run the official Go `deadcode` analyzer for each declared `GOOS`, `GOARCH`, build-tag, package, and test-root variant | A report is configuration-specific and is not automatic deletion permission. Reflection and interface conformance are conservative; `go:linkname` can hide use. See [official `deadcode` docs](https://pkg.go.dev/golang.org/x/tools/cmd/deadcode). |
| JVM bytecode and existing architecture tests | Run existing ArchUnit tests/rules and normal build/test tooling | Imported-class filters and missing classes limit coverage. ArchUnit enforces declared rules; it does not infer business intent. See the [ArchUnit user guide](https://www.archunit.org/userguide/html/000_Index.html). |
| .NET projects | Run repository compiler/analyzer/build/test commands and inspect reflection, DI, serializers, source generation, trimming, and deployment roots | Coverage proves observed execution, not deadness; see [Microsoft code-coverage guidance](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-code-coverage). |
| Other or mixed ecosystems | Use project-pinned compilers, linkers, language servers, linters, dependency analyzers, test collectors, packaging tools, and build graph tools | If semantic tooling is absent or a language is unsupported, use `unknown-or-exempt`/`probable-unused`; never promote regex-only results. |

## Root and variant reconciliation

Run analyzers from the correct workspace and configuration. Compare at least production/shipped and full-repository modes. Enumerate build variants rather than merging incompatible results. A symbol reachable only in tests is live in the full graph but may still be absent from production; an optional feature is unknown unless that feature was analyzed.

If code generation is required for truthful analysis, identify the generator and inputs first. Run it only with authorization, in a disposable/clean workspace, and verify it did not introduce unrelated source changes.

## Corroborating indirect edges

Search text and configuration for string-driven references, but capture exact source locations and mechanisms. Inspect package metadata, exports, command/task definitions, CI, containers, deployment descriptors, templates, routes, registries, plugin entry points, serializers, migration graphs, resource loaders, and documentation contracts. Mark unresolved computed patterns explicitly.
