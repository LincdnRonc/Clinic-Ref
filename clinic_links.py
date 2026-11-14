# Clinic quick links: radiology and pathology login portals, forms and imaging references.
# Edit this file, then run build.py; it writes src/links.html.
# Each link: (name, url, note, tags). Tags: 'net' = NSW Health network only; 'new' = added Nov 2026 from provider
# websites, may need an account; 'check' = URL not confirmed by the provider.
# Do not put usernames, patient IDs or search queries in URLs: the repo is public.

TABS = [
 ('radiology', 'Radiology', 'Referrer image and report portals. Each opens in a new tab at the provider login.', [
  ('Most used', '', [
   ('I-MED Radiology', 'https://pacs.i-med.com.au/Portal/app#/', 'InteleConnect', ()),
   ('Sectra UniView', 'https://prod.nswcloud.sectra.com.au/UniView/#/', 'NSW Health PACS (Sectra cloud)', ()),
   ('Lumus Imaging', 'https://pacs.lumusimaging.com.au/Portal/app#/', 'Healius', ()),
   ('EIR', 'https://viewer.health.nsw.gov.au/pureweb/server/login.jsp', 'NSW Health Enterprise Image Repository', ()),
   ('Spectrum Medical Imaging', 'https://www.smipacs.com.au/Portal/app', '', ()),
   ('Bankstown Lidcombe Medical Imaging', 'https://img.blmedicalimaging.com.au/Portal/app', 'BLMI', ()),
   ('South West Radiology', 'https://images.southwestradiology.com.au/Portal/app#/', 'SWR', ()),
  ]),
  ('St George & Sutherland', '', [
   ('The Cross Radiology: IntelePACS', 'https://pacs.thecrossradiology.com.au/InteleBrowser/app', 'InteleBrowser', ()),
   ('The Cross Radiology: InteleConnect', 'https://pacs.thecrossradiology.com.au/Portal/app', 'Web portal', ()),
   ('Scan Medical', 'https://pacs.scanaptics.com.au/Portal/app#/', 'InteleConnect (Scanaptics)', ()),
   ('Scan Medical: InteleBrowser', 'https://pacs.scanaptics.com.au/InteleBrowser/app', '', ()),
   ('Shire Medical Imaging', 'https://img.shiremedicalimaging.com.au/Portal/app#/', 'Also Mittagong Medical Imaging', ()),
   ('Waratah Imaging', 'https://results.waratahimaging.com.au/Portal/app#/', '', ()),
   ('St George Private Nuclear Medicine', 'https://stgweb.stgeorgeprivatenucmed.com.au/portal/Login.aspx', 'SGP Nuc Med', ()),
   ('SNIG', 'https://pacs.snig.com.au/Portal/app', '', ()),
   ('Castlereagh Imaging (Kogarah)', 'https://mypatients.casimaging.com/Portal/app#/', 'Sonic Imaging; same login as IRG', ('new',)),
   ('Dr Glenn & Partners (Kogarah, Rockdale)', 'https://pacs.drgp.com.au/Portal/app', 'May be the same group as G&P under Wollongong', ('new',)),
   ('Focus Radiology (Engadine, Dapto, Liverpool)', 'https://pacs.focusrad.com.au/Portal', '', ('new', 'check')),
  ]),
  ('Liverpool & South West Sydney', '', [
   ('NIA Imaging', 'https://images.niaimaging.com.au/ZeroFP/', '', ()),
   ('Quantum Radiology', 'https://results.quantumradiology.com.au/sign-in', 'Also Nepean Imaging', ()),
   ('Synergy Radiology', 'https://pacs.synrad.com.au/Portal/app#/', 'Campsie and other Synergy sites', ()),
   ('Truescan (G&P / BLMI)', 'https://pacs.truescan.com.au/Portal/app#/', '', ()),
   ('Clearview Medical Imaging Fairfield', 'https://pacs.cmifairfield.com.au/Portal/app', '', ('new',)),
   ('Oran Park Radiology', 'https://img.oranparkradiology.com.au/Portal/app', '', ('new',)),
  ]),
  ('Wollongong, South Coast & ACT', '', [
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
  ]),
  ('Sydney: other', '', [
   ('San Radiology & Nuclear Medicine', 'https://portal.sanradiology.com.au/webconnect/#/auth', 'Sydney Adventist Hospital', ()),
   ('Macquarie Medical Imaging', 'https://pacs.mqhealth.org.au/Portal/app#/', '', ()),
   ("St Vincent's Clinic Medical Imaging", 'https://pacs.svcmi.com.au/Portal/app#/', '', ()),
   ('Alfred & Mater Imaging', 'https://iwpacs.com.au/Portal/app#/', 'I-MED: Inner West and the Mater', ()),
   ('North Shore Radiology & Nuclear Medicine', 'https://imaging.northshoreradiology.com.au/Portal/app', 'NSRNM; MFA required', ('new',)),
   ('Sydney Imaging Specialists', 'https://pacs.sydneyimaging.com.au/Portal/app', '', ('new',)),
   ('Harbour Radiology', 'https://imaging.harbourradiology.com.au/Portal/app', '', ('new',)),
  ]),
 ]),
 ('pathology', 'Pathology', 'Results portals for referring doctors.', [
  ('Results portals', '', [
   ('MedWay', 'https://www.medway.com.au/Login/ReLogin', 'Laverty Pathology (Healius)', ()),
   ('Sonic Dx', 'https://www.sonicdx.com.au/#/login', 'Douglass Hanly Moir and other Sonic labs', ()),
   ('SEALS', 'http://vmsepat-mas001.nswhealth.net/sls/apl/dls/OMNI.UI.Ward.Main.cls?$AutoOpen=M-RE', 'NSW Health Pathology, South Eastern labs', ('net',)),
   ('4Cyte Pathology', 'https://4cyte.mocloud.com.au/rest/html/explorer_online/index.html#!/app', 'Medical-Objects Explorer Online', ()),
   ('Australian Clinical Labs', 'https://results.clinicallabs.com.au/patients', 'eResults Viewer', ()),
   ('NSW Health Pathology: results for clinicians', 'https://pathology.health.nsw.gov.au/services/healthcare-professionals/results/', 'How to get public pathology results electronically (information page)', ('new',)),
  ]),
 ]),
 ('forms', 'Forms', 'Referral forms.', [
  ('Forms', '', [
   ('Liverpool PET-CT referral form', 'https://www.swslhd.health.nsw.gov.au/Liverpool/PET%5Ccontent/pdf/PET%20CT%20Referral%20Form.pdf', 'PDF', ()),
   ('Liverpool Hospital MRI screening form', 'https://swslhd-intranet.sswahs.nsw.gov.au/Liverpool/Forms/MRI_Screening.pdf', 'PDF, for patients', ('net',)),
  ]),
 ]),
]

NOT_YET = ('Not added yet: Southern Radiology (Miranda, Hurstville; no public login URL found) and a NSW Health Citrix remote-access link '
           '(the link supplied was a Zoom meeting). Send the URLs to add them.')
