# skills

Denzell's personal agent skills. Each folder is one skill with a `SKILL.md` and any supporting scripts or references. Skills are installed in both Claude Code (`~/.claude/skills/`) and Codex (`~/.codex/skills/`).

## Skills

| Skill | Purpose |
| --- | --- |
| make-skill | Create, edit, and sync a personal skill into both Claude Code and Codex |
| critique-poetry | Candid line-level poetry critique and revision advice |
| notebook-digest | OCR newly scanned notebooks, verify against raw scans, summarize, update the global timeline |
| ocr-scanner | Run the local journal-ocr PaddleOCR pipeline on CZUR scans and image folders |
| ship-nit-pr | Ship every small code nit as its own isolated GitHub pull request |
| poems-inbox | Transcribe voice notes emailed to the poems address, save to Poetry Studio, reply with a critique |
| personal-email | Send plaintext email from the personal Fastmail address |
| email-myself | Send a self-addressed email via SMTP from Codex |
| herdr | Run installs and long-lived dev servers in Herdr panes |
| instacart-cli | Drive the Instacart CLI |

## Install

```sh
git clone git@github.com:cdxker/skills.git
for s in skills/*/; do
  s=${s%/}
  ln -sfn "$PWD/$s" ~/.claude/skills/$(basename "$s")
  ln -sfn "$PWD/$s" ~/.codex/skills/$(basename "$s")
done
```

## Credentials

No secrets are committed. `personal-email` and `email-myself` read `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `SMTP_FROM` from the environment; `poems-inbox` expects `POETRY_STUDIO_API_KEY`.
