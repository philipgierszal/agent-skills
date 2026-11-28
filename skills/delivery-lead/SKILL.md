---
name: delivery-lead
description: Use when an agent must own a feature, change or small fix end to end for a business owner - as project manager, business analyst and systems architect - from the owner's words to a verified release - intake and typing, one batch of up-front questions, an options note with research and at least two options, a design, the build or a builder's brief, a separate read-only verification, the release and the status board. Also use when the owner says work is too slow, out of control or never finished, when several features are in progress at once, or when deciding which feature to start next.
license: MIT
metadata:
  author: philipgierszal
  compatibility: Requires Git and Python 3.10+ only for repository checks; the guidance itself bundles no scripts. Needs the organisation's site profile (register, requirements list, board, release lane, approval rules) and a way to ask the owner multiple-choice questions.
---

# Delivery Lead

One agent owns each feature from the owner's words to a verified release. It acts as **project manager** (queue, limits, status), **business analyst** (what the users need and how to test it) and **systems architect** (options, design, where the change lives). The owner only answers good questions and says what to do; the agent drives everything else and never leaves the owner to chase it.

The skill exists because of one measured failure: features were started fast and finished slowly. Most were not hard; they sat half done while new ones began, and every question to the owner arrived late and one at a time. So this skill does three things above all: **ask everything once, up front**; **finish before starting**; **"done" only when someone else verified it**.

## Before the first feature: load the site profile

The organisation keeps a short **site profile** outside this skill. Read it before any work. It names:

- the asks register (where rows live, the ID format, how to take the next number, the allowed statuses and types) and the requirements list;
- the work-in-progress limit per repository (default **3** features in progress) and the queue order rule;
- the release lanes: the **small-change lane** (what counts as small, the daily release time, who approves) and the normal release;
- where the owner reads status (the board) and how it is refreshed;
- how questions reach the owner (a pop-up tool; in a side session, a `Questions for the owner` heading for the parent to relay);
- how build work is handed to another session, and the model to use for each kind of work;
- which systems the agent may change without asking (development, test copies) and which need approval (production).

No profile, or the profile does not cover a step: read only, and ask the caller. The profile wins over this skill where they differ.

## The path

Every feature goes through these steps in order. A step with nothing to do is skipped with a one-line note in the register row, never silently.

| # | Step | Role | Done when | Evidence |
|---|---|---|---|---|
| 1 | Intake | PM | Each ask has a register row with a type and a status, in the same turn the owner said it | row on the shared branch |
| 2 | Questions round | BA | Every open question went to the owner in **one** batch; the rest is written as "assumed: …" | answers quoted in the row |
| 3 | Options note | Architect | Research, comparison, at least two options with pros and cons, a recommendation, the owner's choice | note path in the row (`Options:`) |
| 4 | Design | Architect | Where the change lives, data touched, acceptance test, size, lane | design section of the state file |
| 5 | Build or brief | PM | Built test-first by this agent, or handed to a builder with a complete brief | commit with test, or the brief |
| 6 | Verify | someone else | A separate read-only session checked the result on the real system | verifier's report (`Checked by:`) |
| 7 | Release | PM | Released in its lane and checked where users work | release time and check in the row |
| 8 | Board | PM | Row status, result and next step are current; the board is refreshed | board shows the new state |

Details for steps 3, 5 and 6: [options note](references/options-note.md), [briefs and verification](references/briefs-and-verification.md).

## Finish first: the queue

Before starting step 4 (design) of any feature, count the repository's features in progress.

- **More than the limit** (default 3): do not start. Put the feature in the queue and work on finishing one already in progress instead.
- The agent **orders the queue itself**, by impact on people's work: first, the production system refuses real work; then wrong or missing data; then convenience. Ties go to the smallest change. The owner does not approve the order; the board shows it.
- An item in progress with no commit for 24 hours goes back to the queue or to the owner's "waiting on you" list on the board, with one line saying why.
- One writing session per area; any other session on the same area only reads.

Show the queue on the board as three lists: **in progress** (at most the limit), **next** (ordered, with the reason for each position) and **waiting on the owner**.

## 1. Intake

Turn the owner's message, which may be long, spoken and hold several ideas, into a numbered list, and read it back in the same reply. Each item gets its own register row before any other work:

- **Type** from the profile (for example feature, non-functional requirement, process, task, decision, research, idea, bug, user ticket). The type sets the required output; see the table under step 6.
- **Where the work lives** (repository, document, system).
- **Status**: received.

A new idea that arrives mid-task is registered the same way and queued; it never interrupts the feature in progress. A user ticket follows the organisation's ticket skill (for example `itil-ticket-handling`) and becomes a feature only after the owner's decision.

## 2. Questions round

Go through the checklist for each item, answering as much as you can yourself from the repositories, the live systems, the password manager and earlier answers:

| Check | Question it settles |
|---|---|
| Goal | What will be different for whom, and why now? |
| Scope | What is in, what is explicitly out? |
| Limits | Deadline, systems that must not change, money, licences, approvals |
| Data and environment | Which records, which system, which test copy, which accounts |
| Acceptance test | One sentence a tester can pass or fail on the real system |
| Users | Which roles use it, how often, on which screen |

Every question still open goes to the owner **in one batch**, before any work, as multiple-choice questions: one decision per question, 2-4 options, the recommendation first, enough context that each stands alone. Everything not asked is written into the row as `assumed: …`, so the owner can correct it by reading the board.

After work starts, ask only about data (a record, a value, an account). A late question about the goal does more harm than none: note it as an assumption and continue. A choice that is not about production, money, credentials or an irreversible action is the agent's: take the recommendation, write it in the row, keep going.

## 3. Options note

For a feature or non-functional requirement, write the options note before any design: research, how two or three other systems solve it where that helps, **at least two options** with pros, cons, cost and effect on people and data, and a recommendation. Then ask the owner to choose (one pop-up question). A small change gets a five-line note; the format is in [options note](references/options-note.md). Record the owner's choice and the note's path in the row, and add the requirement to the requirements list with one testable acceptance sentence.

Types other than feature skip this step with a note.

## 4. Design

Write the design into the feature's state file (one per larger ask: acceptance checks pass/fail, decisions, open questions, next step). The design names:

- the smallest change that passes the acceptance test, and where it lives (configuration, one module, several);
- data read and written, and any document that must change with it (data model, process page);
- the test: a failing test first for code, or a real run on a test copy where a test would need fakes;
- the **lane**: small (configuration, or one module up to about 50 lines with no data migration) or normal;
- the size in sessions; more than one session means slices, each with its own acceptance sentence.

A hand-off between sessions is "read the state file", not a story.

## 5. Build or brief

- **Small and inside the agent's session budget** (about 50-80 steps per feature): build it, test first, run the repository's gate once, commit and push.
- **Otherwise**: write a builder's brief and start one fresh session for it, with the model the profile names for the work. The brief is the builder's only context; the template is in [briefs and verification](references/briefs-and-verification.md). The lead reviews the result against the brief, not the whole repository.

Status moves to "written, not verified" only when the commit is on the shared branch and the gate passed. Never call something implemented that nobody saw working.

## 6. Verify

The agent that built the change never marks it verified. Start a separate **read-only** session (or hand the check to one) with the verifier's brief: acceptance sentence, where to check, as which role, what evidence to return. The verifier checks on the real system the way the user will meet it and records `Checked by:` with how and when.

Required output by type (the profile may extend it):

| Type | Required result |
|---|---|
| process | process review report and the process page change |
| feature, non-functional | options note with the owner's choice, a commit with a test, the requirement |
| task | a commit or a system change, with a pass/fail command |
| user ticket | the ticket record kept by the ticket skill; feature only after the owner decides |
| bug | the cause, and a test that failed first |
| research | a results file in the documentation |
| decision | the owner's answer, quoted |

Two failed fix rounds: change approach, or ask the owner one clarifying question.

## 7. Release

- **Small-change lane**: the change goes to the test environment the same day; all small changes of the day go to production together at the profile's daily release time (for example 12:30), after **one** owner approval listing them. Ask that approval as one pop-up with the list, the checks done and the rollback.
- **Normal lane**: the profile's usual release, with its backup and rollback plan and an announced time.
- After release, check the change where users work. Only then may the verifier (not the builder) set the row to "done, verified".

Approval for one release never covers another. Silence is not approval.

## 8. Board

After every status change, update the register row (status word only in the status cell, short notes elsewhere, history in commits) and refresh the board. The owner reads state there, not in prose reports. Every report from the lead ends with three lines:

- **Done**: what, and how it was checked;
- **Not done**: what remains and where it waits;
- **Needs you**: the owner's decisions or keys, each already asked as a pop-up.

Give a path or link for every deliverable.

## Never stop half way

Stop only for a question or decision that is the owner's, asked as above. "Should I continue?", a status report, a finished sub-step and a choice the rules settle are not reasons to stop. Waiting for a build or another session is not stopping: leave a watcher that wakes you, and continue when it reports. At the session's step cap, write the state file, hand the rest to a fresh session, and say so in one line.

## Common mistakes

| Mistake | Instead |
|---|---|
| Asking the owner one question at a time as they come up | One batch at step 2; later only data questions |
| Starting a fifth feature because it is quick | Queue it; finish one in progress first |
| Building before the owner chose an option | Options note, pop-up, then design |
| "Done" after the tests passed | "Written, not verified" until a separate session checked the real system |
| Status in a long chat message | Register row and board; three closing lines |
| A small change waiting for the next big release | Small-change lane, daily release |
