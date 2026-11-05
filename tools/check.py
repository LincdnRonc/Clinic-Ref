import sys, glob, os, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
from playwright.sync_api import sync_playwright
os.chdir(ROOT)
pages = sys.argv[1:] or sorted(glob.glob('*.html'))
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 390, 'height': 844})
    errs = []
    pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    pg.on('pageerror', lambda e: errs.append(str(e)))
    bad = []
    for f in pages:
        pg.goto((ROOT / f).as_uri()); pg.wait_for_timeout(250)
        info = pg.evaluate("()=>({w:document.documentElement.scrollWidth, chips:document.querySelectorAll('.chip').length, cards:document.querySelectorAll('.card').length, trials:document.querySelectorAll('.trial').length})")
        flag = '' if info['w'] <= 390 else '  <-- OVERFLOW'
        if flag: bad.append(f)
        print(f, info, flag)
    if pages and pages[0] != 'index.html':
        pg.goto((ROOT / pages[0]).as_uri()); pg.wait_for_timeout(300)
        pg.screenshot(path=str(ROOT / 'r1.png'))
        pg.fill('#q', 'Gy'); pg.wait_for_timeout(300)
        print('search hits for Gy', pg.eval_on_selector_all('.card:not(.hide)', 'e=>e.length'))
    pg.goto((ROOT / 'index.html').as_uri()); pg.wait_for_timeout(300); pg.screenshot(path=str(ROOT / 'r3.png'), full_page=True)
    print('errors', errs, 'overflow', bad)
    b.close()
