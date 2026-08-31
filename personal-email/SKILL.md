---
name: personal-email
description: Send email from Denzell's personal address (me@cdxker.com, Fastmail) as plaintext. Use whenever the user says "email me" or asks to send results/summaries/reports by email.
---

# Send email

Send **plaintext only** — never HTML, never markdown formatting intended for rendering. Denzell reads raw text.

## How

1. Write the email body to a file (use `$CLAUDE_JOB_DIR/tmp/` or `/tmp/`). Plain prose; section dividers are hyphen lines like `-----`.
2. Send it:

```bash
python3 ~/.claude/skills/personal-email/send_email.py "Subject line" /path/to/body.txt [recipient]
```

- Default recipient is `me@cdxker.com` — Denzell's personal address; prefer this unless he says otherwise. He has also used `denzell@mintlify.com` for work.
- **Always CC `me@cdxker.com`.** The script adds the CC automatically whenever the recipient is a different address; never send from this skill without that CC. Denzell asked for this on 2026-08-28.
- Credentials come from the `SMTP_HOST` / `SMTP_PORT` / `SMTP_USER` / `SMTP_PASSWORD` / `SMTP_FROM` env vars — Fastmail, already set in his environment. From address is `me@cdxker.com`, so self-sent mail may land in Sent/self folders rather than inbox.

## Style — hard rules for Denzell's email reader

His reader chokes on certain characters. These are constraints on the body and subject, not suggestions:

- **Never use equal-sign divider lines** — no `=====` rows anywhere. Use hyphen divider lines (`-----`, any length) for section separation.
- **No parentheses in email bodies or subjects.** Set asides off with hyphens instead: write `the ledger book - trackers, budgets, letters - covers spring` rather than a parenthetical. Exception: verbatim quotations from source material keep their original parentheses.
- Plaintext, `text/plain`, single part with no HTML alternative — the script enforces this. It also normalizes unicode punctuation — em dashes, curly quotes — to ASCII so the message goes out 7bit instead of base64, which keeps it copy/paste-safe.
- For multi-part reports, use clearly separated sections with hyphen divider lines and numbered headings.
- Long content is fine; put the full deliverable in the email rather than only pointing at files.
