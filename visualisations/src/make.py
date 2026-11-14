"""Rebuild visualisations/srpsko-pravo-u-20-grafikona.html from this repository.

    python visualisations/src/make.py [--repo PATH] [--ref REF]

Steps (all read-only on the repository; scratch output goes to visualisations/src/.build/):
  1. git log of REF with author dates and full messages  -> .build/log.txt -> .build/commits.json
  2. git log --name-only: the act folders each commit touches -> .build/paths.json
  3. git ls-tree: every act folder (<kind>/<year>/<number>)  -> .build/actdirs.txt
  4. git archive of data/ and registry/data/                 -> .build/repo/
  5. prep.py turns those into .build/data.json; build.py fills page.tpl.html with it.
Works in a sparse or --no-checkout clone, because everything is read from git objects.
"""
import argparse, io, json, os, re, subprocess, sys, tarfile

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument('--repo', default=os.path.abspath(os.path.join(HERE, '..', '..')))
ap.add_argument('--ref', default=None, help='default: origin/main if present, else HEAD')
ap.add_argument('--out', default=os.path.join(HERE, '..', 'srpsko-pravo-u-20-grafikona.html'))
a = ap.parse_args()
B = os.path.join(HERE, '.build')
os.makedirs(B, exist_ok=True)

def git(*args, **kw):
    return subprocess.run(['git', '-C', a.repo, *args], check=True, capture_output=True, **kw).stdout

ref = a.ref
if not ref:
    ref = 'origin/main' if subprocess.run(['git', '-C', a.repo, 'rev-parse', '--verify', '-q', 'origin/main'], capture_output=True).returncode == 0 else 'HEAD'
sha = git('rev-parse', ref).decode().strip()
print('ref', ref, sha)

# 1. commits with trailers
TR = set('Kind Source Provisions Law In-force Published Act Consolidated Decided Case Court Outcome Area Challenged Text Verified '
         'In-force-rule Issuer Words-changed Affecting Adopted-as Register-number Published-in Also-amended-by Body Subject Type Listing '
         'Gazette Adopted Bill Contracting-authority Applicant Also-concerns Listed-on Enacted'.split())
raw = git('log', ref, '--format=@@C %H|%ad|%cd|%an%n%B', '--date=iso-strict').decode('utf-8', 'replace')
rows, cur = [], None
for line in raw.split('\n'):
    if line.startswith('@@C '):
        if cur: rows.append(cur)
        h, ad, cd, an = line[4:].split('|', 3)
        cur = {'h': h, 'ad': ad, 'cd': cd, 'an': an, 'subj': None, 'body': [], 't': {}}
        continue
    if cur is None: continue
    if cur['subj'] is None:
        cur['subj'] = line; continue
    m = re.match(r'^([A-Z][A-Za-z-]+): (.*)$', line)
    if m and m.group(1) in TR:
        cur['t'].setdefault(m.group(1), []).append(m.group(2))
    else:
        cur['body'].append(line)
if cur: rows.append(cur)
for r in rows: r['body'] = '\n'.join(r['body']).strip()
json.dump(rows, open(os.path.join(B, 'commits.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('commits', len(rows))

# 2. folders per commit
out, cur = {}, None
for l in git('log', ref, '--format=@@C %H', '--name-only', '--no-renames').decode('utf-8', 'replace').split('\n'):
    if l.startswith('@@C '): cur = l[4:]; out[cur] = []; continue
    if not l or cur is None: continue
    p = l.split('/')
    d = '/'.join(p[:3]) if len(p) > 3 else ('/'.join(p[:-1]) or p[0])
    if d not in out[cur]: out[cur].append(d)
json.dump(out, open(os.path.join(B, 'paths.json'), 'w', encoding='utf-8'), ensure_ascii=False)

# 3. act folders in the tree
KINDS = set('zakon uredba pravilnik odluka akt memorandum resenje naredba sporazum uputstvo tarifa statut poslovnik kolektivni kodeks '
            'protokol pravila zakljucak ustav program strategija metodologija plan konvencija ugovor ukaz'.split())
dirs = set()
for f in git('ls-tree', '-r', '--name-only', ref).decode('utf-8', 'replace').split('\n'):
    p = f.split('/')
    if len(p) >= 4 and p[0] in KINDS: dirs.add('/'.join(p[:3]))
open(os.path.join(B, 'actdirs.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(sorted(dirs)) + '\n')

# 4. data tables
tar = git('archive', ref, 'data', 'registry/data')
with tarfile.open(fileobj=io.BytesIO(tar)) as tf:
    tf.extractall(os.path.join(B, 'repo'), filter='data')

# 5. prep + build
env = dict(os.environ, HEAD_SHA=sha)
subprocess.run([sys.executable, '-X', 'utf8', os.path.join(HERE, 'prep.py'), B], check=True, env=env)
subprocess.run([sys.executable, '-X', 'utf8', os.path.join(HERE, 'build.py'), os.path.join(B, 'data.json'), os.path.abspath(a.out)], check=True)
