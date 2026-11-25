# keepassxc-agent-secrets: evaluation record

## 2026-11-25, baseline from a real collaboration

- Source: one owner and many Claude Code and Codex sessions sharing one KeePassXC database on Windows, November 2026. The procedure had been scattered over a project page and agents' memory notes.
- Failures the skill now targets, each seen at least once: an agent said a test account didn't exist after one lookup (it was in the database under another title); an agent-made login was left without a stored password, so the owner couldn't sign in; a read-back timed out and a second `set-login` would have made a duplicate entry; an adapter pin was pointed at the owner's personal entry, so scripts wrote under the owner's name; an entry with an empty URL crashed KeePassXC 2.8.0 on the access dialog; an agent told the owner secrets must never be in the cloud drive when the database already lived there.
- Checked: every rule matches the adapter's real behaviour (exact UUID/path selectors, create-only `set-login`, error codes `locked`, `no_matching_entry`, `entry_mismatch`) and the live backup settings (backup before save, a scheduled verified copy).
- Not yet measured: a fresh agent given only the hand-off block, asked to create and later rotate a staging login. Record that run here with the outcome.
