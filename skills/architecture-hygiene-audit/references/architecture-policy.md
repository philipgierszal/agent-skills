# Architecture Policy

Architecture enforcement requires an explicit, versioned repository policy. Search for an existing policy, architecture tests, ADRs, dependency rules, and package boundaries before proposing `.architecture-hygiene.yml`.

## Suggested policy shape

Use this only when the repository has no equivalent and the user authorizes creating policy:

```yaml
version: 1
modules:
  domain:
    paths: ["src/domain/**"]
    public_roots: ["src/domain/index.ts"]
  adapters:
    paths: ["src/adapters/**"]
rules:
  - id: domain-does-not-import-adapters
    from: domain
    forbid:
      target: adapters
      edge_kinds: [import, re-export]
cycles:
  forbid_between_modules: true
variants:
  - name: production
    targets: ["app"]
retained_paths:
  - path: "scripts/emergency-recovery.ts"
    reason: "Invoked from the operations runbook"
exceptions:
  - rule: domain-does-not-import-adapters
    scope: "src/domain/legacy-bridge.ts"
    owner: "architecture-team"
    rationale: "Migration bridge covered by ADR-0012"
    created: "2026-08-25"
    review_after: "2026-11-25"
```

Path mappings must be mutually understandable and edge kinds explicit. Validate rules against actual package aliases, generated paths, workspace boundaries, and build variants.

## Evaluation rules

An `architecture-violation` needs:

1. a stable policy rule ID;
2. unambiguous source and target module mapping;
3. a typed observed edge with source location;
4. matching scope and variant;
5. evaluated exception status; and
6. a remediation that preserves required behavior.

If any item is missing, emit a proposed rule or `design-smell`, not a violation. Directory shape alone does not establish business architecture.

## Design principles are not universal gates

- DRY violations concern duplicated knowledge; token duplication is a candidate signal.
- SoC/SRP concern independent reasoning and reasons to change; file/class size is a candidate signal.
- OCP, DIP, ISP, and LSP need actual variation, dependency direction, clients, and behavioral contracts.
- KISS compares incidental complexity against required behavior.
- YAGNI rejects presumptive features but does not forbid locality-improving refactoring.

Aggressive deduplication can conflict with KISS and YAGNI. Universal interfaces can conflict with ISP. Resolve these through evidence and domain intent, not a point score.

## Legacy adoption and CI

Baseline known legacy violations by exact rule, edge, and scope, then fail only on regressions. Exceptions need an owner, rationale, precise scope, creation date, and review/expiry date. Do not let a broad directory exception suppress unrelated future edges.

CI may gate:

- deterministic policy violations;
- inventory/ledger reconciliation failures for audit jobs; and
- repository-approved high-certainty unused-code rules with complete root/variant coverage.

Keep `probable-unused`, `orphan-path`, and `design-smell` advisory until reviewed. Never make a newly introduced tool warning blocking without validating its model and establishing a baseline.
