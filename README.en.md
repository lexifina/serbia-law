# Serbia: law history in git

**English** · **[Ili pročitajte na srpskom](README.md)**

<picture>
<source media="(prefers-color-scheme: dark)" srcset="data/effort-dark.svg">
<img alt="Serbian law in this repository: what it holds, changes by the year they took effect, completeness against the official sources, and the correctness of what is held" src="data/effort-light.svg" width="880">
</picture>

The law of Serbia as a git history: one file per provision, one commit per version on the day it took effect, and the act that made each change as the commit's author. `git blame` names the act behind every article; `git log` lists every change to an article; picking a date gives the text in force that day.

Part of [lexifina/global-law](https://github.com/lexifina/global-law), one git history for every country's law: this is Serbia's national law, which global-law reads at `serbia/national/acts/`.

**What is in it now:** the Constitution and 9,748 acts from the official register, with 13,507 versions; 4,034 local acts from 20 cities and municipalities; 12,000 court decisions (11,521 of them from the Constitutional Court); 1,384 bills and 178 draft acts, labelled as not law; and 489 decisions and reports of other public bodies. [`PLAN.md`](PLAN.md) lists every part this repository is meant to hold and how far each one is; [`registry/ACTS.md`](registry/ACTS.md) lists every act from the register, by kind.

Each act is in `<kind>/<year>/<Gazette number>-<page>/`, from its first publication (`zakon/2005/24-3/` is the Закон о раду, the Labour Law, "Службени гласник РС" 24/2005, page 3); acts first published in an earlier Gazette carry its name (`sfrj29-1181` is "Службени лист СФРЈ" 29/1978, page 1181). `registry/data/paths.json` maps each act id to its folder.

The text is in Serbian (Cyrillic, some acts Latin), as the official register prints it. An English translation is not part of this record.

## Questions as git commands

| Question | Command |
| --- | --- |
| Every change to Article 1 of the Labour Law | `git log -p --word-diff -- zakon/2005/24-3/clan-001.md` |
| Which act wrote each line of Article 1? | `git blame zakon/2005/24-3/clan-001.md` |
| Every version of the Labour Law, with the day each took effect | `git log --format="%h %(trailers:key=In-force,valueonly,separator=) %an" -- zakon/2005/24-3` |
| Article 1 in one of those versions | `git show <commit>:zakon/2005/24-3/clan-001.md` |

**Outside git**, we also host this record publicly, for free:

- **[Ask Claude about Serbian law](https://global-law.lexifina.com/v1/try_claude?country=serbia)**: opens Claude with a first question ready.
- **[Ask ChatGPT](https://global-law.lexifina.com/v1/try_chatgpt?country=serbia)**: the same question in ChatGPT.
- **[Call the API in your browser](https://global-law.lexifina.com/v1/search_law?query=godi%C5%A1nji+odmor&jurisdictions=serbia)**: a search of Serbian law for "godišnji odmor", returned as JSON. See the [documentation here](https://lexifina.com/api/global-law).

Both assistants read the record through the free Global law connector (MCP, `https://global-law.lexifina.com/mcp`); the first time, the chat gives you the link that adds it. Ask in Serbian, in Latin or Cyrillic letters, or in English.

**Host it yourself easily.** All it takes is git and Python, and the tools run on your machine:

```sh
git clone --depth 1 https://github.com/lexifina/global-law && cd global-law
python3 tools/countries.py add serbia/national/acts
python3 tools/law.py show 2026-01-01 serbia/national/acts/zakon/2005/24-3/clan-001.md
```

Opened in Claude Code, Cursor, VS Code or Codex, the clone also starts a local MCP server with the same tools ([MCP.md](https://github.com/lexifina/global-law/blob/main/MCP.md)).

## Dates

Each commit is dated at noon, Europe/Belgrade, on the day the version took effect, and carries it in its `In-force:` trailer:

- for an act with several versions, the register's own application day for each version (its version timeline);
- for an act the register keeps as one text, the register's ELI date for it, or the day the act's own in-force clause gives (or its last amendment's), counted from the Gazette day the text's header prints;
- for a single text with neither (most are decisions and notices with no in-force clause), the Gazette day of the last publication the text includes, as its header prints it. Every such version says so in a note in its commit message ("The register keeps only this text and gives no day it took effect ..."), and its part file's decisions say which rule gave the day.

The first version of an act is credited to its original publication when it holds only that publication and its corrections; otherwise it is the "oldest version available", credited to the publisher and naming the publications it already includes.

## How current it is

- [FRESHNESS.en.md](FRESHNESS.en.md): how current each source is, source by source, and how global-law sees this repository
- [WATCHING.en.md](WATCHING.en.md): every official source watched for Serbia, what is read on it and when it was last read
- [monitoring/](monitoring/README.en.md): the state of this repository (latest commits, what arrived, what is paused)

## How it is checked

- Every version is the register's own consolidated text for that version, with the register's change notes (not law text) left out; the units re-join to the register's text line for line.
- Every act is read back from git on the day each version took effect and on the day before, and must match the corpus; only checked batches are pushed. Results are in `registry/REPRODUCE.md`.
- History is append-only: no merge commits, no rewriting, no commit dated in the future, and every commit's trailers parse.
- [vulnerabilities/](vulnerabilities/README.en.md): possible drafting mistakes in Serbian law, found by global-law's detectors and checked by hand.

## What it does not show

- **Acts no longer in force.** The register lists acts in force; earlier texts of an act are here where the register keeps them as versions. Repealed acts and texts as first published are planned from the Службени гласник archive (see `PLAN.md`).
- **Images** (forms, tables, formulas drawn as pictures) are not in the files; versions whose text holds them say so.
- **Local acts, case law, treaties' own Gazette texts, bills and drafts** are planned parts (see `PLAN.md`).

## Sources

| Source | Kind | Past versions | Notes |
| --- | --- | --- | --- |
| [Pravno-informacioni sistem Republike Srbije](https://pravno-informacioni-sistem.rs) | Official register (Службени гласник) | yes, a version timeline per act | The text of every version, its application day and the Gazette publications it includes |

## Licence

See `LICENSE`.

This repository is not legal advice and not an official publication. No AI model wrote or changed legal text; scripts were written by an AI model (see `REPRODUCE.md` and `registry/REPRODUCE.md`).

## Visualisations

[visualisations/](visualisations/): Serbian law in 20 charts, drawn from this repository: what the National Assembly passes and who lends to Serbia, what the statute book is made of and how often it changes, constitutional complaints, appeals to the Information Commissioner over administrative silence, the State Audit Institution's recommendations and Belgrade's Official Gazette. Open [srpsko-pravo-u-20-grafikona.html](visualisations/srpsko-pravo-u-20-grafikona.html) in a browser; [visualisations/README.en.md](visualisations/README.en.md) shows every chart as an image.

## More

From [lexifina/global-law](https://github.com/lexifina/global-law):

- [FEATURES.md](https://github.com/lexifina/global-law/blob/main/FEATURES.md): every feature, and what every corpus must support (`git blame`, `law.py`, the MCP tools)
- [FAQ.md](https://github.com/lexifina/global-law/blob/main/FAQ.md): questions and answers · [CONTRIBUTING.md](https://github.com/lexifina/global-law/blob/main/CONTRIBUTING.md): proposing changes · [MCP.md](https://github.com/lexifina/global-law/blob/main/MCP.md): the MCP server · [REPRODUCE.md](https://github.com/lexifina/global-law/blob/main/REPRODUCE.md): how it was built · [CHANGELOG.md](https://github.com/lexifina/global-law/blob/main/CHANGELOG.md)
- [FRESHNESS.md](https://github.com/lexifina/global-law/blob/main/FRESHNESS.md): how current each corpus is · [Monitoring](https://github.com/lexifina/global-law/tree/main/monitoring): whether updates are running · [WATCHING.md](https://github.com/lexifina/global-law/blob/main/WATCHING.md): how each official source is watched for changes
- [performance/](https://github.com/lexifina/global-law/tree/main/performance): how fast the tools are, measured
- [visualisations/](https://github.com/lexifina/global-law/tree/main/visualisations): charts and bridges across the world's law
- [Vulnerabilities](https://github.com/lexifina/global-law/tree/main/vulnerabilities): mistakes in legislation as published
