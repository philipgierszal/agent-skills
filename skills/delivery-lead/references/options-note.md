# Options note

The options note is the business analyst's and architect's work before any design. It lets the owner choose with one click and keeps the reason for the choice next to the feature.

## When

- Every feature and non-functional requirement, before design.
- Small change (one setting, one field, a label, up to about 50 lines in one module): the five-line form below.
- Not for tasks, bugs, research or decisions; their register row says "options: not needed (type)".

## Research first

Before writing options, spend a few minutes on facts, not opinions:

1. **Current state.** How users do it today, in which system and screen; read the live system, not old documents.
2. **What already exists.** Standard features or settings of the target system that cover the need, installed modules, earlier requirements and rejected ideas in the register.
3. **Other systems.** Where it helps, how two or three comparable systems (or the target system's own app store) solve the same need; one line each with a source link.
4. **Constraints.** Licences, data that must stay read-only, approvals, deadlines from the site profile.

Write what was checked and when. A fact not read from a source is an assumption and is labelled so.

## Full form

```markdown
# <Feature>: options

Register: <ask ID>. Requirement: <ID or "after choice">. Written <date> by <agent>.

## Need
<who, what changes for them, acceptance sentence draft>

## What we checked
- <source, date, finding>

## Options
| | A: <name> | B: <name> | C (optional) |
|---|---|---|---|
| What it is | | | |
| Pros | | | |
| Cons | | | |
| Cost (sessions, licences) | | | |
| Effect on people and data | | | |
| Lane (small / normal) | | | |

## Recommendation
<option, one or two sentences why>

## Owner's choice
<quoted answer, date>
```

Always at least two real options. "Do nothing" counts only when it is a serious choice; then the second option must still be a real build. Prefer the option that uses standard features over custom code, configuration over code, and the smallest change that passes the acceptance test.

## Five-line form (small change)

```markdown
<Feature> (<ask ID>): need - <one line>.
A: <option> - <pro>; <con>.
B: <option> - <pro>; <con>.
Recommendation: <A or B>, because <reason>.
Owner's choice: <quoted answer, date>.
```

## Asking the owner

One pop-up question: "Which option for <feature>?", the recommendation first, each option's label short and its description naming the main cost and effect. If the pop-up is too small for the comparison, put the table in the message just before it. Record the answer word for word in the note and in the register row.
