# Illustrative Architecture Hygiene Report

This is a maintained example for a fictional two-file Python service. It demonstrates the report contract; it is not an audit of a real project.

## Scope

- Revision: `0123456789abcdef0123456789abcdef01234567`
- Production root: `src/main.py`
- Full-repository root: `src/main.py`; `src/legacy.py` is reachable from that root
- Analyzed variant: `linux-cpython-3.13`
- Inventory reconciliation: 2 of 2 paths
- Dynamic limitation: no production trace for string-based callable lookup

## Finding

### Probable unused symbol: `src.legacy:legacy_helper`

Location: `src/legacy.py:4`

The module is reachable because `src/main.py` imports it, but static call analysis found no analyzed caller for `legacy_helper`. Direct calls, tests, and configured entry points were checked. A string-based runtime lookup remains unresolved, so this is not a high-confidence finding and is not evidence that deletion is safe.

Recommended next action: exercise or observe production lookup paths. If that closes the dynamic channel, remove the symbol in a separately authorized change and rerun tests, packaging, startup, and the audit.

## Architecture policy

The observed `application -> legacy` import is allowed by rule `application-may-import-legacy`. No policy violation is reported.

## Conclusion

One probable-unused symbol was found within the documented roots, variant, static evidence, and dynamic-behavior limitations. The source tree was not changed.
