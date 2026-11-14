"""The "Flags by category" chart at the top of vulnerabilities/README*.md (light and dark, English and Serbian).

    python -X utf8 flags_chart.py <out dir>      -> <out>/flags-by-category[-dark][.sr].svg (fonts embedded afterwards)
"""
import csv, os, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROWS = list(csv.DictReader(open(os.path.join(HERE, "out", "data", "flags.csv"), encoding="utf-8")))
W = 880
SANS = "Manrope, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', ui-monospace, SFMono-Regular, Consolas, 'Liberation Mono', monospace"
PAL = {
    "light": dict(bg="#ffffff", border="#dfe5e1", fg="#14201a", muted="#5f6e66", law="#1a7f4b", other="#9fcdb2", soft="#f4f6f5"),
    "dark": dict(bg="#0c120f", border="#26332c", fg="#e9f2ec", muted="#93a69b", law="#3fbf7f", other="#2a6b4a", soft="#141c18"),
}
TXT = {
    "en": dict(title="3,154 flags in seven categories", law="In law texts", other="In drafts, bills, court decisions and reports",
               cats=["Lapsed time limits", "Repeal gaps", "Same-day conflicts", "Retroactive dates", "Duplicate numbering",
                     "Dead currencies", "Publisher notes"], thousands=",",
               tip="{cat}: {n} flags, {law} in law texts"),
    "sr": dict(title="3.154 oznake u sedam vrsta", law="U propisima", other="U nacrtima, predlozima zakona, sudskim odlukama i izveštajima",
               cats=["Istekli rokovi", "Praznine posle ukidanja", "Izmene istog dana", "Retroaktivni datumi", "Dvostruko numerisanje",
                     "Ukinute valute", "Napomene izdavača"], thousands=".",
               tip="{cat}: {n} oznaka, {law} u propisima"),
}
DET = ["lapsed_limit", "repeal_gap", "same_day_conflict", "retroactive_date", "dup_label", "dead_currency", "publisher_flag"]
tot = Counter(r["detector"] for r in ROWS)
law = Counter(r["detector"] for r in ROWS if r["kind"] == "law")


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def chart(mode, lang):
    c, L = PAL[mode], TXT[lang]
    num = lambda v: f"{v:,}".replace(",", L["thousands"])  # noqa: E731
    H = 104 + 7 * 30 + 18
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{SANS}">', "<!--fonts-->",
         f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="8" fill="{c["bg"]}" stroke="{c["border"]}"/>',
         f'<text x="28" y="42" font-size="18" font-weight="700" fill="{c["fg"]}">{esc(L["title"])}</text>',
         f'<rect x="28" y="62" width="10" height="10" rx="2" fill="{c["law"]}"/>',
         f'<text x="44" y="71" font-size="12" fill="{c["muted"]}">{esc(L["law"])}</text>']
    lx = 44 + len(L["law"]) * 6.9 + 22
    o += [f'<rect x="{lx:.0f}" y="62" width="10" height="10" rx="2" fill="{c["other"]}"/>',
          f'<text x="{lx + 16:.0f}" y="71" font-size="12" fill="{c["muted"]}">{esc(L["other"])}</text>']
    x0, x1 = 214, W - 90
    mx = max(tot.values())
    for i, d in enumerate(DET):
        y = 96 + i * 30
        wl = (x1 - x0) * law[d] / mx
        wo = (x1 - x0) * (tot[d] - law[d]) / mx
        tip = esc(L["tip"].format(cat=L["cats"][i], n=num(tot[d]), law=num(law[d])))
        o.append(f'<text x="28" y="{y + 12}" font-size="12.5" fill="{c["fg"]}">{esc(L["cats"][i])}</text>')
        o.append(f'<g><title>{tip}</title><rect x="{x0}" y="{y}" width="{max(3, wl):.1f}" height="16" rx="3" fill="{c["law"]}"/>'
                 + (f'<rect x="{x0 + wl + 2:.1f}" y="{y}" width="{max(3, wo - 2):.1f}" height="16" rx="3" fill="{c["other"]}"/>' if wo else "")
                 + "</g>")
        o.append(f'<text x="{x0 + wl + wo + 8:.1f}" y="{y + 12}" font-family="{MONO}" font-size="12" font-weight="600" fill="{c["fg"]}">{num(tot[d])}</text>')
    o.append("</svg>")
    return "\n".join(o) + "\n"


out = sys.argv[1]
os.makedirs(out, exist_ok=True)
for lang in ("en", "sr"):
    for mode in ("light", "dark"):
        name = f"flags-by-category{'-dark' if mode == 'dark' else ''}{'.sr' if lang == 'sr' else ''}.svg"
        open(os.path.join(out, name), "w", encoding="utf-8", newline="\n").write(chart(mode, lang))
        print(name)
