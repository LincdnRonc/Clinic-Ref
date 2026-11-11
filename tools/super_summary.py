"""Convert the Phase 2 'Super Summary' .docx into exam-summary page fragments.

Usage:  python3 tools/super_summary.py path/to/Super_Summary.docx
Writes src/exam-*.html (one per page in PAGES) and prints a page/tab/card count.

The source is one big Word table per tumour group: a full-width row is a group or
subsite heading, every other row holds topic cells (Epi, Path, Mgmt, EBRT, ...).
Each subsite becomes a tab and each cell a card. Text is reproduced as written
(apart from tumor -> tumour); figures are not copied, a note marks where one sits.
"""
import sys, re, html, pathlib
import docx
from docx.oxml.ns import qn

ROOT = pathlib.Path(__file__).resolve().parent.parent
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
A_BLIP = '{http://schemas.openxmlformats.org/drawingml/2006/main}blip'
MC = '{http://schemas.openxmlformats.org/markup-compatibility/2006}'

# subsite heading (as in the source, upper case) -> (page file, tab id, tab label)
TABS = {
 'MEMORY AIDS': ('exam-overview.html', 'memory', 'Memory aids'),
 'CERVIX': ('exam-gyn.html', 'cervix', 'Cervix'),
 'UTERINE': ('exam-gyn.html', 'uterine', 'Uterine'),
 'VULVA': ('exam-gyn.html', 'vulva', 'Vulva'),
 'VAGINAL': ('exam-gyn.html', 'vaginal', 'Vagina'),
 'OROPHARYNX': ('exam-hn.html', 'oropharynx', 'Oropharynx'),
 'ORAL CAVITY': ('exam-hn.html', 'oral', 'Oral cavity'),
 'LARYNX': ('exam-hn.html', 'larynx', 'Larynx'),
 'HYPOPHARYNX': ('exam-hn.html', 'hypopharynx', 'Hypopharynx'),
 'HNCUP': ('exam-hn.html', 'cup', 'Unknown primary'),
 'NASOPHARYNX': ('exam-hn.html', 'nasopharynx', 'Nasopharynx'),
 'SINONASAL': ('exam-hn.html', 'sinonasal', 'Sinonasal'),
 'SALIVARY GLAND': ('exam-hn.html', 'salivary', 'Salivary'),
 'RECURRENT H&N CA': ('exam-hn.html', 'recurrent', 'Recurrent'),
 'NODAL VOLUMES': ('exam-hn.html', 'nodes', 'Nodal volumes'),
 'DCIS': ('exam-breast.html', 'dcis', 'DCIS'),
 'EBC': ('exam-breast.html', 'early', 'Early breast'),
 'LABC': ('exam-breast.html', 'labc', 'Locally advanced'),
 'OLIGOMETASTATIC': ('exam-breast.html', 'oligo', 'Oligometastatic'),
 'BREAST CA IN PREGNANCY': ('exam-breast.html', 'pregnancy', 'Pregnancy'),
 'MALE BREAST CANCER': ('exam-breast.html', 'male', 'Male breast'),
 'SOFT TISSUE SARCOMA': ('exam-sarcoma.html', 'sts', 'Soft tissue'),
 'OSTEOSARCOMA': ('exam-sarcoma.html', 'osteo', 'Osteosarcoma'),
 'CHONDROSARCOMA & CHORDOMA': ('exam-sarcoma.html', 'chondro', 'Chondrosarcoma & chordoma'),
 'DESMOID TUMORS': ('exam-sarcoma.html', 'desmoid', 'Desmoid'),
 'BLADDER': ('exam-gu.html', 'bladder', 'Bladder'),
 'KIDNEY': ('exam-gu.html', 'kidney', 'Kidney'),
 'TESTICULAR': ('exam-gu.html', 'testis', 'Testis'),
 'PENILE': ('exam-gu.html', 'penile', 'Penile'),
 'FIRPC': ('exam-prostate.html', 'low', 'Low & fav. intermediate'),
 'UIRPC': ('exam-prostate.html', 'unfav', 'Unfav. intermediate'),
 'HRPC & VHRPC': ('exam-prostate.html', 'high', 'High & very high'),
 'OLIGO MET/RECURRENT PCA': ('exam-prostate.html', 'oligo', 'Oligometastatic'),
 'PALLIATIVE RECURRENT PCA': ('exam-prostate.html', 'palliative', 'Palliative'),
 'SALVAGE RT': ('exam-prostate.html', 'salvage', 'Salvage RT'),
 'ADT': ('exam-prostate.html', 'adt', 'ADT'),
 'EARLY STAGE NSCLC': ('exam-thorax.html', 'early', 'Early NSCLC'),
 'LOCALLY ADVANCED NSCLC': ('exam-thorax.html', 'la', 'Locally advanced NSCLC'),
 'LS SMALL CELL LUNG CANCER': ('exam-thorax.html', 'ls', 'Limited SCLC'),
 'ES SMALL CELL LUNG CANCER': ('exam-thorax.html', 'es', 'Extensive SCLC'),
 'MESOTHELIOMA': ('exam-thorax.html', 'meso', 'Mesothelioma'),
 'TYHMOMA': ('exam-thorax.html', 'thymoma', 'Thymoma'),
 'FOLLICULAR LYMPHOMA': ('exam-heme.html', 'fl', 'Follicular'),
 'MARGINAL ZONE LYMPHOMA': ('exam-heme.html', 'mzl', 'Marginal zone'),
 'DLBCL': ('exam-heme.html', 'dlbcl', 'DLBCL'),
 'PRIMARY CNS LYMPHOMA': ('exam-heme.html', 'pcnsl', 'Primary CNS'),
 'PMBCL': ('exam-heme.html', 'pmbcl', 'PMBCL'),
 'OTHER BCL & TLS': ('exam-heme.html', 'otherb', 'Other B-cell'),
 'HODGKIN LYMPHOMA': ('exam-heme.html', 'hodgkin', 'Hodgkin'),
 'T CELL LYMPHOMA': ('exam-heme.html', 'tcell', 'T-cell'),
 'MYELOMA': ('exam-heme.html', 'myeloma', 'Myeloma'),
 'PLASMACYTOMA': ('exam-heme.html', 'plasmacytoma', 'Plasmacytoma'),
 'LEUKAEMIA': ('exam-heme.html', 'leukaemia', 'Leukaemia & TBI'),
 'THYROID': ('exam-endocrine-benign.html', 'thyroid', 'Thyroid'),
 'ADRENAL': ('exam-endocrine-benign.html', 'adrenal', 'Adrenal'),
 'THYROID ORBITOPATHY': ('exam-endocrine-benign.html', 'orbitopathy', 'Thyroid eye disease'),
 'HETEROTROPHIC OSSIFCATION': ('exam-endocrine-benign.html', 'ho', 'Heterotopic ossification'),
 'KELOID': ('exam-endocrine-benign.html', 'keloid', 'Keloid'),
 'AVM': ('exam-endocrine-benign.html', 'avm', 'AVM'),
 'OTHER BENIGN': ('exam-endocrine-benign.html', 'otherbenign', 'Other benign'),
 'BASAL CELL CARCINOMA': ('exam-skin.html', 'bcc', 'BCC'),
 'SQUAMOUS CELL CARCINOMA': ('exam-skin.html', 'scc', 'cSCC'),
 'MERKEL CELL CARCINOMA': ('exam-skin.html', 'merkel', 'Merkel'),
 'KAPOSI’S SARCOMA': ('exam-skin.html', 'kaposi', 'Kaposi'),
 'AFX & PDS': ('exam-skin.html', 'afx', 'AFX & PDS'),
 'MELANOMA': ('exam-skin.html', 'melanoma', 'Melanoma'),
 'GRADE 1-3 GLIOMA': ('exam-cns.html', 'lgg', 'Grade 1–3 glioma'),
 'GRADE 4 GLIOMA': ('exam-cns.html', 'gbm', 'Grade 4 glioma'),
 'MENINGIOMA': ('exam-cns.html', 'meningioma', 'Meningioma'),
 'GERM CELL TUMORS': ('exam-cns.html', 'germ', 'Germ cell'),
 'PINEAL TUMORS': ('exam-cns.html', 'pineal', 'Pineal'),
 'EPENDYMOMA': ('exam-cns.html', 'ependymoma', 'Ependymoma'),
 'VESTIBULAR SCHWANOMMA': ('exam-cns.html', 'vs', 'Vestibular schwannoma'),
 'PITNET': ('exam-cns.html', 'pitnet', 'PitNET'),
 'GASTRIC': ('exam-ugi.html', 'gastric', 'Gastric'),
 'GIST': ('exam-ugi.html', 'gist', 'GIST'),
 'OESOPHAGUS': ('exam-ugi.html', 'oesophagus', 'Oesophagus'),
 'HCC': ('exam-ugi.html', 'hcc', 'HCC'),
 'CHOLANGIOCARCINOMA': ('exam-ugi.html', 'cholangio', 'Cholangiocarcinoma'),
 'PANCREAS': ('exam-ugi.html', 'pancreas', 'Pancreas'),
 'NEUROENDOCRINE': ('exam-ugi.html', 'net', 'Neuroendocrine'),
 'RECTAL': ('exam-lgi.html', 'rectal', 'Rectum'),
 'COLON': ('exam-lgi.html', 'colon', 'Colon'),
 'ANAL': ('exam-lgi.html', 'anal', 'Anal'),
 'WILMS TUMOR': ('exam-peds.html', 'wilms', 'Wilms'),
 'NEUROBLASTOMA': ('exam-peds.html', 'nb', 'Neuroblastoma'),
 'EWINGS SARCOMA': ('exam-peds.html', 'ewing', 'Ewing'),
 'RHABDOMYOSARCOMA': ('exam-peds.html', 'rms', 'RMS'),
 'MEDULLOBLASTOMA': ('exam-peds.html', 'medullo', 'Medulloblastoma'),
 'CRANIOPHARYNGIOMA': ('exam-peds.html', 'cranio', 'Craniopharyngioma'),
 'DIFFUSE MIDLINE GLIOMA': ('exam-peds.html', 'dmg', 'Diffuse midline glioma'),
 'SURVIVORSHIP': ('exam-peds.html', 'survivorship', 'Survivorship'),
 'PAEDIATRICS RT': ('exam-peds.html', 'pedsrt', 'Paediatric RT'),
 'BONE METS': ('exam-pall.html', 'bone', 'Bone mets'),
 'SPINE SABR': ('exam-pall.html', 'spine', 'Spine SABR'),
 'LIVER METS': ('exam-pall.html', 'liver', 'Liver mets'),
 'BRAIN METS': ('exam-pall.html', 'brain', 'Brain mets'),
 'CHEMOTHERAPY': ('exam-clinonc.html', 'chemo', 'Chemotherapy'),
 'TARGETED THERAPY': ('exam-clinonc.html', 'targeted', 'Targeted'),
 'RADIONUCLIDE THERAPY': ('exam-clinonc.html', 'radionuclide', 'Radionuclide'),
 'ACUP': ('exam-clinonc.html', 'acup', 'ACUP'),
 'IMMUNOTHERAPY': ('exam-clinonc.html', 'immuno', 'Immunotherapy'),
 'SVCO': ('exam-clinonc.html', 'svco', 'SVCO'),
 'HYPERCALCAEMIA': ('exam-clinonc.html', 'calcium', 'Hypercalcaemia'),
 'SPINAL CORD COMPRESSION': ('exam-clinonc.html', 'mscc', 'Cord compression'),
 'OTHER': ('exam-clinonc.html', 'emergencies', 'Other emergencies'),
 'RADIOSENSITISNG SYNDROMES': ('exam-clinonc.html', 'radiosensitivity', 'Radiosensitivity'),
 'CLINICAL TRIALS & PROMS': ('exam-clinonc.html', 'trials', 'Trials & PROMs'),
 'RT PLANNING': ('exam-clinonc.html', 'planning', 'RT planning'),
 'VIVA TEMPLATES': ('exam-viva.html', 'viva', 'Viva templates'),
}
GROUP_ROWS = {'GYNAECOLOGY','HEAD AND NECK','BREAST','SARCOMA','GENITOURINARY','PROSTATE','THORAX','HAEMATOLOGY',
              'ENDOCRINE','BENIGN','SKIN','CNS','UGI','LOWER GI','PAEDIATRICS','PALLIATVE','CLINICAL ONCOLOGY'}
# continuation of the previous subsite after a figure placed between tables
CONTINUE_HINTS = {}

# Wingdings arrow used throughout the source
SYM = {'F0E0': '→', 'F0E8': '→', 'F0DF': '←', 'F0E1': '↑', 'F0E2': '↓', 'F0FC': '✓'}
DOSE = re.compile(r'(?<![\w.])(\d+(?:\.\d+)?(?:\s?-\s?\d+(?:\.\d+)?)?\s?Gy(?:\s?/\s?\[?\d+(?:\.\d+)?\]?\s?(?:Gy)?)*\s?(?:/|in)\s?\d+(?:\s?-\s?\d+)?\s?#)')
def dose(s): return DOSE.sub(r'<span class="d">\1</span>', s)
def ausp(s):
    s = re.sub(r'(?<=[\s\w)\]%#])\s?à\s?(?=[\s\w(+\-])', ' → ', s)  # 'à' typed in Wingdings = arrow
    s = re.sub(r'\b([Tt])umor', r'\1umour', s)
    return re.sub(r'\bTUMOR', 'TUMOUR', s)

class Conv:
    def __init__(self, path):
        self.d = docx.Document(path)
        self.numfmt = {}
        try:
            num = self.d.part.numbering_part.element
            absfmt = {}
            for an in num.findall(qn('w:abstractNum')):
                aid = an.get(qn('w:abstractNumId'))
                for lvl in an.findall(qn('w:lvl')):
                    f = lvl.find(qn('w:numFmt'))
                    absfmt[(aid, lvl.get(qn('w:ilvl')))] = f.get(qn('w:val')) if f is not None else 'bullet'
            for n in num.findall(qn('w:num')):
                aid = n.find(qn('w:abstractNumId')).get(qn('w:val'))
                for il in range(9):
                    self.numfmt[(n.get(qn('w:numId')), str(il))] = absfmt.get((aid, str(il)), 'bullet')
        except Exception:
            pass

    # ---- inline text of one paragraph (text boxes excluded) ----
    def runs(self, p):
        segs = []
        def walk(el):
            for ch in el:
                t = ch.tag
                if t == qn('w:r'):
                    rpr = ch.find(qn('w:rPr'))
                    b = False; sup = False
                    if rpr is not None:
                        be = rpr.find(qn('w:b'))
                        b = be is not None and be.get(qn('w:val')) not in ('0', 'false')
                        va = rpr.find(qn('w:vertAlign'))
                        sup = va is not None and va.get(qn('w:val')) == 'superscript'
                    for x in ch:
                        if x.tag == qn('w:t'):
                            tx = x.text or ''
                            if sup and tx.strip() in ('o', '0'): tx = '°'
                            segs.append((tx, b))
                        elif x.tag == qn('w:tab'): segs.append((' ', b))
                        elif x.tag in (qn('w:br'), qn('w:cr')): segs.append(('\n', b))
                        elif x.tag == qn('w:sym'): segs.append((SYM.get(x.get(qn('w:char')).upper(), ''), b))
                elif t in (qn('w:hyperlink'), qn('w:smartTag'), qn('w:ins'), qn('w:fldSimple')) or t.endswith('}sdt') or t.endswith('}sdtContent'):
                    walk(ch)
        walk(p)
        return segs

    def para(self, p):
        segs = self.runs(p)
        text = ''.join(s for s, _ in segs)
        out, cur, curb = [], '', None
        for s, b in segs:
            if b != curb and cur:
                out.append((cur, curb)); cur = ''
            cur += s; curb = b
        if cur: out.append((cur, curb))
        h = ''
        for s, b in out:
            e = dose(ausp(html.escape(s))).replace('\n', '<br>')
            if b and s.strip(): h += f'<b>{e}</b>'
            else: h += e
        allbold = bool(out) and all(b for s, b in out if s.strip())
        ppr = p.find(qn('w:pPr'))
        lvl, fmt = None, None
        if ppr is not None:
            np_ = ppr.find(qn('w:numPr'))
            if np_ is not None and np_.find(qn('w:numId')) is not None:
                nid = np_.find(qn('w:numId')).get(qn('w:val'))
                il = np_.find(qn('w:ilvl')); il = il.get(qn('w:val')) if il is not None else '0'
                if nid != '0':
                    lvl, fmt = int(il), self.numfmt.get((nid, il), 'bullet')
        imgs = len(list(p.iter(A_BLIP)))
        boxes = []
        for ch in p.iter(MC + 'Choice'):
            for tb in ch.iter(qn('w:txbxContent')):
                for bp in tb.findall(qn('w:p')):
                    t = ''.join(s for s, _ in self.runs(bp)).strip()
                    if t: boxes.append(t)
        return dict(text=text.strip(), html=h.strip(), bold=allbold, lvl=lvl, fmt=fmt, imgs=imgs, boxes=boxes)

    # ---- block content of a table cell ----
    def blocks(self, tc):
        items = []
        for ch in tc:
            if ch.tag == qn('w:p'): items.append(('p', self.para(ch)))
            elif ch.tag == qn('w:tbl'): items.append(('t', ch))
            elif ch.tag.endswith('}sdt'):
                for c2 in ch.iter(qn('w:p')): items.append(('p', self.para(c2)))
        return items

    def mini_table(self, tbl):
        rows = []
        for tr in tbl.findall(qn('w:tr')):
            cells = []
            for tc in tr.findall(qn('w:tc')):
                ps = [self.para(p) for p in tc.iter(qn('w:p'))]
                cells.append('<br>'.join(p['html'] for p in ps if p['html']))
            if any(cells): rows.append(cells)
        if not rows: return ''
        n = max(len(r) for r in rows)
        wide = ' wide' if n >= 4 else ''
        out = [f'<div class="tw{wide}"><table class="xs">']
        for i, r in enumerate(rows):
            tag = 'th' if i == 0 and all(len(re.sub('<[^>]+>', '', c)) < 60 for c in r) and len(rows) > 1 else 'td'
            out.append('<tr>' + ''.join(f'<{tag}>{c}</{tag}>' for c in r) + '</tr>')
        out.append('</table></div>')
        return ''.join(out)

    def render(self, items):
        """items -> (title, html). Title = first short heading-like line."""
        out, stack, title = [], [], None
        def close_to(level):
            while len(stack) > level:
                out.append('</li></' + stack.pop() + '>')
        imgnote = False
        for kind, x in items:
            if kind == 't':
                close_to(0); out.append(self.mini_table(x)); continue
            p = x
            if p['imgs']: imgnote = True
            for b in p['boxes']:
                if len(b) >= 25:
                    close_to(0); out.append(f'<p class="box">{dose(ausp(html.escape(b)))}</p>')
            if not p['html']: continue
            if title is None and p['lvl'] is None:
                t = p['text']
                m = re.match(r'^([A-Za-z][^:\n]{0,38}?)\s*:\s*(.*)$', t, re.S)
                if len(t) <= 40:
                    title = t.rstrip(':').strip(); continue
                if m and m.group(2):
                    title = m.group(1).strip()
                    rest = re.sub(r'^(<b>)?' + re.escape(html.escape(m.group(1))) + r'\s*:?\s*(</b>)?\s*:?\s*', '', p['html'])
                    out.append(f'<p>{rest}</p>'); continue
                title = ' '.join(t.split()[:4])
            if p['lvl'] is not None:
                lv = p['lvl'] + 1
                tag = 'ol' if p['fmt'] in ('decimal', 'lowerLetter', 'lowerRoman', 'upperLetter', 'upperRoman') else 'ul'
                if len(stack) < lv:
                    while len(stack) < lv:
                        out.append(f'<{tag}><li>' if len(stack) == lv - 1 else '<ul><li>'); stack.append(tag if len(stack) == lv - 1 else 'ul')
                    out.append(p['html'])
                else:
                    close_to(lv); out.append('</li><li>' + p['html'])
                continue
            close_to(0)
            t = p['text']
            if re.fullmatch(r'[_\-–—=*. ]{5,}', t):
                out.append('<hr>'); continue
            if (p['bold'] or (t.endswith(':') and len(t) < 50)) and 4 <= len(t) <= 60:
                out.append(f'<h4>{p["html"]}</h4>')
            else:
                out.append(f'<p>{p["html"]}</p>')
        close_to(0)
        if imgnote:
            out.append('<p class="note fig">Figure in the original document (not reproduced here).</p>')
        body = '\n'.join(out)
        body = re.sub(r'<li>\s*</li>', '', body)
        return (title or '').strip(), body

TITLE = {'Epi': 'Epidemiology', 'Mgmt': 'Management', 'Path': 'Pathology', 'OARS': 'OARs', 'DDx': 'Differential diagnosis',
         'Natural Hx': 'Natural history', 'RF': 'Risk factors', 'Mgmt paradigm': 'Management paradigm', 'Epi/RF': 'Epidemiology and risk factors'}
def tidy_title(t):
    t = re.sub(r'\s+', ' ', t).strip()
    return TITLE.get(t, t)

def cell_text(tc):
    return ''.join(t.text or '' for t in tc.iter(qn('w:t'))).strip()

def norm(s): return re.sub(r'\s+', ' ', s.replace(' ', ' ')).strip().upper()

def convert(path):
    c = Conv(path)
    body = c.d.element.body
    tabs = {}      # (file, tab) -> dict(label, cards)
    order = []
    cur = None
    def add_card(title, h, key=False):
        if cur is None or not h.strip(): return
        tabs[cur]['cards'].append((title, h, key))
    def start(head):
        nonlocal cur
        f, tid, label = TABS[head]
        cur = (f, tid)
        if cur not in tabs:
            tabs[cur] = dict(label=label, cards=[]); order.append(cur)
    for el in body:
        if el.tag == qn('w:p'):
            p = c.para(el)
            if p['text'].upper().startswith('AUSTRALIAN EPIDEMIOLOGY'):
                continue
            if p['imgs'] and cur:
                note = p['text'] or 'Figure'
                add_card(note if p['text'] else 'Figure', '<p class="note fig">Figure in the original document (not reproduced here).</p>')
            continue
        if el.tag != qn('w:tbl'): continue
        rows = el.findall(qn('w:tr'))
        viva = norm(cell_text(rows[0].findall(qn('w:tc'))[0])) == 'VIVA TEMPLATES'
        i = 0
        while i < len(rows):
            tcs = rows[i].findall(qn('w:tc'))
            texts = [cell_text(tc) for tc in tcs]
            nimg = sum(len(list(tc.iter(A_BLIP))) for tc in tcs)
            if len(tcs) == 1:
                t = norm(texts[0])
                if not t: i += 1; continue
                if t in GROUP_ROWS: i += 1; continue
                if t in TABS and nimg == 0:
                    start(t); i += 1; continue
            # leukaemia comparison: header row of short labels, then rows with the same cell count
            if len(tcs) >= 3 and all(0 < len(x) <= 4 for x in texts):
                hdr = texts; body_rows = []
                j = i + 1
                while j < len(rows) and len(rows[j].findall(qn('w:tc'))) == len(tcs):
                    body_rows.append([c.render(c.blocks(tc)) for tc in rows[j].findall(qn('w:tc'))]); j += 1
                tb = ['<div class="tw wide"><table class="xs"><tr>' + ''.join(f'<th>{html.escape(h)}</th>' for h in hdr) + '</tr>']
                for r in body_rows:
                    tb.append('<tr>' + ''.join(f'<td><b>{html.escape(t)}</b> {h}</td>' if t and not h.startswith('<p>' + html.escape(t)) else f'<td>{h}</td>' for t, h in r) + '</tr>')
                tb.append('</table></div>')
                add_card('Comparison: ' + ', '.join(hdr), ''.join(tb).replace('<p>', ' ').replace('</p>', ' '))
                i = j; continue
            if viva:
                label = re.sub(r'\s+', ' ', texts[0]).strip()
                parts = [c.render(c.blocks(tc)) for tc in tcs[1:]]
                h = ''.join((f'<h4>{html.escape(t)}</h4>' if t and len(tcs) > 2 else '') + b for t, b in parts)
                # first cell may hold several lines (e.g. "UGI Oesophagus")
                first = c.render(c.blocks(tcs[0]))
                ttl = ' · '.join(x for x in [first[0], re.sub('<[^>]+>', ' ', first[1]).strip()] if x) or label
                if len(tcs) > 2:
                    h = ''.join(f'<h4>{html.escape(t)}</h4>{b}' for t, b in [first] + parts)
                    ttl = 'SRS Dmax limits'
                add_card(ausp(ttl), h)
                i += 1; continue
            for tc in tcs:
                if not cell_text(tc) and not list(tc.iter(A_BLIP)): continue
                title, h = c.render(c.blocks(tc))
                if not title: title = 'Figure'
                title = tidy_title(title)
                key = bool(re.match(r'(EBRT|SABR|SBRT|SRS|PMRT|WBRT|Dose|Definitive|Adj|Post-op|Curative|NA |TSET|Small field|LDR|PCI|RT for|Neoadjuvant|Unresectable|Involved)', title, re.I))
                add_card(ausp(title), h, key)
            i += 1
    return tabs, order

def frag(tabs, order, f, intro=None):
    out = []
    first = True
    for key in order:
        if key[0] != f: continue
        tab = tabs[key]
        tid = key[1]
        titles = []
        for t, _, _ in tab['cards']:
            s = re.sub(r'\s+', ' ', t).strip()
            if s and s not in titles and s != 'Figure': titles.append(s)
        lede = ' · '.join(titles[:8])
        hid = '' if first else ' hidden'
        out.append(f'<section class="panel" id="p-{tid}" data-tab="{tid}" data-label="{html.escape(tab["label"])}"{hid}>\n  <div class="panel-head">\n    <h2>{html.escape(tab["label"])}</h2>\n    <p class="lede">{html.escape(lede)}</p>\n    <!--xref:{tid}-->\n    <div class="jump"></div>\n  </div>')
        if first and intro: out.append(intro)
        seen = {}
        for t, h, k in tab['cards']:
            t = re.sub(r'\s+', ' ', t).strip()
            n = seen.get(t, 0) + 1; seen[t] = n
            dt = t if n == 1 else f'{t} ({n})'
            out.append(f'  <article class="card{" key" if k else ""}" data-title="{html.escape(dt)}">\n    <h3>{html.escape(t)}</h3>\n{h}\n  </article>')
        out.append('</section>')
        first = False
    return '\n'.join(out) + '\n'

EPI = '''<section class="panel" id="p-epi" data-tab="epi" data-label="Australian epidemiology">
  <div class="panel-head">
    <h2>Australian epidemiology</h2>
    <p class="lede">Most common cancers by new cases and by deaths, estimated for 2025 (ranked from the charts in the source document).</p>
    <div class="jump"></div>
  </div>
  <article class="card key" data-title="Incidence 2025">
    <h3>New cases, 2025 (top 10)</h3>
    <ol><li>Prostate</li><li>Breast</li><li>Melanoma of the skin</li><li>Lung</li><li>Colorectal</li><li>Non-Hodgkin lymphoma</li><li>Kidney</li><li>Pancreas</li><li>Thyroid</li><li>Uterine</li></ol>
  </article>
  <article class="card key" data-title="Mortality 2025">
    <h3>Cancer deaths, 2025 (top 10)</h3>
    <ol><li>Lung</li><li>Colorectal</li><li>Pancreas</li><li>Prostate</li><li>Breast</li><li>Liver</li><li>Non-Hodgkin lymphoma</li><li>Cancer of unknown primary</li><li>Brain</li><li>Melanoma of the skin</li></ol>
  </article>
</section>
'''

if __name__ == '__main__':
    tabs, order = convert(sys.argv[1])
    files = []
    for f, _ in order:
        if f not in files: files.append(f)
    for f in files:
        txt = frag(tabs, order, f)
        if f == 'exam-overview.html':
            txt = EPI + txt.replace(' data-label="Memory aids">', ' data-label="Memory aids" hidden>', 1)
        (ROOT / 'src' / f).write_text(txt)
        n = sum(len(tabs[k]['cards']) for k in order if k[0] == f)
        print(f, 'tabs', sum(1 for k in order if k[0] == f), 'cards', n)
