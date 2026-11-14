# Ažurnost: da li je tačno danas?

[English](FRESHNESS.en.md)

Kako global-law meri ažurnost svih korpusa (stanja, pragovi od 7 i 30 dana, alat `freshness.py`): [global-law FRESHNESS.md](https://github.com/lexifina/global-law/blob/main/FRESHNESS.md). Ovde je isto merenje za Srbiju, izvor po izvor.

## Kako ga vidi global-law

| Korpus | Stanje | Poslednja provera | Način | Komit u global-law | Novijih komita ovde |
| --- | --- | --- | --- | --- | ---: |
| `serbia/national/acts` | `stale` | 4. 11. 2026. | `source-retrieval` | `2abec326ad` | 18.438 |

`stale`: prag za nacionalno pravo je 7 dana od poslednje provere. Komitovi novijih od zakačenog global-law preuzima pri sledećem prolazu; do tada ih čitajte ovde.

## Izvor po izvor

„Najnoviji zapis“ je najkasniji dan primene ili odluke koji nije u budućnosti; „poslednji put pročitan“ je dan kada je ovaj repozitorijum poslednji put objavio nešto iz izvora. Prag: 7 dana za nacionalne propise, 30 za lokalne akte, sudsku praksu i dokumente.

| Izvor | Komita | Najnoviji zapis | Poslednji put pročitan | Dana od tada | Stanje | Napomena |
| --- | ---: | --- | --- | ---: | --- | --- |
| Pravno-informacioni sistem RS (Službeni glasnik) | 12.388 | 1. 11. 2026. | 3. 11. 2026. | 11 | zastarelo |  |
| Narodna skupština | 1.713 | 14. 11. 2026. | 14. 11. 2026. | 0 | ažurno |  |
| Ustavni sud | 11.521 | 2. 7. 2026. | 14. 11. 2026. | 0 | ažurno |  |
| Apelacioni sud u Kragujevcu | 479 | 14. 5. 2026. | 14. 11. 2026. | 0 | ažurno |  |
| Komisija za zaštitu konkurencije | 243 | 21. 9. 2026. | 14. 11. 2026. | 0 | ažurno |  |
| Republička komisija za zaštitu prava u postupcima javnih nabavki | 165 | 7. 7. 2011. | 14. 11. 2026. | 0 | ažurno | arhiva starog sajta komisije: odluke do 2011. |
| eKonsultacije | 218 | 7. 9. 2026. | 14. 11. 2026. | 0 | ažurno |  |
| Službeni list Grada Beograda | 2.728 | 3. 11. 2026. | 14. 11. 2026. | 0 | ažurno | 1 sa datumom primene u budućnosti |
| Službeni list Grada Novog Sada | 1.279 | 7. 11. 2026. | 14. 11. 2026. | 0 | ažurno | 13 sa datumom primene u budućnosti |
| Službeni list grada Kragujevca | 27 | 22. 11. 2025. | 14. 11. 2026. | 0 | ažurno |  |
| Zaštitnik građana | 19 | 17. 9. 2026. | 14. 11. 2026. | 0 | ažurno |  |
| Vlada Republike Srbije | 12 | 14. 11. 2026. | 14. 11. 2026. | 0 | ažurno |  |
| Agencija za energetiku | 3 | 6. 2. 2026. | 14. 11. 2026. | 0 | ažurno |  |
| Komisija za hartije od vrednosti | 1 | 13. 2. 2026. | 14. 11. 2026. | 0 | ažurno |  |
| Portal otvorenih podataka (data.gov.rs) | 114 | 13. 11. 2026. | 14. 11. 2026. | 0 | ažurno | broj je broj skupova podataka, ne komita |

## Proverite sami

```
git log -1 --format="%cs %s" -- zakon/                # poslednji objavljeni zakon
git log -1 --format="%as %s" -- zakon/2001/24-1/      # poslednja verzija jednog propisa (dan primene)
git log --since=7.days --format="%cs %s" | head        # šta je stiglo ove nedelje
```

Kada je datum koji vas zanima posle poslednje provere, potvrdite tekst u zvaničnom izvoru. Samo zvanična objava ima pravnu snagu.
