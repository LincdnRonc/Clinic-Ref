"""What's New page data. The weekly evidence digest appends to EVIDENCE; SITE is the site change log.

EVIDENCE entry: (date 'YYYY-MM-DD', site, tag, title, summary, url, source, affects)
  tag: 'practice' (practice-changing) | 'confirms' (confirms current practice) | 'watch'
  summary: one or two sentences in our own words (design, arms, headline result). No copied text.
  source: where it was seen (journal, the Limbic, theMednet, Quad Shot, conference)
  affects: list of (page, label) on this site that the item bears on; [] if none
SITE entry: (date, text, page or '')
"""
EVIDENCE = [
 ('2026-11-04', 'Breast', 'confirms', 'HypoMast-IMNI: hypofractionated PMRT including internal mammary nodes',
  'Randomised phase III trial in high-risk breast cancer after mastectomy comparing 16-fraction hypofractionated PMRT with conventional fractionation, both including internal mammary node irradiation. Hypofractionation was reported as noninferior for locoregional control, supporting moderate hypofractionation when the IMN chain is treated. (check)',
  'https://pubmed.ncbi.nlm.nih.gov/42896129/', 'PubMed listing; reported by CancerNetwork and The ASCO Post',
  [('breast-nodes-pmrt.html#pmrt','PMRT'), ('breast-nodes-pmrt.html#rni','Nodal RT')]),
 ('2026-11-09', 'Thorax', 'confirms', 'KEYNOTE-867: pembrolizumab added to SBRT for unresected stage I–II NSCLC',
  'Double-blind phase III trial of SBRT with pembrolizumab or placebo in medically inoperable or surgery-declining stage I–II NSCLC. Adding pembrolizumab did not improve event-free survival, so SBRT alone remains the standard outside a trial. (check)',
  'https://ascopubs.org/doi/10.1200/JCO-26-00404', 'Journal of Clinical Oncology (PubMed 42950173); reported by Targeted Oncology, CancerNetwork, The ASCO Post',
  [('thorax-early.html#sabr','Early-stage NSCLC: SABR')]),
 ('2026-11-14', 'Bladder', 'watch', 'FDA approves perioperative durvalumab with enfortumab vedotin for cisplatin-ineligible MIBC',
  'US FDA approval (announced November 2026) of neoadjuvant enfortumab vedotin plus durvalumab with radical cystectomy, then adjuvant durvalumab, for cisplatin-ineligible muscle-invasive bladder cancer. Not an RT trial, but it raises the bar for trimodality bladder preservation in this group if it reaches Australia. (check)',
  'https://www.fda.gov/drugs/cancer-approvals/fda-approves-durvalumab-enfortumab-vedotin-ejfv-muscle-invasive-bladder-cancer', 'FDA approval notice; reported by OncoDaily and The ASCO Post',
  [('gu-bladder.html#tmt','Bladder preservation'), ('gu-bladder.html#other-settings','Post-op, NMIBC & systemic')]),
 ('2026-11-11', 'Head and neck', 'watch', 'CSCO–ASCO joint guidelines on nasopharyngeal carcinoma (stage IB–III, and recurrent/metastatic)',
  'Two joint Chinese Society of Clinical Oncology and ASCO guidelines published in JCO in November 2026: an update covering definitive treatment of stage IB to III NPC (replacing the 2021 stage II–IVA guideline on chemotherapy with RT), and a new guideline for recurrent and/or metastatic disease. Recommendations not yet read; compare with the NPC page before changing anything. (check)',
  'https://ascopubs.org/doi/10.1200/JCO-26-02648', 'Journal of Clinical Oncology (also JCO-26-02650 for recurrent/metastatic); seen via a journal search',
  [('hn-npc-sinonasal.html#npc','Nasopharynx')]),
 ('2026-11-18', 'Breast', 'confirms', 'IRMA: partial-breast vs whole-breast irradiation for low-risk invasive breast cancer, 5-year results',
  'Multicentre randomised phase III trial comparing external-beam accelerated partial-breast irradiation (twice-daily, 10 fractions) with whole-breast irradiation after breast-conserving surgery in low-risk invasive disease. Five-year results report low local recurrence with PBI, adding to IMPORT LOW and Florence in support of PBI for well-selected low-risk patients. (check)',
  'https://pubmed.ncbi.nlm.nih.gov/43044095/', 'PubMed listing (journal to confirm); reported by Omnicuris (18 Nov 2026), MIMS and OncoDaily',
  [('breast-early.html#pbi','Partial breast')]),
 ('2026-11-20', 'Prostate', 'watch', '24 Gy single-dose vs five-fraction SBRT for intermediate-risk prostate cancer: long-term pooled analysis',
  'Pooled analysis of two separately randomised cohorts comparing 24 Gy in a single fraction with five-fraction SBRT in intermediate-risk prostate cancer, reporting long-term toxicity and biochemical control. Headline figures were not visible in search results, so read the paper before quoting it; single-fraction treatment remains investigational. Date placed from PubMed indexing. (check)',
  'https://pubmed.ncbi.nlm.nih.gov/43057343/', 'PubMed listing (journal to confirm); seen via a journal search',
  [('gu-prostate.html#localised','Localised disease')]),
]
SITE = [
    ('2026-11-25', 'My weekly roster under Tools: Week A/B sessions merged with MDTs, plus the Kinghorn MDT planner.', 'roster.html'),
    ('2026-11-23', '32 more key trials across paediatrics, gynae, lymphoma, CNS, H&N, thorax, GI, GU and melanoma ("More key trials" cards); contouring-guide links shown as call-out boxes.', ''),
    ('2026-11-23', 'New tabs: locally advanced and inflammatory breast cancer, osteosarcoma, other benign conditions; additions on brainstem glioma, ovarian and penile cancer.', 'breast-nodes-pmrt.html#labc'),
    ('2026-11-23', 'New Principles & techniques section: radiobiology, physics, imaging and IGRT, brachytherapy, protons and MR-guided RT, emergencies, simulation and set-up, statistics and trial design.', 'prin-radiobiology.html'),
    ('2026-11-23', 'Prostate contouring guide 2d.3b: how to find the neurovascular elements, internal and accessory pudendal arteries, external sphincter and crura on MRI, with a schematic (Lee and Spratt 2016).', 'contouring/prostate.html#s2d'),
    ('2026-11-23', 'Prostate contouring guide, new section 2d: erectile function-sparing RT. Delineation of neurovascular bundles, internal pudendal arteries, penile bulb and crura; ERECT constraints for 36.25 Gy in 5 fractions; penile bulb and crura goals for conventional and moderately hypofractionated RT; POTEN-C, ERECT, Spratt and ETS-IMRT results.', 'contouring/prostate.html#s2d'),
    ('2026-11-19', 'Exam notes tab on each tumour-site page (44 pages): the matching Phase 2 exam-summary notes (AS summary), labelled as unverified revision notes. The standalone exam section stays for whole-topic revision and general viva tabs.', 'gu-prostate.html#exam'),
 ('2026-11-19', 'Life expectancy calculator on Clinical scores (Prostate tab): Australian Life Tables 2020–22 by age and sex, NCCN ±50% health-quartile adjustment with a Charlson guide, and the NCCN life-expectancy thresholds for each risk group.', 'scores.html#prostate'),
 ('2026-11-19', 'Consent numbers moved from Tools to a Toxicity & consent tab on each tumour-site page, with a print button. Breast, head and neck sub-pages and brain metastases show the shared rates from their general page.', ''),
 ('2026-11-18', 'New MDT decision matrix: tap case details as they are presented and the matching evidence-based scenario remains, with decision, options, RT dose, trials and what still needs establishing. A tab on the prostate, pancreas, oesophagus and gastric, liver and biliary, rectum and lung pages, and all of them on one Tools page. Rows marked (check) are not yet verified.', 'mdt.html'),
 ('2026-11-17', 'EXTEND prostate basket (Tang, JAMA Oncol 2023) added from the paper: intermittent hormone therapy ± metastasis-directed therapy for oligometastatic prostate cancer (PFS HR 0.25; eugonadal PFS HR 0.32). Prostate key trials and MDT card, and oligometastatic page.', 'gu-prostate.html#trials'),
 ('2026-11-17', "New Contacts page (Tools): GenesisCare St Vincent's extensions, St Vincent's Hospital numbers and other GenesisCare NSW centres, with tap-to-call. Mobile numbers are kept off the site.", 'contacts.html'),
 ('2026-11-16', "What's new: the To verify tab has been removed; the list of figures still to check is now kept off the site.", ''),
 ('2026-11-16', 'Prostate contouring guide: new section on 5-fraction SABR (selection, preparation, target volumes and the seminal vesicle rule, urethra, dose and scheduling, target objectives, OAR constraints, margins and motion management, MR-linac), from the ESTRO 2026 SBRT consensus, the PACE planning guidelines and the departmental SBRT protocols.', 'contouring/prostate.html#s2c'),
 ('2026-11-15', 'Pancreas: new Pathway & evidence tab. A flow by resectability group showing where RT enters, a table of RT decision points with the trials for and against, SBRT vs chemoRT selection factors for stable locally advanced disease, and a pre-RT checklist. CONKO-007 added to Key trials (check).', 'gi-pancreas.html#pathway'),
 ('2026-11-15', 'Upper GI key trials expanded (all marked check until read from the papers): MASTERPLAN, PANDAS/PRODIGE 44 and PAULA-1 on pancreas, plus a new metastatic and oligometastatic card (MPACT, NAPOLI-3, EXTEND, SIRT); MISPHEC, ABC-07, KEYNOTE-966, Hong protons and CCTG HE1 on hepatobiliary; KEYNOTE-975, Stahl, JCOG0508, TROG 03.01, SIREC and the first- and second-line immunotherapy trials on oesophagus; RENAISSANCE and palliative gastric RT on gastric; Tang oligometastatic RCC on kidney.', 'gi-pancreas.html#trials'),
 ('2026-11-14', 'New Clinic quick links page (Tools): radiology PACS and pathology results logins (A to Z), plus referral forms.', 'links.html'),
 ('2026-11-14', 'Every key trial now shows its year of publication in brackets (first full report, plus the later update where the card quotes long-term results; meeting name where only presented).', ''),
 ('2026-11-14', 'Evidence digest edits: HypoMast-IMNI added to PMRT trials; KEYNOTE-867 and the JCO SABR vs surgery emulated trial added to early-stage NSCLC; VOLGA (perioperative durvalumab + EV) added to bladder systemic therapy.', 'thorax-early.html#sabr'),
 ('2026-11-14', 'Reirradiation: liver and bladder tabs added (abdomen and pelvis page).', 'rert-pelvis.html#liver'),
 ('2026-11-14', 'Reirradiation section updated from the full papers: head and neck consensus (Biau 2026), ESTRO rectal 2026, UK SABR pelvic method, ESTRO–ISRS spine, thoracic limits compared, Nieder cord risk score in the calculator.', 'rert-constraints.html'),
 ('2026-11-14', 'New Reirradiation section: ESTRO–EORTC principles and workflow, cumulative dose limits with a remaining-dose calculator and cord check, and site pages for CNS/spine/bone, head and neck, thorax and breast, pelvis.', 'rert-principles.html'),
 ('2026-11-14', 'NCCN prostate risk group calculator (prostate page, Staging & risk tab); prostate very-high-risk definition updated to NCCN 2025; disclaimer now on the home page only.', 'gu-prostate.html#staging'),
 ('2026-11-13', 'New Systemic therapy section: concurrent chemo-RT regimens, targeted and immunotherapy timing with RT, breast and prostate endocrine therapy, bone agents, supportive drugs (venlafaxine, dexamethasone and more).', 'sys-chemort.html'),
 ('2026-11-13', 'Auto-staging tab on the tumour-site pages (18 staging systems; also all together on the clinical scores page).', 'scores.html#staging'),
 ('2026-11-13', 'Clinical scores and nomograms page (Child-Pugh, ALBI, PSA doubling time, Roach, CTS5, SINS and more, with links to external tools); personal-resource disclaimer on every page.', 'scores.html'),
 ('2026-11-13', 'One contouring entry per site: each quick guide is now the "Quick reference" first tab of its full guide.', 'index.html#contouring'),
 ('2026-11-13', 'Site-wide search, "Contour now" view on every contouring guide, copy buttons on tables, pinned pages, calculators, consent numbers and doses-at-a-glance pages; installable as an app with offline use.', 'tools.html'),
 ('2026-11-13', 'Contouring pages renamed "contouring guides" and shown in the normal site layout; thorax quick guide and lung guide merged into one Thorax guide.', 'contouring/thorax.html'),
 ('2026-11-13', 'New full contouring guides: breast, gynae, anal canal, spine and bone SBRT, CNS, head and neck, lymphoma ISRT, bladder.', 'index.html#contouring'),
 ('2026-11-12', 'New full contouring guides: lung (now Thorax), biliary, pancreas and stomach, oesophagus and GOJ. Phase 2 exam summary section added.', 'index.html#contouring'),
]
