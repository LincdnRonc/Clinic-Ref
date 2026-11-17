# Clinic quick links: radiology and pathology login portals, forms and imaging references.
# Edit this file, then run build.py; it writes src/links.html.
# Each link: (name, url, note, tags). Tags: 'net' = NSW Health network only; 'new' = added Nov 2026 from provider
# websites, may need an account; 'check' = URL not confirmed by the provider.
# Do not put usernames, patient IDs or search queries in URLs: the repo is public.

TABS = [
 ('radiology', 'Radiology', 'Referrer image and report portals, A to Z. Each opens in a new tab at the provider login.', [
  ('Radiology portals', '', [
   ('I-MED Radiology', 'https://pacs.i-med.com.au/Portal/app#/', 'InteleConnect', ()),
   ('Sectra UniView', 'https://prod.nswcloud.sectra.com.au/UniView/#/', 'NSW Health PACS (Sectra cloud)', ()),
   ('Lumus Imaging', 'https://pacs.lumusimaging.com.au/Portal/app#/', 'Healius', ()),
   ('EIR', 'https://viewer.health.nsw.gov.au/pureweb/server/login.jsp', 'NSW Health Enterprise Image Repository', ()),
   ('Spectrum Medical Imaging', 'https://www.smipacs.com.au/Portal/app', '', ()),
   ('Bankstown Lidcombe Medical Imaging', 'https://img.blmedicalimaging.com.au/Portal/app', 'BLMI', ()),
   ('South West Radiology', 'https://images.southwestradiology.com.au/Portal/app#/', 'SWR', ()),
   ('The Cross Radiology: IntelePACS', 'https://pacs.thecrossradiology.com.au/InteleBrowser/app', 'InteleBrowser', ()),
   ('The Cross Radiology: InteleConnect', 'https://pacs.thecrossradiology.com.au/Portal/app', 'Web portal', ()),
   ('Scan Medical', 'https://pacs.scanaptics.com.au/Portal/app#/', 'InteleConnect (Scanaptics)', ()),
   ('Scan Medical: InteleBrowser', 'https://pacs.scanaptics.com.au/InteleBrowser/app', '', ()),
   ('Shire Medical Imaging', 'https://img.shiremedicalimaging.com.au/Portal/app#/', 'Also Mittagong Medical Imaging', ()),
   ('Waratah Imaging', 'https://results.waratahimaging.com.au/Portal/app#/', '', ()),
   ('St George Private Nuclear Medicine', 'https://stgweb.stgeorgeprivatenucmed.com.au/portal/Login.aspx', 'SGP Nuc Med', ()),
   ('SNIG', 'https://pacs.snig.com.au/Portal/app', '', ()),
   ('Castlereagh Imaging (Kogarah)', 'https://mypatients.casimaging.com/Portal/app#/', 'Sonic Imaging; same login as IRG', ('new',)),
   ('Dr Glenn & Partners (Kogarah, Rockdale)', 'https://pacs.drgp.com.au/Portal/app', 'May be the same group as G&P', ('new',)),
   ('Focus Radiology (Engadine, Dapto, Liverpool)', 'https://pacs.focusrad.com.au/Portal', '', ('new', 'check')),
   ('NIA Imaging', 'https://images.niaimaging.com.au/ZeroFP/', '', ()),
   ('Quantum Radiology', 'https://results.quantumradiology.com.au/sign-in', 'Also Nepean Imaging', ()),
   ('Synergy Radiology', 'https://pacs.synrad.com.au/Portal/app#/', 'Campsie and other Synergy sites', ()),
   ('Truescan (G&P / BLMI)', 'https://pacs.truescan.com.au/Portal/app#/', '', ()),
   ('Clearview Medical Imaging Fairfield', 'https://pacs.cmifairfield.com.au/Portal/app', '', ('new',)),
   ('Oran Park Radiology', 'https://img.oranparkradiology.com.au/Portal/app', '', ('new',)),
   ('Nowra Radiology', 'https://patients.nowra-radiology.com.au/Portal/app#/', '', ()),
   ('Canberra Imaging Group', 'https://cigonline.cig.com.au/sign-in', 'CIG Online; has Break Glass', ()),
   ('Qscan: InteleConnect', 'https://www.qscaniq.com.au/Portal/app#/', 'Qscan iQ', ()),
   ('Qscan Referrer Results', 'https://referrer.qscan.com.au', 'Zed portal: Qscan, South East Radiology, NCRG', ('new',)),
   ('South East Radiology', 'https://pacs.southeastradiology.com.au/Portal/app#/', 'SER (Qscan group)', ()),
   ('IMI / SMI', 'https://pacs.xray.com.au/Portal/app#/', 'Vision Xray Group', ()),
   ('Wollongong Diagnostics: IntelePACS', 'https://pacs.wollongongdiagnostics.com.au/InteleBrowser/app', 'InteleBrowser', ()),
   ('G&P', 'https://pacs.medical-imaging.com.au/Portal/app#/', '', ()),
   ('IRG (Illawarra Radiology Group)', 'https://mypatients.casimaging.com/Portal/app#/', 'Sonic Imaging; same login as Castlereagh', ()),
   ('PRP Diagnostic Imaging', 'https://pacs.prpimaging.com.au/Portal/app#/', '', ()),
   ('San Radiology & Nuclear Medicine', 'https://portal.sanradiology.com.au/webconnect/#/auth', 'Sydney Adventist Hospital', ()),
   ('Macquarie Medical Imaging', 'https://pacs.mqhealth.org.au/Portal/app#/', '', ()),
   ("St Vincent's Imaging (MyVue)", 'https://myvue.imaging.svhs.org.au/portal/WebLogin.aspx?ReturnUrl=%2fportal%2fdefault.aspx', "All St Vincent's imaging (SVHS), incl. St Vincent's Clinic", ()),
   ('Alfred & Mater Imaging', 'https://iwpacs.com.au/Portal/app#/', 'I-MED: Inner West and the Mater', ()),
   ('North Shore Radiology & Nuclear Medicine', 'https://imaging.northshoreradiology.com.au/Portal/app', 'NSRNM; MFA required', ('new',)),
   ('Sydney Imaging Specialists', 'https://pacs.sydneyimaging.com.au/Portal/app', '', ('new',)),
   ('Harbour Radiology', 'https://imaging.harbourradiology.com.au/Portal/app', '', ('new',)),
  ]),
 ]),
 ('pathology', 'Pathology', 'Results portals for referring doctors, A to Z.', [
  ('Results portals', '', [
   ('MedWay', 'https://www.medway.com.au/Login/ReLogin', 'Laverty Pathology (Healius)', ()),
   ('Sonic Dx', 'https://www.sonicdx.com.au/#/login', 'Douglass Hanly Moir and other Sonic labs', ()),
   ('SEALS', 'http://vmsepat-mas001.nswhealth.net/sls/apl/dls/OMNI.UI.Ward.Main.cls?$AutoOpen=M-RE', 'NSW Health Pathology, South Eastern labs', ('net',)),
   ('4Cyte.Med web results portal', 'https://app.4cyte.med', '4Cyte Pathology clinician portal and app', ('new',)),
   ('4Cyte: Medical-Objects web results', 'https://4cyte.mocloud.com.au/rest/html/explorer_online/index.html#!/app', 'Medical-Objects Explorer Online', ()),
   ('Australian Clinical Labs eResults', 'https://results.clinicallabs.com.au/', 'ACL eResults Viewer; MFA optional', ()),
   ('SydPath: medical practitioners', 'https://mediweb.stvincents.com.au/mediportal/htmls/login.php', "St Vincent's Pathology (Mediweb)", ('new',)),
   ('SydPath: hospitals and labs', 'https://sydpath-results.stvincents.com.au/', "St Vincent's Pathology hospital portal", ('new',)),
   ('NSW Health Pathology: results for clinicians', 'https://pathology.health.nsw.gov.au/services/healthcare-professionals/results/', 'How to get public pathology results electronically (information page)', ('new',)),
  ]),
 ]),
 ('forms', 'Forms', 'Referral and pathology request forms. PDF links open or download the form directly.', [
  ('I-MED Radiology request forms', 'i-med.com.au/resources/e-referrals/pdf', [
   ('I-MED standard image request', 'https://assets-us-01.kc-usercontent.com:443/0f1bf390-09c2-00ff-dbea-bab90e37fcfe/b7baf0a8-7cd7-4f54-8522-9e05f6fc6b9b/I-MED_Radiology_Editable_PDF_Imaging_Request_Form_0626.pdf', 'PDF, editable (June 2026)', ()),
   ('I-MED specialist MRI image request', 'https://assets-us-01.kc-usercontent.com:443/0f1bf390-09c2-00ff-dbea-bab90e37fcfe/eca5abb4-b864-4642-aa8c-863eba3e2f4a/VICT204_0626_Specialist_Referral_A4_Editable.pdf', 'PDF, editable (June 2026)', ()),
   ('I-MED prostate MRI request', 'https://assets-us-01.kc-usercontent.com:443/0f1bf390-09c2-00ff-dbea-bab90e37fcfe/f14cedab-ecc7-4f3b-9042-afb764e1b031/VICT183_0626_Multi_MRI_ProstateReferral_Editable.pdf', 'PDF, editable (June 2026)', ()),
   ('I-MED PET/CT image request (NSW)', 'https://assets-us-01.kc-usercontent.com:443/0f1bf390-09c2-00ff-dbea-bab90e37fcfe/9440104f-b337-46b7-8d28-89e3927ff07d/IMEDNSW462_0726_A4_PET_Request_Editable.pdf', 'PDF, editable (July 2026)', ()),
  ]),
  ('Lumus Imaging request form', 'lumusimaging.com.au', [
   ('Lumus Imaging request / referral A4', 'https://www.lumusimaging.com.au/assets/documents/LUMREF001-0922_Referral_A4-LR-V2.pdf', 'PDF (Sept 2022 version); also valid at other radiology providers', ()),
  ]),
  ("St Vincent's Hospital Sydney: medical imaging", 'svhs.org.au', [
   ("St Vincent's Medical Imaging: request an appointment", 'https://forms.svha.org.au/medical-imaging-booking/', 'Online booking page; no PDF request form is published, a copy of the referral is needed (svhs.mi@svha.org.au, 02 8382 1820)', ()),
  ]),
  ("St Vincent's Theranostics and Nuclear Medicine request forms", 'svhs.org.au/our-services/list-of-services/theranostics-and-nuclear-medicine/referral-information', [
   ("St Vincent's FDG PET/CT request", 'https://www.svhs.org.au/ArticleDocuments/3976/77386%20SVH%20PET%20CT%20Patient-Request-Interactive-Form%20%28Jan%202020%29%20%28002%29.pdf.aspx', 'PDF, interactive', ()),
   ("St Vincent's neuro PET/CT request", 'https://www.svhs.org.au/ArticleDocuments/3976/86183_StVincentsHospital-Neuro-PET-CT-Request-Interactive-2%20%28003%29.pdf.aspx', 'PDF, interactive', ()),
   ("St Vincent's PSMA PET request", 'https://www.svhs.org.au/ArticleDocuments/3976/73857-SVH-PSMA-Request-Interactive-Forms.pdf.aspx', 'PDF, interactive', ()),
   ("St Vincent's DOTATATE PET request", 'https://www.svhs.org.au/ArticleDocuments/3976/84998_StVincentsHospital-Dotatate-Request-Form-Interactive.pdf.aspx', 'PDF, interactive', ()),
   ("St Vincent's general nuclear medicine request", 'https://www.svhs.org.au/ArticleDocuments/3976/77386_SVH-NuclearMedicineRequest-InteractiveForm%20%28Jan%202020%29.pdf.aspx', 'PDF, interactive', ()),
  ]),
  ('PRP Diagnostic Imaging request forms', 'prpimaging.com.au', [
   ('PRP referrals: reorder and print', 'https://www.prpimaging.com.au/referrer/resources/referrals-reorder-print/', 'Web page', ()),
   ('PRP Hunter Urology request form', 'https://www.prpimaging.com.au/wp-content/uploads/2021/04/A4-HUNTER-UROLOGY-EDITABLE-DEC-2020-ED.pdf', 'PDF, editable (Dec 2020 version)', ('check',)),
   ('PRP Central Coast urology request form', 'https://www.prpimaging.com.au/wp-content/uploads/2021/04/A4-CC-URO-REF-DEC-2020-NT.pdf', 'PDF (Dec 2020 version)', ('check',)),
  ]),
  ('Laverty Pathology request forms', 'laverty.com.au', [
   ('Laverty online pathology request form (telehealth)', 'https://www.laverty.com.au/?p=1388', 'Web page with the fillable form; Laverty accepts any provider\'s request form', ()),
   ('Laverty telehealth eRequest form', 'https://cdn.intelligencebank.com/au/share/DXK30X/lk8v1/LBYJD/original/LAV_RF050_Telehealth_eRequests_Nov23_RE_2', 'PDF (Nov 2023 version)', ('check',)),
  ]),
  ('SydPath general pathology request forms', 'sydpath.com.au/request-forms', [
   ('SydPath A4 computer request form', 'https://sydpath.com.au/wp-content/uploads/2022/07/SydPath-A4-Fillable-Request-Form-A4-_-0722-V12.pdf', 'PDF, fillable', ()),
  ]),
  ('SydPath specialised pathology request forms', 'sydpath.com.au/request-forms', [
   ('SydPath anatomical pathology request form', 'https://sydpath.com.au/wp-content/uploads/2023/05/SydPath-Anatomical-Pathology-Request-Form.pdf', 'PDF', ()),
   ('SydPath anatomical pathology second opinion request form', 'https://sydpath.com.au/wp-content/uploads/2022/07/SydPath-Anatomical-Pathology-Second-Opinion-Request-Form.pdf', 'PDF', ()),
   ('SydPath molecular oncology NGS request form', 'https://sydpath.com.au/wp-content/uploads/2026/07/SydPath-MolecularOncology-SomaticTesting-Requestform-240726.pdf', 'PDF, somatic testing (July 2026 version)', ()),
   ('SydPath molecular haematology NGS request form', 'https://sydpath.com.au/wp-content/uploads/2025/07/SVH-SYDPATH-Molecular-Haematology-Request-Fillable-PDF-Form-v2.pdf', 'PDF, fillable', ()),
  ]),
  ('Imaging forms', '', [
   ('Liverpool PET-CT referral form', 'https://www.swslhd.health.nsw.gov.au/Liverpool/PET%5Ccontent/pdf/PET%20CT%20Referral%20Form.pdf', 'PDF', ()),
   ('Liverpool Hospital MRI screening form', 'https://swslhd-intranet.sswahs.nsw.gov.au/Liverpool/Forms/MRI_Screening.pdf', 'PDF, for patients', ('net',)),
  ]),
 ]),
]

NOT_YET = ('Not added yet: Southern Radiology (Miranda, Hurstville; no public login URL found) and a NSW Health Citrix remote-access link '
           '(the link supplied was a Zoom meeting). Send the URLs to add them.')
