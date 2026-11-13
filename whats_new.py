"""What's New page data. The weekly evidence digest appends to EVIDENCE; SITE is the site change log.

EVIDENCE entry: (date 'YYYY-MM-DD', site, tag, title, summary, url, source, affects)
  tag: 'practice' (practice-changing) | 'confirms' (confirms current practice) | 'watch'
  summary: one or two sentences in our own words (design, arms, headline result). No copied text.
  source: where it was seen (journal, the Limbic, theMednet, Quad Shot, conference)
  affects: list of (page, label) on this site that the item bears on; [] if none
SITE entry: (date, text, page or '')
"""
EVIDENCE = [
]
SITE = [
 ('2026-11-13', 'Auto-staging tab on the tumour-site pages (18 staging systems; also all together on the clinical scores page).', 'scores.html#staging'),
 ('2026-11-13', 'Clinical scores and nomograms page (Child-Pugh, ALBI, PSA doubling time, Roach, CTS5, SINS and more, with links to external tools); personal-resource disclaimer on every page.', 'scores.html'),
 ('2026-11-13', 'One contouring entry per site: each quick guide is now the "Quick reference" first tab of its full guide.', 'index.html#contouring'),
 ('2026-11-13', 'Site-wide search, "Contour now" view on every contouring guide, copy buttons on tables, pinned pages, calculators, consent numbers and doses-at-a-glance pages; installable as an app with offline use.', 'tools.html'),
 ('2026-11-13', 'Contouring pages renamed "contouring guides" and shown in the normal site layout; thorax quick guide and lung guide merged into one Thorax guide.', 'contouring/thorax.html'),
 ('2026-11-13', 'New full contouring guides: breast, gynae, anal canal, spine and bone SBRT, CNS, head and neck, lymphoma ISRT, bladder.', 'index.html#contouring'),
 ('2026-11-12', 'New full contouring guides: lung (now Thorax), biliary, pancreas and stomach, oesophagus and GOJ. Phase 2 exam summary section added.', 'index.html#contouring'),
]
