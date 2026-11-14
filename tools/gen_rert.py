import html, pathlib
out = pathlib.Path(__file__).resolve().parent.parent / 'src'
V = '<span class="flag caution">Verify</span>'
AU = '<span class="flag au">AU</span>'
def tbl(head, rows, wide=True):
    h = ''.join(f'<th>{c}</th>' for c in head)
    r = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in row) + '</tr>' for row in rows)
    return f'<div class="tw{" wide" if wide else ""}"><table><tr>{h}</tr>{r}</table></div>'
def ul(items): return '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'
def card(title, body, key=False):
    return f'<article class="card{" key" if key else ""}" data-title="{html.escape(title, quote=True)}"><h3>{title}</h3>{body}</article>'
def panel(pid, label, h2, lede, cards, first=False):
    return f'<section class="panel" id="p-{pid}" data-tab="{pid}" data-label="{label}"{"" if first else " hidden"}>\n<div class="panel-head"><h2>{h2}</h2><p class="lede">{lede}</p><div class="jump"></div></div>\n' + '\n'.join(cards) + '\n</section>\n'
def a(url, text): return f'<a href="{url}" target="_blank" rel="noopener">{text}</a>'
def note(t): return f'<p class="note">{t}</p>'
JS = '<script src="assets/rert.js"></script>'
def write(name, panels, js=False): (out/name).write_text(''.join(panels) + (JS if js else ''))
CAVEAT = note('Reirradiation evidence is mostly retrospective and consensus-based. Figures here are cited to their source; anything marked ' + V + ' was entered from memory. Constraints are starting points for an individual decision, not guarantees of safety. Have a colleague and physics review each case.')

# =============================================================== 1. principles
write('rert-principles.html', [
 panel('define','Define & decide','Is it reirradiation, and should we do it?','ESTRO–EORTC consensus definitions and decision statements (Andratschke 2022).',
  [card('Definitions (ESTRO–EORTC 2022)', tbl(['Term','Overlap of irradiated volumes?','Concern about cumulative toxicity?','Example'],[
     ('<b>Reirradiation type 1</b>','Yes','With or without','In-field recurrence; new target inside a prior field'),
     ('<b>Reirradiation type 2</b>','No','Yes','Second lung target with no overlap but cumulative lung or cord dose is a concern'),
     ('<b>Repeat organ irradiation</b>','No','No','Second target in the same organ, far from the first'),
     ('<b>Repeat irradiation</b>','No','No','New course to a different organ')]) +
     note('Decision tree: (1) geometric overlap of irradiated volumes? (2) concern for toxicity from cumulative dose? (3) targets in the same organ? Record the type in the notes and the prescription. Source: Andratschke et al. Lancet Oncol 2022;23:e469–78.') + CAVEAT, key=True),
   card('Decision statements worth knowing', ul([
     'Discuss alternatives and salvage options in a multidisciplinary team and with the patient; define and state the intent (S1, S3).',
     'High-dose curative reirradiation is not recommended if estimated survival is under 6 months (S5).',
     'Within 6 months of the prior course, weigh benefit against toxicity especially carefully (S7).',
     'Do not offer high-dose curative reirradiation if the best response to the first course was progression (S8); judge on the response to and benefit from the first course, not on general radiobiology (S9).',
     'Persistent grade ≥3 toxicity from the first course: discuss critically, taking the patient\'s risk acceptance into account (S6).',
     'For limited life expectancy, reirradiation for symptoms may be considered even when cumulative doses are excessive (S2).',
     'Prioritise target and OAR doses by life expectancy, risk acceptance and treatment goal (S17). Latency of irreversible toxicity can be shorter after reirradiation (S18).',
     '<b>RCR Principles of reirradiation (2024):</b> discuss in the tumour-site MDT and in a separate radiotherapy forum; ideally at least six months from the first course; ECOG performance status 2 or better; classify by the ESTRO–EORTC system; consider biopsy; prospective peer review of contours and plans; cone-beam CT with online matching at every fraction; record cumulative EQD2 or BED with the α/β and any recovery used.']) +
     note('Agreement 76–100% across statements. Source: Andratschke 2022, Table 2.')),
   card('Who does well: common threads across sites', ul([
     'Longer interval since the first course (head and neck RPA uses 2 years; most guidelines set a 6-month minimum).',
     'Small volume, resected or resectable disease, good performance status, no persistent severe toxicity or organ dysfunction.',
     'No or limited distant disease; a durable response to the first course.',
     'A target that can be treated with a tight margin and no elective volume.']))], first=True),
 panel('workflow','Clinic workflow','What to collect and how to add the doses','A working checklist built on the ESTRO–EORTC reporting items and the ReCOG 2026 dose-evaluation consensus.',
  [card('At the first visit: collect', ul([
     '<b>Every prior course:</b> dates, site, dose and fractionation, technique, and the plan in DICOM (CT, structures, dose) if at all possible. Request it from the treating centre on the day.',
     '<b>Response and toxicity:</b> best response, time to recurrence, acute and late toxicity graded by CTCAE, current organ function (swallow, lung function, bowel, bladder, neurology).',
     '<b>The recurrence:</b> histology where feasible, restaging (PET-CT, MRI of the region), in-field versus marginal versus out-of-field.',
     '<b>The patient:</b> performance status, comorbidity, life expectancy, systemic options, what risk they will accept.',
     '<b>Alternatives:</b> surgery, systemic therapy, ablation, best supportive care: documented MDT discussion.']) + note('Reporting items: Andratschke 2022, Table 1.'), key=True),
   card('Adding the doses', ul([
     '<b>Prior plan available electronically:</b> a 3D overlay of the dose distributions is mandatory (S15). Rigid registration first; deformable when anatomy has changed; always check the fusion visually.',
     '<b>Only fields, films or a summary:</b> reconstruct conservatively (S14).',
     '<b>Nothing available:</b> assume the prescription dose was given homogeneously to the region or organ (S13).',
     '<b>Convert before summing:</b> use EQD2 or BED whenever fraction sizes differ (S16), with the α/β used for first-course constraints (S10).',
     '<b>Serial organs:</b> judge on maximum dose. <b>Parallel organs:</b> judge on irradiated volume (S11).',
     '<b>Three levels of rigour</b> (ReCOG case guide): direct point-dose summation; point-dose summation within the overlap region; image-registration-based 3D summation of equieffective dose. Choose by overlap complexity and how close an OAR is to tolerance.',
     'Two accepted ways to set the new plan\'s limits: first-course constraints with a discount for the prior dose, or cumulative constraints on the summed dose (ESTRO/EANO 2025; ESTRO thoracic 2026).']) +
     note('Sources: Andratschke 2022; Paradis et al. ReCOG consensus, Lancet Oncol 2026;27:e101–10; ReCOG case-based guide (PMID 41985779).')),
   card('Document in the plan', ul(['Reirradiation type (1 or 2), intent and goal.','Interval, prior dose to each OAR of concern, α/β and any recovery assumed, with the source of the constraint.','Registration method and summation method (point or 3D; physical or EQD2).','Cumulative OAR doses achieved, and which objectives were prioritised or compromised.','That the patient was told of the specific severe risks.'])),
   card('Planning habits', ul(['No elective volumes; tight GTV-to-CTV margins; daily volumetric IGRT.','Cascade: full target dose if OARs allow; then compromise PTV coverage next to the OAR; then change the prescription (ESTRO/EANO 2025).','Consider hyperfractionation where late toxicity dominates (nasopharynx, rectum) and SBRT where the overlap is small.','Tools: <a href="tools.html">EQD2/BED and cumulative dose calculators</a> · '+a('https://oardoselimitcalculator.netlify.app/','OAR dose limit calculator (Tim Wang)')+' · <a href="rert-constraints.html#calc">remaining-dose calculator</a>.']))]),
 panel('radiobiology','Radiobiology','EQD2, BED and recovery','The arithmetic, and how much recovery it is reasonable to assume.',
  [card('Formulas', ul(['BED = D × (1 + d / (α/β)).','EQD2 = D × (d + α/β) / (2 + α/β).','Use the dose per fraction actually received by the organ, not the prescription fraction size, when you have it.','Typical α/β: 2 Gy for cord and nerves (4 Gy lumbar cord in Nieder), 3 Gy for most late-responding tissues, 10 Gy for tumour and acute effects.']) + note('Survey of clinical practice: α/β of 3 Gy was the most common value; nerve structures 1.5–3 Gy (Stroom et al. Radiother Oncol 2025;210:111030).'), key=True),
   card('Tissue recovery: what can be assumed', tbl(['Source','Statement'],[
     ('ESTRO–EORTC 2022 (S20)','Recovery or dose discount cannot be reliably recommended except for the CNS and spinal cord.'),
     ('ESTRO/EANO glioblastoma 2025','Recovery is consistently described only for brain tissue and cord; no consensus for brainstem and optic structures.'),
     ('ESTRO thoracic 2026','An area of uncertainty; apply cautiously; no numbers given.'),
     ('International practice survey (Stroom 2025)','Where a recovery factor was used, median 25% (IQR 20–35%), applied from a median of 6 months (IQR 6–12).'),
     ('Recurrent NPC (Ng 2021)','Cumulative limits of 130% (desirable) and 150% (acceptable) of first-course tolerance, implying about 30% recovery; about 50% for cord at ≥1 year from primate data; none assumed for optic structures by some authors.'),
     ('UK SABR Consortium pelvic guidance 2025','30% recovery applied to the first-course organ dose at 6–18 months, 50% beyond 18 months; less in patients likely to recover poorly.'),
     ('Head and neck consensus (Biau 2026)','Recovery factors of 10–25% for cord or brainstem must be used with caution and documented.'),
     ('Cord (quoted in Doi 2021)','Simple method: 25% recovery after 6 months, 50% after 12 months.'),
     ('Thoracic practice (Rulach 2021 Table 4)','Paradis limits assume a 6–12 month interval; Troost limits a 9-month interval.'),
     ('Pelvic SABR review (Murray 2017)','Dosimetric room for 25–30 Gy in 5 fractions after about 54 Gy conventional if 50% repair is allowed.')]) +
     note('No recovery should be assumed for any organ that showed grade ≥3 toxicity from the first course.' + ' ' + V)),
   card('Why SBRT changes the sums', ul(['A small high-dose volume with a steep gradient can keep serial-organ maximum dose low even inside a prior field.','But EQD2 at 6–10 Gy per fraction with α/β 2–3 Gy is large: 30 Gy in 5 fractions is an EQD2 of 54 Gy at α/β 3 and 60 Gy at α/β 2.','The linear–quadratic model is less certain above about 8–10 Gy per fraction. '+V]))]),
 panel('consent','Consent & follow-up','Consent and follow-up','What to say and how often to see them.',
  [card('Consent points', ul(['The aim (cure, durable local control, or symptom relief) and the realistic chance of it.','Side-effects are more likely and can be more severe than the first time, can appear sooner, and some are irreversible or fatal (bleeding, fistula, necrosis, myelopathy, depending on site).','The evidence is limited; dose limits are estimates.','Alternatives, including no radiotherapy.','Site-specific rates are on the site pages in this section.']), key=True),
   card('Follow-up', ul(['After high-dose reirradiation: every 3–4 months in the first year, then yearly, unless the risk of irreversible toxicity is low (S22).','Review by a radiation oncologist with imaging and examination (S21).','Record toxicity by CTCAE and feed it back to physics: local outcome data is how constraints improve.','Glioblastoma: MRI every 3 months, clinical toxicity check at 6 weeks (ESTRO/EANO). Lung: clinical review at 4–6 weeks, CT every 3–4 months for 2 years (ESTRO 2026).']))]),
 panel('sources','Sources','Key documents','Papers used for this section, which ones were read in full, and what is still wanted.',
  [card('Consensus statements and guidelines used', ul([
     a('https://doi.org/10.1016/S1470-2045(22)00447-8','Andratschke et al. ESTRO–EORTC consensus on re-irradiation: definition, reporting and decision making.')+' Lancet Oncol 2022;23:e469–78.',
     'Paradis et al. ReCOG consensus on dose evaluation and reporting with multiple courses of RT. Lancet Oncol 2026;27:e101–10.',
     a('https://doi.org/10.1016/j.radonc.2025.111030','Stroom et al. Reirradiation dose constraints in clinical practice: international survey.')+' Radiother Oncol 2025;210:111030.',
     a('https://doi.org/10.1016/j.radonc.2024.110696','Andratschke et al. ESTRO/EANO recommendation on reirradiation of glioblastoma.')+' Radiother Oncol 2025;204:110696.',
     a('https://doi.org/10.1016/j.radonc.2026.111707','Andratschke et al. ESTRO guideline on high-dose thoracic reirradiation for NSCLC.')+' Radiother Oncol 2026;222:111707.',
     a('https://pmc.ncbi.nlm.nih.gov/articles/PMC12874335/','Simone et al. American Radium Society appropriate use criteria: reirradiation for NSCLC (executive summary).')+' Int J Radiat Oncol Biol Phys.',
     'Rulach et al. International Delphi on radical thoracic reirradiation. Adv Radiat Oncol 2021;6:100653.',
     'Biau et al. Reirradiation for recurrent head and neck SCC: ReCOG/ESTRO/ASTRO consensus. Lancet Oncol 2026;27:e350–61.',
     'Ward et al. American Radium Society appropriate use criteria: head and neck retreatment. Int J Radiat Oncol Biol Phys 2022;113:759–86.',
     a('https://doi.org/10.1016/j.ijrobp.2021.01.041','Ng et al. International recommendations on reirradiation by IMRT for recurrent nasopharyngeal carcinoma.')+' Int J Radiat Oncol Biol Phys 2021;110:682–95.',
     'Alongi et al. ESTRO–ISRS recommendations for SBRT reirradiation of spinal metastases. Radiother Oncol 2026;214:111304.',
     'Peulen et al. ESTRO recommendations for reirradiation in locally recurrent rectal cancer (endorsed by ASTRO). Radiother Oncol 2026;223:111647.',
     'Royal College of Radiologists. Principles of reirradiation. 2024.',
     'Doi, Tamari, Oh, Nieder. New clinical data on human spinal cord re-irradiation tolerance. Strahlenther Onkol 2021;197:463–73.',
     'Sahgal et al. HyTEC: spinal cord dose tolerance to SBRT. Int J Radiat Oncol Biol Phys 2021.',
     'Slevin et al. International Delphi for pelvic SABR reirradiation. Radiother Oncol 2021;164:104–14.',
     a('https://doi.org/10.1016/j.tipsro.2025.100326','Moreno-Olmedo et al. UK SABR Consortium guidance: pelvic SABR reirradiation.')+' Tech Innov Patient Support Radiat Oncol 2025;35:100326.',
     'Jereczek-Fossa et al. ESTRO ACROP Delphi: salvage SBRT for intraprostatic relapse. Cancer Treat Rev 2021;98:102206.'])),
   card('Read in full from your Re-irradiation folder (14 Nov 2026)', ul([
     'Biau 2026 (head and neck consensus); Ward 2022 (ARS head and neck); Rulach 2021 (thoracic Delphi); Simone (ARS thoracic); ESTRO/ReCOG lung planning 2026.',
     'UK SABR Consortium pelvic guidance 2025 with supplement; Peulen 2026 (ESTRO rectal reirradiation); Jereczek-Fossa 2021 (ESTRO ACROP prostate).',
     'Alongi 2026 (ESTRO–ISRS spine); HyTEC spinal cord; Doi and Nieder 2021 (cord risk score).',
     'Paradis 2026 (ReCOG dose evaluation) and the ReCOG case-based guide; Stroom 2025 (constraint survey); RCR Principles of reirradiation 2024; ESTRO/EANO glioblastoma 2025.']), key=True),
   card('Still wanted', ul([
     '<b>Sahgal 2012</b> and <b>Nieder 2006</b> originals (currently via HyTEC and Doi 2021).',
     '<b>Slevin 2021</b> Delphi full text; <b>Abusaris 2011/2012</b>.',
     '<b>Paradis 2019</b> appendix E2 (Michigan limits and discount factors).',
     '<b>Departmental reirradiation policy</b> or physics consult template; local cumulative constraint sheet.',
     'Anything you rely on for <b>liver, bladder, oesophagus, paediatric or gynae external-beam reirradiation</b>.',
     'Not yet worked through in detail from the folder: Ward 2022 variant tables, Stroom 2025 per-organ table, Paradis 2026 and the ReCOG case guide worked examples, the ESTRO/ReCOG lung planning workflow, and the ESTRO ACROP prostate tables.'])),
]),
])

# =============================================================== 2. constraints + calculators
cns_rows = [
 ('<b>Spinal cord</b>, conventional reRT','Cumulative BED ≤135.5 Gy<sub>2</sub> (≈68 Gy EQD2), each course ≤98 Gy<sub>2</sub>, interval ≥6 months: risk of myelopathy appears small. No case reported at ≤120 Gy<sub>2</sub> (60 Gy EQD2) under the same conditions. α/β 2 Gy cervical and thoracic, 4 Gy lumbar.','Nieder 2006'),
 ('<b>Thecal sac</b>, SBRT reRT (1–5 fractions)','Cumulative EQD2<sub>2</sub> Dmax ≤70 Gy; SBRT EQD2<sub>2</sub> Dmax ≤25 Gy; SBRT share of cumulative ≤0.5; interval ≥5 months.','Sahgal 2012; HyTEC 2021; endorsed by ESTRO–ISRS 2026'),
 ('<b>Spinal cord</b>, thoracic reRT','Desirable cumulative Dmax 60 Gy EQD2 (α/β 2), maximum 67.5 Gy if the first course gave the cord ≤50 Gy (Delphi). ARS: composite Dmax &lt;57 Gy.','Rulach 2021; ARS thoracic'),
 ('<b>Spinal cord and brainstem</b>, head and neck reRT','Target cumulative EQD2 D0.1cc ≤50 Gy cord, ≤55 Gy brainstem; about 60 Gy at the surface case by case.','Biau 2026'),
 ('<b>Spinal cord</b>, NPC reRT','Cumulative ≤58.5 Gy desirable, 67.5 Gy acceptable (130% and 150% of 45 Gy).','Ng 2021'),
 ('<b>Spinal cord</b>, what centres use','Median cumulative near-maximum 67 Gy EQD2 against 50 Gy for a first course.','Stroom 2025 survey'),
 ('<b>Brain</b>','Necrosis seen beyond a cumulative EQD2 of about 100 Gy with conventional reRT; higher cumulative doses tolerated with FSRT (mean 110 Gy) and SRS (mean 130 Gy) to small volumes. ESTRO/EANO gives no numerical limit.','Sminia & Mayer 2012; ESTRO/EANO 2025'),
 ('<b>Brainstem</b>','Cumulative ≤70.2 Gy desirable, 81 Gy acceptable (reference 54 Gy). No consensus on recovery.','Ng 2021; ESTRO/EANO 2025'),
 ('<b>Optic chiasm and nerves</b>','Cumulative ≤70.2 Gy desirable, 81 Gy acceptable; assume little or no recovery. Unilateral nerve: no limit if the patient accepts the risk of blindness.','Ng 2021'),
 ('<b>Temporal lobe</b>','Cumulative ≤91 Gy desirable, 105 Gy acceptable (reference 70 Gy).','Ng 2021'),
]
hn_rows = [
 ('<b>Carotid artery</b>','Cumulative EQD2 above 120–125 Gy (α/β 2) significantly raises blowout risk: avoid when feasible; ≤125 Gy total suggested for NPC. SBRT: no blowout seen with carotid D0.1cc &lt;47.6 Gy from the SBRT course (5 fractions, alternate days).','Biau 2026; Ng 2021; Gebhardt 2018'),
 ('<b>Mandible</b>','Osteoradionecrosis risk rises significantly above a cumulative EQD2 of 114–119 Gy.','Biau 2026'),
 ('<b>Brachial plexus</b>','Desirable cumulative Dmax 80 Gy EQD2 (α/β 2); 95 Gy acceptable if the interval exceeds 2 years (Delphi). ARS: &lt;85 Gy.','Rulach 2021; ARS thoracic'),
]
tx_rows = [
 ('<b>Oesophagus</b>','V60 &lt;40%; Dmax &lt;100 Gy (the 2020 version allowed 100–110 Gy).','ARS thoracic'),
 ('<b>Lung</b>','Composite V20 &lt;40%.','ARS thoracic'),
 ('<b>Heart</b>','V40 &lt;50%; mean as low as achievable.','ARS thoracic'),
 ('<b>Aorta and great vessels</b>','Dmax &lt;120 Gy.','ARS thoracic'),
 ('<b>Trachea and proximal bronchial tree</b>','Dmax &lt;110 Gy.','ARS thoracic'),
]
pv_rows = [
 ('<b>UK SABR Consortium method</b>','Cumulative limit = de novo 5-fraction SABR constraint in EQD2 (e.g. small bowel D0.1cc 35 Gy/5 = 70 Gy, α/β 3), less the prior dose discounted 30% (6–18 months) or 50% (beyond 18 months).','UK SABR Consortium 2025'),
 ('<b>Rectal reRT, PTV region</b>','Cumulative EQD2 (α/β 3) below 90 Gy probably deliverable without formal organ calculations; not a universal threshold.','ESTRO rectal 2026'),
 ('<b>Bladder, rectum, bowel</b> (older proposal)','110 Gy bladder, 100 Gy rectum, 90 Gy bowel (α/β 3).','Abusaris 2011'),
 ('<b>Bladder</b>','D0.1cc 110 Gy cumulative EQD2 (α/β 3) used as the study limit; cumulative doses up to about 110 Gy observed without attributable severe toxicity.','Leeds isotoxic study 2025; Slevin 2025'),
 ('<b>Rectum</b>','D0.1cc 89.9 Gy cumulative EQD2 (α/β 3) used; up to 82.8–92.4 Gy observed.','Leeds isotoxic study 2025; Slevin 2025'),
 ('<b>Small bowel</b>','D0.1cc 78.8 Gy cumulative EQD2 (α/β 3) used; up to about 112 Gy observed on point summation.','Leeds isotoxic study 2025; Slevin 2025'),
 ('<b>Sacral plexus / cauda equina</b>','D0.1cc 67.2 Gy EQD2 (α/β 2) with 33% recovery applied to the first course; often the dose-limiting structure, with vessels.','Leeds isotoxic study 2025'),
 ('<b>After prostate RT, SBRT reRT</b>','Cumulative EQD2 (α/β 3) that appeared safe: bladder D30% &lt;57.9 Gy; rectum D30% &lt;66.0 Gy, D60% &lt;38.0 Gy, V122.1 Gy &lt;5%.','IEO series (Phys Med 2021)'),
]
calc1 = '''<div class="calc" data-rr="rem">
<label>Prior dose to the organ (Gy)<input type="number" data-k="D1" value="50" min="0" step="0.1"></label>
<label>Prior fractions<input type="number" data-k="n1" value="25" min="1" step="1"></label>
<label>α/β (Gy)<input type="number" data-k="ab" value="3" min="0.5" step="0.5"></label>
<label>Recovery assumed (%)<input type="number" data-k="rec" value="0" min="0" max="75" step="5"></label>
<label>Cumulative limit (Gy EQD2)<input type="number" data-k="lim" value="100" min="0" step="0.1"></label>
<label>Planned fractions<input type="number" data-k="n2" value="5" min="1" step="1"></label>
</div><div class="calcout" data-rro="rem"></div>'''
calc2 = '''<div class="calc" data-rr="cord">
<label>Course 1 cord dose (Gy)<input type="number" data-k="D1" value="30" min="0" step="0.1"></label>
<label>Course 1 fractions<input type="number" data-k="n1" value="10" min="1" step="1"></label>
<label>Course 2 cord dose (Gy)<input type="number" data-k="D2" value="12" min="0" step="0.1"></label>
<label>Course 2 fractions<input type="number" data-k="n2" value="2" min="1" step="1"></label>
<label>Interval (months)<input type="number" data-k="iv" value="12" min="0" step="1"></label>
<label>Cord level<select data-k="ab"><option value="2">Cervical or thoracic (α/β 2)</option><option value="4">Lumbar (α/β 4, Nieder)</option></select></label>
</div><div class="calcout" data-rro="cord"></div>'''
write('rert-constraints.html', [
 panel('limits','Cumulative limits','Published cumulative dose limits','By organ, in EQD2 unless stated, each with its source. These come from different patient groups and methods: read the source before applying one outside its setting.',
  [card('How to use this table', ul(['Limits are for the <b>sum</b> of all courses unless the row says otherwise.','Most are consensus or single-series values, not validated tolerance doses.','Recovery: see <a href="rert-principles.html#radiobiology">radiobiology</a>. Only the cord, the brain and the NPC limits build recovery in.','A limit met on paper still needs clinical judgement about the first-course toxicity, the interval and what the patient will accept.']) + CAVEAT, key=True),
   card('CNS and spine', tbl(['Organ','Limit','Source'], cns_rows)),
   card('Head and neck', tbl(['Organ','Limit','Source'], hn_rows)),
   card('Thorax: four published sets compared (cumulative EQD2)', tbl(['Organ','α/β','Rulach 2021 Delphi','Paradis 2019','Troost 2020 (9-month interval)','ARS'],[('Spinal cord','2','Dmax 60 Gy','D0.1cc &lt;56.25 Gy','Dmax &lt;65 Gy','Dmax &lt;57 Gy'),('Oesophagus','3','Dmax 75–100 Gy','D0.1cc &lt;90.6 Gy','Dmax &lt;100 Gy','V60 &lt;40%, Dmax &lt;100 Gy'),('Brachial plexus','2','Dmax 80–95 Gy','D0.1cc &lt;85 Gy','Dmax &lt;85 Gy','Dmax &lt;85 Gy'),('Great vessels','3','Dmax 110–115 Gy','D0.1cc &lt;123 Gy','Dmax &lt;110 Gy','Dmax &lt;120 Gy'),('Proximal bronchial tree','3','Dmax 80–105 Gy','D0.1cc &lt;90.6 Gy','Dmax &lt;110 Gy','Dmax &lt;110 Gy'),('Skin / chest wall','2.5','ALARA','D0.1cc &lt;105 Gy','—','—'),('Heart','2.5','ALARA','D0.1cc &lt;85 Gy','Dmean &lt;70 Gy','V40 &lt;50%'),('Lung','3','Individualised (no consensus)','Individualised','Dmean &lt;22 Gy','V20 &lt;40%')]) + note('From Rulach 2021, Table 4. Paradis values assume a 6–12 month interval with the organ treated to tolerance the first time. Delphi detail: aorta desirable 115 Gy, pulmonary artery 110 Gy; no consensus for lung. ARS oesophagus Dmax: composite doses above 100 Gy should be discouraged (Simone). The ESTRO 2026 guideline gives no table of its own.')),
   card('Pelvis', tbl(['Organ','Limit or observed dose','Source'], pv_rows) + note('The 2021 international Delphi could not agree on cumulative pelvic constraints or a minimum interval.')),
   card('Sources for this page', ul(['Nieder C et al. Update of human spinal cord reirradiation tolerance. Int J Radiat Oncol Biol Phys 2006.','Sahgal A et al. Reirradiation human spinal cord tolerance for SBRT. Int J Radiat Oncol Biol Phys 2012;82:107–16.','Sahgal A et al. HyTEC spinal cord. Int J Radiat Oncol Biol Phys 2021.',a('https://pmc.ncbi.nlm.nih.gov/articles/PMC3712703/','Sminia P, Mayer R. Radiation tolerance of the human brain. Cancers 2012;4:379–99.'),'Ng WT et al. 2021 (NPC); Biau J et al. 2026 (head and neck); Simone CB et al. ARS thoracic; Gebhardt BJ et al. 2018 (carotid, SBRT).',a('https://pmc.ncbi.nlm.nih.gov/articles/PMC12775924','Isotoxic stereotactic reirradiation for recurrent pelvic cancers. Phys Imaging Radiat Oncol 2025.'),'Slevin F et al. Dose accumulation for pelvic SABR reirradiation. Clin Oncol 2025;43:103861.','Finding safe dose-volume constraints for re-irradiation with SBRT of prostate cancer relapse: the IEO experience. Phys Med 2021.']))], first=True),
 panel('calc','Calculators','Reirradiation calculators','Arithmetic only. They do not replace a physics cumulative dose assessment. The remaining-dose calculator follows the UK SABR Consortium worked method.',
  [card('Remaining dose to an organ', note('Converts the prior organ dose to EQD2, applies any recovery, subtracts it from the cumulative limit you choose, and gives the largest physical dose the organ can receive in the planned number of fractions.') + calc1 + note('EQD2 = D × (d + α/β) / (2 + α/β). The remaining dose is solved from the same formula for the planned fractions. Enter the dose the organ received, not the prescription, when you know it.'), key=True),
   card('Spinal cord reirradiation check', note('Checks two published rule sets: Nieder 2006 for conventional reirradiation and Sahgal 2012 / HyTEC for SBRT reirradiation (thecal sac maximum).') + calc2 + note('Nieder: cumulative BED ≤135.5 Gy<sub>2</sub> with each course ≤98 Gy<sub>2</sub> and interval ≥6 months (no myelopathy reported at ≤120 Gy<sub>2</sub>). Sahgal: cumulative EQD2<sub>2</sub> ≤70 Gy, SBRT course ≤25 Gy, SBRT share ≤0.5, interval ≥5 months; the Sahgal checks always use α/β 2. Nieder risk score from Doi 2021, Table 1: low 0–3, intermediate 4–6, high more than 6 points.'))]),
], js=True)

# =============================================================== 3. CNS, spine, bone
write('rert-cns.html', [
 panel('glioma','Glioma','Glioblastoma and high-grade glioma','ESTRO/EANO 2025 recommendations and RTOG 1205.',
  [card('Selection', ul(['MDT decision weighing risks, benefits and alternatives (Rec 1).','Consider with <b>KPS ≥60</b> and <b>&gt;6 months</b> from the first course, regardless of age or MGMT status (Rec 2).','After gross total resection, only with favourable prognostic factors (Rec 3).','Lesions generally ≤5–6 cm; larger, multifocal or leptomeningeal disease is excluded. Prospective data exist only up to 6 cm (Statement 4).','Expect longer progression-free survival, not proven overall survival benefit (Statement 1).']) + CAVEAT, key=True),
   card('Imaging and volumes', ul(['Contrast-enhanced T1 MRI is required; advanced MRI or amino-acid PET to separate recurrence from pseudoprogression or necrosis (Rec 4).','GTV: enhancing T1 lesion, new or progressive T2/FLAIR change and amino-acid PET-avid regions (Rec 6).','GTV-to-CTV margin is not mandatory; 3–5 mm optional. CTV-to-PTV at most 3 mm (Rec 7).','Rigid registration for delineation and dose accumulation (Rec 5).'])),
   card('Dose', tbl(['Schedule','Notes'],[('<b>35 Gy in 10 fractions</b>','Panel preference; the RTOG 1205 schedule.'),('<b>27–30 Gy in 3–5 fractions</b>','Panel preference for moderate to large lesions.'),('<b>36 Gy in 18 fractions</b>','Alternative for larger targets.'),('<b>Single-fraction SRS</b>','Smaller lesions, e.g. GTV up to 3 cm (Rec 9).')], wide=False) + ul(['EQD2 should be no less than 36 Gy (Rec 8).','Cumulative assessment in EQD2 with α/β 3 Gy (Rec 11); minimum OARs: brain, brainstem, chiasm, optic nerves and tracts, nearby cranial nerves (Statement 5).','No numerical cumulative limits are given. Literature: necrosis beyond about 100 Gy cumulative EQD2 with conventional reRT (Sminia &amp; Mayer 2012).','Cascading prescription: compromise PTV next to OARs before changing the dose (Rec 12).'])),
   card('Systemic therapy and evidence', ul(['<b>RTOG 1205</b> (Tsien 2023, n=170, progression ≥6 months after chemo-RT): bevacizumab ± 35 Gy/10. Median OS 10.1 v 9.7 months (HR 0.98); median PFS 7.1 v 3.8 months; 6-month PFS 54% v 29%; acute grade ≥3 treatment-related events 5%, no delayed high-grade events.','No routine concurrent or maintenance systemic therapy can be recommended (Statements 8–9); target and dose do not change if it is given (Rec 14).','Follow-up: MRI every 3 months, toxicity check at 6 weeks; do not call progression on the 6-week scan (Rec 16).']) + note('Sources: Andratschke 2025 (ESTRO/EANO); Tsien et al. J Clin Oncol 2023;41:1285–95.'))], first=True),
 panel('brainmets','Brain metastases','Brain metastases: a second course','Repeat SRS, SRS after WBRT, and repeat WBRT.',
  [card('Repeat SRS to the same lesion', ul(['Meta-analysis (Singh; 347 patients, 462 lesions): 1-year local control 69%, radionecrosis 16%.','Multicentre NSCLC series (Kowalchuk 2021): second SRS median 18 Gy margin dose; 1-year local control 79%; radionecrosis 20%, symptomatic 7%. Risk rose with maximum dose ≥40 Gy at either course and second-course V12Gy &gt;9 cm³.','Local control was better for tumours ≤1 cm³.','First confirm it is tumour, not necrosis: perfusion MRI, amino-acid PET or resection.','Consider fractionated SRS, resection plus cavity treatment, or LITT for larger lesions. '+V]), key=True),
   card('SRS after WBRT', ul(['Prospective phase 2 (Maranzano 2019): KPS ≥70, lesions ≤20 mm, dose ≤20 Gy (median 18 Gy), median 15 months after WBRT: 2-year control 81%, no radionecrosis, median OS 14 months.','An earlier series from the same group with wider selection had 6% radionecrosis.'])),
   card('Repeat WBRT', ul(['Reserve for multiple recurrences when SRS is not feasible, good performance status and a long interval. Commonly 20–25 Gy in 10 fractions. '+V,'Expect modest benefit and cognitive cost; discuss best supportive care.']))]),
 panel('spine','Spine & cord','Spine metastases and the spinal cord','ESTRO–ISRS 2026 recommendations, Sahgal and Nieder limits and the Nieder risk score.',
  [card('SBRT reirradiation: ESTRO–ISRS 2026', ul([
     'Recommended for carefully selected patients with longer life expectancy when a durable pain response and local control are wanted.',
     '<b>Interval:</b> recommended only if more than <b>12 months</b> from the first course; can be considered in carefully selected patients at 6–12 months (strong consensus).',
     '<b>Dose:</b> 24 Gy/2, 30 Gy/4, 30 Gy/5 or 16 Gy/1.',
     'Baseline SINS strongly recommended; SBRT only for stable or potentially unstable spines (SINS 0–12). Prior surgery is not an exclusion.',
     'MRI for target and cord delineation; CT myelography if MRI is not possible.',
     'Cord: use the HyTEC 2021 constraints.',
     'Meta-analysis behind the recommendations (20 studies, 1538 metastases; median 24 Gy/2 after 30 Gy/10): pooled local control 81% at 1 year and 70% at 2 years; overall pain response 77%, complete 34%; vertebral compression fracture 5.0%, nerve root damage 5.6%, myelopathy 1.7%.']) + note('Source: Alongi F et al. Radiother Oncol 2026;214:111304 (full text).'), key=True),
   card('Cord limits', tbl(['Setting','Rule','Source'],[
     ('Conventional reRT','Cumulative BED ≤135.5 Gy<sub>2</sub>, each course ≤98 Gy<sub>2</sub>, interval ≥6 months. Use the risk score below.','Nieder 2006'),
     ('SBRT after conventional RT','Thecal sac cumulative EQD2<sub>2</sub> Dmax ≤70 Gy; SBRT component ≤25 Gy; ratio ≤0.5; ≥5 months.','Sahgal 2012; HyTEC'),
     ('De novo SBRT, for reference','Cord Dmax for 1–5% myelopathy risk: 12.4–14.0 Gy/1, 17.0 Gy/2, 20.3 Gy/3, 23.0 Gy/4, 25.3 Gy/5.','HyTEC 2021')]) + note('<a href="rert-constraints.html#calc">Cord reirradiation check and risk score calculator</a> · departmental spine SBRT limits are in the <a href="contouring/spine-bone.html">spine and bone guide</a>.')),
   card('Nieder myelopathy risk score', tbl(['Risk factor','Points'],[('Interval under 6 months','4.5'),('Either course EQD2 ≥51 Gy','4.5'),('Cumulative EQD2 60.1–65 Gy','1'),('65.1–70 Gy','2'),('70.1–75 Gy','3'),('75.1–80 Gy','4'),('80.1–85 Gy','5'),('85.1–90 Gy','6 (one more point per 5 Gy above this)')], wide=False) +
     ul(['<b>Low risk</b> 0–3 points: myelopathy under 5%. <b>Intermediate</b> 4–6 points: about 25% in the original data. <b>High</b> more than 6 points: about 90%.','EQD2 with α/β 2 Gy, cord maximum dose.','Update (Doi 2021, 32 patients, median cumulative Dmax 80.7 Gy EQD2): no myelopathy at a median 12 months, including intermediate- and high-risk patients, so the score may overestimate risk with modern planning; follow-up was short.','Simple alternative quoted in the same paper: assume 25% recovery after 6 months and 50% after 12 months.']) + note('Source: Doi H, Tamari K, Oh RJ, Nieder C. Strahlenther Onkol 2021;197:463–73 (Table 1); Nieder 2005 and 2006.')),
   card('Second SBRT after SBRT failure', ul(['Thibault 2015 (40 patients, 56 segments): most often <b>30 Gy in 4 fractions</b> (range 20–35 Gy in 2–5) after a first course of median 24 Gy/2; 1-year local control 81%; median OS 10 months.','ESTRO–ISRS: repeat SBRT to the same level did not carry more adverse events than SBRT after conventional RT.'])),
   card('Cord compression, second course', ul(['Conventional reirradiation (8 Gy/1 to 20 Gy/5) improved motor function in about 40% in one series (Rades 2005).','Keep cumulative cord dose within the Nieder conditions where survival is expected beyond a few months; consider surgery or SBRT for radioresistant histology.']))]),
 panel('bone','Bone','Painful bone metastases','NCIC CTG SC.20.',
  [card('Retreatment for pain', ul(['<b>SC.20</b> (Chow 2014; n=850; TROG participated '+AU+'): 8 Gy/1 v 20 Gy in multiple fractions (5 fractions, or 8 if prior multi-fraction RT to spine or whole pelvis).','Pain response at 2 months, intention to treat: 28% v 32% (non-inferior). Per protocol: 45% v 51% (non-inferiority not met).','Less acute toxicity with 8 Gy: lack of appetite 56% v 66%, diarrhoea 23% v 31%.','Practical: 8 Gy single fraction is reasonable; expect about half of assessable patients to respond. Wait at least 4 weeks after the first course before judging failure. '+V,'Spine: account for cord dose as above. Consider SBRT when durable control matters.']) + note('Source: Chow E et al. Lancet Oncol 2014;15:164–71. eviQ protocol 268 summarises the same trial.'), key=True)]),
])

# =============================================================== 4. head and neck
write('rert-hn.html', [
 panel('hnscc','Head and neck SCC','Recurrent or second primary head and neck SCC','ReCOG/ESTRO/ASTRO consensus (Biau 2026), MIRI collaborative data and ARS 2022.',
  [card('Selection (Biau 2026, panel 1; MIRI RPA)', tbl(['RPA class','Definition','2-year OS'],[
     ('<b>I</b>','More than 2 years from the first course <b>and</b> resected','61.9%'),
     ('<b>II</b>','More than 2 years and unresected, <b>or</b> ≤2 years without organ dysfunction','40.0%'),
     ('<b>III</b>','≤2 years with organ dysfunction (feeding tube or tracheostomy dependence)','16.8%')], wide=False) +
     ul(['Review the previous plan to separate in-field recurrence from marginal failure (100% consensus).',
         '<b>Within 6 months</b> of the first course: generally not advised, except urgent palliation such as uncontrolled bleeding.',
         '<b>6–12 months:</b> only highly selected cases: small, localised, outside the high-dose region, after MDT review.',
         '<b>Post-operative reirradiation:</b> consider for RPA class I with positive margins or extracapsular extension; also where an R0 resection was unlikely even if pathology does not report a positive margin.',
         '<b>RPA class III</b> should generally not be offered curative-intent reirradiation.',
         'MIRI cohort (412 patients, IMRT, median 60 Gy): acute grade ≥3 toxicity 19%, grade 5 1.2%; 2-year grade ≥3 late toxicity 14.2%.']) + CAVEAT, key=True),
   card('Technique (Biau 2026, panel 2)', ul([
     'Post-operative: normofractionated IMRT, not SBRT.',
     'Unresected, RPA class II, <b>≤25 cc</b> (about 3 cm, cT1–2): IMRT or SBRT give similar outcomes.',
     'Unresected, RPA class II, <b>&gt;25 cc</b>: IMRT gives better outcomes than SBRT.',
     'SBRT for unresected <b>laryngeal or hypopharyngeal</b> recurrence: caution, higher risk of severe toxicity.',
     'Concurrent chemotherapy: case by case, mainly large tumours in fit patients.',
     'Protons can be considered to spare critical organs; comparative data are few.',
     'Brachytherapy remains valid for small (&lt;25 cc), well-delineated tumours.'])),
   card('Volumes and dose (Biau 2026, panel 3)', tbl(['Setting','Recommendation'],[
     ('Definitive, CTV','GTV + 5 mm'),('Elective nodes','Not recommended: no survival gain, more toxicity'),
     ('Definitive IMRT','66 Gy commonly used (60–66 Gy in 1.8–2 Gy fractions)'),
     ('Post-operative','60 Gy commonly used; high-risk CTV as for primary treatment'),
     ('SBRT','About 40 Gy in 5 fractions (40–50 Gy range in the literature), alternate days'),
     ('Hyperfractionation','An option; no clear benefit shown in HNSCC')], wide=False) +
     note('MIRI dose analysis (Caudell 2018): ≥66 Gy for definitive IMRT in fit patients; 50–66 Gy adequate after resection of gross disease.')),
   card('SBRT data (Pittsburgh)', ul(['Phase 2 (Vargo 2015, n=50, prior ≥60 Gy): 40–44 Gy in 5 fractions on alternate days with cetuximab: median OS 10 months, 1-year OS 40%.','Carotid (Gebhardt 2018, 75 patients): bleeding events 5.3%, carotid blowout 2.7%; no blowout with carotid D0.1cc &lt;47.6 Gy from the SBRT course. Modelled bleeding risk 0.8% at D0.1cc 20 Gy and 5% at 50 Gy (Ling 2019).'])),
   card('Dose accumulation and constraints (Biau 2026, panels 4–5)', ul([
     'Retrieve the previous CT, contours and dose; use deformable registration with rigorous QA where available; express cumulative OAR dose in EQD2 (α/β 2–3 Gy); voxel-wise 3D EQD2 summation where possible. Conservative manual point-dose addition for cord, brainstem and carotids remains acceptable.',
     '<b>Carotid:</b> cumulative EQD2 above 120–125 Gy (α/β 2) significantly raises blowout risk: avoid when feasible. Encasement beyond 180° and previous ulceration add risk; so does daily (not alternate-day) SBRT.',
     'Carotid blowout in a 1554-patient reirradiation cohort with carotid involvement: 2.6%, with 76% mortality.',
     '<b>Mandible:</b> osteoradionecrosis risk rises significantly above a cumulative EQD2 of 114–119 Gy; also depends on high-dose subvolume, dose per fraction, dental status and trauma. Reported rates 2–18%.',
     '<b>Spinal cord:</b> target cumulative EQD2 D0.1cc ≤50 Gy. <b>Brainstem:</b> ≤55 Gy. Case by case, about 60 Gy at the surface may be accepted depending on interval, prior dose distribution and reliability of dose accumulation.',
     'Recovery factors of 10–25% for cord or brainstem: use with caution and document explicitly.',
     'Consent specifically for carotid blowout, osteoradionecrosis, fistula, feeding-tube and tracheostomy dependence, and treatment-related death.']) +
     note('Sources: Biau J et al. Lancet Oncol 2026;27:e350–61 (full text, panels 1–5); Ward MC et al. IJROBP 2018;100:586–94; Caudell JJ et al. IJROBP 2018; Ward MC et al. ARS AUC, IJROBP 2022;113:759–86; Vargo JA et al. IJROBP 2015; Gebhardt BJ et al. IJROBP 2018;101(1).'))], first=True),
 panel('npc','Nasopharynx','Locally recurrent nasopharyngeal carcinoma','International recommendations (Ng 2021), the hyperfractionation trial (You 2023) and post-operative guidance (Li 2024).',
  [card('Selection', ul(['Exclude nodal and distant disease (FDG-PET/CT); MDT review.','<b>Surgery first</b> for resectable recurrence where expertise exists. Post-operative reRT for a positive margin; consider for close margins.','Radical reRT not recommended at ≤6 months from the first course; some prefer 12 months.','Exclude if prior toxicity was grade ≥1 at brainstem, cord or chiasm, or grade ≥3 at temporal lobe, optic nerve, brachial plexus, soft tissue or bone.','Bulk alone is not an exclusion.']) + CAVEAT, key=True),
   card('Volumes and dose', ul(['rGTV on co-registered MRI ± PET. CTV = rGTV + up to 5 mm, edited at barriers and critical OARs (0 mm acceptable next to them). PTV = CTV + 2–3 mm. No elective nodal irradiation.','<b>60–66 Gy EQD2</b>; doses ≥68 Gy were associated with excess fatal toxicity.','Preferred: hyperfractionation 1.1–1.2 Gy twice daily, ≥6 hours apart (lower-agreement item in 2021, since supported by a phase 3 trial).','Priorities: (1) brainstem, cord, chiasm, both optic nerves, rGTV; (2) PTV, temporal lobe, one optic nerve; (3) carotid.','Chemotherapy recommended for rT3–4N0 and any node-positive recurrence; induction then concurrent cisplatin preferred.'])),
   card('Hyperfractionation trial (You 2023, Lancet)', tbl(['','65 Gy in 54 fractions twice daily','60 Gy in 27 fractions daily'],[('Grade ≥3 late toxicity','34%','57%'),('Grade 5 late toxicity','7% (all nasal haemorrhage)','24% (haemorrhage 16%, temporal lobe necrosis 4%, nasopharyngeal necrosis 3%)'),('3-year overall survival','74.6%','55.0% (HR 0.54)')], wide=False) + note('144 patients, locally advanced recurrence, IMRT in both arms; no grade ≥3 radiation complication allowed before entry. Median follow-up 45 months.')),
   card('Cumulative limits (Ng 2021) and toxicity', tbl(['Structure','Desirable','Acceptable'],[('Brainstem','≤70.2 Gy','81 Gy'),('Spinal cord','≤58.5 Gy','67.5 Gy'),('Optic chiasm, optic nerves','≤70.2 Gy','81 Gy'),('Temporal lobe','≤91 Gy','105 Gy'),('Carotid','≤125 Gy total','no agreed limit')], wide=False) + ul(['Rule: 130% (desirable) and 150% (acceptable) of first-course tolerance in EQD2; keep as low as achievable.','Worked example from the paper: brainstem already at 50 Gy EQD2 leaves about 20 Gy desirable and 31 Gy acceptable.','Reported harms: carotid blowout 31% at 68 Gy and 19% at 60 Gy in an older randomised trial; temporal lobe necrosis 13–31%; mucosal necrosis and massive haemorrhage about 16% in a carbon-ion series.','Post-operative reRT (Li 2024): around 60 Gy; hyperfractionation may reduce toxicity.']) + note('Sources: Ng WT et al. IJROBP 2021;110:682–95; You R et al. Lancet 2023;401:917–27; Li JS et al. IJROBP 2024;120:1294–306.'))]),
])

# =============================================================== 5. thorax and breast
write('rert-thorax-breast.html', [
 panel('lung','Lung','High-dose thoracic reirradiation for NSCLC','ESTRO 2026 guideline, ARS appropriate use criteria and the 2021 Delphi.',
  [card('Selection and work-up (ESTRO 2026)', ul(['Curative intent: ECOG 0–1, life expectancy ≥6 months, <b>≥6 months</b> since the prior thoracic course.','Widespread metastases exclude curative reRT; limited metastases by oligometastatic principles.','Interstitial lung disease: highly selected cases only. Prior or persistent grade ≥3 toxicity: weigh critically.','Larger and ultracentral tumours carry more toxicity.','Work-up: FDG-PET/CT, contrast CT chest, MRI brain; pathological confirmation when feasible; lung function tests. No absolute lung function cut-off (Rulach 2021).','Palliative reirradiation is generally safe for symptom control.']) + CAVEAT, key=True),
   card('Dose and technique (ESTRO 2026)', tbl(['Situation','Recommendation'],[('Peripheral lesion ≤5 cm','SBRT with BED<sub>10</sub> ≥100 Gy, for type 1 or type 2 reRT'),('Central lesion','Individualise by prior dose, interval, prior tolerance and cumulative limits'),('Not suitable for SBRT','60 Gy/30 or 55 Gy/20 if cumulative constraints are met'),('Alternatives','66 Gy/33, 60 Gy/15, twice-daily or CHART-type schedules; 60 Gy/15 needs particular care')], wide=False) + ul(['Aim for at least 50 Gy EQD2 to the target; reduce PTV coverage if an OAR limit would be exceeded.','PTV margin ≤5 mm; no isotropic GTV-to-CTV margin; no elective nodal irradiation.','VMAT or IMRT/SBRT with type B or C algorithms; daily online volumetric imaging.','Cumulative assessment in EQD2; rigid then deformable registration; visual check of the fusion is mandatory.'])),
   card('Cumulative limits (ARS, EQD2)', tbl(['Organ','Composite limit'],[('Oesophagus','V60 &lt;40%; Dmax &lt;100 Gy'),('Lung','V20 &lt;40%'),('Heart','V40 &lt;50%'),('Aorta and great vessels','Dmax &lt;120 Gy'),('Trachea and proximal bronchial tree','Dmax &lt;110 Gy'),('Spinal cord','Dmax &lt;57 Gy'),('Brachial plexus','Dmax &lt;85 Gy')], wide=False) + note('Derived largely from conventionally fractionated reirradiation series. Dose-limiting toxicities: acute oesophagitis and pneumonitis; late pulmonary, cardiac, oesophageal and brachial plexus injury; fatal haemorrhage and airway necrosis from vessel and bronchial maximum doses.')),
   card('Systemic therapy, toxicity and follow-up', ul(['Concurrent chemotherapy may improve control but increases severe toxicity, especially oesophagitis; best kept for locoregional nodal recurrence.','Immunotherapy: sequential, preferably in a trial. Osimertinib with thoracic RT carries a higher pneumonitis risk (see <a href="sys-timing.html">targeted therapy and RT</a>).','Quoted risk from the literature: grade 3 pneumonitis 5–23%; grade 5 toxicity up to 20% depending on technique and location (Rulach 2021).','Delphi limits (Rulach 2021): cord 60 Gy desirable, 67.5 Gy maximum if the first course gave ≤50 Gy; brachial plexus 80 Gy, 95 Gy if more than 2 years apart; aorta 115 Gy; pulmonary artery 110 Gy; heart and skin as low as achievable. Four sets are compared on the <a href="rert-constraints.html">limits page</a>.','Follow-up: review at 4–6 weeks; CT chest every 3–4 months for 2 years, then 6-monthly to 5 years.']) + note('Sources: Andratschke N et al. Radiother Oncol 2026;222:111707; Simone CB et al. ARS AUC executive summary; Rulach R et al. Adv Radiat Oncol 2021;6:100653.'))], first=True),
 panel('breast','Breast','Breast and chest wall','Second breast conservation with partial-breast reirradiation, and chest wall recurrence.',
  [card('Second breast conservation: NRG/RTOG 1014', ul(['Eligibility: in-breast recurrence <b>&gt;1 year</b> after whole-breast RT, <b>&lt;3 cm</b>, unifocal on MRI, no skin involvement, excised with negative margins, clinically node negative.','<b>45 Gy in 30 fractions of 1.5 Gy twice daily</b> over 15 days, 3D-conformal partial breast; CTV = cavity + 1.5 cm; start within 9 weeks of surgery.','58 patients, median follow-up 5.5 years: 5-year in-breast recurrence <b>5%</b>; mastectomy 10%.','Late treatment-related grade 3 events 7% (fibrosis, breast atrophy and pain, infection); grade 2 in 26%.']) + CAVEAT, key=True),
   card('Brachytherapy and European data', ul(['GEC-ESTRO multicentre analysis of lumpectomy plus accelerated partial-breast reirradiation (Hannoun-Levi 2023): 5-year second local relapse 4%; distant metastasis 7%. The TAM score (time interval, APBI risk group, molecular subtype) was prognostic.','Matched comparison with salvage mastectomy: no difference in survival or third breast events (Hannoun-Levi 2021).','Third in-breast event about 10% after second conservation with reirradiation, similar to mastectomy, against about 20% after lumpectomy alone (Montagne 2020 review).','Multicatheter interstitial HDR is the largest experience; doses such as 32 Gy in 8 or 34 Gy in 10 fractions twice daily are used. '+V])),
   card('Chest wall and regional recurrence', ul(['Combine surgery, reirradiation and systemic therapy where possible; reirradiation should be strongly considered for high risk of second recurrence or unresectable disease (DEGRO, Harms 2016).','Partial chest wall or scar reRT of 45 Gy in 1.8 Gy fractions gave high local control with low skin toxicity in a German series.','Hyperthermia with reirradiation is used in specialist centres for unresectable chest wall disease (large Dutch and German series). Not widely available in Australia. '+V,'Limits to respect: skin and ribs, brachial plexus (see <a href="rert-constraints.html">limits</a>), heart and lung for left-sided fields.']) + note('Sources: Arthur DW et al. JAMA Oncol 2020;6:75–82; Arthur DW et al. IJROBP 2017 (toxicity); Hannoun-Levi JM et al. IJROBP 2023 and 2021; Montagne L et al. 2020; Harms W et al. Strahlenther Onkol 2016.'))]),
])

# =============================================================== 6. pelvis
write('rert-pelvis.html', [
 panel('rectum','Rectum','Locally recurrent rectal cancer','ESTRO 2026 recommendations (endorsed by ASTRO) and supporting series.',
  [card('ESTRO 2026: who and why', ul([
     'Discuss every patient in a specialist MDT with experience in rectal reirradiation; planning and delivery by a team with reirradiation radiobiology expertise.',
     'Discuss benefits, risks and uncertainties with the patient, including the aims of each option and effect on quality of life.',
     '<b>Resectable or borderline:</b> consider neoadjuvant (chemo)reirradiation to improve the R0 resection rate.',
     '<b>Not resectable or not operable:</b> consider definitive (chemo)reirradiation for prolonged local control.',
     '<b>Symptoms with poor performance status (WHO ≥2) or prognosis under 6 months:</b> standard palliative regimens.']) + CAVEAT, key=True),
   card('Dose and fractionation (ESTRO 2026)', tbl(['Setting','Schedule'],[
     ('Neoadjuvant or definitive','<b>40.8 Gy in 1.2 Gy fractions twice daily</b>'),
     ('Neoadjuvant or definitive','30–39 Gy in 1.5 Gy fractions twice daily ± IORT'),
     ('Neoadjuvant or definitive','30 Gy in 1.8–2 Gy fractions daily ± IORT'),
     ('Palliative','8 Gy × 1 or 4 Gy × 5'),
     ('SBRT','Consider for 1–3 small, discrete lesions without invasion of GI tract or bladder, as an alternative to surgery, in experienced centres (conditional)')], wide=False) +
     ul(['Concurrent oral or intravenous fluoropyrimidine with neoadjuvant or definitive reirradiation if the patient is fit for it.','IMRT/VMAT for all neoadjuvant or definitive courses; daily volumetric imaging for SBRT and where a specific organ is of concern.','Neoadjuvant planning: prioritise PTV coverage where an R1 resection is likely; organs that will be resected can be deprioritised.','Protons or carbon ions, and regional hyperthermia: conditional, in centres with experience.'])),
   card('Cumulative dose', ul(['No evidence-based organ constraints exist for rectal reirradiation.','Panel view: a <b>cumulative EQD2 (α/β 3) below 90 Gy</b> to the PTV can probably be delivered without formal organ constraint calculations with acceptable severe toxicity; typical courses of 30–40 Gy give a cumulative 80–90 Gy. Not a universal safe threshold: read with organ-specific dose–volume data, overlap volume and intent.','Doses above 50 Gy improved local control in two studies at the cost of more severe late toxicity.'])),
   card('Outcomes quoted', ul(['Guren 2014 review (375 patients): median survival 39–60 months when resected, 12–16 months when palliative; symptom relief in 82–100%.','Pooled symptomatic response 75% in 413 patients (Lee review); non-operative 1-, 2- and 3-year OS 63.5%, 34.2% and 23.8%.','Non-operated series (Tao): late grade 3–4 toxicity 16%; symptoms improved in 70% for a median 10 months.','SBRT, UK multicentre (Johnson; 68 patients, 81 lesions, 30 Gy/5): 2-year OS 77%, median OS 38.7 months.','DESTROY-1 phase 1 (pelvic SBRT reRT, 5 fractions): up to 45 Gy after &gt;60 Gy prior or prior small-bowel irradiation, 50 Gy after &lt;60 Gy.']) + note('Sources: Peulen HMU et al. ESTRO recommendations for reirradiation in locally recurrent rectal cancer. Radiother Oncol 2026;223:111647 (full text); Guren MG et al. Radiother Oncol 2014.'))], first=True),
 panel('sabr','Pelvic SABR','Pelvic SABR reirradiation: nodes and sidewall','UK SABR Consortium guidance v2 (2025), the international Delphi (Slevin 2021) and the Leeds data.',
  [card('Eligibility (UK SABR Consortium / NHS England)', ul([
     'Recurrence in the pelvis of a histologically confirmed pelvic primary; prior pelvic RT with no enduring significant toxicity.',
     'Not for curative surgery (ineligible, declined, or positive margins).',
     '<b>More than 6 months</b> since the first course; WHO performance status ≤2; life expectancy over 6 months.',
     '<b>Excluded:</b> previously irradiated pelvic bone or spinal metastases; concurrent systemic or targeted therapy.',
     '<b>Do not use outside a trial</b> if tumour infiltrates the lumen of the GI tract or the bladder wall.',
     '<b>Avoid</b> with pelvic fibrosis, residual grade 3 toxicity from the first course, or inflammatory bowel disease.',
     'Caution after brachytherapy (dose reconstruction) and beyond the tested limit of 3 lesions, each under 6 cm.',
     'Delphi 2021: no consensus on minimum interval, lesion number or size, or cumulative constraints.']) + CAVEAT, key=True),
   card('Volumes, dose and coverage', tbl(['Item','Guidance'],[
     ('CTV, well-defined node','= GTV'),('CTV, soft tissue or spiculated node','GTV + 5 mm, edited at barriers'),('CTV, bone','GTV + 3–5 mm'),('PTV','5 mm typical; depends on equipment and imaging'),
     ('Dose, toxicity-limiting group (mainly prostate)','<b>30 Gy in 5 fractions</b>'),
     ('Dose, control-maximising group (mainly rectal, gynae)','Isotoxic escalation up to <b>45 Gy in 5</b> when the PTV is ≥1 cm from organs at risk and verification imaging is good'),
     ('Coverage','PTV V100% ≥95%; minimum 70% of PTV covered when compromising for an organ at risk; D0.1cc maximum 110–130% inside the PTV'),
     ('Planning priority (30 Gy/5)','Small bowel, large bowel, GTV, cauda equina, bladder, femoral heads, lumbosacral plexus, then PTV')]) +
     ul(['Daily IGRT with no action level; replicate bladder filling and enemas.','Follow-up at 6–8 weeks, then 3-monthly markers or imaging.','NHS commissioning-through-evaluation cohort (185 patients): local control 76% at 1 year and 47% at 2 years; grade 3 toxicity 3.8%; no grade 4–5.'])),
   card('How the UK guidance sets organ limits', ul([
     'Cumulative limit = the usual <b>de novo 5-fraction SABR constraint</b> converted to EQD2. Example: small bowel D0.1cc 35 Gy in 5 fractions = 70 Gy EQD2 (α/β 3).',
     'Convert the first-course organ dose to EQD2, then discount it for recovery: <b>30% at 6–18 months, 50% beyond 18 months</b>.',
     'Remaining EQD2 = limit minus discounted prior dose; convert back to 5 fractions.',
     'Worked example from the guidance: 45 Gy/25 to small bowel one year earlier = 43.2 Gy EQD2; less 30% = 30.2 Gy; remaining 39.8 Gy EQD2.',
     'α/β: 3 Gy for bowel, rectum, bladder, femoral heads and skin; 2 Gy for lumbosacral plexus and cauda equina.',
     'Use less recovery after extensive pelvic surgery, with diabetes or vasculopathy, in older or heavily pre-treated patients.',
     'The guidance calls this pragmatic and not evidence-based. Check any spreadsheet by hand. The <a href="rert-constraints.html#calc">remaining-dose calculator</a> does the same arithmetic.'])),
   card('Cumulative doses used and observed (Leeds)', tbl(['Organ','Study limit, cumulative EQD2 (D0.1cc)','Highest cumulative dose observed (56 patients)'],[('Bladder','110.0 Gy (α/β 3)','110–112 Gy'),('Rectum','89.9 Gy (α/β 3)','82.8–92.4 Gy'),('Small bowel','78.8 Gy (α/β 3)','111.9 Gy (point summation)'),('Colon','—','69.8–94.3 Gy'),('Sacral plexus','67.2 Gy (α/β 2) with 33% recovery','101.4 Gy'),('Vessels','—','108.1 Gy')]) + note('No severe toxicity attributable to reirradiation in the Leeds cohort; these are observed doses, not tolerance doses. Older proposal (Abusaris 2011): 110 Gy bladder, 100 Gy rectum, 90 Gy bowel (α/β 3).') +
     note('Sources: UK SABR Consortium guidance v2 (supplement to Moreno-Olmedo E et al. tipsRO 2025;35:100326; full text); Slevin F et al. Radiother Oncol 2021;164:104–14; Slevin F et al. Clin Oncol 2025;43:103861; Phys Imaging Radiat Oncol 2025 (isotoxic study); Abusaris H et al. Radiother Oncol 2011;99:235–9.'))]),
 panel('prostate','Prostate','Local recurrence after prostate radiotherapy','MASTER meta-analysis, ESTRO ACROP Delphi and brachytherapy series.',
  [card('Choosing a salvage modality (MASTER, Valle 2021)', tbl(['','Adjusted 5-year RFS','Severe GU toxicity'],[('Radical prostatectomy','reference','20%'),('SBRT','about 60%','5.6%'),('HDR brachytherapy','about 60%','9.6%'),('LDR brachytherapy','no significant difference from RP','9.1%'),('Cryotherapy','about 50%','—')], wide=False) + note('150 studies, study-level, heterogeneous. No modality differed significantly from prostatectomy for 5-year recurrence-free survival; all three radiotherapy options had less severe GU toxicity, and HDR less severe GI toxicity.') + CAVEAT, key=True),
   card('Selection and work-up', ul(['Biopsy-proven local recurrence, usually ≥2 years after primary RT, with PSMA PET and MRI excluding metastases. '+V+' for the interval.','ESTRO ACROP Delphi (salvage SBRT): consensus on no age limit, ECOG 0–1, satisfactory urinary flow, exclusion of metastatic disease, and target defined on MRI.','No consensus on concurrent ADT, how to account for the first-course dose, or whether Phoenix criteria apply after salvage.','Focal salvage suits unifocal disease with imaging–pathology concordance; whole-gland otherwise.'])),
   card('Schedules reported', ul(['<b>HDR brachytherapy:</b> 19 Gy in 1 fraction (focal), or 12–13.5 Gy × 2 (24–27 Gy). Dose-escalated focal HDR up to 30 Gy in 1–2 fractions was reported as safe in the F-SHARP phase 1/2 (ASTRO 2024).','<b>SBRT:</b> commonly 30–36 Gy in 5–6 fractions. '+V,'<b>LDR (RTOG 0526):</b> late grade 3 GI/GU events 14%; 10-year biochemical PFS 46%.','Systematic review (2021): 2-year bRFS about 74% HDR, 71% LDR, 55% SBRT; late grade ≥3 GU 7.9% HDR, 13.6% LDR, 2.7% SBRT.','Cumulative rectum and bladder limits from one SBRT series: see <a href="rert-constraints.html">limits</a>.']) + note('Sources: Valle LF et al. Eur Urol 2021;80(3); Jereczek-Fossa BA et al. Cancer Treat Rev 2021;98:102206; Crook J et al. RTOG 0526, IJROBP 2019; Front Oncol 2021;11:681448.'))]),
 panel('gynae','Gynae','Gynaecological recurrence after pelvic RT','Mostly brachytherapy; evidence is retrospective.',
  [card('Options', ul(['Central recurrence: pelvic exenteration is the surgical standard, with high morbidity.','<b>Image-guided interstitial brachytherapy</b> is the best-suited reirradiation technique for central and paracentral recurrences: more conformal than EBRT or SBRT in dosimetric comparisons (Bockel 2021).','Reported 2–3 year local control about 50% with interstitial brachytherapy.','<b>SBRT</b> for nodal and sidewall relapse: local control about 80% at 1 year and 50% at 2 years.','HDR schedules of 4–6 Gy twice daily for 5–10 fractions (EQD2<sub>10</sub> about 40–50 Gy) are common.','Better outcomes with small recurrences, longer interval, complete response and higher target dose.']) + CAVEAT, key=True),
   card('Risks and consent', ul(['Fistula, bowel obstruction, vaginal necrosis and ureteric stenosis are the feared late effects; quote unit data where available. '+V,'Refer to a centre with interstitial experience.','Cumulative EQD2 limits for rectum, bladder, bowel and urethra have been proposed from published series (Faundez 2026) but are not standardised.']) + note('Sources: Bockel S et al. Cancers 2021;13:1226; ecancer 2026;20:2091; narrative reviews of gynaecological reirradiation.'))]),
])
print('written')
