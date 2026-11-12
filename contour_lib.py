# Contouring guideline library data.
# Each region: (tab id, tab label, lede, [ (card title, [entries]) ])
# entry: (year, title, cite, note, link, star)
#   link: 'pm:PMID' (verified on PubMed), 'doi:...', 'q:search terms' (PubMed title search), or full https URL
#   star: True = start here (current major guideline)

LIB = [
('breast','Breast','Whole breast, chest wall, regional nodes, reconstruction, partial breast and cardiac OARs.',[
 ('Target volumes: breast, chest wall and nodes',[
  (2015,'ESTRO consensus guideline on CTV delineation for elective RT of early breast cancer','Offersen · Radiother Oncol','The standard European atlas: CTVp breast/chest wall, levels 1–4, IMN, interpectoral; vessel-based nodal borders.','pm:25630428',True),
  (2016,'ESTRO guideline version 1.1 (post-mastectomy chest wall)','Offersen · Radiother Oncol','Adds chest-wall CTV after mastectomy without reconstruction.','pm:26791404',True),
  (2019,'ESTRO-ACROP PMRT after implant-based immediate reconstruction','Kaidar-Person · Radiother Oncol','Implant usually excluded from CTV; pre- vs subpectoral implant volumes.','pm:31108277',True),
  (2021,'Planning PMRT after implant reconstruction using ESTRO-ACROP','Kaidar-Person · Clin Oncol','Worked planning examples for the 2019 guideline.','pm:32988717',False),
  (2013,'DBCG national contouring guidelines and atlas','Nielsen · Acta Oncol','Danish atlas; basis of later ESTRO work.','pm:23421926',False),
  (2009,'RTOG breast cancer contouring atlas (web)','RTOG / NRG consensus','Larger, muscle-based nodal volumes (SCV to cricoid). Still used in NRG trials; compare with ESTRO.','q:RTOG breast cancer atlas axillary lymph nodes Gentile',False),
  (2015,'Axillary nodes on the RTOG atlas: evaluation','Gentile · IJROBP','Nodal recurrence mapping vs RTOG volumes.','pm:26383674',False),
  (2020,'RTOG vs ESTRO breast nodal atlases compared','Loganadane · IJROBP','Where the two atlases differ and coverage of recurrences.','pm:32334035',False),
  (2018,'Recurrence patterns validating the ESTRO CTV guideline','Chang · Radiother Oncol','Supports ESTRO borders; notes recurrences outside some volumes.','pm:29050960',False),
  (2019,'FDG-PET/CT lymph-node atlas in breast cancer','Borm · IJROBP','Where involved nodes sit relative to ESTRO/RTOG volumes.','pm:30118822',False),
  (2019,'Comparison of breast contouring guidelines (Australasian)','Gee · J Med Imaging Radiat Oncol','ANZ review of ESTRO vs RTOG vs others.','pm:30267561',False),
  (2024,'Prone-position axillary contouring atlas','Purswani · Pract Radiat Oncol','Nodal anatomy shifts when prone.','pm:38729261',False),
 ]),
 ('Tumour bed, partial breast and set-up',[
  (2018,'GEC-ESTRO breast WG: target definition for APBI / boost','Strnad · Radiother Oncol','Tumour-bed definition, clips, seroma, margins for APBI and boost.','q:Recommendations from GEC ESTRO Breast Cancer Working Group target definition accelerated partial breast irradiation',True),
  (2020,'MRI contouring of primary breast tumours (preoperative PBI)','Vasmel · Pract Radiat Oncol','For neoadjuvant / ablative PBI studies.','pm:32315784',False),
  (2024,'ASTRO partial breast irradiation guideline','Shaitelman · Pract Radiat Oncol','Selection and technique (not an atlas).','pm:37977261',False),
  (2023,'ESTRO-ACROP positioning, immobilisation and set-up verification for breast RT','Mast · tipsRO','Immobilisation, DIBH, IGRT.','pm:37745181',False),
 ]),
 ('Cardiac OARs',[
  (2011,'Heart atlas for breast RT (whole heart, chambers, LAD)','Feng · IJROBP','The widely used cardiac substructure atlas.','pm:20421148',True),
  (2017,'Cardiac contouring atlas for radiotherapy','Duane · Radiother Oncol','Detailed CT substructure atlas (coronaries, valves).','q:Duane cardiac contouring atlas for radiotherapy',False),
  (2020,'Danish whole heart and substructure delineation guidelines','Milo · Radiother Oncol','DBCG cardiac guideline.','pm:32544606',False),
 ]),
]),
('thorax','Thorax','NSCLC, SCLC, SBRT, post-op, mesothelioma, thymus and thoracic OARs.',[
 ('Lung cancer targets',[
  (2018,'ESTRO-ACROP target volume definition for locally advanced NSCLC','Nestle · Radiother Oncol','PET-CT GTV, involved-node CTV, post-op CTV, motion management.','pm:29605476',True),
  (2026,'ESTRO-EORTC guideline on target delineation for stage I–III SCLC','Levy · Radiother Oncol','Newest SCLC guideline: post-chemo volumes, nodal selection.','pm:41932500',True),
  (2017,'ESTRO-ACROP SBRT for peripheral early-stage NSCLC','Guckenberger · Radiother Oncol','Simulation, 4D ITV, GTV=CTV, PTV, dose reporting.','q:ESTRO ACROP consensus guideline on implementation and practice of stereotactic body radiotherapy for peripherally located early stage non-small cell lung cancer',True),
  (2009,'IASLC lymph node map','Rusch · J Thorac Oncol','Nodal station anatomy for N-staging and CTV naming.','q:Rusch IASLC lymph node map proposal revision TNM',True),
  (2013,'CT atlas for the IASLC lymph node map: a radiation oncologist perspective','Lynch · Pract Radiat Oncol','Station 1–11 CT borders used for nodal and post-op CTVs (ANZ authors).','pm:24674264',True),
  (2022,'Lung ART: PORT vs no PORT for resected pN2 NSCLC (protocol CTV rules in supplement)','Le Péchoux · Lancet Oncol','rCTV + 1 cm with station limits; no DFS benefit, more cardiopulmonary toxicity.','pm:34919827',False),
  (2015,'Atlas of thoracic lymph-node delineation (oesophageal cancer, IASLC stations)','Huang · Radiother Oncol','CT station-by-station atlas; useful for lung too.','pm:26142269',False),
  (2010,'Evidence-based CTV for post-operative RT in NSCLC (Lung ART)','Spoelstra · IJROBP','Bronchial stump, hilum and station selection by lobe.','q:Spoelstra evidence-based approach clinical target volume postoperative radiotherapy non-small cell lung cancer',False),
  (2004,'Hemithorax RT after extrapleural pneumonectomy','Senan · Lung Cancer','Historical mesothelioma post-EPP volumes.','pm:15261442',False),
  (2011,'ITMIG definitions and policies: radiation therapy for thymic tumours','Gomez · J Thorac Oncol','Thymoma/thymic carcinoma CTV after resection.','q:ITMIG standard definitions policies thymic malignancies radiation therapy Gomez',False),
 ]),
 ('Thoracic OARs',[
  (2011,'RTOG thoracic OAR atlas: lung, proximal bronchial tree, oesophagus, cord, ribs, brachial plexus','Kong · IJROBP','Standard thoracic OAR definitions.','pm:20934273',True),
  (2008,'Brachial plexus contouring (RTOG atlas)','Hall · IJROBP','Scalene-based method from neural foramina to first rib.','pm:18448267',True),
  (2012,'Validating the RTOG brachial plexus atlas','Yi · IJROBP','Atlas vs MRI anatomy.','pm:21536393',False),
  (2023,'STOPSTORM: critical structures for cardiac radioablation','Balgobind · Radiother Oncol','Cardiac substructures and OARs for STAR.','pm:37827279',False),
 ]),
]),
('hn','Head & neck','Nodal levels, primary CTV, NPC, post-op, PNI, cutaneous SCC, re-irradiation and OARs.',[
 ('Neck nodes and primary CTV',[
  (2014,'Delineation of neck node levels: 2013 update (DAHANCA, EORTC, HKNPCSG, NCIC, RTOG, TROG)','Grégoire · Radiother Oncol','The nodal atlas: levels I–X with borders. Start here.','pm:24183870',True),
  (2018,'Delineation of the primary tumour CTV (CTV-P) in laryngeal, hypopharyngeal, oropharyngeal and oral cavity SCC','Grégoire · Radiother Oncol','The 5 + 5 mm CTV-P concept, edited for barriers.','pm:29180076',True),
  (2018,'Selection of target volumes: T and N (oral cavity, pharynx, larynx)','Grégoire · Oral Oncol','Which nodal levels to treat by site and stage.','pm:30527228',True),
  (2019,'Selection of lymph node target volumes: node-positive neck','Biau · Radiother Oncol','Level selection and margins for involved nodes / ENE.','q:Biau selection of lymph node target volumes for definitive head and neck radiation therapy 2019 update',True),
  (2006,'Proposal for the delineation of the nodal CTV in the node-positive and post-op neck','Grégoire · Radiother Oncol','Earlier node-positive guidance (superseded).','pm:16616387',False),
  (2003,'CT-based delineation of lymph node levels in the node-negative neck','Grégoire · Radiother Oncol','Original consensus (superseded by 2014).','pm:14644481',False),
  (2024,'Neck CTV for oral/oropharyngeal SCC based on nodal distribution','Liu · Radiother Oncol','Data-driven refinements to level borders.','pm:38490491',False),
  (2023,'Impact of consensus guidelines on primary CTV','Bollen · Radiother Oncol','How the 2018 guideline changes CTV-P.','pm:37739317',False),
 ]),
 ('Post-operative, PNI, skin and re-irradiation',[
  (2025,'ESTRO consensus: post-operative CTVs in oral cavity cancer','Evans · Radiother Oncol','Newest post-op guidance (tumour bed, flap, nodes).','pm:40925473',True),
  (2018,'Target delineation for post-operative H&N RT','Evans · Oral Oncol','Practical post-op approach.','pm:30409314',False),
  (2014,'Contouring guide for perineural invasion in H&N cancer','Ko · Pract Radiat Oncol','Cranial-nerve pathways for PNI CTV.','pm:25407876',True),
  (2019,'Trigeminal nerve contouring guidelines (PNI)','Biau · Radiother Oncol','V1–V3 branches to the skull base.','pm:30206021',True),
  (2020,'HNCIG post-operative RT for cutaneous SCC of the H&N','Porceddu · IJROBP','Indications, volumes, PNI and nodal levels for skin SCC.','pm:32289475',True),
  (2026,'Re-irradiation of recurrent HNSCC: international consensus','Biau · Lancet Oncol','Selection, volumes and cumulative dose.','pm:42372755',False),
 ]),
 ('Nasopharynx',[
  (2025,'NPC primary target delineation: CSTRO/CACA/CSCO/HNCIG/ESTRO/ASTRO guideline and atlas','Tang · Lancet Oncol','Newest: CTV margins, post-induction volumes, stepwise extension.','pm:40907526',True),
  (2025,'NPC neck target delineation: same consortium','Tang · Lancet Oncol','Neck CTV, equivocal nodes, level boundary modifications.','pm:40907527',True),
  (2018,'International guideline for CTV delineation in NPC','Lee · Radiother Oncol','The previous standard; still widely cited.','pm:29153464',False),
  (2025,'International NPC CTV by dose level','Lin · IJROBP','Dose-level CTV definitions.','pm:40419028',False),
  (2025,'International NPC consensus: volumes after induction chemotherapy','Fourati · Pract Radiat Oncol','Pre vs post-IC volumes.','pm:40146085',False),
  (2021,'Re-irradiation IMRT for recurrent NPC: consensus','Ng · IJROBP','Volumes and constraints for re-RT.','pm:33571626',False),
 ]),
 ('H&N OARs',[
  (2015,'CT-based delineation of OARs in the H&N region (DAHANCA, EORTC, GORTEC, HKNPCSG, NCIC, NRG, TROG)','Brouwer · Radiother Oncol','The standard H&N OAR atlas.','pm:26277855',True),
  (2011,'Delineation of swallowing OARs (DARS)','Christianen · Radiother Oncol','Pharyngeal constrictors, larynx, oesophageal inlet.','q:Christianen delineation of organs at risk involved in swallowing for radiotherapy treatment planning',False),
  (2020,'Global Harmonization Group: OAR delineation guidance','Mir · Radiother Oncol','Harmonised OAR names and definitions.','pm:32504762',False),
  (2019,'Muscles of mastication atlas','Hague · Radiother Oncol','Trismus-relevant OARs.','pm:30420234',False),
  (2019,'Brainstem substructures (nausea/vomiting)','Beddok · Radiother Oncol','Area postrema / dorsal vagal complex.','pm:30172454',False),
 ]),
]),
('cns','CNS','Glioma, glioblastoma, meningioma and skull base, brain metastases, neuro OARs.',[
 ('Gliomas',[
  (2023,'ESTRO-EANO guideline on target delineation and RT details for glioblastoma','Niyazi · Radiother Oncol 184:109663','Current GBM standard: cavity + enhancement, 15 mm CTV.','doi:10.1016/j.radonc.2023.109663',True),
  (2025,'ESTRO-EANO guideline for IDH-mutant WHO grade 2–3 diffuse glioma','Baumert · Radiother Oncol 202:110594','Lower-grade glioma volumes (T2/FLAIR-based).','q:ESTRO-EANO guideline on target delineation and radiotherapy for IDH-mutant WHO CNS grade 2 and 3 diffuse glioma',True),
  (2016,'ESTRO-ACROP target delineation of glioblastomas','Niyazi · Radiother Oncol','Previous version (20 mm CTV).','pm:26777122',False),
  (2019,'NRG brain tumour specialists: GBM contouring consensus','Kruser · J Neurooncol','US approach (two-phase vs single-phase).','pm:30888558',False),
 ]),
 ('Skull base, meningioma and metastases',[
  (2021,'ESTRO-ACROP target volume delineation of skull base tumours','Combs · Radiother Oncol','Pituitary, meningioma, craniopharyngioma, vestibular schwannoma, chordoma, chondrosarcoma.','pm:33309848',True),
  (2025,'DOTATATE PET in meningioma RT planning: guideline','Perlow · IJROBP','Using SSTR PET for meningioma GTV.','pm:39701546',False),
  (2026,'Skull-base chordoma target delineation consensus','McDonald · IJROBP','Chordoma GTV/CTV.','pm:42799736',False),
  (2018,'Consensus contouring for post-operative cavity SRS (brain metastases)','Soliman · IJROBP','Cavity, surgical tract, dural and bone-flap margins.','pm:29157748',True),
  (2010,'Hippocampal contouring atlas (RTOG 0933)','Gondi · IJROBP','Hippocampus on T1 MRI; avoidance zone +5 mm.','q:Gondi hippocampal-sparing whole-brain radiotherapy a how-to technique hippocampal contouring',True),
 ]),
 ('Neuro OARs',[
  (2018,'EPTN neuro-oncology contouring atlas (CT/MR)','Eekers · Radiother Oncol','Comprehensive brain OAR atlas (updated 2021, online).','pm:29548560',True),
  (2015,'Brain OAR atlas','Scoccianti · Radiother Oncol','Optic apparatus, cochlea, pituitary, hippocampus and more.','q:Scoccianti organs at risk in the brain and their dose-constraints in adults and in children a radiation oncologist guide for delineation',False),
 ]),
]),
('gi','GI','Oesophagus, stomach, pancreas, liver, rectum and anus.',[
 ('Upper GI',[
  (2015,'Expert consensus contouring guidelines for IMRT in oesophageal and GEJ cancer','Wu · IJROBP','GTV, CTV margins and nodal coverage by tumour location.','pm:26104943',True),
  (2021,'ESTRO-ACROP delineation of lymph-node areas in upper GI malignancies','Valentini · Radiother Oncol','Station borders for oesophagus, stomach, pancreas, biliary (+FALCON case).','pm:34547352',True),
  (2009,'EORTC-ROG: neoadjuvant RT volumes for GEJ and gastric adenocarcinoma','Matzinger · Radiother Oncol','Gastric/GEJ CTV by tumour site.','q:Matzinger EORTC-ROG expert opinion radiotherapy volume treatment guidelines neoadjuvant adenocarcinomas gastroesophageal junction stomach',False),
  (2012,'RTOG post-op CTV for pancreatic head cancer','Goodman · IJROBP','Pancreaticojejunostomy, coeliac, SMA, portal vein, aorta.','pm:22483737',True),
  (2019,'CTV atlas for biliary cancer including elective nodes','Bisello · Oncol Lett','CTV-T margins for intrahepatic, extrahepatic and gallbladder cancer; 10 mm vessel-surrogate nodal rules.','doi:10.3892/ol.2018.9774',True),
  (2017,'CTV in biliary carcinoma: systematic review of nodal involvement','Marinelli · Anticancer Res','Stations ≥5% by subsite; celiac and SMA <5%.','doi:10.21873/anticanres.11404',False),
  (2023,'Recurrence patterns and nodal CTV in resected perihilar cholangiocarcinoma','Park · ctRO','PV/CHA/CA +10 mm, LGA +15 mm, aorta 15/5/15 mm; covers 86% of regional relapses.','q:Park patterns of locoregional recurrences clinical target volume resected perihilar extrahepatic cholangiocarcinoma',False),
  (2020,'AGITG/TROG pancreatic SBRT guidelines','Oar · Pract Radiat Oncol','Australasian SBRT volumes and constraints.','pm:31761541',True),
  (2025,'NRG pancreatic dose-escalation contouring atlas','Sanford · IJROBP','Ablative pancreas volumes and OARs.','pm:39510320',False),
  (2014,'RTOG upper abdominal normal-organ contouring atlas','Jabbour · Pract Radiat Oncol','Liver, kidneys, stomach, bowel, duodenum.','pm:24890348',True),
 ]),
 ('Liver SBRT and MRI upper abdominal OARs',[
  (2020,'MRI-based upper abdominal organs-at-risk atlas','Lukovic · IJROBP','Hepatobiliary-phase and bSSFP plus MR-linac sequences; biliary tree on MRI. DICOM sets on econtour.org. Used in our liver SBRT OAR protocol.','pm:31953061',True),
  (2015,'Predictors of toxicity of SBRT to the central hepatobiliary tract','Osmundson · IJROBP','Defines cHBT: portal vein (splenic confluence to first bifurcation) + 15 mm; V40/V37.7 limits.','q:Predictors of toxicity associated with stereotactic body radiation therapy to the central hepatobiliary tract',True),
  (2017,'Central liver toxicity after SBRT: expanded analysis and nomogram','Toesca · Radiother Oncol','15 mm portal vein expansion confirmed as cHBT surrogate; limits for primary liver cancer.','pm:27865544',False),
  (2021,'HyTEC: radiation dose-volume effects for liver SBRT','Miften · IJROBP','Exclude GTV from liver; report absolute volumes; NTCP for liver and GI.','pm:29482870',False),
  (2022,'UK 2022 consensus on normal tissue constraints for SABR','Diez · Clin Oncol','Liver, luminal GI, bile duct and kidney limits for 3 and 5 fx; bony canal surrogate.','pm:35272913',True),
 ]),
 ('Rectum and anus',[
  (2016,'International consensus guidelines on CTV delineation in rectal cancer','Valentini · Radiother Oncol','Subsites (mesorectum, presacral, internal iliac, obturator, external iliac, inguinal, ischiorectal) and when to include them.','q:Valentini international consensus guidelines on clinical target volume delineation in rectal cancer',True),
  (2006,'Definition and delineation of CTV for rectal cancer','Roels · IJROBP','Original subsite review.','q:Roels definition and delineation of the clinical target volume for rectal cancer',False),
  (2009,'RTOG elective CTV for anorectal cancer atlas','Myerson · IJROBP','Anal and rectal elective nodal volumes.','pm:19117696',True),
  (2012,'AGITG contouring atlas and planning guidelines for IMRT in anal cancer','Ng · IJROBP','Australasian anal atlas: CTVA/B/C and inguinal borders.','pm:22401917',True),
  (2023,'Nordic (NOAC) elective CTV delineation in anal cancer','Nilsson · Acta Oncol','Smaller, data-driven elective volumes.','pm:37504978',False),
  (2026,'Inguinal CTV contouring in anal cancer','De Luca · Clin Transl Radiat Oncol','Inguinal node distribution vs atlases.','pm:41756143',False),
 ]),
]),
('gu','GU','Prostate, prostate bed, pelvic nodes, bladder, kidney and penis.',[
 ('Prostate and prostate bed',[
  (2018,'ESTRO-ACROP CT/MRI-based CTV of the prostate (EBRT)','Salembier · Radiother Oncol','Prostate and SV CTV on CT/MRI; ECE margin.','pm:29496279',True),
  (2010,'Radiographic and anatomic basis for prostate contouring errors (MRI vs CT)','McLaughlin · IJROBP','Teaching atlas of apex/base pitfalls. Pearls on our prostate page.','doi:10.1016/j.ijrobp.2009.02.019',True),
  (2023,'ESTRO-ACROP prostate bed delineation for post-op RT','Dal Pra · Clin Transl Radiat Oncol','Current prostate bed standard.','pm:37251620',True),
  (2023,'ESTRO-ACROP: macroscopic recurrence after prostatectomy','Dirix · Clin Transl Radiat Oncol','Treat whole bed; boost only with anatomical correlate.','pm:37808453',True),
  (2010,'RTOG consensus CTV for post-op prostate RT','Michalski · IJROBP','US prostate-bed atlas.','pm:19394158',False),
  (2008,'Post-prostatectomy RT consensus guidelines (FROGG, Australia)','Sidhom · Radiother Oncol','Australasian prostate-bed CTV.','pm:18514340',False),
  (2024,'MRI-guided RT for the prostate bed: consensus','Sritharan · IJROBP','Prostate bed on MRI / MR-linac.','pm:37633499',False),
 ]),
 ('Pelvic nodes and PSMA',[
  (2021,'NRG consensus pelvic lymph-node atlas for prostate cancer','Hall · IJROBP','Current nodal standard (10-step).','pm:32861817',True),
  (2024,'GFRU pelvic nodal CTV guideline','De Hertogh · IJROBP','French update to nodal volumes.','pm:37506982',False),
  (2015,'Pelvic node CTV guidelines (PIVOTAL)','Harris · IJROBP','UK trial volumes up to L4/5.','pm:26104940',False),
  (2021,'PSMA-PET lymph-node atlas for salvage RT','Schiller · Eur Urol Oncol','Where PSMA-positive nodes sit vs atlases.','pm:32451312',False),
  (2022,'PSMA-PET/CT node atlas vs NRG 2020','Vogel · Eur Urol Oncol','Coverage of PSMA nodes by NRG volumes.','pm:36280446',False),
  (2024,'PERYTON: PSMA-PET-based salvage CTV','Staal · IJROBP','Trial volumes in the PSMA era.','pm:37729971',False),
 ]),
 ('Bladder, kidney, penis and pelvic OARs',[
  (2016,'Bladder adjuvant RT CTV consensus (post-cystectomy)','Baumann · IJROBP','Pelvic sidewall and cystectomy bed CTV.','pm:27511849',True),
  (2022,'Updated adjuvant bladder RT guideline (IBIS)','Verghote · Pract Radiat Oncol','Update of the post-cystectomy volumes.','pm:35691550',False),
  (2026,'IROCK renal cell carcinoma SABR contouring','Dhar · IJROBP','Primary kidney SABR volumes.','pm:41580163',True),
  (2025,'InPACT: penile cancer nodal RT standardisation','Cooper · IJROBP','Inguinal/pelvic nodal volumes.','pm:40180061',False),
  (2012,'RTOG pelvic normal tissue contouring atlas (male and female)','Gay · IJROBP','Bladder, rectum, bowel bag, femoral heads, penile bulb.','pm:22483697',True),
 ]),
]),
('gyn','Gynae','Cervix (EBRT and brachytherapy), endometrium, vagina and vulva.',[
 ('External beam',[
  (2025,'Consensus CTVs for IMRT of intact cervical cancer: update','Fields · Pract Radiat Oncol','Newest intact cervix CTV (uterus, parametria, vagina, nodes).','pm:39547646',True),
  (2011,'Consensus guidelines for CTV delineation for IMRT of intact cervix','Lim · IJROBP','Previous standard; ITV margins for uterus.','pm:20472347',True),
  (2021,'NRG/RTOG consensus CTV for post-op endometrial and cervical cancer: update','Small · IJROBP','Current post-hysterectomy CTV.','pm:32905846',True),
  (2008,'Consensus CTV for IMRT in post-op endometrial and cervical cancer','Small · IJROBP','Original RTOG post-op atlas.','pm:18037584',False),
  (2016,'NRG consensus contouring for vulvar cancer','Gaffney · IJROBP','Vulva and inguinofemoral node CTV.','q:Gaffney consensus recommendations for radiation therapy contouring and treatment of vulvar carcinoma',True),
  (2010,'JCOG consensus pelvic nodal CTV (cervix)','Toita · Jpn J Clin Oncol','Japanese nodal borders.','pm:20133334',False),
  (2011,'JCOG consensus CTV for primary disease (intact cervix)','Toita · Jpn J Clin Oncol','Japanese primary CTV.','pm:21875938',False),
  (2016,'Pictorial atlas for intact cervix target delineation','Eminowicz · Pract Radiat Oncol','Image-based teaching atlas.','pm:27032573',False),
 ]),
 ('Brachytherapy',[
  (2005,'GEC-ESTRO (I): GTV, HR-CTV and IR-CTV in cervix brachytherapy (MRI)','Haie-Meder · Radiother Oncol','Origin of HR-CTV / IR-CTV.','pm:15763303',True),
  (2006,'GEC-ESTRO (II): 3D dose-volume parameters','Pötter · Radiother Oncol','D90, D2cc and EQD2 reporting.','doi:10.1016/j.radonc.2005.11.014',False),
  (2018,'EMBRACE II: outcomes and evolution of the target concept','Pötter · Clin Transl Radiat Oncol','EMBRACE II target concept (CTV-HR, CTV-IR, nodal) and dose aims.','pm:29594251',True),
  (2014,'CT- vs MR-based cervical brachytherapy CTV consensus','Viswanathan · IJROBP','HR-CTV on CT when MRI is unavailable.','pm:25304792',True),
  (2017,'CT-based HR-CTV recommendations for cervix IGBT','Ohno · J Radiat Res','Japanese CT-based HR-CTV.','pm:27837120',False),
  (2020,'GEC-ESTRO/ACROP target concept for vaginal cancer brachytherapy','Schmid · Radiother Oncol','Primary vaginal cancer targets.','pm:31874348',False),
  (2023,'GEC-ESTRO/ABS/CBG targets for vaginal recurrence','Kamrava · IJROBP','Recurrent endometrial/cervical cancer in the vagina.','pm:36191741',False),
  (2012,'ABS consensus: adjuvant vaginal cuff brachytherapy','Small · Brachytherapy','Cuff length and dose.','pm:22265439',False),
 ]),
]),
('heme','Haematology','ILROG involved-site RT (Hodgkin, nodal and extranodal NHL), myeloma and plasmacytoma.',[
 ('ILROG',[
  (2014,'ILROG: modern RT for Hodgkin lymphoma: field and dose','Specht · IJROBP','ISRT/INRT concepts, pre-chemo GTV, CTV, ITV.','pm:23790512',True),
  (2014,'ILROG: nodal non-Hodgkin lymphoma target definition and dose','Illidge · IJROBP','ISRT for aggressive and indolent nodal NHL.','pm:24725689',True),
  (2015,'ILROG: extranodal lymphomas field and dose','Yahalom · IJROBP','Organ-by-organ volumes (stomach, orbit, skin, CNS, bone, etc).','pm:25863750',True),
  (2018,'ILROG: solitary plasmacytoma and multiple myeloma','Tsang · IJROBP','Plasmacytoma GTV/CTV and doses.','q:Tsang radiation therapy for solitary plasmacytoma and multiple myeloma guidelines from the International Lymphoma Radiation Oncology Group',False),
 ]),
]),
('sarc','Sarcoma & skin','Extremity and retroperitoneal sarcoma, cutaneous SCC and PNI.',[
 ('Sarcoma',[
  (2011,'RTOG consensus GTV/CTV for pre-op RT of extremity STS','Wang · IJROBP','3 cm longitudinal, 1.5 cm radial, include suspicious oedema.','pm:21676552',True),
  (2015,'Pre-op RT for retroperitoneal sarcoma: international expert consensus','Baldini · IJROBP','RPS GTV/ITV/CTV/PTV and high-risk margin.','q:Baldini treatment guidelines for preoperative radiation therapy for retroperitoneal sarcoma preliminary consensus of an international expert panel',True),
 ]),
 ('Skin',[
  (2020,'HNCIG post-op RT for cutaneous SCC of the H&N','Porceddu · IJROBP','See H&N tab.','pm:32289475',True),
  (2014,'Perineural invasion contouring guide','Ko · Pract Radiat Oncol','See H&N tab.','pm:25407876',False),
  (2019,'Trigeminal nerve contouring guidelines','Biau · Radiother Oncol','PNI pathways for facial skin cancers.','pm:30206021',False),
  (2012,'Adjuvant nodal RT after lymphadenectomy for melanoma (ANZMTG 01.02 / TROG 02.01)','Burmeister · Lancet Oncol','Trial field definitions for parotid/neck, axilla and groin.','q:Burmeister adjuvant radiotherapy versus observation alone for patients at risk of lymph-node field relapse after therapeutic lymphadenectomy for melanoma',False),
 ]),
]),
('sbrt','SBRT & bone','Spine and non-spine bone SBRT, oligometastases.',[
 ('Spine and bone',[
  (2012,'ISRC: target volume definition for spinal SRS','Cox · IJROBP','The six-sector spine CTV rules.','pm:22608954',True),
  (2017,'Consensus contouring for post-operative spine SBRT','Redmond · IJROBP','Pre-op extent, epidural "donut", hardware.','pm:27843035',True),
  (2020,'Sacral metastases SBRT target delineation consensus','Dunne · Radiother Oncol','Sacral sector-based CTV.','q:Dunne international consensus recommendations for target volume delineation specific to sacral metastases and spinal stereotactic body radiation therapy',False),
  (2020,'Non-spine bone metastases SBRT: contouring practice patterns','Nguyen · Pract Radiat Oncol','Basis for non-spine bone CTV recommendations.','pm:32171852',True),
  (2022,'Deviation from spine SBRT contouring guidelines and outcome','Chen · Radiother Oncol','Why the sector rules matter.','pm:35667571',False),
 ]),
]),
('peds','Paediatrics','Craniospinal, paediatric CNS and solid tumours (mostly trial protocols).',[
 ('Paediatric',[
  (2018,'SIOPE guideline on craniospinal irradiation (target volumes and technique)','Ajithkumar · Radiother Oncol','CSI CTV: cribriform plate, temporal lobes, thecal sac.','q:Ajithkumar SIOPE brain tumour group consensus guideline on craniospinal target volume delineation',True),
  (2018,'Hippocampal sparing during craniospinal irradiation','Padovani · IJROBP','Feasibility and contouring.','pm:29485078',False),
  (2022,'Response-based RT for CNS germ cell tumours','Murphy · IJROBP','Whole-ventricular volumes.','pm:34990779',False),
  (2022,'Whole-ventricular RT: photon vs proton','Mak · Pediatr Blood Cancer','Ventricular CTV definition.','pm:35373903',False),
  (2023,'Inter-observer variation for high-risk neuroblastoma','Jazmati · Radiother Oncol','Why neuroblastoma volumes need peer review.','pm:36640946',False),
  (2023,'Dentofacial structures in paediatric RT: survey','Davey · Clin Transl Radiat Oncol','Teeth and jaw as OARs.','pm:37790584',False),
 ]),
]),
('general','General & online','Cross-site reviews, naming, and online atlases.',[
 ('Cross-site',[
  (2020,'Systematic review of contouring guidelines in radiation oncology','Lin · IJROBP','Catalogue of published guidelines by site.','pm:32311418',True),
  (2020,'Global Harmonization Group OAR guidance','Mir · Radiother Oncol','Harmonised OAR definitions.','pm:32504762',False),
 ]),
 ('Online atlases',[
  (None,'eContour: interactive contouring cases','econtour.org','Free case library tied to published guidelines.','https://econtour.org/',True),
  (None,'NRG Oncology contouring atlases','nrgoncology.org','RTOG/NRG atlases (breast, pelvis, H&N, GI, sarcoma).','https://www.nrgoncology.org/',False),
  (None,'ESTRO FALCON EduCases','estro.org','Contouring workshops and online cases linked to ESTRO guidelines.','https://www.estro.org/',False),
 ]),
]),
]
