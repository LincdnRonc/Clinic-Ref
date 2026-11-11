"""Convert the Phase 2 'Super Summary' .docx into exam-summary page fragments.

Usage:  python3 tools/super_summary.py path/to/Super_Summary.docx
Writes src/exam-*.html (one per page in PAGES) and prints a page/tab/card count.

The source is one big Word table per tumour group: a full-width row is a group or
subsite heading, every other row holds topic cells (Epi, Path, Mgmt, EBRT, ...).
Each subsite becomes a tab and each cell a card. Text is reproduced as written
(apart from tumor -> tumour); figures are not copied, a note marks where one sits.

Formatting is applied by rule, not copied from the source's (uneven) bolding:
  h4 (accent colour): lines ending in ':', section words (Staging, Volumes...), short lines
      followed by a list ('Basal type'), numbered steps ('1. Surgery'), trial-name lines
      ('EORTC 22922', 'AMAROS – RT instead of ALND') and any line followed by 'P:'.
  bold: the leading 'Label:' of a line (P:, I:, O:, Dose:, Luminal A:) and trial names
      anywhere in the text (TRIAL_WORDS, TRIAL_PHRASES and cooperative-group + number).
  dose chips: 50Gy/25# style doses.  Add missing trial names to TRIAL_WORDS / TRIAL_PHRASES.
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


# ---- consistent inline formatting (source bold is ignored: it was applied unevenly) ----
TRIAL_WORDS = [  # matched case-sensitively, as whole words
 'ADAURA','ADRIATIC','AEGEAN','ALINA','AMAROS','ARASENS','ART-DECO','ARTDECO','ASCENDE-RT','AVATAR','BART','BC2001','BCON',
 'BILCAP','C-POST','CARMENA','CASPIAN','Caspian','CATNON','CHAARTED','CHHiP','CHISEL','CODEL','COMBI-AD','CONTINUUM','CONVERT',
 'CREST','CRITICS','CROSS','CURB','DART','DIAMOND','EBCTCG','EMBARK','ENCEPHALON','ENZAMET','ESOPEC','EUROPA','EXTEND','FABREC',
 'Fabrec','FROLIS','FLAME','FLYER','HEARTBEAT','HORRAD','HYBRID','HYPNO','HYPORT-STS','HYPO-RT-PC','INDIGO','INSEMA','INSEMNA',
 'Insema','INTERLACE','IMpower133','LACC','LANA-1','LATITUDE','LAURA','LUSTRE','MAGIC','MARCH','MATTERHORN','MERCURY','NADINA',
 'NICHE','NIAGARA','OCAT','OLIGOMA','OPRA','ORATOR','ORIOLE','OUTBACK','PACIFIC','PET-PLAN','PIVOT','POLCAGB','POP-RT','POSEIDON',
 'PROSPECT','PROTECT','ProtecT','PROTEUS','QUARTZ','RADICALS','RADIOSA','RAIDER','RAPCHEM','RAPIDO','RAVES','ROADS','ROSEL','RUBY',
 'SABR-COMET','SANO','SENOMAC','Senomac','SHERBERT','SINODAR-ONE','SMART','SOUND','Sound','SPAN-C','SPPORT','STAMPEDE','STARS',
 'STOMP','STOPCAP','STRASS','STREXIT','SUPREMO','SURTIME','THORA','TOPGEAR','VALSG','VISION','VORTEX','WOLVERINE','iROCK','IROCK',
 'iSABR','ARTISTIC','DBCG','ACCORD','CAPP','Codel','De-escalate','Doremy','FORT','Florence','GORTEC','LYSA','Landoni',
 'Mammosite','MINDACT','POST','ProPSMA','ROCS','SEMPET','Treasure','UNFOLDER','B24','DELPHI-306','STELLAR','VESPER','Oligoma',
 'Trendy','TRENDY','I-MAT','TARGIT','sweDCIS','TAM-01','Bonner','Hoskin','Lowry','NOVEL','HYPO-PMRT','DADSPPORT','MARCAP','GROINSS-V','Senti-MERORL','TARGIT-A','SKAGEN','EORTC','EMBRACE','RetroEMBRACE',
]
TRIAL_PHRASES = [  # matched case-insensitively
 'RT CHARM','IMPORT HIGH','IMPORT LOW','FAST-FORWARD','FAST FORWARD','FASTRACK II','PRIME II','UK START B','START B','START A',
 'LUNG-ART','LUNG ART','MARS II','PEACE V STORM','NON BELIEVERS','DUTCH TME','STOCKHOLM III','VA LARYNX','NEO-AEGIS','SCORAD III',
 'SC.24','GROINSS VII','GROINSS-V II','HOSKIN TRIAL','LOWRY TRIAL','CHINESE NCC','MILAN','PATCHELL','TOPAZ-1','RASOLUTE 302',
 'SAKK 01/10','SAK 01/10','SAKK 17/04','TROG BIG 07.01','TROG BIG','DBCG IMN 2','DBCG-IMN','DBCG IMN','CALGB/ALLIANCE 140503',
 'ESO-SHANGHAI','EMBRACE II','EMBRACE I','DBCG SKAGEN','NEOCRTEC5010','ROAM','EXPERT',
]
_GRP = (r'RTOG|NRG[\s-]?[A-Z]{2}|NRG|EORTC|TROG|CALGB|NSABP(?:[\s-]?B)?|ECOG(?:\s?E)?|SWOG(?:\s?S)?|JCOG|GOG|ACOSOG[\s-]?Z|DBCG|NCIC(?:\s?[A-Z]{2}\.)?|CCTG|'
        r'Alliance|NCCTG\s?N|INT|Intergroup|GHSG\s?HD|HD|KEYNOTE|Keynote|CHECKMATE|CheckMate|Checkmate|PORTEC|PACE|PREOPANC|PRODIGE|SARC|ESPAC|'
        r'CONKO|IESLG|FLOT|ACNS|AREN|ANBL|ARST|AEWS|NOA|GETUG(?:-AFU)?|ARTIST|ACT|NADIM|PEACE|PLATO|SIOP|UKCCCR\s?ACT|TROG\s?BIG|EV|CE|LAP')
TRIAL_RE = re.compile(
    r'(?<![\w-])(?:'
    + r'(?:' + _GRP + r')[\s\-.]?(?:[A-Z]{1,2}(?=\d)|[A-Z](?=\s|$|[,);:]))?\d(?:[\d.\-/]*\d)?[A-Za-z]?(?:\s?(?:I{1,3}|IV)\b)?'   # group + number
    + r'|(?:PACE|ACT|PEACE)\s?(?:[A-C]|I{1,3}|IV|[1-5])\b'
    + r'|[ESN]\d{4}[A-Z]?|N\d{3}[A-Z]|Z-?0?0?11|MA[.\s]?(?:20|17)'
    + r'|' + '|'.join(sorted((re.escape(w) for w in TRIAL_WORDS), key=len, reverse=True))
    + r')(?![\w-])')
TRIAL_CI = re.compile(r'(?<![\w-])(?:' + '|'.join(sorted((re.escape(w).replace(r'\ ', r'\s') for w in TRIAL_PHRASES), key=len, reverse=True)).replace('MILAN', r'MILAN(?!\s+criteria)') + r')(?![\w-])', re.I)
# words that look like group+number but are not trials
NOT_TRIAL = re.compile(r'^(?:E\d|S\d|N\d|Z\d{1}$|HD\d?$|CE\d|MA\d{2,}|INT\d?$|ACT\d|EV\d?$|N[0-3][a-c]?$|E[1-9]$|S[0-9]$)')
def _trial_ok(m):
    t = m.group(0)
    if t.startswith('ECOG') and not re.search(r'\d{4}', t): return False   # ECOG 0-1 = performance status
    if re.fullmatch(r'[ESNZ]\d+[A-Za-z]?', t):          # E3311 / S1001 / N107C / Z0011 / Z11
        return bool(re.fullmatch(r'Z0?0?11|[ESN]\d{3,}[A-Z]?', t)) and t != 'S100'
    if re.fullmatch(r'(?:HD|CE|EV|MA|INT|LAP)[\s.-]?\d+', t):
        return bool(re.fullmatch(r'(?:HD[\s-]?1\d|CE\.?6|EV-?30\d|MA[.\s]?20|MA[.\s]?17|INT[\s-]?0\d{3}|LAP[\s-]?0?7)', t))
    if re.fullmatch(r'(?:ACT)[\s-]?\d.*', t): return False
    return True
def _outside_tags(h, fn):
    parts = re.split(r'(<b>.*?</b>|<span class="d">.*?</span>|<[^>]+>)', h)
    return ''.join(p if (i % 2) else fn(p) for i, p in enumerate(parts))
def bold_trials(h):
    def one(seg):
        seg = TRIAL_CI.sub(lambda m: f'<b>{m.group(0)}</b>', seg)
        return _outside_tags(seg, lambda s2: TRIAL_RE.sub(lambda m: f'<b>{m.group(0)}</b>' if _trial_ok(m) else m.group(0), s2))
    return _outside_tags(h, one)
LABEL_RE = re.compile(r'^([A-Z0-9][A-Za-z0-9 /&+()\-–≤≥.,\'’]{0,26}?)\s?:(?=\s|$)')
def fmt_inline(text, label=True):
    h = ausp(html.escape(text.strip()))
    if label:
        m = LABEL_RE.match(h)
        if m and not re.fullmatch(r'\d+', m.group(1)):
            h = f'<b>{m.group(1)}:</b>' + h[m.end():]
    h = bold_trials(h)
    h = _outside_tags(h, dose)
    h = h.replace('</b><b>', '').replace('\n', '<br>')
    return h
def starts_with_trial(text):
    """True if the line is a trial heading: a trial name, optionally followed by a short qualifier."""
    h = bold_trials(html.escape(text.strip()))
    m = re.match(r'^<b>[^<]+</b>', h)
    if not m: return False
    rest = re.sub(r'<[^>]+>', '', h[m.end():]).strip()
    return rest == '' or bool(re.match(r'^(?:[–\-:/&(,]|trial|et al|vs\b|and\b|\d|[A-Z]{2,}|\w+\)?\s*$)', rest)) and len(text) <= 70

SECTION_WORDS = {'rf','rfs','risk factors','staging','pathology','path','ddx','work-up','workup','work up','mgmt','management','toxicities',
 'toxicity','volumes','oars','sim','simulation','dose','f/u','follow-up','follow up','fu','prognosis','evidence','trials','natural hx',
 'natural history','presentation','screening','investigations','ix','ihc','molecular','genetics','technique','planning','pre-invasive',
 'invasive','subtypes','classification','anatomy','epi','biological subtypes','gene panel','genetic testing','acute','late','side effects',
 'indications','contraindications','treatment','surveillance','imaging','examination','history','diagnosis','histology','pathophysiology'}

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
        h = fmt_inline(text) if text.strip() else ''
        allbold = bool(out) and all(b for s, b in out if s.strip())
        ppr = p.find(qn('w:pPr'))
        lvl, fmt, nid = None, None, None
        if ppr is not None:
            np_ = ppr.find(qn('w:numPr'))
            if np_ is not None and np_.find(qn('w:numId')) is not None:
                nid = np_.find(qn('w:numId')).get(qn('w:val'))
                il = np_.find(qn('w:ilvl')); il = il.get(qn('w:val')) if il is not None else '0'
                if nid != '0':
                    lvl, fmt = int(il), self.numfmt.get((nid, il), 'bullet')
                else:
                    nid = None
        imgs = len(list(p.iter(A_BLIP)))
        boxes = []
        for ch in p.iter(MC + 'Choice'):
            for tb in ch.iter(qn('w:txbxContent')):
                for bp in tb.findall(qn('w:p')):
                    t = ''.join(s for s, _ in self.runs(bp)).strip()
                    if t: boxes.append(t)
        return dict(text=text.strip(), html=h.strip(), bold=allbold, lvl=lvl, fmt=fmt, nid=nid, imgs=imgs, boxes=boxes)

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
                cells.append('<br>'.join(fmt_inline(p['text'], label=False) for p in ps if p['text']))
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
        """items -> (title, html). Title = first short heading-like line.
        Headings (h4) are decided by rule, not by the source's bolding:
          - a short line ending in ':' (or a known section word such as Staging, Volumes)
          - a short line followed directly by a list (e.g. '1. Surgery', 'Basal type')
          - a trial name line (e.g. 'EORTC 22922', 'AMAROS – RT instead of ALND') or any line followed by 'P:'
        Lines typed with a leading dash become list items."""
        blocks, title, imgnote = [], None, False
        for kind, x in items:
            if kind == 't':
                blocks.append(('raw', self.mini_table(x))); continue
            p = dict(x)
            if p['imgs']: imgnote = True
            for b in p['boxes']:
                if len(b) >= 25: blocks.append(('raw', f'<p class="box">{fmt_inline(b)}</p>'))
            t = p['text']
            if not t: continue
            if p['lvl'] is None and re.match(r'^[-•▪]\s*\S', t):
                t = re.sub(r'^[-•▪]\s*', '', t)
                p.update(text=t, html=fmt_inline(t), lvl=0, fmt='bullet')
            if title is None and p['lvl'] is None:
                m = re.match(r'^([A-Za-z][^:\n]{0,38}?)\s*:\s*(.*)$', t, re.S)
                if len(t) <= 40:
                    title = t.rstrip(':').strip(); continue
                if m and m.group(2):
                    title = m.group(1).strip()
                    rest = m.group(2).strip()
                    blocks.append(('p', dict(p, text=rest, html=fmt_inline(rest)))); continue
                title = ' '.join(t.split()[:4])
            blocks.append(('li' if p['lvl'] is not None else 'p', p))
        # Word numbered steps (1., 2., ...) that carry their own bullet sub-points become numbered headings,
        # matching the typed '1. Surgery' style; long ones stay list items with the bullets nested under them.
        ORD = ('decimal', 'lowerLetter', 'lowerRoman', 'upperLetter', 'upperRoman')
        counters, shift = {}, None
        for n, (k, p) in enumerate(blocks):
            if k != 'li': shift = None; continue
            if p['fmt'] in ORD:
                key = (p['nid'], p['lvl'])
                counters[key] = counters.get(key, 0) + 1
                nk2 = blocks[n + 1] if n + 1 < len(blocks) else (None, None)
                has_sub = nk2[0] == 'li' and (nk2[1]['lvl'] > p['lvl'] or (nk2[1]['lvl'] == p['lvl'] and nk2[1]['fmt'] not in ORD))
                if has_sub and p['lvl'] == 0 and len(p['text']) <= 80:
                    t = f"{counters[key] if p['fmt'] == 'decimal' else chr(96 + counters[key])}. {p['text']}"
                    blocks[n] = ('p', dict(p, text=t, html=fmt_inline(t), lvl=None, numhead=True))
                    shift = None
                elif has_sub:
                    shift = p['lvl']
                else:
                    shift = None
            elif shift is not None and p['lvl'] == shift:
                p['lvl'] = shift + 1
        out, stack = [], []
        def close_to(level):
            while len(stack) > level:
                out.append('</li></' + stack.pop() + '>')
        NUM = re.compile(r'^\d{1,2}\s?[.)]\s?[A-Za-z]')
        num_idx = [n for n, (k, p) in enumerate(blocks) if k == 'p' and NUM.match(p['text']) and len(p['text']) <= 55]
        num_head = any(n + 1 < len(blocks) and blocks[n + 1][0] == 'li' for n in num_idx)
        for n, (kind, p) in enumerate(blocks):
            if kind == 'raw':
                close_to(0); out.append(p); continue
            if kind == 'li':
                lv = p['lvl'] + 1
                tag = 'ol' if p['fmt'] in ('decimal', 'lowerLetter', 'lowerRoman', 'upperLetter', 'upperRoman') else 'ul'
                if len(stack) < lv:
                    while len(stack) < lv:
                        last = len(stack) == lv - 1
                        out.append(f'<{tag}><li>' if last else '<ul><li>'); stack.append(tag if last else 'ul')
                    out.append(p['html'])
                elif stack[lv - 1] != tag:
                    close_to(lv - 1); out.append(f'<{tag}><li>' + p['html']); stack.append(tag)
                else:
                    close_to(lv); out.append('</li><li>' + p['html'])
                continue
            close_to(0)
            t = p['text']
            if re.fullmatch(r'[_\-–—=*. ]{5,}', t):
                out.append('<hr>'); continue
            nxt = blocks[n + 1] if n + 1 < len(blocks) else (None, None)
            nk, nt = nxt[0], (nxt[1]['text'] if nxt[0] in ('p', 'li') else '')
            core = t.rstrip(': ').strip()
            single = bool(re.fullmatch(r'[A-Z]', core))
            colon_label = t.endswith(':') and 3 <= len(t) <= 60 and not single and '\n' not in t
            section = core.lower() in SECTION_WORDS
            before_list = nk == 'li' and len(t) <= 45 and not t.endswith('.') and not re.search(r'\S:\s+\S', t) and not single and t.count(',') < 2
            mnemonic = nk == 'p' and len(t) <= 40 and re.match(r'^[A-Z]\s?[-–]\s?\w', nt) and not re.match(r'^[A-Z]\s?[-–]', t)
            topic = len(t) <= 45 and not re.search(r'[<>≤≥%]|\dGy|\bvs\b', t) and (
                re.search(r'\b(scores?|staging|stage|grading|classification|criteria|outcomes|histology|groups|assay|types|borders|subtypes|algorithm|stratification)\b\)?$', t, re.I)
                or re.match(r'^Mgmt\s?[–-]', t)
                or re.fullmatch(r'(Low|Intermediate|High|Very high|Favourable|Unfavourable) risk|Resectable|Unresectable|Borderline resectable|Primary|Outcomes|Prognosis|Advanced stage|Early stage|Grade \d|WHO G\d|\d+ ?yr OS', t.strip(' :–-'), re.I))
            trial = (starts_with_trial(t) and not t.endswith('.') and not re.search(r':\s+\S', t)) \
                    or (nk == 'p' and re.match(r'^P\s?:', nt) and len(t) <= 70 and not re.match(r'^[A-Z]\s?:', t))
            statement = re.search(r'[<>≤≥%]|\dGy|\b(is|are|was|were|has|have|can|should|shows?|showed|presents?)\b', t)
            if before_list and statement: before_list = False
            letter_label = re.match(r'^(?:[A-Z0-9]\s?[:\-–]\s|[A-Z] [A-Z][a-z])', t)
            numbered = (num_head and n in num_idx) or p.get('numhead')
            if numbered: core = re.sub(r'^(\d{1,2})\s?([.)])\s?', r'\1\2 ', core)
            if numbered or (not letter_label and (colon_label or section or before_list or trial or mnemonic or topic)):
                out.append(f'<h4>{dose(ausp(html.escape(core if not t.endswith(")") else t.strip())))}</h4>')
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
