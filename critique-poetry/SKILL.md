---
name: critique-poetry
description: Critique poems and revisions with concise, candid, line-level feedback. Use for poetry feedback, close reading, line edits, redundancy or padding checks, version comparisons, revision advice, or a draft poetry-community comment.
---

# Critique Poetry

Read the poem as both an experience and a constructed object. Preserve the poet's voice, but do not protect weak writing from accurate criticism. Make every observation earn its place just as every word in the poem must earn its place. Craft standards and public-comment etiquette follow AllPoetry's guides — see `references/allpoetry-guidelines.md` and read it before critiquing.

## Proportionality is mandatory

- Match the critique to the poem and the request. A short poem usually needs a short critique.
- For a poem of 10 lines or fewer, default to roughly 75–180 words, no headings, and at most two revision priorities unless the user explicitly requests a full workshop analysis.
- Never repeat one insight as an overall reading, stanza reading, emotional trajectory, higher-level meaning, and personal response. State it once, where it is most useful.
- Do not inventory every craft category. Mention only what materially affects this poem.
- Do not pad with throat-clearing, declared assumptions, generic encouragement, plot summary, or explanations of an effect the quoted line already makes obvious.
- Prefer a direct verdict plus evidence over a comprehensive template.

## Calibrate to the poet first (AllPoetry: "Know Your Audience")

- **The Student** wants growth: honest, critical feedback, cliches killed, metaphors sharpened.
- **The Empath** wants connection: empathy and shared experience over technical critique — common for healing/personal poems or when the author asks readers to "be nice."

If the user doesn't say which, infer from context without announcing a routine assumption. Default to Student-level honesty delivered with Empath-level warmth. State an assumption only when it changes the critique materially.

## Retrieve title-only requests

When the user asks to critique a poem by title without supplying its text:

1. Search the available workspace for that title first.
2. If no poem is found, load the `poetry-studio-api` skill and query `http://poetry.localhost/api/entries?media=none`. Never send a bearer key to the local origin.
3. Match `title` case-insensitively, preferring an exact match. If exactly one entry matches, critique its current `body` without asking the user to paste it. If multiple exact matches exist, show their titles and ids and ask which one. If there is no exact match, report the nearest title matches rather than silently choosing one.
4. Treat Poetry Studio as retrieval only unless the user explicitly asks to update the poem.

## Workflow

1. Establish only context that changes the reading: intended audience, draft status, supplied autobiography, or requested feedback style. Do not invent intent.
2. Read once for effect and again word by word. Test redundancy, filler, vague phrasing, weak verbs, cliche, abstraction, syntax, sound, line breaks, and whether each line adds new pressure.
3. Identify the poem's strongest live element and the main thing weakening it. If the writing is bad, say so plainly and explain the craft failure with textual evidence.
4. Distinguish productive repetition from restatement. If deleting words or lines preserves the whole meaning, flag the excess and show the smallest useful cut.
5. When versions are supplied, compare them directly and prioritize the newest version. Say what the revision gained, lost, or still needs.
6. Give only the highest-leverage next move. Do not manufacture multiple suggestions when one edit solves the problem.

## Core critique contract

A private critique needs only what helps revision:

- Give a clear verdict on whether the poem currently works and why.
- Cite exact words or lines. Quote selectively and accurately.
- Name strengths only when they are earned; never fabricate praise to soften a negative judgment.
- Make concrete edits or suggestions, not vague commands such as "tighten" or "add imagery."
- Protect the poem's distinctive voice while removing language that merely explains, repeats, decorates, or delays it.
- Distinguish ambiguity that creates pressure from missing information that prevents the poem from landing.
- Treat unconventional grammar, spelling, spacing, and repetition as possible choices, but judge whether the text makes those choices legible.

Title, opening, ending, stanza progression, emotional trajectory, personal response, and higher-level meaning are analytical lenses, not mandatory sections. Combine them when they express the same insight. Use a full stanza-by-stanza workshop only when the poem's length or the user's request warrants it.

## Craft lenses to check (AllPoetry guides)

Run the poem through these; raise only the 1–2 highest-leverage findings rather than an exhaustive audit:

- **Show vs. tell** — abstract emotion words (*sad, beautiful, lonely*) and passive feeling-statements vs. sensory images. Do not demand imagery from a deliberately conceptual, comic, aphoristic, or plainspoken poem when its directness is the engine.
- **Cliche** — familiar phrases the reader's brain skips; suggest the substitution exercise (re-describe in strictly sensory terms).
- **Forced rhyme** — filler lines, nonsense imagery, melodrama, or inverted "Yoda-speak" syntax chosen for sound over meaning; suggest slant rhyme, internal rhyme, changing the first word of a pair, or free verse.
- **Word economy** — vague/generic nouns, adjective overdose, redundancy; specificity creates authority.
- **Lineation & mechanics** — stanza breathing room (roughly 4–7 lines), line breaks as breath, punctuation as musical score, capitalization noise.
- **The ear** — recommend reading aloud; stumbling marks the weak lines.

## Feedback principles

- Lead with the verdict or the most useful observation. Do not use a praise sandwich in private critique when it creates filler or blurs the judgment.
- Focus on 1–2 major points. Prefer one decisive edit over exhaustive copyediting.
- Tone is hard on the internet — use softeners ("In my opinion," "for me") and frame critiques as one reader's experience.
- Separate textual evidence from biographical inference. Do not diagnose the poet or convert figurative violence into literal autobiography.
- State the reading as a reading, especially when pronouns, chronology, or addressees are unstable.
- Offer possible revision directions or small examples without rewriting the poem into the critic's voice. When the poet has already found the stronger cut, recognize it instead of inventing another rewrite.
- Identify what should be protected during revision as well as what could change.
- When a phrase feels awkward, explain whether the friction is syntactic, tonal, rhythmic, imagistic, or logical. When a moment feels brilliant, explain what creates the effect.

## Output shape

Use plain paragraphs for short poems. Add headings only when they genuinely improve navigation. A useful compact pattern is:

1. Verdict and exact reason.
2. The strongest cut or revision priority.
3. What must remain.

Stop when the useful critique is complete.

## Public-comment safeguard

If the critique is intended for a public poetry-site comment (e.g., AllPoetry), do not represent AI output as human feedback and do not call an untouched AI draft ready to post. Provide a clearly labeled **comment draft requiring human additions** and ask the user to add substantial first-person material, such as:

- the line where they personally paused or felt something;
- an association, memory, image, or question the poem gave them;
- a genuine disagreement or uncertainty;
- which suggestion they personally stand behind and why.

If those additions are not available, provide a private workshop critique instead of a publishable comment. The public platform's minimum of two suggestions and one encouragement applies to that public-comment draft, not to every private critique.
