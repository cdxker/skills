---
name: make-skill
description: Create, edit, fix, extend, rename, or synchronize a personal skill and ALWAYS install it in both Claude Code (~/.claude/skills/) and Codex (~/.codex/skills/). ALWAYS invoke this skill whenever Denzell asks to make, create, add, save, update, change, modify, improve, or otherwise work on a skill or SKILL.md—including casual wording, misspellings, requests to change a skill description or trigger behavior, and phrases such as "make a skill", "save this as a skill", "turn this into a skill", or "make sure this skill triggers".
---

# Make a skill (Claude Code + Codex, always both)

Denzell runs two agent harnesses. Every personal skill lives in **both**:

- Claude Code: `~/.claude/skills/<name>/SKILL.md`
- Codex: `~/.codex/skills/<name>/SKILL.md`

Never write to only one. This applies to edits too — after changing a skill
in either location, copy it to the other so they stay byte-identical.

## Format

One directory per skill, containing `SKILL.md` with YAML frontmatter:

```markdown
---
name: <kebab-case-slug, matches the directory name>
description: <what it does + explicit trigger phrases/conditions, one line>
---

# Title

Instructions written TO the agent (imperative), not about it.
```

- The `description` is what the harness uses to decide when to load the
  skill — pack it with trigger words the user would actually say.
- Supporting files (scripts, references) go in the same directory; refer to
  them by `~/.claude/skills/<name>/...` paths. Copy those to Codex too.
- Keep it self-contained: an agent with no other context should be able to
  follow it. Encode hard rules ("never X") explicitly — skills are
  constitutions, not suggestions.

## Procedure

1. Draft the skill content once.
2. `Write` it to `~/.claude/skills/<name>/SKILL.md`.
3. `mkdir -p ~/.codex/skills/<name>` and copy the file there.
4. Verify both copies exist and are identical (`diff`).
5. If the skill stores non-obvious facts worth remembering, add a one-line
   pointer to the memory index as usual.

## Existing conventions to respect

- Email: plaintext only (see `personal-email`).
- Long-lived/dev-server and install commands run in Herdr panes, never in
  the agent terminal, except Poetry Studio's persistent local server, which
  uses the enabled `poetry-dev.service` systemd user unit and never Herdr.
- Short paragraphs and small chunks in anything Denzell reads directly.
