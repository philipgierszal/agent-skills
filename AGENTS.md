# Repository Guide for Coding Agents

This repository publishes reusable Agent Skills. Keep the installable boundary small, portable, deterministic, and safe.

## Before editing

- Read the owning `skills/<name>/SKILL.md` and only the references needed for the change.
- Read the matching evaluation record and tests before changing triggers, safety rules, scripts, or output contracts.
- Keep work focused on the requested skill or repository surface. Do not add plugin manifests, release frameworks, category folders, or generated scaffolding without a concrete supported distribution need.

## Skill contract

- Each stable skill lives at `skills/<name>/SKILL.md`; its frontmatter `name` must match the directory.
- State the installed unit's license in `license`. Because the currently tested Codex `quick_validate.py` rejects the Agent Skills specification's top-level `compatibility` field, record real runtime requirements in `metadata.compatibility` and mirror them in the README.
- Put runtime helpers in the skill's `scripts/`, progressive detail in `references/`, and client-specific presentation in `agents/`.
- Preserve safe defaults. A documentation change must not silently authorize writes, deletion, deployment, or external messages.
- Treat analyzer output as evidence, not ground truth. Keep limitations and counter-evidence visible.
- Use relative links within a skill so the installed directory remains self-contained.

## Verification

Run focused tests while editing, then the full contract before handoff:

```bash
python -m unittest discover -s tests -v
python -m ruff check .
python -m compileall -q skills tests
python skills/architecture-hygiene-audit/scripts/validate_ledger.py \
  --inventory examples/architecture-hygiene-audit/inventory.json \
  --ledger examples/architecture-hygiene-audit/ledger.json
```

When behavior changes, update or add evaluation evidence under `evals/`. When public usage changes, update the README, example, and contribution guidance in the same change.

## Public repository hygiene

- Never commit secrets, access tokens, customer data, private repository excerpts, or workstation-specific paths.
- Include source and license provenance beside copied code, data, templates, or media.
- Do not claim compatibility with a client or platform that was not tested.
- Keep `main` releasable; do not add a tag or release until public installation and remote CI are verified.
