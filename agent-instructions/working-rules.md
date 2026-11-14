## Working with the owner

These rules come from reviewing a real collaboration (November 2026). The owner often works from a phone (Remote Control), sends many ideas in one message, and found that agents said "done" when work wasn't finished, drifted from what was asked, and asked for things that already existed. "Owner" means the person you work for.

1. **Every question is a pop-up.** Claude: the `AskUserQuestion` tool. Codex: `request_user_input` where available; otherwise end the turn with only the question and numbered choices. Never put a question only in prose or a summary box. One decision per question, 2–4 options, recommendation first, and enough context that the question stands on its own.
2. **Ask once, up front, for everything you will need.** Logins, password-manager entries, approvals and choices go in one pop-up at the start, not in a retry loop. Check the password manager, the repositories and earlier answers first; don't ask for what already exists.
3. **Register every ask before working on it.** In the same turn, give each ask from the owner a row in the project's asks register (its instructions name it): a number, a type, where the work lives, and a status. One message with several ideas gets several rows. A product feature also goes into the project's requirements list at once. Status runs received → in progress → written, not verified → done, verified (only with how and when it was checked), or waiting on the owner / rejected. Clarify a vague ask with one pop-up question, but register it first. Read the register at the start of a session, and update a row whenever its work moves.
4. **"Done" means verified.** Merged, pushed, deployed where it applies, and checked on the real system. If you only wrote the code, say "written, not verified". Never say "implemented" for something you didn't see working.
5. **Every report ends with three lines:** *Done* (and how it was checked), *Not done*, *Needs you*. Give a path or link for every deliverable, so the owner never has to ask "where is it?".
6. **Stay on the ask.** Say in one line what done looks like before starting. A new idea mid-task goes on the register; finish or explicitly park the current one first. When work remains and nothing blocks it, keep going instead of stopping to report status.
7. **A correction becomes a rule.** When the owner corrects you, update the rule's home right away (memory, these instructions or the project's rules), so the mistake doesn't happen twice.
8. **Run to the goal, not to the next status update.** A slice or batch session starts in goal mode with a done condition: what must be true and verified, or "blocked on the owner", or the step cap (about 100 steps) reached. Claude Code: `/goal <condition>`, in auto mode so tool approvals don't stall it. Codex: its goal mode.
9. **Side sessions never open pop-ups.** A pop-up in a session started from another one does not reach the owner's phone, even with Remote Control on, and the session blocks. A side session ends its turn with its questions, each with options and a recommendation, under a heading `Questions for the owner`. The parent session asks them as pop-ups and sends the answers back, quoting the owner's words. Never message a session that is blocked on a pop-up: the message queues and restarts it later. Status updates to the owner use plain words, not session jargon.
10. **Never ask the owner for "go".** When the owner asks for something, start it at once. If the app refuses to start a new session (it does in turns triggered by a background event or by a pop-up answer), hand the work to an idle linked session, or do it in this session. Stop only for a real clarifying question, asked as a pop-up.

## Working economy

Measured on one project (10–14 November 2026): over 99% of tokens went on re-reading context, and runs over 200 steps took half of everything. Cost is roughly steps × context per step × model price.

- One task per fresh session with a short brief. A planning session writes briefs and reviews results; it doesn't build through its own subagents.
- Stop at about 100 steps, at the brief's token budget, or after two failed fixes. Report, then split the rest.
- Choose the model for the job, and always pass `model` when spawning a subagent:
  - Haiku: searching and reading;
  - Sonnet: mechanical edits and diff reviews;
  - Opus at medium effort: code and planning;
  - Opus at high effort: design, production and security;
  - Fable: only when Opus at high is stuck.
  
  The guide is the `token-usage-review` skill's `references/model-and-effort.md`.
- Read only what the task needs: search for the lines, read ranges, don't re-read files already in context.
- Review the diff, not the repository. Run repository-wide audits only when asked.
- After each batch of work, run the `token-usage-review` skill. When a cause shows up twice, propose a one-line rule.
