# Site version, shown in every page header and at the foot of the home page.
#
# Format: MONTH.RELEASE[.PATCH]
#   - MONTH is the calendar month number (11 = November). Start again at .1 each new month (e.g. 12.1).
#   - RELEASE goes up by one for each normal update (new page, new section, content changes): 11.1 -> 11.2.
#   - PATCH is for small fixes (typos, a link, a single figure): 11.3 -> 11.3.1 -> 11.3.2.
# Bump VERSION and VERSION_DATE in every commit that changes the site, and add a line to HISTORY.

VERSION = '11.12'
VERSION_DATE = '23 Nov 2026'

HISTORY = [
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
