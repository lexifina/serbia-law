"""Compute the numbers behind "Srpsko pravo u 20 grafikona" (run by make.py).

    python prep.py <build dir>

Inputs in the build dir, written by make.py from the repository's git objects:
  commits.json  - every commit: author date, subject, body, trailers
  paths.json    - the act folders each commit touches
  actdirs.txt   - every act folder in the tree (<kind>/<year>/<number>)
  repo/data/... - bills-*.csv, local/beograd/acts-*.csv, registers/*
Output: <build dir>/data.json, with a "profile" (record counts, coverage) and one entry per chart (c01-c20; c10 uses c09).
"""
import collections, csv, datetime as dt, glob, json, os, re, statistics, sys

W = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '.build')
R = os.path.join(W, 'repo')
C = collections.Counter
DD = collections.defaultdict

CYR = dict(zip('абвгдђежзијклљмнњопрстћуфхцчџш',
               ['a','b','v','g','d','đ','e','ž','z','i','j','k','l','lj','m','n','nj','o','p','r','s','t','ć','u','f','h','c','č','dž','š']))
def lat(s):
    out = []
    for i, ch in enumerate(s):
        lo = ch.lower()
        if lo in CYR:
            t = CYR[lo]
            if ch != lo:
                nxt = s[i + 1] if i + 1 < len(s) else ''
                t = t.upper() if (len(t) > 1 and nxt and nxt.isupper()) else t[0].upper() + t[1:]
            out.append(t)
        else:
            out.append(ch)
    return ''.join(out)

rows = json.load(open(os.path.join(W, 'commits.json'), encoding='utf-8'))
PATHS = json.load(open(os.path.join(W, 'paths.json'), encoding='utf-8'))
def T(r, k, d=None):
    v = r['t'].get(k)
    return v[0] if v else d
def kind(r): return T(r, 'Kind', '')
def folder(r):
    p = PATHS.get(r['h']) or []
    return p[0] if p else ''
def day(s):
    try: return dt.date.fromisoformat(s[:10])
    except Exception: return None

OUT = {'profile': {}, 'charts': {}}
OUT['profile']['built'] = dt.date.today().isoformat()
OUT['profile']['head'] = os.environ.get('HEAD_SHA', '')
OUT['profile']['commits'] = len(rows)
OUT['profile']['kinds'] = C(kind(r) or 'other' for r in rows).most_common()

# ---------------------------------------------------------------- bills
BILLS = []
for f in sorted(glob.glob(os.path.join(R, 'data', 'bills-*.csv'))):
    BILLS += list(csv.DictReader(open(f, encoding='utf-8')))

LOAN_RX = re.compile(r'зајм|кредит|финансијск\w* уговор|уговор\w* о финансирању|финансирањ\w* пројект', re.I)
def bill_type(t):
    tl = t.lower()
    if 'гаранциј' in tl: return 'guarantee'
    if 'потврђивањ' in tl:
        return 'loan' if LOAN_RX.search(tl) else 'treaty'
    if 'буџет' in tl and ('завршн' in tl or 'буџету' in tl): return 'budget'
    if 'аутентичн' in tl: return 'interp'
    if re.search(r'изменам|измени|допунам|допуни', tl): return 'amend'
    return 'new'

adopted = [b for b in BILLS if b['status'] == 'adopted' and b['law_adopted']]
OUT['profile']['bills'] = {'filed': len(BILLS), 'adopted': len(adopted), 'in_procedure': sum(1 for b in BILLS if b['status'] != 'adopted'),
                           'first_filed': min(b['bill_date'] for b in BILLS if b['bill_date']), 'last_adopted': max(b['law_adopted'] for b in adopted)}

# 1. what the Assembly passes, by year and type
y_t = DD(C)
for b in adopted:
    y_t[int(b['law_adopted'][:4])][bill_type(b['bill_title'])] += 1
years = [y for y in sorted(y_t) if sum(y_t[y].values()) >= 40]
OUT['charts']['c01'] = {'years': years, 'types': ['amend', 'new', 'treaty', 'loan', 'guarantee', 'budget', 'interp'],
                        'rows': [{'y': y, **{k: y_t[y][k] for k in ['amend', 'new', 'treaty', 'loan', 'guarantee', 'budget', 'interp']}} for y in years],
                        'n': sum(sum(y_t[y].values()) for y in years)}

# 2. voting days
per_day = C(b['law_adopted'] for b in adopted)
days = sorted(per_day.items())
big = sorted(days, key=lambda x: -x[1])[:8]
types_on_day = DD(C)
for b in adopted: types_on_day[b['law_adopted']][bill_type(b['bill_title'])] += 1
OUT['charts']['c02'] = {'days': [{'d': d, 'n': n, 't': dict(types_on_day[d])} for d, n in days],
                        'big': [d for d, _ in big], 'n_days': len(days), 'n_laws': sum(per_day.values()),
                        'share_10plus': round(sum(n for _, n in days if n >= 10) / sum(per_day.values()), 3)}

# 3. filing to adoption, by convocation
lag = DD(list)
for b in adopted:
    if not b['bill_date']: continue
    d = (dt.date.fromisoformat(b['law_adopted']) - dt.date.fromisoformat(b['bill_date'])).days
    if d < 0: continue
    lag[int(b['convocation'])].append((d, bill_type(b['bill_title'])))
CONV = {8: '2008–2012', 9: '2012–2014', 10: '2014–2016', 11: '2016–2020', 12: '2020–2022', 13: '2022–2024', 14: '2024–'}
c03 = []
for c in sorted(lag):
    if c not in CONV or len(lag[c]) < 50: continue
    v = sorted(d for d, _ in lag[c])
    q = statistics.quantiles(v, n=4)
    c03.append({'c': c, 'span': CONV[c], 'n': len(v), 'med': statistics.median(v), 'q1': q[0], 'q3': q[2],
                'p90': statistics.quantiles(v, n=10)[8], 'le7': sum(1 for d in v if d <= 7), 'le14': sum(1 for d in v if d <= 14),
                'pts': [d for d, _ in lag[c]]})
OUT['charts']['c03'] = c03

# 4. lenders
LENDERS = [
    ('wb', r'Међународн\w* банк\w* за обнову и развој|Међународн\w* удружењ\w* за развој|Светск\w* банк'),
    ('ebrd', r'Европск\w* банк\w* за обнову и развој'),
    ('eib', r'Европск\w* инвестицион'),
    ('ceb', r'Банк\w* за развој Савета Европе|Развојн\w* банк\w* Савета Европе'),
    ('kfw', r'KfW|KFW|KFV|КфВ|КФВ|Кредитанштал|Kreditanstalt'),
    ('china', r'Export.?Import|Еxport|Експорт.?импорт|Кин'),
    ('uae', r'Абу Даби|Емират'),
    ('russia', r'Руск\w* Федерациј'),
    ('azer', r'Азербејџан'),
    ('afd', r'Француск\w* агенциј\w* за развој'),
    ('kuwait', r'Кувајт'),
    ('commercial', r'J\.?P\.? ?Morgan|Citi|HSBC|Société|Deutsche|UniCredit|Intesa|Raiffeisen|Erste|OTP|Credit Suisse|BNP|Goldman|Ziraat|Denizbank'),
    ('hungary', r'Мађарск'), ('italy', r'Италиј'), ('turkey', r'Турск'), ('japan', r'Јапан|JICA'), ('saudi', r'Саудијск'),
]
lend = DD(C); unk = []
for b in adopted:
    t = b['bill_title']
    if bill_type(t) != 'loan': continue
    y = int(b['law_adopted'][:4])
    for key, rx in LENDERS:
        if re.search(rx, t):
            lend[key][y] += 1; break
    else:
        lend['other'][y] += 1; unk.append(t)
OUT['charts']['c04'] = {'lenders': [{'k': k, 'total': sum(v.values()), 'by': dict(v)} for k, v in sorted(lend.items(), key=lambda kv: -sum(kv[1].values()))],
                        'years': years, 'other_examples': [lat(t)[:160] for t in unk[:6]]}

# 5. treaty partners
PARTNERS = [
    ('Russia', 'Руск\\w* Федерациј', 'east'), ('China', 'Кин[ае]|Кинеск', 'asia'), ('Hungary', 'Мађарск', 'eu'),
    ('Republika Srpska', 'Републик\\w* Српск', 'wb'), ('Montenegro', 'Црн\\w* Гор', 'wb'), ('Bosnia and Herzegovina', 'Босн\\w* и Херцеговин', 'wb'),
    ('North Macedonia', 'Македониј', 'wb'), ('Croatia', 'Хрватск', 'eu'), ('Slovenia', 'Словениј', 'eu'), ('Albania', 'Албаниј', 'wb'),
    ('Romania', 'Румуниј', 'eu'), ('Bulgaria', 'Бугарск', 'eu'), ('Greece', 'Грчк|Хеленск', 'eu'), ('Cyprus', 'Кипар|Кипр', 'eu'),
    ('Austria', 'Аустриј', 'eu'), ('Germany', 'Немачк', 'eu'), ('France', 'Француск', 'eu'), ('Italy', 'Италиј', 'eu'),
    ('Slovakia', 'Словачк', 'eu'), ('Czechia', 'Чешк', 'eu'), ('Poland', 'Пољск', 'eu'), ('Spain', 'Шпаниј', 'eu'),
    ('Portugal', 'Португал', 'eu'), ('Belgium', 'Белгиј', 'eu'), ('Netherlands', 'Холандиј|Низоземск', 'eu'),
    ('Luxembourg', 'Луксембург', 'eu'), ('Denmark', 'Данск', 'eu'), ('Sweden', 'Шведск', 'eu'), ('Finland', 'Финск', 'eu'),
    ('Ireland', 'Ирск', 'eu'), ('Malta', 'Малт', 'eu'), ('Estonia', 'Естониј', 'eu'), ('Latvia', 'Летониј', 'eu'), ('Lithuania', 'Литваниј', 'eu'),
    ('Switzerland', 'Швајцарск', 'europe'), ('Norway', 'Норвешк', 'europe'), ('United Kingdom', 'Велик\\w* Британиј|Уједињен\\w* Краљевств', 'europe'),
    ('Turkey', 'Турск', 'europe'), ('Ukraine', 'Украјин', 'east'), ('Belarus', 'Белорус', 'east'), ('Moldova', 'Молдав', 'east'),
    ('Azerbaijan', 'Азербејџан', 'east'), ('Kazakhstan', 'Казахстан', 'east'), ('Uzbekistan', 'Узбекистан', 'east'), ('Georgia', 'Грузиј', 'east'),
    ('Armenia', 'Јермениј', 'east'), ('Kyrgyzstan', 'Киргиз', 'east'), ('Tajikistan', 'Таџикистан', 'east'), ('Turkmenistan', 'Туркменистан', 'east'),
    ('Mongolia', 'Монголиј', 'asia'), ('India', 'Индиј', 'asia'), ('Indonesia', 'Индонезиј', 'asia'), ('Japan', 'Јапан', 'asia'),
    ('South Korea', 'Кореј', 'asia'), ('Vietnam', 'Вијетнам', 'asia'), ('Singapore', 'Сингапур', 'asia'), ('Thailand', 'Тајланд', 'asia'),
    ('Malaysia', 'Малезиј', 'asia'), ('Philippines', 'Филипин', 'asia'), ('Sri Lanka', 'Шри Ланк', 'asia'), ('Pakistan', 'Пакистан', 'asia'),
    ('Iran', 'Иран', 'asia'), ('Iraq', 'Ирак', 'asia'), ('Israel', 'Израел', 'asia'), ('Palestine', 'Палестин', 'asia'),
    ('United Arab Emirates', 'Уједињен\\w* Арапск\\w* Емират|Абу Даби', 'asia'), ('Qatar', 'Катар', 'asia'), ('Saudi Arabia', 'Саудијск', 'asia'),
    ('Kuwait', 'Кувајт', 'asia'), ('Oman', 'Оман', 'asia'), ('Bahrain', 'Бахреин', 'asia'), ('Jordan', 'Јордан', 'asia'), ('Lebanon', 'Либан', 'asia'),
    ('Egypt', 'Египт|Арапск\\w* Републик\\w* Египат', 'africa'), ('Tunisia', 'Тунис', 'africa'), ('Morocco', 'Мароко|Мароканск', 'africa'),
    ('Algeria', 'Алжир', 'africa'), ('Angola', 'Анголе|Анголск', 'africa'), ('Ghana', 'Гане|Гана', 'africa'), ('Nigeria', 'Нигериј', 'africa'),
    ('Ethiopia', 'Етиопиј', 'africa'), ('Kenya', 'Кениј', 'africa'), ('South Africa', 'Јужноафричк', 'africa'), ('Zambia', 'Замбиј', 'africa'),
    ('Zimbabwe', 'Зимбабве', 'africa'), ('Senegal', 'Сенегал', 'africa'), ('Uganda', 'Уганд', 'africa'), ('Tanzania', 'Танзаниј', 'africa'),
    ('Mozambique', 'Мозамбик', 'africa'), ('Cuba', 'Куб[ае]|Кубанск', 'americas'), ('United States', 'Сједињен\\w* Америчк', 'americas'),
    ('Brazil', 'Бразил', 'americas'), ('Argentina', 'Аргентин', 'americas'), ('Mexico', 'Мексик', 'americas'), ('Chile', 'Чиле', 'americas'),
    ('Venezuela', 'Венецуел', 'americas'), ('Canada', 'Канад', 'americas'), ('Nicaragua', 'Никарагв', 'americas'), ('Peru', 'Перу', 'americas'),
    ('Uruguay', 'Уругвај', 'americas'), ('Colombia', 'Колумбиј', 'americas'), ('Australia', 'Аустралиј', 'americas'),
    ('Holy See', 'Свет\\w* Столиц', 'europe'), ('San Marino', 'Сан Марин', 'europe'), ('Monaco', 'Монак', 'europe'), ('Liechtenstein', 'Лихтенштај', 'europe'),
    ('Iceland', 'Исланд', 'europe'),
    ('European Union', 'Европск\\w* униј|Европск\\w* заједниц|Европск\\w* комисиј', 'multi'),
    ('Council of Europe', 'Савет\\w* Европе', 'multi'), ('United Nations', 'Уједињених нација|УНИЦЕФ|UNDP|УНДП', 'multi'),
]
part = C(); part_years = DD(C); n_treaty = 0; n_matched = 0
for b in adopted:
    t = b['bill_title']
    if bill_type(t) != 'treaty': continue
    n_treaty += 1
    hits = set()
    for name, rx, grp in PARTNERS:
        if name == 'Council of Europe' and re.search('Банк\\w* за развој Савета Европе', t): continue
        if re.search(rx, t): hits.add(name)
    if hits: n_matched += 1
    for h in hits:
        part[h] += 1; part_years[h][int(b['law_adopted'][:4])] += 1
grp = {n: g for n, _, g in PARTNERS}
OUT['charts']['c05'] = {'partners': [{'name': n, 'g': grp[n], 'n': c, 'by': dict(part_years[n])} for n, c in part.most_common(30)],
                        'n_treaty': n_treaty, 'n_matched': n_matched, 'n_partners': len(part)}

# ---------------------------------------------------------------- the statute book
as_adopted = {b['law_path'] for b in BILLS if b['law_in_repo'] == 'as-adopted' and b['law_path']}
actdirs = [l.strip() for l in open(os.path.join(W, 'actdirs.txt'), encoding='utf-8') if l.strip()]
acts = [a for a in actdirs if a not in as_adopted]
OUT['profile']['acts_in_tree'] = len(acts)
OUT['profile']['as_adopted'] = len([a for a in actdirs if a in as_adopted])
MAKER = {'zakon': 'assembly', 'ustav': 'assembly', 'poslovnik': 'assembly',
         'uredba': 'government', 'zakljucak': 'government', 'strategija': 'government', 'program': 'government', 'plan': 'government',
         'pravilnik': 'ministries', 'naredba': 'ministries', 'uputstvo': 'ministries', 'metodologija': 'ministries',
         'odluka': 'decisions', 'resenje': 'decisions',
         'sporazum': 'treaties', 'memorandum': 'treaties', 'protokol': 'treaties', 'konvencija': 'treaties', 'ugovor': 'treaties',
         }
kinds = C(a.split('/')[0] for a in acts)
OUT['charts']['c06'] = {'kinds': [{'k': k, 'n': n, 'm': MAKER.get(k, 'other')} for k, n in kinds.most_common()], 'n': len(acts)}

# 7. layers: year of the act's original gazette, by state
def state_of(a):
    k, y, num = a.split('/')[:3]
    y = int(y)
    pre = re.match(r'[a-z]*', num).group(0)
    if pre == 'fnrj': return 'fnrj'
    if pre == 'sfrj': return 'sfrj'
    if pre == 'srs': return 'srs'
    if pre == 'srj': return 'srj'
    if pre == 'scg': return 'scg'
    if pre == 'mu': return 'mu'
    return 'rs'
lay = DD(C)
for a in acts:
    if a.startswith('ustav/'): continue
    y = int(a.split('/')[1])
    lay[y][state_of(a)] += 1
OUT['charts']['c07'] = {'rows': [{'y': y, **lay[y]} for y in sorted(lay)], 'states': ['fnrj', 'sfrj', 'srs', 'srj', 'scg', 'rs', 'mu'],
                        'tot': dict(C(state_of(a) for a in acts if not a.startswith('ustav/'))),
                        'pre1992': sum(1 for a in acts if not a.startswith('ustav/') and int(a.split('/')[1]) < 1992)}

# 8. vacatio legis (as enacted texts)
vac = DD(lambda: DD(C))
vac_all = C()
for r in rows:
    if kind(r) != 'law': continue
    if 'as enacted' not in r['body'][:600] and 'as enacted' not in r['subj']: continue
    p, f = day(T(r, 'Published', '')), day(T(r, 'In-force', ''))
    if not p or not f: continue
    k = folder(r).split('/')[0]
    if k not in ('zakon', 'uredba', 'pravilnik', 'odluka'): continue
    d = (f - p).days
    b = 'same' if d <= 0 else 'next' if d == 1 else 'early' if d < 8 else 'eighth' if d == 8 else 'later'
    vac[k][p.year][b] += 1
    vac_all[b] += 1
c08 = {}
for k in ('zakon', 'uredba', 'pravilnik', 'odluka'):
    c08[k] = [{'y': y, **vac[k][y], 'n': sum(vac[k][y].values())} for y in range(2009, 2027) if sum(vac[k][y].values()) >= 8]
OUT['charts']['c08'] = {'by': c08, 'all': dict(vac_all)}

# 9/10. amendment history of laws in force: gazette issues that changed each act
GZ = re.compile(r'Службени (?:гласник|лист) (?:РС|СРЈ|СФРЈ|ФНРЈ|СРС|СЦГ)(?: - Међународни уговори)? (\d+)/(\d{4})')
issue_date = {}
for r in rows:
    if kind(r) not in ('law', 'court'): continue
    m = GZ.search(T(r, 'Law', '') or '')
    p = T(r, 'Published')
    if m and p and 'РС' in m.group(0) and 'Међународни' not in m.group(0):
        issue_date.setdefault((int(m.group(2)), int(m.group(1))), p)
by_year_max = DD(int)
for (y, n) in issue_date: by_year_max[y] = max(by_year_max[y], n)
def gz_date(y, n):
    if (y, n) in issue_date: return issue_date[(y, n)], True
    known = sorted((nn, issue_date[(yy, nn)]) for (yy, nn) in issue_date if yy == y)
    lo = [k for k in known if k[0] < n]; hi = [k for k in known if k[0] > n]
    if lo and hi:
        (n0, d0), (n1, d1) = lo[-1], hi[0]
        d0, d1 = dt.date.fromisoformat(d0), dt.date.fromisoformat(d1)
        return (d0 + (d1 - d0) * (n - n0) / (n1 - n0)).isoformat(), False
    return dt.date(y, 7, 1).isoformat(), False

hist = DD(set); titles = {}
for r in rows:
    k = kind(r)
    if k not in ('law', 'publisher', 'court'): continue
    f = folder(r)
    if not f.startswith('zakon/'): continue
    if T(r, 'Act'): titles.setdefault(f, T(r, 'Act'))
    texts = [T(r, 'Law', '') or ''] + r['t'].get('Also-amended-by', [])
    if k == 'publisher': texts.append(r['body'])
    for tx in texts:
        for m in GZ.finditer(tx):
            if 'РС' not in m.group(0) or 'Међународни' in m.group(0): continue
            hist[f].add((int(m.group(2)), int(m.group(1))))
ranked = sorted(((len(v), f) for f, v in hist.items() if f in titles), reverse=True)
top = []
for n, f in ranked[:25]:
    t = titles[f]
    ev = sorted(hist[f])
    pts = []
    for y, num in ev:
        d, exact = gz_date(y, num)
        pts.append({'g': f'{num}/{y}', 'd': d, 'x': exact})
    top.append({'f': f, 't': lat(t), 'n': n, 'first': ev[0][0], 'pts': pts})
OUT['charts']['c09'] = {'top': top, 'n_laws': len(hist), 'median': statistics.median(len(v) for v in hist.values()),
                        'dist': dict(C(min(len(v), 30) for v in hist.values()))}

# 11. the legal year: changes in force by month (amendment texts, 2016-2025)
mon = DD(C); jan1 = C(); tot = C()
for r in rows:
    if kind(r) != 'law': continue
    if 'as enacted' in r['body'][:600]: continue
    f = day(T(r, 'In-force', ''))
    if not f or not (2016 <= f.year <= 2025): continue
    mon[f.year][f.month] += 1
    tot[f.year] += 1
    if f.month == 1 and f.day == 1: jan1[f.year] += 1
OUT['charts']['c11'] = {'rows': [{'y': y, 'm': [mon[y][m] for m in range(1, 13)], 'jan1': jan1[y], 'n': tot[y]} for y in range(2016, 2026)]}

# ---------------------------------------------------------------- Constitutional Court
dec = [r for r in rows if kind(r) == 'decision' and T(r, 'Court') == 'Уставни суд']
uz = [r for r in dec if (T(r, 'Case', '') or '').startswith('Уж')]
def outcome(o):
    o = o or ''
    if o.startswith('Одлука о усвајању'): return 'granted'
    if o.startswith('Одлука о одбијању'): return 'rejected'
    if 'одбацивању' in o: return 'dismissed'
    return 'other'
oy = DD(C)
for r in uz:
    y = int(T(r, 'Decided', '0000')[:4] or 0)
    oy[y][outcome(T(r, 'Outcome'))] += 1
OUT['profile']['cc'] = {'decisions': len(dec), 'uz': len(uz), 'full_text': sum(1 for r in dec if not T(r, 'Text')),
                        'first': min(T(r, 'Decided') for r in dec if T(r, 'Decided')), 'last': max(T(r, 'Decided') for r in dec if T(r, 'Decided'))}
OUT['charts']['c12'] = {'rows': [{'y': y, **oy[y]} for y in sorted(oy) if y >= 2008 and sum(oy[y].values()) >= 10],
                        'tot': dict(C(outcome(T(r, 'Outcome')) for r in uz))}

# 13. rights invoked
ART = {'21': ('Zabrana diskriminacije', 'Prohibition of discrimination'), '22': ('Zaštita ljudskih i manjinskih prava', 'Protection of human and minority rights'),
       '27': ('Pravo na slobodu i bezbednost', 'Right to liberty and security'), '30': ('Pritvor', 'Detention'), '31': ('Trajanje pritvora', 'Length of detention'),
       '32': ('Pravo na pravično suđenje', 'Right to a fair trial'), '33': ('Posebna prava okrivljenog', 'Rights of the accused'),
       '34': ('Pravna sigurnost u kaznenom pravu', 'Legal certainty in criminal law'), '35': ('Pravo na rehabilitaciju i naknadu štete', 'Rehabilitation and compensation'),
       '36': ('Jednaka zaštita prava i pravno sredstvo', 'Equal protection of rights and legal remedy'), '39': ('Sloboda kretanja', 'Freedom of movement'),
       '42': ('Zaštita podataka o ličnosti', 'Protection of personal data'), '46': ('Sloboda mišljenja i izražavanja', 'Freedom of thought and expression'),
       '51': ('Pravo na obaveštenost', 'Right to information'), '58': ('Mirno uživanje imovine', 'Peaceful enjoyment of property'),
       '59': ('Pravo nasleđivanja', 'Right of inheritance'), '60': ('Pravo na rad', 'Right to work'), '64': ('Prava deteta', 'Rights of the child'),
       '65': ('Prava i dužnosti roditelja', 'Rights and duties of parents'), '66': ('Posebna zaštita porodice', 'Protection of the family'),
       '68': ('Zdravstvena zaštita', 'Health care'), '69': ('Socijalna zaštita', 'Social protection'), '70': ('Penzijsko osiguranje', 'Pension insurance'),
       '76': ('Ravnopravnost nacionalnih manjina', 'Equality of national minorities'), '24': ('Pravo na život', 'Right to life'),
       '25': ('Nepovredivost fizičkog i psihičkog integriteta', 'Physical and mental integrity'), '23': ('Dostojanstvo', 'Human dignity')}
arts = DD(C)
for r in uz:
    seen = set()
    for p in r['t'].get('Provisions', []):
        for m in re.findall(r'Члан (\d+)', p):
            seen.add(m)
    o = outcome(T(r, 'Outcome'))
    for a in seen:
        arts[a]['n'] += 1; arts[a][o] += 1
with_art = sum(1 for r in uz if any(re.search(r'Члан \d+', p) for p in r['t'].get('Provisions', [])))
top_art = sorted(arts.items(), key=lambda kv: -kv[1]['n'])[:14]
OUT['charts']['c13'] = {'arts': [{'a': a, 'sr': ART.get(a, ('Član ' + a, 'Article ' + a))[0], 'en': ART.get(a, ('', 'Article ' + a))[1],
                                   'n': v['n'], 'granted': v['granted'], 'rejected': v['rejected'], 'dismissed': v['dismissed']} for a, v in top_art],
                        'with_art': with_art, 'uz': len(uz)}

# 14. waiting: filing year (case number) vs decision year
wait = C(); waits = DD(list)
for r in uz:
    m = re.search(r'/(\d{4})', T(r, 'Case', '') or '')
    dy = int((T(r, 'Decided', '') or '0000')[:4] or 0)
    if not m or not dy: continue
    fy = int(m.group(1))
    if fy < 2007 or dy < fy: continue
    wait[(fy, dy)] += 1
    waits[dy].append(dy - fy)
OUT['charts']['c14'] = {'cells': [{'f': f, 'd': d, 'n': n} for (f, d), n in sorted(wait.items())],
                        'med': {d: statistics.median(v) for d, v in waits.items() if len(v) >= 10},
                        'n': sum(wait.values())}

# 15. what is challenged
def challenged_group(c):
    s = c.strip()
    sl = s.lower()
    if re.match(r'^(поступ\w*|радње|пропушт)', sl) or 'поступак у току' in sl: return 'proceedings'
    m = re.match(r'^(?:пресуда|решење|одлука|закључак|наредба|рјешење)?\s*(?:\d+\s*)?([А-Яа-яЂђЈјЉљЊњЋћЏџ]+)', s, re.I)
    mark = (m.group(1) if m else '').lower()
    if mark.startswith('рж') or mark.startswith('р4') or mark in ('рр',): return 'reasonable_time'
    if mark.startswith('гж'): return 'civil_appeal'
    if mark.startswith('рев') or mark.startswith('прев') or mark.startswith('рж'): return 'revision'
    if mark in ('п', 'п1', 'п2', 'пл', 'пр', 'ст', 'о', 'р') : return 'civil_first'
    if mark.startswith('к') : return 'criminal'
    if mark.startswith('у') or mark.startswith('узп') : return 'administrative'
    if mark.startswith('и') or mark.startswith('ипв') : return 'enforcement'
    if mark.startswith('пж') or mark.startswith('пвж'): return 'commercial'
    if mark.startswith('пр') or mark.startswith('прж') or mark.startswith('пжп') or mark.startswith('ппж'): return 'misdemeanour'
    return 'other'
chg = DD(C)
for r in uz:
    cs = r['t'].get('Challenged', [])
    if not cs: continue
    g = challenged_group(cs[0])
    chg[g]['n'] += 1; chg[g][outcome(T(r, 'Outcome'))] += 1
OUT['charts']['c15'] = {'groups': [{'g': g, **v} for g, v in sorted(chg.items(), key=lambda kv: -kv[1]['n'])],
                        'n': sum(v['n'] for v in chg.values())}

# 16. general acts found unconstitutional / unlawful
def act_type(s):
    s = (s or '').strip().lower()
    for k, rx in [('law', r'^(закон|законик|уставни закон)'), ('regulation', r'^(уредб|правилник|наредб|упутств|одлук[аеу] влад)'),
                  ('statute', r'^(статут|пословник|колективн|правила)'), ('local', r'^(одлук|решењ|програм|план)')]:
        if re.match(rx, s): return k
    return 'other'
nc = DD(C); nc_list = []
for r in dec:
    if not (T(r, 'Outcome', '') or '').startswith('Одлука о утврђивању несагласности'): continue
    y = int((T(r, 'Decided', '') or '0000')[:4] or 0)
    ch = (r['t'].get('Challenged') or [''])[0]
    typ = act_type(ch)
    case = T(r, 'Case', '') or ''
    if case.startswith('IУл'): typ = 'local'
    nc[y][typ] += 1
    nc_list.append({'y': y, 'c': lat(case), 't': lat(ch)[:140], 'typ': typ})
OUT['charts']['c16'] = {'rows': [{'y': y, **nc[y]} for y in sorted(nc) if y >= 2008], 'n': len(nc_list),
                        'laws': sorted([x for x in nc_list if x['typ'] == 'law'], key=lambda x: -x['y'])[:40],
                        'tot': dict(C(x['typ'] for x in nc_list))}

# ---------------------------------------------------------------- Commissioner, audit, Belgrade
REG = os.path.join(R, 'data', 'registers')
z = list(csv.DictReader(open(os.path.join(REG, 'poverenik', 'zalbe-iz-oblasti-prava-na-pristup-informacijama.csv'), encoding='utf-8')))
GROUND = {'Žalba na ćutanje uprave': 'silence', 'Žalba na odgovor': 'answer', 'Žalba na zakljucak i rešenje': 'decision',
          'Žalba na rešenje': 'decision', 'Žalba na obaveštenje sa elementima odluke': 'notice', 'Žalba na troškove': 'costs'}
zy = DD(C)
for r in z:
    y = int(r['CreateDate'][:4])
    zy[y][GROUND.get(r['BasicOfStarting'], 'other')] += 1
OUT['profile']['poverenik'] = {'appeals': len(z), 'first': min(r['CreateDate'] for r in z), 'last': max(r['CreateDate'] for r in z)}
OUT['charts']['c17'] = {'rows': [{'y': y, **zy[y], 'n': sum(zy[y].values())} for y in sorted(zy)], 'n': len(z),
                        'silence': sum(v['silence'] for v in zy.values())}

AG = {'Gradski i opštinski organi i mesne zajednice': ('Organi gradova i opština', 'City and municipal bodies'),
      'Ustanove osnovnog i srednjeg obrazovanja': ('Osnovne i srednje škole', 'Primary and secondary schools'),
      'Ministarstva': ('Ministarstva', 'Ministries'), 'Republička javna preduzeća': ('Republička javna preduzeća', 'State-owned enterprises'),
      'Lokalna javna preduzeća': ('Lokalna javna preduzeća', 'Local public enterprises'),
      'Republičke agencije, direkcije, zavodi, fondovi i dr.': ('Republičke agencije, zavodi i fondovi', 'State agencies, institutes and funds'),
      'Pravosudni organi': ('Pravosudni organi', 'Courts and prosecutors'), 'Ustanove u oblasti zdravstva': ('Zdravstvene ustanove', 'Health institutions'),
      'Ustanove visokog obrazovanja': ('Visokoškolske ustanove', 'Universities and colleges'),
      'Ustanove u oblasti nauke, kulture i informisanja': ('Nauka, kultura i informisanje', 'Science, culture and media institutions'),
      'Ustanove socijalne zaštite': ('Ustanove socijalne zaštite', 'Social care institutions'),
      'Javne službe i druge organizacije lokalne samouprave': ('Javne službe lokalne samouprave', 'Local public services')}
ag = DD(C)
for r in z:
    g = r['AuthorityGroup']
    if g not in AG: g = 'other'
    ag[g]['n'] += 1
    if GROUND.get(r['BasicOfStarting']) == 'silence': ag[g]['silence'] += 1
OUT['charts']['c18'] = {'groups': [{'sr': AG.get(g, ('Ostali organi', 'Other bodies'))[0], 'en': AG.get(g, ('Ostali organi', 'Other bodies'))[1],
                                     'n': v['n'], 'silence': v['silence']} for g, v in sorted(ag.items(), key=lambda kv: -kv[1]['n'])],
                        'top': [{'a': a, 'n': n} for a, n in C(r['Authority'] for r in z if GROUND.get(r['BasicOfStarting']) == 'silence').most_common(12)]}

# 19. State Audit Institution recommendations
dri = []
for f in ('registar-preporuka-1.csv',):  # -2 is the same register again, without the audit-type column
    for r in csv.DictReader(open(os.path.join(REG, 'dri', f), encoding='utf-8')):
        st = next((v for k, v in r.items() if k and k.startswith('Статус')), '')
        dri.append({'who': r['Назив субјекта ревизије'], 'st': st, 'type': r.get('Врста ревизије', '')})
def auditee(w):
    wl = w.lower()
    if re.search(r'завршни рачун|консолидовани', wl): return 'state_accounts'
    if re.search(r'партиј|странк|покрет', wl): return 'party'
    if re.search(r'суд у|основни суд|виши суд|привредни суд|тужилаштв|затвор|казнено-поправн|окружни затвор', wl): return 'judiciary'
    if re.search(r' - го |^го |градска општина', wl): return 'local'
    if re.match(r'^(град|општина|градска општина)', wl) or 'општина' in wl[:20]: return 'local'
    if wl.startswith('министарство') or 'министарство' in wl: return 'ministry'
    if re.search(r'јавно предузеће|^јп |јкп|ј\.п\.|д\.о\.о|доо|а\.д\.|ад |предузеће', wl): return 'enterprise'
    if re.search(r'фонд|завод|агенциј|управа|дирекциј|институт|републички|републичка', wl): return 'agency'
    if re.search(r'а\. ?д\.|д\. ?o\. ?o|д\. ?о\. ?о|^кјп|^кјп|^нип|компанија', wl): return 'enterprise'
    if re.search(r'управни округ|служба|организациј|национална служба|академиј', wl): return 'agency'
    if re.search(r'^дом |дом за|клиник|радио телевизиј', wl): return 'institution'
    if re.search(r'школ|факултет|универзитет|дом здравља|болниц|клинич|здравствен|центар за социјални|установа|музеј|позориш|библиотек|вртић|предшколск', wl): return 'institution'
    if re.search(r'покрајин', wl): return 'province'
    if re.search(r'странк|покрет|савез', wl): return 'party'
    return 'other'
STS = {'Поступљено по препоруци': 'done', 'Делимично поступљено': 'partly', 'У току': 'ongoing', 'Није поступљено по препоруци': 'not', 'Није применљива': 'na'}
au = DD(C)
for d in dri:
    a = auditee(d['who']); au[a]['n'] += 1; au[a][STS.get(d['st'], 'na')] += 1
OUT['charts']['c19'] = {'groups': [{'g': g, **v} for g, v in sorted(au.items(), key=lambda kv: -kv[1]['n'])], 'n': len(dri),
                        'tot': dict(C(STS.get(d['st'], 'na') for d in dri)),
                        'not_top': [{'who': lat(w), 'n': n} for w, n in C(d['who'] for d in dri if STS.get(d['st']) == 'not').most_common(10)]}

# 20. Belgrade's gazette 2002-2014: who issues local law
lb = []
for f in glob.glob(os.path.join(R, 'data', 'local', 'beograd', 'acts-*.csv')):
    lb += list(csv.DictReader(open(f, encoding='utf-8')))
def issuer(s):
    if s == 'Акти Града': return 'Grad Beograd'
    m = re.match(r'Акти градских општина (.+)', s)
    if m: return lat(m.group(1))
    return None
hm = DD(C); kinds_bg = DD(C)
for r in lb:
    i = issuer(r['section'])
    if not i: continue
    y = int(r['date'][:4])
    hm[i][y] += 1
    w = r['title'].split()[0].lower() if r['title'] else ''
    t = 'plan' if 'план' in r['title'].lower()[:40] and 'регулациј' in r['title'].lower() else ('budget' if 'буџет' in r['title'].lower() else ('resenje' if w.startswith('решењ') else ('odluka' if w.startswith('одлук') else 'other')))
    kinds_bg[y][t] += 1
yrs = sorted({y for v in hm.values() for y in v})
OUT['charts']['c20'] = {'years': yrs, 'rows': [{'i': i, 'by': dict(v), 'n': sum(v.values())} for i, v in sorted(hm.items(), key=lambda kv: (kv[0] != 'Grad Beograd', -sum(kv[1].values())))],
                        'n': len(lb), 'plans': {y: kinds_bg[y]['plan'] for y in yrs}}
OUT['profile']['local'] = {'beograd_index': len(lb), 'local_texts': sum(1 for r in rows if kind(r) == 'local-act')}

json.dump(OUT, open(os.path.join(W, 'data.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('ok', os.path.getsize(os.path.join(W, 'data.json')))
