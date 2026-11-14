---
name: process-model-review
description: Use when asked to audit, review or check a company's documented business processes (process pages, BPMN diagrams, process maps) for coverage, clarity, coherence, system mapping, controls or KPIs, or to find which processes are missing, against reference models and the systems' real data.
license: MIT
metadata:
  author: philipgierszal
  compatibility: Requires Git and Python 3.10+; read access to the process repository; read-only database access is optional (needed for process mining).
---

# Process Model Review

Judge processes the way a process owner and an auditor would. Boxes and arrows are the last thing to check. First ask whether the process is the right one, whether the documented logic matches what the business and its systems actually do, and whether a new employee could follow it. Read-only: findings and a report, no edits to the processes under review unless asked.

## Baseline: what to measure against

No single source is enough. Use all four, and say which one each finding rests on.

1. **Reference models, for coverage and naming.**
   - APQC PCF 8.0 (cross-industry) is the process list.
   - SCOR DS (Plan, Order, Source, Transform, Fulfill, Return, Orchestrate) covers the supply chain.
   - ITIL 4 / ISO/IEC 20000 cover service requests, incidents and SLAs.
   - The target system's standard flows: for Odoo, its documentation for the version in use.
   
   A reference process with no page is a candidate gap, not a defect.
2. **Modelling-quality rules, for clarity.** Use 7PMG and BPMN Method & Style; the checks are below.
3. **The systems' real data, for logic.** Rebuild document chains from the ERP and compare them with the documented flow (process mining).
4. **People, for the why.** Interviews and walkthroughs explain exceptions and rules that data can't show. Mark anything they have not confirmed as unconfirmed.

Old mappings (such as a vendor's mapping from years ago) are a starting point, never evidence that a process works that way today.

## Checks per process

**Purpose and boundaries**
- One trigger.
- A named outcome as an end state.
- An owner role.
- Clear hand-offs to neighbouring processes, each with a sending and a receiving role.

**Clarity**
- Verb-object activity labels.
- One start and one end per level; end events named for the end state.
- No implicit starts or ends, no dead ends, no orphan paths.
- No more than about 50 elements per level, otherwise decompose.
- No OR gateways where XOR will do.
- One decomposition rule across the whole map.

**Coherence**
- Role names are identical across pages and match the role register.
- Every sub-process referenced exists.
- The same business object has the same name everywhere.
- Every cited reference code (PCF/SCOR) exists.

**Business logic**
- Every decision (credit limit, discount, approval, routing) has a stated rule, preferably as a decision table (DMN style), not buried in prose.

**Systems**
- Every step names the system and the document or record it creates.
- Steps outside any system are marked as such.

**Controls**
- Segregation-of-duties pairs, for example:
  - quote vs price approval;
  - sales vs credit release;
  - purchase order vs goods receipt;
  - goods receipt vs invoice posting;
  - admin vs account review.
- Each is either enforced or recorded as an exception.

**Measures**
- At least one KPI per process, with its source (APQC measures, SCOR metrics).

## Procedure

1. **Inventory.** List every process page and diagram. Parse its trigger, outcome, roles, systems, sub-processes and reference codes.
2. **Structural checks.** Run them on the diagrams (BPMN XML can be parsed). Script the mechanical ones.
3. **Coverage matrix.** Map each page to PCF and SCOR codes. List reference processes with no page, and pages with no reference process (which may be legitimate local processes). Also list every process the repository *talks about* (in other pages, requirements, delivery logs, decisions) that has no page.
4. **System mapping.** For each process, check which systems and documents it names against the system register and, where possible, the database.
5. **Data check (read-only).** Build an event log from document chains, for example offer → order → goods issue → invoice → payment, with case ID, activity, timestamp and user. One order spans many documents, so the object-centric form (OCEL 2.0) fits best; PM4Py reads it. Compare the variants found with the documented flow. Report steps that appear in the data but not in the documents, and the reverse.
6. **Rules, controls and KPIs.** Check each page for them.
7. **Readability test.** Read each page as a new employee in that role and note where you could not tell what to do next.

## Output

- One findings table per process: ID, check, evidence (file:line or query), severity, recommendation.
- Severity levels:
  - **Critical:** a missing or broken control, or a documented flow that the data contradicts;
  - **Major:** a coverage gap, a dead end or an incoherence across pages;
  - **Minor:** labels and naming;
  - **Info:** an observation.
- A coverage matrix: reference process ↔ page ↔ systems ↔ status.
- A short summary: the five most important findings, and what is unconfirmed and needs an interview.

Sources and caveats: [references/sources.md](references/sources.md).
