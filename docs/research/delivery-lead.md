# Delivery lead: one agent owns a feature end to end

Proposal for the `delivery-lead` skill, 2026-11-28. The repository's issue tracker was not reachable from the authoring session, so the proposal is kept here, as for earlier skills.

## Problem

In one real collaboration (an owner and several AI agent sessions moving a company to a new ERP), features were started quickly but finished slowly: the median finished feature took a day, while open features had a median age of four days and open tasks nine (register, 2026-11-28; see the [evaluation record](../../evals/delivery-lead.md)). The owner reported losing control and simple features taking too long. Causes seen in the register and session history:

- too much work in progress: new features started before earlier ones were verified;
- questions to the owner one at a time, late, sometimes about the goal after the build began;
- builds before options were compared, so rework after the owner saw the result;
- "done" said by the session that built the change, without a check on the real system;
- small changes waiting for large releases.

## Proposal

One skill that makes a single agent the **delivery lead** for each feature, combining the project manager, business analyst and systems architect roles, with eight steps: intake and type, one questions batch, options note, design, build or brief, separate read-only verification, release in a lane, board update. It enforces a work-in-progress limit per repository (default 3) with a queue the agent orders by impact, and a daily small-change release.

## Alternatives considered

| Option | Pros | Cons |
|---|---|---|
| A. One delivery-lead skill (chosen by the owner, 2026-11-28) | One place for the whole path; one agent accountable; reuses existing skills (ticket handling, process review, test-first) at their steps | A long skill; the organisation's details must live in a site profile |
| B. Separate PM, BA and architect skills | Smaller files, each reusable alone | Hand-offs between roles are where the work stalled; no single owner of "done" |
| C. Rules only, no skill | Nothing new to install | Rules were already written and still not followed in order; no checklist at the moment of work |

## Relation to existing practice

Work-in-progress limits and "stop starting, start finishing" come from Kanban (David J. Anderson, *Kanban*, 2010; [Kanban Guide](https://kanban.university/kanban-guide/)). Separating the builder from the verifier follows the ordinary four-eyes principle and ITIL 4 change enablement, where the change is checked before and after release ([ITIL essentials](../../skills/itil-ticket-handling/references/itil-essentials.md)). The options note follows the lightweight decision-record habit of listing at least two options with their consequences ([ADR, Michael Nygard 2011](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)). Numbers in the skill (limit 3, about 50 lines for a small change, 50-80 steps per session, a daily release time) are the owner's choices for one site, kept as profile defaults.

## Side effects

The skill itself writes nothing outside the work it leads. It asks the owner before any production write, release or credential use, follows the site profile for every other write, and never sends e-mail or messages to anyone but the owner.

## Validation

Deterministic: `tests/test_skill_package.py` checks the frontmatter, links, the eight steps in order, the work-in-progress limit and the separate verifier. Behavioural: the evaluation record, to be extended with the first full run.
