# Selected repair patches

These are reviewed local adaptations, not upstream releases or installable skills. The [repair record](../../docs/skill-repairs.md) covers the larger local repair effort. The catalog continues to reference upstream versions and does not apply patches automatically.

| Patch | Change |
| --- | --- |
| [Supply-chain auditor](supply-chain-risk-auditor.patch) | Native Windows cache ownership check and offline regression tests |
| [Specification compliance](spec-to-code-compliance.patch) | Direct host-agent workflow replacing missing mandatory orchestration dependencies |

Both derive from [Trail of Bits skills](https://github.com/trailofbits/skills), with exact catalog source references in [provenance.json](provenance.json). Adaptations by Philip Gierszal and Codex, 2026-09-05. Original material and these derivative patches are licensed under [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/). Preserve attribution and share-alike terms when redistributing adaptations. No endorsement by the original authors is implied. This license applies to these patches independently of the repository's default license.

To evaluate a patch, use a recovery-backed copy of the relevant complete skill package and inspect the diff. Patch paths are relative to that package root. Run `git apply --check <patch-path>` there before applying it; reject mismatches rather than forcing an unknown revision. The original package and dependencies are not bundled here. Run its relevant tests after application.

The Windows ownership check uses Windows PowerShell and fails closed if ownership lookup fails. It does not assess every ACL permission. Its offline suite excludes a port-binding test under the local test policy. The specification workflow requires actual source inspection and honest coverage records; it is not an automated correctness proof.
