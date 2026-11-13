"""Wrap the hand-written contouring protocols (src/contouring/*.html) in the site shell.

The protocols are authored as standalone print-style documents (cover page, section.page
blocks with page footers). This turns each one into a normal site page: site header with
breadcrumb, search and section chips, the all-pages menu, one tab (panel) per protocol
section and one card per sub-heading, styled by assets/site.css + assets/protocol.css.

Source format A (most protocols): <section class="page" id="sN"> blocks, with optional
<div class="sechead" id="sN"> starting a section part-way through a page.
Source format B (rectal-long-course): a .masthead then a .wrap with <h2><span class="num">.
"""
import html, re
from bs4 import BeautifulSoup, NavigableString, Tag

SKIP_STYLE_IDS = {'qr-mobile', 'site-band'}


def _scale_px(css):
    # protocol CSS was tuned for a ~10 px print base; the site base is ~15.5 px
    return re.sub(r'font-size:\s*([\d.]+)px', lambda m: f'font-size:{float(m.group(1))*1.5:.1f}px', css)


def _keep_styles(soup):
    out = []
    for st in soup.find_all('style'):
        css = st.string or ''
        if st.get('id') in SKIP_STYLE_IDS:
            continue
        if '@page' in css or '.masthead' in css:   # the print stylesheet: replaced by protocol.css
            # keep page-specific pill colours (e.g. liver .p-liver) that live in the main sheet
            extra = re.findall(r'\.p-[\w-]+\{[^}]*\}', css)
            if extra:
                out.append('\n'.join(extra))
            continue
        out.append(_scale_px(css))
    return '\n'.join(out)


def _text(node):
    return re.sub(r'\s+', ' ', node.get_text(' ', strip=True)).strip()


def _short_label(num, title):
    t = re.sub(r'^Scenario [A-Z]\s*[—–-]\s*', '', title)
    t = re.split(r',| and | & |: | \(| — | – |;| for | after | with ', t)[0].strip()
    if len(t) > 34:
        t = t[:32].rsplit(' ', 1)[0] + '…'
    return f'{num} {t}'.strip() if num else t


def _wrap_tables(soup):
    for tb in soup.find_all('table'):
        if 'toc' in (tb.get('class') or []):
            for td in tb.select('td.pg, th.pg'):
                td.decompose()
        par = tb.parent
        if isinstance(par, Tag) and 'tw' in (par.get('class') or []):
            continue
        tb.wrap(soup.new_tag('div', attrs={'class': 'tw'}))


def _nodes_to_cards(nodes, panel_title, soup):
    """Group a flat list of nodes into site cards, splitting at top-level <h3>."""
    lede, cards, cur = [], [], None
    for n in nodes:
        if isinstance(n, NavigableString):
            if not n.strip():
                continue
            n = soup.new_string(str(n))
        if isinstance(n, Tag) and n.name == 'h3':
            cur = {'h3': n, 'body': []}
            cards.append(cur)
            continue
        if cur is None:
            # leading short paragraphs become the panel lede
            if isinstance(n, Tag) and n.name == 'p' and not cards and not lede_blocked(lede):
                lede.append(n)
                continue
            cur = {'h3': None, 'body': []}
            cards.append(cur)
        cur['body'].append(n)
    out = []
    for c in cards:
        h3 = c['h3']
        body = c['body']
        lbl_card = False
        if h3 is None:
            first = next((b for b in body if isinstance(b, Tag)), None)
            nested = first.find('h3') if isinstance(first, Tag) else None
            lbl = first.find(class_='lbl') if isinstance(first, Tag) and 'callout' in (first.get('class') or []) else None
            if nested is not None:
                title = _text(nested)
                h3html = ''
            elif lbl is not None:
                title = _text(lbl)
                lbl.decompose()
                h3html = f'<h3>{html.escape(title)}</h3>'
                first.unwrap()   # the card itself now carries the callout
                lbl_card = True
            else:
                title = panel_title
                h3html = f'<h3>{html.escape(title)}</h3>'
        else:
            title = _text(h3)
            h3html = f'<h3>{h3.decode_contents()}</h3>'
        dtitle = re.sub(r'^\d+(\.\d+)*[a-z]?\s+', '', title)
        inner = ''.join(str(b) for b in body)
        key = ' key' if (h3 is None and lbl_card) else ''
        out.append(f'<article class="card{key}" data-title="{html.escape(dtitle)}">{h3html}{inner}</article>')
    return ''.join(str(p) for p in lede), ''.join(out)


def lede_blocked(lede):
    return len(lede) >= 2


def _segments_a(soup):
    """Format A: split section.page blocks into protocol sections."""
    segs = [{'id': 'overview', 'nodes': [], 'head': None}]
    for sec in soup.select('section.page'):
        sid = sec.get('id')
        if sid and re.fullmatch(r's\d+[a-z]?', sid):
            segs.append({'id': sid, 'nodes': [], 'head': None})
        for ch in list(sec.children):
            if isinstance(ch, Tag):
                cls = ch.get('class') or []
                if 'foot' in cls:
                    continue
                if 'sechead' in cls:
                    cid = ch.get('id')
                    if cid and cid != segs[-1]['id']:
                        segs.append({'id': cid, 'nodes': [], 'head': None})
                    segs[-1]['head'] = ch
                    continue
            segs[-1]['nodes'].append(ch)
    return segs


def _segments_b(soup):
    """Format B (rectal atlas): split .wrap at top-level h2."""
    wrap = soup.select_one('div.wrap')
    segs = [{'id': 'overview', 'nodes': [], 'head': None}]
    n = 0
    for ch in list(wrap.children):
        if isinstance(ch, Tag) and ch.name == 'h2':
            n += 1
            num = ch.find(class_='num')
            sid = 's' + (num.get_text(strip=True) if num else str(n))
            segs.append({'id': sid, 'nodes': [], 'head': ch})
            continue
        if isinstance(ch, Tag) and 'foot' in (ch.get('class') or []):
            continue
        segs[-1]['nodes'].append(ch)
    return segs


def _head_parts(head):
    """Return (num, title, eyebrow, extra_html) from a .sechead div or a format-B h2."""
    if head is None:
        return '', '', '', ''
    h2 = head if head.name == 'h2' else head.find('h2')
    eyebrow = head.find(class_='eyebrow') if head.name != 'h2' else None
    num_el = h2.find(class_=['sectnum', 'num'])
    num = num_el.get_text(strip=True) if num_el else ''
    if num_el:
        num_el.extract()
    pills = [str(p.extract()) for p in h2.find_all(class_='pill')]
    title = _text(h2)
    return num, title, (_text(eyebrow) if eyebrow else ''), ' '.join(pills)


def convert(src_html, fname, long, short, data_site, tree_html, fonts, foot):
    soup = BeautifulSoup(src_html, 'html.parser')
    for s in soup.find_all('script'):
        s.decompose()
    for el in soup.select('#installChip, #iosHint, link[rel=manifest]'):
        el.decompose()
    extra_css = _keep_styles(soup)

    # related links from the old sticky navy bar
    related = []
    bar = soup.find('div', style=re.compile(r'position:\s*sticky'))
    if bar:
        for a in bar.find_all('a'):
            if 'index.html' in (a.get('href') or '') and a.get('href', '').rstrip('#').endswith('index.html'):
                continue
            related.append(f'<a href="{a.get("href")}">{html.escape(_text(a))}</a>')
        bar.decompose()

    mast = soup.select_one('.masthead')
    sub = mast.select_one('.sub') if mast else None
    pills = mast.select_one('.pillrow') if mast else None
    meta = mast.select_one('.meta') if mast else None
    eyebrow = mast.select_one('.eyebrow') if mast else None
    if mast:
        mast.extract()

    _wrap_tables(soup)
    fmt_a = bool(soup.select('section.page'))
    segs = _segments_a(soup) if fmt_a else _segments_b(soup)

    panels = []
    for seg in segs:
        wrapped = seg['nodes']
        if seg['id'] == 'overview':
            title, label = 'Overview', 'Overview'
            lede_html = (f'<p class="lede">{sub.decode_contents()}</p>' if sub else '')
            extra = ''
            if pills:
                extra += f'<div class="pillrow">{pills.decode_contents()}</div>'
            if meta:
                extra += f'<p class="note">{meta.decode_contents()}</p>'
            lede2, cards_html = _nodes_to_cards(wrapped, 'Overview', soup)
            head_html = f'<h2>{html.escape(long)}</h2>{lede_html}{lede2}{extra}'
            eb = _text(eyebrow) if eyebrow else ''
            if eb:
                head_html = f'<p class="eyebrow">{html.escape(eb)}</p>' + head_html
        else:
            num, title, eb, pill_html = _head_parts(seg['head'])
            if not title:
                title = seg['id']
            label = _short_label(num, title)
            lede2, cards_html = _nodes_to_cards(wrapped, title, soup)
            numhtml = f'<span class="sectnum">{html.escape(num)}</span>' if num else ''
            head_html = (f'<p class="eyebrow">{html.escape(eb)}</p>' if eb else '') + \
                f'<h2>{numhtml}{html.escape(title)} {pill_html}</h2>' + \
                (f'<div class="lede">{lede2}</div>' if lede2 else '')
            if not cards_html.strip():
                continue
        panels.append(
            f'<section class="panel" id="p-{seg["id"]}" data-tab="{seg["id"]}" data-label="{html.escape(label)}"'
            f'{"" if not panels else " hidden"}>\n  <div class="panel-head">{head_html}<div class="jump"></div></div>\n  {cards_html}\n</section>')

    tree_rel = re.sub(r'href="(?!https?:|#|\.\./)', 'href="../', tree_html)
    rel = (' · '.join(related))
    xref = f'<p class="xref"><b>Related:</b> {rel}</p>' if rel else ''
    return f'''<!DOCTYPE html>
<html lang="en-AU" data-site="{data_site}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(long)}</title>
{fonts}
<link rel="stylesheet" href="../assets/site.css">
<link rel="stylesheet" href="../assets/protocol.css">
<style>{extra_css}</style>
</head>
<body class="proto">
<header class="top">
  <div class="top-inner">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a> › <a href="../index.html#contouring">Contouring</a> › <span>{html.escape(long)}</span></nav>
    <div class="title-row">
      <h1>{html.escape(short)} <span>Contouring protocol</span></h1>
      <div class="meta">Full protocol · Nov 2026</div>
    </div>
    <form class="search" role="search" id="searchForm">
      <label for="q" class="note" style="position:absolute;left:-9999px">Search this protocol</label>
      <input id="q" type="search" placeholder="Search this protocol: border, margin, dose, trial" autocomplete="off">
      <button type="button" id="clear">Clear</button>
    </form>
    <nav class="chips" role="tablist" aria-label="Sections" id="chips"></nav>
  </div>
</header>
<div class="layout">
<aside class="side">{tree_rel}</aside>
<main id="main">
{xref}
<div class="empty" id="empty">No cards match. Try a shorter term such as a structure, a margin (5 mm) or a trial name.</div>
{''.join(panels)}
</main>
</div>
{foot}
<script src="../assets/site.js"></script>
</body>
</html>
'''
