# Edge cases

[Srpski](EDGE-CASES.md) · **English**

The 17 flags that survived the model review, each checked by hand. Back to [the vulnerabilities README](README.en.md).

## Open: check the date against the Gazette (4)

| Act | What the record says | Why it is probably a data error |
| --- | --- | --- |
| [Одлука о условима које треба да испуни организација удруженог рада која врши дезинфекцију, дезинсекцију и дератизацију](https://github.com/lexifina/serbia-law/commit/24f267b15abe645fa7cf1608710a34d1b4d0f28d) („Службени гласник СРС” 23/1979) | in force 17 June 1971, published 9 June 1979 | The decision rests on a 1977 law, so it cannot have applied from 1971. The date is the register's. |
| [Одлука о оснивању Геронтолошког центра у Вршцу](https://github.com/lexifina/serbia-law/commit/c8d81385c52c6853457e768f08ca48382fda8c02) („Службени гласник РС” 50/1999) | in force 3 December 1992, published 25 November 1999 | The date may belong to an earlier founding act that the 1999 text restates. |
| [Правилник о безбедности машина](https://github.com/lexifina/serbia-law/commit/57306156d7f951d8c63f80fe625413132a584718), as amended by „Службени гласник РС” 21/2020 | version in force 1 September 2016, amendment published 6 March 2020 | The register dates the consolidated version from the rulebook's own start, not from the amendment. |
| [Уредба о начину и поступку извршавања војне, радне и материјалне обавезе](https://github.com/lexifina/serbia-law/commit/187e6a51b8a8ae31b16cb9ab324468a1a59a72ac), as amended by „Службени гласник РС” 40/2019 | version in force 15 June 2016, amendment published 7 June 2019 | The same pattern as the rulebook above. |

## Explained by how this repository was built (4)

| Provision | What the record says | What happened |
| --- | --- | --- |
| [Закон о буџету Републике Србије за 2020. годину, члан 3.](https://github.com/lexifina/serbia-law/blob/542a099cd5a137d6bd315b1596b033ce44dcd54e/zakon/2019/84-3/clan-003.md) | no text for 203 days (24 April to 13 November 2020) | The article is a table of state guarantees, which the register shows as an image in the 60/2020 version, so the build dropped it. The article was not repealed. |
| [Закон о основном образовању и васпитању, чл. 97, 98 и 99](https://github.com/lexifina/serbia-law/blob/542a099cd5a137d6bd315b1596b033ce44dcd54e/zakon/2013/55-3/clan-097.md) | no text for 64 days (15 September to 18 November 2017) | The amendment 27/2018 is dated in force 15 September 2017, before 101/2017, which brings the articles back. The order comes from the register's dates, not from the law. |

## Lawful (5)

| Provision | What the record says | Why it is lawful |
| --- | --- | --- |
| [Закон о утврђивању порекла имовине и посебном порезу, чл. 2, 12 и 25](https://github.com/lexifina/serbia-law/blob/542a099cd5a137d6bd315b1596b033ce44dcd54e/zakon/2020/18-3/clan-002.md) | two laws change each article on 11 March 2021 | The law (18/2020) applied only from 11 March 2021, and 18/2021 amended it before that day. The original wording never applied. |
| [Одлука о извештавању банака](https://github.com/lexifina/serbia-law/blob/542a099cd5a137d6bd315b1596b033ce44dcd54e/odluka/2014/125-39/tekst.md) | two changes on 30 September 2023 | Only the publisher's note in the consolidated text changes; no rule is in conflict. |
| [Одлука о управљању ризиком концентрације по основу изложености банке одређеним врстама производа](https://github.com/lexifina/serbia-law/blob/542a099cd5a137d6bd315b1596b033ce44dcd54e/odluka/2018/103-88/tekst.md) | loans approved "until 18 March 2020" | A deliberate cut-off date that marks which loans the rule covers, not a rule that has run out. |

## Spent (1)

| Provision | What the record says | Why it is harmless |
| --- | --- | --- |
| [Одлука о јединственој структури за идентификацију и класификацију рачуна ... (IBAN), тачка 11](https://github.com/lexifina/serbia-law/blob/542a099cd5a137d6bd315b1596b033ce44dcd54e/odluka/2006/116-30/tekst.md) | account codes issued before 3 March 2007 "may be used until 31 October 2007" | A transitional rule that ended in 2007 but is still in the text of a decision in force. It is the clearest lapsed time limit in Serbian law found here, and it has no effect today. |

## Not law (3)

| Text | What the record says | Why it does not count |
| --- | --- | --- |
| [Bill 1867-25](https://github.com/lexifina/serbia-law/blob/542a099cd5a137d6bd315b1596b033ce44dcd54e/predlog/14/1867-25/tekst.md) and [bill 774-21](https://github.com/lexifina/serbia-law/blob/542a099cd5a137d6bd315b1596b033ce44dcd54e/predlog/12/774-21/tekst.md) | rules "until" 1 August 1992 and 31 December 2001 | Bills, not law; both dates are deliberate cut-offs. |
| [Republic Commission for Public Procurement, 4-00-1237/2010](https://github.com/lexifina/serbia-law/blob/542a099cd5a137d6bd315b1596b033ce44dcd54e/kjn/2010/4-00-1237-2010.md) | a period ending 23 August 2008 | A decision in one procurement case, not legislation. |
