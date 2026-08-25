# Public Agent Skills Repository Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish `philipgierszal/agent-skills` as a trustworthy public catalog with clear installation, a verified example, contributor guidance, and deterministic CI.

**Architecture:** Preserve `skills/<name>/` as the only installable boundary and keep development material at repository root. Add a package-contract test first, then make metadata, examples, documentation, and CI satisfy that contract before changing GitHub visibility and discovery settings.

**Tech Stack:** Agent Skills `SKILL.md`, Markdown, YAML, JSON, Python 3.10+, PyYAML, `unittest`, Ruff, Git, GitHub Actions, GitHub CLI.

---

## File Map

- `README.md`: public landing page, installation, use, catalog, compatibility, maintenance, and project links.
- `AGENTS.md`: concise repository rules for humans using coding agents.
- `CONTRIBUTING.md`: accepted changes, workflow, validation, behavioral evidence, and provenance.
- `SECURITY.md`: supported version and private vulnerability-reporting route.
- `requirements-dev.txt`: pinned local/CI lint and YAML-validation dependencies.
- `.github/ISSUE_TEMPLATE/bug.yml`: reproducible defect intake.
- `.github/ISSUE_TEMPLATE/skill-proposal.yml`: new-skill and behavior-change intake.
- `.github/PULL_REQUEST_TEMPLATE.md`: focused review and verification checklist.
- `.github/workflows/validate.yml`: least-privilege Windows/Linux validation matrix.
- `skills/architecture-hygiene-audit/SKILL.md`: portable license and compatibility metadata.
- `examples/architecture-hygiene-audit/*`: maintained illustrative policy, inventory, ledger, and report.
- `tests/test_skill_package.py`: stable package, link, and example-integrity contract.

### Task 1: Establish the public package contract with a failing test

**Files:**
- Create: `tests/test_skill_package.py`

- [ ] **Step 1: Write the metadata and public-file tests**

Create a `unittest.TestCase` that:

```python
from __future__ import annotations

import importlib.util
import json
import re
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "architecture-hygiene-audit"


def load_frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", maxsplit=2)
    if len(parts) != 3 or parts[0].strip():
        raise AssertionError(f"{path} must start with YAML frontmatter")
    value = yaml.safe_load(parts[1])
    if not isinstance(value, dict):
        raise TypeError(f"{path} frontmatter must be a mapping")
    return value


class SkillPackageTests(unittest.TestCase):
    def test_stable_skills_have_codex_compatible_metadata(self) -> None:
        skill_files = sorted((ROOT / "skills").glob("*/SKILL.md"))
        self.assertTrue(skill_files)

        for skill_file in skill_files:
            frontmatter = load_frontmatter(skill_file)
            metadata = frontmatter.get("metadata")
            with self.subTest(skill=skill_file.parent.name):
                self.assertEqual(skill_file.parent.name, frontmatter.get("name"))
                self.assertIsInstance(frontmatter.get("description"), str)
                self.assertEqual("MIT", frontmatter.get("license"))
                self.assertNotIn("compatibility", frontmatter)
                self.assertIsInstance(metadata, dict)
                if not isinstance(metadata, dict):
                    self.fail("metadata must be a mapping")
                self.assertEqual("philipgierszal", metadata.get("author"))
                self.assertRegex(
                    str(metadata.get("compatibility", "")),
                    r"Git.*Python 3\.10\+",
                )

    def test_public_community_files_exist(self) -> None:
        for relative in (
            "AGENTS.md",
            "CONTRIBUTING.md",
            "SECURITY.md",
            ".github/ISSUE_TEMPLATE/bug.yml",
            ".github/ISSUE_TEMPLATE/skill-proposal.yml",
            ".github/PULL_REQUEST_TEMPLATE.md",
            ".github/workflows/validate.yml",
        ):
            with self.subTest(path=relative):
                self.assertTrue((ROOT / relative).is_file(), relative)
```

- [ ] **Step 2: Add relative-link and example reconciliation tests**

In the same class, scan Markdown links in every skill Markdown file, ignore absolute/scheme/anchor links, and assert each relative target exists. Dynamically import `validate_ledger.py`, load the example `inventory.json` and `ledger.json`, and call `validate(inventory, ledger)`.

- [ ] **Step 3: Run the test and observe RED**

Run:

```bash
python -m unittest tests.test_skill_package -v
```

Expected: failures for missing metadata, community files, and example files. Failures must be missing-contract failures, not syntax or import errors.

- [ ] **Step 4: Commit the RED contract**

```bash
git add tests/test_skill_package.py
git commit -m "test: define public skill package contract"
```

### Task 2: Add truthful skill metadata and a validator-backed example

**Files:**
- Modify: `skills/architecture-hygiene-audit/SKILL.md`
- Create: `examples/architecture-hygiene-audit/README.md`
- Create: `examples/architecture-hygiene-audit/.architecture-hygiene.yml`
- Create: `examples/architecture-hygiene-audit/inventory.json`
- Create: `examples/architecture-hygiene-audit/ledger.json`
- Create: `examples/architecture-hygiene-audit/report.md`

- [ ] **Step 1: Extend frontmatter with actual package constraints**

Insert below the description:

```yaml
license: MIT
metadata:
  author: philipgierszal
  compatibility: Requires Git and Python 3.10+; designed for coding agents with shell access.
```

- [ ] **Step 2: Create the illustrative artifact set**

Use the shared revision `0123456789abcdef0123456789abcdef01234567` and digest `sha256:architecture-hygiene-example-v1` in both JSON documents. Inventory exactly `src/main.py` and `src/legacy.py`. Give both paths complete ledger records; make `src/main.py` a production root and `src/legacy.py` a candidate with one `probable-unused` symbol finding. Keep uncertainty explicit and do not claim safe deletion.

The policy defines `application` and `legacy` path modules, allows `application -> legacy`, and identifies `src/main.py` as the production root. The report states that it is illustrative, records the two analyzed root scopes and one Linux CPython variant, and recommends runtime verification before removal.

- [ ] **Step 3: Validate the example directly**

```bash
python skills/architecture-hygiene-audit/scripts/validate_ledger.py \
  --inventory examples/architecture-hygiene-audit/inventory.json \
  --ledger examples/architecture-hygiene-audit/ledger.json
```

Expected: `Ledger valid: 2/2 paths reconciled.`

- [ ] **Step 4: Re-run the package test**

```bash
python -m unittest tests.test_skill_package -v
```

Expected: example and metadata assertions pass; community-file assertions remain RED.

- [ ] **Step 5: Commit the installable metadata and example**

```bash
git add skills/architecture-hygiene-audit/SKILL.md examples tests/test_skill_package.py
git commit -m "feat: add verified architecture audit example"
```

### Task 3: Build the public onboarding and contribution surface

**Files:**
- Modify: `README.md`
- Create: `AGENTS.md`
- Create: `CONTRIBUTING.md`
- Create: `SECURITY.md`
- Create: `.github/ISSUE_TEMPLATE/bug.yml`
- Create: `.github/ISSUE_TEMPLATE/skill-proposal.yml`
- Create: `.github/PULL_REQUEST_TEMPLATE.md`

- [ ] **Step 1: Rewrite the landing page around user actions**

Lead with the evidence-first promise, validation and MIT badges, then publish these commands:

```bash
npx skills@latest add philipgierszal/agent-skills --skill architecture-hygiene-audit
npx skills@latest add philipgierszal/agent-skills --skill architecture-hygiene-audit --global --agent codex
npx skills@latest add philipgierszal/agent-skills --list
```

Give explicit and implicit invocation examples, a one-row catalog with Stable/read-only status, a link to the verified example, Git/Python 3.10 requirements, update/removal commands, validation commands, and links to contribution, security, research, and license documents. Remove the private-authentication warning.

- [ ] **Step 2: Add the maintainer and contributor contracts**

`AGENTS.md` requires reading the owning skill and references before editing, running focused tests first, preserving safe defaults, updating examples/evals when behavior changes, and avoiding unrelated generated/plugin infrastructure.

`CONTRIBUTING.md` accepts fixes, references/adapters, verified examples, and proposed skills; permits typo-only PRs directly; asks for an issue before new skills or behavior changes; provides exact setup/validation commands; and requires behavioral evidence and third-party provenance.

`SECURITY.md` supports the latest `main`, sends ordinary bugs to Issues, and directs command-injection, path-traversal, secret-handling, or destructive-behavior reports to GitHub's **Security → Report a vulnerability** flow without asking reporters to disclose exploit details publicly.

- [ ] **Step 3: Add focused issue forms and pull-request checklist**

The bug form collects skill, environment, repository shape, invocation, expected/actual behavior, logs with secrets removed, and a safety-impact checkbox. The proposal form collects problem, trigger language, expected outputs, side effects, portability, and evidence. The pull-request template asks for problem, change, validation, behavior evidence, docs/evals, and provenance.

- [ ] **Step 4: Run package and existing tests**

```bash
python -m unittest discover -s tests -v
```

Expected: all tests pass, with only platform-specific filename tests skipped on Windows.

- [ ] **Step 5: Commit the public project surface**

```bash
git add README.md AGENTS.md CONTRIBUTING.md SECURITY.md .github tests/test_skill_package.py
git commit -m "docs: prepare agent skills repository for public use"
```

### Task 4: Add reproducible development dependencies and CI

**Files:**
- Create: `requirements-dev.txt`
- Create: `.github/workflows/validate.yml`

- [ ] **Step 1: Pin the linter used locally and in CI**

Create `requirements-dev.txt` with the current verified PyPI releases:

```text
PyYAML==6.0.3
ruff==0.16.3
```

- [ ] **Step 2: Create the least-privilege validation workflow**

Trigger on pushes to `main` and pull requests. Set `permissions: contents: read`. Pin `actions/checkout` to `de0fac2e4500dabe0009e67214ff5f5447ce83dd` (`v6.0.2`) and `actions/setup-python` to `a309ff8b426b58ec0e2a45f0f869d46889d02405` (`v6.2.0`). Matrix `ubuntu-latest` and `windows-latest` against Python `3.10` and `3.14`. Install `requirements-dev.txt`, then run:

```text
python -m unittest discover -s tests -v
python -m ruff check .
python -m compileall -q skills tests
python skills/architecture-hygiene-audit/scripts/validate_ledger.py --inventory examples/architecture-hygiene-audit/inventory.json --ledger examples/architecture-hygiene-audit/ledger.json
```

- [ ] **Step 3: Run the complete local validation contract**

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python -m ruff check .
python -m compileall -q skills tests
python skills/architecture-hygiene-audit/scripts/validate_ledger.py --inventory examples/architecture-hygiene-audit/inventory.json --ledger examples/architecture-hygiene-audit/ledger.json
python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/architecture-hygiene-audit
```

Expected: zero failures, zero lint violations, `Ledger valid: 2/2 paths reconciled.`, and `Skill is valid!`.

- [ ] **Step 4: Commit CI**

```bash
git add requirements-dev.txt .github/workflows/validate.yml README.md
git commit -m "ci: validate public skill package"
```

### Task 5: Review, publish, and verify the public repository

**Files:**
- Review: all changed files

- [ ] **Step 1: Inspect the exact publication diff**

```bash
git diff --check origin/main...HEAD
git diff --stat origin/main...HEAD
git status --short
```

Expected: no whitespace errors; only intentional repository-publication files; no secrets or local paths in public guidance.

- [ ] **Step 2: Push the validated commits**

```bash
git push -u origin HEAD:main
```

Expected: the remote `main` ref advances to local `HEAD`.

- [ ] **Step 3: Set public discovery and security settings**

```bash
gh repo edit philipgierszal/agent-skills --visibility public --accept-visibility-change-consequences --description "Evidence-first Agent Skills for repository architecture, dead-code, and code-hygiene audits."
gh repo edit philipgierszal/agent-skills --add-topic agent-skills --add-topic codex --add-topic code-quality --add-topic software-architecture --add-topic dead-code --add-topic static-analysis
gh api --method PUT repos/philipgierszal/agent-skills/private-vulnerability-reporting
```

Expected: each command exits zero. Do not create a tag or release in this task.

- [ ] **Step 4: Verify the public state independently**

```bash
gh repo view philipgierszal/agent-skills --json url,visibility,description,repositoryTopics,defaultBranchRef
git ls-remote origin refs/heads/main
git rev-parse HEAD
git status --short --branch
```

Expected: visibility `PUBLIC`; URL `https://github.com/philipgierszal/agent-skills`; description and six topics match; remote `main` SHA equals local `HEAD`; working tree is clean.

- [ ] **Step 5: Verify unauthenticated discovery and installation metadata**

Open the public URL without relying on a private session and verify that README content and the validation workflow are readable. Run the public catalog preview:

```bash
npx skills@latest add philipgierszal/agent-skills --list
```

Expected: `architecture-hygiene-audit` is listed without repository authentication.
