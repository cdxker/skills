---
name: poems-inbox
description: Handle audio emailed to poemes@cdxker.com (or any voice note Denzell says to "add to poems"): transcribe it, save the text as a Poetry Studio poem, upload the audio to the Recordings library, reply with the transcript and a critique. Trigger on mail To poemes@cdxker.com or poem@cdxker.com, "add to poems", "add this to poems", "save this voice note as a poem", or an m4a/mp3/webm voice memo about a poem.
---

# Poems inbox

Every audio attachment on a mail to poemes@cdxker.com or poem@cdxker.com is a poem drop. Do all
of the steps below for each audio file, without asking. Mail to this address
never needs the words "add to poems" to count; the address is the instruction.

## 1. Transcribe

Use faster-whisper with the `small` model at minimum; `base` garbles names and
line ends:

```sh
uv run --with faster-whisper python3 -c "
from faster_whisper import WhisperModel
segs,_=WhisperModel('small').transcribe('FILE', beam_size=5)
for s in segs: print(s.text.strip())"
```

Keep the transcript honest. Fix obvious homophones, keep every "like", swear
and hesitation that carries voice, and never invent lines. Where a name or
word is unclear, pick the likeliest and say so in the entry `note`.

## 2. Save the poem to Poetry Studio

Load the `poetry-studio-api` skill and follow its preflight exactly. Facts
that skill will not tell you:

- The email-agent process does not inherit `POETRY_STUDIO_API_KEY`. It is
  exported in `~/.zshrc`; run the request inside
  `zsh -c 'source ~/.zshrc >/dev/null 2>&1; ...'` with `set +x`, never
  print the key.
- Poems are root-level entries: `POST /api/entries` with `title`, `body`,
  `note`, no `parent_id`. Lines separated by `\n`, stanzas by a blank line.
- Title: the strongest short phrase from the recording, not the filename.
- Always set `slug` too: a kebab-case form of the title, unique per account
  (`^[a-z0-9][a-z0-9-]{0,99}$`). The Lines wall only shows root writing that
  has a slug or children; a slugless entry is filed but invisible on the site.
  Denzell wants every poems@ drop on the site, poem or not (Aug 30, 2026).
- `note`: source file name, duration, mail date and subject, transcription
  model, and any uncertain words.
- Also upload the audio: convert to mp3 first
  (`ffmpeg -i in.m4a -codec:a libmp3lame -q:a 4 out.mp3`), then
  `POST /api/media/upload/recording?title=...` with
  `Content-Type: audio/mpeg` and the raw file as body. m4a is rejected.
- Report both entry ids in the reply.

Local dev at http://poetry.localhost also requires auth now; production
`https://api.poetry.cdxker.com` is the canonical store. Do not write to
`~/work/cdxker/poems` (a Mintlify experiment) unless asked.

## 3. Reply

Plaintext, per the email-agent rules. Include, in this order:

1. The full transcript, formatted as saved.
2. A critique following the `critique-poetry` skill: short, verdict first,
   one or two line-level moves, what to keep. Treat a raw spoken note as a
   draft, not a finished poem; say what the poem inside it is.
3. Where it was saved: entry id, recording id.

Do not add the audio's content to GLOBAL_TIMELINE.md or diagnose Denzell
from it; it is writing material.
