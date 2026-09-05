# Curated upstream skills

A personal selection of other authors' work. These are **references**, not extra skills installed by this repository. Start small and add a specialist when its task recurs.

The [machine-readable catalog](../catalog.json) pins every source to a full Git revision and records a body hash, review level, rationale, and caveat. A matching body does not prove identical helpers, successful installation, or end-to-end behavior.

## Start here

| Need | Preferred starting point |
| --- | --- |
| Understand an unfamiliar repository | `acquire-codebase-knowledge` |
| Design module boundaries | `codebase-design` |
| Clarify domain vocabulary | `domain-modeling` |
| Diagnose a hard defect | `diagnosing-bugs` |
| Test-first implementation when requested | `tdd` |
| Answer a technical question with sources | `research` |
| Test a design assumption cheaply | `prototype` |
| Write maintainable agent instructions | `writing-for-agents` |

These are preferences, not certification. This review did not run every workflow against a real project. See the [audit and limitations](skill-audit.md).

## Reading the selection

- **starter:** focused choices for recurring engineering work.
- **specialist:** useful for a matching domain or explicit task.
- **choose-one:** overlapping process frameworks; select one owner for a phase.
- **review-first:** known defect, incomplete integration, in-progress package, or unreviewed upstream differences.

Avoid standalone Superpowers copies alongside its plugin in the same client. Matt Pocock's engineering skills and Superpowers overlap in planning, debugging, testing, review and implementation; loading both complete workflows can add contradictory checkpoints.

## Pinned references

### mattpocock/skills

| Skill | Selection | Reason / caveat |
| --- | --- | --- |
| [ask-matt](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/ask-matt/SKILL.md) | specialist | Author-specific engineering coach/router requiring companion skills; optional, not a general task bootstrap. |
| [code-review](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/code-review/SKILL.md) | review-first | The reviewed diff command compares commits and omits staged/unstaged changes. Restrict to committed changes until repaired and regression-tested. |
| [codebase-design](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/codebase-design/SKILL.md) | starter | Focused guidance for codebase design. Verify required project conventions and tools for the matching task. |
| [diagnosing-bugs](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/diagnosing-bugs/SKILL.md) | starter | Focused guidance for diagnosing bugs. Verify required project conventions and tools for the matching task. |
| [domain-modeling](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/domain-modeling/SKILL.md) | starter | Focused guidance for domain modeling. Verify required project conventions and tools for the matching task. |
| [grill-with-docs](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/grill-with-docs/SKILL.md) | specialist | Interactive document refinement; use when that questioning workflow is wanted. |
| [implement](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/implement/SKILL.md) | specialist | Needs issue-tracker conventions and agreed scope; issue/PR writes require authorization. |
| [improve-codebase-architecture](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/improve-codebase-architecture/SKILL.md) | review-first | Its deletion-test wording is ambiguous alongside the companion design reference. Clarify the intended heuristic before proposals; tracker publication is separate. |
| [prototype](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/prototype/SKILL.md) | starter | Focused guidance for prototype. Verify required project conventions and tools for the matching task. |
| [research](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/research/SKILL.md) | starter | Focused guidance for research. Verify required project conventions and tools for the matching task. |
| [resolving-merge-conflicts](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/resolving-merge-conflicts/SKILL.md) | review-first | The stage-everything instruction can include unrelated work. Stage only resolved paths within the authorized change. |
| [setup-matt-pocock-skills](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/setup-matt-pocock-skills/SKILL.md) | specialist | Creates tracker/domain conventions used by other engineering skills. Configure only when adopting that workflow. |
| [tdd](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/tdd/SKILL.md) | starter | Focused guidance for tdd. Verify required project conventions and tools for the matching task. |
| [to-spec](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/to-spec/SKILL.md) | specialist | Focused guidance for to spec. Verify required project conventions and tools for the matching task. |
| [to-tickets](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/to-tickets/SKILL.md) | specialist | Focused guidance for to tickets. Verify required project conventions and tools for the matching task. |
| [triage](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/triage/SKILL.md) | specialist | Focused guidance for triage. Verify required project conventions and tools for the matching task. |
| [wayfinder](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/wayfinder/SKILL.md) | specialist | Focused guidance for wayfinder. Verify required project conventions and tools for the matching task. |
| [wizard](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/wizard/SKILL.md) | specialist | Focused guidance for wizard. Verify required project conventions and tools for the matching task. |
| [claude-handoff](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/in-progress/claude-handoff/SKILL.md) | review-first | Upstream marks this in-progress. Specialized claude handoff workflow; verify client support and avoid overlapping workflow owners. |
| [implement-spec](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/in-progress/implement-spec/SKILL.md) | review-first | Upstream marks this in-progress. Specialized implement spec workflow; verify client support and avoid overlapping workflow owners. |
| [loop-me](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/in-progress/loop-me/SKILL.md) | review-first | Upstream marks this in-progress. Specialized loop me workflow; verify client support and avoid overlapping workflow owners. |
| [retro](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/in-progress/retro/SKILL.md) | review-first | Upstream marks this in-progress. Specialized retro workflow; verify client support and avoid overlapping workflow owners. |
| [setup-ts-deep-modules](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/in-progress/setup-ts-deep-modules/SKILL.md) | review-first | Upstream marks this in-progress. Specialized setup ts deep modules workflow; verify client support and avoid overlapping workflow owners. |
| [writing-beats](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/in-progress/writing-beats/SKILL.md) | review-first | Upstream marks this in-progress. Specialized writing beats workflow; verify client support and avoid overlapping workflow owners. |
| [writing-fragments](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/in-progress/writing-fragments/SKILL.md) | review-first | Upstream marks this in-progress. Specialized writing fragments workflow; verify client support and avoid overlapping workflow owners. |
| [writing-shape](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/in-progress/writing-shape/SKILL.md) | review-first | Upstream marks this in-progress. Specialized writing shape workflow; verify client support and avoid overlapping workflow owners. |
| [git-guardrails-claude-code](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/misc/git-guardrails-claude-code/SKILL.md) | specialist | Claude Code hook configuration, not a Codex runtime safeguard. Review host-wide changes before installation. |
| [migrate-to-shoehorn](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/misc/migrate-to-shoehorn/SKILL.md) | review-first | The example installs a test-only dependency as a production dependency. Use the existing package manager and devDependency convention. |
| [scaffold-exercises](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/misc/scaffold-exercises/SKILL.md) | specialist | Focused guidance for scaffold exercises. Verify required project conventions and tools for the matching task. |
| [setup-pre-commit](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/misc/setup-pre-commit/SKILL.md) | specialist | Changes project hooks and dependencies. Follow the project local-CI policy and existing package manager. |
| [grill-me](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/productivity/grill-me/SKILL.md) | specialist | Overlapping grilling entry. Prefer one chosen questioning workflow. |
| [grilling](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/productivity/grilling/SKILL.md) | specialist | Intensive questioning for unresolved decisions, not a universal approval gate. |
| [handoff](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/productivity/handoff/SKILL.md) | specialist | Focused guidance for handoff. Verify required project conventions and tools for the matching task. |
| [teach](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/productivity/teach/SKILL.md) | specialist | Focused guidance for teach. Verify required project conventions and tools for the matching task. |
| [to-questionnaire](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/productivity/to-questionnaire/SKILL.md) | specialist | Focused guidance for to questionnaire. Verify required project conventions and tools for the matching task. |
| [wait-what](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/productivity/wait-what/SKILL.md) | specialist | Focused guidance for wait what. Verify required project conventions and tools for the matching task. |
| [writing-for-agents](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/productivity/writing-for-agents/SKILL.md) | starter | Focused guidance for writing for agents. Verify required project conventions and tools for the matching task. |

### obra/superpowers

| Skill | Selection | Reason / caveat |
| --- | --- | --- |
| [brainstorming](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/brainstorming/SKILL.md) | choose-one | Opinionated approval and companion workflow. Apply host authorization and port rules; avoid duplicate standalone and plugin installations. |
| [dispatching-parallel-agents](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/dispatching-parallel-agents/SKILL.md) | choose-one | An opinionated development-process phase. Use one framework owner, preserve host policy, and avoid overlapping global workflows. |
| [executing-plans](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/executing-plans/SKILL.md) | choose-one | An opinionated development-process phase. Use one framework owner, preserve host policy, and avoid overlapping global workflows. |
| [finishing-a-development-branch](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/finishing-a-development-branch/SKILL.md) | review-first | Directory location is not proof of worktree ownership. Cleanup must use creation provenance and preserve already-authorized user choices. |
| [receiving-code-review](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/receiving-code-review/SKILL.md) | choose-one | An opinionated development-process phase. Use one framework owner, preserve host policy, and avoid overlapping global workflows. |
| [requesting-code-review](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/requesting-code-review/SKILL.md) | choose-one | An opinionated development-process phase. Use one framework owner, preserve host policy, and avoid overlapping global workflows. |
| [subagent-driven-development](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/subagent-driven-development/SKILL.md) | choose-one | An opinionated development-process phase. Use one framework owner, preserve host policy, and avoid overlapping global workflows. |
| [systematic-debugging](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/systematic-debugging/SKILL.md) | review-first | A diagnostic example prints an environment value under a Secrets heading. Use presence-only diagnostics for secrets. |
| [test-driven-development](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/test-driven-development/SKILL.md) | review-first | Delete-code/start-over wording must not erase existing user work. Constrain fresh implementation to the authorized scope and preserve unrelated or pre-existing changes. |
| [using-git-worktrees](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/using-git-worktrees/SKILL.md) | review-first | An ignore check can pass on the unselected alternative directory. Validate the chosen path and record worktree ownership before cleanup. |
| [using-superpowers](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/using-superpowers/SKILL.md) | review-first | The standalone hierarchy wrongly places skills above system instructions. Repair precedence claims and broad bootstrap triggers before adoption. |
| [verification-before-completion](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/verification-before-completion/SKILL.md) | choose-one | An opinionated development-process phase. Use one framework owner, preserve host policy, and avoid overlapping global workflows. |
| [writing-plans](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/writing-plans/SKILL.md) | choose-one | An opinionated development-process phase. Use one framework owner, preserve host policy, and avoid overlapping global workflows. |
| [writing-skills](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/writing-skills/SKILL.md) | review-first | The 1024-character total-frontmatter claim and workflow-free description rule are stricter than the specification. Use current packaging guidance. |

### vercel-labs/agent-skills

| Skill | Selection | Reason / caveat |
| --- | --- | --- |
| [vercel-composition-patterns](https://github.com/vercel-labs/agent-skills/blob/063bee94c3f4df8453406c830b0a7df0f2860278/skills/composition-patterns/SKILL.md) | specialist | React composition reference; upstream folder and declared name differ. Confirm installer discovery before changing managed directories. |
| [vercel-react-best-practices](https://github.com/vercel-labs/agent-skills/blob/063bee94c3f4df8453406c830b0a7df0f2860278/skills/react-best-practices/SKILL.md) | specialist | React/Next.js-specific guidance; check project versions. Upstream folder and declared name differ, so confirm installer discovery. |
| [web-design-guidelines](https://github.com/vercel-labs/agent-skills/blob/063bee94c3f4df8453406c830b0a7df0f2860278/skills/web-design-guidelines/SKILL.md) | specialist | Fetches an external guideline source. Record the retrieved revision/content when reproducible reviews matter. |

### trailofbits/skills

| Skill | Selection | Reason / caveat |
| --- | --- | --- |
| [differential-review](https://github.com/trailofbits/skills/blob/d3323cefbcf645678b8dc481de204b02ad3d02dc/plugins/differential-review/skills/differential-review/SKILL.md) | review-first | The installed body differs from this revision. Re-review before upgrading; a review does not authorize remediation or publication. |
| [property-based-testing](https://github.com/trailofbits/skills/blob/d3323cefbcf645678b8dc481de204b02ad3d02dc/plugins/property-based-testing/skills/property-based-testing/SKILL.md) | specialist | Specialist testing techniques; choose generators and invariants for the target language rather than adding a framework automatically. |
| [spec-to-code-compliance](https://github.com/trailofbits/skills/blob/d3323cefbcf645678b8dc481de204b02ad3d02dc/plugins/spec-to-code-compliance/skills/spec-to-code-compliance/SKILL.md) | review-first | The installed skill depends on an absent plugin workflow and checker agent. Install the complete compatible plugin or adapt and test the workflow. |
| [supply-chain-risk-auditor](https://github.com/trailofbits/skills/blob/d3323cefbcf645678b8dc481de204b02ad3d02dc/plugins/supply-chain-risk-auditor/skills/supply-chain-risk-auditor/SKILL.md) | review-first | Windows offline tests expose os.getuid() failures. Current advisory checks also need network evidence; resolve platform compatibility first. |
| [variant-analysis](https://github.com/trailofbits/skills/blob/d3323cefbcf645678b8dc481de204b02ad3d02dc/plugins/variant-analysis/skills/variant-analysis/SKILL.md) | specialist | Useful after a known bug, with direct-step fallback. The optional parallel workflow requires the full compatible plugin; missing companion skills must not block a narrow manual hunt. |

### anthropics/skills

| Skill | Selection | Reason / caveat |
| --- | --- | --- |
| [frontend-design](https://github.com/anthropics/skills/blob/41bbe19d1a1a7eaab5e7bb9050a417e5c6cffc8f/skills/frontend-design/SKILL.md) | review-first | The installed body differs from this upstream revision. Review the reference independently; respect the actual brand brief and browser QA requirements. |

### github/awesome-copilot

| Skill | Selection | Reason / caveat |
| --- | --- | --- |
| [acquire-codebase-knowledge](https://github.com/github/awesome-copilot/blob/7b1ebe6333397841ca918dec904d24d4695fe953/skills/acquire-codebase-knowledge/SKILL.md) | starter | Useful onboarding inventory. Treat dependency classification and code churn as evidence to investigate, not proof of production reachability or fragility. |
| [agentic-eval](https://github.com/github/awesome-copilot/blob/7b1ebe6333397841ca918dec904d24d4695fe953/skills/agentic-eval/SKILL.md) | review-first | Conceptual examples include undefined helpers; they are not runnable evaluation programs. Adapt to the host evaluation framework and bound iteration/cost. |
| [github-actions-efficiency](https://github.com/github/awesome-copilot/blob/7b1ebe6333397841ca918dec904d24d4695fe953/skills/github-actions-efficiency/SKILL.md) | review-first | Contains live workflow pushes and run monitoring. Use only source inspection where host policy prohibits GitHub Actions. |

### OKHP3/mermaid-diagram-bpmn

| Skill | Selection | Reason / caveat |
| --- | --- | --- |
| [okhp3-as-is-process-capture](https://github.com/OKHP3/mermaid-diagram-bpmn/blob/f8200e8d685fda7c86e492082076a1526713af1e/skills/okhp3-as-is-process-capture/SKILL.md) | specialist | A distinct process-documentation stage requiring its upstream artifacts. Verify the relevant validators and rendering for the chosen workflow. |
| [okhp3-decision-model-authoring](https://github.com/OKHP3/mermaid-diagram-bpmn/blob/f8200e8d685fda7c86e492082076a1526713af1e/skills/okhp3-decision-model-authoring/SKILL.md) | review-first | The example declares Unique but overlapping amount/role rules can match simultaneously. Test overlap rejection before relying on it. |
| [okhp3-elicitation-interviews](https://github.com/OKHP3/mermaid-diagram-bpmn/blob/f8200e8d685fda7c86e492082076a1526713af1e/skills/okhp3-elicitation-interviews/SKILL.md) | specialist | A distinct process-documentation stage requiring its upstream artifacts. Verify the relevant validators and rendering for the chosen workflow. |
| [okhp3-future-state-change-strategy](https://github.com/OKHP3/mermaid-diagram-bpmn/blob/f8200e8d685fda7c86e492082076a1526713af1e/skills/okhp3-future-state-change-strategy/SKILL.md) | specialist | A distinct process-documentation stage requiring its upstream artifacts. Verify the relevant validators and rendering for the chosen workflow. |
| [okhp3-process-gap-exception-analysis](https://github.com/OKHP3/mermaid-diagram-bpmn/blob/f8200e8d685fda7c86e492082076a1526713af1e/skills/okhp3-process-gap-exception-analysis/SKILL.md) | specialist | A distinct process-documentation stage requiring its upstream artifacts. Verify the relevant validators and rendering for the chosen workflow. |
| [okhp3-process-intake-and-scope](https://github.com/OKHP3/mermaid-diagram-bpmn/blob/f8200e8d685fda7c86e492082076a1526713af1e/skills/okhp3-process-intake-and-scope/SKILL.md) | specialist | A distinct process-documentation stage requiring its upstream artifacts. Verify the relevant validators and rendering for the chosen workflow. |
| [okhp3-process-measures-controls](https://github.com/OKHP3/mermaid-diagram-bpmn/blob/f8200e8d685fda7c86e492082076a1526713af1e/skills/okhp3-process-measures-controls/SKILL.md) | specialist | A distinct process-documentation stage requiring its upstream artifacts. Verify the relevant validators and rendering for the chosen workflow. |
| [okhp3-process-narrative-authoring](https://github.com/OKHP3/mermaid-diagram-bpmn/blob/f8200e8d685fda7c86e492082076a1526713af1e/skills/okhp3-process-narrative-authoring/SKILL.md) | specialist | A distinct process-documentation stage requiring its upstream artifacts. Verify the relevant validators and rendering for the chosen workflow. |
| [okhp3-process-validation-scoring](https://github.com/OKHP3/mermaid-diagram-bpmn/blob/f8200e8d685fda7c86e492082076a1526713af1e/skills/okhp3-process-validation-scoring/SKILL.md) | review-first | A summary score or regex check does not prove the underlying artifact validators ran. Integration coverage needs verification. |
| [okhp3-publication-handoff-packaging](https://github.com/OKHP3/mermaid-diagram-bpmn/blob/f8200e8d685fda7c86e492082076a1526713af1e/skills/okhp3-publication-handoff-packaging/SKILL.md) | review-first | The release-gate wording omits pending approvals although handoff requires all approvals. Pending required approvals must block release; validate that gate explicitly. |
| [okhp3-raci-governance-matrix](https://github.com/OKHP3/mermaid-diagram-bpmn/blob/f8200e8d685fda7c86e492082076a1526713af1e/skills/okhp3-raci-governance-matrix/SKILL.md) | review-first | The example omits Accountable assignments in two rows despite its exactly-one-A rule. Validate generated matrices. |
| [okhp3-sipoc-generation](https://github.com/OKHP3/mermaid-diagram-bpmn/blob/f8200e8d685fda7c86e492082076a1526713af1e/skills/okhp3-sipoc-generation/SKILL.md) | specialist | A distinct process-documentation stage requiring its upstream artifacts. Verify the relevant validators and rendering for the chosen workflow. |
| [okhp3-sop-work-instructions](https://github.com/OKHP3/mermaid-diagram-bpmn/blob/f8200e8d685fda7c86e492082076a1526713af1e/skills/okhp3-sop-work-instructions/SKILL.md) | specialist | A distinct process-documentation stage requiring its upstream artifacts. Verify the relevant validators and rendering for the chosen workflow. |
| [okhp3-stakeholder-and-role-mapping](https://github.com/OKHP3/mermaid-diagram-bpmn/blob/f8200e8d685fda7c86e492082076a1526713af1e/skills/okhp3-stakeholder-and-role-mapping/SKILL.md) | specialist | A distinct process-documentation stage requiring its upstream artifacts. Verify the relevant validators and rendering for the chosen workflow. |
| [okhp3-visual-process-modeling](https://github.com/OKHP3/mermaid-diagram-bpmn/blob/f8200e8d685fda7c86e492082076a1526713af1e/skills/okhp3-visual-process-modeling/SKILL.md) | review-first | The installed body differs from this revision. Rendering and syntax checks need the compatible BPMN/Mermaid toolchain. |

## Ownership and licenses

Linked material remains with its authors. This repository's MIT license does not relicense upstream content. `license_note` records the observed declaration or repository metadata; unresolved declarations remain `not established`. Read the pinned package license before copying or redistributing it.

App-bundled skills such as Figma, documents, spreadsheets and Sites belong to their supported plugins. Private workstation procedures are outside this public selection.

See [maintaining the collection](maintaining-the-collection.md) for adding references, avoiding duplicates, and developing original skills.
