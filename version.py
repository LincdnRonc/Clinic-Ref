# Site version, shown in every page header and at the foot of the home page.
#
# Format: MONTH.RELEASE[.PATCH]
#   - MONTH is the calendar month number (11 = November). Start again at .1 each new month (e.g. 12.1).
#   - RELEASE goes up by one for each normal update (new page, new section, content changes): 11.1 -> 11.2.
#   - PATCH is for small fixes (typos, a link, a single figure): 11.3 -> 11.3.1 -> 11.3.2.
# Bump VERSION and VERSION_DATE in every commit that changes the site, and add a line to HISTORY.

VERSION = '11.4'
VERSION_DATE = '19 Nov 2026'

HISTORY = [
    ('11.4', '19 Nov 2026', 'Phase 2 exam summary: content from Lincoln\'s own 2025 summary added where it is not already in the AS summary (cards tagged LD), plus new tabs: exam approach, viva framework, plan evaluation, doses and constraints, QA/CIED/IGRT, ovary, skin RT technique, angiosarcoma, H&N general, retinoblastoma, reirradiation, late toxicity, brachytherapy, pathogenesis.'),
    ('11.3', '19 Nov 2026', 'Life expectancy calculator (Australian Life Tables 2020–22, NCCN ±50% health adjustment, NCCN treatment thresholds) on the Prostate tab of Clinical scores; prostate page thresholds updated.'),
    ('11.2', '19 Nov 2026', 'Consent numbers moved from Tools into a Toxicity & consent tab on each tumour-site page.'),
    ('11.1', '19 Nov 2026', 'Version numbers introduced (replaces "Synthesised Nov 2026").'),
]
