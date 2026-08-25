## Problem

Describe the user or maintainer problem this change solves.

## Change

Explain the chosen approach and important alternatives considered.

## Verification

- [ ] `python -m unittest discover -s tests -v`
- [ ] `python -m ruff check .`
- [ ] `python -m compileall -q skills tests`
- [ ] The maintained example passes `validate_ledger.py`.
- [ ] I manually reviewed the changed skill instructions and safety boundaries.

## Behavioral evidence

Link or summarize RED/GREEN scenarios when triggers, workflow, confidence, side effects, or completion behavior changed. Write `Not applicable — no behavior change` only when that is true.

## Documentation and provenance

- [ ] Public installation, catalog, examples, and compatibility docs are current.
- [ ] Evaluations are current for behavioral changes.
- [ ] Third-party material includes source, version/commit, license, modifications, and required notices.
- [ ] The change contains no secrets, customer data, private repository excerpts, or workstation-specific paths.
