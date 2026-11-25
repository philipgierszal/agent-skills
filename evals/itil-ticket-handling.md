# itil-ticket-handling: evaluation record

## 2026-11-25, baseline failure and dry read

- Context: a small company moving to Odoo 20 Enterprise. Employees file "report a problem / idea" tickets from a top-bar button into a private Helpdesk team with four stages (Received, In progress, Done, Not planned). A scheduled agent picks up new tickets every 10 minutes.
- Failure that motivated the skill: the first two real tickets from a salesperson sat in Received with no reply for over an hour. The only entry on each was the form's automatic screenshot note, which the form posts as the agent's own user, so a naive "has the agent written here?" check would have counted both as handled. Nobody asked the requester anything, and the stage never moved.
- Dry read of both tickets against the skill (read-only, Claude Code, Opus 5.5):

| Ticket | Request (paraphrased) | State reached | Next step by the skill |
|---|---|---|---|
| A | Quotation printout: show the unit of measure differently, remove the delivery-date and transport-price lines | 1 Logged (requester, screenshot, page "home" only) | 2 Classified: change request, one team, can wait → Low; one register row per ask (three asks); internal note. 3 Clarified: which printout and which unit wording, with likely answers |
| B | Quotation form: remove the tax-included / tax-excluded choice and the "shipping" button | 1 Logged | 2 Classified: change request, Low; two asks. 3 Clarified: hide for everyone or for this role only; is the shipping cost ever added by hand |

- What the dry read checked in the live system before any write: no stage of the team has an e-mail, SMS or rating template; the requester is the only follower; the requester's notifications go to the Odoo inbox, so a requester message sends no e-mail.
- The adapter now counts only `Agent:`-prefixed notes and requester messages as agent work, because of the automatic screenshot note.
- Not yet measured: a full lifecycle on a real ticket (questions answered, change released, requester confirms). Record that run here, with the requester's confirmation, when it happens.
