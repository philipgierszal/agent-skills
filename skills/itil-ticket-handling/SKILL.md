---
name: itil-ticket-handling
description: Use when an agent picks up, answers, works on or closes a ticket that an employee raised about an internal business system - a helpdesk ticket, an in-app "report a problem / idea" form, a service-desk request - and must keep the requester informed the ITIL 4 way - log, classify, ask clarifying questions, diagnose, change, verify, resolve, confirm with the requester, close - with internal notes, requester messages and stage changes on the ticket itself. Includes an Odoo Helpdesk adapter.
license: MIT
metadata:
  author: philipgierszal
  compatibility: Requires Git and Python 3.10+ only for repository checks; the guidance itself bundles no scripts. Needs read and write access to the ticketing system (for Odoo, JSON-RPC as a user allowed to post on the ticket) and an organisation's site profile naming the team, stages, language, register and approval rules.
---

# ITIL Ticket Handling

Every ticket an employee raises gets the same treatment, whoever handles it: it is logged, classified, clarified, fixed through a controlled change, verified where the requester works, and closed only after the requester confirms. The requester sees progress on their own ticket; the people who approve changes see a record they can trust.

This is ITIL 4 incident management, service request management, problem management and change enablement, cut down for a small organisation whose support work is done by AI agents and whose owner is the only change authority. Background and sources: [ITIL essentials](references/itil-essentials.md).

## Before the first ticket: load the site profile

The organisation keeps a short **site profile** outside this skill. Read it before touching any ticket. It must name:

- the ticket queue (team), its stages and which ITIL state each stage stands for;
- the requester's language and the signature for messages;
- which writes the agent may make on the ticket without asking (for example: internal notes, messages to the requester, stage changes) and that every other write needs approval;
- where work is registered (the work register and the requirements list) and how IDs are cited;
- who approves releases to production, and how the agent reaches them;
- how build work is handed to another session or person;
- the guard checks to run after any write.

No profile, or the profile does not cover a step: do only reads, and ask the caller. The profile wins over this skill where they differ.

## The lifecycle

One ticket moves through these states in order. Skipping a state is allowed only when it has nothing to do (a clear ticket needs no questions); the note still says so. Stage names come from the profile; the table shows the usual mapping onto a four-stage queue (Received / In progress / Done / Not planned).

| # | State | Done when | Stage | On the ticket |
|---|---|---|---|---|
| 1 | Logged | The ticket exists with the requester, the screen or record it is about, and any screenshot. | Received | nothing yet |
| 2 | Classified | Type (incident, service request, change request or idea), impact, urgency, priority, and a register row exist. | Received | internal note: classification and register ID |
| 3 | Clarified | Every fact the fix depends on is known; the questions were asked and answered, or none were needed. | Received while waiting for the requester | message to the requester with at most 3 questions; internal note when answered |
| 4 | Diagnosed | Cause or gap found and reproduced outside production; the fix and its size are known. | In progress | internal note: diagnosis; short message: "we know what to change" |
| 5 | Change | The fix is built, tested and approved; linked to its register row and requirement. | In progress | internal note: change ID, test result, approval reference |
| 6 | Verified | The change is installed on production and checked there, by reading the live system or walking the requester's own steps. | In progress | internal note: how and when it was checked |
| 7 | Resolved | The requester was told what changed and asked to confirm. | In progress | message to the requester: what changed, where to look, "please confirm" |
| 8 | Confirmed | The requester confirmed, or did not reply within the profile's confirmation window. | Done | internal note quoting the confirmation, or noting the silence |
| 9 | Closed | Register row and any knowledge note updated; nothing open on the ticket. | Done | final internal note: register status, knowledge entry |

Rejected ideas or out-of-scope requests leave at step 2 or 4 to **Not planned**, always with a message to the requester saying why and what they can do instead.

### 1. Logged

Read the whole ticket: title, description (forms often add the page, record and action the user was on), attachments (open screenshots and look at them), tags, the requester's user, role and access groups. Note the time the ticket arrived; response time starts there.

### 2. Classified

- **Type.** Something that worked and now fails or gives a wrong result: *incident*. A standard ask (access, a report, a setting): *service request*. A change to how the system works (remove a field, change a printout): *change request*. A suggestion without a concrete need yet: *idea*. A ticket can hold several asks; split them into separate register rows and say so on the ticket.
- **Impact** (how many people or how much money or customer exposure) and **urgency** (how soon work stops or harm grows) give the **priority**, from the table in [ITIL essentials](references/itil-essentials.md#priority). Do not ask the requester for the priority; infer it and ask only when the answer changes it.
- **Repeat?** Search the register and open tickets for the same symptom. Two or more tickets with one cause: link them and open a *problem* row (see "Problems" below).
- **Register.** One register row per ask, before any other work, with the ticket number in it. A product change also gets a requirement in the requirements list. Cite both IDs in the internal note.
- **Owner decides scope.** Register the ticket as "pending owner decision". Create no requirement (FR/NFR) and no feature branch until the system owner decides whether to implement it and how to classify it; clarifying questions to the requester go ahead meanwhile. The requirement above is created only after that decision.

Internal note: `Agent: classified as <type>, priority <P> (impact <x>, urgency <y>). Register <Z-id>; requirement <FR-id or "none">. <one-line analysis>.`

### 3. Clarified

Ask only what you cannot find yourself. Read the screen, the record, the configuration and the logs first, and reproduce on a test copy.

When a question remains:

- **one** message, **at most 3 numbered questions**, plain words in the requester's language;
- each question is closed and offers its likely answers, so the requester can reply "1b, 2a": for example `1. Should the unit show "pcs" for every product, or the unit set on each product? (a) always "pcs", (b) the product's own unit`;
- say what you will do once you have the answers and that the ticket stays open meanwhile;
- address only the requester; no one else on the ticket, no separate e-mail.

Do not repeat a question the requester already answered. If an answer opens a new unknown, ask once more with the same limits; after two rounds without clarity, ask the owner (escalation) instead of the requester.

If the requester has not answered within the profile's reminder window (default 2 working days), send one short reminder. After a second window, note it, tell the owner, and leave the ticket in Received; never close an unclarified ticket on silence.

### 4. Diagnosed

Reproduce on a test copy (never by experimenting on production), read the code or configuration, and find the cause. Record in an internal note: what you reproduced, where, the cause, the proposed change and its size. Move the ticket to **In progress** and tell the requester in one or two sentences that the cause is known and what will change, without technical detail.

If the cause is in a third-party product, say so in the note, register the vendor ask, and give the requester the workaround if there is one.

### 5. Change

Every fix that changes the production system is a change:

- **Small and clear** (a setting, a translation, a field label) and allowed by the profile: build it, test it on the test copy, and request release approval.
- **Larger** (code, data migration, several asks): hand it to a build session or person, using the profile's hand-off method, with a brief that names the ticket, the register row, the requirement, the acceptance sentence and the test copy to use. Do not build it inside a short watch run.
- **Release to production always needs the approval named in the profile**, asked in the place the profile names, with the change, its test evidence and its rollback. Approval for one change does not cover another.

Internal note when the change is ready: change reference (branch, commit or configuration script), test result and where it ran, approval reference once given.

### 6. Verified

After the release, check the change on production the way the requester will meet it: read the live record or configuration, or walk the requester's steps with a role account if the profile allows it. "Deployed" is not "verified". Internal note: what was checked, how, when.

### 7. Resolved

Message the requester: what changed, where to see it (screen and menu path), and a request to confirm it works for them, with the likely answers ("works" / "still wrong: …"). Keep the ticket **In progress**.

A workaround is not a resolution: if only a workaround exists, give it, keep the ticket open, and keep the register row open.

### 8. Confirmed

The requester confirms: internal note quoting their words, stage **Done**. The requester reports it still fails: back to step 4 with the new facts, stage stays In progress. No reply: one reminder after 2 working days; after 5 working days from the resolution message (or the profile's windows), move to **Done** with a note that the ticket closed on silence, and tell the requester that a reply reopens it. Any later reply from the requester puts the ticket back to In progress.

### 9. Closed

Update the register row to its verified state with how and when it was checked. If the fix teaches something others will need (a recurring question, a workaround, a configuration rule), add or update one knowledge entry where the profile keeps knowledge (issue, environment, resolution, cause) and link it in the final note. Then nothing on the ticket is open.

## Problems

Open a problem when two or more tickets share a cause, when an incident's cause is unknown after diagnosis, or when a workaround is in use. The problem is a register row linked from each ticket. Each ticket still follows the lifecycle: it can be resolved by a workaround only if the requester accepts it, and the problem row stays open until the root-cause change is verified.

## Writing on the ticket

| Kind | Audience | Use for | Never |
|---|---|---|---|
| Internal note | the support team and the owner | classification, diagnosis, change and approval references, verification evidence, register status | addressed to the requester |
| Message to the requester | the requester only | acknowledgement, questions, progress in plain words, resolution, confirmation request | internal IDs, branch names, stack traces, other people's names |
| Stage change | everyone | the state table above | a stage the work has not reached |

Every message: in the requester's language, short, one subject, signed as the profile says. Start each internal note with `Agent:` so the next agent can tell agent work from human work. Use the system's own reply and note features; send nothing by e-mail or any other channel.

## Escalation

Stop and ask the owner (through the place the profile names, never through the requester) when:

- a write beyond what the profile allows is needed (any record other than this ticket, configuration, data, access rights, users or licences);
- a release to production is ready;
- the ticket asks for something only the owner can decide (money, priorities between departments, a rejected idea the requester disputes);
- two clarification rounds did not settle the facts;
- the ticket concerns a security or data-protection incident: then also stop public replies beyond an acknowledgement.

Write the escalation as one question with options and a recommendation, and note on the ticket (internally) that it waits for the owner.

## Each run

1. Find tickets that are **new** (no agent note yet) or **waiting on the agent** (the requester wrote after the agent's last entry, or a step finished elsewhere). If none, end at once.
2. For each, find its current state from the last agent note and the stage, then do the next state's work and write its entry.
3. After any write, run the profile's guard checks.
4. Report per ticket: number, state reached, what the requester was told, what waits on whom.

## Adapters

- [Odoo Helpdesk](references/odoo-helpdesk.md): reading tickets and attachments, posting notes and messages, changing stages, detecting new and waiting tickets.
