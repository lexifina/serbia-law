# Monitoring: does Serbia keep up?

[Srpski](README.md)

How global-law monitors every corpus (a pass every 15 minutes, a check of every commit, a public status): [global-law monitoring/](https://github.com/lexifina/global-law/tree/main/monitoring). This page is the state of this repository alone.

**Status 2026-11-14**

| | |
| --- | --- |
| Last commit | 2026-11-14 16:23 UTC: vulnerabilities/: what the other flags are moves into EDGE-CASES; the READMEs point to it in a note under the category t… |
| Last 24 hours | 12,408 court and other decisions; 4,034 local acts; 1,601 drafts and bills; 269 laws as adopted; 102 documents and tables; 24 documentation |
| Last 7 days | 12,408 court and other decisions; 4,034 local acts; 1,601 drafts and bills; 269 laws as adopted; 102 documents and tables; 28 documentation |
| Last 30 days | 12,408 court and other decisions; 12,358 acts; 4,034 local acts; 1,601 drafts and bills; 1,037 publisher texts; 269 laws as adopted; 102 documents and tables; 50 documentation; 28 Constitutional Court rulings in the text |
| global-law | `serbia/national/acts` is `stale`, pinned at `2abec326ad`, 18,438 newer commits here |
| Stale sources | Legal Information System of Serbia (Official Gazette) ([FRESHNESS.en.md](../FRESHNESS.en.md)) |

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

## Watch it yourself: a fork and GitHub Actions

Anyone can fork this repository and keep their copy current without us. GitHub Actions is free for public repositories.

1. Fork it: <https://github.com/lexifina/serbia-law/fork>.
2. In the fork, copy [`monitoring/fork-workflow.yml`](fork-workflow.yml) to `.github/workflows/refresh.yml` and commit it to `main`.
3. On the fork's **Actions** tab, enable workflows (GitHub turns them off in forks by default) and run **Refresh from lexifina/serbia-law** once.

Every 6 hours the workflow takes the new commits from this repository into your fork's `main` (through GitHub's own "Sync fork", so your `main` is this repository plus your workflow file), rebuilds WATCHING, FRESHNESS and this page for your copy, publishes them to a `status` branch and shows FRESHNESS in the run summary. A run takes about two minutes. The workflow does not read the official sources: it checks how current this repository is.
