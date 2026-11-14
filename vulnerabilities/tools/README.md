# Tools

The scripts behind this Serbia-only run of global-law's vulnerability detectors. They run inside a copy of
[global-law/vulnerabilities/scripts](https://github.com/lexifina/global-law/tree/main/vulnerabilities/scripts) (Python 3.11+,
`pip install duckdb pyarrow`), with a bare clone of this repository at `sources/corpus/serbia-law.git` and a blobless bare
clone of global-law at `sources/global-law.git`, and a `pins.json` that names only serbia-law and its commit.

| Script | What it does |
| --- | --- |
| `run_serbia.sh` | Indexes the history and texts, runs the detectors that apply to Serbia |
| `add_root_serbia.py` | Adds Serbia's history rows from this repository's commit trailers (global-law does not replay Serbia yet), so the history detectors have input |
| `rerun.sh` | Runs the history and reference detectors again after that |
| `flags_chart.py` | Draws the chart at the top of the README (light and dark, English and Serbian; fonts embedded afterwards) |
| `build_serbia_vulns.py` | Builds `data/flags.csv`, `data/reviewed.csv` and `data/by_category.csv` from the findings and the model review |

The model review is global-law's `triage/triage.py` (`--per 40`), with `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL` and
`LLM_AUTH` set for an OpenAI-compatible Responses API.
