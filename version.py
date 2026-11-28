# Site version, shown in every page header and at the foot of the home page.
#
# Format: MONTH.RELEASE[.PATCH]
#   - MONTH is the calendar month number (11 = November). Start again at .1 each new month (e.g. 12.1).
#   - RELEASE goes up by one for each normal update (new page, new section, content changes): 11.1 -> 11.2.
#   - PATCH is for small fixes (typos, a link, a single figure): 11.3 -> 11.3.1 -> 11.3.2.
# Bump VERSION and VERSION_DATE in every commit that changes the site, and add a line to HISTORY.

VERSION = '11.28.1'
VERSION_DATE = '28 Nov 2026'

HISTORY = [
    ('11.28.1', '28 Nov 2026', 'Request forms: signature pad restored, with an option to print "Electronically signed by" instead.'),
    ('11.28', '28 Nov 2026', 'Request forms: "Electronically signed by" field replaces the signature pad; requesting doctor moved to the bottom of the PDF; copies-to (cc) section; more fields (Medicare expiry, concession card, health fund, hospital status, interpreter, results phone/fax, medicines, LMP, mobility, infection precautions, anticoagulants, image-guided procedure).'),
    ('11.27.1', '28 Nov 2026', 'Tools icon added to the quick-launch bar on every page (jumps to the Tools section of the home page).'),
    ('11.27', '28 Nov 2026', 'New Tools page: Request forms (generic pathology and radiology / nuclear medicine requests, with My details, signature pad and Generate PDF).'),
    ('11.26.1', '28 Nov 2026', 'Access log: deploy also reads ACCESS_LOG_URL when saved as an Actions variable rather than a secret.'),
    ('11.26', '28 Nov 2026', 'Access log: name box on the password screen (remembered per device); each login, and each return visit after 30 minutes, is recorded to a Google Sheet when the ACCESS_LOG_URL secret is set (tools/access_log.js, tools/access_log.gs).'),
    ('11.25.2', '28 Nov 2026', 'Oral boards tab: source and caveat line under the heading removed.'),
    ('11.25.1', '28 Nov 2026', 'Trial tables tab: source and caveat line under the heading removed.'),
    ('11.25', '28 Nov 2026', 'Rad Onc Tables (Estes) added: new Trial tables tab on each tumour-site page (about 980 key studies routed by site, with need-to-know, recent and also-in-Key-trials tags, filter box, details on tap) and new Oral boards tab on each Phase 2 exam-summary page (about 380 case rows: workup, treatment, sim, dose, fields, constraints, follow-up). Imported by tools/estes_import.py into data/estes.json.'),
    ('11.24', '26 Nov 2026', 'Clinic links: new Clinical tools tab (Mednet, UpToDate, eviQ, Therapeutic Guidelines, CIAP, OpenEvidence, MDCalc, NCCN, ESMO, ASTRO, drug interaction checkers, eContour, NRG atlases, Radiopaedia, trial registries).'),
    ('11.23.7', '26 Nov 2026', 'Home page: Phase 2 exam summary cards removed; exam pages now reached from the sidebar menu only.'),
    ('11.23.6', '26 Nov 2026', 'Contouring guides: quick-launch icons (including Log out) added to the header, and the fixed "Full guide · Nov 2026" label replaced with the site version.'),
    ('11.23.5', '26 Nov 2026', 'Log out icon added at the right-hand end of the quick-launch bar (clears the remembered password and returns to the login screen).'),
    ('11.23.4', '25 Nov 2026', 'Guideline PDFs page: Google Scholar search links replaced with direct PubMed (PMID) links where verified, otherwise an exact-title PubMed search; protocols, books and departmental documents marked Not on PubMed.'),
    ('11.23.3', '25 Nov 2026', 'Floating Share button (link and QR code) removed from all pages; site is for personal use only.'),
    ('11.23.2', '25 Nov 2026', "Clinic links, Radiology: St Vincent's VueMotion link replaced with the onsite SVH PACS portal (SVH network only, no 2FA)."),
    ('11.23.1', '25 Nov 2026', "Clinic links, Radiology: St Vincent's Imaging (VueMotion) PACS portal added (no 2FA needed onsite)."),
    ('11.23', '25 Nov 2026', 'Clinic links: star (☆) any radiology, pathology or forms link to add it to a Favourites box at the top of its tab; saved in this browser.'),
    ('11.22', '25 Nov 2026', 'New Tools page: My weekly roster (Week A/B sessions with this week\'s MDTs, week navigation, choice of MDTs, full Kinghorn MDT planner).'),
    ('11.21', '24 Nov 2026', 'IBTR! 2.0 calculator built into Clinical scores, Breast (10-year in-breast recurrence with and without RT); reproduces the Evidencio tool on 33 test cases.'),
    ('11.20.3', '24 Nov 2026', 'T Pro and Heidi sign-in icons added to the quick-launch bar.'),
    ('11.20.2', '23 Nov 2026', 'Clinical scores, Breast: IBTR! 2.0 now links directly to the Evidencio calculators (with and without RT) instead of a web search.'),
    ('11.20.1', '23 Nov 2026', 'Exam summary, Hodgkin: classical HL subtypes laid out as nested lists (features under each subtype).'),
    ('11.20', '23 Nov 2026', 'Contouring-guide links now shown as solid call-out boxes; 32 key trials added from the Pocket RO gap check (paediatric COG and SIOP, gynae GOG/NSGO/SOLO-1/PAOLA-1, Hodgkin ECHELON-1/RATHL, DLBCL SWOG 8736/S0014, RTOG 0424, ARUBA, NRG-HN006, ARTSCAN III, RTOG 0912, RTOG 0618, EORTC 08941/08993, RTOG 9904, EORTC 22911, TE19, MSLT-II), each flagged check.'),
    ('11.19', '23 Nov 2026', 'Staging & risk merged into the Overview (or first) tab on every tumour-site page; #staging links still jump to the stagers.'),
    ('11.18', '23 Nov 2026', 'Contouring guides grouped by tumour site (major sites first, then minor, then reference and software) on the home page and in the sidebar; Search all pages removed from the sidebar menu.'),
    ('11.17', '23 Nov 2026', 'Tumour-site gaps from Pocket RO: new LABC & inflammatory tab (Nodes and PMRT), Osteosarcoma tab (Paediatric solid), Other benign tab (keloid, gynaecomastia, thyroid eye disease, orbital, desmoid, vertebral haemangioma); brainstem glioma, ovarian and penile additions.'),
    ('11.16.2', '23 Nov 2026', 'Share button: larger, QR icon, top centre (top right on phones), with an × to hide it for the rest of the browser session.'),
    ('11.16.1', '23 Nov 2026', 'Fix: Genesis quick icon image was not uploaded (*.png is git-ignored); now committed.'),
    ('11.16', '23 Nov 2026', 'Floating Share button on every page: link to the current page (optionally the open tab), Copy link, phone Share sheet, and a QR code generated on the device.'),
    ('11.15.1', '23 Nov 2026', 'Genesis quick icon now uses the GenesisCare image supplied by Lincoln.'),
    ('11.15', '23 Nov 2026', 'Header quick icons for Radiology, Pathology, Forms (Clinic links tabs) and Contacts, beside Keep, Tasks and Genesis.'),
    ('11.14.1', '23 Nov 2026', 'Fix: Staging & risk tabs lost their drop-down stagers after the 11.12 tab reorder (script was moved above the tabs); restored on all pages.'),
    ('11.14', '23 Nov 2026', 'New Principles & techniques section (8 pages): radiobiology, physics, imaging and IGRT, brachytherapy, protons and MR-guided RT, emergencies, simulation and set-up, statistics and trial design. Written in our own words, informed by Pocket Radiation Oncology 2nd ed. and cited sources.'),
    ('11.13', '23 Nov 2026', 'Overview tab added to every tumour-site page that did not open with an overview or general tab (38 pages): each management tab with its bottom line and a link, plus links to Staging & risk, Toxicity & consent, Key trials and the MDT matrix. Built from the page itself, so it updates when the page does; not indexed twice in search.'),
    ('11.12', '23 Nov 2026', 'Consistent tab order on every tumour-site page: overview or general tab (if any), then Staging & risk, management and planning tabs, Toxicity & consent, Key trials, MDT decision matrix, then eviQ, Guidelines and Exam notes.'),
    ('11.11.1', '23 Nov 2026', 'Fix: callout boxes at the top of contouring guides (e.g. Governing principles of this guide) showed empty; their text is back on all 16 affected guides.'),
    ('11.11', '23 Nov 2026', 'Interface clean-up: one collapsible Related line replaces the three cross-link bars; shorter page titles; eviQ, Guidelines and Exam notes tabs behind a More chip (revert with MORE_TABS = False in build.py); home page uses the sidebar on wide screens and the group buttons on phones; group colours only on card borders; Still to add moved to Site updates; contouring-guide badges and sources in a collapsible About this guide.'),
    ('11.10', '23 Nov 2026', 'Cleaner interface: removed descriptive blurbs (home-page tagline, hub-card descriptions now shown on hover, section summaries that only described what follows, exam topic lists, PDF-library and calculator intros); kept and shortened only the caveats and clinical bottom lines. Compact home-page cards.'),
    ('11.9', '23 Nov 2026', 'Prostate guide 2d.3b: erectile-structure anatomy and variants on MRI (neurovascular patterns, IPA course, accessory pudendal arteries, external sphincter, crura) with an original schematic, from Lee and Spratt, Lancet Oncol 2016.'),
    ('11.8', '23 Nov 2026', 'Prostate contouring guide section 2d: erectile function-sparing RT (NVB, IPA, penile bulb, crura delineation; ERECT SBRT constraints; conventional and moderate hypofractionation constraints; POTEN-C, ERECT, Spratt, ETS-IMRT trials).'),
    ('11.7.1', '23 Nov 2026', 'Teams meeting shortcut in the header quick-launch icons (link kept in a GitHub secret, added only to the password-protected site).'),
    ('11.7', '23 Nov 2026', "What's new: evidence digest 23 Nov 2026 (IRMA 5-year partial-breast results; single-dose vs five-fraction prostate SBRT pooled analysis)."),
    ('11.6', '20 Nov 2026', 'Removed the content added from Lincoln\'s 2025 summary in 11.4 (LD cards and the 14 tabs it created); Exam notes tabs now show the AS summary only.'),
    ('11.5', '19 Nov 2026', 'Exam notes tab on 44 tumour-site pages: the matching Phase 2 exam-summary tabs (AS + LD), copied at build time and not indexed twice in search.'),
    ('11.4', '19 Nov 2026', 'Phase 2 exam summary: content from Lincoln\'s own 2025 summary added where it is not already in the AS summary (cards tagged LD), plus new tabs: exam approach, viva framework, plan evaluation, doses and constraints, QA/CIED/IGRT, ovary, skin RT technique, angiosarcoma, H&N general, retinoblastoma, reirradiation, late toxicity, brachytherapy, pathogenesis.'),
    ('11.3', '19 Nov 2026', 'Life expectancy calculator (Australian Life Tables 2020–22, NCCN ±50% health adjustment, NCCN treatment thresholds) on the Prostate tab of Clinical scores; prostate page thresholds updated.'),
    ('11.2', '19 Nov 2026', 'Consent numbers moved from Tools into a Toxicity & consent tab on each tumour-site page.'),
    ('11.1', '19 Nov 2026', 'Version numbers introduced (replaces "Synthesised Nov 2026").'),
]
