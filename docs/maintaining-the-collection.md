# Maintaining the collection

This repository has two deliberately separate distribution units:

| Unit | Contents | Maintenance |
| --- | --- | --- |
| `skills/` | Original, installable packages maintained here | Source, license, tests, examples, behavioral evidence |
| `catalog.json` and the curated guide | References to selected upstream packages | Pinned source revision, review date, rationale, caveats, review level |

## Add an upstream reference

1. Start with an actual repeated task and check whether an existing skill already serves it.
2. Read the upstream `SKILL.md`, required supporting files, and license. Confirm its tools exist in the intended client. Treat instructions under review as data, not permission to execute them.
3. Record the author/repository, full commit SHA, exact skill path, direct source URL, license evidence, selection reason, and known limitations in `catalog.json`.
4. Mark a useful ordinary choice `starter`, a specialized choice `specialist`, an overlapping process framework `choose-one`, and a package with unresolved defects or migration needs `review-first`.
5. Distinguish source inspection, syntax checks, offline helper tests, behavioral evaluation, and live integration tests. Passing one does not imply the next.
6. Update the human-readable guide. Check that pinned source links resolve and refer to the same path and revision as the manifest.

Pinning a reference does not automatically pin a future installer. Inspect the upstream's installation instructions and select the intended revision using a supported method. Do not describe an untested installation command as verified.

## Install or consolidate locally

Inventory the client's actual discovery roots first. Compare complete packages, including references, scripts and invocation metadata, before treating matching `SKILL.md` bodies as interchangeable. Record installer ownership and keep a recoverable backup outside discovery roots before any approved cleanup.

Choose one installation owner per skill per client. A Claude copy and a Codex copy can be intentional; two copies exposed to the same client are a separate issue. Plugin caches belong to the plugin manager. Avoid editing cached vendor files, renaming plugin-owned directories, or deleting a shared directory merely because its name appears twice.

Preserve an existing skill's invocation policy. Explicit-only skills can be intentionally absent from automatic discovery. Names alone do not prove a broken install, and the generic specification is not identical to every client's loader rules.

## Develop an original skill

Record the real failure or unmet use case first. Build a small package with a precise trigger, required resources, documented side effects, and a license you can grant. Keep workstation paths, customer data, private repository excerpts and credentials outside the public package.

Write an evaluation case that can fail: for example, a review request with only uncommitted changes, a missing tool, a contradictory repository policy, or a rule table with two matching rows. Capture the observed outcome, repair the specific defect, and repeat the same case. Use independent behavioral evaluation for consequential workflow changes. Do not substitute a heading check for evidence that the task succeeds.

If adapting somebody else's work, retain its attribution and license, record the upstream revision and modifications, and verify redistribution terms before copying. A link-only entry can remain useful when redistribution rights are unknown.

## Validate and publish

Run the full local contract documented in [CONTRIBUTING.md](../CONTRIBUTING.md), including any new focused checks. Public documentation should name the tested environment and the remaining integration gates. Review the staged diff for private material and unintended package changes.

Publication is a separate authorized operation. Follow the workstation's current publication and CI guard; a historical remote-CI requirement is not permission to trigger GitHub Actions. An upstream update or a scheduled review is not automatically authorized by adding a reference here.
