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
def eviq_panel(f):
    items = EVIQ.get(f)
    if not items: return ''
    li = ''.join(f'<li><a href="{html.escape(u)}" target="_blank" rel="noopener">{(html.escape(i)+" · ") if i else ""}{html.escape(t)}</a></li>' for i,t,u in items)
    return f'''
<section class="panel" id="p-eviq" data-tab="eviq" data-label="eviQ protocols" hidden>
  <div class="panel-head">
    <h2>eviQ protocols</h2>
    <p class="lede">Links to the current Australian eviQ radiation oncology protocols for this site. They open on eviQ, which is the authoritative and up-to-date source; no eviQ content is copied here.</p>
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
 'ctr-bladder.html':'gu','ctr-kidney-liver.html':'gu','contouring/prostate.html':'gu','contouring/bladder.html':'gu','contouring/rectal-long-course.html':'gi','contouring/liver-sbrt.html':'gi','contouring/thorax.html':'thorax','contouring/biliary.html':'gi','contouring/pancreas-stomach.html':'gi','contouring/oesophagus.html':'gi','contouring/breast.html':'breast','contouring/gynae.html':'gyn','contouring/anal.html':'gi','contouring/spine-bone.html':'pall','contouring/cns.html':'cns','contouring/head-neck.html':'hn','contouring/lymphoma.html':'heme','ctr-library.html':'contouring','ctr-mim.html':'contouring','ctr-monaco.html':'contouring'}
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
        links = ''.join(f'<a href="{pg[0]}"{" aria-current=\"page\"" if pg[0]==current else ""}>{html.escape(pg[1])}</a>' for pg in pages)
        out.append(f'<details data-site="{gid}"{" open" if here else ""}><summary>{html.escape(head)}</summary>{links}</details>')
    return ('<details class="menu"><summary><span class="burger" aria-hidden="true"></span>All pages</summary>'
            '<nav class="tree" aria-label="All pages"><a class="home" href="index.html">Home</a><a class="home" href="index.html#search">Search all pages</a>' + ''.join(out) + '</nav></details>')
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
def tools_bar(gid):
    if gid not in _SCORETAB: return ''
    t,l = _SCORETAB[gid]
    return f'<p class="xref"><b>Calculators:</b> <a href="scores.html#{t}">{l} scores and nomograms</a> · <a href="tools.html">EQD2, BED and re-irradiation</a></p>'
DISCLAIMER = '<footer class="disclaimer"><p><b>Personal resource, not for distribution.</b> This site is the author\'s personal working reference. Every effort is made to keep it accurate, but it may contain errors or be out of date. Anyone else who uses it must exercise their own clinical judgement and independently verify all information, including doses, volumes, constraints, scores and calculator results, against primary sources and local protocols. It is not medical advice and not a medical device.</p></footer>'
def page(f, short, long, desc, group, gname, gid, foot):
    body = (root/'src'/f).read_text() + eviq_panel(f)
    if f.startswith('exam-'): body = xref_back(f, body)
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
      <h1>{html.escape(long)} <span>Quick Reference</span></h1>
      <div class="meta">Synthesised Nov 2026</div>
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
{xref_bar(f)}
{tools_bar(gid)}
<div class="empty" id="empty">No cards match. Try a shorter term such as a trial name, a dose (50/25) or a drug.</div>
{body}
</main>
</div>
{foot}
{DISCLAIMER}
<script src="assets/site.js"></script>
<script src="assets/extras.js"></script>
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
 ('benign.html','Benign MSK','Benign musculoskeletal','Heterotopic ossification 7/1, osteoarthritis, plantar fasciitis and Dupuytren\'s low-dose RT.'),
]
PALL = [
 ('pall-brain.html','Brain metastases','Brain metastases','SRS vs WBRT, SRS dose by size, cavity SRS, HA-WBRT + memantine, necrosis limits, QUARTZ.'),
 ('pall-wbrt.html','WBRT principles','Whole-brain radiotherapy principles','Who still needs WBRT, 20/5 vs 30/10 vs PCI doses, HA technique, memantine and amantadine, acute/subacute/late toxicity timeline, consent rates.'),
 ('pall-bone-spine.html','Bone, cord & spine SBRT','Bone metastases, cord compression and spine SBRT','8/1 vs multiple fractions, SC.24, MSCC (NOMS, SINS, SCORAD), HyTEC cord limits, VCF.'),
 ('pall-oligo.html','Oligomets & palliation','Oligometastases and general palliation','SABR-COMET, CURB, NRG-LU002; palliative regimens for lung, SVC, H&N, bleeding, liver and coeliac plexus.'),
]
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
 ('mrl','MR-linac','MR-linac',MRL,FOOT_MRL),
 ('exam','Exam summary','Phase 2 exam summary',EXAM,FOOT_EXAM),
] + EXTRA
# old gu.html -> redirect to home GU section
(root/'gu.html').write_text('<!DOCTYPE html>\n<html lang="en-AU"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=index.html#gu"><title>GU Quick Reference</title></head><body><p>The GU reference is now split by tumour site. <a href="index.html#gu">Go to the GU pages</a>.</p></body></html>\n')
def cards(pages): return ''.join(f'<a class="hubcard" href="{f}"{_ds(f)}><h3>{html.escape(long)}</h3><p>{html.escape(desc)}</p></a>' for f,short,long,desc in pages)

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
 ('contouring/head-neck.html','Head and neck contouring guide',('hn',)),('contouring/cns.html','CNS contouring guide',('cns',)),
 ('contouring/oesophagus.html','Oesophagus and GOJ contouring guide',('gi',)),('contouring/pancreas-stomach.html','Pancreas and stomach contouring guide',('gi',)),
 ('contouring/biliary.html','Cholangiocarcinoma and gallbladder contouring guide',('gi',)),('contouring/liver-sbrt.html','Liver SBRT OAR contouring guide',('gi',)),
 ('contouring/rectal-long-course.html','Rectal long-course atlas',('gi',)),('contouring/anal.html','Anal canal contouring guide',('gi',)),
 ('contouring/prostate.html','Prostate contouring guide',('gu',)),('contouring/bladder.html','Bladder contouring guide',('gu',)),
 ('contouring/gynae.html','Gynaecological contouring guide',('gyn',)),('contouring/lymphoma.html','Lymphoma ISRT contouring guide',('heme',)),
 ('contouring/spine-bone.html','Spine and bone SBRT contouring guide',('sbrt',))]]
def build_library():
    out=[]
    for i,(tid,label,lede,cards_) in enumerate(LIB):
        h=' hidden' if i else ''
        out.append(f'<section class="panel" id="p-{tid}" data-tab="{tid}" data-label="{html.escape(label)}"{h}>\n  <div class="panel-head">\n    <h2>{html.escape(label)}</h2>\n    <p class="lede">{html.escape(lede)}</p>\n    <div class="jump"></div>\n  </div>')
        prot = [c for c in CONTOUR if tid in c[4]] + [c for c in LIB_FULL if tid in c[4]]
        if prot:
            out.append('  <article class="card key" data-title="Our guides"><h3>Our guides</h3><ul class="eviq">'+''.join(f'<li><a href="{f}">{html.escape(long)}</a></li>' for f,short,long,desc,tags in prot)+'</ul></article>')
        for title,entries in cards_:
            lis=[]
            for yr,t,cite,note,l,star in sorted(entries,key=lambda e:not e[5]):
                u,kind=_link(l)
                st='<span class="libstar">Start here</span> ' if star else ''
                y=f'{yr} · ' if yr else ''
                lis.append(f'<li>{st}<a href="{html.escape(u)}" target="_blank" rel="noopener">{html.escape(t)}</a><span class="libmeta">{y}{html.escape(cite)} · {kind}</span><span class="libnote">{html.escape(note)}</span></li>')
            out.append(f'  <article class="card" data-title="{html.escape(title)}"><h3>{html.escape(title)}</h3><ul class="lib">{"".join(lis)}</ul></article>')
        out.append('</section>')
    out.append('<p class="note">Links marked PubMed open the abstract (verified PMID); "PubMed search" runs a title search where the PMID has not been checked yet. ESTRO-ACROP guidelines and Clin Transl Radiat Oncol papers are usually free to read; many IJROBP atlases are free as PubMed Central author manuscripts.</p>')
    return '\n'.join(out)
# (file, short, long, desc, library tabs)
CONTOUR = [
 ('ctr-library.html','Library','Contouring guideline library','Every major international contouring guideline and atlas by tumour site, old and new, with links.',()),
 ('ctr-sarcoma.html','Sarcoma','Sarcoma contouring guide','Extremity 3 cm / 1.5 cm CTV with oedema, post-op, and retroperitoneal volumes.',('sarc',)),
 ('ctr-kidney-liver.html','Kidney SABR','Kidney SABR contouring guide','Primary kidney SABR (IROCK): GTV, ITV and PTV, motion management and OARs. Quick guide only.',('gu',)),
 ('ctr-skin.html','Skin','Skin contouring guide','BCC/cSCC clinical margins, electron and orthovoltage fields, post-op cSCC, PNI, Merkel and melanoma.',('sarc',)),
 ('ctr-peds.html','Paeds','Paediatric contouring guide','CSI CTV pitfalls, CNS boosts, pre-chemo CTV rules for RMS, Ewing, Wilms, neuroblastoma; paediatric OARs.',('peds',)),
]
(root/'src'/'ctr-library.html').write_text(build_library())
CNAV = [(f,short,long,desc) for f,short,long,desc,_ in CONTOUR] + [
 ('contouring/breast.html','Breast','Breast contouring guide','Whole breast, tumour bed and SIB, partial breast with trial volumes, multicatheter APBI, chest wall with and without implants, ESTRO/RTOG nodal borders, Liverpool DVH scorecards.'),
 ('contouring/cns.html','CNS','CNS contouring guide','Glioblastoma (ESTRO-EANO 2023), IDH-mutant glioma (2025), meningioma (RTOG 0539/EORTC), vestibular schwannoma, SRS for metastases and cavities, HA-WBRT, EPTN OAR constraints.'),
 ('contouring/gynae.html','Gynae','Gynaecological contouring guide','Cervix EBRT (EMBRACE II ITV and nodal SIB), MRI-guided brachytherapy targets and aims, post-op cervix and endometrium, vaginal vault and vaginal cancer, vulva definitive and post-op, inguinal margins, constraints.'),
 ('contouring/spine-bone.html','Spine & bone SBRT','Spine and bone SBRT contouring guide','St George selection and workflow, ISRC sector CTV table, post-op spine, sacrum (Dunne), non-spine bone and soft tissue, re-irradiation cord limits, 1–5 fraction constraints.'),
 ('contouring/head-neck.html','Head & neck','Head and neck contouring guide','Neck level border tables (Grégoire 2014), 5 + 5 mm primary CTV, Biau 2019 level selection, DAHANCA post-op, PATHOS, NPC 2024 dose levels, HNCIG cSCC, PNI pathways, DAHANCA constraints.'),
 ('contouring/lymphoma.html','Lymphoma ISRT','Lymphoma ISRT contouring guide','ILROG pre- and post-chemo GTV, ISRT CTV for indolent, early HL/DLBCL, mediastinal, advanced and extranodal disease, doses, mini-atlas margins.'),
 ('contouring/thorax.html','Thorax','Thorax contouring guide','Lung SABR (peripheral, central, ultracentral), stage II–III definitive, PORT, limited-stage SCLC, IASLC station borders and landmarks, thoracic OAR definitions and constraints.'),
 ('contouring/prostate.html','Prostate','Prostate contouring guide','Intact prostate and SVs, prostate bed, NRG pelvic nodes, CT vs MRI apex/base pearls, IGRT, OARs.'),
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
CNAV = CNAV[:1] + sorted(CNAV[1:], key=lambda c: c[1].lower())
CNAV += SOFTWARE
# ---------------- Tools: calculators, consent numbers, doses at a glance, what's new ----------------
TOOLS = [
 ('tools.html','Calculators','Calculators and tools','EQD2 and BED, cumulative dose across courses, treatment gap, and links to re-irradiation tools and SABR constraint tables.'),
 ('scores.html','Clinical scores','Clinical scores and nomograms','Child-Pugh, ALBI, MELD, PSA doubling time, Roach, CAPRA, CTS5, Van Nuys, SINS, Mirels, RPA, IPI, Sedlis, brachytherapy EQD2 and more, with links to MSKCC, PREDICT, GPA and other external tools.'),
 ('consent.html','Consent numbers','Consent numbers by site','The toxicity rates to quote, gathered from every tumour-site page. Print one site as a sheet.'),
 ('doses.html','Doses at a glance','Doses at a glance','Dose and fractionation cards from every tumour-site page in one place.'),
 ('whats-new.html',"What's new","What's new",'New evidence and landmark trials by tumour site, and changes to this site.'),
]
FOOT_TOOLS = '<footer><p>Calculators use the linear-quadratic model and are for education and cross-checking only; they are not a medical device. Verify every result independently. Consent numbers and doses are copied from the tumour-site pages, where the sources are cited. Follow departmental protocols.</p></footer>'
def _panels(f):
    t = (root/'src'/f).read_text()
    return re.findall(r'<section class="panel" id="p-([\w-]+)" data-tab="[\w-]+" data-label="([^"]+)"[^>]*>(.*?)</section>', t, re.S)
def _cards(body):
    return re.findall(r'<article class="card[^"]*" data-title="([^"]*)">.*?</article>', body, re.S), re.findall(r'(<article class="card.*?</article>)', body, re.S)
def _gather(pick):
    out = []
    for i,(gid,gname,head,pages,_) in enumerate(GROUPS):
        if gid in ('exam','mrl'): continue
        parts = []
        for g in pages:
            f, short, long = g[0], g[1], g[2]
            got = []
            for pid,label,body in _panels(f):
                titles, arts = _cards(body)
                got += [a for t,a in zip(titles,arts) if pick(pid,label,t)]
            if got:
                parts.append(f'<article class="card key" data-title="{html.escape(long)}"><h3>{html.escape(long)}</h3><p class="note">From the <a href="{f}">{html.escape(long)}</a> page, where sources and trials are cited.</p></article>' + ''.join(got))
        if parts:
            out.append(f'<section class="panel" id="p-{gid}" data-tab="{gid}" data-label="{html.escape(head)}"{" hidden" if out else ""}>\n<div class="panel-head"><h2>{html.escape(head)}</h2><div class="jump"></div><p><button type="button" class="printbtn" onclick="window.print()">Print this site</button></p></div>\n' + ''.join(parts) + '\n</section>')
    return '\n'.join(out)
(root/'src'/'consent.html').write_text(_gather(lambda pid,label,t: pid in ('consent','toxicity') or re.search(r'consent|toxicit', t, re.I)))
(root/'src'/'doses.html').write_text(_gather(lambda pid,label,t: re.search(r'\bdoses?\b|fractionation|regimen', t, re.I) and not re.search(r'constraint|OAR|toxicit|limit', t, re.I)))
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
    site_ = ''.join(f'<li><b>{d}</b> · {html.escape(t)}' + (f' <a href="{p}">Open</a>' if p else '') + '</li>' for d,t,p in _wn.SITE)
    return (f'<section class="panel" id="p-evidence" data-tab="evidence" data-label="Evidence"><div class="panel-head"><h2>New evidence and landmark trials</h2><p class="lede">Summaries are in our own words; open the source for the full paper. Tags are a first read, not a guideline.</p><div class="jump"></div></div>{cards_}</section>\n'
            f'<section class="panel" id="p-site" data-tab="site" data-label="Site updates" hidden><div class="panel-head"><h2>Site updates</h2><div class="jump"></div></div><article class="card" data-title="Change log"><h3>Change log</h3><ul>{site_}</ul></article></section>')
(root/'src'/'whats-new.html').write_text(_wn_page())
for g in TOOLS:
    (root/g[0]).write_text(page(*g, TOOLS, 'Tools', 'tools', FOOT_TOOLS))

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
    (root/f).write_text(_proto_convert(srcp.read_text(), f, long, short, CTR_SITE.get(f,'contouring'), tree(f), FONTS, FOOT_CTR + DISCLAIMER, _qp.read_text() if _qp.exists() else None))
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
contour_cards = cards(CNAV)
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
<body>
<header class="top">
  <div class="top-inner" style="padding-bottom:12px">
    <div class="title-row">
      <h1>Radiation Oncology <span>Quick Reference</span></h1>
      <div class="meta">Synthesised Nov 2026</div>
    </div>
    <p class="lede" style="margin:4px 0 0">Clinic-ready summaries by tumour site: management by stage, doses, planning volumes and constraints, consent numbers and landmark trials.</p>
    <p class="note" style="margin:4px 0 0"><b>Personal resource, not for distribution.</b> Verify everything independently and use your own clinical judgement; full notice at the foot of each page.</p>
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
<nav class="sitenav" aria-label="Tumour groups"><a href="#tools">Tools</a>{groupnav}<a href="#contouring">Contouring</a></nav>
  <h2 class="group-title" id="tools">Tools and updates</h2>
  <div class="hub">{cards(TOOLS)}</div>
{sections}
  <h2 class="group-title" id="contouring" data-site="contouring">Contouring library and guides</h2>
  <div class="hub">{contour_cards}</div>
{('<h2 class="group-title" id="soon">Still to add</h2><div class="hub">'+cards_soon+'</div>') if soon else ''}
</div>
</main>
</div>
{FOOT.replace('RadOncReview GI document','RadOncReview tumour-site documents').replace('NCCN, ASTRO, ASCO','NCCN, ASTRO and others')}
{DISCLAIMER}
<script src="assets/site.js"></script>
<script src="assets/extras.js"></script>
</body>
</html>
'''
(root/'index.html').write_text(home)
print('built')

# ---------------- Search index and offline app files ----------------
from bs4 import BeautifulSoup as _BS
import json as _json, hashlib as _hl
_idx = []; _files = ['index.html']
for _p in sorted(list(root.glob('*.html')) + list((root/'contouring').glob('*.html'))):
    _rel = str(_p.relative_to(root))
    _t = _p.read_text()
    if 'http-equiv="refresh"' in _t or _rel in ('index.html','gu.html'): continue
    _files.append(_rel) if _rel in ('consent.html','doses.html') else None
    if _rel in ('consent.html','doses.html'): continue
    _files.append(_rel)
    _sp = _BS(_t, 'html.parser')
    _h1 = _sp.find('h1'); _ttl = re.sub(r'\s+',' ',_h1.get_text(' ',strip=True)).replace(' Quick Reference','') if _h1 else _rel
    for _pan in _sp.select('section.panel'):
        if _pan.get('data-tab') == 'eviq': continue
        for _c in _pan.select('article.card'):
            _x = re.sub(r'\s+',' ',_c.get_text(' ',strip=True))
            _idx.append([_rel, _ttl, _pan.get('data-tab'), _pan.get('data-label'), _c.get('data-title') or '', _x])
(root/'assets'/'search-index.js').write_text('window.QR_INDEX=' + _json.dumps(_idx, ensure_ascii=False, separators=(',',':')) + ';')
_assets = ['assets/site.css','assets/extras.css','assets/protocol.css','assets/site.js','assets/extras.js','assets/tools.js','assets/scores.js','assets/search-index.js','assets/icon-192.png','assets/icon-512.png','manifest.webmanifest']
(root/'manifest.webmanifest').write_text(_json.dumps({'name':'Radiation Oncology Quick Reference','short_name':'RadOnc QR','start_url':'./index.html','scope':'./','display':'standalone','background_color':'#f3f5f6','theme_color':'#10243f','icons':[{'src':'assets/icon-192.png','sizes':'192x192','type':'image/png'},{'src':'assets/icon-512.png','sizes':'512x512','type':'image/png','purpose':'any maskable'}]}, indent=1))
_ver = _hl.md5(''.join((root/x).read_text(errors='ignore') if not x.endswith('.png') else x for x in _files+_assets).encode()).hexdigest()[:10]
(root/'sw.js').write_text("""// Generated by build.py. Network first (2.5 s), then the offline copy.
const V='qr-%s';const FILES=%s;
self.addEventListener('install',e=>{self.skipWaiting();e.waitUntil(caches.open(V).then(c=>Promise.allSettled(FILES.map(f=>c.add(f)))));});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==V).map(x=>caches.delete(x)))).then(()=>self.clients.claim()));});
self.addEventListener('fetch',e=>{const r=e.request;if(r.method!=='GET'||new URL(r.url).origin!==location.origin)return;
 e.respondWith((async()=>{const c=await caches.open(V);const hit=await c.match(r,{ignoreSearch:true});
  const net=fetch(r).then(x=>{if(x.ok)c.put(r,x.clone());return x;});
  if(!hit)return net;
  return Promise.race([net.catch(()=>hit),new Promise(res=>setTimeout(()=>res(hit),2500))]);})());});
""" % (_ver, _json.dumps(_files+_assets)))
print('search index', len(_idx), 'cards;', len(_files), 'pages')
