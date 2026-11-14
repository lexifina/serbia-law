# Ranjivosti u propisima Srbije

**Srpski** · [English](README.en.md)

Detektori ranjivosti iz repozitorijuma [lexifina/global-law](https://github.com/lexifina/global-law/tree/main/vulnerabilities) traže mehaničke greške u propisima: pravilo koje se i dalje primenjuje „do” datuma koji je prošao, odredbu ukinutu pre nego što je njena zamena stupila na snagu, dve izmene iste odredbe istog dana, pravilo koje važi pre nego što je objavljeno. Lista koju je global-law objavio (9. novembra 2026) još nije obuhvatala Srbiju, pa je ovo provera samo ovog repozitorijuma, u stanju na commitu [`542a099`](https://github.com/lexifina/serbia-law/commit/542a099cd5a137d6bd315b1596b033ce44dcd54e) od 14. novembra 2026.

**Ukratko:** detektori su označili 3.154 mesta. Jezički model je pregledao 194 najjača, i za svako izneo argumente za i protiv; 17 je izdržalo proveru. Pregledano ručno u ovom repozitorijumu, nijedno nije potvrđena greška u pravu Srbije. Osam potiče od načina na koji registar datira verzije ili od načina na koji je ovaj repozitorijum napravljen, pet je zakonito, jedno je istekla prelazna odredba, a tri uopšte nisu propisi. Kasnije će ovo biti formalizovano u Lean-u, slično našem radu na [poreskom zakoniku SAD](https://lexifina.com/blog/formalizing-the-us-tax-code) i [sudskoj praksi SAD](https://lexifina.com/blog/formalizing-all-us-case-law-in-lean).

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

## Granični slučajevi

17 oznaka koje su izdržale pregled modelom, svaka ručno proverena, grupisane prema tome šta su se ispostavile: [EDGE-CASES.md](EDGE-CASES.md).

## Šta su ostale oznake

- **Istekli rokovi:** 1.727 od 2.151 nalazi se u odlukama o javnim nabavkama, obrazloženjima, nacrtima i predlozima zakona, gde su datumi činjenice slučaja ili jednokratni koraci. Model je pregledao 40 najjačih ukupno i 40 najjačih u propisima: u propisima su to prelazne odredbe koje su ispunile svrhu, namerni presečni datumi ili tekst koji je izrada repozitorijuma pogrešno pročitala.
- **Dvostruko numerisanje, ukinute valute, napomene izdavača:** pročitano ručno, ne modelom. To su lažni pogoci: „dm” su decimetri, a „DM” dijabetes, „dinara” opisuje današnje novčanice, a „brojevi” i „napomene” su engleski tekst međunarodnih ugovora ili pozivi na članove ponovljeni u obrazloženjima.

## Problemi pronađeni u ovom repozitorijumu

- **Izgubljeni eksponenti** u starijim pravilnicima: „dm³” piše kao „dm?” (na primer [pravilnik/1971/sfrj10-190/clan-039.md](https://github.com/lexifina/serbia-law/blob/542a099cd5a137d6bd315b1596b033ce44dcd54e/pravilnik/1971/sfrj10-190/clan-039.md)).
- **Tabele koje registar prikazuje kao slike** nedostaju u datotekama, što može da izgleda kao ukinut član (zakon o budžetu za 2020. u [graničnim slučajevima](EDGE-CASES.md)).
- **Verzije datirane danom primene iz registra** mogu da počnu pre nego što je objavljena izmena koja ih je donela (četiri otvorena slučaja u [graničnim slučajevima](EDGE-CASES.md)).

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
