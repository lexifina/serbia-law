"""Builds serbia-law's vulnerabilities/ folder from the Serbia-only run of global-law's detectors and model review.

    python -X utf8 build_serbia_vulns.py <out dir>

Inputs (from gl/vulnerabilities/scripts/): findings/run/*.parquet and *.jsonl, findings/run/triage.jsonl, pins.json.
Writes <out>/data/flags.csv, <out>/data/reviewed.csv, <out>/data/by_category.csv. The READMEs are written by hand.
"""
import csv, json, os, sys
from collections import Counter
import duckdb

HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.join(HERE, "gl", "vulnerabilities", "scripts")
RUN = os.path.join(SCR, "findings", "run")
OUT = sys.argv[1]
PIN = json.load(open(os.path.join(SCR, "pins.json"), encoding="utf-8"))["corpora"][0]["sha"]
BLOB = f"https://github.com/lexifina/serbia-law/blob/{PIN}/"
COMMIT = "https://github.com/lexifina/serbia-law/commit/"

CATS = {  # detector -> (English, Serbian) category, as in global-law's list
    "lapsed_limit": ("Lapsed time limits", "Istekli rokovi"),
    "repeal_gap": ("Repeal gaps", "Praznine posle ukidanja"),
    "same_day_conflict": ("Same-day conflicts", "Izmene istog dana"),
    "retroactive_date": ("Retroactive or pre-publication dates", "Datumi pre donošenja ili objavljivanja"),
    "dup_label": ("Duplicate numbering", "Dvostruko numerisanje"),
    "dead_currency": ("Dead currencies", "Ukinute valute"),
    "publisher_flag": ("Publisher notes", "Napomene izdavača"),
}
NOT_LAW = ("nacrt/", "predlog/", "sudska-praksa/", "kjn/", "zastitnik-gradjana/", "dri/", "rik/")


def kind_of(path: str) -> str:
    if not path:
        return "law"
    return "other" if path.startswith(NOT_LAW) else "law"


rows = []
con = duckdb.connect()


def pq(name):
    p = os.path.join(RUN, name).replace("\\", "/")
    return con.sql(f"select * from '{p}'").fetchall(), con.sql(f"select * from '{p}' limit 0").columns


r_, cols = pq("ranked_lapsed_limit.parquet")
for r in r_:
    d = dict(zip(cols, r))
    rows.append(dict(detector="lapsed_limit", path=d["path"], date=str(d["until"] or ""), reference=d.get("last_law") or "",
                     summary=(d.get("context") or "").replace("\n", " ")[:400], score=round(d["score"] or 0, 3)))
r_, cols = pq("ranked_repeal_gap.parquet")
for r in r_:
    d = dict(zip(cols, r))
    rows.append(dict(detector="repeal_gap", path=d["path"], date=str(d["removed_on"]), reference=f'{d["removed_by"]} -> {d["back_by"]}',
                     summary=f'removed {d["removed_on"]}, back {d["back_on"]} ({d["gap_days"]} days without text)', score=round(d["score"] or 0, 3)))
r_, cols = pq("ranked_same_day_conflict.parquet")
for r in r_:
    d = dict(zip(cols, r))
    rows.append(dict(detector="same_day_conflict", path=d["path"], date=str(d["in_force"]), reference="; ".join(d["laws"] or []),
                     summary=f'{d["n_laws"]} laws change it on {d["in_force"]}, made {d["spread_days"]} days apart', score=round(d["score"] or 0, 3)))
import subprocess
AUTHOR_COMMIT = {}
for line in subprocess.run(["git", "-C", os.path.join(SCR, "sources", "corpus", "serbia-law.git"), "log", "--format=%H%x09%an", PIN],
                           capture_output=True, text=True, encoding="utf-8").stdout.splitlines():
    sha, an = line.split("	", 1)
    AUTHOR_COMMIT.setdefault(an, sha)
r_, cols = pq("ranked_retroactive_date.parquet")
for r in r_:
    d = dict(zip(cols, r))
    first = AUTHOR_COMMIT.get(d["law"], "")
    rows.append(dict(detector="retroactive_date", path="", date=str(d["in_force"]), reference=d["law"],
                     summary=f'in force {d["in_force"]}, {d["made_field"].lower()} {d["made"]} ({d["back_days"]} days earlier): {d.get("subject") or ""}'[:400],
                     score=round(d["score"] or 0, 3), url=(COMMIT + first) if first else ""))
for det in ("dup_label", "dead_currency", "publisher_flag"):
    for line in open(os.path.join(RUN, f"{det}.jsonl"), encoding="utf-8"):
        d = json.loads(line)
        summ = (f'"{d.get("label")}" appears {d.get("n")} times' if det == "dup_label" else (d.get("text") or "").replace("\n", " ")[:300])
        rows.append(dict(detector=det, path=d["path"], date="", reference=str(d.get("line") or ""), summary=summ, score=""))

# the model review
rev = {}
TRIAGE = [os.path.join(RUN, "triage.jsonl"), os.path.join(os.path.dirname(RUN), "runlaw", "triage.jsonl")]  # all; law texts only
for line in (l for f in TRIAGE if os.path.exists(f) for l in open(f, encoding="utf-8")):
    d = json.loads(line)
    row = d["row"]
    key = (d["detector"], row.get("path") or row.get("law"), str(row.get("in_force") or row.get("removed_on") or row.get("until") or ""),
           (row.get("context") or "").replace("\n", " ")[:80] if d["detector"] == "lapsed_limit" else "")
    rev[key] = d
for r in rows:
    key = (r["detector"], r["path"] or r["reference"], r["date"], r["summary"][:80] if r["detector"] == "lapsed_limit" else "")
    d = rev.get(key)
    v = (d or {}).get("verify") or {}
    b = (d or {}).get("rebut") or {}
    r["review"] = v.get("verdict", "")
    r["review_note"] = v.get("reason", "")
    r["survives_rebuttal"] = "" if not b else ("yes" if b.get("survives") else "no")
    r["category"], r["category_sr"] = CATS[r["detector"]]
    r["kind"] = kind_of(r["path"])
    r.setdefault("url", BLOB + r["path"] if r["path"] else "")

os.makedirs(os.path.join(OUT, "data"), exist_ok=True)
fields = ["category", "category_sr", "detector", "kind", "path", "date", "reference", "summary", "score", "review", "survives_rebuttal", "review_note", "url"]
rows.sort(key=lambda r: (list(CATS).index(r["detector"]), r["kind"] != "law", -(r["score"] or 0) if r["score"] != "" else 0))
with open(os.path.join(OUT, "data", "flags.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
with open(os.path.join(OUT, "data", "reviewed.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
    w.writeheader()
    w.writerows([r for r in rows if r["review"]])
tot = Counter(r["detector"] for r in rows)
law = Counter(r["detector"] for r in rows if r["kind"] == "law")
revd = Counter(r["detector"] for r in rows if r["review"])
cand = Counter(r["detector"] for r in rows if r["review"] == "candidate_defect")
surv = Counter(r["detector"] for r in rows if r["survives_rebuttal"] == "yes")
with open(os.path.join(OUT, "data", "by_category.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["category", "category_sr", "flags", "in_law_texts", "model_reviewed", "candidate_defects", "survive_rebuttal"])
    for det, (en, sr) in CATS.items():
        w.writerow([en, sr, tot[det], law[det], revd[det], cand[det], surv[det]])
print(len(rows), "flags;", sum(revd.values()), "reviewed;", sum(cand.values()), "candidates;", sum(surv.values()), "survive")
for det, (en, sr) in CATS.items():
    print(f"{en:40s} {tot[det]:5d} law {law[det]:5d} rev {revd[det]:4d} cand {cand[det]:3d} surv {surv[det]:3d}")
