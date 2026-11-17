"""Add private contacts (mobiles, staff names) to the built contacts.html at deploy time only.

The repo is public, so these numbers never live in it. They are kept in the GitHub Actions secret
CONTACTS_PRIVATE and added by .github/workflows/deploy.yml just before tools/encrypt_site.js locks
the site with the password. Locally (no secret) this does nothing.

CONTACTS_PRIVATE is a JSON list of rows:
  {"tab": "svh", "card": "Services", "service": "Vascular access", "number": "0414 783 785",
   "note": "Mobile", "replace": ""}
  tab      panel id on contacts.html: gc-svh, svh or centres
  card     card title in that tab; a new card is made at the end of the tab if none has that title
  replace  optional: the public row (by service name) that this row replaces
For local testing: CONTACTS_PRIVATE_FILE=path/to/file.json python3 tools/private_contacts.py
"""
import html, json, os, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / 'contacts.html'


def num(s):
    out = []
    for part in [x.strip() for x in s.split(' / ')]:
        d = re.sub(r'\D', '', part)
        if '@' in part:
            out.append(f'<a href="mailto:{html.escape(part)}">{html.escape(part)}</a>')
        elif re.fullmatch(r'\d{4,5}', part.replace(' ', '')) or re.fullmatch(r'\d{2}', d):
            out.append(f'<span class="ext">{html.escape(part)}</span>')
        else:
            if len(d) == 8:
                d = '02' + d
            tel = '+61' + d[1:] if d.startswith('0') else d
            out.append(f'<a href="tel:{tel}">{html.escape(part)}</a>')
    return ' / '.join(out)


def row(r):
    note = f'<br><span class="note">{html.escape(r["note"])}</span>' if r.get('note') else ''
    return f'<tr><td>{html.escape(r["service"])}{note}</td><td>{num(r["number"])}</td></tr>'


def main():
    raw = os.environ.get('CONTACTS_PRIVATE', '')
    if not raw and os.environ.get('CONTACTS_PRIVATE_FILE'):
        raw = pathlib.Path(os.environ['CONTACTS_PRIVATE_FILE']).read_text()
    if not raw.strip():
        print('private contacts: none set, page left as is')
        return
    rows = json.loads(raw)
    t = PAGE.read_text()
    added = 0
    for r in rows:
        m = re.search(rf'<section class="panel" id="p-{re.escape(r["tab"])}".*?</section>', t, re.S)
        if not m:
            sys.exit(f'private contacts: no tab "{r["tab"]}"')
        panel = m.group(0)
        title = html.escape(r['card'])
        cm = re.search(rf'<article class="card" data-title="{re.escape(title)}">.*?</article>', panel, re.S)
        if cm:
            card = cm.group(0)
            if r.get('replace'):
                card2, n = re.subn(rf'<tr><td>{re.escape(html.escape(r["replace"]))}(<br>.*?)?</td>.*?</tr>', lambda _: row(r), card, count=1, flags=re.S)
                if not n:
                    card2 = card.replace('</tbody>', row(r) + '</tbody>', 1)
            else:
                card2 = card.replace('</tbody>', row(r) + '</tbody>', 1)
            panel2 = panel.replace(card, card2, 1)
        else:
            new = (f'  <article class="card" data-title="{title}"><h3>{title}</h3><table class="contacts"><thead><tr>'
                   f'<th>Service</th><th>Number</th></tr></thead><tbody>{row(r)}</tbody></table></article>\n')
            panel2 = panel[:-len('</section>')] + new + '</section>'
        t = t.replace(panel, panel2, 1)
        added += 1
    # The "Not on this page" note is only for the public copy.
    t = re.sub(r'\s*<article class="card" data-title="Not on this page">.*?</article>', '', t, flags=re.S)
    PAGE.write_text(t)
    print(f'private contacts: {added} rows added')


if __name__ == '__main__':
    main()
