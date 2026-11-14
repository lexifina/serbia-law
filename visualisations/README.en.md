# Serbian law in 20 charts

[Srpski](README.md)

Charts on every country's law, from the whole of global-law: [global-law visualisations/](https://github.com/lexifina/global-law/tree/main/visualisations). These are the charts on Serbia alone.

Twenty charts on Serbian law, drawn only from the data in this repository: the acts of the Legal Information System, the National Assembly's bills, the Constitutional Court's case law, appeals to the Commissioner for Information of Public Importance, the State Audit Institution's recommendations and the Official Gazette of the City of Belgrade.

Open [`srpsko-pravo-u-20-grafikona.html`](srpsko-pravo-u-20-grafikona.html) in a browser. The page is one file with all its data inside; it loads only the d3 library and its fonts from the web. The controls at the top right switch the language (Serbian in Latin script, or English) and the theme (light or dark). Each chart names its data path in the repository, its record count and its limits, and has a table of every number under it. Hover over a mark for the exact values.

The charts are descriptive: they show what the sources record, not why.

## The charts

### I. The National Assembly

1. **What the Assembly passes.** Laws by year and type: amendments, new laws, treaty ratifications, loans, guarantees, budget.
   ![1](stills/en/01.png)
2. **Who lends to Serbia.** Laws ratifying loan agreements, by lender and year.
   ![2](stills/en/02.png)
3. **Who Serbia signs treaties with.** Ratification laws by the other contracting party.
   ![3](stills/en/03.png)
4. **Laws pass in bundles.** Every voting day and how many laws passed on it; two thirds of all laws pass on days with 10 or more.
   ![4](stills/en/04.png)
5. **From bill to law.** How many days a bill spends in the Assembly, by convocation.
   ![5](stills/en/05.png)

### II. The statute book

6. **Who writes the rules.** Acts in force by kind: laws are about one in six; the rest are rulebooks, decisions and decrees.
   ![6](stills/en/06.png)
7. **Yugoslav layers.** Acts in force that were published in the gazettes of the FPRY, SFRY, Socialist Republic of Serbia, FRY and Serbia and Montenegro.
   ![7](stills/en/07.png)
8. **Vacatio legis.** How many laws, decrees, rulebooks and decisions take effect before the eighth day after publication (Constitution, art. 196).
   ![8](stills/en/08.png)
9. **The most-changed laws.** The number of Official Gazette issues that changed the text, for 25 laws.
   ![9](stills/en/09.png)
10. **Lives of laws.** The same issues on a time axis.
    ![10](stills/en/10.png)
11. **The legal year.** Amendments by the month they took effect, 2016–2025.
    ![11](stills/en/11.png)

### III. The Constitutional Court

12. **Constitutional complaints in the published case law.** Decisions by year and outcome, and what the database actually shows.
    ![12](stills/en/12.png)
13. **Which rights complainants invoke.** The Constitution's articles cited in decisions and how many of those decisions granted the complaint.
    ![13](stills/en/13.png)
14. **How long a complaint waits.** The year filed (from the case number) against the year decided.
    ![14](stills/en/14.png)
15. **What is challenged.** The challenged act by court register; a fifth of complaints challenge proceedings still running or a ruling on a reasonable-time request.
    ![15](stills/en/15.png)
16. **When the Court says "not in conformity".** General acts found unconstitutional or unlawful, by year and kind.
    ![16](stills/en/16.png)

### IV. The administration under scrutiny

17. **Administrative silence.** Appeals to the Commissioner by year and ground; almost half are because the body never answered.
    ![17](stills/en/17.png)
18. **Who stays silent.** The share of appeals over silence, by type of body.
    ![18](stills/en/18.png)
19. **State Audit Institution recommendations.** The status of recommendations by type of audited body.
    ![19](stills/en/19.png)

### V. Belgrade

20. **Belgrade's Official Gazette.** Acts by issuer (the City and its 17 municipalities) and year, 2002–2014.
    ![20](stills/en/20.png)

## Data

As of commit `542a099cd5` (14 November 2026).

| Dataset | Where in the repository | Records | Coverage |
| --- | --- | ---: | --- |
| Git history | branch `main` | 31,883 commits | the commit date is the date of entry into force or of decision |
| Register acts | `<kind>/<year>/<number>/`, `registry/data/acts.json` | 9,835 acts | acts in force in the Legal Information System, the oldest from 1947 |
| Bills | `data/bills-*.csv` | 2,794 (2,296 passed) | 2007–2026, complete from 2011 |
| Constitutional Court | `sudska-praksa/ustavni-sud/` | 11,521 decisions (10,759 Už) | 2008–2026 |
| Appeals to the Commissioner | `data/registers/poverenik/` | 80,153 appeals | 2013–2026 |
| SAI recommendations | `data/registers/dri/registar-preporuka-1.csv` | 3,736 recommendations | status on 30 April 2026 |
| Belgrade Official Gazette | `data/local/beograd/` | 13,554 acts | 2002–2014 |

## Limits

- **The register records acts in force.** Repealed acts are not in it, so charts 6, 7 and 9 describe the law in force today, not everything ever enacted. For many acts the register has text only from the mid-2010s; earlier amendments are known only as a list of Official Gazette numbers.
- **The Constitutional Court's case-law database is a selection.** The Court does not publish every decision, so the share of granted complaints in it (chart 12) is not a success rate.
- **Types are read from titles.** The kind of law (chart 1), the lender (4), the treaty partner (5), the court register (15), the kind of challenged act (16) and the type of audited body (19) are read from title text by the rules in `src/prep.py`. Whatever the rules do not recognise is shown as "Other" and is visible in the table.
- **The bill list has no field for urgent procedure or for the sponsor.** Chart 3 measures only the time from filing to passage.
- **Partial years** (2026 for bills and appeals) are drawn lighter and labelled as such.

## Rebuilding

```sh
python visualisations/src/make.py            # git log + tables -> src/.build/ -> srpsko-pravo-u-20-grafikona.html
node visualisations/src/stills.cjs           # images for these READMEs (needs Playwright; PLAYWRIGHT=<path> if not global)
```

`make.py` reads everything from git objects, so it also works in a sparse or `--no-checkout` clone. It reads `origin/main` (or `HEAD`) by default; `--ref` picks another branch or commit. It writes nothing into the repository except the page and the `src/.build/` folder (which git ignores).

| File | What it does |
| --- | --- |
| `src/make.py` | extracts the history, act folders and tables into `src/.build/`, then runs `prep.py` and `build.py` |
| `src/prep.py` | computes every number for the 20 charts and the data profile into `src/.build/data.json` |
| `src/page.tpl.html` | the page: text in both languages, the charts (d3), the tables |
| `src/build.py` | puts `data.json` into the template and writes the page |
| `src/stills.cjs` | draws each chart as a PNG into `stills/sr/` and `stills/en/` |
