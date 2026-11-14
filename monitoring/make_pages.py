"""Write this repository's own WATCHING.md, FRESHNESS.md and monitoring/README.md (Serbian) and their .en.md copies.

    python monitoring/make_pages.py [--ref origin/main] [--today YYYY-MM-DD]

Everything is read from git: each commit's Source trailer names the official source it came from, its author date is
the day the text applies or the decision was given, and its committer date is the day this repository published it.
global-law's row for this corpus is read from global-law's data/freshness.tsv (skipped when offline).
"""
import argparse, collections, csv, datetime as dt, io, os, re, subprocess, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ap = argparse.ArgumentParser()
ap.add_argument('--ref', default=None)
ap.add_argument('--today', default=None)
a = ap.parse_args()

def git(*args):
    return subprocess.run(['git', '-C', ROOT, *args], check=True, capture_output=True).stdout.decode('utf-8', 'replace')

ref = a.ref or ('origin/main' if subprocess.run(['git', '-C', ROOT, 'rev-parse', '-q', '--verify', 'origin/main'], capture_output=True).returncode == 0 else 'HEAD')
head = git('rev-parse', ref).strip()
TODAY = dt.date.fromisoformat(a.today) if a.today else dt.datetime.now(dt.timezone.utc).date()
GL = 'https://github.com/lexifina/global-law/blob/main'
GLT = 'https://github.com/lexifina/global-law/tree/main'
CORPUS = 'serbia/national/acts'

# ------------------------------------------------------------------ sources
# domain -> (key, Serbian name, English name, what is read for new items, level)
SRC = [
    ('pravno-informacioni-sistem.rs', 'pis', 'Pravno-informacioni sistem RS (Službeni glasnik)', 'Legal Information System of Serbia (Official Gazette)',
     ('spisak važećih propisa po oblastima i vremenska linija verzija svakog propisa', 'the listing of acts in force by area and each act\'s timeline of versions'), 'national'),
    ('parlament.gov.rs', 'na', 'Narodna skupština', 'National Assembly',
     ('spisak predloga zakona po sazivu, usvojeni zakoni i sednice', 'the list of bills by convocation, the laws passed and the sittings'), 'national'),
    ('ustavni.sud.rs', 'us', 'Ustavni sud', 'Constitutional Court',
     ('baza sudske prakse', 'the case-law database'), 'courts'),
    ('kg.ap.sud.rs', 'apkg', 'Apelacioni sud u Kragujevcu', 'Court of Appeal in Kragujevac',
     ('sudska praksa na sajtu suda', 'the case law on the court\'s site'), 'courts'),
    ('kzk.gov.rs', 'kzk', 'Komisija za zaštitu konkurencije', 'Commission for Protection of Competition',
     ('spisak odluka', 'the list of decisions'), 'courts'),
    ('kjn.rs', 'kjn', 'Republička komisija za zaštitu prava u postupcima javnih nabavki', 'Republic Commission for the Protection of Rights in Public Procurement',
     ('arhiva odluka', 'the decisions archive'), 'courts'),
    ('ekonsultacije.gov.rs', 'ek', 'eKonsultacije', 'eKonsultacije (public consultations)',
     ('spisak javnih konsultacija', 'the list of public consultations'), 'national'),
    ('sllistbeograd.rs', 'bg', 'Službeni list Grada Beograda', 'Official Gazette of the City of Belgrade',
     ('arhiva brojeva lista', 'the archive of issues'), 'local'),
    ('skupstina.novisad.rs', 'ns', 'Službeni list Grada Novog Sada', 'Official Gazette of the City of Novi Sad',
     ('brojevi lista', 'the gazette\'s issues'), 'local'),
    ('kragujevac.ls.gov.rs', 'kg', 'Službeni list grada Kragujevca', 'Official Gazette of the City of Kragujevac',
     ('brojevi lista', 'the gazette\'s issues'), 'local'),
    ('rik.parlament.gov.rs', 'rik', 'Republička izborna komisija', 'Republic Electoral Commission',
     None, 'records'),
    ('ombudsman.rs', 'zg', 'Zaštitnik građana', 'Protector of Citizens (Ombudsman)', None, 'records'),
    ('srbija.gov.rs', 'vlada', 'Vlada Republike Srbije', 'Government of Serbia',
     ('dokumenti, strategije, programi i planovi', 'documents, strategies, programmes and plans'), 'records'),
    ('aers.rs', 'aers', 'Agencija za energetiku', 'Energy Agency', None, 'records'),
    ('sec.gov.rs', 'hov', 'Komisija za hartije od vrednosti', 'Securities Commission', None, 'records'),
    ('data.gov.rs', 'odp', 'Portal otvorenih podataka (data.gov.rs)', 'Open data portal (data.gov.rs)',
     ('stranice skupova podataka (Poverenik, DRI, Ministarstvo pravde, Zaštitnik građana)', 'the dataset pages (Commissioner, State Audit Institution, Ministry of Justice, Ombudsman)'), 'records'),
]
THRESH = {'national': 7, 'local': 30, 'courts': 30, 'records': 30}
NOTES = {'kjn': ('arhiva starog sajta komisije: odluke do 2011.', 'the archive of the commission\'s old site: decisions up to 2011'),
         'odp': ('broj je broj skupova podataka, ne komita', 'the count is datasets, not commits')}
PAUSED = {}  # source key -> (Serbian, English) reason, when a source is deliberately not re-read
KIND_SR = {'law': 'propisi', 'publisher': 'tekstovi izdavača', 'court': 'odluke Ustavnog suda u tekstu', 'law-as-adopted': 'zakoni kako su usvojeni',
           'draft': 'nacrti i predlozi', 'decision': 'sudske i druge odluke', 'local-act': 'lokalni akti', 'record': 'dokumenti i tabele'}
KIND_EN = {'law': 'acts', 'publisher': 'publisher texts', 'court': 'Constitutional Court rulings in the text', 'law-as-adopted': 'laws as adopted',
           'draft': 'drafts and bills', 'decision': 'court and other decisions', 'local-act': 'local acts', 'record': 'documents and tables'}

def src_of(url):
    host = re.sub(r'^https?://', '', url).split('/')[0].lower()
    for dom, *rest in SRC:
        if host == dom or host.endswith('.' + dom) or host == 'www.' + dom:
            return rest[0]
    return None

# ------------------------------------------------------------------ read git
SEP = '\x1f'
fmt = SEP.join(['%H', '%aI', '%cI', '%(trailers:key=Kind,valueonly,separator=%x1e)', '%(trailers:key=Source,valueonly,separator=%x1e)',
                '%(trailers:key=Listed-on,valueonly,separator=%x1e)'])
S = {k: {'n': 0, 'kinds': collections.Counter(), 'newest': None, 'future': 0, 'last': None, 'listed': collections.Counter(), 'folders': collections.Counter()} for _, k, *_ in SRC}
commits = []
cur = None
for line in git('log', ref, '--format=@@' + fmt, '--name-only', '--no-renames').split('\n'):
    if line.startswith('@@'):
        h, ad, cd, kind, srcs, listed = line[2:].split(SEP)
        cur = {'h': h, 'ad': ad[:10], 'cd': cd[:19], 'kind': kind.strip(), 'src': [s for s in srcs.split('\x1e') if s.strip()], 'listed': [s for s in listed.split('\x1e') if s.strip()], 'files': []}
        commits.append(cur)
    elif line.strip() and cur is not None:
        cur['files'].append(line.strip())
for c in commits:
    k = next((src_of(s) for s in c['src'] if src_of(s)), None)
    if not k: continue
    s = S[k]
    s['n'] += 1; s['kinds'][c['kind'] or 'record'] += 1
    d = dt.date.fromisoformat(c['ad'])
    if d > TODAY: s['future'] += 1
    elif not s['newest'] or d > s['newest']: s['newest'] = d
    cd = dt.date.fromisoformat(c['cd'][:10])
    if not s['last'] or cd > s['last']: s['last'] = cd
    for l in c['listed']: s['listed'][l] += 1
    for f in c['files'][:1]:
        p = f.split('/')
        s['folders']['/'.join(p[:2]) + '/' if p[0] in ('local', 'nacrt', 'predlog', 'sudska-praksa', 'odluke-tela') and len(p) > 2 else p[0] + '/'] += 1

# data tables: bills and the open-data registers
def table_rows(path):
    try: return list(csv.DictReader(io.StringIO(git('show', f'{ref}:{path}'))))
    except subprocess.CalledProcessError: return []
bills_files = [f for f in git('ls-tree', '--name-only', ref, 'data/').split('\n') if re.match(r'data/bills-\d{4}\.csv$', f)]
n_bills = sum(len(table_rows(f)) for f in bills_files)
bills_last = git('log', '-1', '--format=%cs', ref, '--', 'data/bills-*.csv').strip()
reg_sources = []
for body in [d for d in git('ls-tree', '--name-only', ref, 'data/registers/').split('\n') if d]:
    for r in table_rows(body + '/SOURCES.csv'):
        reg_sources.append({'body': body.split('/')[-1], 'dataset': r.get('dataset', ''), 'page': r.get('dataset_page', ''), 'downloaded': r.get('downloaded', ''), 'modified': r.get('portal_last_modified', ''), 'rows': r.get('rows', ''), 'file': body + '/' + r.get('file', '')})
if reg_sources:
    S['odp']['n'] = len(reg_sources)
    S['odp']['last'] = max(dt.date.fromisoformat(r['downloaded']) for r in reg_sources if r['downloaded'])
    S['odp']['newest'] = max(dt.date.fromisoformat(r['modified']) for r in reg_sources if r['modified'])
    S['odp']['folders']['data/registers/'] = len(reg_sources)
    S['odp']['kinds']['record'] = len(reg_sources)

# global-law's row for this corpus
gl = None
try:
    with urllib.request.urlopen('https://raw.githubusercontent.com/lexifina/global-law/main/data/freshness.tsv', timeout=30) as resp:
        for r in csv.DictReader(io.StringIO(resp.read().decode('utf-8')), delimiter='\t'):
            if r['path'] == CORPUS: gl = r
except Exception as e:
    print('global-law freshness not read:', e, file=sys.stderr)
behind = int(git('rev-list', '--count', f'{gl["pinned"]}..{ref}').strip()) if gl and gl.get('pinned') and subprocess.run(['git', '-C', ROOT, 'cat-file', '-e', gl['pinned']], capture_output=True).returncode == 0 else None

# ------------------------------------------------------------------ helpers
def d_sr(d): return f'{d.day}. {d.month}. {d.year}.' if d else '–'
def d_en(d): return d.isoformat() if d else '–'
def num(n, lang): return f'{n:,}'.replace(',', '.' if lang == 'sr' else ',')
def status(k, s, lang):
    if k in PAUSED: return ('pauzirano' if lang == 'sr' else 'paused')
    if not s['last']: return ('nije čitano' if lang == 'sr' else 'never read')
    lvl = next(x[-1] for x in SRC if x[1] == k)
    age = (TODAY - s['last']).days
    ok = age <= THRESH[lvl]
    return ('ažurno' if ok else 'zastarelo') if lang == 'sr' else ('current' if ok else 'stale')
def name(k, lang):
    x = next(x for x in SRC if x[1] == k)
    return x[2] if lang == 'sr' else x[3]
def link(k):
    x = next(x for x in SRC if x[1] == k)
    return 'https://www.' + x[0] if not x[0].startswith(('skupstina.', 'kragujevac.', 'kzk.', 'kjn.', 'ekonsultacije.', 'ombudsman.', 'data.', 'rik.')) else 'https://' + x[0]
def what(k, lang):
    x = next(x for x in SRC if x[1] == k)
    if x[4]: return x[4][0 if lang == 'sr' else 1]
    pages = [u for u, _ in S[k]['listed'].most_common(3)]
    if pages: return ', '.join(f'[{("stranica" if lang == "sr" else "page")} {i}]({u})' for i, u in enumerate(pages, 1))
    return '–'
def folders(k):
    return ', '.join(f'`{f}`' for f, _ in S[k]['folders'].most_common(4)) + (' …' if len(S[k]['folders']) > 4 else '')
def kinds(k, lang):
    m = KIND_SR if lang == 'sr' else KIND_EN
    return '; '.join(f'{num(n, lang)} {m.get(kk, kk)}' for kk, n in S[k]['kinds'].most_common())
ORDER = [x[1] for x in SRC if S[x[1]]['n']]
def other(lang, base):
    return f'[English]({base}.en.md)' if lang == 'sr' else f'[Srpski]({base}.md)'

last_commit = git('log', '-1', '--format=%cI%x1f%s', ref).strip().split('\x1f')
def window(days):
    cut = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)
    c = collections.Counter()
    for x in commits:
        if dt.datetime.fromisoformat(x['cd']).replace(tzinfo=dt.timezone.utc) >= cut: c[x['kind'] if x['kind'] not in ('', 'documentation', 'layout') else 'docs'] += 1
    return c

# ------------------------------------------------------------------ WATCHING
def watching(lang):
    sr = lang == 'sr'
    o = []
    o.append('# Praćenje izvora: šta se prati za Srbiju' if sr else '# Watching the sources: what is watched for Serbia')
    o.append('')
    o.append(other(lang, 'WATCHING'))
    o.append('')
    o.append((f'Kako global-law prati izvore svih zemalja (detektori promena, dnevna provera, šta znači pogodak): [global-law WATCHING.md]({GL}/WATCHING.md). '
              'Ova stranica je isto to, samo za Srbiju: svaki zvanični izvor iz kojeg ovaj repozitorijum uzima tekstove, šta se na njemu čita da bi se videlo da li ima nečeg novog, i kada je poslednji put pročitan.')
             if sr else
             (f'How global-law watches every country\'s sources (change detectors, the daily poll, what a hit means): [global-law WATCHING.md]({GL}/WATCHING.md). '
              'This page is the same thing for Serbia only: every official source this repository takes text from, what is read on it to see whether anything is new, and when it was last read.'))
    o.append('')
    o.append((f'Napravljeno {d_sr(TODAY)} iz istorije gita (`{head[:10]}`): izvor svakog komita je u njegovom redu `Source:`, a „poslednji put pročitan“ je dan kada je ovaj repozitorijum poslednji put objavio nešto iz tog izvora.')
             if sr else
             (f'Built on {d_en(TODAY)} from the git history (`{head[:10]}`): each commit names its source in its `Source:` line, and "last read" is the day this repository last published something from that source.'))
    o.append('')
    o.append('| Izvor | Šta se čita | Fascikle | Komita | Poslednji put pročitan | Stanje |' if sr else '| Source | What is read | Folders | Commits | Last read | State |')
    o.append('| --- | --- | --- | ---: | --- | --- |')
    for k in ORDER:
        s = S[k]
        o.append(f'| [{name(k, lang)}]({link(k)}) | {what(k, lang)} | {folders(k)} | {num(s["n"], lang)} | {(d_sr if sr else d_en)(s["last"])} | {status(k, s, lang)} |')
    o.append('')
    o.append(('Uz to, [`data/bills-*.csv`](data/) drži spisak svih predloga zakona Narodne skupštine (' + num(n_bills, lang) + f' predloga; poslednji put osveženo {d_sr(dt.date.fromisoformat(bills_last)) if bills_last else "–"}), a [`data/registers/`](data/registers/) ' + num(len(reg_sources), lang) + ' skupova podataka sa portala otvorenih podataka; svaki je naveden u `SOURCES.csv` svoje fascikle sa adresom, danom preuzimanja i danom kada ga je portal poslednji put izmenio.')
             if sr else
             ('In addition, [`data/bills-*.csv`](data/) holds the National Assembly\'s list of every bill (' + num(n_bills, lang) + f' bills; last refreshed {bills_last or "–"}), and [`data/registers/`](data/registers/) ' + num(len(reg_sources), lang) + ' datasets from the open-data portal; each is listed in its folder\'s `SOURCES.csv` with its address, the day it was downloaded and the day the portal last changed it.'))
    o.append('')
    o.append('## Kako se prati' if sr else '## How it is watched')
    o.append('')
    if sr:
        o += ['- **Nema automatskog dnevnog praćenja za Srbiju.** Detektori promena global-law-a napravljeni su, ali još nisu uključeni (vidi gore). Svaki izvor se ponovo čita kada se pokrene njegova traka u ovom repozitorijumu, a datum iznad pokazuje kada je to poslednji put urađeno.',
              '- **Pravila ponašanja.** Svaki izvor se čita uz poštovanje njegovog robots.txt, sa pauzama između zahteva; tekstovi uvek dolaze iz zvaničnog izvora, a promena se nikada ne izvodi iz detektora.',
              '- **Pogodak.** Kada izvor objavi nešto novo, to postaje novi komit sa datumom dana kada se primenjuje; global-law ga zatim preuzima pri sledećem prolazu ([monitoring/](monitoring/)).']
    else:
        o += ['- **There is no automatic daily watch for Serbia yet.** global-law\'s change detectors are built but not switched on (see above). Each source is re-read when its lane in this repository runs, and the date above shows when that last happened.',
              '- **Manners.** Every source is read within its robots.txt, with pauses between requests; text always comes from the official source, never from a detector.',
              '- **A hit.** When a source publishes something new, it becomes a new commit dated the day it applies; global-law picks it up on its next pass ([monitoring/](monitoring/README.en.md)).']
    o.append('')
    o.append(('Samo zvanična objava (Službeni glasnik RS, službeni listovi gradova, sajtovi sudova i organa) ima pravnu snagu.' if sr else
              'Only the official publication (the Official Gazette of Serbia, the cities\' official gazettes, the courts\' and bodies\' own sites) has legal force.'))
    o.append('')
    return '\n'.join(o)

# ------------------------------------------------------------------ FRESHNESS
def freshness(lang):
    sr = lang == 'sr'
    D = d_sr if sr else d_en
    o = ['# Ažurnost: da li je tačno danas?' if sr else '# Freshness: is it true right now?', '', other(lang, 'FRESHNESS'), '']
    o.append((f'Kako global-law meri ažurnost svih korpusa (stanja, pragovi od 7 i 30 dana, alat `freshness.py`): [global-law FRESHNESS.md]({GL}/FRESHNESS.md). '
              'Ovde je isto merenje za Srbiju, izvor po izvor.') if sr else
             (f'How global-law measures freshness for every corpus (the statuses, the 7- and 30-day thresholds, the `freshness.py` tool): [global-law FRESHNESS.md]({GL}/FRESHNESS.md). '
              'Here is the same measure for Serbia, source by source.'))
    o.append('')
    o.append('## Kako ga vidi global-law' if sr else '## How global-law sees it')
    o.append('')
    if gl:
        lv = dt.date.fromisoformat(gl['last_verified']) if gl.get('last_verified') else None
        o.append('| Korpus | Stanje | Poslednja provera | Način | Komit u global-law | Novijih komita ovde |' if sr else '| Corpus | Status | Last checked | Method | Commit pinned in global-law | Newer commits here |')
        o.append('| --- | --- | --- | --- | --- | ---: |')
        o.append(f'| `{CORPUS}` | `{gl["status"]}` | {D(lv)} | `{gl["method"]}` | `{gl["pinned"][:10]}` | {num(behind, lang) if behind is not None else "–"} |')
        o.append('')
        o.append((f'`{gl["status"]}`: prag za nacionalno pravo je 7 dana od poslednje provere. Komitovi novijih od zakačenog global-law preuzima pri sledećem prolazu; do tada ih čitajte ovde.' if sr else
                  f'`{gl["status"]}`: the threshold for national law is 7 days since the last check. global-law takes commits newer than the pinned one on its next pass; until then, read them here.'))
    else:
        o.append('Red global-law-a nije pročitan pri pravljenju ove stranice; vidi [data/freshness.tsv](' + GL + '/data/freshness.tsv).' if sr else
                 'global-law\'s row could not be read when this page was built; see [data/freshness.tsv](' + GL + '/data/freshness.tsv).')
    o.append('')
    o.append('## Izvor po izvor' if sr else '## Source by source')
    o.append('')
    o.append(('„Najnoviji zapis“ je najkasniji dan primene ili odluke koji nije u budućnosti; „poslednji put pročitan“ je dan kada je ovaj repozitorijum poslednji put objavio nešto iz izvora. Prag: 7 dana za nacionalne propise, 30 za lokalne akte, sudsku praksu i dokumente.') if sr else
             ('"Newest record" is the latest day of application or decision that is not in the future; "last read" is the day this repository last published something from the source. Threshold: 7 days for national acts, 30 for local acts, case law and documents.'))
    o.append('')
    o.append('| Izvor | Komita | Najnoviji zapis | Poslednji put pročitan | Dana od tada | Stanje | Napomena |' if sr else '| Source | Commits | Newest record | Last read | Days since | State | Note |')
    o.append('| --- | ---: | --- | --- | ---: | --- | --- |')
    for k in ORDER:
        s = S[k]
        age = (TODAY - s['last']).days if s['last'] else None
        note = PAUSED[k][0 if sr else 1] if k in PAUSED else (NOTES[k][0 if sr else 1] if k in NOTES else '')
        if s['future']: note = (note + '; ' if note else '') + (f'{num(s["future"], lang)} sa datumom primene u budućnosti' if sr else f'{num(s["future"], lang)} dated in the future')
        o.append(f'| {name(k, lang)} | {num(s["n"], lang)} | {D(s["newest"])} | {D(s["last"])} | {age if age is not None else "–"} | {status(k, s, lang)} | {note} |')
    o.append('')
    o.append('## Proverite sami' if sr else '## Check it yourself')
    o.append('')
    o.append('```')
    o.append('git log -1 --format="%cs %s" -- zakon/                ' + ('# poslednji objavljeni zakon' if sr else '# the last law published'))
    o.append('git log -1 --format="%as %s" -- zakon/2001/24-1/      ' + ('# poslednja verzija jednog propisa (dan primene)' if sr else '# one act\'s latest version (day it applies)'))
    o.append('git log --since=7.days --format="%cs %s" | head        ' + ('# šta je stiglo ove nedelje' if sr else '# what arrived this week'))
    o.append('```')
    o.append('')
    o.append(('Kada je datum koji vas zanima posle poslednje provere, potvrdite tekst u zvaničnom izvoru. Samo zvanična objava ima pravnu snagu.') if sr else
             ('When the date you care about is after the last check, confirm the text against the official source. Only the official publication has legal force.'))
    o.append('')
    return '\n'.join(o)

# ------------------------------------------------------------------ monitoring
def monitoring(lang):
    sr = lang == 'sr'
    D = d_sr if sr else d_en
    lc = dt.datetime.fromisoformat(last_commit[0]).astimezone(dt.timezone.utc)
    w1, w7, w30 = window(1), window(7), window(30)
    km = KIND_SR if sr else KIND_EN
    def wtxt(c): return '; '.join(f'{num(n, lang)} {km.get(k, ("dokumentacija" if sr else "documentation") if k == "docs" else k)}' for k, n in c.most_common()) or ('ništa' if sr else 'none')
    o = ['# Praćenje: da li Srbija ide u korak?' if sr else '# Monitoring: does Serbia keep up?', '', other(lang, 'README'), '']
    o.append((f'Kako global-law prati sve korpuse (prolaz na svakih 15 minuta, provera svakog komita, javni status): [global-law monitoring/]({GLT}/monitoring). '
              'Ovde je stanje samo za ovaj repozitorijum.') if sr else
             (f'How global-law monitors every corpus (a pass every 15 minutes, a check of every commit, a public status): [global-law monitoring/]({GLT}/monitoring). '
              'This page is the state of this repository alone.'))
    o.append('')
    o.append(f'**{"Stanje" if sr else "Status"} {D(TODAY)}**')
    o.append('')
    o.append('| | |')
    o.append('| --- | --- |')
    o.append(f'| {"Poslednji komit" if sr else "Last commit"} | {lc.strftime("%Y-%m-%d %H:%M")} UTC: {last_commit[1][:120]}{"…" if len(last_commit[1]) > 120 else ""} |')
    o.append(f'| {"Poslednja 24 sata" if sr else "Last 24 hours"} | {wtxt(w1)} |')
    o.append(f'| {"Poslednjih 7 dana" if sr else "Last 7 days"} | {wtxt(w7)} |')
    o.append(f'| {"Poslednjih 30 dana" if sr else "Last 30 days"} | {wtxt(w30)} |')
    if gl:
        o.append(f'| global-law | `{CORPUS}` {"je" if sr else "is"} `{gl["status"]}`, {"zakačen na" if sr else "pinned at"} `{gl["pinned"][:10]}`' + (f', {num(behind, lang)} {"novijih komita ovde" if sr else "newer commits here"}' if behind else '') + ' |')
    for k, (rsr, ren) in PAUSED.items():
        o.append(f'| {name(k, lang)} | {"pauzirano: " + rsr if sr else "paused: " + ren} |')
    stale = [name(k, lang) for k in ORDER if status(k, S[k], lang) in ('zastarelo', 'stale')]
    o.append(f'| {"Zastareli izvori" if sr else "Stale sources"} | {", ".join(stale) if stale else ("nema" if sr else "none")} ([{"FRESHNESS.md" if sr else "FRESHNESS.en.md"}](../{"FRESHNESS.md" if sr else "FRESHNESS.en.md"})) |')
    o.append('')
    o.append('## Kako nove izmene stižu' if sr else '## How new changes arrive')
    o.append('')
    if sr:
        o += ['1. Traka za svaki izvor čita njegov spisak novih tekstova (vidi [WATCHING.md](../WATCHING.md)) i svaku promenu objavljuje kao komit sa datumom dana kada se primenjuje.',
              '2. Pre objavljivanja svaki komit prolazi provere ovog repozitorijuma: tekst se poredi sa izvorom, a datumi sa zaglavljem Službenog glasnika (vidi [REPRODUCE.md](../REPRODUCE.md)).',
              f'3. global-law na svakih 15 minuta proverava nove komitove i pomera svoj pokazivač na `{CORPUS}` (vidi [global-law monitoring/]({GLT}/monitoring)).']
    else:
        o += ['1. Each source\'s lane reads its list of new texts (see [WATCHING.en.md](../WATCHING.en.md)) and publishes each change as a commit dated the day it applies.',
              '2. Before publishing, every commit goes through this repository\'s checks: the text against the source, the dates against the Official Gazette header (see [REPRODUCE.md](../REPRODUCE.md)).',
              f'3. Every 15 minutes global-law checks new commits and moves its pin on `{CORPUS}` (see [global-law monitoring/]({GLT}/monitoring)).']
    o.append('')
    o.append('## Proverite sami' if sr else '## Check it yourself')
    o.append('')
    o.append('```')
    o.append('git fetch && git log -1 --format="%cI %s" origin/main')
    o.append('git log --since=1.day --format="%cs %s" origin/main | wc -l')
    o.append('python monitoring/make_pages.py           ' + ('# ponovo napravi ove tri stranice' if sr else '# rebuild these three pages'))
    o.append('```')
    o.append('')
    o.append('## Pratite sami: fork i GitHub Actions' if sr else '## Watch it yourself: a fork and GitHub Actions')
    o.append('')
    if sr:
        o += ['Svako može da napravi fork ovog repozitorijuma i da ga sam drži ažurnim, bez nas. GitHub Actions je besplatan za javne repozitorijume.',
              '',
              '1. Napravite fork: <https://github.com/lexifina/serbia-law/fork>.',
              '2. U forku kopirajte [`monitoring/fork-workflow.yml`](fork-workflow.yml) u `.github/workflows/refresh.yml` i pošaljite izmenu u granu `main`.',
              '3. Na kartici **Actions** forka uključite tokove rada (GitHub ih u forkovima podrazumevano isključuje) i jednom pokrenite **Refresh from lexifina/serbia-law**.',
              '',
              'Svakih 6 sati tok rada preuzima nove komitove iz ovog repozitorijuma u `main` vašeg forka (GitHub-ovim „Sync fork“, pa je `main` ovaj repozitorijum plus vaš tok rada), ponovo pravi WATCHING, FRESHNESS i ovu stranicu za vaš primerak, objavljuje ih u granu `status` i prikazuje FRESHNESS u sažetku pokretanja. Jedno pokretanje traje oko dva minuta. Tok rada ne čita zvanične izvore: proverava koliko je ovaj repozitorijum ažuran.']
    else:
        o += ['Anyone can fork this repository and keep their copy current without us. GitHub Actions is free for public repositories.',
              '',
              '1. Fork it: <https://github.com/lexifina/serbia-law/fork>.',
              '2. In the fork, copy [`monitoring/fork-workflow.yml`](fork-workflow.yml) to `.github/workflows/refresh.yml` and commit it to `main`.',
              '3. On the fork\'s **Actions** tab, enable workflows (GitHub turns them off in forks by default) and run **Refresh from lexifina/serbia-law** once.',
              '',
              'Every 6 hours the workflow takes the new commits from this repository into your fork\'s `main` (through GitHub\'s own "Sync fork", so your `main` is this repository plus your workflow file), rebuilds WATCHING, FRESHNESS and this page for your copy, publishes them to a `status` branch and shows FRESHNESS in the run summary. A run takes about two minutes. The workflow does not read the official sources: it checks how current this repository is.']
    o.append('')
    return '\n'.join(o)

def write(path, text):
    with open(os.path.join(ROOT, path), 'w', encoding='utf-8', newline='\n') as f: f.write(text)
    print('wrote', path)
write('WATCHING.md', watching('sr')); write('WATCHING.en.md', watching('en'))
write('FRESHNESS.md', freshness('sr')); write('FRESHNESS.en.md', freshness('en'))
write('monitoring/README.md', monitoring('sr')); write('monitoring/README.en.md', monitoring('en'))
