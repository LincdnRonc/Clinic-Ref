"""Rebuild pdf_index.json from a recursive listing of OneDrive "01 Contouring Guidelines".

Usage: python3 tools/pdf_index.py listing.json
listing.json = the device_list_dir(recursive) result: {"entries":[{name,type,size},...]}.
Only file names, folders and sizes are stored; the PDFs themselves stay in OneDrive.
"""
import json, re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = ('Contouring Software & Tools',)
EXCLUDE_FILES = {'Kirkland.pdf'}           # not a guideline: keep out of the index
TITLES = {   # opaque file names -> titles (read from page 1)
 'nihms176272.pdf': '2010 Red J Hippocampal-sparing whole brain RT: a how-to technique (Gondi)',
 'nihms50816.pdf': '2008 Red J Consensus CTV for postoperative pelvic IMRT in endometrial and cervical cancer (Small)',
 'nihms651052.pdf': '2014 PRO RTOG upper abdominal normal organ contouring guidelines (Jabbour)',
 'NIHMS349403-supplement-02.pdf': 'RTOG female pelvis normal tissue contouring atlas (supplement)',
 '1-s2.0-S0167814026005499-main.pdf': '2026 Green J How to optimise prostate SBRT: ESTRO clinical practice consensus (Draulans)',
 'Anatomy.pdf': 'Anatomy curriculum notes (2019)',
}
DOIS = {'nihms176272.pdf': 'doi:10.1016/j.ijrobp.2010.01.039', 'nihms50816.pdf': 'doi:10.1016/j.ijrobp.2007.09.042',
        'nihms651052.pdf': 'doi:10.1016/j.prro.2013.06.004'}
def main(path):
    d = json.load(open(path))
    if isinstance(d, list): d = json.loads(d[0]['text'])
    out = []
    for e in d['entries']:
        n = e['name']
        if e['type'] != 'file' or not n.lower().endswith('.pdf'): continue
        parts = n.split('/')
        fn = parts[-1]
        if parts[0] in EXCLUDE_DIRS or fn in EXCLUDE_FILES: continue
        if re.search(r'\(\d\)\.pdf$', fn, re.I): continue          # duplicate downloads
        if fn in ('s.pdf', '3093_001.pdf', '1-s2.0-S0360301619344773-main.pdf'): continue  # no readable text
        top = parts[0] if len(parts) > 1 else 'General & Multi-site'
        sub = '/'.join(parts[1:-1])
        out.append({'top': top, 'sub': sub, 'file': fn, 'path': n, 'mb': round(e.get('size', 0)/1e6, 1),
                    'title': TITLES.get(fn, ''), 'link': DOIS.get(fn, '')})
    out.sort(key=lambda x: (x['top'], x['sub'], x['file'].lower()))
    (ROOT/'pdf_index.json').write_text(json.dumps(out, indent=0, ensure_ascii=False))
    print(len(out), 'PDFs')
if __name__ == '__main__': main(sys.argv[1])
