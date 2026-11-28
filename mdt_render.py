"""Renders mdt_data.py into page panels (used by build.py). Logic in assets/mdt.js."""
import re, html, json
from mdt_data import MATRICES, MDT_PAGES

_MDT = {m['id']: m for m in MATRICES}
LEDE = 'Red line: still to be established. (check): not yet verified against the source.'

def txt(x):
    x = html.escape(x, quote=False)
    x = re.sub(r'\[\[(.+?)\|(.+?)\]\]', r'<b>\1 <span class="yr">(\2)</span></b>', x)
    return re.sub(r'\{(.+?)\}', r'<span class="d">\1</span>', x)

def _matrix(m, first):
    mid = m['id']; off = '' if first else ' mdt-inactive'
    fs = ''
    for fd in m['fields']:
        show = f' data-show="{html.escape(json.dumps(fd["show"]))}"' if fd['show'] else ''
        opts = ''.join(f'<button type="button" class="mdt-o" data-v="{v}" aria-pressed="false">{html.escape(l)}</button>' for v, l in fd['opts'])
        fs += f'<fieldset class="mdt-f" data-f="{fd["id"]}"{show}><legend>{html.escape(fd["label"])}</legend><div class="mdt-opts">{opts}</div></fieldset>'
    note = f'<p class="note">{txt(m["note"])}</p>' if m.get('note') else ''
    out = [f'<div class="mdt-in{off}" data-m="{mid}" data-label="{html.escape(m["label"])}">{note}{fs}'
           '<p class="mdt-next" hidden></p><div class="mdt-bar"><span class="mdt-count"></span>'
           '<button type="button" class="mdt-reset">Clear case</button>'
           '<button type="button" class="mdt-compact" aria-pressed="false">Decisions only</button></div></div>']
    grp = None
    for r in m['rows']:
        g = re.sub(r'\W+', '-', r['grp'].lower()).strip('-')
        if r['grp'] != grp:
            grp = r['grp']
            out.append(f'<h3 class="mdt-grp{off}" data-m="{mid}" data-g="{g}">{html.escape(grp)}</h3>')
        when = r['when'] if isinstance(r['when'], list) else [r['when']]
        dl = ''.join(f'<div class="{c}"><dt>{lab}</dt><dd>{txt(r[k])}</dd></div>' for k, c, lab in
                     [('rec', 'rec', 'Decision'), ('alt', 'alt', 'Options'), ('rt', 'rt', 'RT'), ('ev', 'ev', 'Evidence'), ('ask', 'ask', 'Check')] if r[k])
        more = f'<p class="note"><a href="{r["more"][0]}">{html.escape(r["more"][1])} →</a></p>' if r.get('more') else ''
        cls = 'card mdt-row' + (' mdt-mod' if r['strict'] else '') + off
        st = ' data-strict' if r['strict'] else ''
        out.append(f'<article class="{cls}" data-m="{mid}" data-g="{g}" data-title="MDT: {html.escape(r["title"])}" '
                   f'data-when="{html.escape(json.dumps(when))}"{st}><h3>{html.escape(r["title"])}</h3><dl class="mdt-dl">{dl}</dl>{more}</article>')
    return '\n'.join(out)

def section(ids, tab='mdt', label='MDT decision matrix', head='MDT decision matrix', first=False):
    ms = [_MDT[i] for i in ids]
    sw = ''
    if len(ms) > 1:
        sw = ('<div class="mdt-switch" role="group" aria-label="Choose matrix">' +
              ''.join(f'<button type="button" class="mdt-pick" data-pick="{m["id"]}" aria-pressed="{"true" if i == 0 else "false"}">{html.escape(m["label"])}</button>' for i, m in enumerate(ms)) + '</div>')
    hid = '' if first else ' hidden'
    return (f'\n<section class="panel mdt-panel" id="p-{tab}" data-tab="{tab}" data-label="{html.escape(label)}"{hid}>\n'
            f'  <div class="panel-head"><h2>{html.escape(head)}</h2><p class="lede">{html.escape(LEDE)}</p>{sw}</div>\n'
            + '\n'.join(_matrix(m, i == 0) for i, m in enumerate(ms)) + '\n</section>\n')

def panel(f):
    ids = MDT_PAGES.get(f)
    return (section(ids) + '<script src="assets/mdt.js"></script>') if ids else ''

TOOL = [('prostate', 'Prostate', ['prostate']), ('pancreas', 'Pancreas', ['pancreas']),
        ('ugi', 'Upper GI', ['oesophagus', 'gastric', 'hcc', 'biliary', 'livermets']),
        ('rectum', 'Rectum', ['rectum']), ('lung', 'Lung', ['nsclc', 'sclc'])]

def tool_page():
    return ''.join(section(ids, tab=t, label=l, head=f'{l}: MDT decision matrix', first=(i == 0)) for i, (t, l, ids) in enumerate(TOOL)) + '<script src="assets/mdt.js"></script>'
