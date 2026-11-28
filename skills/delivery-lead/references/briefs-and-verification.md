# Briefs and verification

A brief is the only context a fresh session gets. A short, complete brief costs far less than a long session re-reading history: re-reading context was measured at over 99% of tokens, and sessions over 200 steps took half of everything.

## Builder's brief

```markdown
# <date> <feature> (<ask ID>)

Goal: <acceptance sentence; what must be true and verified>.
Read first: <state file path>, <options note path>, <the rules file and sections that apply>.
Scope: <files or module>; out of scope: <...>.
Design: <the chosen option and the design points from the state file>.
Test: <failing test first, or the real run on which test copy>.
Environment: <where it may write without asking>; never <production systems>.
Lane: <small / normal>.
Model: <model and effort from the profile>. Step cap: <50-80>.
Stop only for: a data question or an owner decision. End the first turn with
`Questions for the owner` (options and a recommendation each) if there are any,
and build only after the answers.
Finish: gate green once, commit, push, update the state file and the register row
to "written, not verified". Report: Done / Not done / Needs you.
```

Rules for the lead while the builder works:

- Do not build the same files in parallel; one writing session per area.
- Wait with a watcher, not by polling; when the builder reports, review its diff against the brief (not the repository).
- Relay the builder's `Questions for the owner` as pop-ups at once and send back the owner's words, quoted.
- Two failed rounds: change approach or ask the owner one question; never a third blind retry.

## Verifier's brief

The verifier is a separate session that only reads. It never fixes what it finds; it reports, and the lead or the builder fixes.

```markdown
# <date> verify <feature> (<ask ID>)

Read-only. Do not change code, data or configuration.
Acceptance sentence: <...>.
Where: <system and environment>, as role <test role>, in the users' language.
Steps: <the user's steps, from the state file>.
Also check: <the requirement text vs the code (spec compliance), the diff for
correctness, any document that must change with it>.
Evidence to return: pass/fail per acceptance check, how and when checked,
anything that differs from the brief.
Model: <cheaper model for reading, unless production or security>.
```

Only the verifier's pass lets the row move to "done, verified", with `Checked by:` naming the verifying session, and how and when. A pass on a test copy verifies the build; "done, verified" for a released change needs the check where users work.

## Small-change lane

A small change is configuration, or one module change up to about 50 lines with no data migration (the profile may set other limits).

1. Built and tested the same day, on the test environment.
2. Verified there by the separate session.
3. Collected on the day's release list: ask ID, one line of what changes for users, the check done, the rollback.
4. At the profile's daily release time (for example 12:30), one owner approval for the whole list, asked as one pop-up; then one release.
5. Checked where users work; row to "done, verified" by the verifier.

A change that grows past the small limits during the build moves to the normal lane, with a note in the row.
