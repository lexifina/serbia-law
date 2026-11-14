# Praćenje: da li Srbija ide u korak?

[English](README.en.md)

Kako global-law prati sve korpuse (prolaz na svakih 15 minuta, provera svakog komita, javni status): [global-law monitoring/](https://github.com/lexifina/global-law/tree/main/monitoring). Ovde je stanje samo za ovaj repozitorijum.

**Stanje 14. 11. 2026.**

| | |
| --- | --- |
| Poslednji komit | 2026-11-14 15:51 UTC: Visualisations: Serbian law in 20 charts (visualisations/srpsko-pravo-u-20-grafikona.html), linked from both READMEs |
| Poslednja 24 sata | 12.408 sudske i druge odluke; 4.034 lokalni akti; 1.601 nacrti i predlozi; 269 zakoni kako su usvojeni; 102 dokumenti i tabele; 19 dokumentacija |
| Poslednjih 7 dana | 12.408 sudske i druge odluke; 4.034 lokalni akti; 1.601 nacrti i predlozi; 269 zakoni kako su usvojeni; 102 dokumenti i tabele; 23 dokumentacija |
| Poslednjih 30 dana | 12.408 sudske i druge odluke; 12.358 propisi; 4.034 lokalni akti; 1.601 nacrti i predlozi; 1.037 tekstovi izdavača; 269 zakoni kako su usvojeni; 102 dokumenti i tabele; 45 dokumentacija; 28 odluke Ustavnog suda u tekstu |
| global-law | `serbia/national/acts` je `stale`, zakačen na `2abec326ad`, 18.433 novijih komita ovde |
| Registar propisa | pauziran: čeka pismenu saglasnost Službenog glasnika (uslovi korišćenja registra; vidi PLAN.md) |
| Zastareli izvori | nema ([FRESHNESS.md](../FRESHNESS.md)) |

## Kako nove izmene stižu

1. Traka za svaki izvor čita njegov spisak novih tekstova (vidi [WATCHING.md](../WATCHING.md)) i svaku promenu objavljuje kao komit sa datumom dana kada se primenjuje.
2. Pre objavljivanja svaki komit prolazi provere ovog repozitorijuma: tekst se poredi sa izvorom, a datumi sa zaglavljem Službenog glasnika (vidi [REPRODUCE.md](../REPRODUCE.md)).
3. global-law na svakih 15 minuta proverava nove komitove i pomera svoj pokazivač na `serbia/national/acts` (vidi [global-law monitoring/](https://github.com/lexifina/global-law/tree/main/monitoring)).

## Proverite sami

```
git fetch && git log -1 --format="%cI %s" origin/main
git log --since=1.day --format="%cs %s" origin/main | wc -l
python monitoring/make_pages.py           # ponovo napravi ove tri stranice
```
