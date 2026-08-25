# Architecture Hygiene Audit Example

This directory contains a small, illustrative audit of a fictional Python service. It shows the artifact contract without presenting the result as evidence from a real project.

The example includes:

- [`.architecture-hygiene.yml`](.architecture-hygiene.yml), an explicit dependency policy;
- [`inventory.json`](inventory.json), the two-path frozen scope;
- [`ledger.json`](ledger.json), one disposition per inventoried path; and
- [`report.md`](report.md), the corresponding human-readable result.

Validate the machine-readable artifacts from the repository root:

```bash
python skills/architecture-hygiene-audit/scripts/validate_ledger.py \
  --inventory examples/architecture-hygiene-audit/inventory.json \
  --ledger examples/architecture-hygiene-audit/ledger.json
```

Expected output:

```text
Ledger valid: 2/2 paths reconciled.
```

The example deliberately reports a `probable-unused` symbol rather than claiming safe deletion. A real audit must discover the target repository's own roots, variants, dynamic behavior, external consumers, and native analyzers.
