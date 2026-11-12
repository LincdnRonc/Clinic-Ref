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
