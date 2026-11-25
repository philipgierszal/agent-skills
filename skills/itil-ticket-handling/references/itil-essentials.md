# ITIL essentials for a small support team

What the skill takes from ITIL 4 and KCS v6, and what it leaves out. The official ITIL 4 practice guides are paywalled; definitions below come from secondary sources that quote them, and each inference is marked. The research record with sources is `docs/research/itil-ticket-handling.md` in the repository this skill comes from.

## Ticket types

| Type | ITIL 4 meaning | Quick test | Route |
|---|---|---|---|
| Incident | An unplanned interruption to a service, or a reduction in its quality. | "It worked yesterday, it does not today." | Restore service first (workaround allowed), then fix. |
| Service request | A user-initiated request that is an agreed part of service delivery (access, a report, a setting). | "I did not have it yesterday, I need it today, and it is a normal thing to ask." | Fulfil; no diagnosis needed. |
| Change request | Adding, modifying or removing anything that could affect services. | "Make the system work differently." | Change enablement: build, test, approve, release, verify. |
| Idea | *Inference:* ITIL 4 has no term for a feature idea; treat it as a proposed change. | "It would be nice if…" | Register it, tell the requester where it went; accept or mark not planned. |
| Problem | The cause, or potential cause, of one or more incidents. | Second ticket with the same cause; unknown cause after diagnosis; workaround in use. | One problem row linked from every ticket. |

A **known error** is a problem that has been analysed but not resolved. A **workaround** reduces or removes the impact when no full fix exists; record the symptoms and context it applies to.

## Priority

ITIL 4 sets priority from **impact** (how many people, how much money or customer exposure) and **urgency** (how soon work stops or harm grows). Official matrices are illustrative; a small team needs three levels.

| Impact ↓ / Urgency → | Work blocked now | Work slowed, workaround exists | Can wait |
|---|---|---|---|
| Many people, customers or money | High | High | Medium |
| One team or one process | High | Medium | Low |
| One person | Medium | Low | Low |

Security and financial-data issues are always High. *Inference:* target the first response within the working day for High, the next working day otherwise; no minute-level service levels.

## States

ITIL 4 lists activities (log, categorise, prioritise, resolve or escalate, close), not mandatory states. Tools add states such as Waiting for user, Resolved and Closed. The skill's nine-step lifecycle maps those activities onto any queue's stages through the site profile.

- **Resolved** means the fix is delivered and the requester is asked to confirm; **closed** is final. A requester who rejects the resolution sends the ticket back to work.
- No ITIL source sets an auto-close window. Vendor defaults range from 3 business days (Jira Service Management templates) to 7 (ServiceNow). *Inference used by the skill:* reminder after 2 working days, close on silence after 5, and any reply reopens.
- Never auto-close an incident that blocks work, or one whose facts are still unclear.
- *Design choice, not ITIL text:* a ticket whose fix is a release resolves only after the release is installed and verified on production. ITIL separates restoring service (incident resolution) from deploying the permanent fix (problem closure).

## Change enablement

- Change types: **standard** (pre-authorised, low risk, documented), **normal** (assessed and authorised by a change authority according to risk), **emergency** (expedited assessment, record completed afterwards).
- The change authority can be a person, a team or an automated check; a change advisory board is not required. *Inference:* in a one-owner company the owner is the change authority; agent reviews and passing tests support the approval and do not replace it.
- A change record names: the reason, scope, affected service, test evidence, rollback and its trigger, schedule, approval, and links to the tickets it fixes.
- Verify after release: objective met, plan followed, no rollback needed, no new incidents. Review a change formally only when it failed or caused an incident.

## Escalation

- **Functional:** to whoever owns that part of the system, or to the vendor.
- **Hierarchic:** to the owner, for decisions, money, priorities or approvals.
- ITIL 4 also allows **swarming**: several people (or agents) work one ticket together under one named owner instead of passing it down tiers.

## Communication

- ITIL 4's service desk practice stresses empathy and communication adapted to the user's level: users judge the whole service by how the desk handles their problem.
- Requester-visible messages hold questions, status, workaround and resolution; internal notes hold the diagnosis trail and technical detail. Choose the type deliberately on every entry: tools have sent internal detail to requesters, and resolutions out without explanation, through a wrong default.
- Search first, then ask. *Inference:* at most three numbered, closed questions in one message, each with likely answers and the assumption you will make if there is no answer.
- Give a "next update by" with every update on a long-running ticket; *inference:* weekly while waiting for a release.

## Knowledge (KCS v6)

- KCS captures knowledge inside the work, not afterwards. Solve loop: capture, structure, reuse, improve; evolve loop: process integration, content health, performance assessment.
- Article structure: **issue** (in the requester's words), **environment**, **resolution** (numbered steps), **cause** (optional). Keep requester-specific data out.
- Search before writing; "flag it or fix it" when an existing entry is wrong.
- *Inference:* a small team skips the evolve-loop machinery: write or update one entry when a ticket teaches something reusable and review the most-used entries now and then.

## Left out on purpose

A configuration management database, support tiers, a change advisory board, a separate known-error database, problem and change manager roles, separate change request forms (the ticket and the register row carry the record), satisfaction surveys beyond the confirmation question, and minute-level service levels.
