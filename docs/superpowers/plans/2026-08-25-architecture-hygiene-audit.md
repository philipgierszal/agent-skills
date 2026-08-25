# Architecture Hygiene Audit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build, behaviorally verify, install, and publish a reusable `architecture-hygiene-audit` Codex skill that proves per-file audit coverage without overstating dead-code certainty.

**Architecture:** A concise orchestrator skill delegates semantic analysis to ecosystem-native tools and uses two deterministic Python helpers for Git inventory and ledger reconciliation. Progressive references define evidence, report, architecture-policy, and analyzer-adapter contracts; audit mode remains read-only.

**Tech Stack:** Agent Skills/Codex `SKILL.md`, YAML UI metadata, Python 3 standard library, `unittest`, Git, GitHub CLI.

---

## File Map

- `evals/architecture-hygiene-audit.md`: baseline and post-skill behavioral scenarios, observed gaps, and evaluation rubric.
- `skills/architecture-hygiene-audit/SKILL.md`: discovery metadata, scope contract, audit workflow, safety gate, completion criteria.
- `skills/architecture-hygiene-audit/agents/openai.yaml`: UI metadata and implicit invocation policy.
- `skills/architecture-hygiene-audit/scripts/inventory.py`: deterministic Git path inventory.
- `skills/architecture-hygiene-audit/scripts/validate_ledger.py`: schema and inventory reconciliation gate.
- `skills/architecture-hygiene-audit/references/evidence-model.md`: graph, finding, confidence, and dynamic-channel model.
- `skills/architecture-hygiene-audit/references/adapter-selection.md`: ecosystem-native analyzer routing and limitations.
- `skills/architecture-hygiene-audit/references/architecture-policy.md`: repository policy and exception schema.
- `skills/architecture-hygiene-audit/references/report-contract.md`: machine and human report requirements.
- `tests/test_inventory.py`: inventory behavior tests in temporary Git repositories.
- `tests/test_validate_ledger.py`: ledger reconciliation and confidence-gate tests.
- `README.md`: repository purpose, installation, invocation, and development commands.
- `LICENSE`: MIT license for the custom repository.

### Task 1: Preserve the failing behavioral baseline

**Files:**
- Create: `evals/architecture-hygiene-audit.md`

- [ ] **Step 1: Record the three existing baseline scenarios**

Include the TypeScript monorepo/Knip deadline scenario, the conflicting SOLID/SoC/DRY/KISS/YAGNI enforcement scenario, and the Python/Vulture plugin scenario verbatim enough to rerun. Define this rubric:

```markdown
| Criterion | Required behavior |
| --- | --- |
| Scope proof | Uses deterministic inventory and exact ledger reconciliation |
| Roots | Separates production and full-repository roots |
| Variants | Records analyzed and missing build/runtime variants |
| Dynamic behavior | Checks reflection, computed imports, registration, config, generation, framework conventions, and external consumers |
| Evidence | Uses typed, source-located evidence and calibrated finding classes |
| Architecture | Gates explicit versioned rules; keeps design principles advisory |
| Safety | Audit remains read-only and makes no deletion claim |
| Claim | Says only “no known findings under the documented model” |
```

- [ ] **Step 2: Capture baseline observations verbatim**

Record the useful baseline decisions plus the unresolved failure: both agents promised comprehensive ledgers (`"Inventory all 12,000 files mechanically"` and `"I would create one path ledger"`) without an executable reconciliation contract, so completeness depended on prose rather than a machine check.

- [ ] **Step 3: Commit the RED artifact**

```bash
git add evals/architecture-hygiene-audit.md
git commit -m "test: capture architecture audit baseline"
```

### Task 2: Write failing inventory tests

**Files:**
- Create: `tests/test_inventory.py`
- Test: `tests/test_inventory.py`

- [ ] **Step 1: Write tests before the helper exists**

Use `unittest`, `tempfile.TemporaryDirectory`, and `subprocess.run`. Load `skills/architecture-hygiene-audit/scripts/inventory.py` through `importlib.util` only after it exists. Tests must create a temporary Git repository with a tracked Unicode filename, a tracked filename containing spaces, a non-ignored untracked file, an ignored file, and a symlink when supported. Assert:

```python
self.assertEqual(
    [entry["path"] for entry in result["files"]],
    sorted(["docs/żółć note.md", "src/main file.py", "src/untracked.py"]),
)
self.assertNotIn("build/ignored.py", {entry["path"] for entry in result["files"]})
self.assertEqual(result["inventory_version"], 1)
self.assertTrue(all(entry["sha256"] for entry in result["files"]))
```

Also assert the helper rejects a non-Git directory with a clear `InventoryError`.

- [ ] **Step 2: Run the focused test and verify RED**

Run: `python -m unittest tests.test_inventory -v`

Expected: FAIL because `skills/architecture-hygiene-audit/scripts/inventory.py` does not exist.

- [ ] **Step 3: Commit the failing tests**

```bash
git add tests/test_inventory.py
git commit -m "test: specify deterministic repository inventory"
```

### Task 3: Implement deterministic inventory

**Files:**
- Create: `skills/architecture-hygiene-audit/scripts/inventory.py`
- Test: `tests/test_inventory.py`

- [ ] **Step 1: Implement the minimal inventory interface**

Provide these functions and CLI:

```python
class InventoryError(RuntimeError):
    pass

def build_inventory(repo: Path) -> dict[str, object]:
    """Return a stable inventory of tracked and non-ignored untracked paths."""

def write_inventory(repo: Path, output: Path) -> None:
    output.write_text(
        json.dumps(build_inventory(repo), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

def main(argv: Sequence[str] | None = None) -> int:
    # --repo and --output; print a specific error and return 2 on InventoryError
```

Use `git -C <repo> ls-files --cached --others --exclude-standard -z` and parse bytes on NUL boundaries. Determine tracked paths from a separate cached query and Git modes from `git ls-files --stage -z`. Normalize paths to POSIX form, sort paths, record `tracked`, `git_mode`, `kind`, `size_bytes`, and SHA-256. Record `revision` and dirty state. Treat mode `160000` as `submodule` and symlinks explicitly. Never descend through path text returned by another shell.

- [ ] **Step 2: Run inventory tests and verify GREEN**

Run: `python -m unittest tests.test_inventory -v`

Expected: all inventory tests PASS.

- [ ] **Step 3: Commit inventory implementation**

```bash
git add skills/architecture-hygiene-audit/scripts/inventory.py tests/test_inventory.py
git commit -m "feat: add deterministic Git inventory"
```

### Task 4: Write failing ledger-validation tests

**Files:**
- Create: `tests/test_validate_ledger.py`
- Test: `tests/test_validate_ledger.py`

- [ ] **Step 1: Define minimal valid fixtures and failure cases**

Create inventory and ledger dictionaries in test helpers. A valid file record has:

```python
{
    "path": "src/main.py",
    "review_status": "content-reviewed",
    "role": "production entrypoint",
    "reachability": "root",
    "evidence": ["pyproject.toml:project.scripts"],
    "unresolved_dynamic_references": [],
    "findings": [],
}
```

Assert `validate(inventory, ledger)` accepts full coverage and rejects missing, duplicate, and unexpected paths; invalid enum values; empty evidence; missing rationales for `metadata-only` or `excluded`; and high-certainty findings that retain unresolved dynamic references or omit counter-evidence checks.

- [ ] **Step 2: Run the focused test and verify RED**

Run: `python -m unittest tests.test_validate_ledger -v`

Expected: FAIL because `skills/architecture-hygiene-audit/scripts/validate_ledger.py` does not exist.

- [ ] **Step 3: Commit the failing tests**

```bash
git add tests/test_validate_ledger.py
git commit -m "test: specify audit ledger reconciliation"
```

### Task 5: Implement the ledger gate

**Files:**
- Create: `skills/architecture-hygiene-audit/scripts/validate_ledger.py`
- Test: `tests/test_validate_ledger.py`

- [ ] **Step 1: Implement validation without semantic analysis**

Expose:

```python
REVIEW_STATUSES = {"content-reviewed", "tool-reviewed", "metadata-only", "excluded"}
REACHABILITY = {"root", "reachable", "unreachable", "candidate", "unknown", "not-applicable"}
FINDING_CLASSES = {
    "confirmed-unreachable", "high-confidence-unused", "probable-unused",
    "orphan-path", "architecture-violation", "design-smell", "unknown-or-exempt",
}
HIGH_CERTAINTY = {"confirmed-unreachable", "high-confidence-unused", "architecture-violation"}

class LedgerValidationError(ValueError):
    def __init__(self, errors: list[str]): ...

def validate(inventory: dict[str, object], ledger: dict[str, object]) -> None:
    """Raise LedgerValidationError with all discovered contract violations."""
```

The CLI accepts `--inventory` and `--ledger`, prints every error, exits `2` on invalid input, and prints `Ledger valid: N/N paths reconciled.` on success. It must aggregate errors so one run exposes all repair work.

- [ ] **Step 2: Run ledger tests and verify GREEN**

Run: `python -m unittest tests.test_validate_ledger -v`

Expected: all ledger tests PASS.

- [ ] **Step 3: Commit ledger implementation**

```bash
git add skills/architecture-hygiene-audit/scripts/validate_ledger.py tests/test_validate_ledger.py
git commit -m "feat: validate exhaustive audit ledgers"
```

### Task 6: Initialize and author the skill

**Files:**
- Create: `skills/architecture-hygiene-audit/SKILL.md`
- Create: `skills/architecture-hygiene-audit/agents/openai.yaml`
- Create: `skills/architecture-hygiene-audit/references/evidence-model.md`
- Create: `skills/architecture-hygiene-audit/references/adapter-selection.md`
- Create: `skills/architecture-hygiene-audit/references/architecture-policy.md`
- Create: `skills/architecture-hygiene-audit/references/report-contract.md`

- [ ] **Step 1: Initialize only the required resource directories**

Run:

```bash
python ~/.codex/skills/.system/skill-creator/scripts/init_skill.py architecture-hygiene-audit --path skills --resources scripts,references --interface display_name="Architecture Hygiene Audit" --interface short_description="Audit repository architecture and dead-code evidence" --interface default_prompt="Use $architecture-hygiene-audit to audit this repository exhaustively."
```

Because `scripts/` already exists, preserve it; if the initializer rejects the existing folder, create `SKILL.md`, `agents/openai.yaml`, and `references/` directly with the same schema rather than reinitializing or deleting scripts.

- [ ] **Step 2: Write discriminating metadata**

Use this frontmatter:

```yaml
---
name: architecture-hygiene-audit
description: Use when asked to audit an entire repository for dead code, orphaned files, unused methods or exports, dependency cycles, architecture-rule violations, repository structure problems, or SOLID, separation-of-concerns, DRY, KISS, and YAGNI concerns.
---
```

Keep implicit invocation enabled. The body must explicitly require exhaustive inventory, root/variant discovery, native analyzers, dynamic-channel preflight, typed evidence, exact ledger reconciliation, read-only behavior, and calibrated claims. It must route to each reference only at the phase that needs it and stay under 500 lines.

- [ ] **Step 3: Write the progressive references**

`evidence-model.md` defines node/edge provenance, the seven finding classes, confidence promotion conditions, and dynamic false-positive channels. `adapter-selection.md` routes JavaScript/TypeScript to Knip or existing compiler/linter tools, Python to Vulture or existing analyzers, Go to official `deadcode`, JVM architecture to ArchUnit, and unknown ecosystems to native project tools with downgraded confidence. `architecture-policy.md` defines `.architecture-hygiene.yml`, explicit rules, proposed boundaries, exceptions, baselining, and deterministic CI gates. `report-contract.md` defines `inventory.json`, `ledger.json`, the Markdown report, raw tool evidence, and the claim language.

- [ ] **Step 4: Validate authoring constraints**

Run:

```bash
python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/architecture-hygiene-audit
```

Expected: `Skill is valid!`

- [ ] **Step 5: Commit the authored skill**

```bash
git add skills/architecture-hygiene-audit
git commit -m "feat: add architecture hygiene audit skill"
```

### Task 7: Verify behavioral GREEN and refactor gaps

**Files:**
- Modify: `evals/architecture-hygiene-audit.md`
- Modify if observations require: `skills/architecture-hygiene-audit/SKILL.md`
- Modify if observations require: `skills/architecture-hygiene-audit/references/*.md`

- [ ] **Step 1: Run independent evaluations with the skill loaded**

Give fresh agents each baseline scenario plus only the new skill path. Require an actionable audit plan and artifact contract, but do not reveal the rubric or baseline gaps.

- [ ] **Step 2: Score every response against the eight-criterion rubric**

All scenarios must satisfy scope proof, roots, variants, dynamic behavior, evidence, architecture, safety, and calibrated-claim requirements. Capture exact misses or rationalizations.

- [ ] **Step 3: Make the minimum evidence-supported instruction changes**

Only change the skill where an evaluation demonstrates a gap. Re-run the failed scenario and keep all prior scenarios green.

- [ ] **Step 4: Record GREEN results and commit**

```bash
git add evals/architecture-hygiene-audit.md skills/architecture-hygiene-audit
git commit -m "test: verify architecture audit behavior"
```

### Task 8: Document, install, and publish

**Files:**
- Create: `README.md`
- Create: `LICENSE`
- Modify: design document only to remove any trailing whitespace found by Git checks.

- [ ] **Step 1: Add repository documentation and MIT license**

Document installation with:

```bash
npx skills@latest add philipgierszal/agent-skills --skill architecture-hygiene-audit
```

Also document manual Codex installation, `$architecture-hygiene-audit` invocation, read-only guarantees, tests, research provenance, and why this is not a Matt Pocock fork. Use an MIT license copyrighted `2026 Philip Gierszal`.

- [ ] **Step 2: Run the full verification suite**

Run:

```bash
python -m unittest discover -s tests -v
python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/architecture-hygiene-audit
python skills/architecture-hygiene-audit/scripts/inventory.py --repo . --output "$TEMP/architecture-hygiene-inventory.json"
```

Create a complete smoke-test ledger for the inventory, validate it, run `git diff --check`, and inspect `git status --short`.

- [ ] **Step 3: Install the verified skill**

Install from the local repository into `~/.codex/skills/architecture-hygiene-audit`. Refuse to overwrite an unrelated existing destination. Compare source and installed directory hashes after copying.

- [ ] **Step 4: Commit documentation**

```bash
git add README.md LICENSE docs skills tests evals
git commit -m "docs: publish custom agent skills repository"
```

- [ ] **Step 5: Create the private GitHub repository and push**

Run:

```bash
gh repo create philipgierszal/agent-skills --private --source . --remote origin --push --description "Reusable custom agent skills for Codex and compatible agents"
```

- [ ] **Step 6: Verify publication and installation**

Confirm the remote default branch and HEAD SHA with `gh repo view` and `gh api`, compare it with local `git rev-parse HEAD`, verify `git status --short --branch` is clean and tracking `origin/main`, rerun skill validation from the installed path, and compare installed source files with the committed skill.

