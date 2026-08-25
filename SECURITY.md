# Security Policy

## Supported version

Security fixes are applied to the latest revision on `main`. No tagged release is currently supported separately.

## Report a vulnerability privately

Use GitHub's private [Report a vulnerability](https://github.com/philipgierszal/agent-skills/security/advisories/new) form. Do not open a public issue for a vulnerability or include exploit details in a public pull request.

Private reporting is appropriate for issues such as:

- command or argument injection in bundled scripts or generated analyzer commands;
- path traversal, unsafe symlink handling, or writes outside the documented audit output;
- accidental secret collection or disclosure;
- destructive behavior that contradicts a skill's safety boundary; or
- a dependency or installation path that could execute untrusted code unexpectedly.

Include the affected skill and revision, environment, minimal reproduction, impact, and any suggested mitigation. Remove real secrets and private customer or repository data from the report.

Ordinary correctness bugs, false positives, documentation errors, and feature requests can use GitHub Issues unless publishing them would expose a security weakness.

## Scope note

Skills instruct an agent and may invoke tools available in the user's environment. Users should review requested commands, repository permissions, installed dependencies, and generated artifacts before acting on findings. The `architecture-hygiene-audit` skill does not authorize source deletion or remediation.
