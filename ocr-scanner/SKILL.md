---
name: ocr-scanner
description: OCR Denzell's CZUR scans, journals, notebooks, photographed pages, or image folders with the local journal-ocr PaddleOCR pipeline. Use whenever Denzell asks to OCR, transcribe, index, search, batch-process, or make scans searchable, mentions CZUR OCR or journal OCR, or asks to resume or validate an OCR run.
---

# OCR Scanner

Use the canonical local implementation at:

`/home/cdxker/work/cdxker/journal-ocr`

Read its `README.md` before operating it. The CLI is `journal-ocr`, implemented
in `journal_ocr.py`, with exact dependencies recorded in `uv.lock`.

## Hard Rules

- Never alter, rename, recompress, rotate, crop, overwrite, or delete source
  scans while OCRing them. The pipeline may only create or update the derived
  `ocr/` directory inside each supplied scan folder.
- Treat OCR as a searchable aid, never as authoritative text. Denzell's
  handwriting is difficult for machine OCR. Raw scans govern every quotation,
  date, identity, safety passage, and consequential interpretation.
- Keep processing local. This pipeline sends no journal images to an API.
- Do not silently correct OCR or source spellings. Put manual corrections in a
  separate reviewed transcript when requested.
- Run dependency installation or `uv sync` in a Herdr pane in the repository,
  never in the agent execution terminal. Use a dedicated Herdr pane for long
  multi-folder OCR runs so progress remains visible.

## Setup

The known-good stack is Python 3.12, PaddleOCR 3.7.0, PaddlePaddle 3.2.0, and
OpenCV 4.10.0.84. The repository's `pyproject.toml` and `uv.lock` pin it.

If `/home/cdxker/work/cdxker/journal-ocr/.venv` does not exist or `uv sync
--check` indicates the environment is stale, run `uv sync` in a Herdr pane.
Paddle models are cached under `~/.paddlex/official_models/`; reuse the cache.

## Run OCR

Inspect the requested folders first. Confirm that:

- they contain the intended top-level image files;
- separate physical books have already been split into separate folders;
- filename sorting reflects page order;
- an existing `ocr/` directory is derived output rather than source material.

From `/home/cdxker/work/cdxker/journal-ocr`, run:

```bash
uv run journal-ocr --workers 2 --cpu-threads 10 "/absolute/scan/folder"
```

Supply multiple quoted absolute folders in one command when appropriate. Use
`--resume` by default if any requested folder already has structured `.json`
sidecars, unless Denzell explicitly wants a clean rerun.

The pipeline recognizes JPEG, PNG, WebP, TIFF, and TIF images. It sorts images
by filename and automatically splits images whose width-to-height ratio is at
least 1.2 into left and right pages.

## Validate Every Run

For each folder, verify all of the following before reporting success:

- source image count equals plain-text sidecar count;
- source image count equals same-stem Markdown sidecar count, excluding
  `combined.md`;
- source image count equals structured JSON sidecar count, excluding
  `manifest.json`;
- `manifest.json.image_count` equals the source image count;
- `combined.md` has one `##` image heading per source image;
- every JSON record's `source` names its image and `line_count` matches its
  contained lines;
- every bounding box remains within the original image dimensions;
- the command reported no failed images.

Open representative outputs, including at least one first page, one middle
page, one last page, and one detected spread. Compare them with the raw scans
to characterize quality honestly.

## Outputs

Each processed folder receives:

- `ocr/<image-stem>.txt` for quick search;
- `ocr/<image-stem>.md` for a linked Markdown transcription beside the other
  derived files;
- `ocr/<image-stem>.json` for text, confidence, sections, and boxes;
- `ocr/combined.md` for a linked folder transcript;
- `ocr/manifest.json` for counts and engine versions.

When reporting completion, state the folders processed, image and detected-line
counts, whether any spreads were split, and that machine handwriting OCR is
error-prone. Point to the original images for verification.
