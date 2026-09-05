# Research: a simple development lifecycle built from skills

Researched 2026-09-05 using primary documentation and source. This is a design recommendation, not a benchmark or an implemented framework. The [proposal](../development-workflow.md) defines the handoffs; the [example](../examples/development-workflow.md) demonstrates them.

## Answer and selection

Skills can guide the whole lifecycle: discovering needs, writing stories, recording architectural decisions, specifying behavior, implementing it, and reviewing behavior, security and authorization. A collection of skill names alone does not connect these stages. The missing layer is a small shared artifact contract with evidence-based completion gates.

Recommend one router and five working skills: requirements, specification, implementation, review, and security. Keep stories inside requirements, ADRs inside specification, and task planning inside implementation. Security participates during design and implementation review. Start with one change record and split it only when useful.

This is a synthesis of the sources below, not a framework they jointly prescribe. The current repository contains upstream references in `catalog.json` and an original installable `architecture-hygiene-audit` skill. Proposed delivery packages are documentation only. The [audit](../skill-audit.md) records why existing references cannot yet be treated as a verified workflow.

## Framework comparison

The comparison describes pinned default-branch source. Release labels are those reported by the owning repositories on the research date; they are not assertions that a release contains all inspected main-branch changes.

| Source snapshot | Useful contribution | Adopt / leave out of the first version |
| --- | --- | --- |
| [GitHub Spec Kit, 4a7341a](https://github.com/github/spec-kit/tree/4a7341a93d944d6efe153b71da4a1adb9c2b578c), release [v1.0.4](https://github.com/github/spec-kit/releases/tag/v1.0.4) | Explicit spec, plan and task artifacts; acceptance scenarios and cross-artifact consistency checks | Adopt criterion IDs and coverage checks. Leave out the full CLI/extension harness unless multiple tool integrations justify it. |
| [Fission-AI OpenSpec, e062b95](https://github.com/Fission-AI/OpenSpec/tree/e062b9572be933564ba3899d059377dfa1393e32), release [v1.12.0](https://github.com/Fission-AI/OpenSpec/releases/tag/v1.12.0) | Changes expressed as deltas to existing behavior; durable capability specifications | Adopt focused change records and reconciliation after implementation. Leave out cross-repository stores and custom schema infrastructure initially. |
| [BMAD Method, 05bfbd4](https://github.com/bmad-code-org/BMAD-METHOD/tree/05bfbd46d00766ec88eb9b42e76be2c575d64d7b), release [v6.12.0](https://github.com/bmad-code-org/BMAD-METHOD/releases/tag/v6.12.0) | Flexible planning paths and configurable review lenses | Adopt proportional planning and evidence-based finding triage. Do not make its broader tooling or multiple reviewers mandatory for each small change. |
| [Superpowers, b36e082](https://github.com/obra/superpowers/tree/b36e0829c6d0140e93cfef2ca599b1b07d4a7797), release [v6.3.0](https://github.com/obra/superpowers/releases/tag/v6.3.0) | Implementation discipline, scoped review and fresh verification evidence | Adopt precise review inputs and honest completion claims. Avoid a second competing workflow controller and overlapping installations. |
| [Matt Pocock skills, 3cca18b](https://github.com/mattpocock/skills/tree/3cca18b368ae95cdbdebbff572ccafa662551015), release [v1.2.3](https://github.com/mattpocock/skills/releases/tag/v1.2.3) | Small composable skills, domain language, specifications and vertical slices | Adopt the packaging approach and selective ADRs. Avoid exhaustive paperwork or automatic tracker publication. |

Important qualifications from the inspected source:

- Spec Kit's [spec template](https://github.com/github/spec-kit/blob/4a7341a93d944d6efe153b71da4a1adb9c2b578c/templates/spec-template.md) provides useful acceptance structure. Its [analysis command](https://github.com/github/spec-kit/blob/4a7341a93d944d6efe153b71da4a1adb9c2b578c/templates/commands/analyze.md) is described as read-only, but configured hooks can execute commands. A personal review contract must define its actual permitted effects.
- OpenSpec's [existing-project guide](https://github.com/Fission-AI/OpenSpec/blob/e062b9572be933564ba3899d059377dfa1393e32/docs/existing-projects.md) avoids documenting the whole system upfront. Its [review guide](https://github.com/Fission-AI/OpenSpec/blob/e062b9572be933564ba3899d059377dfa1393e32/docs/reviewing-changes.md) does not make verification a mechanical prerequisite for archiving. Archival and apparent test coverage are not executed-test evidence.
- BMAD's inspected main [planning guidance](https://github.com/bmad-code-org/BMAD-METHOD/blob/05bfbd46d00766ec88eb9b42e76be2c575d64d7b/docs/plan/choose-a-planning-path.md) is more flexible than older descriptions of mandatory phases. Its [review workflow](https://github.com/bmad-code-org/BMAD-METHOD/blob/05bfbd46d00766ec88eb9b42e76be2c575d64d7b/docs/build/review-a-change.md) offers useful lenses; a security-review extension does not establish complete RBAC assurance.
- Superpowers' [verification skill](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/verification-before-completion/SKILL.md) supports claims tied to actual checks. Passing tests still needs reconciliation with requirements.
- Matt's [spec skill](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/to-spec/SKILL.md) and [ticket skill](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/to-tickets/SKILL.md) connect intent to slices. External publication behavior needs the host's authorization rules. The [README](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/README.md) warns that installing both distribution methods duplicates skills.

## Requirements, stories and decisions

| Primary source | Pattern evaluated and selected |
| --- | --- |
| [GOV.UK: learning user needs](https://www.gov.uk/service-manual/user-research/start-by-learning-user-needs) | Separate observed needs from proposed solutions; retain evidence and assumptions. |
| [Bill Wake: INVEST](https://xp123.com/invest-in-good-stories-and-smart-tasks/) | Keep stories valuable, small and testable; distinguish user outcomes from implementation tasks. |
| [Cucumber: Example Mapping](https://cucumber.io/blog/bdd/example-mapping-introduction/) | Discover business rules, examples and unresolved questions before writing implementation details. |
| [Gherkin reference](https://cucumber.io/docs/gherkin/reference/) | Use executable scenario syntax when it fits the project; do not require it for every acceptance criterion. |
| [Michael Nygard: ADRs](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) and [MADR](https://adr.github.io/madr/) | Record significant context, alternatives, decision and consequences; preserve superseded decisions. Avoid an ADR for routine edits. |
| [Shape Up: pitches](https://basecamp.com/shapeup/1.5-chapter-06) | Make the problem, boundaries and major risks explicit. Borrow these fields without importing an entire delivery cadence. |

The resulting artifact is a change specification, not duplicated PRD, story, design and ticket descriptions. Stable IDs connect needs, criteria, tasks and observed results. Unknown business policy blocks dependent implementation; it does not prevent unrelated authorized work.

## Security and authorization sources

Security must influence requirements and design as well as review. Use a bounded threat model and selected verifiable controls; do not label a clean scanner or completed checklist a security certification.

| Primary source and status at research date | Application to the proposal |
| --- | --- |
| [NIST SSDF 1.1, SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final), final February 2022 | Integrate secure practices throughout development. [SSDF 1.2](https://csrc.nist.gov/projects/ssdf/publications) is a draft, not the final baseline. |
| [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/), stable 5.0.0, May 2025 | Select applicable requirements and preserve their version and identifiers beside verification evidence. |
| [OWASP WSTG 4.2](https://wstg.owasp.org/v4.2/), stable; 4.3 unreleased on the [project page](https://owasp.org/www-project-web-security-testing-guide/) | Choose testing techniques for the actual changed surface; do not imply the entire standard was assessed. |
| [Threat Modeling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html) | Identify assets, trust boundaries, abuse cases and controls early. |
| [Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) | Define permissions beyond roles, enforce server-side checks and default deny. No external policy service is required by this proposal. |
| OWASP API Security 2023: [objects](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/), [properties](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/), [functions](https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization/) | Review each boundary independently, including tenant, ownership, fields, administration and alternate entry points. |
| [Authorization Testing Automation](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Testing_Automation_Cheat_Sheet.html) | Maintain allow/deny matrices and independently reasoned expected cases; verify denial has no prohibited side effects. |
| [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | Include applicable accessibility requirements and human evaluation for UI changes. |

Other review lenses follow the affected behavior: concurrency and invariants for writes, migration/recovery for persistent changes, compatibility for interfaces, measured performance for workload changes, and operational failure/retry behavior for jobs and integrations. The proposal names evidence for each instead of requiring every specialist skill every time.

## Alternatives and validation boundary

1. **Preferred: a thin owned workflow with attributed upstream references.** Best matches the requested simple personal collection. It requires maintaining and evaluating the handoff contract; fewer packages alone do not prove better results.
2. **Adopt OpenSpec or Spec Kit as the artifact framework.** Appropriate if standardized tooling and generated integrations become more valuable than minimal setup. Choose one, then add explicit authorization review and executed verification evidence.
3. **Adopt the broader BMAD workflow.** Appropriate if its planning and review tooling address demonstrated coordination needs. Its current flexibility should be assessed directly rather than rejected based on older tutorials.

Before writing or promoting executable skills, pilot a small bug, an ordinary feature and an authorization-sensitive change. Evaluate missed requirements, useful findings, false completion claims, interruptions and artifact maintenance. Include skipped required tests, stale evidence and uncommitted-only defects. No installations, comparative runtime experiments or application security tests were performed for this research.
