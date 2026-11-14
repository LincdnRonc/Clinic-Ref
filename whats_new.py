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
]
SITE = [
 ('2026-11-14', 'New Clinic quick links page (Tools): radiology PACS and pathology results logins grouped by St George, Liverpool, Wollongong and Sydney, plus referral forms and imaging references.', 'links.html'),
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
