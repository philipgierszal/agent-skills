# Research: public Agent Skills repository structure

Date: 2026-08-26

## Executive recommendation

Publish this project as an independent, standards-first repository with a deliberately small public surface:

1. keep installable skills under `skills/<skill-name>/`;
2. make the root README a fast path from problem to install to first successful invocation;
3. add lightweight community files and CI validation before inviting contributions;
4. retain tests, behavioral eval records, examples, and research outside the installable skill payload; and
5. use repository-wide semantic tags and a changelog only when there is a meaningful release, without introducing Node/package/plugin machinery solely to create a version number.

This takes the most reusable parts of both reference repositories without cloning their scale. Superpowers uses a flat `skills/<name>/` catalog backed by `docs/`, `scripts/`, `tests/`, community files, release notes, and many harness-specific plugin directories ([Superpowers root](https://github.com/obra/superpowers), [Superpowers skills tree](https://github.com/obra/superpowers/tree/main/skills)). Matt Pocock's repository uses categorized skill buckets (`engineering`, `productivity`, `in-progress`, and `deprecated`), matching documentation, a Claude plugin manifest, Changesets, a changelog, and an automated release workflow ([Matt Pocock skills root](https://github.com/mattpocock/skills), [skills tree](https://github.com/mattpocock/skills/tree/main/skills), [release workflow](https://github.com/mattpocock/skills/blob/main/.github/workflows/release.yml)). Those structures solve real problems at their current size; a one-to-several-skill repository should not inherit all of them pre-emptively.

Do **not** fork either upstream repository for this purpose. The intended product, ownership, release history, and scope are independent. Reference their public patterns and credit inspiration where useful, but keep the repository's Git history and issue tracker about this collection.

## What the primary sources establish

### The portable unit is a self-contained skill directory

The Agent Skills specification defines the minimum unit as a directory containing `SKILL.md`; `scripts/`, `references/`, and `assets/` are optional. It requires `name` and `description`, constrains skill names, allows short `license`, `compatibility`, and string-valued `metadata` fields, and recommends progressive disclosure with `SKILL.md` under 500 lines and only shallow file references ([Agent Skills specification](https://agentskills.io/specification)).

OpenAI adds an optional `agents/openai.yaml` for UI metadata, invocation policy, and tool dependencies. It advises front-loading trigger terms in the description, keeping each skill focused, preferring instructions over scripts unless deterministic behavior is needed, and testing trigger prompts ([OpenAI skill guidance](https://learn.chatgpt.com/docs/build-skills)).

The public `skills` CLI discovers flat `skills/<name>/SKILL.md` layouts and also supports up to two category levels, so beginning flat does not prevent later categorization. It accepts a GitHub `owner/repo`, can list or select individual skills, supports local sources, and distinguishes project from global installation ([skills CLI README](https://github.com/vercel-labs/skills/blob/main/README.md)).

### The two large repositories optimize for different products

Superpowers is both a skills collection and a multi-harness framework. Its root includes separate metadata or bootstrap directories for Codex, Claude, Cursor, Devin, Hermes, Kimi, OpenCode, Pi, and other clients, plus hooks, assets, scripts, tests, and release tooling ([Superpowers root](https://github.com/obra/superpowers)). Its README therefore needs per-client installation instructions, a complete workflow narrative, a catalog, philosophy, community links, contribution rules, update behavior, licensing, and telemetry disclosure ([Superpowers README](https://github.com/obra/superpowers/blob/main/README.md)).

Matt Pocock's repository emphasizes a discoverable collection of small, composable engineering practices. Its README leads with a distinct promise, explains two installation philosophies, gives the `npx skills@latest add mattpocock/skills` path, explains setup, then groups the catalog by user-invoked versus model-invoked skills ([Matt Pocock README](https://github.com/mattpocock/skills/blob/main/README.md)). Its stable, in-progress, and deprecated buckets make lifecycle state structural; in-progress skills are deliberately excluded from the plugin and top-level README until promotion ([in-progress policy](https://github.com/mattpocock/skills/blob/main/skills/in-progress/README.md)).

The lesson is not to reproduce either tree literally. Adopt the portable skill boundary, clear installation path, curated catalog, visible lifecycle, and behavior-validation culture. Omit infrastructure whose corresponding distribution channel or maintenance problem does not yet exist.

## Recommended root layout

```text
agent-skills/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── SECURITY.md
├── CHANGELOG.md                    # add with the first tagged release
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug.yml
│   │   └── skill-proposal.yml
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/
│       └── validate.yml
├── skills/
│   └── architecture-hygiene-audit/
│       ├── SKILL.md
│       ├── agents/
│       │   └── openai.yaml
│       ├── scripts/
│       ├── references/
│       └── assets/                 # only when the skill actually needs assets
├── tests/
│   └── architecture-hygiene-audit/
├── evals/
│   └── architecture-hygiene-audit/
├── examples/
│   └── architecture-hygiene-audit/ # only verified, maintained examples
└── docs/
    ├── research/
    └── decisions/                  # ADRs only for durable repository decisions
```

For the current single skill, preserving the existing root-level `tests/` files and single eval document is reasonable. Introduce per-skill subdirectories when a second skill would otherwise make ownership ambiguous. Do not create empty `assets/`, category, example, or decision directories merely to match a diagram.

### Adopt now

- `skills/<name>/SKILL.md` as the public installation boundary.
- Per-skill `scripts/` and `references/`, because they are part of the skill's runtime contract and are installed with it.
- Per-skill `agents/openai.yaml`, because the current skill already has meaningful Codex display and invocation metadata; OpenAI documents this as the optional place for those settings ([OpenAI skill guidance](https://learn.chatgpt.com/docs/build-skills)).
- Root `tests/`, `evals/`, and `docs/`, which let maintainers verify behavior without shipping development material as part of the selected skill.
- A small `.github/workflows/validate.yml` that runs structural frontmatter/link tests, unit tests, lint, compilation, and the maintained reconciliation fixture. Keep external reference validation and public installer discovery as release gates until pinned, tested CI integrations are available.
- `CONTRIBUTING.md`, `SECURITY.md`, and focused issue/PR templates before actively inviting outside contributions. GitHub surfaces `CONTRIBUTING.md` when users open issues or pull requests and on the repository's contribute page ([GitHub contribution-guideline documentation](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors)).

### Deliberately omit for now

- Harness bootstrap directories, hooks, commands, and duplicated manifests from Superpowers. Add a harness adapter only after testing and supporting that distribution channel.
- Matt's `engineering/`, `productivity/`, `in-progress/`, and `deprecated/` hierarchy while the catalog is small. A flat directory is easier to browse and is natively discovered by the installer. Add lifecycle folders only when several unreleased or retired skills would otherwise clutter the stable catalog.
- `.changeset/`, `package.json`, lockfiles, and automated version-sync scripts solely for Markdown skills. Matt's package and release workflow keep a Claude plugin, package version, changelog, and Git tags synchronized ([package metadata](https://github.com/mattpocock/skills/blob/main/package.json), [Changesets configuration](https://github.com/mattpocock/skills/blob/main/.changeset/config.json)); Superpowers synchronizes one version across numerous client manifests ([Superpowers version map](https://github.com/obra/superpowers/blob/main/.version-bump.json)). This repository does not yet have that synchronization problem.
- A repository-wide plugin manifest at first release. OpenAI says direct skill folders are best for authoring/local discovery and recommends a plugin when distributing multiple reusable skills or bundling connectors ([OpenAI skill guidance](https://learn.chatgpt.com/docs/build-skills)). Add `.codex-plugin/plugin.json` or another client manifest when there are at least two stable skills, a marketplace submission, a connector, or a tested need for managed updates.
- A setup/router skill until users truly need repository-wide configuration or catalog routing. One audit skill should install and work directly.

## README information architecture

The public README should be user-facing, not a record of internal repository decisions. GitHub describes the README as the place to tell visitors why the project is useful, what they can do with it, and how to use it, while longer material belongs elsewhere ([GitHub README guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)).

Recommended order:

1. **Name and one-sentence promise.** Say that this is a collection of evidence-first Agent Skills, then name the concrete outcome.
2. **Thirty-second install.** Put one copyable public command above background explanation.
3. **First invocation.** Give a real prompt that includes `$architecture-hygiene-audit` and a plain-language example that can trigger it implicitly.
4. **Skill catalog.** Use a compact table with skill name/link, when to use it, key output, safety/side-effect level, and status.
5. **What the current skill produces.** Show inventory/ledger reconciliation, confidence categories, and a short report excerpt or link to a maintained example.
6. **Requirements and compatibility.** State Git and Python requirements and name the clients actually tested. Avoid “works everywhere” claims merely because the format is portable.
7. **Update and uninstall.** Link to or show `npx skills update` and `npx skills remove` so installation is not a one-way door; the CLI documents both commands ([skills CLI README](https://github.com/vercel-labs/skills/blob/main/README.md)).
8. **Develop and validate.** List exact local commands and link to the contribution guide.
9. **Contributing, security, roadmap/release policy, and license.** Keep each concise and link to the owning document.

The current README should immediately remove the sentence that the repository is private and the authentication warning once visibility changes. Move the long “why this is not a Matt Pocock fork” explanation into a decision note or compress it to one attribution sentence; public users primarily need value, installability, trust, and support information.

### Installation commands to publish

Use the standard interactive command as the primary path:

```bash
npx skills@latest add philipgierszal/agent-skills --skill architecture-hygiene-audit
```

Optionally add an explicit global Codex command for readers who want the skill in every repository:

```bash
npx skills@latest add philipgierszal/agent-skills \
  --skill architecture-hygiene-audit \
  --global \
  --agent codex
```

The CLI's documented source format is `owner/repo`; `--skill` selects one skill, `--global` changes the scope, and `--agent` selects the target client ([skills CLI README](https://github.com/vercel-labs/skills/blob/main/README.md)). Also document a no-install preview/list command:

```bash
npx skills@latest add philipgierszal/agent-skills --list
```

Do not lead with manual copying into `~/.codex/skills`. Keep it as troubleshooting or contributor-local development guidance because it is client-specific and does not preserve update provenance.

## Discovery metadata

Discovery has three separate surfaces and each should be intentional:

1. **Skill discovery:** keep `name` identical to the directory name and make `description` contain concrete triggers. The specification requires the match and recommends descriptive keywords; OpenAI notes that long skill lists may shorten descriptions, so the main trigger should be front-loaded ([Agent Skills specification](https://agentskills.io/specification), [OpenAI skill guidance](https://learn.chatgpt.com/docs/build-skills)).
2. **Client presentation:** retain `agents/openai.yaml` with `display_name`, `short_description`, a representative default prompt, and an explicit implicit-invocation policy. Add icons or brand color only if real visual assets exist; do not create decoration that adds licensing or maintenance burden.
3. **GitHub discovery:** set a concise repository description and relevant topics such as `agent-skills`, `codex`, `code-quality`, `software-architecture`, `dead-code`, and `static-analysis`. GitHub states that topics help people find related repositories and projects to contribute to ([GitHub topics documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics)).

Add license and compatibility information because they describe real constraints rather than marketing metadata. The portable specification places `compatibility` at the top level, but the current Codex validator requires this temporary equivalent:

```yaml
license: MIT
metadata:
  author: philipgierszal
  compatibility: Requires Git and Python 3.10+; designed for coding agents with shell access.
```

A per-skill version in metadata is optional and non-normative. If used, automate it from the repository release; otherwise omit it to avoid a second stale version source.

Implementation note (2026-08-26): the current local Codex `quick_validate.py` accepts `name`, `description`, `license`, `allowed-tools`, and `metadata`, but rejects the specification's top-level `compatibility` key. This repository therefore carries the truthful requirement as the string `metadata.compatibility` and in the README until Codex validation converges with the portable specification.

## Contribution and review contract

`CONTRIBUTING.md` should make a small contribution easy while protecting behavior:

- state accepted contribution types: fixes to existing skills, new adapters/references, verified examples, and proposed new skills;
- require a focused issue for large or behavior-changing work, but allow typo/documentation PRs directly;
- give the exact setup and validation commands;
- require `SKILL.md` frontmatter to validate, referenced paths to exist, and scripts to be deterministic and safe by default;
- require trigger tests and before/after behavioral evidence when instructions or invocation policy change;
- require catalog/README updates for stable new skills;
- require source and license provenance for copied code, data, templates, or media; and
- explain the lifecycle: experimental work is not advertised as stable, deprecated skills remain discoverable only long enough to provide migration guidance, then are removed in a major release.

The pull-request template can borrow Superpowers' most valuable questions—problem, change, alternatives, tested environment, evaluation delta, and human review—without copying its 143-line, multi-harness submission ceremony ([Superpowers PR template](https://github.com/obra/superpowers/blob/main/.github/PULL_REQUEST_TEMPLATE.md)). For this repository, a roughly 20-line template with checkboxes for validation, behavior evidence, documentation, and provenance is proportionate.

Add a Contributor Covenant only when there is a maintained reporting address and willingness to enforce it. Superpowers includes the Contributor Covenant and a concrete enforcement contact ([Superpowers Code of Conduct](https://github.com/obra/superpowers/blob/main/CODE_OF_CONDUCT.md)); copying the file without a real contact or enforcement owner would create a promise the project cannot meet.

Because this skill executes repository analyzers and bundled scripts, publish `SECURITY.md` with a private vulnerability-reporting channel before actively promoting it. Keep ordinary bugs in public issues and secret-handling, command injection, path traversal, or destructive-behavior reports private.

## Licensing and provenance

Keep the existing root MIT license. Both comparison repositories use MIT for their software and skill collections ([Matt Pocock license](https://github.com/mattpocock/skills/blob/main/LICENSE), [Superpowers license](https://github.com/obra/superpowers/blob/main/LICENSE)). Add `license: MIT` to each skill's frontmatter so the installed unit carries an unambiguous license declaration, as supported by the Agent Skills specification ([Agent Skills specification](https://agentskills.io/specification)).

Do not add `NOTICE`, `ThirdPartyNoticeText.txt`, or a provenance manifest until third-party material is actually copied or redistributed. Links and credited inspiration in research/design documentation do not justify importing upstream files. If future skills include copied scripts, templates, images, fixtures, or substantial text, retain the original notice and document source, version/commit, license, and modifications next to the owning asset.

## Examples, validation, and CI

### Examples

Publish only examples that are generated from a known fixture and kept current. A good first example set would contain:

- a minimal `.architecture-hygiene.yml` policy;
- a shortened human-readable audit report; and
- a machine-readable ledger that passes the repository validator.

Link them from the skill catalog entry. Keep runtime templates under the skill's `assets/`; keep explanatory sample output under root `examples/` so it is not installed unnecessarily.

### Deterministic validation

The Agent Skills specification names `skills-ref validate ./my-skill` as the reference frontmatter validator ([Agent Skills specification](https://agentskills.io/specification)). The implemented pull-request workflow is deliberately deterministic and network-independent after dependency installation:

1. parse every stable skill's YAML frontmatter and assert its required metadata;
2. check skill-relative Markdown links;
3. run `python -m unittest discover -s tests -v`;
4. run Ruff and compile the Python sources; and
5. reconcile the maintained inventory/ledger fixture.

After the repository is public, use `skills-ref validate` and a clean-room `npx skills` discovery/install against the public URL as manual release gates. Move them into CI only after their versions and supported runtimes are pinned and exercised. Keep the README command on `skills@latest` for end users, where the priority is a current interactive installer.

### Behavioral evaluation

Retain eval specifications and RED/GREEN results in `evals/`. Superpowers explicitly requires behavior tests and evaluation evidence for skill changes ([Superpowers contributing section](https://github.com/obra/superpowers/blob/main/README.md), [Superpowers PR template](https://github.com/obra/superpowers/blob/main/.github/PULL_REQUEST_TEMPLATE.md)); Matt's changelog similarly records invocation-policy and cross-harness behavior changes, not only file edits ([Matt Pocock changelog](https://github.com/mattpocock/skills/blob/main/CHANGELOG.md)).

Do not make paid or nondeterministic model evals a required check on every external pull request. Require recorded before/after evidence for behavioral changes and run the full eval suite at maintainer review or release time. Deterministic schema, script, and fixture tests should remain the merge gate.

## Release and versioning policy

Start simple:

- `main` is releasable;
- feature branches merge through pull requests;
- every user-visible change is summarized under `Unreleased` in `CHANGELOG.md` after the first tagged release;
- tag the first public, validated state `v0.1.0` if the contract is still evolving, or `v1.0.0` only when compatibility and output contracts are intentionally stable; and
- create a GitHub release for each tag with install/update instructions, added/changed/deprecated/removed sections, and any migration notes.

Use repository-wide semantic versioning while all skills ship together:

- patch: corrections that preserve triggers, safety, and report/schema contracts;
- minor: a new backward-compatible skill or additive capability;
- major: removed/renamed skills, changed invocation policy, new side effects, incompatible script requirements, or breaking output/schema changes.

Matt's Changesets workflow and Superpowers' synchronized manifest versioning are good later-stage patterns, but they should be introduced only when manual release preparation becomes error-prone ([Matt release workflow](https://github.com/mattpocock/skills/blob/main/.github/workflows/release.yml), [Superpowers release notes](https://github.com/obra/superpowers/blob/main/RELEASE-NOTES.md)). Until a plugin or package exists, the repository tag is the single version source.

## Immediate implementation checklist

1. Change the GitHub repository visibility to public and set its description/topics.
2. Rewrite the README around the public install and first-use path; remove the private-repository warning.
3. Add `license`, `metadata.compatibility`, and `metadata.author` frontmatter to the current skill while documenting the temporary Codex compatibility workaround.
4. Add `CONTRIBUTING.md`, `SECURITY.md`, concise issue forms, and a pull-request template.
5. Add a validation workflow that runs structural package tests, lint, compilation, and the smoke fixture; reserve reference validation and installer discovery for the post-publication release gate.
6. Add one verified example report/policy pair rather than placeholder directories.
7. Create the first repository tag/release only after the public URL, clean-room install, and CI pass have been verified.
8. Defer plugin manifests, Changesets, category buckets, setup/router skills, and multi-harness bootstrap code until their triggering need exists.
