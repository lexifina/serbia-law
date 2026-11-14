# Srpsko pravo u 20 grafikona

[English](README.en.md)

Grafikoni o pravu svih zemalja, iz celog global-law-a: [global-law visualisations/](https://github.com/lexifina/global-law/tree/main/visualisations). Ovde su samo grafikoni o Srbiji.

Dvadeset grafikona o srpskom pravu, nacrtanih samo iz podataka ovog repozitorijuma: propisi iz Pravno-informacionog sistema, predlozi zakona Narodne skupštine, praksa Ustavnog suda, žalbe Povereniku za informacije od javnog značaja, preporuke Državne revizorske institucije i Službeni list Grada Beograda.

Otvorite [`srpsko-pravo-u-20-grafikona.html`](srpsko-pravo-u-20-grafikona.html) u pregledaču. Stranica je jedna datoteka sa svim podacima u sebi; sa interneta učitava samo biblioteku d3 i fontove. Gore desno se biraju jezik (srpski, latinica, ili engleski) i tema (svetla ili tamna). Uz svaki grafikon stoje putanja podataka u repozitorijumu, broj zapisa i ograničenja, a ispod njega tabela sa svim brojevima. Pređite mišem preko oznake da vidite tačne vrednosti.

Grafikoni su opisni: pokazuju šta izvori beleže, ne zašto.

## Grafikoni

### I. Narodna skupština

1. **Šta Skupština usvaja.** Zakoni po godini i vrsti: izmene i dopune, novi zakoni, potvrđivanje ugovora, zajmovi, garancije, budžet.
   ![1](stills/sr/01.png)
2. **Ko pozajmljuje Srbiji.** Zakoni o potvrđivanju ugovora o zajmu, po zajmodavcu i godini.
   ![2](stills/sr/02.png)
3. **S kim Srbija sklapa ugovore.** Zakoni o potvrđivanju po drugoj strani ugovornici.
   ![3](stills/sr/03.png)
4. **Zakoni se usvajaju u paketima.** Svaki dan za glasanje i koliko je zakona tada usvojeno; dve trećine zakona prođe na danima sa 10 ili više zakona.
   ![4](stills/sr/04.png)
5. **Od predloga do zakona.** Koliko dana predlog provede u Skupštini, po sazivu.
   ![5](stills/sr/05.png)

### II. Pravni poredak

6. **Ko piše propise.** Važeći akti po vrsti: zakoni su oko šestine; ostalo su pravilnici, odluke i uredbe.
   ![6](stills/sr/06.png)
7. **Jugoslovenski slojevi.** Važeći akti objavljeni u glasilima FNRJ, SFRJ, SR Srbije, SRJ i SCG.
   ![7](stills/sr/07.png)
8. **Vacatio legis.** Koliko zakona, uredbi, pravilnika i odluka stupa na snagu pre osmog dana od objavljivanja (Ustav, čl. 196).
   ![8](stills/sr/08.png)
9. **Najčešće menjani zakoni.** Broj izdanja Službenog glasnika koja su menjala tekst, za 25 zakona.
   ![9](stills/sr/09.png)
10. **Život zakona.** Ista izdanja na vremenskoj osi.
    ![10](stills/sr/10.png)
11. **Pravna godina.** Izmene po mesecu stupanja na snagu, 2016–2025.
    ![11](stills/sr/11.png)

### III. Ustavni sud

12. **Ustavne žalbe u objavljenoj praksi.** Odluke po godini i ishodu, i šta baza zapravo pokazuje.
    ![12](stills/sr/12.png)
13. **Na koja prava se žalioci pozivaju.** Članovi Ustava navedeni u odlukama i koliko je tih odluka usvojeno.
    ![13](stills/sr/13.png)
14. **Koliko žalba čeka.** Godina podnošenja (iz broja predmeta) naspram godine odluke.
    ![14](stills/sr/14.png)
15. **Šta se osporava.** Osporeni akt po upisniku suda; petina žalbi osporava sam postupak koji traje ili odluku o zahtevu za suđenje u razumnom roku.
    ![15](stills/sr/15.png)
16. **Kada Sud kaže „nesaglasno“.** Opšti akti oglašeni neustavnim ili nezakonitim, po godini i vrsti.
    ![16](stills/sr/16.png)

### IV. Uprava pod nadzorom

17. **Ćutanje uprave.** Žalbe Povereniku po godini i osnovu; skoro polovina je zato što organ nije odgovorio.
    ![17](stills/sr/17.png)
18. **Ko ćuti.** Udeo žalbi zbog ćutanja po vrsti organa.
    ![18](stills/sr/18.png)
19. **Preporuke Državne revizorske institucije.** Status preporuka po vrsti revidiranog subjekta.
    ![19](stills/sr/19.png)

### V. Beograd

20. **Službeni list Grada Beograda.** Akti po izdavaocu (Grad i 17 gradskih opština) i godini, 2002–2014.
    ![20](stills/sr/20.png)

## Podaci

Stanje na komitu `542a099cd5` (14. novembar 2026).

| Skup podataka | Gde je u repozitorijumu | Zapisa | Obuhvat |
| --- | --- | ---: | --- |
| Istorija gita | grana `main` | 31.883 komita | datum komita je datum stupanja na snagu ili odluke |
| Akti u registru | `<vrsta>/<godina>/<broj>/`, `registry/data/acts.json` | 9.835 akata | važeći akti PIS-a, najstariji iz 1947. |
| Predlozi zakona | `data/bills-*.csv` | 2.794 (2.296 usvojeno) | 2007–2026, potpuno od 2011. |
| Ustavni sud | `sudska-praksa/ustavni-sud/` | 11.521 odluka (10.759 Už) | 2008–2026 |
| Žalbe Povereniku | `data/registers/poverenik/` | 80.153 žalbe | 2013–2026 |
| Preporuke DRI | `data/registers/dri/registar-preporuka-1.csv` | 3.736 preporuka | status na dan 30. 4. 2026. |
| Sl. list Grada Beograda | `data/local/beograd/` | 13.554 akta | 2002–2014 |

## Ograničenja

- **Registar beleži važeće akte.** Ukinuti akti nisu u njemu, pa grafikoni 6, 7 i 9 opisuju pravo koje danas važi, ne sve što je ikada doneto. Za mnoge akte registar ima tekst tek od sredine 2010-ih; ranije izmene poznate su samo kao spisak brojeva Službenog glasnika.
- **Baza sudske prakse Ustavnog suda je izbor.** Sud ne objavljuje sve odluke, pa udeo usvojenih žalbi u bazi (grafikon 12) nije stopa uspeha žalbi.
- **Vrste se čitaju iz naslova.** Vrsta zakona (grafikon 1), zajmodavac (4), druga strana ugovora (5), upisnik suda (15), vrsta osporenog akta (16) i vrsta revidiranog subjekta (19) pročitani su iz teksta naslova pravilima u `src/prep.py`. Šta pravila nisu prepoznala stoji kao „Ostalo“ i vidi se u tabeli.
- **Spisak predloga zakona nema podatak o hitnom postupku ni o predlagaču.** Grafikon 3 meri samo vreme od podnošenja do usvajanja.
- **Delimične godine** (2026 kod predloga i žalbi) nacrtane su svetlije i tako označene.

## Ponovno pravljenje

```sh
python visualisations/src/make.py            # git log + tabele -> src/.build/ -> srpsko-pravo-u-20-grafikona.html
node visualisations/src/stills.cjs           # slike za ove README datoteke (traži Playwright; PLAYWRIGHT=<putanja> ako nije globalno)
```

`make.py` čita sve iz git objekata, pa radi i u delimičnom (sparse) ili `--no-checkout` klonu. Podrazumevano čita `origin/main` (ili `HEAD`); `--ref` bira drugu granu ili komit. Ništa ne upisuje u repozitorijum osim stranice i fascikle `src/.build/` (koja se ne čuva u gitu).

| Datoteka | Šta radi |
| --- | --- |
| `src/make.py` | izvlači istoriju, fascikle akata i tabele u `src/.build/`, pa pokreće `prep.py` i `build.py` |
| `src/prep.py` | računa sve brojeve za 20 grafikona i profil podataka u `src/.build/data.json` |
| `src/page.tpl.html` | stranica: tekstovi na oba jezika, grafikoni (d3), tabele |
| `src/build.py` | ubacuje `data.json` u šablon i piše stranicu |
| `src/stills.cjs` | crta svaki grafikon kao PNG u `stills/sr/` i `stills/en/` |
