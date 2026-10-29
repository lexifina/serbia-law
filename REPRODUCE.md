# How this repository was made (Serbia)

This file is written by the build on 2026-10-29, the day the source data was retrieved.

## Sources

| Source | Address | Retrieved | Licence |
| --- | --- | --- | --- |
| Pravno-informacioni sistem RS, register API (reg.pravno-informacioni-sistem.rs/api) | <https://pravno-informacioni-sistem.rs> | 2026-10-29 | Free public official register |

Every word of law in this repository comes from these sources. Lexifina reads them and records each act's dated versions, and the laws that made each change, in one corpus file. This repository is built from that file.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `ustav` | Устав Републике Србије | 2 | 2006-11-08 to 2022-02-09 |

The build made 2 commits:

| Commits | Kind |
| ---: | --- |
| 1 | first version of an act |
| 1 | one law on its in-force day |
| 0 | changes no amendment note explains, credited to the publisher |

Other counts:
- 0 commits on the branch `buduci`: laws not yet in force on 2026-10-29.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 2 laws in the record.
- 4 tags.

## Dates

Each commit is dated at noon (Europe/Belgrade) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: Устав чл. 196: закон ступа на снагу најраније осмог дана од дана објављивања; Устав и акт о промени Устава ступају на снагу проглашењем (чл. 203) https://pravno-informacioni-sistem.rs/eli/rep/sgrs/skupstina/ustav/2006/98/1/reg

## How the history is built

`tools/build.py` turns the corpus into this history in one pass: one commit per law, on the day it took effect. The same corpus always gives the same commit hashes. `tools/check_repo.py` reads every version back from git and compares it with the corpus. `tools/on.py` shows the law as it stood on any date. The corpus format is described in `tools/SCHEMA.md`.

- Corpus: sha256 `c4f6af9b2f2cbf74f995e0e3f81b186c7aa0be50e8d7af5dd35261ae18e3a77f` (401609 bytes).
- Builder blob hashes (`git hash-object`): `build.py` `a4faa25af85facb64b956b372f6b528aafdd7ec1`, `check.py` `3e59cb6f05eccb94a9ec14431a7f6781221e83ef`, `on.py` `644a6c0857fbcc72562032b58d57aa113fee0641`.
- Python 3.12.10; git version 2.46.0.windows.1.

## Checks

Not yet run for this build.

No second build of this corpus has been compared yet.

## Decisions made by hand

- Version dates come from the register's ELI metadata: 2006 text in force 2006-11-08 (proclamation, Art. 206); amended text version_date 2022-02-09 (Act on amendment proclaimed, SG 16/2022).
- Changes in 2022 are credited to Amendments I-XXIX; the register's per-article notes name SG 115/2021 (Amandman N).
- Article captions and part headings are dropped from article files in this first cut (unverified heuristic: trailing lines without final punctuation).

## What AI did and did not do

The scripts that read the sources and build this repository were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- Claude Code (claude-opus-5-5) wrote fetch/parse code; no model wrote or altered legal text.
