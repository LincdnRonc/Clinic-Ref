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
 'ctr-bladder.html':'gu','ctr-kidney-liver.html':'gu','contouring/prostate.html':'gu','contouring/rectal-long-course.html':'gi','contouring/liver-sbrt.html':'gi','ctr-library.html':'contouring'}
def _ds(f): return f' data-site="{CTR_SITE[f]}"' if f in CTR_SITE else ''
def sitenav(current, group):
    links = ['<a href="index.html">Home</a>']
    for f,short,_,_ in group:
        cur = ' aria-current="page"' if f==current else ''
        links.append(f'<a href="{f}"{cur}{_ds(f)}>{html.escape(short)}</a>')
    return '<nav class="sitenav" aria-label="All pages">' + ''.join(links) + '</nav>'
def page(f, short, long, desc, group, gname, gid, foot):
    body = (root/'src'/f).read_text() + eviq_panel(f)
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
<main id="main">
{sitenav(f, group)}
<div class="empty" id="empty">No cards match. Try a shorter term such as a trial name, a dose (50/25) or a drug.</div>
{body}
</main>
{foot}
<script src="assets/site.js"></script>
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
] + EXTRA
for gid,gname,_,pages,foot in GROUPS:
    for g in pages:
        (root/g[0]).write_text(page(*g, pages, gname, gid, foot))
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
def build_library():
    out=[]
    for i,(tid,label,lede,cards_) in enumerate(LIB):
        h=' hidden' if i else ''
        out.append(f'<section class="panel" id="p-{tid}" data-tab="{tid}" data-label="{html.escape(label)}"{h}>\n  <div class="panel-head">\n    <h2>{html.escape(label)}</h2>\n    <p class="lede">{html.escape(lede)}</p>\n    <div class="jump"></div>\n  </div>')
        prot = [c for c in CONTOUR if tid in c[4]]
        if prot:
            out.append('  <article class="card key" data-title="Our quick protocols"><h3>Our quick protocols</h3><ul class="eviq">'+''.join(f'<li><a href="{f}">{html.escape(long)}</a></li>' for f,short,long,desc,tags in prot)+'</ul></article>')
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
 ('ctr-breast.html','Breast','Breast contouring protocol','ESTRO breast, chest wall and nodal borders, tumour bed, implant reconstruction, cardiac OARs.',('breast',)),
 ('ctr-thorax.html','Thorax','Thorax contouring protocol','LA-NSCLC GTV/CTV/ITV, PORT stations, SBRT, SCLC and thoracic OAR definitions.',('thorax',)),
 ('ctr-hn.html','H&N','Head and neck contouring protocol','5 + 5 mm CTV-P, neck levels I–X landmarks, level selection, post-op, PNI and OARs.',('hn',)),
 ('ctr-cns.html','CNS','CNS contouring protocol','Glioblastoma (15 mm CTV), IDH-mutant glioma, meningioma and skull base, cavity SRS, hippocampus.',('cns',)),
 ('ctr-upper-gi.html','Upper GI','Upper GI contouring protocol','Oesophagus/GEJ margins, gastric nodal stations, post-op and SBRT pancreas, abdominal OARs.',('gi',)),
 ('ctr-anal.html','Anal','Anal canal contouring protocol','AGITG regions A, B and C, primary and nodal margins, inguinal borders, pitfalls.',('gi',)),
 ('ctr-gyn.html','Gynae','Gynae contouring protocol','Intact cervix CTV components, post-op cuff ITV, vulva, and IGABT HR-CTV / IR-CTV.',('gyn',)),
 ('ctr-heme.html','Lymphoma','Lymphoma ISRT contouring protocol','ILROG pre-chemo GTV to ISRT CTV, indolent RT alone, and extranodal organ CTVs.',('heme',)),
 ('ctr-sarcoma.html','Sarcoma','Sarcoma contouring protocol','Extremity 3 cm / 1.5 cm CTV with oedema, post-op, and retroperitoneal volumes.',('sarc',)),
 ('ctr-bladder.html','Bladder','Bladder contouring protocol','Whole-bladder and tumour CTV, simulation and adaptive IGRT, post-cystectomy side walls and bed.',('gu',)),
 ('ctr-kidney-liver.html','Kidney & liver','Kidney and liver SBRT contouring protocol','Primary kidney SABR (IROCK) and liver SBRT: imaging, GTV rules, motion, OARs.',('gu','gi')),
 ('ctr-skin.html','Skin','Skin contouring protocol','BCC/cSCC clinical margins, electron and orthovoltage fields, post-op cSCC, PNI, Merkel and melanoma.',('sarc',)),
 ('ctr-peds.html','Paeds','Paediatric contouring protocol','CSI CTV pitfalls, CNS boosts, pre-chemo CTV rules for RMS, Ewing, Wilms, neuroblastoma; paediatric OARs.',('peds',)),
 ('ctr-spine.html','Spine & bone','Spine and bone SBRT contouring protocol','ISRC six-sector rules, post-op epidural donut, sacral and non-spine bone CTV.',('sbrt',)),
]
(root/'src'/'ctr-library.html').write_text(build_library())
CNAV = [(f,short,long,desc) for f,short,long,desc,_ in CONTOUR] + [
 ('contouring/prostate.html','Prostate','Prostate contouring protocol','Intact prostate and SVs, prostate bed, NRG pelvic nodes, CT vs MRI apex/base pearls, IGRT, OARs.'),
 ('contouring/rectal-long-course.html','Rectum','Rectal long-course atlas','Elective compartments and borders, GTV criteria, 45 vs 50–54 Gy volumes.'),
 ('contouring/liver-sbrt.html','Liver SBRT OARs','Liver SBRT OAR contouring protocol','Liver, luminal GI and other OARs on CT and MRI, central hepatobiliary tract, MR-linac re-contouring zone, UK 2022 constraints.')]
FOOT_CTR = '<footer><p>Quick-reference summaries of published contouring guidelines, written in our own words. Borders are condensed; anything marked for checking should be confirmed against the original paper and its images. Not affiliated with or endorsed by ESTRO, NRG, ILROG, AGITG or other groups. Follow departmental protocols.</p></footer>'
for f,short,long,desc,_ in CONTOUR:
    (root/f).write_text(page(f,short,long,desc,CNAV,'Contouring','contouring',FOOT_CTR))
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
</head>
<body>
<header class="top">
  <div class="top-inner" style="padding-bottom:12px">
    <div class="title-row">
      <h1>Radiation Oncology <span>Quick Reference</span></h1>
      <div class="meta">Synthesised Nov 2026</div>
    </div>
    <p class="lede" style="margin:4px 0 0">Clinic-ready summaries by tumour site: management by stage, doses, planning volumes and constraints, consent numbers and landmark trials.</p>
  </div>
</header>
<main>
<nav class="sitenav" aria-label="Tumour groups">{groupnav}<a href="#contouring">Contouring</a></nav>
{sections}
  <h2 class="group-title" id="contouring" data-site="contouring">Contouring guidelines and protocols</h2>
  <div class="hub">{contour_cards}</div>
{('<h2 class="group-title" id="soon">Still to add</h2><div class="hub">'+cards_soon+'</div>') if soon else ''}
</main>
{FOOT.replace('RadOncReview GI document','RadOncReview tumour-site documents').replace('NCCN, ASTRO, ASCO','NCCN, ASTRO and others')}
</body>
</html>
'''
(root/'index.html').write_text(home)
print('built')
