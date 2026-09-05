# Contributing

Thanks for improving these Agent Skills. Small, evidence-backed changes are welcome.

## Good contributions

For link-only upstream additions, follow the [collection maintenance guide](docs/maintaining-the-collection.md). Keep third-party packages outside `skills/` unless redistribution, provenance, testing, and maintenance ownership are established. A curated reference does not need a new skill-proposal issue because it does not change an installed skill's behavior.

- Corrections and clearer safety or evidence rules.
- Deterministic analyzer adapters and reference guidance.
- Tests for bundled scripts and output contracts.
- Verified, non-sensitive examples.
- New skills with a focused trigger, useful output, and explicit side effects.

Typo and link fixes can go straight to a pull request. Please open a skill-proposal issue before adding a skill or materially changing triggers, invocation policy, side effects, schemas, or compatibility. That keeps design discussion separate from implementation review.

## Set up

Requirements are Git and Python 3.10 or newer.

```bash
git clone https://github.com/philipgierszal/agent-skills.git
cd agent-skills
python -m pip install -r requirements-dev.txt
```

## Make a focused change

1. Read the owning `SKILL.md`, its relevant `references/`, tests, and evaluation record.
2. Add a failing test before changing executable behavior.
3. Keep runtime files inside `skills/<name>/`; keep maintainer tests, examples, research, and evaluations at repository root.
4. Preserve deterministic, read-only behavior unless the skill explicitly documents and requires authorization for a side effect.
5. Update the README catalog and verified example when the public contract changes.

For a new stable skill, frontmatter must include a directory-matching `name`, trigger-rich `description`, `license`, `metadata.author`, and truthful `metadata.compatibility`. The portable Agent Skills specification defines `compatibility` at the top level, but the current Codex validator rejects it; this repository uses the metadata field temporarily and mirrors the requirement in the README. Every relative link must resolve within the installed skill directory. Do not add empty folders or client/plugin manifests that are not tested and maintained.

## Behavioral evidence

Instruction changes can pass a linter while making an agent worse. Record before/after scenarios under `evals/` when changing trigger language, workflow order, confidence rules, safety boundaries, or completion gates. Include the tested client/model context and retain failures that explain the final design.

Paid or nondeterministic model evaluations are not required for every contributor checkout. Maintainers review their evidence separately; deterministic tests remain the merge gate.

## Validate

Run the complete local contract:

```bash
python -m unittest discover -s tests -v
python -m ruff check .
python -m compileall -q skills tests
python skills/architecture-hygiene-audit/scripts/validate_ledger.py \
  --inventory examples/architecture-hygiene-audit/inventory.json \
  --ledger examples/architecture-hygiene-audit/ledger.json
```

The example validator must report `Ledger valid: 2/2 paths reconciled.` Platform-specific filename tests may be skipped on Windows; other skips or failures need explanation.

## Pull requests

Keep pull requests narrow and explain the problem, the chosen approach, validation performed, behavioral evidence, documentation impact, and provenance. A human must review skill instructions before merge. Do not include private repository content or logs containing secrets.

If code, prose, fixtures, templates, data, or media came from elsewhere, record its source URL, version or commit, license, modifications, and required notices beside the owning material. Inspiration links alone do not authorize copying.

Security-sensitive findings do not belong in public issues or pull requests. Follow [`SECURITY.md`](SECURITY.md).
