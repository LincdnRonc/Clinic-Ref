# Figures to verify against original papers

## Breast
- AMAROS 5 y lymphoedema: source gives 25% → 12% (ALND vs axillary RT). The published figure is usually 23% vs 11% (clinical signs).
- TARGIT-A: the source gives estimated 10 y local failure (1.7% EBRT vs 6.6% IORT) from a secondary analysis, not trial-reported LR.
- EXPERT (ANZ 1601): no results in source; card says check before quoting.

## Thorax
- VT radioablation: the source header gives 24/1 for Cuculich/Robinson but 25/1 for the phase I/II. The page uses 25 Gy × 1.
- Takahashi PCI (ES-SCLC): the source has two sets of brain-metastasis figures (12 mo 59 → 33%, and "1y 69 → 48%"). The page uses 12 mo 59 → 33%.

## CNS: vestibular schwannoma (cns-vs.html)
- Source is a Nov 2026 evidence review (Claude doc), not RadOncReview. Pollock 2006, Breivik 2013, Régis 2010 and the Bartek RCT were taken from secondary summaries; check originals.
- cns-benign.html VS panel (from RadOncReview) quotes 10 y control about 97% and serviceable hearing 41–79% at 5 y; cns-vs.html quotes 91–94% at 10 y (Pittsburgh, Vienna, Munich) and about 50% at 5 y. Different source series, not a conflict, but harmonise if preferred.
- Brainstem surface point dose (<12–14 Gy single fraction) is common practice, not from a single guideline; check departmental SRS protocol.

## Liver SBRT OAR protocol (contouring/liver-sbrt.html), v1.0 Nov 2026
- v1.1: Section 3 rewritten from the Jabbour 2014 author manuscript (PMC4285338). Jabbour has no border table; its definitions are in the text, and Table 1 gives kappa values. Resolved: liver portal-vein/IVC/gallbladder rules, whole duodenum to the ligament of Treitz, loops not bowel bag, renal pelvis included, chest wall = liver + lung expanded 2 cm (no sternum or vertebral bodies), CBD extent.
- Still open from Section 3: oesophagus and heart borders (Jabbour gives contours but no written rule; check against Kong 2011 RTOG thoracic atlas); small/large bowel cranio-caudal extent (departmental); Lukovic 2020 full text for MRI-specific tips (the ScienceDirect link supplied had expired; needs the PDF uploaded).
- UK SABR 2022 (Diez) Tables 2–5 were read from the accepted manuscript, whose extracted text flattens the optimal/mandatory columns. Every value marked check in Section 8 needs its column confirmed in the published tables (stomach, duodenum, small and large bowel 3 fx; liver 5 fx mean 13 vs 15.2; CBD 50 Gy; combined kidney; heart second values; spinal canal 20.3/25.3).
- Osmundson 2015: PMID not yet verified (library uses a title search). Check from the methods whether the cHBT was cropped by GTV/PTV.
- TG-263 names to confirm against the worksheet: Chestwall, GreatVes / A_Aorta / V_Venacava_I, Bile_Duct_Common, V_Portal. Confirm the 16-character limit and z-prefix rule in the report itself (taken from a secondary summary).
- MR-linac re-contouring zone (3 cm radial / 2 cm CC) is adopted from a single-fraction SMART protocol in pancreas; needs departmental sign-off for liver.
- Oesophagus cranial extent ("2–3 slices above the PTV") is a placeholder; set departmentally.

## Palliative: WBRT principles (pall-wbrt.html), Nov 2026
- Source is an evidence synthesis (trial abstracts, news reports of ASTRO/WCLC 2026), not RadOncReview. NRG CC009 and MAVERICK are conference data; update when published.
- NRG CC001 6-month cognitive failure: the JCO 2020 / ASCO Post figure 68.2 → 59.5% is used. The SNO 2018 preliminary report gave 69.1 → 58.0%. pall-brain.html currently quotes 63 → 55%; harmonise.
- Cochrane 2018 lower-BED HR 1.21: check which schedules fall in that comparison (mainly ultra-rapid 10/1, 12/2). eviQ 1251 says 20/5 is neither inferior nor superior to higher doses.
- DeAngelis 1989: "no dementia with ≤3 Gy per fraction" comes from a secondary review; check the original.
- HA-WBRT constraints: only hippocampus D100% ≤9 Gy, Dmax ≤16 Gy and PTV D98% ≥25 Gy are quoted. Add the full CC001 table (PTV D2%, V30, optic structures) from the protocol if wanted.
- Re-irradiation (20/10) and PCNSL 23.4/13 are common practice, not trial-quoted figures here; check against departmental and haematology protocols.
- Hair regrowth timing (2–3 months) and the somnolence window are general textbook values.
- Amantadine: no RCT in brain RT; the dose is standard Parkinson's/TBI dosing. Check the AU product information for renal dosing.

## Lung contouring protocol (contouring/lung.html, Nov 2026)
- SUNSET 60 Gy/8 # result (Giuliani 2024) taken from the web abstract; not in the folder or departmental protocol.
- Lung ART primary results (3-year DFS 47% vs 44%, late G3–4 cardiopulmonary 11% vs 5%) from the published abstract; folder holds only the protocol supplement.
- Departmental V4 55 Gy/20 # spinal canal minor range printed "41–454 Gy" (read as 41–44); spinal canal extent "10 mm" above/below PTV (Kong/RTOG use 10 cm).
- Lung OAR definition: Kong 2011 (inflated lung only) vs NRG template (include collapsed lung).
- UK 2022 Table 2 skin column placement (transcribed from two-column PDF).
- TG-263 names and RayStation 4D workflow to confirm with physics.
- Departmental source is the Liverpool/Macarthur V4 (2024) protocol (chosen by Lincoln as the departmental standard for all sites).
- Missing starred source: Guckenberger 2017 ESTRO-ACROP SBRT.

## Oesophagus & GOJ protocol (contouring/oesophagus.html)
- CROSS volumes (PTV = GTV + 4 cm CC, 3 cm into stomach, 1.5 cm radial) quoted from memory/site note — verify against van Hagen 2012 NEJM or the CROSS protocol.
- No Liverpool oesophageal protocol: simulation, 4D policy, PTV margins, IGRT match and constraints are SW ODN 2023 (SCOPE2) values.
- Airway edit of CTV_B (not on SW ODN edit list); adjuvant cranio-caudal extent; conduit dose; splenic vaccination pathway (SW ODN cites BCSH); adjuvant nivolumab PBS status; AJCC location definitions.
- Machiels 2019 (Radiat Oncol) page number; Nowee 2019 journal (ctRO?).
- Elective coeliac/gastrohepatic coverage for N+ GOJ adenocarcinoma and cervical elective neck levels: departmental decision.

## Breast protocol (contouring/breast.html)
- Departmental source: SWSLHD (Liverpool/Macarthur) breast contouring protocol v4.0 (June 2021). It has no partial breast or brachytherapy section.
- DBCG PBI CTV/PTV margins and RAPID PTV margin (+10 mm) need the trial papers; RAPID CTV from a secondary source.
- 26 Gy/5 to the IMPORT LOW partial breast volume is an extrapolation of FAST-Forward; check local/eviQ 3658.
- GEC-ESTRO 2015 EBRT PTV margin stated as 10 mm in the text and 20 mm in the summary.
- Department level 4 cranial "often inferior edge of cricoid" vs ESTRO (≤2 slices above subclavian vein).
- Department palliative "40.05 Gy/9#" as written (likely a typo).
- Routine 3 mm PMRT bolus (department) vs Delphi 2021 (not routine).
- IGRT policy; RayStation NS crop recipe; local PBI/brachytherapy names; autologous flap guideline not in folder.
- DBCG PBI page numbers (JCO 2022;40:4189–?).

## Gynae protocol (contouring/gynae.html)
- Departmental source: SSWAHS (LCTC & MCTC) gynae RT contouring protocol, 22 June 2020 (K Lim, reviewed V Do), written for MIM/Pinnacle; confirm it is current and the RayStation names/template.
- High-risk CTV-E upper border: department gives top of L2 (risk table) and top of L1 (expansions, CTVn_PA); EMBRACE II says at least renal veins (usually incl. L2). Page uses renal veins / top of L1, whichever is higher.
- Presacral strip width: department 10 mm (cervix sections) vs 15 mm (vagina section); Small 2021 1–1.5 cm.
- Department external/internal iliac inferior border "top of acetabulum" vs Small 2021 (circumflex origin / vessels turn laterally).
- Department inguinal anterior 20 mm vs Gaffney appendix anterior 23 mm (anteromedial 35, anterolateral 25, medial 22).
- Department definitive vulva CTVp = GTVp + 0.5–1 cm vs Gaffney 2016 whole vulva; page follows Gaffney — confirm with gynae team.
- Post-op EBRT OAR constraints: none in the department document; page quotes NRG GYN template (2018) example values.
- IGRT method for post-op, vaginal and vulval cases not in the department document.
- CTV_IR margin per direction (Haie-Meder 2005 / ICRU 88) not in folder; NRG template gives CTV_HR + 5–15 mm.
- Not in folder: Fields 2025 intact cervix update, Viswanathan 2014 CT vs MRI HR-CTV, ABS vaginal cuff guideline (Small 2012), Schmid 2020, Kamrava 2023.
- EMBRACE II summary paper reference (Pötter 2018 CTRO 9:48–60): add DOI after checking.

## Anal protocol (contouring/anal.html)
- Departmental source: SWSLHD anal canal SCC contouring protocol (1 Sept 2020), written for Pinnacle; confirm current RayStation names and simulation guide.
- Department inguinal anterior border "minimum 7 mm" in front of femoral vessels vs AGITG "minimum 20 mm" (department otherwise copies AGITG); page uses ~20 mm (to 5 mm from skin) + visible nodes.
- Department T1N0 CTV42 excludes external iliac and inguinal nodes and starts at the top of the mesorectum (differs from AGITG/UK/ECOG); confirm intended.
- No departmental IGRT method or OAR constraint table; page quotes UK v4 planning sheet and ECOG-ACRIN EA2182 table.
- RTOG 0529 protocol constraints not in folder.

## Spine and bone SBRT protocol (contouring/spine-bone.html)
- Departmental source: St George CCC spine SBRT protocol, DRAFT v9 (2024) — confirm it is the current approved version. It lists de novo schedules only (post-op and re-irradiation taken from the 2021 bone and soft tissue SABR protocol, origin not stated in the document).
- Motion management: St George "none required" vs folder spine protocol 4D-CT for mid-thoracic and below (OAR ITVs).
- 1-fraction OAR constraints are from the 2021 bone/soft tissue protocol (St George table covers 2, 3 and 5 fractions).
- National spine SABR protocol (2023) sacrum CTV = GTV, PTV + 10 mm differs from Dunne 2020 (page follows Dunne).
- Local RayStation names/prefixes.
- ISRC row "body + bilateral pedicles": sector list derived from the CTV description (PDF table layout garbled).

## CNS protocol (contouring/cns.html)
- No Liverpool or St George CNS protocol in the folder; page uses ESTRO-EANO (glioma), RTOG 0539/EORTC 22042 (meningioma, via ARRO case), ISRS (VS), Soliman 2018 + Canberra Health Services SRS guideline, RTOG 0933/NRG CC001. Local PTV/IGRT and naming to confirm.
- Baumert 2025 margins now verified from the paper (G2 GTV + 10 mm, G3 + 15 mm, PTV ≤3 mm; 50.4/28 and 59.4/33).
- Not in folder: Combs 2021 ESTRO-ACROP skull base (pituitary, craniopharyngioma, skull-base meningioma), EORTC 1308, grade 1 intact meningioma margins.
- RTOG 0539 and EORTC 22042 volumes taken from the ARRO case slides, not the protocols themselves.

## Head and neck protocol (contouring/head-neck.html)
- No departmental H&N protocol in the folder; page follows DAHANCA 2018 / Grégoire 2014 & 2018 / Biau 2019; local PTV margins, IGRT and naming to confirm.
- Biau 2019 node-positive CTV-N-HR = GTV-N + 5 mm now verified (clears the quick-protocol check).
- Evans 2025 ESTRO post-op oral cavity not in folder; folder items not yet used: trigeminal atlas 2018, PNS guideline 2018, parotid pathways 2022, ESTRO base of skull 2021, ASTRO oropharynx.
- NPC Ib indications and CTVp_50 structure list summarised, not reproduced in full (see Lin 2025 Table 1/E1).

## Lymphoma ISRT protocol (contouring/lymphoma.html)
- No departmental lymphoma protocol; page follows Wirth 2020 ILROG overview, Specht 2014 and the ILROG mini-atlas. ITV/PTV/IGRT institutional.
- Wirth Table 1 (Dabaja 2018) OAR optimal/acceptable levels not reproduced: folder text extraction garbled — transcribe from the PDF.
- Not in folder: Illidge 2014, Yahalom 2015, Tsang 2018 plasmacytoma, TBI/TMI guidance.

## Bladder (contouring/bladder.html) — Nov 2026
Sources in folder: FROGG 2020 (Cardoso, JMIRO 64:882–893) and Baumann 2016 post-cystectomy consensus slides (NRG-GU001). No departmental bladder protocol.
- Departmental bladder filling (empty vs comfortably full), bowel preparation, contrast, immobilisation — not in sources.
- Departmental PTV margins; FROGG gives only an example (15 mm sup/ant, 10 mm elsewhere with daily CBCT, Adil 2019). High-risk PTV margin not given.
- Plan-of-the-day library: number and timing of scans, selection rule — not in sources (RAIDER/BC2001 protocols would resolve).
- Elective node dose in a 20-fraction SIB: FROGG quotes 45–50.4 Gy in 1.8 Gy only. GTVn-to-CTV margin not given.
- FROGG Table 14 title says 64 Gy/32 but the text says 64 Gy in 34 fractions; page uses 32.
- Post-cystectomy: dose, fractionation, PTV and IGRT not in the slides (NRG-GU001 protocol).
- Baumann: presacral nodes listed only for positive margins in the coverage table but included in the "nodal CTV" union — check the IJROBP paper.
- Baumann plane 2: border table says from the posterior aspect of the symphysis; figure caption says the anterior border — check the paper figure.
- BC2001/BCON CTV and PTV margins quoted from the bladder site page for comparison (not from a supplied PDF).
- Department structure names (TG-263 suggestions only; diversion and ostomy bag names non-standard).
- IBIS post-cystectomy update (Verghote 2022) quoted on ctr-bladder.html was not supplied.

## Clinical scores page (scores.html) and calculators (tools.html)
- All scoring rules and formulas were entered from memory of the standard definitions, not from supplied sources; each is tagged Verify on the page. Check against the original papers: Child-Pugh, ALBI (Johnson 2015), MELD, Roach formulas, D'Amico, UCSF-CAPRA, CTS5 (Dowsett 2018 coefficients and cut-offs), USC/Van Nuys PI, SINS (Fisher 2010), Mirels, ESCC, RPA (Gaspar 1997), IPI/R-IPI, IPS, Deauville, Sedlis (GOG 92), ProMisE order, mrTRG, ppo-FEV1 segment counts, Cockcroft-Gault/Calvert.
- Gap calculator defaults (K 0.9 Gy/day, Tk 28 days) need the RCR interruptions guidance.
- External tools marked "(web search)" have no verified address yet; IBTR! 2.0's original Tufts address may be dead.

## Auto-staging (assets/staging.js)
- All 18 stage-group tables and the abbreviated T/N definitions were entered from memory (AJCC 8; lung TNM 9; FIGO 2018 cervix; FIGO 2009 endometrium; Lugano). Verify each against the manual. Known edition caveats: anal and nasopharynx have AJCC version 9 updates; endometrium FIGO 2023 not implemented; breast prognostic stage not implemented. No stager yet for testis, vulva, skin/melanoma, sarcoma, thyroid, salivary, SCLC-specific or paediatric tumours.
