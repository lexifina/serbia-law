# Serbia: law history in git

The law of Serbia as a git history: one file per provision, one commit per version on the day it took effect, and the act that made each change as the commit's author. `git blame` names the act behind every article; `git log` lists every change to an article; picking a date gives the text in force that day.

It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law).

**What is in it now**

| Folder | Act | Versions | History |
| --- | --- | ---: | --- |
| `ustav/` | Устав Републике Србије (Constitution of the Republic of Serbia) | 2 | As promulgated (in force 8 November 2006), and with the Amendments I-XXIX (in force 9 February 2022); 29 articles changed |

The text is in Serbian (Cyrillic), the language of the official register. An English translation is not part of this record.

## A lawyer's questions as git commands

| Question | Command |
| --- | --- |
| What did Article 4 say on 1 January 2020? | `python tools/on.py 2020-01-01 ustav clan-004` |
| Which act wrote each paragraph of Article 4? | `git blame ustav/clan-004.md` |
| Every change to Article 4 | `git log -p --word-diff ustav/clan-004.md` |
| Every version in the record, in order | `git log --reverse --format="%ad %an" --date=short main` |

## Dates

Each commit is dated at noon, Europe/Belgrade, on the day the version took effect, as the register's version timeline gives it (2006-11-08 and 2022-02-09). The first commit is "oldest version available", credited to the publisher, as the text of the Constitution of 2006.

## How it is checked

- Both versions are the register's own text for the version, and the register's version timeline lists exactly these two versions. The latest version is the register's current text, the "editorially cleaned" consolidation including Amendments I-XXIX.
- Every article of the register's text is in the record apart from the omissions below; the 29 articles that differ between the two versions are the ones credited to the Amendments.
- Every version is read back from git on the day it took effect and on the day before; both must match the corpus. Results are in `REPRODUCE.md`.
- No merge commits, no commit dated backwards or in the future, and every commit's trailers parse.

## What it does not show

- **Article captions and the headings of parts and sections** (for example "Носиоци суверености", "ПРВИ ДЕО") are not in the files. The register prints them between articles; this build does not keep them.
- **The 2006 Constitution's earlier history.** Serbia's earlier constitutions (1990 and before) are not here.
- **Other acts.** The Criminal Code and other laws are not yet in the record.
- **The amendment notes** that the register prints under changed articles are not law text and are not in the files.

## Sources

| Source | Kind | Past versions | Notes |
| --- | --- | --- | --- |
| [Pravno-informacioni sistem Republike Srbije](https://pravno-informacioni-sistem.rs) | Official register (Службени гласник) | yes, a version timeline per act | Used: the text of both versions and their dates |

## Licence

See `LICENSE`. This repository is not legal advice and not an official publication. No AI model wrote or changed legal text; scripts were written by an AI model (see `REPRODUCE.md`).

## На српском

Историја закона Србије у гиту: једна датотека по члану, једна ревизија по верзији на дан ступања на снагу. Тренутно садржи Устав Републике Србије у две верзије: проглашен 2006. (на снази од 8. новембра 2006) и са Амандманима I-XXIX (од 9. фебруара 2022). Текст је из Правно-информационог система Републике Србије. Наслови чланова и делова нису укључени.
