# Monitoring: does Serbia keep up?

[Srpski](README.md)

How global-law monitors every corpus (a pass every 15 minutes, a check of every commit, a public status): [global-law monitoring/](https://github.com/lexifina/global-law/tree/main/monitoring). This page is the state of this repository alone.

**Status 2026-11-14**

| | |
| --- | --- |
| Last commit | 2026-11-14 15:51 UTC: Visualisations: Serbian law in 20 charts (visualisations/srpsko-pravo-u-20-grafikona.html), linked from both READMEs |
| Last 24 hours | 12,408 court and other decisions; 4,034 local acts; 1,601 drafts and bills; 269 laws as adopted; 102 documents and tables; 19 documentation |
| Last 7 days | 12,408 court and other decisions; 4,034 local acts; 1,601 drafts and bills; 269 laws as adopted; 102 documents and tables; 23 documentation |
| Last 30 days | 12,408 court and other decisions; 12,358 acts; 4,034 local acts; 1,601 drafts and bills; 1,037 publisher texts; 269 laws as adopted; 102 documents and tables; 45 documentation; 28 Constitutional Court rulings in the text |
| global-law | `serbia/national/acts` is `stale`, pinned at `2abec326ad`, 18,433 newer commits here |
| Register of acts | paused: waiting for Službeni glasnik's written consent (the register's terms of use; see PLAN.md) |
| Stale sources | none ([FRESHNESS.en.md](../FRESHNESS.en.md)) |

## How new changes arrive

1. Each source's lane reads its list of new texts (see [WATCHING.en.md](../WATCHING.en.md)) and publishes each change as a commit dated the day it applies.
2. Before publishing, every commit goes through this repository's checks: the text against the source, the dates against the Official Gazette header (see [REPRODUCE.md](../REPRODUCE.md)).
3. Every 15 minutes global-law checks new commits and moves its pin on `serbia/national/acts` (see [global-law monitoring/](https://github.com/lexifina/global-law/tree/main/monitoring)).

## Check it yourself

```
git fetch && git log -1 --format="%cI %s" origin/main
git log --since=1.day --format="%cs %s" origin/main | wc -l
python monitoring/make_pages.py           # rebuild these three pages
```
