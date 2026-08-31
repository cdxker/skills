---
name: email-myself
description: Send private notes, drafts, summaries, files, or the current answer to the user's own inbox through the configured SMTP account. Use when the user says to email, mail, send, or forward something to themselves or to me@cdxker.com.
---

# Email Myself

Send mail with `scripts/send_self_email.py`. Treat `me@cdxker.com` as the fixed default recipient.

## Workflow

1. Resolve “this” from the immediate conversation. When it clearly means the latest answer or artifact, use that content without asking the user to repeat it. Ask only when multiple materially different items are plausible.
2. Choose a short, descriptive subject. Preserve useful headings, spacing, URLs, and file paths in a plain-text body.
3. Run the bundled script. Pass generated text through a single-quoted heredoc so the shell does not expand `$`, backticks, or command substitutions:

```bash
python3 /home/cdxker/.codex/skills/email-myself/scripts/send_self_email.py \
  --subject 'Descriptive subject' <<'EMAIL_BODY'
Body text goes here.
EMAIL_BODY
```

4. Report success only after the script exits successfully. On failure, report the concise error without printing configuration values or retrying blindly.

For existing content, prefer `--body-file /absolute/path`. Add files with repeatable `--attach /absolute/path`. Use `--dry-run` to validate configuration and message construction without sending.

## Configuration and safety

- Read `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `SMTP_FROM`, and `SMTP_SECURE` from the environment. Never write credentials into the skill, source files, command arguments, logs, or responses.
- Keep the recipient fixed at `me@cdxker.com`. Use a different workflow if the user explicitly asks to contact another person.
- Treat sending as an external action. A direct instruction such as “email this to me” authorizes one send of the resolved content; do not ask for redundant confirmation.
- Do not claim delivery beyond the SMTP server's accepted-send result.
- Do not send an empty body. Do not silently omit missing attachments.

