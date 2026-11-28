"""Render data/estes.json (Rad Onc Tables, C. Estes; imported by tools/estes_import.py).

trials_panel(f, body): "Trial tables" tab on a tumour-site page (Key Studies routed to that page).
boards_panel(f):       "Oral boards" tab on a Phase 2 exam-summary page.
Text is reproduced as written (US spelling) and is not source-checked.
"""
import html, json, re
from pathlib import Path

root = Path(__file__).resolve().parent
_D = json.loads((root/'data'/'estes.json').read_text()) if (root/'data'/'estes.json').exists() else {'trials': [], 'boards': []}
SRC = 'Rad Onc Tables (Christopher Estes, MD)'

def _t(s):
    """Escape and keep line breaks."""
    s = html.escape(s.strip())
    s = re.sub(r'\n\s*\n', '<br><br>', s)
    return s.replace('\n', '<br>')

_MEET = r'(ASTRO|ASCO|ESTRO|ESMO|SABCS|ASH|AACR|GI ASCO|GU ASCO|WCLC|SNO|ASCO GI|ASCO GU)'
def year_label(cite, trial):
    yrs = []
    for line in cite.split('\n'):
        m = re.search(rf'{_MEET}\W*((?:19|20)\d\d)', line)
        if m: yrs.append(f'{m.group(1)} {m.group(2)}'); continue
        ys = re.findall(r'(?:19|20)\d\d', line)
        if ys: yrs.append(ys[-1])
    yrs = [y for i, y in enumerate(yrs) if y not in yrs[:i]]
    if not yrs:
        return 'protocol' if re.search(r'protocol|ongoing', trial + ' ' + cite, re.I) else 'year not given'
    if len(yrs) == 1: return yrs[0]
    return f'{yrs[0]}; {yrs[-1]}'

def _norm(s): return re.sub(r'[^a-z0-9]', '', re.sub(r'<[^>]+>|\(.*?\)|⭐️?', '', s.lower()))

def _key_names(body):
    names = set()
    for m in re.finditer(r'<div class="trial"><b>(.*?)</b>', body, re.S):
        for part in re.split(r'/|\+| and ', re.sub(r'<span class="yr">.*?</span>', '', m.group(1))):
            n = _norm(part)
            if len(n) >= 4: names.add(n)
    return names

def _trial(e, keyset):
    name = e['trial'].replace('\n', ' ').strip()
    star = '⭐' in name
    name = re.sub(r'\s*⭐️?', '', name).strip()
    yr = year_label(e['citation'], name)
    nn = _norm(name)
    tags = []
    if star: tags.append('<span class="et-tag et-star" title="Need-to-know trial (Estes)">need to know</span>')
    if e.get('recent'): tags.append('<span class="et-tag et-new">recent</span>')
    if nn and any(nn == k or (len(nn) >= 5 and (nn in k or k in nn)) for k in keyset):
        tags.append('<span class="et-tag">also in Key trials</span>')
    sub = html.escape(e['subtopic'].replace('\n', ' '))
    n = f' · n={html.escape(e["n"])}' if e['n'] and re.fullmatch(r'[\d,~>< ]+', e['n']) else ''
    meta = sub + n
    dl = []
    for k, lab in (('question','Question'),('patients','Patients'),('methods','Arms'),('results','Results'),('commentary','Commentary'),('notes','Notes')):
        if e.get(k): dl.append(f'<dt>{lab}</dt><dd>{_t(e[k])}</dd>')
    if e['citation']: dl.append(f'<dt>Citation</dt><dd>{_t(e["citation"])}</dd>')
    links = ' · '.join(f'<a href="{html.escape(u, quote=True)}" target="_blank" rel="noopener">{"PubMed" if "pubmed" in u or "ncbi" in u else "Paper"} {i+1}</a>' for i, u in enumerate(e['links'][:6]))
    if links: dl.append(f'<dt>Links</dt><dd>{links}</dd>')
    bl = _t(e['interpretation']) if e['interpretation'] else _t(e['results'].split('\n\n')[0])
    return (f'<div class="trial et{" et-k" if star else ""}"><b>{html.escape(name)} <span class="yr">({html.escape(yr)})</span></b>'
            f'<i>{meta}{"".join(tags)}</i><span>{bl}</span>'
            f'<details class="et-more"><summary>Details</summary><dl>{"".join(dl)}</dl></details></div>')

def _topic_label(t):
    t = re.sub(r'\s+', ' ', t).strip()
    return t[:1].upper() + t[1:] if t else 'Other'

def trials_panel(f, body):
    rows = [e for e in _D['trials'] if e.get('page') == f]
    if not rows: return ''
    keyset = _key_names(body)
    groups = {}
    for e in rows:
        t = _topic_label(e['topic']) if e['topic'] and e['topic'] != 'Introduction' else ''
        if e['sheet'] == 'Peds' and t.lower().startswith('hodgkin'): t = 'Paediatric Hodgkin'
        elif e['sheet'] == 'Peds' and t and not t.lower().startswith('cns'): t = 'Paediatric: ' + t
        groups.setdefault(t or '_intro', []).append(e)
    intro = groups.pop('_intro', [])
    cards = []
    for e in intro:
        if e['trial'] != 'Introduction' or not e['commentary']: continue
        cards.append(f'<article class="card et-intro" data-title="{html.escape(_topic_label(e["subtopic"]))} overview"><h3>{html.escape(_topic_label(e["subtopic"]))}: overview</h3><p>{_t(e["commentary"])}</p></article>')
    for t, es in groups.items():
        es = [e for e in es if e['trial'] != 'Introduction']
        if not es: continue
        cards.append(f'<article class="card" data-title="{html.escape(t)}"><h3>{html.escape(t)} <span class="et-count">{len(es)}</span></h3>'
                     + ''.join(_trial(e, keyset) for e in es) + '</article>')
    return ('\n<section class="panel" id="p-tables" data-tab="tables" data-label="Trial tables" data-src="estes" hidden>\n'
            '  <div class="panel-head">\n    <h2>Trial tables</h2>\n'
            '    <div class="et-tools"><input type="search" class="et-filter" placeholder="Filter trials on this tab" aria-label="Filter trials">'
            '<label><input type="checkbox" class="et-only"> Need to know only</label></div>\n'
            '    <div class="jump"></div>\n  </div>\n' + '\n'.join(cards) + '\n</section>')

def boards_panel(f):
    rows = [e for e in _D['boards'] if e.get('page') == f]
    if not rows: return ''
    cards = []
    for e in rows:
        if not e['title']:
            cards.append(f'<article class="card" data-title="Update note"><h3>Update note</h3><p>{_t(e["note"])}</p></article>'); continue
        title, extra = e['title'], e.get('sub', '')
        if len(title) > 55:
            m = re.match(r'(.{8,55}?)(?:\s\(|\.\s|,\s|:\s)(.*)', title)
            if m: title, extra = m.group(1), (m.group(2).rstrip(')') + ('\n' + extra if extra else ''))
        e = dict(e, title=title)
        sub = f'<p class="note">{_t(extra)}</p>' if extra else ''
        dl = ''.join(f'<dt>{html.escape(re.sub(r" \(full in reference tab\)", "", h))}</dt><dd>{_t(v)}</dd>' for h, v in e['fields'])
        cards.append(f'<article class="card ob" data-title="{html.escape(e["title"])}"><h3>{html.escape(e["title"])}</h3>{sub}<dl class="ob-dl">{dl}</dl></article>')
    return ('\n<section class="panel" id="p-boards" data-tab="boards" data-label="Oral boards" data-src="estes" hidden>\n'
            '  <div class="panel-head">\n    <h2>Oral boards tables</h2>\n'
            '    <div class="jump"></div>\n  </div>\n' + '\n'.join(cards) + '\n</section>')
