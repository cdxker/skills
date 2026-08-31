---
name: notebook-digest
description: Full pipeline for newly scanned notebooks/journals — OCR new CZURImages scan folders, ultracode page-per-agent read and raw-scan verification, series summary with a straight merged timeline, plaintext email, and GLOBAL_TIMELINE.md update. Use when Denzell says he added/scanned more notebooks or journals and wants them OCR'd and summarized, asks for a "straight timeline" over a scan range, asks to "digest" new scans, or invokes the Art OCR / ultracode OCR workflow.
---

# Notebook digest — scan folders to emailed timeline

Run the whole chain for newly scanned notebook folders: machine OCR, page-level
agent reading verified against raw scans, a series report in the established
format, an email, and a timeline update. This wraps the `ocr-scanner` skill;
load that skill too and obey its hard rules (never modify source scans; OCR is
a search aid only; raw scans govern every quote, date, name, amount, and
safety passage).

## 1. Find the target folders

New scans live under `/home/cdxker/CZURImages/<date-range label>/`. Identify
folders the user means by: recent image mtimes, missing or incomplete `ocr/`
directories (compare top-level image count to `ocr/*.json` count excluding
`manifest.json`), and what `GLOBAL_TIMELINE.md` says was already processed.
Confirm scope in one sentence if genuinely ambiguous; otherwise proceed.
Folder labels are organizational; page dates govern.

## 2. Machine OCR — in a Herdr pane, never the agent terminal

One process for all folders, from `/home/cdxker/work/cdxker/journal-ocr`:

```
herdr tab create --workspace <current ws> --cwd /home/cdxker/work/cdxker/journal-ocr --label "OCR run" --no-focus
herdr pane run <pane-id> "export PATH=$HOME/.local/bin:$PATH; uv run journal-ocr --workers 2 --cpu-threads 10 --resume '<abs folder>' ...; echo OCR_RUN_EXIT=\$?"
```

`uv` is NOT on the pane's default PATH — always export PATH first. Use
`--resume` whenever any folder already has JSON sidecars. Do not run one OCR
process per folder; the CLI takes many folders and agents would thrash the CPU.

Monitor by process, not by scrollback text (old `OCR_RUN_EXIT` lines from
failed attempts linger in the pane and cause false matches):
poll `herdr pane process-info --pane <id>` until `journal-ocr` disappears,
then read the pane tail for `OCR_RUN_EXIT=0`.

## 3. Validate before any agent reads

For every folder, from the main terminal: image count == txt == md (minus
combined.md) == json (minus manifest.json) == manifest `image_count` ==
`## ` headings in combined.md. Zero failed images. Fix or rerun before
continuing.

## 4. Ultracode workflow — one agent per PAGE, never per book

Per-book agents context-rot and serialize; the required shape is:

1. **List pages** — one cheap agent per folder (sonnet, effort low) returns
   sorted image filenames.
2. **Read pages** — one sonnet agent per page: read `ocr/<stem>.md`, then the
   raw scan with Read, verify against the handwriting, return a compact
   structured record: image, dates as written plus resolved guess, 2–6
   sentence gist, 0–5 key quotes each flagged `verified` only if read off the
   scan, names exactly as written, money amounts scan-verified, safety flags,
   page kind (diary/ledger/letter/fiction/poem/list/cover), ocr quality.
3. **Merge books** — one sonnet agent per folder merges its page records into
   a book summary, dated timeline (resolve page-local dates using the label
   range, keep uncertainty explicit like "2024-09-xx"), 4–8 verified
   passages with image filenames, aggregated safety review.
4. **Synthesize** — default-model agent reads `GLOBAL_TIMELINE.md` and the
   nearest existing series summary for voice, then writes the report.

Use `pipeline()` over books so each book merges as its pages finish. A proven
working script lives beside this skill:
`~/.claude/skills/notebook-digest/page-per-agent.workflow.js` — copy it to the
session scratchpad, adjust the synthesis prompt's output path and date range,
and launch with `Workflow({scriptPath, args: {books: [{path, label, short}]}})`.

Rules baked into every agent prompt:
- Preserve original spellings exactly, including misspellings; never silently
  correct OCR or source spelling.
- Keep person names distinct exactly as written (Pani/Rani/Goddess Devi,
  Aurelia, Anna, Kaisa, Edith, Luna, Violette, ...); never merge people
  without in-text evidence.
- Separate documented events from fantasy/fiction/letters; label fiction.
- Report safety-relevant passages factually with date + image ref; never
  interpret, diagnose, or omit. No inference of current intent.
- Verify every dollar amount and date against the raw scan.

## 5. The report

Write `CZURImages/<series-name>-summary.md` mirroring
`CZURImages/Field-Notes-2024-series-summary.md` exactly: H1 title, bold date
range, the blockquote source warning ("OCR is error-prone and is a search aid
only. Raw scans govern."), intro naming the books, `## Series-Level Reading`,
`## Straight Timeline` (one merged chronological line-per-date interleaving
all books, book-attributed in brackets, coverage gaps stated explicitly),
one `## Book N:` section per book ending in `### Verified Passages` with
image filenames, then a safety review and source cautions section.

## 6. Email

Load `personal-email` and send the summary to me@cdxker.com: series reading,
~15 key timeline moments, safety review, OCR caveats, report path, validation
stats. Plaintext, hyphen dividers, no parentheses outside verbatim quotes.

## 7. Update GLOBAL_TIMELINE.md

Add (a) a dated bullet in "Current decision window" recording what was
scanned, OCR'd, validated, and where the report lives, and (b) a new
`### <range>` section in the long-term chronology with the key findings,
safety review, and the verified/OCR-derived distinction. Convert relative
dates to absolute. New names get an explicit do-not-merge note.
