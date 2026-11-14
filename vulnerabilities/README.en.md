# Vulnerabilities in Serbian law

[Srpski](README.md) · **English**

The vulnerability detectors from [lexifina/global-law](https://github.com/lexifina/global-law/tree/main/vulnerabilities) look for mechanical mistakes in legislation: a rule applying "until" a date that has passed, a provision repealed before its replacement took effect, two amendments to the same provision on the same day, a rule in force before it was published. global-law's published list (9 November 2026) did not include Serbia yet, so this is a run over this repository only, as it stood at commit [`542a099`](https://github.com/lexifina/serbia-law/commit/542a099cd5a137d6bd315b1596b033ce44dcd54e) on 14 November 2026.

**In short:** the detectors raised 3,154 flags. A language model reviewed 194 of the strongest, arguing each one for and against; 17 survived. Checked by hand in this repository, none of them is a confirmed defect in Serbian law. Eight come from how the register dates versions or how this repository was built, five are lawful, one is a spent transitional rule, and three are not law at all. Four dates stay open until they are checked against the Службени гласник.

A flag is a prompt to look, not legal advice, and nothing here has been tested in court.

## Flags by category

| Category | What it looks for | Flags | In law texts | Reviewed | Survived review |
| --- | --- | ---: | ---: | ---: | ---: |
| Lapsed time limits | Text still applying a rule "until" a date that has passed | 2,151 | 424 | 76 | 5 |
| Repeal gaps | A provision removed before its replacement took effect | 38 | 38 | 38 | 4 |
| Same-day conflicts | Two laws changing the same provision on the same day | 145 | 145 | 40 | 4 |
| Retroactive or pre-publication dates | A rule in force before it was made or published | 339 | 339 | 40 | 4 |
| Duplicate numbering | Two units with the same number in one provision | 400 | 209 | 0 | 0 |
| Dead currencies | Amounts in currencies no longer in use | 67 | 26 | 0 | 0 |
| Publisher notes | Notes that an amendment could not be carried out | 14 | 6 | 0 | 0 |

"In law texts" counts laws, by-laws, decisions and treaties. The other flags are in drafts, bills, court decisions and reports, which this repository also holds and labels as not law.

## The 17 cases that survived the review

### Open: check the date against the Gazette (4)

| Act | What the record says | Why it is probably a data error |
| --- | --- | --- |
| [Одлука о условима које треба да испуни организација удруженог рада која врши дезинфекцију, дезинсекцију и дератизацију](https://github.com/lexifina/serbia-law/commit/24f267b15abe645fa7cf1608710a34d1b4d0f28d) („Службени гласник СРС” 23/1979) | in force 17 June 1971, published 9 June 1979 | The decision rests on a 1977 law, so it cannot have applied from 1971. The date is the register's. |
| [Одлука о оснивању Геронтолошког центра у Вршцу](https://github.com/lexifina/serbia-law/commit/c8d81385c52c6853457e768f08ca48382fda8c02) („Службени гласник РС” 50/1999) | in force 3 December 1992, published 25 November 1999 | The date may belong to an earlier founding act that the 1999 text restates. |
| [Правилник о безбедности машина](https://github.com/lexifina/serbia-law/commit/57306156d7f951d8c63f80fe625413132a584718), as amended by „Службени гласник РС” 21/2020 | version in force 1 September 2016, amendment published 6 March 2020 | The register dates the consolidated version from the rulebook's own start, not from the amendment. |
| [Уредба о начину и поступку извршавања војне, радне и материјалне обавезе](https://github.com/lexifina/serbia-law/commit/187e6a51b8a8ae31b16cb9ab324468a1a59a72ac), as amended by „Службени гласник РС” 40/2019 | version in force 15 June 2016, amendment published 7 June 2019 | The same pattern as the rulebook above. |

### Explained by how this repository was built (4)

| Provision | What the record says | What happened |
| --- | --- | --- |
| [Закон о буџету Републике Србије за 2020. годину, члан 3.](https://github.com/lexifina/serbia-law/blob/542a099cd5a137d6bd315b1596b033ce44dcd54e/zakon/2019/84-3/clan-003.md) | no text for 203 days (24 April to 13 November 2020) | The article is a table of state guarantees, which the register shows as an image in the 60/2020 version, so the build dropped it. The article was not repealed. |
| [Закон о основном образовању и васпитању, чл. 97, 98 и 99](https://github.com/lexifina/serbia-law/blob/542a099cd5a137d6bd315b1596b033ce44dcd54e/zakon/2013/55-3/clan-097.md) | no text for 64 days (15 September to 18 November 2017) | The amendment 27/2018 is dated in force 15 September 2017, before 101/2017, which brings the articles back. The order comes from the register's dates, not from the law. |

### Lawful (5)

| Provision | What the record says | Why it is lawful |
| --- | --- | --- |
| [Закон о утврђивању порекла имовине и посебном порезу, чл. 2, 12 и 25](https://github.com/lexifina/serbia-law/blob/542a099cd5a137d6bd315b1596b033ce44dcd54e/zakon/2020/18-3/clan-002.md) | two laws change each article on 11 March 2021 | The law (18/2020) applied only from 11 March 2021, and 18/2021 amended it before that day. The original wording never applied. |
| [Одлука о извештавању банака](https://github.com/lexifina/serbia-law/blob/542a099cd5a137d6bd315b1596b033ce44dcd54e/odluka/2014/125-39/tekst.md) | two changes on 30 September 2023 | Only the publisher's note in the consolidated text changes; no rule is in conflict. |
| [Одлука о управљању ризиком концентрације по основу изложености банке одређеним врстама производа](https://github.com/lexifina/serbia-law/blob/542a099cd5a137d6bd315b1596b033ce44dcd54e/odluka/2018/103-88/tekst.md) | loans approved "until 18 March 2020" | A deliberate cut-off date that marks which loans the rule covers, not a rule that has run out. |

### Spent (1)

| Provision | What the record says | Why it is harmless |
| --- | --- | --- |
| [Одлука о јединственој структури за идентификацију и класификацију рачуна ... (IBAN), тачка 11](https://github.com/lexifina/serbia-law/blob/542a099cd5a137d6bd315b1596b033ce44dcd54e/odluka/2006/116-30/tekst.md) | account codes issued before 3 March 2007 "may be used until 31 October 2007" | A transitional rule that ended in 2007 but is still in the text of a decision in force. It is the clearest lapsed time limit in Serbian law found here, and it has no effect today. |

### Not law (3)

| Text | What the record says | Why it does not count |
| --- | --- | --- |
| [Bill 1867-25](https://github.com/lexifina/serbia-law/blob/542a099cd5a137d6bd315b1596b033ce44dcd54e/predlog/14/1867-25/tekst.md) and [bill 774-21](https://github.com/lexifina/serbia-law/blob/542a099cd5a137d6bd315b1596b033ce44dcd54e/predlog/12/774-21/tekst.md) | rules "until" 1 August 1992 and 31 December 2001 | Bills, not law; both dates are deliberate cut-offs. |
| [Republic Commission for Public Procurement, 4-00-1237/2010](https://github.com/lexifina/serbia-law/blob/542a099cd5a137d6bd315b1596b033ce44dcd54e/kjn/2010/4-00-1237-2010.md) | a period ending 23 August 2008 | A decision in one procurement case, not legislation. |

## What the other flags are

- **Lapsed time limits:** 1,727 of the 2,151 are in procurement decisions, explanatory memoranda, drafts and bills, where the dates are case facts or one-off steps. The model reviewed the 40 strongest overall and the 40 strongest in law texts: in law texts, the dates are transitional clauses that have run their course, deliberate cut-off dates, or text the build misread.
- **Duplicate numbering, dead currencies, publisher notes:** read by hand, not by a model. They are false positives: "dm" is decimetres and "DM" diabetes, "dinara" describes today's banknotes, and the "numbers" and "notes" are English treaty text or article references repeated in explanations.

## Problems found in this repository

- **Lost superscripts** in older rulebooks: "dm³" reads "dm?" (for example [pravilnik/1971/sfrj10-190/clan-039.md](https://github.com/lexifina/serbia-law/blob/542a099cd5a137d6bd315b1596b033ce44dcd54e/pravilnik/1971/sfrj10-190/clan-039.md)).
- **Tables the register shows as images** are missing from the files, which can look like a repealed article (the 2020 budget law above).
- **Versions dated by the register's application day** can start before the amendment that made them was published (the four open cases above).

## Files

| File | What it holds |
| --- | --- |
| [data/flags.csv](data/flags.csv) | Every flag, one row per provision and issue |
| [data/reviewed.csv](data/reviewed.csv) | The 194 flags the model reviewed, with its verdict and reason |
| [data/by_category.csv](data/by_category.csv) | The counts in the table above |
| [tools/](tools/) | The scripts that made this run |

Columns: `category` and `category_sr` (the category in English and Serbian), `detector`, `kind` (`law` or `other`), `path` (the file in this repository), `date` (the date the flag turns on), `reference` (the law or line involved), `summary`, `score` (the detector's ranking, 0 to 1), `review` (`artefact`, `lawful` or `candidate_defect`), `survives_rebuttal`, `review_note` (the model's reason, in English), `url` (the provision or commit at the commit that was read).

## How it was made

- **Detectors:** global-law's [vulnerabilities/scripts](https://github.com/lexifina/global-law/tree/main/vulnerabilities/scripts), run on this repository at commit `542a099`. global-law does not replay Serbia's history yet, so the history table the detectors read was built from this repository's own commit trailers (`Law`, `Kind`, `In-force`).
- **Model review:** gpt-5.4-mini, the 40 strongest flags per category, and for lapsed time limits also the 40 strongest in law texts; one pass says whether a flag is real, a second argues that it is not. Where a flag was reviewed twice, the later review is kept. global-law's own list used a different model.
- **Hand check:** every case that survived was read in this repository's history and texts. The four open dates still need the Службени гласник itself.

To report a correction, open an issue with the provision and an official source.

## Licence

The lists and notes are Lexifina's, dedicated to the public domain under CC0 1.0, like the rest of this repository's own contributions. Quoted law text is as the official register prints it; see [LICENSE](../LICENSE).
