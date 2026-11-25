# Odoo Helpdesk adapter

How to do each lifecycle step on an Odoo Helpdesk ticket (`helpdesk.ticket`, Odoo 17 or later, Enterprise). The examples use a JSON-RPC helper `kw(model, method, args, **kwargs)` that calls `/web/dataset/call_kw` as the agent's own Odoo user; use whatever session helper the site provides. Check every write against the site profile first: the snippets show *how*, the profile says *whether*.

## Find the queue and the agent

```python
team = kw('ir.model.data', 'search_read',
          [['module', '=', '<module>'], ['name', '=', '<team xml id>']], fields=['res_id'])[0]['res_id']
me = kw('res.users', 'read', [<agent user id>], fields=['partner_id'])[0]['partner_id'][0]
stages = {s['name']: s['id'] for s in kw('helpdesk.stage', 'search_read',
          [['team_ids', 'in', [team]]], fields=['name'])}
```

Resolve stages and tags by XML ID or by the team's own stage list, never by a hard-coded database ID.

## New and waiting tickets

```python
for t in kw('helpdesk.ticket', 'search_read', [['team_id', '=', team]],
            fields=['id', 'name', 'stage_id', 'partner_id', 'create_date'], order='id'):
    msgs = kw('mail.message', 'search_read',
              [['model', '=', 'helpdesk.ticket'], ['res_id', '=', t['id']],
               ['message_type', 'in', ['comment', 'email']]],
              fields=['id', 'date', 'author_id', 'subtype_id', 'body'], order='id')
    mine = [m for m in msgs if m['author_id'] and m['author_id'][0] == me]
    new = not mine
    waiting = mine and any(m['id'] > mine[-1]['id'] and m['author_id'][0] != me for m in msgs)
```

- **New:** the agent never wrote on it.
- **Waiting on the agent:** someone other than the agent wrote after the agent's last entry. Read that message first.
- A form may post an automatic note (a screenshot, for example) as the agent's own user. Count only entries that start with `Agent:` or were addressed to the requester as the agent's work, or the first ticket will look handled.
- The lifecycle state is in the last `Agent:` internal note; the stage alone is not enough, because several states share one stage.

## Read the ticket

```python
t = kw('helpdesk.ticket', 'read', [ticket_id],
       fields=['name', 'description', 'stage_id', 'tag_ids', 'partner_id', 'user_id', 'priority', 'create_date'])[0]
files = kw('ir.attachment', 'search_read',
           [['res_model', '=', 'helpdesk.ticket'], ['res_id', '=', ticket_id]],
           fields=['id', 'name', 'mimetype'])
```

Download an image with `GET /web/content/<attachment id>?download=true` in the same session, save it to a scratch folder and look at it. Read the requester's user and groups (`res.users` with `partner_id = t['partner_id']`) to know what they can see. `description` is HTML; strip tags before analysis.

## Internal note

```python
kw('helpdesk.ticket', 'message_post', [ticket_id],
   body='<p>Agent: classified as change request, priority Low ...</p>', body_is_html=True,
   message_type='comment', subtype_xmlid='mail.mt_note', partner_ids=[])
```

`mail.mt_note` is visible to internal users who can read the ticket and notifies nobody.

**HTML over JSON-RPC.** A string body arrives as a plain `str`, not a `Markup`, so `message_post(body='<p>…</p>')` stores it escaped and the reader sees raw tags (`<p>`, `<ol>`). Either pass `body_is_html=True` with HTML, as in these examples (Odoo logs a warning for internal users; harmless), or send plain text with no tags at all (its line breaks collapse, so keep it to one short paragraph). Never send tags without `body_is_html=True`. Escape any text quoted from the requester with `html.escape` before putting it into an HTML body.

## Message to the requester

```python
kw('helpdesk.ticket', 'message_post', [ticket_id],
   body='<p>Hello,</p><ol><li>…</li></ol><p>…</p>', body_is_html=True,
   message_type='comment', subtype_xmlid='mail.mt_comment', partner_ids=[requester_partner_id])
```

`mail.mt_comment` with `partner_ids` notifies exactly those partners and any followers subscribed to discussions. Check the followers before posting (`mail.followers` with `res_model='helpdesk.ticket'`); if anyone other than the requester and the support team follows, ask before posting. Whether the requester also gets an e-mail depends on their notification preference (`res.users.notification_type`: `inbox` keeps it inside Odoo). The site profile says which is expected; never send mail any other way.

## Stage change

```python
kw('helpdesk.ticket', 'write', [[ticket_id], {'stage_id': stages['In progress']}])
```

A stage with an e-mail, SMS or rating template sends it to the requester. Check `template_id`, `sms_template_id` and `rating_template_id` on the target `helpdesk.stage` before the first move; a stage with a template needs the profile's explicit consent. Odoo tracks the change in the chatter, so no extra note is needed for the move itself, only for the reason.

## After writing

Re-read the ticket and the message you just posted to confirm the write landed as intended (stage, subtype, recipients), then run the profile's guard checks.

```python
msg = kw('mail.message', 'read', [message_id], fields=['body', 'subtype_id', 'partner_ids'])[0]
assert '&lt;' not in msg['body'], 'body stored escaped: the reader sees raw tags'
```

`message_post` returns the new message's ID. If the body holds `&lt;`, the reader sees raw tags: post a corrected entry with `body_is_html=True`, and note on the ticket (internally) that the earlier entry was garbled.

## Fields not to touch without approval

Assignee, team, priority, tags, customer, SLA, and any record other than the ticket, unless the site profile allows it. Record the suggested priority in the classification note instead.
