export const meta = {
  name: 'fall-2024-notebook-page-ocr-read',
  description: 'One agent per scanned notebook page: verify OCR against the raw scan, then merge per book and synthesize a straight timeline',
  phases: [
    { title: 'List pages', detail: 'enumerate scan images per notebook folder', model: 'sonnet' },
    { title: 'Read pages', detail: 'one sonnet agent per page: raw scan + OCR sidecar -> structured page record', model: 'sonnet' },
    { title: 'Merge books', detail: 'one sonnet agent per notebook merges its page records into a book summary + dated timeline', model: 'sonnet' },
    { title: 'Synthesize', detail: 'merge all books into the series report with a straight interleaved timeline' },
  ],
}

const BOOKS = args.books

const LIST_SCHEMA = {
  type: 'object', required: ['images'],
  properties: { images: { type: 'array', items: { type: 'string' } } },
}

const PAGE_SCHEMA = {
  type: 'object',
  required: ['image', 'dates', 'gist', 'key_quotes', 'names', 'money', 'safety_flags', 'kind', 'ocr_quality'],
  properties: {
    image: { type: 'string' },
    dates: { type: 'array', items: { type: 'string' }, description: 'dates visible on the page, as written (e.g. "8/21", "Nov 5"), plus resolved guess like 2024-08-21 when justified' },
    gist: { type: 'string', description: '2-6 sentences: what is on this page, concretely' },
    key_quotes: {
      type: 'array',
      items: { type: 'object', required: ['quote', 'verified'], properties: { quote: { type: 'string' }, verified: { type: 'boolean', description: 'true only if you read it off the raw scan yourself' } } },
      description: '0-5 load-bearing lines, spelling preserved exactly',
    },
    names: { type: 'array', items: { type: 'string' }, description: 'person names exactly as written on the page' },
    money: { type: 'array', items: { type: 'string' }, description: 'dollar/tribute amounts as written, verified against the raw scan' },
    safety_flags: { type: 'string', description: 'suicidal/self-harm/crisis language on this page, factually, or "none"' },
    kind: { type: 'string', description: 'diary | ledger/tracker | letter | fiction/fantasy | poem/lyrics | list/index | cover/blank | mixed' },
    ocr_quality: { type: 'string', description: 'one short phrase' },
  },
}

const BOOK_SCHEMA = {
  type: 'object',
  required: ['folder', 'book_summary', 'timeline', 'verified_passages', 'ocr_quality', 'safety_review'],
  properties: {
    folder: { type: 'string' },
    book_summary: { type: 'string', description: '1-3 dense paragraphs in the style described in the prompt' },
    timeline: {
      type: 'array',
      items: {
        type: 'object', required: ['date', 'entry'],
        properties: {
          date: { type: 'string' }, entry: { type: 'string' },
          source_image: { type: 'string' }, verified_against_raw: { type: 'boolean' },
        },
      },
    },
    verified_passages: {
      type: 'array',
      items: { type: 'object', required: ['quote', 'image'], properties: { quote: { type: 'string' }, image: { type: 'string' } } },
      description: '4-8 load-bearing raw-scan-verified quotations',
    },
    ocr_quality: { type: 'string' },
    safety_review: { type: 'string' },
  },
}

const RULES = `RULES that apply to everything you write:
- Preserve original spellings in quotes exactly, including misspellings. Never silently correct OCR or source spelling.
- Keep person names distinct exactly as written (Pani/Rani/Goddess Devi, Aurelia, Anna, Kaisa, Edith, Luna, Fede, Nick, Dens, Ricky...); never merge people without in-text evidence.
- Separate documented events from fantasy/fiction/letters; label fiction as fiction.
- Report safety-relevant passages (suicidal language, self-harm, crisis) factually with image refs; do not interpret, diagnose, or omit them.
- OCR of this handwriting is error-prone: the raw scan governs; anything not checked against the scan stays hedged.`

const bookResults = await pipeline(
  BOOKS,
  // Stage 1: enumerate this book's pages
  b => agent(
    `List the scan image files (jpg/jpeg/png/webp/tif, top level only, NOT inside ocr/) in the folder "${b.path}". Return them sorted by filename. Do not modify anything.`,
    { label: `list:${b.short}`, phase: 'List pages', model: 'sonnet', effort: 'low', schema: LIST_SCHEMA },
  ),
  // Stage 2: one agent per page
  (listed, b) => parallel(listed.images.map(img => () => {
    const stem = img.replace(/\.[^.]+$/, '')
    return agent(`
You are reading ONE page of Denzell's private handwritten 2024 pocket notebook "${b.label}".

Raw scan (authoritative): ${b.path}/${img}
Machine OCR sidecar (error-prone search aid): ${b.path}/ocr/${stem}.md

Do exactly this:
1. Read the OCR sidecar.
2. Read the raw scan image with the Read tool and check the OCR against the actual handwriting. The image may be a two-page spread.
3. Return the structured page record. Mark quotes verified=true only for text you read off the scan yourself. Verify every dollar amount and every date against the scan. Be concise — the gist is 2-6 sentences, not a transcript.

Context: these notebooks are minute-by-minute timestamped captain's logs mixing Trieve startup work (Nick, Mintlify as a customer, Qdrant, Kubernetes, outages), mediated findom/chastity relationships, substances, family, the Svartpilen 401 motorcycle, friends, church/faith, poems, and money.

${RULES}

Do not modify, rename, or delete any file. image field = "${img}".
`, { label: `page:${b.short}:${stem.slice(-12)}`, phase: 'Read pages', model: 'sonnet', schema: PAGE_SCHEMA })
  })),
  // Stage 3: merge this book's page records
  (pages, b) => {
    const good = (pages || []).filter(Boolean)
    log(`${b.short}: ${good.length} page records, merging`)
    return agent(`
You are merging per-page readings of Denzell's handwritten notebook "${b.label}" (folder: ${b.path}) into one book record. Each page was read by an agent that checked the machine OCR against the raw scan. Page records, in page order:

${JSON.stringify(good)}

Produce:
- book_summary: 1-3 dense paragraphs in the voice of a careful archival report (see rules), covering the book's span, its dominant threads (work, relationships, money, substances, family, faith, writing), and how it connects into the notebook series.
- timeline: chronological dated entries for the whole book, one per dated day or notable moment. Resolve page-local dates ("8/21") to full dates using the book's labeled range, keeping uncertainty explicit ("2024-09-xx"). Carry source_image and verified_against_raw through from the page records.
- verified_passages: pick the 4-8 most load-bearing quotes that page agents marked verified=true, with their image filenames.
- safety_review: aggregate every safety flag from the pages, factually, with dates and image refs; or "none found".

${RULES}

folder field = "${b.path}". Your final output is the structured object only.
`, { label: `merge:${b.short}`, phase: 'Merge books', model: 'sonnet', schema: BOOK_SCHEMA })
  },
)

const books = bookResults.filter(Boolean)
log(`${books.length}/${BOOKS.length} books merged`)

phase('Synthesize')
const synthesis = await agent(`
You are synthesizing per-notebook readings of Denzell's newly scanned fall 2024 pocket notebooks into ONE series report file. Write the file to:

  /home/cdxker/CZURImages/Field-Notes-2024-fall-series-summary.md

FORMAT: mirror the existing report /home/cdxker/CZURImages/Field-Notes-2024-series-summary.md — read it first to copy its exact structure and voice: an H1 title, a bold date-range line, the blockquote source warning ("OCR is error-prone and is a search aid only. Raw scans govern."), an intro naming the books, a "## Series-Level Reading" section, then one "## Book N: <label>" section per book each ending with a "### Verified Passages" list of quotes with image filenames.

ADDITION, per the user's request: after Series-Level Reading, include a "## Straight Timeline" section — one merged chronological timeline (July 22 through December 26, 2024) interleaving ALL books' dated entries, showing everything that was happening at once: startup work, relationships, money, substances, family, motorcycle, faith, writing. One line or short paragraph per date, book-attributed where useful. Note coverage gaps explicitly (e.g. Sep 19-21, Oct 31-Nov 13; the separate "Main" book covers Nov 1-12). Entries from the "April 10 2024 - July 21 2024" Joshua Tree companion ledger fall before this range — summarize what its newly OCR'd pages add in its own book section rather than forcing them into the fall timeline.

CONTEXT to read before writing: /home/cdxker/GLOBAL_TIMELINE.md (especially the Apr 10-Jul 21 2024 section and the Externally section — these new books bridge into the Externally era, Sep 2024-Feb 2025, and overlap the Oct 2024 creator-spend peak) and /home/cdxker/CZURImages/Field-Notes-2024-series-summary.md in full for voice and spring-2024 context.

${RULES}

Per-book structured readings (JSON):

${JSON.stringify(books, null, 1).slice(0, 350000)}

Write the complete file, then return a compact plain-text digest: the series-level reading (2-3 paragraphs), the 15 most important timeline moments, any safety-relevant findings, and notable OCR-quality caveats. Your returned text is data for the orchestrator, not a user-facing message.
`, { label: 'synthesize', phase: 'Synthesize' })

return { books_merged: books.length, digest: synthesis }
