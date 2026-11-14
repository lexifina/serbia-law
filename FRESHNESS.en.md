# Freshness: is it true right now?

[Srpski](FRESHNESS.md)

How global-law measures freshness for every corpus (the statuses, the 7- and 30-day thresholds, the `freshness.py` tool): [global-law FRESHNESS.md](https://github.com/lexifina/global-law/blob/main/FRESHNESS.md). Here is the same measure for Serbia, source by source.

## How global-law sees it

| Corpus | Status | Last checked | Method | Commit pinned in global-law | Newer commits here |
| --- | --- | --- | --- | --- | ---: |
| `serbia/national/acts` | `stale` | 2026-11-04 | `source-retrieval` | `2abec326ad` | 18,433 |

`stale`: the threshold for national law is 7 days since the last check. global-law takes commits newer than the pinned one on its next pass; until then, read them here.

## Source by source

"Newest record" is the latest day of application or decision that is not in the future; "last read" is the day this repository last published something from the source. Threshold: 7 days for national acts, 30 for local acts, case law and documents.

| Source | Commits | Newest record | Last read | Days since | State | Note |
| --- | ---: | --- | --- | ---: | --- | --- |
| Legal Information System of Serbia (Official Gazette) | 12,388 | 2026-11-01 | 2026-11-03 | 11 | paused | waiting for Službeni glasnik's written consent (the register's terms of use; see PLAN.md) |
| National Assembly | 1,713 | 2026-11-14 | 2026-11-14 | 0 | current |  |
| Constitutional Court | 11,521 | 2026-07-02 | 2026-11-14 | 0 | current |  |
| Court of Appeal in Kragujevac | 479 | 2026-05-14 | 2026-11-14 | 0 | current |  |
| Commission for Protection of Competition | 243 | 2026-09-21 | 2026-11-14 | 0 | current |  |
| Republic Commission for the Protection of Rights in Public Procurement | 165 | 2011-07-07 | 2026-11-14 | 0 | current | the archive of the commission's old site: decisions up to 2011 |
| eKonsultacije (public consultations) | 218 | 2026-09-07 | 2026-11-14 | 0 | current |  |
| Official Gazette of the City of Belgrade | 2,728 | 2026-11-03 | 2026-11-14 | 0 | current | 1 dated in the future |
| Official Gazette of the City of Novi Sad | 1,279 | 2026-11-07 | 2026-11-14 | 0 | current | 13 dated in the future |
| Official Gazette of the City of Kragujevac | 27 | 2025-11-22 | 2026-11-14 | 0 | current |  |
| Protector of Citizens (Ombudsman) | 19 | 2026-09-17 | 2026-11-14 | 0 | current |  |
| Government of Serbia | 12 | 2026-11-14 | 2026-11-14 | 0 | current |  |
| Energy Agency | 3 | 2026-02-06 | 2026-11-14 | 0 | current |  |
| Securities Commission | 1 | 2026-02-13 | 2026-11-14 | 0 | current |  |
| Open data portal (data.gov.rs) | 114 | 2026-11-13 | 2026-11-14 | 0 | current | the count is datasets, not commits |

## Check it yourself

```
git log -1 --format="%cs %s" -- zakon/                # the last law published
git log -1 --format="%as %s" -- zakon/2001/24-1/      # one act's latest version (day it applies)
git log --since=7.days --format="%cs %s" | head        # what arrived this week
```

When the date you care about is after the last check, confirm the text against the official source. Only the official publication has legal force.
