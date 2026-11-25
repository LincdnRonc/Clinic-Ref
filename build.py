from version import VERSION, VERSION_DATE
import re, pathlib, html
root = pathlib.Path(__file__).resolve().parent
GU = [
 ('gu-prostate.html','Prostate','Prostate','Risk groups, fractionation menu, brachytherapy, post-op and salvage RT, metastatic disease, ADT, consent numbers.'),
 ('gu-bladder.html','Bladder','Bladder','Trimodality therapy selection and doses, post-cystectomy RT, NMIBC, perioperative immunotherapy.'),
 ('gu-kidney.html','Kidney','Kidney','SABR for primary RCC (FASTRACK II), oligometastatic RCC, holding systemic therapy, IMDC.'),
 ('gu-testis.html','Testis','Testis','Seminoma by stage, para-aortic and dog-leg fields, INRT (SAKK 01/10), markers, follow-up.'),
 ('gu-other.html','UTUC, urethra & penile','UTUC, urethra and penile','Upper tract urothelial, urethral and penile cancer, plus Peyronie\'s disease.'),
]
GYN = [
 ('gyn-cervix.html','Cervix','Cervix','Surgery vs chemoRT by stage, Sedlis/Peters adjuvant RT, INTERLACE and KEYNOTE-A18, MRI-guided brachytherapy doses and limits.'),
 ('gyn-endometrial.html','Endometrial','Endometrial','Adjuvant RT by risk and molecular class, VBT and boost schedules, inoperable disease, uterine sarcoma.'),
 ('gyn-vulva-vagina.html','Vulva & vagina','Vulva and vagina','SLNB and groin RT (GROINSS-V), margins, chemoRT doses, vaginal brachytherapy.'),
 ('gyn-general.html','General gynae','General gynae','Nodal volumes, constraints, IMRT evidence, toxicity, re-irradiation and ovarian cancer.'),
]
GI = [
 ('gi-oesophagus-gastric.html','Oesophagus & gastric','Oesophagus and gastric','Oesophageal, GOJ and gastric cancer: perioperative strategy, definitive chemoRT, organ preservation, palliation.'),
 ('gi-pancreas.html','Pancreas','Pancreas','Resectability, neoadjuvant and adjuvant therapy, SBRT dosing and constraints, coeliac plexus radiosurgery.'),
 ('gi-hepatobiliary.html','Liver & biliary','Liver and biliary','HCC SBRT by liver function, liver metastases, gallbladder and cholangiocarcinoma.'),
 ('gi-rectum-colon.html','Rectum & colon','Rectum and colon','MRI risk groups, SCRT vs LCCRT, TNT, watch-and-wait, planning volumes, metastatic CRC.'),
 ('gi-anal.html','Anal','Anal canal','5-FU/MMC chemoRT, dose-painted IMRT, 26-week response assessment, de-escalation.'),
 ('gi-general.html','General GI','General GI','Liver and pelvic constraints, proctitis, re-irradiation, NETs, small bowel, oligometastases.'),
]
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&family=Barlow+Semi+Condensed:wght@500;600;700&display=swap" rel="stylesheet">'
FOOT = '<footer><p>Synthesised from the RadOncReview GI document (collaborative, US-centric: NCCN, ASTRO, ASCO), including 2025–26 guidelines and ASTRO \'26 abstracts. Doses are as reported in the source and its trials. Check eviQ, departmental protocols and drug availability before prescribing.</p></footer>'
from eviq_links import EVIQ
# Quick-launch icons in the page header (own icons, not the services' logos)
APPLINKS = (
 '<nav class="applinks" aria-label="Quick launch" style="display:flex;gap:6px">'
 + ''.join(
  f'<a href="{u}" target="_blank" rel="noopener" title="{t}" aria-label="{t}" class="al" '
  f'style="display:flex;flex-direction:column;align-items:center;gap:2px;text-decoration:none;color:#5b6675;font-size:10px;line-height:1">'
  + (f'<img src="{g}" alt="" width="30" height="30" class="al-img" style="width:30px;height:30px;flex:none;border-radius:8px;display:block">' if bg == 'img' else
  f'<svg viewBox="0 0 24 24" width="30" height="30" aria-hidden="true" '
  f'style="width:30px;height:30px;flex:none;border-radius:8px;padding:3px;box-sizing:border-box;background:{bg}">{g}</svg>')
  + f'<span>{lab}</span></a>'
  for u,t,lab,bg,g in [
   ('https://keep.google.com/','Google Keep','Keep','#f4b400',
    '<path d="M12 4.5a5 5 0 0 0-3 9v1.8h6v-1.8a5 5 0 0 0-3-9z" fill="#fff"/><rect x="9.6" y="16.4" width="4.8" height="2.2" rx=".8" fill="#fff"/>'),
   ('https://tasks.google.com/','Google Tasks','Tasks','#2f6fde',
    '<path d="M6.5 12.5l3.6 3.6 7.4-7.6" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>'),
   ('https://anywhere.genesiscare.com.au/','GenesisCare Anywhere (remote access)','Genesis','img','assets/icon-genesis.png'),
   ('https://tpro-au.com/signin','T Pro dictation (sign in)','T Pro','#1f4e8c',
    '<rect x="9.2" y="3.8" width="5.6" height="10" rx="2.8" fill="#fff"/><path d="M6.6 11.4a5.4 5.4 0 0 0 10.8 0M12 16.8v3M9 19.8h6" fill="none" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/>'),
   ('https://scribe.heidihealth.com/en/','Heidi scribe (sign in)','Heidi','#5b3f8f',
    '<path d="M5 6.2A1.7 1.7 0 0 1 6.7 4.5h10.6A1.7 1.7 0 0 1 19 6.2v8.1a1.7 1.7 0 0 1-1.7 1.7h-6.8L7 19.3V16h-.3A1.7 1.7 0 0 1 5 14.3z" fill="none" stroke="#fff" stroke-width="1.7" stroke-linejoin="round"/><path d="M8.8 10.2v0M10.9 8.4v3.6M13 7.5v5.4M15.1 9.1v2.2" stroke="#fff" stroke-width="1.6" stroke-linecap="round"/>'),
  ])
 + ''.join(  # site shortcuts: same tab, own icons
  f'<a href="{u}" title="{t}" aria-label="{t}" class="al al-site" '
  f'style="display:flex;flex-direction:column;align-items:center;gap:2px;text-decoration:none;color:#5b6675;font-size:10px;line-height:1">'
  f'<svg viewBox="0 0 24 24" width="30" height="30" aria-hidden="true" '
  f'style="width:30px;height:30px;flex:none;border-radius:8px;padding:3px;box-sizing:border-box;background:{bg}">{g}</svg>'
  f'<span>{lab}</span></a>'
  for u,t,lab,bg,g in [
   ('links.html#radiology','Radiology portals','Radiology','#35596b',
    '<rect x="4.5" y="4.5" width="15" height="15" rx="2" fill="none" stroke="#fff" stroke-width="1.8"/><path d="M12 7v10M8.5 9.5c1.5.6 2.5.6 3.5 0 1 .6 2 .6 3.5 0M8.5 12.5c1.5.6 2.5.6 3.5 0 1 .6 2 .6 3.5 0M9 15.5c1.2.5 2 .5 3 0 1 .5 1.8.5 3 0" fill="none" stroke="#fff" stroke-width="1.4" stroke-linecap="round"/>'),
   ('links.html#pathology','Pathology results','Pathology','#9b1c3f',
    '<path d="M10 4.5h4M11 4.5v5.2l-4.3 7.6A1.6 1.6 0 0 0 8.1 19.7h7.8a1.6 1.6 0 0 0 1.4-2.4L13 9.7V4.5" fill="none" stroke="#fff" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/><path d="M8.7 15h6.6" stroke="#fff" stroke-width="1.6" stroke-linecap="round"/>'),
   ('links.html#forms','Request and referral forms','Forms','#a14a0b',
    '<path d="M7 3.8h7l3.5 3.5v12.9H7z" fill="none" stroke="#fff" stroke-width="1.8" stroke-linejoin="round"/><path d="M13.8 3.8v3.7h3.7M9.5 11.5h5.5M9.5 14.5h5.5M9.5 17.3h3.5" fill="none" stroke="#fff" stroke-width="1.5" stroke-linecap="round"/>'),
   ('contacts.html','Phone and contact list','Contacts','#0d7366',
    '<path d="M8.2 4.6l2 3.6-1.6 1.6a10 10 0 0 0 5.6 5.6l1.6-1.6 3.6 2-.9 2.9c-.2.6-.8 1-1.5.9A14 14 0 0 1 4.4 7a1.4 1.4 0 0 1 .9-1.5z" fill="none" stroke="#fff" stroke-width="1.7" stroke-linejoin="round"/>'),
  ])
 + '<!--MEETING_LINK-->'  # Teams meeting icon: added at deploy from the MEETING_URL secret (tools/private_links.py)
 # Log out (always last): StatiCrypt clears the remembered password when the URL has ?staticrypt_logout
 + '<a href="?staticrypt_logout" title="Log out" aria-label="Log out" class="al al-logout" '
   'style="display:flex;flex-direction:column;align-items:center;gap:2px;text-decoration:none;color:#5b6675;font-size:10px;line-height:1">'
   '<svg viewBox="0 0 24 24" width="30" height="30" aria-hidden="true" '
   'style="width:30px;height:30px;flex:none;border-radius:8px;padding:3px;box-sizing:border-box;background:#5b6675">'
   '<path d="M13.5 8V5.5a1 1 0 0 0-1-1H6a1 1 0 0 0-1 1v13a1 1 0 0 0 1 1h6.5a1 1 0 0 0 1-1V16" fill="none" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
   '<path d="M9.5 12h10M16.5 8.8l3.2 3.2-3.2 3.2" fill="none" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
   '</svg><span>Log out</span></a>'
 + '</nav>')

def eviq_panel(f):
    items = EVIQ.get(f)
    if not items: return ''
    li = ''.join(f'<li><a href="{html.escape(u)}" target="_blank" rel="noopener">{(html.escape(i)+" · ") if i else ""}{html.escape(t)}</a></li>' for i,t,u in items)
    return f'''
<section class="panel" id="p-eviq" data-tab="eviq" data-label="eviQ protocols" hidden>
  <div class="panel-head">
    <h2>eviQ protocols</h2>
    <div class="jump"></div>
  </div>
  <article class="card key" data-title="eviQ links">
    <h3>Protocols on eviQ</h3>
    <ul class="eviq">{li}</ul>
    <p class="note">eviQ Cancer Treatments Online, Cancer Institute NSW (eviq.org.au). This site is not affiliated with or endorsed by eviQ or the Cancer Institute NSW. Check the protocol version and your departmental protocols before use.</p>
  </article>
</section>
'''
CTR_SITE = {'ctr-breast.html':'breast','ctr-thorax.html':'thorax','ctr-hn.html':'hn','ctr-skin.html':'hn','ctr-cns.html':'cns','ctr-peds.html':'cns',
 'ctr-upper-gi.html':'gi','ctr-anal.html':'gi','ctr-gyn.html':'gyn','ctr-heme.html':'heme','ctr-sarcoma.html':'sarcoma','ctr-spine.html':'pall',
 'ctr-bladder.html':'gu','ctr-kidney-liver.html':'gu','contouring/prostate.html':'gu','contouring/bladder.html':'gu','contouring/rectal-long-course.html':'gi','contouring/liver-sbrt.html':'gi','contouring/thorax.html':'thorax','contouring/biliary.html':'gi','contouring/pancreas-stomach.html':'gi','contouring/oesophagus.html':'gi','contouring/breast.html':'breast','contouring/gynae.html':'gyn','contouring/anal.html':'gi','contouring/spine-bone.html':'pall','contouring/cns.html':'cns','contouring/wbrt.html':'cns','contouring/brain-mets.html':'cns','contouring/head-neck.html':'hn','contouring/lymphoma.html':'heme','ctr-library.html':'contouring','ctr-mim.html':'contouring','ctr-monaco.html':'contouring'}
def _ds(f): return f' data-site="{CTR_SITE[f]}"' if f in CTR_SITE else ''
def sitenav(current, group):
    links = ['<a href="index.html">Home</a>']
    for f,short,_,_ in group:
        cur = ' aria-current="page"' if f==current else ''
        links.append(f'<a href="{f}"{cur}{_ds(f)}>{html.escape(short)}</a>')
    return '<nav class="sitenav" aria-label="All pages">' + ''.join(links) + '</nav>'
def tree(current):
    """Collapsible all-pages menu: one <details> per group, current group open."""
    groups = [(gid, head, pages) for gid,_,head,pages,_ in GROUPS] + [('contouring','Contouring',CNAV), ('tools','Tools',TOOLS)]
    out = []
    for gid, head, pages in groups:
        here = any(pg[0]==current for pg in pages)
        links, last = '', None
        for pg in pages:
            sub = CGROUP_OF.get(pg[0]) if gid == 'contouring' else None
            if sub and sub != last: links += f'<span class="tree-sub">{html.escape(sub)}</span>'; last = sub
            links += f'<a href="{pg[0]}"{" aria-current=\"page\"" if pg[0]==current else ""}>{html.escape(pg[1])}</a>'
        out.append(f'<details data-site="{gid}"{" open" if here else ""}><summary>{html.escape(head)}</summary>{links}</details>')
    return ('<details class="menu"><summary><span class="burger" aria-hidden="true"></span>All pages</summary>'
            '<nav class="tree" aria-label="All pages"><a class="home" href="index.html">Home</a>' + ''.join(out) + '</nav></details>')
from exam_links import EXAM, FOOT_EXAM, XREF
def _tablabels(f):
    t = (root/'src'/f).read_text()
    return dict(re.findall(r'data-tab="([^"]+)" data-label="([^"]+)"', t))
def xref_bar(f):
    if f not in XREF: return ''
    links = []
    for ef, tab in XREF[f]:
        lab = _tablabels(ef).get(tab, tab)
        links.append(f'<a href="{ef}#{tab}">{lab}</a>')
    return '<p class="xref" data-site="exam"><b>Exam summary:</b> ' + ' · '.join(links) + '</p>'
def xref_back(f, body):
    def rep(m):
        tab = m.group(1)
        back = [cf for cf, lst in XREF.items() if (f, tab) in lst]
        if not back: return ''
        names = {g[0]: g[2] for _,_,_,pages,_ in GROUPS for g in pages}
        return '<p class="xref"><b>Clinic page:</b> ' + ' · '.join(f'<a href="{cf}">{html.escape(names.get(cf, cf))}</a>' for cf in back) + '</p>'
    return re.sub(r'<!--xref:([\w-]+)-->', rep, body)
_SCORETAB = {'breast':('breast','Breast'),'gu':('prostate','Prostate'),'thorax':('lung','Lung'),'cns':('cns','CNS'),'gi':('gi','Liver and GI'),'gyn':('gynae','Gynae'),'pall':('bone','Bone and spine'),'sarcoma':('bone','Bone (Mirels)'),'heme':('heme','Lymphoma'),'hn':('general','Head and neck')}
_SYSLINK = {'breast':('sys-breast-endocrine.html','Breast endocrine therapy'),'gu':('sys-prostate-adt.html','Prostate ADT'),'pall':('sys-bone.html','Bone agents')}
def tools_bar(gid):
    if gid not in _SCORETAB: return ''
    t,l = _SCORETAB[gid]
    x,xl = _SYSLINK.get(gid, ('sys-chemort.html','Concurrent chemo-RT'))
    return f'<p class="xref"><b>Systemic therapy:</b> <a href="{x}">{xl}</a> · <a href="sys-timing.html">Targeted and immunotherapy with RT</a> · <a href="sys-supportive.html">Supportive drugs</a> · <b>Reirradiation:</b> <a href="rert-principles.html">principles</a>, <a href="rert-constraints.html">limits and calculators</a></p><p class="xref"><b>Calculators:</b> <a href="scores.html#{t}">{l} scores and nomograms</a> · <a href="tools.html">EQD2, BED and re-irradiation</a></p>'
def related_bar(f, gid):
    rows = re.findall(r'<p class="xref"[^>]*>(.*?)</p>', xref_bar(f) + tools_bar(gid), re.S)
    if not rows: return ''
    return '<details class="related"><summary>Related</summary>' + ''.join(f'<div class="rel-row">{r}</div>' for r in rows) + '</details>'
DISCLAIMER = '<footer class="disclaimer"><p><b>Private resource, not for distribution.</b> This site is the author\'s own working reference and is not intended for use by anyone else. It may contain errors, omissions or out-of-date information, and is not medical advice or a medical device. Anyone who accesses it does so entirely at their own risk, must rely on their own clinical judgement, and must independently verify all information (including doses, volumes, constraints, scores and calculator results) against primary sources and local protocols. To the fullest extent permitted by law, the author accepts no responsibility or liability for any loss, injury or damage arising from use of, or reliance on, any content on this site.</p></footer>'
STAGERS = {'nccn':'Prostate NCCN risk group','breast':'Breast (AJCC 8 anatomic stage)','lung':'Lung (TNM 9th edition)','prostate':'Prostate (AJCC 8)','crc':'Colon and rectum (AJCC 8)','anal':'Anal canal (AJCC 8)',
 'oes_scc':'Oesophagus, squamous (AJCC 8 clinical)','oes_ac':'Oesophagus, adenocarcinoma (AJCC 8 clinical)','gastric':'Stomach (AJCC 8 clinical)','pancreas':'Pancreas (AJCC 8)','hcc':'Hepatocellular carcinoma (AJCC 8)',
 'hn':'Oral cavity, larynx, hypopharynx, p16-negative oropharynx (AJCC 8)','opc':'Oropharynx, p16-positive (AJCC 8 clinical)','npc':'Nasopharynx (AJCC 8)','bladder':'Bladder (AJCC 8)','kidney':'Kidney (AJCC 8)',
 'cervix':'Cervix (FIGO 2018)','endo':'Endometrium (FIGO 2009)','lugano':'Lymphoma (Lugano)'}
STAGE_PAGES = {'breast-early.html':['breast'],'breast-nodes-pmrt.html':['breast'],'breast-planning.html':['breast'],'thorax-early.html':['lung'],'thorax-stage3.html':['lung'],'thorax-sclc.html':['lung'],'thorax-metastatic.html':['lung'],
 'gu-prostate.html':['nccn','prostate'],'gu-bladder.html':['bladder'],'gu-kidney.html':['kidney'],'gi-oesophagus-gastric.html':['oes_scc','oes_ac','gastric'],'gi-pancreas.html':['pancreas'],'gi-hepatobiliary.html':['hcc'],
 'gi-rectum-colon.html':['crc'],'gi-anal.html':['anal'],'gyn-cervix.html':['cervix'],'gyn-endometrial.html':['endo'],'hn-oropharynx.html':['opc','hn'],'hn-larynx.html':['hn'],'hn-oral-salivary.html':['hn'],
 'hn-npc-sinonasal.html':['npc'],'hn-general.html':['hn','opc','npc'],'heme-hodgkin.html':['lugano'],'heme-nhl.html':['lugano'],'scores.html':list(STAGERS)}
import mdt_render as _mdt
(root/'src'/'mdt.html').write_text(_mdt.tool_page())
def stage_panel(f):
    ids = STAGE_PAGES.get(f)
    if not ids: return ''
    cards_ = ''.join(f'<article class="card{" key" if i==0 else ""}" data-title="{html.escape(STAGERS[k])}"><h3>{html.escape(STAGERS[k])}</h3><div data-stage="{k}"></div></article>' for i,k in enumerate(ids))
    return f'''
<section class="panel" id="p-staging" data-tab="staging" data-label="Staging &amp; risk" hidden>
  <div class="panel-head"><h2>Auto-staging and risk groups</h2><p class="lede">A cross-check, not a substitute for the staging manual: T definitions are abbreviated.</p><div class="jump"></div></div>
  {cards_}
</section>
<script src="assets/staging.js"></script>'''
# ---- Consent numbers: a "Toxicity & consent" tab on each tumour-site page ----
# Pages without their own consent figures show the shared rates from a sibling page (copied at build, not indexed twice).
CONSENT_FROM = {
 'breast-early.html':'breast-planning.html', 'breast-nodes-pmrt.html':'breast-planning.html',
 'hn-larynx.html':'hn-general.html', 'hn-npc-sinonasal.html':'hn-general.html', 'hn-oral-salivary.html':'hn-general.html',
 'hn-oropharynx.html':'hn-general.html', 'hn-thyroid-cup.html':'hn-general.html',
 'pall-brain.html':'pall-wbrt.html',
}
_PRINTBTN = '<p><button type="button" class="printbtn" onclick="window.print()">Print consent sheet</button></p>'
def _consent_print(body):
    return re.sub(r'(<section class="panel" id="p-consent"[^>]*>\s*<div class="panel-head">.*?<div class="jump"></div>)', lambda m: m.group(1) + _PRINTBTN, body, count=1, flags=re.S)
def consent_panel(f):
    src_f = CONSENT_FROM.get(f)
    if not src_f or 'id="p-consent"' in (root/'src'/f).read_text(): return ''
    m = re.search(r'<section class="panel" id="p-consent"[^>]*>.*?<div class="jump"></div>\s*</div>(.*?)</section>', (root/'src'/src_f).read_text(), re.S)
    if not m: return ''
    names = {g[0]: g[2] for _,_,_,pages,_ in GROUPS for g in pages}
    return (f'\n<section class="panel" id="p-consent" data-tab="consent" data-label="Toxicity &amp; consent" data-borrowed="{src_f}" hidden>\n'
            f'  <div class="panel-head">\n    <h2>Toxicity and consent numbers</h2>\n'
            f'    <p class="lede">From the <a href="{src_f}#consent">{html.escape(names.get(src_f, src_f))}</a> page.</p>\n'
            f'    <div class="jump"></div>{_PRINTBTN}\n  </div>\n{m.group(1).strip()}\n</section>')
def exam_panel(f):
    """'Exam notes' tab: the matching Phase 2 exam-summary tabs (XREF), copied at build time, not indexed twice."""
    if f not in XREF: return ''
    parts = []
    for ef, tab in XREF[f]:
        m = re.search(rf'<section class="panel" id="p-{re.escape(tab)}" data-tab="{re.escape(tab)}" data-label="([^"]+)"[^>]*>.*?<div class="jump"></div>\s*</div>(.*?)</section>', (root/'src'/ef).read_text(), re.S)
        if not m: continue
        label, cards_ = m.group(1), re.sub(r'<!--.*?-->', '', m.group(2), flags=re.S).strip()
        if not cards_: continue
        parts.append(f'<div class="gather"><article class="card gather-head" data-title="{label}"><h3>{label}</h3><p class="note">From the <a href="{ef}#{tab}">exam summary</a>.</p></article>{cards_}</div>')
    if not parts: return ''
    return ('\n<section class="panel gathered" id="p-exam" data-tab="exam" data-label="Exam notes" data-borrowed="exam" hidden>\n'
            '  <div class="panel-head">\n    <h2>Exam notes</h2>\n'
            '    <p class="lede">AS\'s Phase 2 summary, as written and not source-checked. Where it disagrees with this page, go by this page.</p>\n'
            '    <div class="jump"></div>\n  </div>\n' + ''.join(parts) + '\n</section>')
MORE_TABS = True  # rarely used tabs (eviQ, Guidelines, Exam notes) behind a "More" chip; set False to revert
_MORE_JS = '<script src="assets/more-tabs.js"></script>' if MORE_TABS else ''
# Tab order on tumour-site pages: overview/general tab if there is one, Staging & risk, management tabs in author order,
# (planning tabs stay beside their management tab), toxicity and consent, key trials, MDT matrix, then eviQ / Guidelines / Exam notes.
TUMOUR_GIDS = {'breast','cns','gi','gu','gyn','heme','hn','sarcoma','thorax','pall'}
def _tab_rank(tid, label):
    l = html.unescape(label).lower()
    if tid in ('stage', 'staging'): return 1
    if tid in ('eviq','guidelines','exam'): return 8
    if tid == 'mdt' or 'mdt' in l: return 7
    if 'key trials' in l: return 6
    if l.startswith('toxicity'): return 5
    return 2
_LEAD_RE = r'overview|approach|general|management|decide'
_SIDE_TABS = ('staging','stage','consent','trials','mdt','eviq','guidelines','exam')
def add_overview(body):
    """Tumour-site pages without an overview/general first tab get a generated Overview tab built only from
    the page's own tab bottom lines (no new content). Marked data-generated so search does not index it twice."""
    secs = list(re.finditer(r'<section class="panel[^"]*"[^>]*>.*?</section>', body, re.S))
    if not secs: return body
    lab0 = html.unescape(re.search(r'data-label="([^"]*)"', secs[0].group(0)).group(1)).lower()
    if re.search(_LEAD_RE, lab0): return body
    rows, side = [], []
    for m in secs:
        t = m.group(0)
        tid = re.search(r'data-tab="([^"]*)"', t).group(1); lab = re.search(r'data-label="([^"]*)"', t).group(1)
        if tid in _SIDE_TABS or 'key trials' in lab.lower() or lab.lower().startswith('toxicity'):
            side.append((tid, lab)); continue
        head = re.search(r'<div class="panel-head">(.*?)<div class="jump">', t, re.S)
        led = re.search(r'<p class="lede"[^>]*>(.*?)</p>', head.group(1), re.S) if head else None
        rows.append(f'<dt><a href="#{tid}">{lab}</a></dt>' + (f'<dd>{led.group(1).strip()}</dd>' if led else ''))
    order = {'staging':0,'stage':0,'consent':1,'trials':2,'mdt':3}
    side = [x for x in sorted(side, key=lambda x: order.get(x[0], 4 if 'trials' not in x[1].lower() else 2)) if x[0] not in ('eviq','guidelines','exam','staging','stage')]
    also = ' · '.join(f'<a href="#{t}">{l}</a>' for t, l in side)
    ov = ('<section class="panel" id="p-overview" data-tab="overview" data-label="Overview" data-generated="1">\n'
          '  <div class="panel-head"><h2>Overview</h2><div class="jump"></div></div>\n'
          f'  <article class="card key" data-title="At a glance"><h3>At a glance</h3><dl class="ov">{"".join(rows)}</dl></article>\n'
          + (f'  <article class="card" data-title="Also on this page"><h3>Also on this page</h3><p>{also}</p></article>\n' if also else '')
          + '</section>\n')
    return body[:secs[0].start()] + ov + body[secs[0].start():]
def merge_staging(body):
    """Fold the Staging & risk panel into the first (overview) panel; keeps id="staging" so old #staging links work."""
    m = re.search(r'<section class="panel" id="p-staging"[^>]*>(.*?)</section>\s*', body, re.S)
    if not m: return body
    inner = m.group(1)
    head = re.search(r'<div class="panel-head">.*?<div class="jump"></div></div>', inner, re.S)
    cards_ = inner[head.end():] if head else inner
    block = ('<p class="note" id="staging"><b>Staging and risk:</b> a cross-check, not a substitute for the staging manual; '
             'T definitions are abbreviated.</p>\n' + cards_.strip() + '\n')
    body = body[:m.start()] + body[m.end():]
    first = re.search(r'<section class="panel[^"]*"[^>]*>.*?</section>', body, re.S)
    end = first.end() - len('</section>')
    return body[:end] + block + body[end:]
def order_tabs(body):
    secs = list(re.finditer(r'<section class="panel[^"]*"[^>]*>.*?</section>\s*', body, re.S))
    if len(secs) < 3 or any('<section' in m.group(0)[8:] for m in secs): return body
    head = body[:secs[0].start()]
    # scripts and anything else between or after panels must stay AFTER the panels (e.g. staging.js needs its boxes)
    tail = ''.join(body[a.end():b.start()] for a, b in zip(secs, secs[1:])) + body[secs[-1].end():]
    items = []
    for i, m in enumerate(secs):
        tid = re.search(r'data-tab="([^"]*)"', m.group(0)).group(1); lab = re.search(r'data-label="([^"]*)"', m.group(0)).group(1)
        lead = i == 0 and re.search(_LEAD_RE, html.unescape(lab).lower())
        items.append((0 if lead else _tab_rank(tid, lab), i, m.group(0)))
    items.sort()
    out = [x[2] for x in items]
    # only the first tab is visible before the script runs
    out = [re.sub(r'(<section class="panel[^>]*?)( hidden)?(>)', (r'\1\3' if k == 0 else (lambda m: m.group(1) + ' hidden' + m.group(3))), x, count=1) for k, x in enumerate(out)]
    return head + '\n'.join(out) + '\n' + tail
def page(f, short, long, desc, group, gname, gid, foot):
    body = _consent_print((root/'src'/f).read_text()) + consent_panel(f) + _mdt.panel(f) + stage_panel(f) + eviq_panel(f) + guide_lib_panel(f) + exam_panel(f)
    if f.startswith('exam-'): body = xref_back(f, body)
    if gid in TUMOUR_GIDS: body = order_tabs(merge_staging(add_overview(body)))
    title = f'{long} Quick Reference'
    site = CTR_SITE.get(f, gid)
    return f'''<!DOCTYPE html>
<html lang="en-AU" data-site="{site}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(long)} Quick Reference</title>
{FONTS}
<link rel="stylesheet" href="assets/site.css">
<link rel="stylesheet" href="assets/extras.css">
<link rel="manifest" href="manifest.webmanifest">
<meta name="theme-color" content="#10243f">
</head>
<body>
<header class="top">
  <div class="top-inner">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> › <a href="index.html#{gid}">{html.escape(gname)}</a> › <span>{html.escape(long)}</span></nav>
    <div class="title-row">
      <h1>{html.escape(long)}</h1>
      <div class="hdr-right" style="display:flex;align-items:center;gap:10px;align-self:center;flex-shrink:0">{APPLINKS}<div class="meta">v{VERSION}</div></div>
    </div>
    <form class="search" role="search" id="searchForm">
      <label for="q" class="note" style="position:absolute;left:-9999px">Search this page</label>
      <input id="q" type="search" placeholder="Search this page: trial, dose, drug" autocomplete="off">
      <button type="button" id="clear">Clear</button>
    </form>
    <nav class="chips" role="tablist" aria-label="Sections" id="chips"></nav>
  </div>
</header>
<div class="layout">
<aside class="side">{tree(f)}</aside>
<main id="main">
{related_bar(f, gid)}
<div class="empty" id="empty">No cards match. Try a shorter term such as a trial name, a dose (50/25) or a drug.</div>
{body}
</main>
</div>
{foot}
<script src="assets/site.js"></script>
<script src="assets/extras.js"></script>
{_MORE_JS}
</body>
</html>
'''
FOOT_GU = '<footer><p>Synthesised from the RadOncReview GU document (collaborative, US-centric: NCCN, ASTRO, AUA), including 2026 EAU and ASTRO guidelines and ASTRO \'26 abstracts. Doses are as reported in the source and its trials. Check eviQ, departmental protocols and drug availability before prescribing.</p></footer>'
FOOT_GYN = FOOT.replace('RadOncReview GI document','RadOncReview Gynecologic document').replace('ASTRO, ASCO','ASTRO, GOG/NRG')
def mkfoot(doc, bodies):
    return FOOT.replace('RadOncReview GI document', f'RadOncReview {doc} document').replace('NCCN, ASTRO, ASCO', bodies)
BREAST = [
 ('breast-early.html','DCIS & early breast','DCIS and early breast','DCIS, whole-breast fractionation (26/5), boost, partial breast and brachytherapy, omission in older women.'),
 ('breast-nodes-pmrt.html','Nodes & PMRT','Nodes and PMRT','Positive sentinel node (Z-11, AMAROS), regional nodal RT, IMN, PMRT by stage, post-neoadjuvant, reconstruction.'),
 ('breast-planning.html','Breast planning & consent','Breast planning and consent','Volumes, tangent borders, constraints, acute and late toxicity numbers to quote.'),
]
THORAX = [
 ('thorax-early.html','Early NSCLC (SABR)','Early-stage NSCLC (SABR)','Dose by location (peripheral, central, ultracentral), HILUS caution, operable vs inoperable, SABR constraints and toxicity.'),
 ('thorax-stage3.html','Stage III NSCLC','Stage III NSCLC','ChemoRT then durvalumab or osimertinib, hypofractionation for unfit, PORT, neoadjuvant chemo-IO, superior sulcus, constraints.'),
 ('thorax-metastatic.html','Metastatic NSCLC','Metastatic NSCLC','Consolidative RT with TKIs (SINDAS, NORTHSTAR), driver-negative and IO-era trials (LU002, LONESTAR), oligoprogression (CURB), palliative thoracic doses, consent numbers.'),
 ('thorax-sclc.html','Small cell','Small cell lung cancer','45/30 BID vs 66–70 Gy, ADRIATIC, PCI vs MRI surveillance, extensive stage and CREST.'),
 ('thorax-other.html','Thymic, meso & other','Thymic, mesothelioma and other thoracic','Thymic PORT by resection, mesothelioma RT, thoracic re-irradiation, VT radioablation.'),
]
HN = [
 ('hn-general.html','H&N general','Head and neck: general','PORT risk groups and chemo, definitive dose levels, fractionation, volumes, constraints, consent numbers, re-irradiation (RPA).'),
 ('hn-oropharynx.html','Oropharynx','Oropharynx','HPV+ OPC by ASTRO 2024, TORS vs RT, unilateral neck, cetuximab failure, de-escalation trials.'),
 ('hn-larynx.html','Larynx & hypopharynx','Larynx and hypopharynx','Early glottic 2.25 Gy schedules and fields, larynx preservation (RTOG 91-11), T4 laryngectomy.'),
 ('hn-oral-salivary.html','Oral cavity & salivary','Oral cavity, lip and salivary','Neck management by DOI, PORT indications, lip and brachytherapy, salivary PORT and nerve coverage.'),
 ('hn-npc-sinonasal.html','Nasopharynx & sinonasal','Nasopharynx and sinonasal','NPC chemo by stage, induction GC/TPF, volumes and temporal lobe limits; sinonasal PORT and neck.'),
 ('hn-thyroid-cup.html','Thyroid & unknown primary','Thyroid and unknown primary','RAI and EBRT indications, anaplastic, PORT volumes; SCC unknown primary workup and volumes.'),
 ('skin.html','Skin','Skin: BCC, SCC, melanoma and Merkel','PORT indications and NCCN dose table, TROG 05.01, C-POST, melanoma nodal RT, Merkel doses and margins.'),
]
CNS = [
 ('cns-glioma.html','Glioma','Glioma (adult)','GBM by age and PS (Stupp, Perry, 25/5), volumes, IDH-mutant grade 2–3 (RTOG 9802, CATNON, INDIGO), re-irradiation.'),
 ('cns-benign.html','Benign & functional','Benign and functional CNS','Meningioma (ROAM, RTOG 0539), vestibular schwannoma SRS, pituitary, optic tolerance, AVM, trigeminal neuralgia.'),
 ('cns-vs.html','Vestibular schwannoma','Vestibular schwannoma','Surveillance vs SRS vs surgery by Koos grade, work-up and hearing classes, SRS doses and cochlear limits, consent numbers, V-REX and ACOUNEU.'),
 ('cns-general.html','Eye & tolerances','Uveal melanoma and CNS tolerances','COMS sizes and plaque dosing, brain necrosis, optic, hippocampal, lens and lacrimal limits.'),
 ('peds-cns.html','Paediatric CNS','Paediatric CNS','Medulloblastoma risk groups and CSI, ependymoma, germ cell tumours, craniopharyngioma, LGG and DIPG.'),
 ('peds-solid.html','Paediatric solid tumours','Paediatric solid tumours','RMS dose by group, Ewing sarcoma, Wilms flank/abdomen/lung, neuroblastoma, retinoblastoma.'),
 ('peds-late.html','Paediatric late effects','Paediatric late effects','Dose thresholds for IQ, endocrine, hearing, growth, fertility, stroke and second cancers.'),
]
HEME = [
 ('heme-hodgkin.html','Hodgkin','Hodgkin lymphoma','Favourable vs unfavourable, 20 vs 30 Gy, PET-adapted omission (HD16, HD17, H10, RAPID), advanced stage, ISRT.'),
 ('heme-nhl.html','Non-Hodgkin','Non-Hodgkin lymphoma','DLBCL consolidation and doses, FLYER and S1001, indolent 24 Gy vs 4 Gy, MALT and orbit, PCNSL WBRT.'),
 ('heme-other.html','Myeloma, TBI & skin','Plasmacytoma, TBI and cutaneous lymphoma','Plasmacytoma doses, myeloma palliation, TBI regimens and toxicity, ALL cranial RT, MF and TSEBT.'),
]
SARCOMA = [
 ('sarcoma-sts.html','Soft tissue & bone sarcoma','Sarcoma','Extremity STS pre-op 50/25 vs post-op, volumes and bone limits, retroperitoneal (STRASS), chordoma, desmoid, Kaposi.'),
 ('benign.html','Benign','Benign conditions','Heterotopic ossification, osteoarthritis, plantar fasciitis, Dupuytren\'s, keloid, gynaecomastia, thyroid eye disease and other low-dose RT.'),
]
PALL = [
 ('pall-brain.html','Brain metastases','Brain metastases','SRS vs WBRT, SRS dose by size, cavity SRS, HA-WBRT + memantine, necrosis limits, QUARTZ.'),
 ('pall-wbrt.html','WBRT principles','Whole-brain radiotherapy principles','Who still needs WBRT, 20/5 vs 30/10 vs PCI doses, HA technique, memantine and amantadine, acute/subacute/late toxicity timeline, consent rates.'),
 ('pall-bone-spine.html','Bone, cord & spine SBRT','Bone metastases, cord compression and spine SBRT','8/1 vs multiple fractions, SC.24, MSCC (NOMS, SINS, SCORAD), HyTEC cord limits, VCF.'),
 ('pall-oligo.html','Oligomets & palliation','Oligometastases and general palliation','SABR-COMET, CURB, NRG-LU002; palliative regimens for lung, SVC, H&N, bleeding, liver and coeliac plexus.'),
]
PRIN = [
 ('prin-radiobiology.html','Radiobiology','Radiobiology','5 Rs, LQ model and α/β, normal tissue effects, hypoxia, radiation protection, pregnancy and fertility.'),
 ('prin-physics.html','Physics','Radiation physics','Photon and electron beams, ICRU volumes and reporting, PTV margins, implanted cardiac devices.'),
 ('prin-imaging.html','Imaging & IGRT','Imaging and IGRT','CT numbers and windows, MRI sequences, PET tracers, image guidance and adaptation.'),
 ('prin-brachy.html','Brachytherapy','Brachytherapy','Dose rates, isotopes, prostate LDR and HDR doses and metrics, gynae, breast and other sites.'),
 ('prin-techniques.html','Protons & MRgRT','Protons and MR-guided RT','Bragg peak, range uncertainty, indications and access; MR-guided adaptive RT and its evidence.'),
 ('prin-emergencies.html','Emergencies','Emergencies','Cord compression, SVC obstruction, airway compromise, bleeding, raised ICP and leptomeningeal disease.'),
 ('prin-setup.html','Simulation & set-up','Simulation and set-up','Pre-simulation checklist, set-up and preparation by site, landmarks and motion management.'),
 ('prin-stats.html','Statistics & trials','Statistics and trial design','Error and power, hazard ratios and NNT, non-inferiority, bias, test choice, levels of evidence.'),
]
FOOT_PRIN = '<footer><p>Principles pages written in our own words for this site, informed by Tang and Farooqi, Pocket Radiation Oncology, 2nd ed. (Wolters Kluwer, 2025) and the other sources listed on each page. Items flagged Verify are teaching values to confirm against a primary source before relying on them clinically.</p></footer>'
MRL = [
 ('mrl-images.html','Sequences & signal','MR-linac sequences and signal','T2 nav vs 3D Vane, what shade each organ is (biliary tree, stomach, duodenum, vessels), pitfalls and artefacts.'),
 ('mrl-liver-gi.html','Liver & upper GI','MR-linac liver and upper GI','Liver lesion appearance by type, Couinaud orientation for liver SABR, duodenum D1–D4, stomach, bowel and pancreas.'),
 ('mrl-tumour-nodes.html','Tumours & nodes','MR-linac tumours and involved nodes','Involved node features and size thresholds, node vs vessel vs bowel, pancreas, biliary, gastric, rectal, prostate and cervix GTVs on T2 and 3D Vane.'),
 ('mrl-pelvis.html','Pelvis','MR-linac pelvis','Prostate zones, apex, SVs, spacer, rectal wall, cervix and uterus, nodes vs vessels on T2.'),
 ('mrl-workflow.html','Adaptive workflow','MR-linac adaptive workflow and resources','ATP vs ATS, editing propagated contours, gas and bulk density, atlases and papers.'),
]
FOOT_MRL = '<footer><p>Practical MR-linac (Elekta Unity) delineation tips written for T2 navigator-triggered and T1 3D Vane images. Signal descriptions are typical, not absolute; always compare with diagnostic imaging and the reference plan. Follow departmental MR-linac and physics protocols.</p></footer>'
try:
    from groups_extra import EXTRA
except ImportError:
    EXTRA = []
# (gid, crumb name, home heading, pages, footer)
SYS = [
 ('sys-chemort.html','Concurrent chemo-RT','Concurrent chemotherapy with RT','Regimens and doses by site (stage III NSCLC, head and neck, GI, cervix, bladder, glioma), half-lives, toxicities and first-line management.'),
 ('sys-timing.html','Targeted & immunotherapy','Targeted therapy and immunotherapy with RT','ESMO–ESTRO and OligoCare consensus on stopping and restarting around RT, SBRT and SRS by drug class; immune-related toxicity; pneumonitis.'),
 ('sys-breast-endocrine.html','Breast endocrine','Endocrine therapy for breast cancer','Tamoxifen, aromatase inhibitors, ovarian suppression, CDK4/6; duration, sequencing with RT, side-effect management.'),
 ('sys-prostate-adt.html','Prostate ADT','Endocrine therapy for prostate cancer','LHRH agonists and antagonists, antiandrogens, ARPIs; duration with RT; monitoring and side-effect management.'),
 ('sys-bone.html','Bone agents','Bisphosphonates and denosumab','Zoledronic acid and denosumab by indication, calcium and dental checks, MRONJ, what changes with RT.'),
 ('sys-supportive.html','Supportive drugs','Supportive and symptom drugs','Venlafaxine and alternatives for hot flushes, dexamethasone, antiemetics, mucositis, bowel, bladder, sexual health, late effects.'),
]
FOOT_SYS = '<footer><p>Systemic therapy notes for a radiation oncologist, not a prescribing reference. Doses, half-lives and withholding intervals not attributed to a named source were entered from memory and are flagged Verify. Prescribe from eviQ, the product information and local protocols, with the treating medical oncologist and pharmacist.</p></footer>'
RERT = [
 ('rert-principles.html','Principles & workflow','Reirradiation: principles and workflow','ESTRO–EORTC definitions and decision statements, clinic checklist, dose summation, radiobiology and recovery, consent, sources still needed.'),
 ('rert-constraints.html','Limits & calculators','Reirradiation: cumulative limits and calculators','Published cumulative dose limits by organ with sources; remaining-dose calculator; spinal cord reirradiation check (Nieder, Sahgal).'),
 ('rert-cns.html','CNS, spine & bone','Reirradiation: CNS, spine and bone','Glioblastoma (ESTRO/EANO, RTOG 1205), repeat SRS and WBRT, spine SBRT and cord limits, painful bone metastases (SC.20).'),
 ('rert-hn.html','Head & neck','Reirradiation: head and neck','MIRI RPA, dose, SBRT and carotid blowout, cumulative limits; recurrent nasopharyngeal carcinoma and hyperfractionation.'),
 ('rert-thorax-breast.html','Thorax & breast','Reirradiation: thorax and breast','ESTRO 2026 lung guideline, ARS composite constraints; second breast conservation (RTOG 1014, GEC-ESTRO), chest wall.'),
 ('rert-pelvis.html','Abdomen & pelvis','Reirradiation: abdomen and pelvis','Recurrent rectal cancer (ESTRO 2026), pelvic SABR (UK guidance), liver repeat SBRT, bladder, salvage after prostate RT, gynaecological brachytherapy.'),
]
FOOT_RERT = '<footer><p>Reirradiation notes built from consensus statements, guidelines and trials named on each page. Evidence is largely retrospective; cumulative limits are estimates. Items flagged Verify were entered from memory. Every case needs an individual cumulative dose assessment with physics and a multidisciplinary decision.</p></footer>'
GROUPS = [
 ('breast','Breast','Breast',BREAST,mkfoot('Breast','NCCN, ASTRO, ASCO')),
 ('cns','CNS','CNS & Paediatrics',CNS,mkfoot('CNS and Peds','NCCN, ASTRO, COG')),
 ('gi','GI','Gastrointestinal',GI,FOOT),
 ('gu','GU','Genitourinary',GU,FOOT_GU),
 ('gyn','Gynae','Gynaecological',GYN,FOOT_GYN),
 ('heme','Haematology','Haematology',HEME,mkfoot('Hematologic','NCCN, ILROG, ASTRO')),
 ('hn','H&N','Head and neck & Skin',HN,mkfoot('Head and Neck, Thyroid and Skin','NCCN, ASTRO, ASCO')),
 ('sarcoma','Sarcoma','Sarcoma',SARCOMA,mkfoot('Sarcoma/Musculoskeletal','NCCN, ASTRO, ESMO')),
 ('thorax','Thorax','Thorax',THORAX,mkfoot('Thorax','NCCN, ASTRO, ASCO')),
 ('pall','Palliative','Palliative & oligometastases',PALL,mkfoot('Brain Mets/Palliative/Oligo/Immuno','NCCN, ASTRO, ASCO')),
 ('sys','Systemic therapy','Systemic therapy & supportive drugs',SYS,FOOT_SYS),
 ('rert','Reirradiation','Reirradiation',RERT,FOOT_RERT),
 ('prin','Principles','Principles & techniques',PRIN,FOOT_PRIN),
 ('mrl','MR-linac','MR-linac',MRL,FOOT_MRL),
 ('exam','Exam summary','Phase 2 exam summary',EXAM,FOOT_EXAM),
] + EXTRA
# old gu.html -> redirect to home GU section
(root/'gu.html').write_text('<!DOCTYPE html>\n<html lang="en-AU"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=index.html#gu"><title>GU Quick Reference</title></head><body><p>The GU reference is now split by tumour site. <a href="index.html#gu">Go to the GU pages</a>.</p></body></html>\n')
def cards(pages): return ''.join(f'<a class="hubcard" href="{f}"{_ds(f)} title="{html.escape(desc, quote=True)}"><h3>{html.escape(long)}</h3></a>' for f,short,long,desc in pages)

# ---------------- Contouring library and protocols ----------------
from contour_lib import LIB
from urllib.parse import quote_plus
def _link(l):
    if l.startswith('pm:'): return f'https://pubmed.ncbi.nlm.nih.gov/{l[3:]}/', 'PubMed'
    if l.startswith('doi:'): return f'https://doi.org/{l[4:]}', 'DOI'
    if l.startswith('q:'): return 'https://pubmed.ncbi.nlm.nih.gov/?term='+quote_plus(l[2:]), 'PubMed search'
    return l, 'Website'
LIB_FULL = [(f,'',n,'',t) for f,n,t in [
 ('contouring/breast.html','Breast contouring guide',('breast',)),('contouring/thorax.html','Thorax contouring guide',('thorax',)),
 ('contouring/head-neck.html','Head and neck contouring guide',('hn',)),('contouring/cns.html','Primary CNS contouring guide',('cns',)),('contouring/brain-mets.html','Brain metastases contouring guide (SRS, cavity, HA-WBRT)',('cns',)),('contouring/wbrt.html','Whole brain VMAT contouring guide (standard, HA, helmet)',('cns',)),
 ('contouring/oesophagus.html','Oesophagus and GOJ contouring guide',('gi',)),('contouring/pancreas-stomach.html','Pancreas and stomach contouring guide',('gi',)),
 ('contouring/biliary.html','Cholangiocarcinoma and gallbladder contouring guide',('gi',)),('contouring/liver-sbrt.html','Liver SBRT OAR contouring guide',('gi',)),
 ('contouring/rectal-long-course.html','Rectal long-course atlas',('gi',)),('contouring/anal.html','Anal canal contouring guide',('gi',)),
 ('contouring/prostate.html','Prostate contouring guide',('gu',)),('contouring/bladder.html','Bladder contouring guide',('gu',)),
 ('contouring/gynae.html','Gynaecological contouring guide',('gyn',)),('contouring/lymphoma.html','Lymphoma ISRT contouring guide',('heme',)),
 ('contouring/spine-bone.html','Spine and bone SBRT contouring guide',('sbrt',))]]
# Guideline links per contouring guide (from contour_lib.LIB): (tab, card title or None = all, keyword filter or None)
GUIDE_LIB = {
 'contouring/breast.html': [('breast',None,None)],
 'contouring/thorax.html': [('thorax',None,None)],
 'contouring/head-neck.html': [('hn',None,None)],
 'contouring/cns.html': [('cns','Gliomas',None),('cns','Skull base, meningioma and metastases',r'^(?!.*(cavity|Hippocamp|HA-WBRT|Leptomening|VMAT))'),('cns','Neuro OARs',None)],
 'contouring/brain-mets.html': [('cns','Skull base, meningioma and metastases',r'cavity|Hippocamp|HA-WBRT|Leptomening|VMAT'),('cns','Neuro OARs',None)],
 'contouring/wbrt.html': [('cns','Skull base, meningioma and metastases',r'Hippocamp|HA-WBRT|Leptomening|VMAT')],
 'contouring/oesophagus.html': [('gi','Upper GI',r'oesoph|GEJ|SCOPE|upper GI malig|cervical')],
 'contouring/pancreas-stomach.html': [('gi','Upper GI',r'pancrea|gastric|GEJ|EORTC-ROG|upper GI malig|upper abdominal')],
 'contouring/biliary.html': [('gi','Upper GI',r'biliar|cholangio')],
 'contouring/liver-sbrt.html': [('gi','Liver SBRT and MRI upper abdominal OARs',None),('gi','Upper GI',r'upper abdominal')],
 'contouring/rectal-long-course.html': [('gi','Rectum and anus',r'rectal|anorectal')],
 'contouring/anal.html': [('gi','Rectum and anus',r'anal|anorectal')],
 'contouring/prostate.html': [('gu','Prostate and prostate bed',None),('gu','Pelvic nodes and PSMA',None),('gu','Bladder, kidney, penis and pelvic OARs',r'pelvic normal')],
 'contouring/bladder.html': [('gu','Bladder, kidney, penis and pelvic OARs',r'[Bb]ladder|pelvic normal')],
 'contouring/gynae.html': [('gyn',None,None)],
 'contouring/lymphoma.html': [('heme',None,None)],
 'contouring/spine-bone.html': [('sbrt',None,None)],
 'ctr-sarcoma.html': [('sarc','Sarcoma',None)],
 'ctr-skin.html': [('sarc','Skin',None)],
 'ctr-peds.html': [('peds',None,None)],
 'ctr-kidney-liver.html': [('gu','Bladder, kidney, penis and pelvic OARs',r'IROCK|renal')],
}
# PDF page tab for each guide (ctr-library.html#<tab>)
GUIDE_PDFTAB = {'contouring/breast.html':'breast','contouring/thorax.html':'thorax','contouring/head-neck.html':'hn','contouring/cns.html':'cns','contouring/brain-mets.html':'cns','contouring/wbrt.html':'cns',
 'contouring/oesophagus.html':'ugi','contouring/pancreas-stomach.html':'ugi','contouring/biliary.html':'ugi','contouring/liver-sbrt.html':'oar','contouring/rectal-long-course.html':'lgi','contouring/anal.html':'lgi',
 'contouring/prostate.html':'gu','contouring/bladder.html':'gu','contouring/gynae.html':'gyn','contouring/lymphoma.html':'heme','contouring/spine-bone.html':'sbrt','ctr-sarcoma.html':'sarc','ctr-skin.html':'sarc','ctr-peds.html':'general','ctr-kidney-liver.html':'gu'}
_LIBD = {tid:(label,lede,cards_) for tid,label,lede,cards_ in LIB}
def _lib_li(e):
    yr,t,cite,note,l,star = e
    u,kind=_link(l)
    st='<span class="libstar">Start here</span> ' if star else ''
    y=f'{yr} · ' if yr else ''
    return f'<li>{st}<a href="{html.escape(u)}" target="_blank" rel="noopener">{html.escape(t)}</a><span class="libmeta">{y}{html.escape(cite)} · {kind}</span><span class="libnote">{html.escape(note)}</span></li>'
def guide_lib_panel(f):
    """Hidden-by-default 'Guidelines' tab for a contouring guide: published guidelines and atlases, plus the OneDrive PDFs."""
    if f not in GUIDE_LIB: return ''
    up = '../' if f.startswith('contouring/') else ''
    arts = []
    for tid,ctitle,kw in GUIDE_LIB[f]:
        for title,entries in _LIBD[tid][2]:
            if ctitle and title != ctitle: continue
            es = [e for e in entries if not kw or re.search(kw, e[1]+' '+e[3])]
            if not es: continue
            es = sorted(es, key=lambda e: not e[5])
            arts.append(f'<article class="card" data-title="{html.escape(title)}"><h3>{html.escape(title)}</h3><ul class="lib">{"".join(_lib_li(e) for e in es)}</ul></article>')
    tab = GUIDE_PDFTAB.get(f)
    if tab:
        arts.append(f'<article class="card key" data-title="Original PDFs"><h3>Original PDFs</h3><p>The original guideline and atlas PDFs for this site are kept in OneDrive (01 Contouring Guidelines). <a href="{up}ctr-library.html#{tab}">See the list of PDFs for this site</a>.</p></article>')
    return (f'<section class="panel" id="p-guidelines" data-tab="guidelines" data-label="Guidelines" hidden>\n  <div class="panel-head"><h2>Published guidelines and atlases</h2>'
            f'<p class="lede">"Start here" marks the current standard.</p><div class="jump"></div></div>\n' + '\n'.join(arts) + '\n</section>')
def _inject_panel(htmltext, panel):
    if not panel: return htmltext
    i = htmltext.rfind('</section>', 0, htmltext.find('</main>'))
    return htmltext[:i+10] + '\n' + panel + htmltext[i+10:]

# ---- Guideline PDFs page (ctr-library.html): what is in OneDrive "01 Contouring Guidelines", by site
PDF_TABS = [('breast','Breast',['Breast']),('thorax','Thorax',['Thoracic - Lung & Heart']),('hn','Head & neck',['Head and Neck']),
 ('cns','CNS',['CNS & Brain']),('ugi','Upper GI',['Upper GI']),('lgi','Rectum & anus',['Lower GI - Rectal','Lower GI - Anal']),
 ('gu','GU',['Genitourinary - Prostate','Genitourinary - Bladder & Other GU']),('gyn','Gynae',['Gynae']),('heme','Haematology',['Lymphoma & Haematological']),
 ('sarc','Sarcoma & skin',['Sarcoma','Skin']),('sbrt','SABR & bone',['SABR - Spine & Bone','SABR - General & Constraints']),
 ('oar','OARs & pelvis',['OARs & Normal Tissue','Pelvis - Nodal & Anatomy (multi-site)']),('general','General & books',['General & Multi-site'])]
_JOUR = {'Green J':'Radiother Oncol','Red J':'IJROBP','PRO':'Pract Radiat Oncol','JMIRO':'J Med Imaging Radiat Oncol','ctRO':'Clin Transl Radiat Oncol','JACMP':'J Appl Clin Med Phys','JCO':'J Clin Oncol','JTO':'J Thorac Oncol'}
def _pdf_title(p):
    t = p['title'] or re.sub(r'\.pdf$', '', p['file'], flags=re.I)
    t = t.replace('_', ' ').replace('  ', ' ').strip()
    m = re.match(r'^\(?((?:19|20)\d\d)\)?\s+(.*)$', t)
    yr, rest = (m.group(1), m.group(2)) if m else ('', t)
    jour = ''
    for k,v in _JOUR.items():
        if rest.startswith(k+' '): jour, rest = v, rest[len(k)+1:]; break
    else:
        m2 = re.match(r'^(Acta Oncol|Clin Oncol|Front Oncol|Adv Radiat Oncol|Semin Radiat Oncol|Lancet Oncol|BJR|Anticancer Res|Oncol Lett|PLOS One|Hepatoma Res|Curr Oncol|Breast|Green|NRG)\)?\s+(.*)$', rest)
        if m2: jour, rest = m2.group(1), m2.group(2)
    return yr, jour, rest.strip(' -')
_STOP = set('the and for with from into guideline guidelines consensus contouring delineation radiotherapy radiation therapy target volume volumes cancer atlas recommendations international estro acrop group'.split())
def _words(s): return {w for w in re.findall(r'[a-z]{4,}', s.lower()) if w not in _STOP}
def _pdf_link(p, yr, title):
    if p['link'] == 'none': return None, 'Not on PubMed'
    if p['link']: return _link(p['link'])
    best = None
    for tid,label,lede,cards_ in LIB:
        for _,entries in cards_:
            for e in entries:
                if not yr or str(e[0]) != yr: continue
                ov = len(_words(title) & _words(e[1]+' '+e[2]))
                if ov >= 2 and (best is None or ov > best[0]): best = (ov, e[4])
    if best: return _link(best[1])
    return _link('q:' + title)
def build_pdf_page():
    import json as _j
    pdfs = _j.loads((root/'pdf_index.json').read_text())
    out = []
    for i,(tid,label,tops) in enumerate(PDF_TABS):
        mine = [p for p in pdfs if p['top'] in tops]
        out.append(f'<section class="panel" id="p-{tid}" data-tab="{tid}" data-label="{html.escape(label)}"{" hidden" if i else ""}>\n  <div class="panel-head">\n    <h2>{html.escape(label)}</h2>\n\n    <div class="jump"></div>\n  </div>')
        guides = [c for c in LIB_FULL + CONTOUR if GUIDE_PDFTAB.get(c[0]) == tid]
        if guides:
            out.append('  <article class="card key" data-title="Our guides"><h3>Our guides</h3><ul class="eviq">'+''.join(f'<li><a href="{g[0]}#guidelines">{html.escape(g[2])}</a></li>' for g in guides)+'</ul></article>')
        groups = {}
        for p in mine:
            groups.setdefault((p['top'], p['sub']), []).append(p)
        for (top,sub),ps in groups.items():
            ctitle = (sub.split('/')[-1] if sub else (top if len(tops) > 1 else 'Main folder'))
            lis = []
            for p in sorted(ps, key=lambda p: (_pdf_title(p)[0] or '0000'), reverse=True):
                yr, jour, t = _pdf_title(p)
                u, kind = _pdf_link(p, yr, t)
                meta = ' · '.join(x for x in [yr, jour, kind, f'{p["mb"]} MB'] if x)
                ttl = f'<a href="{html.escape(u)}" target="_blank" rel="noopener">{html.escape(t)}</a>' if u else f'<span class="libtitle">{html.escape(t)}</span>'
                lis.append(f'<li>{ttl}<span class="libmeta">{html.escape(meta)}</span><span class="libnote">OneDrive file: {html.escape(p["path"])}</span></li>')
            out.append(f'  <article class="card" data-title="{html.escape(ctitle)}"><h3>{html.escape(ctitle)}</h3><ul class="lib">{"".join(lis)}</ul></article>')
        if tid == 'general':
            for title,entries in _LIBD['general'][2]:
                out.append(f'  <article class="card" data-title="{html.escape(title)}"><h3>{html.escape(title)}</h3><ul class="lib">{"".join(_lib_li(e) for e in entries)}</ul></article>')
        out.append('</section>')
    out.append('<p class="note">The PDFs are not copied to this site: the repository is public, and journal articles, books and departmental protocols cannot be republished. Open the file from OneDrive, or use the title link for the publisher version. The published guideline lists with verified PubMed links are now the "Guidelines" tab of each contouring guide.</p>')
    return '\n'.join(out)

# (file, short, long, desc, library tabs)
CONTOUR = [
 ('ctr-library.html','Guideline PDFs','Contouring guideline PDFs','The original guideline, atlas and protocol PDFs in OneDrive, by tumour site, with links to the published versions.',()),
 ('ctr-sarcoma.html','Sarcoma','Sarcoma contouring guide','Extremity 3 cm / 1.5 cm CTV with oedema, post-op, and retroperitoneal volumes.',('sarc',)),
 ('ctr-kidney-liver.html','Kidney SABR','Kidney SABR contouring guide','Primary kidney SABR (IROCK): GTV, ITV and PTV, motion management and OARs. Quick guide only.',('gu',)),
 ('ctr-skin.html','Skin','Skin contouring guide','BCC/cSCC clinical margins, electron and orthovoltage fields, post-op cSCC, PNI, Merkel and melanoma.',('sarc',)),
 ('ctr-peds.html','Paeds','Paediatric contouring guide','CSI CTV pitfalls, CNS boosts, pre-chemo CTV rules for RMS, Ewing, Wilms, neuroblastoma; paediatric OARs.',('peds',)),
]
(root/'src'/'ctr-library.html').write_text(build_pdf_page())
CNAV = [(f,short,long,desc) for f,short,long,desc,_ in CONTOUR] + [
 ('contouring/breast.html','Breast','Breast contouring guide','Whole breast, tumour bed and SIB, partial breast with trial volumes, multicatheter APBI, chest wall with and without implants, ESTRO/RTOG nodal borders, Liverpool DVH scorecards.'),
 ('contouring/cns.html','Primary CNS','Primary CNS contouring guide','Glioblastoma (ESTRO-EANO 2023), IDH-mutant glioma (2025), meningioma (RTOG 0539/EORTC), vestibular schwannoma, barrier editing, EPTN OAR constraints.'),
 ('contouring/brain-mets.html','Brain metastases','Brain metastases contouring guide','Intact and cavity SRS (Soliman 2018, Canberra), dose by size, systemic therapy around SRS, HA-WBRT summary, SRS and HyTEC limits.'),
 ('contouring/wbrt.html','Whole brain (VMAT)','Whole brain VMAT contouring guide','Volume-based standard WBRT, hippocampal-avoidance WBRT (RTOG 0933 atlas, NRG CC001) and the helmet volume for leptomeningeal disease (SIOPE foramina, optic sheaths, thecal sac to C2); constraints and RayStation build.'),
 ('contouring/gynae.html','Gynae','Gynaecological contouring guide','Cervix EBRT (EMBRACE II ITV and nodal SIB), MRI-guided brachytherapy targets and aims, post-op cervix and endometrium, vaginal vault and vaginal cancer, vulva definitive and post-op, inguinal margins, constraints.'),
 ('contouring/spine-bone.html','Spine & bone SBRT','Spine and bone SBRT contouring guide','St George selection and workflow, ISRC sector CTV table, post-op spine, sacrum (Dunne), non-spine bone and soft tissue, re-irradiation cord limits, 1–5 fraction constraints.'),
 ('contouring/head-neck.html','Head & neck','Head and neck contouring guide','Neck level border tables (Grégoire 2014), 5 + 5 mm primary CTV, Biau 2019 level selection, DAHANCA post-op, PATHOS, NPC 2024 dose levels, HNCIG cSCC, PNI pathways, DAHANCA constraints.'),
 ('contouring/lymphoma.html','Lymphoma ISRT','Lymphoma ISRT contouring guide','ILROG pre- and post-chemo GTV, ISRT CTV for indolent, early HL/DLBCL, mediastinal, advanced and extranodal disease, doses, mini-atlas margins.'),
 ('contouring/thorax.html','Thorax','Thorax contouring guide','Lung SABR (peripheral, central, ultracentral), stage II–III definitive, PORT, limited-stage SCLC, IASLC station borders and landmarks, thoracic OAR definitions and constraints.'),
 ('contouring/prostate.html','Prostate','Prostate contouring guide','Intact prostate and SVs, 5-fraction SABR (PACE, ESTRO 2026), prostate bed, NRG pelvic nodes, CT vs MRI apex/base pearls, IGRT, OARs.'),
 ('contouring/bladder.html','Bladder','Bladder contouring guide','Bladder preservation (FROGG 2020): whole-bladder CTV and extension rules, high-risk CTV and escalation, nodes, PTV and plan of the day; post-cystectomy bed and nodal borders (Baumann/NRG-GU001); constraints.'),
 ('contouring/rectal-long-course.html','Rectum','Rectal long-course atlas','Elective compartments and borders, GTV criteria, 45 vs 50–54 Gy volumes.'),
 ('contouring/anal.html','Anal canal','Anal canal contouring guide','T1N0 and T2–4/N+ primary and nodal CTVs, all elective regions with border tables (department/AGITG vs UK, NOAC, ECOG), ischiorectal fossa and risk-adapted options, doses, constraints.'),
 ('contouring/oesophagus.html','Oesophagus & GOJ','Oesophagus and GOJ contouring guide','Neoadjuvant and definitive involved-field build (SCOPE2), GOJ and coeliac rules, cervical and SCF node-positive volumes, adjuvant tumour bed, constraints.'),
 ('contouring/pancreas-stomach.html','Pancreas & stomach','Pancreas and stomach contouring guide','Pancreas neoadjuvant, definitive, NRG dose-escalated (triangle) and SBRT volumes; RTOG post-op CTV; gastric nodal anatomy; constraints.'),
 ('contouring/biliary.html','Biliary','Cholangiocarcinoma and gallbladder contouring guide','Intrahepatic SBRT and chemoRT, perihilar and distal CTV margins, post-op nodal templates (Park, RTOG), gallbladder, doses.'),
 ('contouring/liver-sbrt.html','Liver SBRT OARs','Liver SBRT OAR contouring guide','Liver, luminal GI and other OARs on CT and MRI, central hepatobiliary tract, MR-linac re-contouring zone, UK 2022 constraints.')]
SOFTWARE = [
 ('ctr-mim.html','MIM shortcuts','MIM contouring shortcuts','MIM 7.4 default hotkeys, creating your own, mouse actions, contouring tools, H&N OAR recipes, saving and recovery. Printable PDF.'),
 ('ctr-monaco.html','Monaco shortcuts','Monaco contouring shortcuts','Elekta Monaco hot keys, navigation, contouring toolkit, Monaco-specific gotchas, workflow and W/L presets. Printable PDF.')]
# Contouring guides grouped by tumour site: major sites first, then minor sites, then reference material
CGROUPS = [
 ('Breast', ['contouring/breast.html']),
 ('Genitourinary', ['contouring/prostate.html', 'contouring/bladder.html', 'ctr-kidney-liver.html']),
 ('Thorax', ['contouring/thorax.html']),
 ('Gastrointestinal', ['contouring/oesophagus.html', 'contouring/pancreas-stomach.html', 'contouring/liver-sbrt.html', 'contouring/biliary.html', 'contouring/rectal-long-course.html', 'contouring/anal.html']),
 ('Head and neck', ['contouring/head-neck.html']),
 ('Gynaecological', ['contouring/gynae.html']),
 ('CNS', ['contouring/cns.html', 'contouring/brain-mets.html', 'contouring/wbrt.html']),
 ('Haematology', ['contouring/lymphoma.html']),
 ('Bone and spine', ['contouring/spine-bone.html']),
 ('Sarcoma and skin', ['ctr-sarcoma.html', 'ctr-skin.html']),
 ('Paediatrics', ['ctr-peds.html']),
 ('Reference and software', ['ctr-library.html', 'ctr-mim.html', 'ctr-monaco.html']),
]
_cby = {c[0]: c for c in CNAV + SOFTWARE}
_cgrouped = [f for _, fs in CGROUPS for f in fs]
assert set(_cgrouped) == set(_cby), ('contouring pages missing from CGROUPS', set(_cby) ^ set(_cgrouped))
CNAV = [_cby[f] for f in _cgrouped]
CGROUP_OF = {f: g for g, fs in CGROUPS for f in fs}
# ---------------- Tools: calculators, doses at a glance, what's new ----------------
TOOLS = [
 ('roster.html','My roster','My weekly roster','Week A/B sessions merged with this week\'s MDTs, with the full Kinghorn MDT planner.'),
 ('mdt.html','MDT decision matrix','MDT decision matrix','Tap case details as they are presented to narrow to an evidence-based option: prostate, pancreas, upper GI (oesophagus, gastric, HCC, biliary, liver mets), rectum and lung (NSCLC, SCLC).'),
 ('links.html','Clinic links','Clinic quick links','Radiology PACS and pathology results logins, A to Z, and referral forms.'),
 ('contacts.html','Contacts','Phone and contact list',"GenesisCare St Vincent's extensions, St Vincent's Hospital numbers and other GenesisCare NSW centres."),
 ('tools.html','Calculators','Calculators and tools','EQD2 and BED, cumulative dose across courses, treatment gap, and links to re-irradiation tools and SABR constraint tables.'),
 ('scores.html','Clinical scores','Clinical scores and nomograms','Auto-staging for 18 sites, Child-Pugh, ALBI, MELD, PSA doubling time, life expectancy, Roach, CAPRA, CTS5, Van Nuys, SINS, Mirels, RPA, IPI, Sedlis, brachytherapy EQD2 and more, with links to MSKCC, PREDICT, GPA and other external tools.'),
 ('doses.html','Doses at a glance','Doses at a glance','Dose and fractionation cards from every tumour-site page in one place.'),
 ('whats-new.html',"What's new","What's new",'New evidence and landmark trials by tumour site, and changes to this site.'),
]
FOOT_TOOLS = '<footer><p>Calculators use the linear-quadratic model and are for education and cross-checking only; they are not a medical device. Verify every result independently. Doses are copied from the tumour-site pages, where the sources are cited. Follow departmental protocols.</p></footer>'
def _panels(f):
    t = (root/'src'/f).read_text()
    return re.findall(r'<section class="panel" id="p-([\w-]+)" data-tab="[\w-]+" data-label="([^"]+)"[^>]*>(.*?)</section>', t, re.S)
def _cards(body):
    return re.findall(r'<article class="card[^"]*" data-title="([^"]*)">.*?</article>', body, re.S), re.findall(r'(<article class="card.*?</article>)', body, re.S)
def _gather(pick):
    out = []
    for i,(gid,gname,head,pages,_) in enumerate(GROUPS):
        if gid in ('exam','mrl','sys','rert','prin'): continue
        parts = []
        for g in pages:
            f, short, long = g[0], g[1], g[2]
            got = []
            for pid,label,body in _panels(f):
                titles, arts = _cards(body)
                got += [a for t,a in zip(titles,arts) if pick(pid,label,t)]
            if got:
                parts.append(f'<div class="gather"><article class="card gather-head" data-title="{html.escape(long)}"><h3>{html.escape(long)}</h3><p class="note">From the <a href="{f}">{html.escape(long)}</a> page, where sources and trials are cited.</p></article>' + ''.join(got) + '</div>')
        if parts:
            out.append(f'<section class="panel gathered" id="p-{gid}" data-tab="{gid}" data-label="{html.escape(head)}"{" hidden" if out else ""}>\n<div class="panel-head"><h2>{html.escape(head)}</h2><div class="jump"></div><p><button type="button" class="printbtn" onclick="window.print()">Print this site</button></p></div>\n' + ''.join(parts) + '\n</section>')
    return '\n'.join(out)
# Consent numbers now live in a 'Toxicity & consent' tab on each tumour-site page (see consent_panel); old Tools URL redirects home.
(root/'src'/'doses.html').write_text(_gather(lambda pid,label,t: (re.search(r'\bdoses?\b|fractionation|regimen', t, re.I) and not re.search(r'constraint|OAR|toxicit|limit', t, re.I)) or re.search(r'\bboost\b|HDR schedules', t, re.I)))
import whats_new as _wn
_TAG = {'practice':('Practice-changing','new'),'confirms':('Confirms practice','au'),'watch':('Watch','caution')}
def _wn_page():
    ev = sorted(_wn.EVIDENCE, key=lambda e: e[0], reverse=True)
    if ev:
        cards_ = ''
        for d,site,tag,title,summ,url,src_,aff in ev:
            lab,cls = _TAG.get(tag,('Watch','caution'))
            affh = (' Affects: ' + ' · '.join(f'<a href="{p}">{html.escape(l)}</a>' for p,l in aff) + '.') if aff else ''
            cards_ += f'<article class="card" data-title="{html.escape(title)}"><h3>{html.escape(title)}</h3><p><span class="flag {cls}">{lab}</span> <b>{html.escape(site)}</b> · {d} · {html.escape(src_)}</p><p>{html.escape(summ)}</p><p class="note"><a href="{html.escape(url)}" target="_blank" rel="noopener">Open the source</a>.{affh}</p></article>'
    else:
        cards_ = '<article class="card key" data-title="No entries yet"><h3>No entries yet</h3><p>The weekly evidence digest adds entries here: new phase III radiotherapy trials and guideline updates, each tagged practice-changing, confirms practice or watch, with the page on this site it affects.</p></article>'
    _done = {h for _,_,h,_,_ in GROUPS} | {x for _,_,h,_,_ in GROUPS for x in h.split(' & ')}
    _soon = [x for x in ['Breast','Thorax','Head and neck','Skin','CNS','Haematology','Sarcoma','Paediatrics','Palliative & oligometastases'] if x not in _done]
    soon_card = (f'<article class="card" data-title="Still to add"><h3>Still to add</h3><p>{", ".join(_soon)}</p></article>') if _soon else ''
    site_ = ''.join(f'<li><b>{d}</b> · {html.escape(t)}' + (f' <a href="{p}">Open</a>' if p else '') + '</li>' for d,t,p in _wn.SITE)
    return (f'<section class="panel" id="p-evidence" data-tab="evidence" data-label="Evidence"><div class="panel-head"><h2>New evidence and landmark trials</h2><p class="lede">Tags are a first read, not a guideline.</p><div class="jump"></div></div>{cards_}</section>\n'
            f'<section class="panel" id="p-site" data-tab="site" data-label="Site updates" hidden><div class="panel-head"><h2>Site updates</h2><div class="jump"></div></div><article class="card" data-title="Change log"><h3>Change log</h3><ul>{site_}</ul></article>{soon_card}</section>')
(root/'src'/'whats-new.html').write_text(_wn_page())
# ---------------- Clinic quick links (clinic_links.py -> src/links.html) ----------------
import clinic_links as _cl
_QTAG = {'net':('NSW Health network','caution'),'new':('Added Nov 2026','new'),'check':('Check URL','caution')}
def _links_page():
    out = []
    for i,(tid,label,lede,cards_) in enumerate(_cl.TABS):
        h = ' hidden' if i else ''
        out.append(f'<section class="panel" id="p-{tid}" data-tab="{tid}" data-label="{html.escape(label)}"{h}>\n  <div class="panel-head">\n    <h2>{html.escape(label)}</h2>{chr(10)+'    <p class="lede">'+html.escape(lede)+'</p>' if lede else ''}\n    <div class="jump"></div>\n  </div>')
        for title,note,links in cards_:
            lis = []
            for name,url,n,tags in sorted(links, key=lambda x: x[0].lower()):
                fl = ''.join(f' <span class="flag {_QTAG[t][1]}">{_QTAG[t][0]}</span>' for t in tags)
                host = re.sub(r'^https?://(www\.)?','',url).split('/')[0]
                nn = f'<span class="qn">{html.escape(n)}</span>' if n else ''
                lis.append(f'<li><a href="{html.escape(url)}" target="_blank" rel="noopener"><b>{html.escape(name)}</b>{nn}<span class="qh">{html.escape(host)}</span>{fl}</a><button type="button" class="fav" data-href="{html.escape(url)}" aria-label="Add to favourites" title="Add to favourites">☆</button></li>')
            np_ = f'<p class="note">{html.escape(note)}</p>' if note else ''
            out.append(f'  <article class="card" data-title="{html.escape(title)}"><h3>{html.escape(title)}</h3>{np_}<ul class="qlinks">{"".join(lis)}</ul></article>')
        out.append('</section>')
    return '\n'.join(out)
(root/'src'/'links.html').write_text(_links_page())

# ---------------- Phone and contact list (clinic_contacts.py -> src/contacts.html) ----------------
import clinic_contacts as _cc
def _num(s):
    out = []
    for part in [x.strip() for x in s.split(' / ')]:
        d = re.sub(r'\D','',part)
        if '@' in part:
            out.append(f'<a href="mailto:{html.escape(part)}">{html.escape(part)}</a>')
        elif re.fullmatch(r'\d{4,5}', part.replace(' ','')) or re.fullmatch(r'\d{2}', d):
            out.append(f'<span class="ext">{html.escape(part)}</span>')
        else:
            if len(d) == 8: d = '02' + d
            tel = '+61' + d[1:] if d.startswith('0') else d
            out.append(f'<a href="tel:{tel}">{html.escape(part)}</a>')
    return ' / '.join(out)
def _contacts_page():
    out = []
    for i,(tid,label,lede,cards_) in enumerate(_cc.TABS):
        h = ' hidden' if i else ''
        out.append(f'<section class="panel" id="p-{tid}" data-tab="{tid}" data-label="{html.escape(label)}"{h}>\n  <div class="panel-head">\n    <h2>{html.escape(label)}</h2>{chr(10)+'    <p class="lede">'+html.escape(lede)+'</p>' if lede else ''}\n    <div class="jump"></div>\n  </div>')
        if tid == 'centres':
            rows = ''.join(f'<tr><td><b>{html.escape(c)}</b><br><span class="note">{html.escape(a)}</span></td><td>' + '<br>'.join(f'{html.escape(l)}: {_num(n)}' for l,n in nums) + '</td></tr>' for c,a,nums in cards_)
            out.append(f'  <article class="card" data-title="GenesisCare centres"><h3>GenesisCare centres</h3><table class="contacts"><thead><tr><th>Centre</th><th>Contact</th></tr></thead><tbody>{rows}</tbody></table></article>')
        else:
            for title,note,rows_ in cards_:
                rows = ''.join(f'<tr><td>{html.escape(s)}' + (f'<br><span class="note">{html.escape(n)}</span>' if n else '') + f'</td><td>{_num(v)}</td></tr>' for s,v,n in rows_)
                np_ = '<p class="note">' + re.sub(r'\b(\d{4} \d{4})\b', lambda m: _num(m.group(1)), html.escape(note)) + '</p>' if note else ''
                out.append(f'  <article class="card" data-title="{html.escape(title)}"><h3>{html.escape(title)}</h3>{np_}<table class="contacts"><thead><tr><th>Service</th><th>Number</th></tr></thead><tbody>{rows}</tbody></table></article>')
        if tid == 'svh':
            out.append(f'  <article class="card" data-title="Not on this page"><h3>Not on this page</h3><p class="note">{html.escape(_cc.NOT_HERE)}</p></article>')
        out.append('</section>')
    return '\n'.join(out)
(root/'src'/'contacts.html').write_text(_contacts_page())
FOOT_CONTACTS = '<footer><p>From the SVH contact list, November 2026. Short numbers are internal extensions; tap a full number to call. Mobile numbers and staff names are added only to the password-protected site when it deploys (GitHub secret CONTACTS_PRIVATE, see tools/private_contacts.py), never to the public repository. Check with switch if a number no longer works. Edit clinic_contacts.py for the rest.</p></footer>'

FOOT_LINKS = '<footer><p>Links open each provider\'s own login page; nothing is stored here. Accounts, passwords and MFA are set up with each provider. Links marked "Added Nov 2026" came from provider websites and a published NSW provider list and may need a new account. Edit clinic_links.py to change them.</p></footer>'
for g in TOOLS:
    (root/g[0]).write_text(page(*g, TOOLS, 'Tools', 'tools', FOOT_LINKS if g[0]=='links.html' else FOOT_CONTACTS if g[0]=='contacts.html' else FOOT_TOOLS))

FOOT_SW = '<footer><p>Software quick references compiled from vendor user and training guides and a departmental MIM guide. Shortcuts and tool names change between versions and local configurations; check in your installed version. Not affiliated with or endorsed by MIM Software, GE HealthCare or Elekta. Follow departmental work instructions.</p></footer>'
for f,short,long,desc in SOFTWARE:
    (root/f).write_text(page(f,short,long,desc,CNAV,'Contouring','contouring',FOOT_SW))
FOOT_CTR = '<footer><p>Quick-reference summaries of published contouring guidelines, written in our own words. Borders are condensed; anything marked for checking should be confirmed against the original paper and its images. Not affiliated with or endorsed by ESTRO, NRG, ILROG, AGITG or other groups. Follow departmental protocols.</p></footer>'
for f,short,long,desc,_ in CONTOUR:
    (root/f).write_text(page(f,short,long,desc,CNAV,'Contouring','contouring',FOOT_CTR))
# Full contouring protocols: authored in src/contouring/, wrapped in the site shell
import sys as _sys; _sys.path.insert(0, str(root/'tools'))
from protocol_shell import convert as _proto_convert
for f,short,long,desc in CNAV:
    if not f.startswith('contouring/'): continue
    srcp = root/'src'/f
    if not srcp.exists(): continue
    _qp = root/'src'/'quick'/pathlib.Path(f).name
    (root/f).write_text(_inject_panel(_proto_convert(srcp.read_text(), f, long, short, CTR_SITE.get(f,'contouring'), tree(f), FONTS, FOOT_CTR, _qp.read_text() if _qp.exists() else None), guide_lib_panel(f)))
# Retired URLs: lung protocol and thorax quick guide merged into contouring/thorax.html
def _redirect(path, target, tabmap=None):
    tm = repr(tabmap or {}).replace("'", '"')
    (root/path).write_text(f'''<!DOCTYPE html><html lang="en-AU"><head><meta charset="utf-8"><title>Moved</title>
<meta http-equiv="refresh" content="0; url={target}">
<script>var m={tm};var h=location.hash.slice(1);location.replace("{target}"+(h?"#"+(m[h]||h):""));</script>
</head><body><p>This page has moved to <a href="{target}">the thorax contouring guide</a>.</p></body></html>
''')
_redirect('contouring/lung.html', 'thorax.html')
_redirect('ctr-thorax.html', 'contouring/thorax.html', {'nsclc':'s3','sbrt':'s2','oar':'s8'})
def _redirect2(path, default, bytab=None):
    tm = _json_dumps(bytab or {})
    (root/path).write_text(f'''<!DOCTYPE html><html lang="en-AU"><head><meta charset="utf-8"><title>Moved</title>
<meta http-equiv="refresh" content="0; url={default}">
<script>var m={tm};location.replace(m[location.hash.slice(1)]||"{default}");</script>
</head><body><p>This quick guide is now the Quick reference tab of the <a href="{default}">full contouring guide</a>.</p></body></html>
''')
from json import dumps as _json_dumps
for _old,_new in [('breast','breast'),('hn','head-neck'),('cns','cns'),('anal','anal'),('gyn','gynae'),('heme','lymphoma'),('spine','spine-bone'),('bladder','bladder')]:
    _redirect2(f'ctr-{_old}.html', f'contouring/{_new}.html#quick')
_redirect2('ctr-upper-gi.html', 'contouring/oesophagus.html#quick', {'stomach':'contouring/pancreas-stomach.html#quick','pancreas':'contouring/pancreas-stomach.html#quick'})
for gid,gname,_,pages,foot in GROUPS:
    for g in pages:
        (root/g[0]).write_text(page(*g, pages, gname, gid, foot))
contour_cards = ''.join(f'<h3 class="sub-title">{html.escape(g)}</h3><div class="hub">{cards([_cby[f] for f in fs])}</div>' for g, fs in CGROUPS)
# Old Tools page: consent numbers moved to each tumour-site page
(root/'consent.html').write_text('<!DOCTYPE html>\n<html lang="en-AU"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=index.html"><title>Moved</title>'
  '<script>var h=location.hash.slice(1);location.replace("index.html"+(h?"#"+h:""));</script></head>'
  '<body><p>Consent numbers are now in the Toxicity &amp; consent tab of each tumour-site page. <a href="index.html">Go to the home page</a>.</p></body></html>\n')
# Home
groupnav = ''.join(f'<a href="#{gid}" data-site="{gid}">{html.escape(head)}</a>' for gid,_,head,_,_ in GROUPS)
sections = ''.join(f'\n  <h2 class="group-title" id="{gid}" data-site="{gid}">{html.escape(head)}</h2>\n  <div class="hub" data-site="{gid}">{cards(pages)}</div>' for gid,_,head,pages,_ in GROUPS)
ALL = ['Breast','Thorax','Head and neck','Skin','CNS','Haematology','Sarcoma','Paediatrics','Palliative & oligometastases']
DONE = {head for _,_,head,_,_ in GROUPS} | {x for _,_,head,_,_ in GROUPS for x in head.split(' & ')}
soon = [x for x in ALL if x not in DONE]
cards_soon = ''.join(f'<div class="hubcard soon" aria-disabled="true"><h3>{s}</h3><p>Not added yet</p></div>' for s in soon)
home = f'''<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Radiation Oncology Quick Reference</title>
{FONTS}
<link rel="stylesheet" href="assets/site.css">
<link rel="stylesheet" href="assets/extras.css">
<link rel="manifest" href="manifest.webmanifest">
<meta name="theme-color" content="#10243f">
</head>
<body class="home">
<header class="top">
  <div class="top-inner" style="padding-bottom:12px">
    <div class="title-row">
      <h1>Radiation Oncology <span>Quick Reference</span></h1>
      <div class="hdr-right" style="display:flex;align-items:center;gap:10px;align-self:center;flex-shrink:0">{APPLINKS}<div class="meta">v{VERSION}</div></div>
    </div>
    <form class="search" role="search" id="siteSearch" onsubmit="return false">
      <label for="gq" class="note" style="position:absolute;left:-9999px">Search all pages</label>
      <input id="gq" type="search" placeholder="Search every page: border, dose, trial, structure" autocomplete="off">
      <button type="button" id="gclear">Clear</button>
    </form>
  </div>
</header>
<div class="layout">
<aside class="side">{tree('index.html')}</aside>
<main>
<div id="gresults" hidden></div>
<div id="homebody">
<div id="pinned" hidden></div>
<nav class="sitenav" aria-label="Tumour groups"><a href="links.html">Clinic links</a><a href="contacts.html">Contacts</a><a href="#tools">Tools</a>{groupnav}<a href="#contouring">Contouring</a></nav>
  <h2 class="group-title" id="tools">Tools and updates</h2>
  <div class="hub">{cards(TOOLS)}</div>
{sections}
  <h2 class="group-title" id="contouring" data-site="contouring">Contouring guides</h2>
  {contour_cards}
</div>
</main>
</div>
{FOOT.replace('RadOncReview GI document','RadOncReview tumour-site documents').replace('NCCN, ASTRO, ASCO','NCCN, ASTRO and others')}
{DISCLAIMER}
<p class="note" style="text-align:center;margin:8px 0 24px">Version {VERSION} · updated {VERSION_DATE}</p>
<script src="assets/site.js"></script>
<script src="assets/extras.js"></script>
</body>
</html>
'''
(root/'index.html').write_text(home)
# Every key trial shows its publication year: <b>NAME <span class="yr">(YYYY)</span></b>
_noyr = []
for _f in sorted(root.glob('src/*.html')):
    if _f.name == 'doses.html': continue
    for _m in re.finditer(r'<div class="trial"><b>(.*?)</b>', _f.read_text(), re.S):
        if 'class="yr"' not in _m.group(1): _noyr.append(f'{_f.name}: {re.sub("<[^>]+>", "", _m.group(1)).strip()}')
if _noyr:
    print(f'WARNING: {len(_noyr)} key trial(s) without a publication year (add <span class="yr">(YYYY)</span> inside the <b>):')
    for _x in _noyr: print('  ' + _x)
for _p in list(root.glob('*.html')) + list((root/'contouring').glob('*.html')):
    _t = _p.read_text(); _n = re.sub(r'\s*<p class="lede"[^>]*>\s*</p>', '', _t)
    # notes that link to a contouring guide become a solid call-out box
    _n = re.sub(r'<p class="note">(?=(?:(?!</p>).)*?<a href="(?:\.\./)?contouring/)', '<p class="note ctr-cta">', _n, flags=re.S)
    _n = re.sub(r'(<p class="note ctr-cta">(?:(?!</p>).)*?</a>)\.(\s*</p>)', r'\1\2', _n, flags=re.S)
    if not MORE_TABS: _n = re.sub(r'\n?<script src="(\.\./)?assets/more-tabs\.js"></script>', '', _n)
    if _n != _t: _p.write_text(_n)
print('built')

# ---------------- Search index and offline app files ----------------
from bs4 import BeautifulSoup as _BS
import json as _json, hashlib as _hl
_metare = re.compile(r'(<div class="meta">)([^<]*)(</div>)')
for _p in sorted(list(root.glob('*.html')) + list((root/'contouring').glob('*.html'))):
    _t = _p.read_text()
    _n = _metare.sub(lambda m: m.group(1) + re.sub(r'Synthesised Nov 2026|Nov 2026|v\d+\.\d+(?:\.\d+)?', 'v' + VERSION, m.group(2)) + m.group(3), _t)
    if _n != _t: _p.write_text(_n)
_idx = []; _files = ['index.html']
for _p in sorted(list(root.glob('*.html')) + list((root/'contouring').glob('*.html'))):
    _rel = str(_p.relative_to(root))
    _t = _p.read_text()
    if 'http-equiv="refresh"' in _t or _rel in ('index.html','gu.html'): continue
    _files.append(_rel) if _rel == 'doses.html' else None
    if _rel == 'doses.html': continue
    _files.append(_rel)
    _sp = _BS(_t, 'html.parser')
    _h1 = _sp.find('h1'); _ttl = re.sub(r'\s+',' ',_h1.get_text(' ',strip=True)).replace(' Quick Reference','') if _h1 else _rel
    for _pan in _sp.select('section.panel'):
        if _pan.get('data-tab') == 'eviq' or _pan.has_attr('data-borrowed') or _pan.has_attr('data-generated'): continue
        for _c in _pan.select('article.card'):
            _x = re.sub(r'\s+',' ',_c.get_text(' ',strip=True))
            _idx.append([_rel, _ttl, _pan.get('data-tab'), _pan.get('data-label'), _c.get('data-title') or '', _x])
(root/'assets'/'search-index.js').write_text('window.QR_INDEX=' + _json.dumps(_idx, ensure_ascii=False, separators=(',',':')) + ';')
_assets = ['assets/site.css','assets/extras.css','assets/protocol.css','assets/site.js','assets/extras.js','assets/tools.js','assets/scores.js','assets/staging.js','assets/rert.js','assets/more-tabs.js','assets/icon-genesis.png','assets/mdt.js','assets/roster.js','assets/search-index.js','assets/icon-192.png','assets/icon-512.png','manifest.webmanifest']
(root/'manifest.webmanifest').write_text(_json.dumps({'name':'Radiation Oncology Quick Reference','short_name':'RadOnc QR','start_url':'./index.html','scope':'./','display':'standalone','background_color':'#f3f5f6','theme_color':'#10243f','icons':[{'src':'assets/icon-192.png','sizes':'192x192','type':'image/png'},{'src':'assets/icon-512.png','sizes':'512x512','type':'image/png','purpose':'any maskable'}]}, indent=1))
_ver = _hl.md5(''.join((root/x).read_text(errors='ignore') if not x.endswith('.png') else x for x in _files+_assets).encode()).hexdigest()[:10]
(root/'sw.js').write_text("""// Generated by build.py. Network first (2.5 s), then the offline copy.
const V='qr-%s';const FILES=%s;
self.addEventListener('install',e=>{self.skipWaiting();e.waitUntil(caches.open(V).then(c=>Promise.allSettled(FILES.map(f=>c.add(new Request(f,{cache:'reload'}))))));});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==V).map(x=>caches.delete(x)))).then(()=>self.clients.claim()));});
self.addEventListener('fetch',e=>{const r=e.request;if(r.method!=='GET'||new URL(r.url).origin!==location.origin)return;
 e.respondWith((async()=>{const c=await caches.open(V);const hit=await c.match(r,{ignoreSearch:true});
  const net=fetch(r).then(x=>{if(x.ok)c.put(r,x.clone());return x;});
  if(!hit)return net;
  return Promise.race([net.catch(()=>hit),new Promise(res=>setTimeout(()=>res(hit),2500))]);})());});
""" % (_ver, _json.dumps(_files+_assets)))
print('search index', len(_idx), 'cards;', len(_files), 'pages')
