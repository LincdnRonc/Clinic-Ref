"""Import Christopher Estes' Rad Onc Tables (Key Studies and Oral Boards .xlsx exports) into data/estes.json.

    python3 tools/estes_import.py "Rad Onc Tables - Key Studies.xlsx" "Rad Onc Tables - Oral Boards.xlsx"

The spreadsheets themselves are not stored in this repo. build.py renders data/estes.json as:
  - a "Trial tables" tab on each tumour-site page (Key Studies, routed by sheet and topic: ROUTES below), and
  - an "Oral boards" tab on each Phase 2 exam-summary page (Oral Boards rows, routed by sheet: BOARD_ROUTES).
Text is kept as written (US spelling); only whitespace is tidied.
"""
import json, re, sys
from pathlib import Path
import openpyxl

root = Path(__file__).resolve().parent.parent

def clean(v):
    if v is None: return ''
    s = str(v).replace('\r', '').strip()
    s = re.sub(r'[ \t]+\n', '\n', s); s = re.sub(r'\n{3,}', '\n\n', s)
    return s

def low(s): return s.lower()

# ---------- Key Studies: (sheet, topic, subtopic) -> clinic page ----------
def route(sheet, topic, sub):
    t, s = low(topic), low(sub)
    ts = t + ' ' + s
    if sheet == 'Benign':
        if re.search(r'avm|trigeminal|tremor', t): return 'cns-benign.html'
        return 'benign.html'
    if sheet == 'Breast':
        if re.search(r'dcis|early|hormone', t): return 'breast-early.html'
        if re.search(r'imrt|lidocaine|adverse|hyperthermia', t): return 'breast-planning.html'
        if t == 'various' and not re.search(r'sln|alnd|axill|amaros', s): return 'breast-early.html'
        return 'breast-nodes-pmrt.html'
    if sheet == 'CNS':
        if 'brain metast' in t: return 'pall-brain.html'
        if re.search(r'glio|astrocytoma', t): return 'cns-glioma.html'
        if re.search(r'acoustic|schwannoma', t): return 'cns-vs.html'
        if re.search(r'meningioma|avm|trigeminal', t): return 'cns-benign.html'
        if 'lymphoma' in t: return 'heme-nhl.html'
        return 'cns-general.html'
    if sheet == 'Cutaneous': return 'skin.html'
    if sheet == 'GI':
        if t.startswith('anal'): return 'gi-anal.html'
        if re.search(r'rect|colon|colorectal', t): return 'gi-rectum-colon.html'
        if re.search(r'esoph|gastric', t): return 'gi-oesophagus-gastric.html'
        if 'pancrea' in t: return 'gi-pancreas.html'
        if re.search(r'hcc|biliary|gallbladder|liver|cholang', t): return 'gi-hepatobiliary.html'
        return 'gi-general.html'
    if sheet == 'GU':
        if 'bladder' in t: return 'gu-bladder.html'
        if 'renal' in t: return 'gu-kidney.html'
        if 'seminoma' in t: return 'gu-testis.html'
        return 'gu-other.html'
    if sheet == 'Gyn':
        if 'and cervix' in t or 'ovar' in t: return 'gyn-general.html'
        if 'cervi' in t: return 'gyn-cervix.html'
        if re.search(r'endomet|uter', t): return 'gyn-endometrial.html'
        if re.search(r'vulv|vagin', t): return 'gyn-vulva-vagina.html'
        return 'gyn-general.html'
    if sheet == 'H&N':
        if 'oral' in t: return 'hn-oral-salivary.html'
        if 'nasophar' in t: return 'hn-npc-sinonasal.html'
        if re.search(r'larynx|hypophar', t): return 'hn-larynx.html'
        if 'oropharynx' in t: return 'hn-oropharynx.html'
        if 'unknown' in t: return 'hn-thyroid-cup.html'
        return 'hn-general.html'
    if sheet == 'Lung':
        if t.startswith('sclc'): return 'thorax-sclc.html'
        if re.search(r'meso|thym', t): return 'thorax-other.html'
        if 'breast, prostate' in t: return 'pall-oligo.html'
        if 'sbrt' in t: return 'thorax-early.html'
        if re.search(r'oligomet|metastatic|crizotinib', s): return 'thorax-metastatic.html'
        if re.search(r'lobar|lobectomy|segment|wedge|sbrt', s): return 'thorax-early.html'
        return 'thorax-stage3.html'
    if sheet == 'Lymphoma':
        if re.search(r'hodgkin|nodular', t) and 'non-hodgkin' not in t: return 'heme-hodgkin.html'
        if re.search(r'mycosis|leuk', t): return 'heme-other.html'
        return 'heme-nhl.html'
    if sheet == 'Palliation':
        if re.search(r'bone|spine', t): return 'pall-bone-spine.html'
        return 'pall-oligo.html'
    if sheet == 'Peds':
        if t.startswith('cns'): return 'peds-cns.html'
        if 'hodgkin' in t: return 'heme-hodgkin.html'
        if 'leuk' in t: return 'heme-other.html'
        return 'peds-solid.html'
    if sheet == 'Prostate': return 'gu-prostate.html'
    if sheet == 'Radiopharm':
        if 'prostate' in t: return 'gu-prostate.html'
        if 'thyroid' in t: return 'hn-thyroid-cup.html'
        return 'gi-general.html'
    if sheet == 'Sarcoma': return 'sarcoma-sts.html'
    return None

# Recent sheet: topics are free text, so route by keywords (first match wins)
RECENT_KW = [
 (r'brain met', 'pall-brain.html'), (r'prostat|pluvicto', 'gu-prostate.html'), (r'osteoarth|dupuytren|macular', 'benign.html'),
 (r'breast|rni|triple neg', None), (r'meningioma', 'cns-benign.html'), (r'glio', 'cns-glioma.html'), (r'sclc', 'thorax-sclc.html'),
 (r'nsclc', None), (r'rect', 'gi-rectum-colon.html'), (r'esoph|gastric', 'gi-oesophagus-gastric.html'), (r'hcc', 'gi-hepatobiliary.html'),
 (r'gallbladder', 'gi-hepatobiliary.html'), (r'pancrea', 'gi-pancreas.html'), (r'neuroendocrine', 'gi-general.html'),
 (r'bladder', 'gu-bladder.html'), (r'renal', 'gu-kidney.html'), (r'cervi', 'gyn-cervix.html'), (r'endomet', 'gyn-endometrial.html'),
 (r'vulv', 'gyn-vulva-vagina.html'), (r'oropharynx', 'hn-oropharynx.html'), (r'h&n|head and neck', 'hn-general.html'),
 (r'cutaneous', 'skin.html'), (r'pcnsl|cns lymphoma', 'heme-nhl.html'), (r'hodgkin', 'heme-hodgkin.html'),
 (r'rms|rhabdo|ewing', 'peds-solid.html'), (r'liver', 'pall-oligo.html'),
]

TRIAL_KEYS = ['theTopic','theSubtopic','theTrial','theCitation','theN','thePatients','theMethods','theResults',
              'theInterpretation','theCommentary','theNotes','theReference','theQuestion']

def norm_name(s): return re.sub(r'[^a-z0-9]', '', re.sub(r'⭐️?|\(protocol\)', '', s.lower()))

def key_studies(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    out, seen, recent = [], {}, []
    for ws in wb:
        if ws.title in ('About', 'Legend'): continue
        hdr = [c.value for c in ws[1]]
        for r in ws.iter_rows(min_row=3, values_only=True):
            d = dict(zip(hdr, r))
            name = clean(d.get('theTrial'))
            if not name: continue
            e = {k[3:].lower(): clean(d.get(k)) for k in TRIAL_KEYS}
            e['links'] = [clean(d.get(f'theLink{i}')) for i in range(1, 11) if clean(d.get(f'theLink{i}')).startswith('http')]
            e['sheet'] = ws.title
            if ws.title == 'Recent': recent.append(e); continue
            e['page'] = route(ws.title, e['topic'], e['subtopic'])
            if not e['page']: continue
            k = (e['page'], norm_name(name), e['citation'][:30])
            if k in seen: continue
            seen[k] = e; out.append(e)
    # Recent: flag the matching entry, or add it if the site sheets do not have it
    added = 0
    for e in recent:
        nk = norm_name(e['trial'])
        hits = [x for x in out if norm_name(x['trial']) == nk]
        if hits:
            for x in hits: x['recent'] = 1
            continue
        txt = (e['topic'] + ' ' + e['subtopic']).lower(); page = None
        for rx, pg in RECENT_KW:
            if re.search(rx, txt):
                if pg: page = pg
                elif 'nsclc' in rx: page = 'thorax-metastatic.html' if 'oligo' in txt else 'thorax-stage3.html'
                else: page = 'breast-nodes-pmrt.html' if re.search(r'rni|locally|oligo|pmrt|triple', txt) else 'breast-early.html'
                break
        if page:
            e['page'] = page; e['recent'] = 1; out.append(e); added += 1
            seen[(page, nk, e['citation'][:30])] = e
    print(f'key studies: {len(out)} entries ({added} only in Recent)')
    return out

# ---------- Oral Boards: sheet -> exam page (row-level overrides by keyword) ----------
def board_route(sheet, title):
    t = title.lower()
    if sheet == 'BREAST': return 'exam-breast.html'
    if sheet == 'CNS': return 'exam-cns.html'
    if sheet == 'GU':
        if re.search(r'prostat|brachy|gynecomastia', t): return 'exam-prostate.html'
        return 'exam-gu.html'
    if sheet == 'GI':
        if re.search(r'anal|rect|colon|wle', t): return 'exam-lgi.html'
        return 'exam-ugi.html'
    if sheet == 'GYN': return 'exam-gyn.html'
    if sheet == 'LYMPHOMA': return 'exam-heme.html'
    if sheet == 'LUNG': return 'exam-thorax.html'
    if sheet == 'H&N':
        if re.search(r'thyroid|keloid', t): return 'exam-endocrine-benign.html'
        if re.search(r'merkel|cutaneous|kaposi|scalp|lentigo|^melanoma', t): return 'exam-skin.html'
        return 'exam-hn.html'
    if sheet == 'PEDS': return 'exam-peds.html'
    if sheet == 'SARCOMA': return 'exam-sarcoma.html'
    if sheet == 'SRS & SBRT':
        if re.search(r'meningioma|vestibular|trigeminal|avm|pituitary|paragang', t): return 'exam-cns.html'
        return 'exam-pall.html'
    if sheet == 'TOXICITY': return 'exam-clinonc.html'
    if sheet in ('BENIGN',): return 'exam-endocrine-benign.html'
    if sheet in ('SKIN',): return 'exam-skin.html'
    if sheet in ('PALLBONE MET',): return 'exam-pall.html'
    return None

def oral_boards(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    out = []
    for ws in wb:
        if ws.title in ('About', 'References'): continue
        hdr = [clean(c.value) for c in ws[1]]
        for r in ws.iter_rows(min_row=2, values_only=True):
            cells = [clean(c) for c in r]
            if not any(cells): continue
            filled = [(hdr[i] if i < len(hdr) else '', c) for i, c in enumerate(cells) if c]
            first = cells[0]
            if len(filled) == 1 and filled[0][0] == hdr[0]:
                if len(first) < 30 or re.search(r'\bsee .* sections?\s*$', first): continue          # section title row (e.g. "Breast")
                out.append({'sheet': ws.title, 'page': board_route(ws.title, first), 'title': '', 'note': first, 'fields': []}); continue
            lines = first.split('\n')
            title, rest = lines[0].strip(' :'), '\n'.join(lines[1:]).strip()
            fields = [(h or 'Notes', c) for h, c in filled[1:]] if first else [(h or 'Notes', c) for h, c in filled]
            page = board_route(ws.title, first)
            if page: out.append({'sheet': ws.title, 'page': page, 'title': title, 'sub': rest, 'fields': fields})
    print(f'oral boards: {len(out)} rows')
    return out

if __name__ == '__main__':
    ks, ob = sys.argv[1], sys.argv[2]
    data = {'trials': key_studies(ks), 'boards': oral_boards(ob)}
    (root/'data').mkdir(exist_ok=True)
    (root/'data'/'estes.json').write_text(json.dumps(data, ensure_ascii=False, indent=0))
    print('wrote data/estes.json', (root/'data'/'estes.json').stat().st_size // 1024, 'KB')
