# Skill collection audit — 2026-09-05

The collection contains useful specialist knowledge, repeated installations, incompatible client assumptions, and several reproducible defects. **It is not accurate to say that every installed skill works.** This audit supports a smaller curated selection and identifies the remaining repair and integration gates.

## Scope and method

The closing inventory contains **281 physical skill instances, 140 declared names, and 154 distinct normalized instruction bodies** across personal Codex, shared agent, Claude and plugin-cache roots. The initial snapshot had 280 instances; a new `variant-analysis` skill appeared and the computer-use plugin version changed during inspection. The computer-use instruction body was unchanged. Counts include cached/explicit-only packages, not just the current automatic discovery list.

| Root category | Instances |
| --- | ---: |
| Personal Codex, including system skills | 91 |
| Shared agent skills | 37 |
| Claude, including workstation-only skills | 94 |
| Plugin caches, including non-active packages | 59 |

The review read unique instruction bodies, inspected relevant supporting files and available tool contracts, checked frontmatter, compared normalized hashes, reviewed file-reference candidates, parsed bundled Python files, and ran selected safe offline helper checks. Private paths and full workstation reports remain outside this public repository.

The catalog links 78 upstream entries from seven repositories. Source retrieval verified their pinned paths and normalized body hashes. Most matched a reviewed installed body; the manifest explicitly labels the three differing upstream bodies as reference-only. Matching a `SKILL.md` is not a complete-package provenance claim.

## Why skills appear doubled

| Pattern | Evidence | Disposition |
| --- | --- | --- |
| Shared agent + personal Codex copies | 36 common packages have equal contents after normalizing CRLF/LF. Raw bytes differ because of line endings. | Choose one discovery owner for this client after recording installer ownership and a recovery copy. |
| Standalone Superpowers + plugin | All 14 names occur in both forms; the plugin and standalone bodies differ. | Choose a maintained distribution and preserve deliberate adaptations before removing anything. |
| Claude + Codex copies | Separate client installations repeat many names. | They may be intentional; a cross-client repeat is not automatically redundant. |
| Short aliases and interactive commands | `grill-me`, `grill-with-docs`, `handoff`, and writing helpers have distinct routing or interaction purposes. | Keep only useful commands, preserving explicit-only invocation policy. |
| Plugin cache material | Templates, older browser support and runtime/internal skills exist outside the active catalog. | Cache presence does not prove activation. Let the plugin manager own those files. |

No installed skill was deleted, renamed, disabled, or patched during this audit. Removing duplicates is a separate environment mutation; it is not needed to publish a link-only selection.

## Confirmed failures and important repairs

| Skill / group | Finding | Evidence level / next gate |
| --- | --- | --- |
| `code-review` | The documented three-dot diff against `HEAD` sees committed differences, while the advertised WIP use includes uncommitted changes. | Temporary Git fixture reproduced an empty documented diff alongside a modified tracked file and an untracked file. Add explicit committed/staged/unstaged/untracked scope handling. |
| `supply-chain-risk-auditor` | Windows execution reaches `os.getuid()`, which is unavailable on Windows. | Selected offline suite: 75 passed, 17 failed, 1 deliberately deselected because it binds a port. Repair platform handling and repeat the suite; no current advisory safety claim follows from offline tests. |
| `okhp3-decision-model-authoring` | The Unique example has overlapping conditions; the validator also accepts a deliberately overlapping Unique table. | A two-rule fixture with opposite outputs and a shared matching input returned `valid: true`. Structural validation does not establish hit-policy semantics. |
| `okhp3-raci-governance-matrix` | Two example activity rows omit an Accountable role despite the exactly-one-A rule. | Source contradiction; validate examples and generated matrices against the same invariant. |
| `okhp3-process-validation-scoring` | The orchestrator contains simplified checks and trusts a stored score instead of establishing the full validation it describes. | Source inspection; add direct-validator parity and forged-score regression cases. |
| `okhp3-publication-handoff-packaging` | The release gate names rejected approvals but omits pending required approvals, while handoff requires all approvals collected. | Source ambiguity; pending required approvals must block release and need a regression case. |
| `spec-to-code-compliance` | The installed instruction package requires a named plugin workflow and checker absent from the installed unit and callable tool set. | Blocked as that installed unit; reference material can still be useful. Verify the complete compatible plugin separately. |
| `systematic-debugging` | An example prints a raw environment value while checking secrets. | Source inspection; use presence-only output and redaction for secret-bearing values. |
| `using-superpowers` | The standalone hierarchy says skills can override system instructions; broad bootstrap triggers also over-select it. | Instruction conflict. Actual host instruction precedence always governs. |
| `test-driven-development` | Delete-code/start-over wording can reach existing user work if applied indiscriminately. | Source review; constrain fresh implementation to authorized scope and preserve pre-existing changes. |
| `using-git-worktrees` | An ignore check can pass because an unselected alternative directory is ignored. | Source inspection; verify the actual selected worktree path and track ownership before cleanup. |
| `resolving-merge-conflicts` | “Stage everything” can include unrelated changes. | Source inspection; stage the resolved paths within the authorized change. |
| `agentic-eval` | Examples call undefined helpers and present illustrative prompt loops as code patterns. | Conceptual reference, not a runnable evaluator. Supply real programs, metrics, bounded execution and held-out cases. |
| `writing-skills` | The total-frontmatter limit is misstated, and an uppercase example conflicts with portable naming. | Check the current specification rather than adopting a local style rule as a format requirement. |

The linked [curated selection](curated-skills.md) records per-entry caveats and flags unresolved packages `review-first`. It is not a recommendation to execute every linked workflow.

## Client and policy conflicts

- **Document rendering:** the app document skill prescribes a LibreOffice workflow while the reviewed Windows environment requires Microsoft Word. That rendering path cannot be used unchanged under the local policy.
- **Sites:** workflow restrictions on QA and port inspection conflict with that environment's mandatory browser QA and port registry. Resolve the host-policy conflict before running the workflow.
- **Figma Slides:** a helper recommends `closePlugin` while the foundation skill prohibits it. Use the foundation tool lifecycle contract and validate slide output through the supported tools.
- **Plugin management:** prescribed discovery tool names are absent from the exposed tool set. Other management tools are available; use only their actual schemas and authorization boundaries.
- **CI workflows:** `github-actions-efficiency` and some generic setup examples assume GitHub Actions. A local-CI-only workstation must not execute those remote workflow instructions.
- **Client vocabulary:** `Task`, `Skill`, `TodoWrite`, `WebFetch`, shell dialects, hooks and slash commands are not universally interchangeable APIs. A working adapter must use the tools the actual client exposes.

Figma, Sites, notebook/runtime and live Excel tools were found among deferred tools; absence from the initial short tool list was not treated as proof that these integrations are unavailable. No live plugin writes were performed merely to test connectivity.

## Packaging checks

All inventoried entrypoints had parseable YAML and nonempty descriptions within the portable description limit. All **101 inventoried Python file instances** passed syntax parsing. This does not execute imports, validate examples inside Markdown, or prove behavior.

The Vercel React/composition directory names differ from their declared names. Bundled presentation/spreadsheet skills use display-style names that do not satisfy strict lowercase portable naming. These are portability findings, not evidence that the app loader rejected them. Candidate missing Markdown targets in the skill-creator, setup and wayfinder examples were example/output placeholders, not confirmed missing runtime assets.

The [Agent Skills specification](https://agentskills.io/specification) defines name, description and optional compatibility fields. Client validators can be stricter or lag the specification; do not remove supported invocation metadata just to satisfy a generic checker. The [official skill-building guidance](https://developers.openai.com/codex/skills/) is an additional client reference.

## Verification results and limits

| Check | Observed result | What it does not prove |
| --- | --- | --- |
| OKHP3 offline suites | 196 tests passed across 15 packages | Domain semantics, real stakeholder quality, all cross-package integration or rendering |
| BPMN generator bounded subset | 12 tests passed across 4 inspected offline suites | Full pipeline, HTTP server, rendering or complete suite acceptance |
| Agent-team package validator | Passed: 14 files, 5 directories | Agent behavior or live coordination quality |
| Architecture/security helper smoke checks | Expected valid/invalid fixtures accepted or rejected | Full edge-case correctness or a target security audit |
| Supply-chain selected offline suite | 75 passed, 17 Windows failures, 1 port-binding test deselected | Current advisory coverage or successful Windows execution |
| Python syntax | 101 file instances parsed | Imports, dependencies, live tool behavior or prompt examples |
| Repository local unit contract | 37 tests run: 35 passed, 2 expected Windows filename skips | Third-party package runtime acceptance |
| Repository lint and byte compilation | Passed | Behavioral quality |
| Repository example validator | `Ledger valid: 2/2 paths reconciled.` | Unrelated installed skills |
| Pin/path retrieval | 78 catalog references fetched successfully at recorded revisions | A supported installer or exact helper-file match |

Browser/app output, Word rendering, Figma operations, live spreadsheets, email/marketing, private databases, device tests, paid model evaluations and production access were not performed. Those require appropriate fixtures, tools and authorization for the actual task. Their status is **not end-to-end verified**, not passed.

LikeC4's pinned executable was not found on PATH, and its download-enabled entrypoints were not run. Full BPMN tests include port-binding and package-writing cases outside the read-only preflight; only the explicitly recorded offline subset ran.

## Recommended direction

Keep the small starter set, add specialists by task, and choose one process framework per phase. Preserve local private procedures separately. For original public skills, extract a portable capability from repeated work, retain provenance for adaptations, and add failing examples before claiming a repair.

The next improvement is reliable selection and evidence, not installing another large overlapping bundle. Follow the [maintenance guide](maintaining-the-collection.md) to grow the collection without accumulating untracked copies.
