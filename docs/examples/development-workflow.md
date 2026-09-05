# Worked example: close an assigned support ticket

This is a synthetic design walkthrough, not approved policy for an existing application. All verification below is **planned, not executed**. The feature record is shown as one document to demonstrate the minimal workflow.

## Need and scope

**NEED-01:** An agent needs to mark a resolved assigned ticket as closed so that the active queue reflects remaining work. In a real project, attach the interview, observed workflow, request or existing specification that establishes this need.

**STORY-01:** An active support agent can close an assigned ticket after recording its resolution. Reassignment, bulk closing, reopening and cross-tenant support are outside this illustrative change.

This distinction matters: the story is a useful outcome; adding a database column or endpoint is an implementation task. [INVEST and tasks](https://xp123.com/invest-in-good-stories-and-smart-tasks/)

## Accepted criteria for the example

| ID | Observable criterion |
| --- | --- |
| AC-01 | An active agent closes an open ticket assigned to them in their own tenant, with a nonempty resolution |
| AC-02 | An unauthenticated/inactive actor, wrong role, different tenant or different assignee cannot close it; denial changes no ticket data and queues no work |
| AC-03 | This operation cannot alter tenant, assignee or other protected properties through additional request fields |
| AC-04 | A ticket that is no longer open cannot be closed again through this transition |
| AC-05 | A competing assignment or state change is handled according to the agreed transactional rule; a stale authorization decision cannot silently authorize the write |

For a real project, the product owner must settle whether managers, delegated agents or background services have additional rights. Their absence from this example is not a recommendation to remove existing permissions.

## ADR-EX-01: retain role plus scoped policy predicates

Status: illustrative accepted decision for this example only.

Context: an agent role does not identify which ticket, tenant or state is permitted. The hypothetical application already has a server-side policy mechanism.

Options: role-only checks; the existing policy mechanism with tenant/assignee/state predicates; a new external policy service.

Decision: use the existing mechanism with explicit predicates. Role-only checks cannot express the required scope; a new service adds no demonstrated benefit for this change.

Consequences: all closure entry points must call the policy and preserve its decision through the state update. Tests cover each relevant denial boundary. A future shared-policy requirement can supersede this decision. This compact record follows the purpose of ADRs without implying that every authorization edit needs one. [Original ADR guidance](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)

## Specification excerpt

AUTH-01 permits `ticket.close` only when all conditions hold: actor is active and authenticated, actor has the support-agent role, actor and ticket belong to the same tenant, actor is the current assignee, and ticket state is open. The resolution is the only client-writable property in this operation.

Read actor identity from the trusted session and ticket attributes from persisted state. Recheck the relevant state consistently with the update. No applicable allow rule means deny. The exact API error shape and concurrency strategy must use the real application's conventions; these are implementation details to settle before coding, not fabricated facts about a repository.

Read-field policy and list visibility are separate rules if this feature changes them. Supplying an object ID or a hidden UI control does not establish access. [OWASP object-level authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)

## Tasks and evidence

| Task | Criteria | Planned evidence |
| --- | --- | --- |
| TASK-01: implement scoped policy and transition | AC-01, AC-02, AC-04 | Intended closure plus independently specified denial cases |
| TASK-02: restrict request properties | AC-03 | Attempted tenant/assignee/property injection changes nothing prohibited |
| TASK-03: preserve authorization through competing updates | AC-05 | Controlled concurrent assignment/state-change test |
| TASK-04: wire the supported entry points and UI | AC-01–AC-05 | Integration checks; real browser checks if UI changes |
| TASK-05: review changed code against the contract | AC-01–AC-05 | Functional and authorization findings, fixes and repeated relevant checks |

Minimum denial cases: wrong role; same role with another tenant's ticket ID; same tenant with another assignee's ticket; inactive actor; prohibited extra fields; already-closed ticket; assignment changed before update. Include any applicable alternate API or background path in the scope rather than assuming the visible endpoint is the only route.

At handoff, each row receives a concrete test or manual-check reference, tested revision/context, observed outcome and remaining limitations. Until those checks run, the status is **specified**, not verified or released. A missing cross-tenant test remains missing even if the rest of the suite is green.
