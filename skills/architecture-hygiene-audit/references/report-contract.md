# Report Contract

Write audit artifacts outside the repository by default. If the user requests committed reports, generate the inventory before creating them and follow the repository's documentation convention.

## Required artifacts

```text
<audit-dir>/
├── inventory.json
├── ledger.json
├── report.md
└── raw/
    ├── commands.md
    └── <analyzer outputs>
```

`inventory.json` comes only from `scripts/inventory.py`. `ledger.json` is the machine-readable evidence graph and disposition record. `raw/commands.md` records commands, versions, working directories, configuration, scopes/variants, exit codes, and output paths.

## Ledger example

This example is complete for one path; real ledgers contain exactly one row for every inventory path:

```json
{
  "ledger_version": 1,
  "inventory_revision": "0123456789abcdef",
  "variants_analyzed": ["production/windows-x64", "full-repository/windows-x64"],
  "unresolved_channels": ["Linux deployment variant was not available"],
  "files": [
    {
      "path": "src/orders/validate.ts",
      "review_status": "content-reviewed",
      "role": "Order validation policy",
      "reachability": "reachable",
      "evidence": ["knip-full.json", "src/orders/submit.ts:14"],
      "relations": [
        {
          "kind": "import",
          "target": "src/orders/types.ts",
          "target_type": "file",
          "evidence": ["src/orders/validate.ts:1"],
          "confidence": "direct",
          "scopes": ["production", "test"]
        }
      ],
      "unresolved_dynamic_references": [],
      "findings": [
        {
          "class": "design-smell",
          "subject": "src/orders/validate.ts::validateOrder",
          "location": "src/orders/validate.ts:8",
          "summary": "Validation duplicates syntax but represents Order-specific knowledge",
          "evidence": ["src/returns/validate.ts:7", "CONTEXT.md:Order"],
          "counter_evidence_checked": ["The rules have different owners and change histories"],
          "confidence_rationale": "DRY does not justify coupling separate domain policies",
          "action": "Keep separate; review only shared value-level primitives"
        }
      ]
    }
  ]
}
```

For `metadata-only` or `excluded`, add a non-empty `review_rationale`. For `architecture-violation`, add `policy_rule`. Every finding requires a source-located subject, including unused methods and exports.

## Human report

`report.md` contains:

1. audited revision, dirty state, scope, exclusions, and artifact hashes;
2. inventory reconciliation counts by file role and review status;
3. workspaces/modules, production roots, full-repository roots, and analyzed/missing variants;
4. analyzer commands, versions, failures, blind spots, and raw evidence links;
5. module dependency/cycle summary and explicit policy evaluation;
6. findings grouped by class, each with subject/location, evidence, counter-evidence, rationale, affected scopes/variants, and safe action;
7. orphan and unknown/exempt path tables;
8. unresolved dynamic channels, external-consumer gaps, and unsupported syntax/tools;
9. proposed deterministic CI rules versus advisory design reviews; and
10. limitations and the exact calibrated conclusion.

Do not collapse unknown/exempt rows into “clean.” A generated, vendored, binary, or standalone file remains visible with provenance and disposition.

## Validation and claim gate

Run:

```bash
python "<SKILL_ROOT>/scripts/validate_ledger.py" --inventory "<audit-dir>/inventory.json" --ledger "<audit-dir>/ledger.json"
```

Do not call the audit exhaustive if validation fails. Do not say “there is no dead code.” Use:

> No known findings within the documented roots, variants, tools, and dynamic-behavior model. Unresolved limitations are listed below.

If any analyzer, root family, dynamic channel, external consumer, or declared variant is unresolved, name it immediately after that sentence.
