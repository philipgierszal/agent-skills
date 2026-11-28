# delivery-lead: evaluation record

## 2026-11-28, baseline failure and dry read

- Context: a small company moving from an old ERP to Odoo. One owner, often on a phone, sends several asks per message; AI agents do the analysis, build and checks. Every ask has a row in a monthly asks register with a type and a status (received, in progress, written not verified, done verified, waiting on the owner, rejected).
- Failure that motivated the skill, measured from the register on 2026-11-28: features that were finished took a median of 1 day from the ask (35 features), but 41 features were still open with a median age of 4 days, and 118 tasks were open with a median age of 9 days. The owner said simple features took far too long and that they felt a loss of control. The bottleneck was work started and not finished, not the speed of any one build. Questions to the owner arrived late and one at a time; several rows reached "written, not verified" and stayed there because no separate session was asked to check them.
- Dry read of the skill against the register (read-only, Claude Code, Opus 5.5, same day):

| Check | Register state | What the skill does |
|---|---|---|
| Finish first (limit 3 per repository) | 9 feature rows in progress, all in the ERP repository | No new feature build starts in that repository; the lead orders the 9 by impact (production refuses work, then data, then convenience) and finishes or parks the extras |
| Verify step | 17 feature rows and 49 task rows at "written, not verified" | The lead starts read-only verifier sessions for the oldest first; only a verifier's pass sets "done, verified" |
| Questions round | Owner answers came as single pop-ups across the day | One batch per ask at intake; unasked points recorded as "assumed: …" |
| Small-change lane | Small fixes waited for the next large release | Same-day test environment, one daily release at the profile's time after one approval for the day's list |

- What this record does not yet show: a full run of one feature through all eight steps with the new skill, and its effect on the median age of open features. Record that run here (feature, steps, dates, verifier) when it happens, and the register's open-feature count and median age one week after the skill was installed.
