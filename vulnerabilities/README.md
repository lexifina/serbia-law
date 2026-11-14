# Ranjivosti u propisima Srbije

**Srpski** · [English](README.en.md)

Detektori ranjivosti iz repozitorijuma [lexifina/global-law](https://github.com/lexifina/global-law/tree/main/vulnerabilities) traže mehaničke greške u propisima: pravilo koje se i dalje primenjuje „do” datuma koji je prošao, odredbu ukinutu pre nego što je njena zamena stupila na snagu, dve izmene iste odredbe istog dana, pravilo koje važi pre nego što je objavljeno. Lista koju je global-law objavio (9. novembra 2026) još nije obuhvatala Srbiju, pa je ovo provera samo ovog repozitorijuma, u stanju na commitu [`542a099`](https://github.com/lexifina/serbia-law/commit/542a099cd5a137d6bd315b1596b033ce44dcd54e) od 14. novembra 2026.

**Ukratko:** detektori su označili 3.154 mesta. Jezički model je pregledao 194 najjača, i za svako izneo argumente za i protiv; 17 je izdržalo proveru. Pregledano ručno u ovom repozitorijumu, nijedno nije potvrđena greška u pravu Srbije. Osam potiče od načina na koji registar datira verzije ili od načina na koji je ovaj repozitorijum napravljen, pet je zakonito, jedno je istekla prelazna odredba, a tri uopšte nisu propisi. Četiri datuma ostaju otvorena dok se ne provere u „Službenom glasniku”.

Oznaka je poziv da se pogleda, a ne pravni savet, i ništa od ovoga nije provereno pred sudom.

## Oznake po vrsti

| Vrsta | Šta traži | Oznake | U propisima | Pregledano | Izdržalo pregled |
| --- | --- | ---: | ---: | ---: | ---: |
| Istekli rokovi | Tekst koji se i dalje primenjuje „do” datuma koji je prošao | 2.151 | 424 | 76 | 5 |
| Praznine posle ukidanja | Odredba uklonjena pre nego što je njena zamena stupila na snagu | 38 | 38 | 38 | 4 |
| Izmene istog dana | Dva propisa menjaju istu odredbu istog dana | 145 | 145 | 40 | 4 |
| Datumi pre donošenja ili objavljivanja | Pravilo koje važi pre nego što je doneto ili objavljeno | 339 | 339 | 40 | 4 |
| Dvostruko numerisanje | Dve jedinice sa istim brojem u jednoj odredbi | 400 | 209 | 0 | 0 |
| Ukinute valute | Iznosi u valutama koje se više ne koriste | 67 | 26 | 0 | 0 |
| Napomene izdavača | Napomene da izmena nije mogla da se unese | 14 | 6 | 0 | 0 |

„U propisima” obuhvata zakone, podzakonske akte, odluke i međunarodne ugovore. Ostale oznake su u nacrtima, predlozima zakona, sudskim odlukama i izveštajima, koje ovaj repozitorijum takođe sadrži i označava kao tekstove koji nisu propisi.

## 17 slučajeva koji su izdržali pregled

### Otvoreno: datum treba proveriti u „Službenom glasniku” (4)

| Akt | Šta piše u zapisu | Zašto je verovatno greška u podacima |
| --- | --- | --- |
| [Одлука о условима које треба да испуни организација удруженог рада која врши дезинфекцију, дезинсекцију и дератизацију](https://github.com/lexifina/serbia-law/commit/24f267b15abe645fa7cf1608710a34d1b4d0f28d) („Службени гласник СРС” 23/1979) | na snazi od 17. juna 1971, objavljena 9. juna 1979. | Odluka se poziva na zakon iz 1977. godine („Службени гласник СРС” 28/77), pa nije mogla da se primenjuje od 1971. Datum potiče iz registra. |
| [Одлука о оснивању Геронтолошког центра у Вршцу](https://github.com/lexifina/serbia-law/commit/c8d81385c52c6853457e768f08ca48382fda8c02) („Службени гласник РС” 50/1999) | na snazi od 3. decembra 1992, objavljena 25. novembra 1999. | Datum možda pripada ranijem aktu o osnivanju koji tekst iz 1999. ponavlja. |
| [Правилник о безбедности машина](https://github.com/lexifina/serbia-law/commit/57306156d7f951d8c63f80fe625413132a584718), sa izmenom iz „Службеног гласника РС” 21/2020 | verzija na snazi od 1. septembra 2016, izmena objavljena 6. marta 2020. | Registar datira prečišćenu verziju od početka primene samog pravilnika, a ne od izmene. |
| [Уредба о начину и поступку извршавања војне, радне и материјалне обавезе](https://github.com/lexifina/serbia-law/commit/187e6a51b8a8ae31b16cb9ab324468a1a59a72ac), sa izmenom iz „Службеног гласника РС” 40/2019 | verzija na snazi od 15. juna 2016, izmena objavljena 7. juna 2019. | Isti obrazac kao kod pravilnika iznad. |

### Objašnjeno načinom izrade ovog repozitorijuma (4)

| Odredba | Šta piše u zapisu | Šta se dogodilo |
| --- | --- | --- |
| [Закон о буџету Републике Србије за 2020. годину, члан 3.](https://github.com/lexifina/serbia-law/blob/542a099cd5a137d6bd315b1596b033ce44dcd54e/zakon/2019/84-3/clan-003.md) | bez teksta 203 dana (od 24. aprila do 13. novembra 2020) | Član je tabela državnih garancija, koju registar u verziji 60/2020 prikazuje kao sliku, pa je izrada repozitorijuma izostavila. Član nije ukinut. |
| [Закон о основном образовању и васпитању, чл. 97, 98 и 99](https://github.com/lexifina/serbia-law/blob/542a099cd5a137d6bd315b1596b033ce44dcd54e/zakon/2013/55-3/clan-097.md) | bez teksta 64 dana (od 15. septembra do 18. novembra 2017) | Izmena 27/2018 datirana je kao da važi od 15. septembra 2017, pre izmene 101/2017, koja te članove vraća. Redosled potiče od datuma u registru, ne od zakona. |

### Zakonito (5)

| Odredba | Šta piše u zapisu | Zašto je zakonito |
| --- | --- | --- |
| [Закон о утврђивању порекла имовине и посебном порезу, чл. 2, 12 и 25](https://github.com/lexifina/serbia-law/blob/542a099cd5a137d6bd315b1596b033ce44dcd54e/zakon/2020/18-3/clan-002.md) | dva propisa menjaju svaki od ovih članova 11. marta 2021. | Zakon (18/2020) primenjuje se tek od 11. marta 2021, a izmena 18/2021 promenila ga je pre tog dana. Prvobitni tekst se nikada nije primenjivao. |
| [Одлука о извештавању банака](https://github.com/lexifina/serbia-law/blob/542a099cd5a137d6bd315b1596b033ce44dcd54e/odluka/2014/125-39/tekst.md) | dve izmene 30. septembra 2023. | Menja se samo napomena izdavača u prečišćenom tekstu; nijedno pravilo nije u sukobu. |
| [Одлука о управљању ризиком концентрације по основу изложености банке одређеним врстама производа](https://github.com/lexifina/serbia-law/blob/542a099cd5a137d6bd315b1596b033ce44dcd54e/odluka/2018/103-88/tekst.md) | krediti odobreni „do 18. marta 2020. godine” | Namerni presečni datum koji određuje na koje se kredite pravilo odnosi, a ne pravilo koje je isteklo. |

### Isteklo (1)

| Odredba | Šta piše u zapisu | Zašto je bezopasno |
| --- | --- | --- |
| [Одлука о јединственој структури за идентификацију и класификацију рачуна ... (IBAN), тачка 11](https://github.com/lexifina/serbia-law/blob/542a099cd5a137d6bd315b1596b033ce44dcd54e/odluka/2006/116-30/tekst.md) | oznake računa izdate do 3. marta 2007. „mogu da se primenjuju najkasnije do 31. oktobra 2007. godine” | Prelazna odredba koja je istekla 2007, ali je i dalje u tekstu odluke koja je na snazi. To je najjasniji istekli rok u pravu Srbije koji je ovde pronađen, i danas nema dejstvo. |

### Nije propis (3)

| Tekst | Šta piše u zapisu | Zašto se ne računa |
| --- | --- | --- |
| [Predlog zakona 1867-25](https://github.com/lexifina/serbia-law/blob/542a099cd5a137d6bd315b1596b033ce44dcd54e/predlog/14/1867-25/tekst.md) i [predlog zakona 774-21](https://github.com/lexifina/serbia-law/blob/542a099cd5a137d6bd315b1596b033ce44dcd54e/predlog/12/774-21/tekst.md) | pravila „do” 1. avgusta 1992. i 31. decembra 2001. | Predlozi, a ne propisi; oba datuma su namerni presečni datumi. |
| [Republička komisija za zaštitu prava u postupcima javnih nabavki, 4-00-1237/2010](https://github.com/lexifina/serbia-law/blob/542a099cd5a137d6bd315b1596b033ce44dcd54e/kjn/2010/4-00-1237-2010.md) | period koji se završava 23. avgusta 2008. | Odluka u jednom postupku javne nabavke, a ne propis. |

## Šta su ostale oznake

- **Istekli rokovi:** 1.727 od 2.151 nalazi se u odlukama o javnim nabavkama, obrazloženjima, nacrtima i predlozima zakona, gde su datumi činjenice slučaja ili jednokratni koraci. Model je pregledao 40 najjačih ukupno i 40 najjačih u propisima: u propisima su to prelazne odredbe koje su ispunile svrhu, namerni presečni datumi ili tekst koji je izrada repozitorijuma pogrešno pročitala.
- **Dvostruko numerisanje, ukinute valute, napomene izdavača:** pročitano ručno, ne modelom. To su lažni pogoci: „dm” su decimetri, a „DM” dijabetes, „dinara” opisuje današnje novčanice, a „brojevi” i „napomene” su engleski tekst međunarodnih ugovora ili pozivi na članove ponovljeni u obrazloženjima.

## Problemi pronađeni u ovom repozitorijumu

- **Izgubljeni eksponenti** u starijim pravilnicima: „dm³” piše kao „dm?” (na primer [pravilnik/1971/sfrj10-190/clan-039.md](https://github.com/lexifina/serbia-law/blob/542a099cd5a137d6bd315b1596b033ce44dcd54e/pravilnik/1971/sfrj10-190/clan-039.md)).
- **Tabele koje registar prikazuje kao slike** nedostaju u datotekama, što može da izgleda kao ukinut član (zakon o budžetu za 2020. iznad).
- **Verzije datirane danom primene iz registra** mogu da počnu pre nego što je objavljena izmena koja ih je donela (četiri otvorena slučaja iznad).

## Datoteke

| Datoteka | Šta sadrži |
| --- | --- |
| [data/flags.csv](data/flags.csv) | Sve oznake, jedan red po odredbi i problemu |
| [data/reviewed.csv](data/reviewed.csv) | 194 oznake koje je model pregledao, sa ocenom i obrazloženjem |
| [data/by_category.csv](data/by_category.csv) | Brojevi iz tabele iznad |
| [tools/](tools/) | Skripte kojima je provera urađena |

Kolone: `category` i `category_sr` (vrsta na engleskom i srpskom), `detector`, `kind` (`law` za propis ili `other`), `path` (datoteka u ovom repozitorijumu), `date` (datum na koji se oznaka odnosi), `reference` (propis ili red o kome je reč), `summary`, `score` (rangiranje detektora, od 0 do 1), `review` (`artefact` za grešku u podacima, `lawful` za zakonito ili `candidate_defect` za moguću grešku), `survives_rebuttal`, `review_note` (obrazloženje modela, na engleskom), `url` (odredba ili commit u stanju koje je pročitano).

## Kako je urađeno

- **Detektori:** [vulnerabilities/scripts](https://github.com/lexifina/global-law/tree/main/vulnerabilities/scripts) iz repozitorijuma global-law, pokrenuti nad ovim repozitorijumom na commitu `542a099`. global-law još ne ponavlja istoriju Srbije, pa je tabela istorije koju detektori čitaju napravljena iz trailera commitova ovog repozitorijuma (`Law`, `Kind`, `In-force`).
- **Pregled modelom:** gpt-5.4-mini, 40 najjačih oznaka po vrsti, a za istekle rokove i 40 najjačih u propisima; jedan prolaz ocenjuje da li je oznaka stvarna, drugi iznosi argumente da nije. Gde je oznaka pregledana dvaput, zadržan je kasniji pregled. Lista samog global-law napravljena je drugim modelom.
- **Ručna provera:** svaki slučaj koji je izdržao pregled pročitan je u istoriji i tekstovima ovog repozitorijuma. Za četiri otvorena datuma potreban je sam „Službeni glasnik”.

Ispravku možete prijaviti otvaranjem issue-a sa odredbom i zvaničnim izvorom.

## Licenca

Liste i napomene su doprinos Lexifine i stavljene su u javno vlasništvo pod licencom CC0 1.0, kao i ostali sopstveni doprinosi ovog repozitorijuma. Citirani tekst propisa je onakav kakav ga štampa zvanični registar; vidi [LICENSE](../LICENSE).

Ovo je prevod engleske verzije ([README.en.md](README.en.md)); ako se razlikuju, važi engleska verzija.
