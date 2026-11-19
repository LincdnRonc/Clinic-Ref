"""Add the extra content from Lincoln's own Phase 2 summary (2025 'Super Summary', PDF) to the exam-summary pages.

Usage:  python3 tools/ld_summary.py
Reads tools/ld_summary_data.json and writes it into src/exam-*.html between <!--ld:start--> and <!--ld:end-->
markers (re-running replaces what was added before, so it is safe after tools/super_summary.py regenerates the pages).

The data holds only material that is not already in the AS summary: each line of the PDF was compared with the
exam tab it belongs to and dropped if the same fact was already there. Cards are tagged "LD".
  page, tab   exam page and tab id the cards belong to
  new, label  True for a tab that does not exist in the AS summary (created at the end of the page, with this label)
  cards       [{title, html}]
"""
import json, re, html, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / 'tools' / 'ld_summary_data.json').read_text())

def card(c):
    t = html.escape(c['title'])
    return (f'  <article class="card ld" data-title="{t}">\n    <h3>{t} <span class="ldtag" title="From Lincoln\'s 2025 summary">LD</span></h3>\n'
            f'{c["html"]}\n  </article>\n')

def main():
    pages = {}
    for d in DATA: pages.setdefault(d['page'], []).append(d)
    for page, items in pages.items():
        p = ROOT / 'src' / page
        s = p.read_text()
        s = re.sub(r'<!--ld:start-->.*?<!--ld:end-->\n?', '', s, flags=re.S)
        for d in items:
            block = '<!--ld:start-->\n' + ''.join(card(c) for c in d['cards']) + '<!--ld:end-->\n'
            if d['new']:
                lab = html.escape(d['label'])
                block = (f'<!--ld:start-->\n<section class="panel" id="p-{d["tab"]}" data-tab="{d["tab"]}" data-label="{lab}" hidden>\n'
                         f'  <div class="panel-head">\n    <h2>{lab}</h2>\n    <p class="lede">From Lincoln\'s 2025 summary (not in the AS summary).</p>\n    <div class="jump"></div>\n  </div>\n'
                         + block.replace('<!--ld:start-->\n', '').replace('<!--ld:end-->\n', '') + '</section>\n<!--ld:end-->\n')
                s = s.rstrip('\n') + '\n' + block
            else:
                m = re.search(rf'<section class="panel" id="p-{re.escape(d["tab"])}"[^>]*>.*?(?=</section>)', s, re.S)
                if not m: raise SystemExit(f'tab {d["tab"]} not found in {page}')
                s = s[:m.end()] + block + s[m.end():]
        p.write_text(s)
    print(f'{len(DATA)} tabs, {sum(len(d["cards"]) for d in DATA)} cards on {len(pages)} pages')

if __name__ == '__main__':
    main()
