"""Add private header shortcuts (the Teams meeting link) to every built page at deploy time only.

The repo is public, so the meeting link never lives in it. It is kept in the GitHub Actions secret
MEETING_URL and swapped in for the <!--MEETING_LINK--> placeholder that build.py puts in the
header quick-launch icons, just before tools/encrypt_site.js locks the site with the password.
Locally (no secret) this does nothing and the icon simply doesn't show.
For local testing: MEETING_URL='https://...' python3 tools/private_links.py
"""
import html, os, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
MARK = '<!--MEETING_LINK-->'
SKIP = {'.git', '.github', 'src', 'tools', 'node_modules', '_site'}


def icon(url):
    u = html.escape(url.strip(), quote=True)
    t = 'Teams meeting'
    return (f'<a href="{u}" target="_blank" rel="noopener" title="{t}" aria-label="{t}" class="al" '
            'style="display:flex;flex-direction:column;align-items:center;gap:2px;text-decoration:none;color:#5b6675;font-size:10px;line-height:1">'
            '<svg viewBox="0 0 24 24" width="30" height="30" aria-hidden="true" '
            'style="width:30px;height:30px;flex:none;border-radius:8px;padding:3px;box-sizing:border-box;background:#5b5fc7">'
            '<rect x="3.5" y="7" width="11" height="10" rx="2" fill="none" stroke="#fff" stroke-width="2"/>'
            '<path d="M14.5 10.5l5-2.8v8.6l-5-2.8z" fill="#fff"/></svg>'
            '<span>Meeting</span></a>')


def main():
    url = os.environ.get('MEETING_URL', '').strip()
    if not url:
        print('private links: MEETING_URL not set, pages left as is')
        return
    a, n = icon(url), 0
    for p in ROOT.rglob('*.html'):
        if SKIP & set(p.relative_to(ROOT).parts):
            continue
        t = p.read_text()
        if MARK in t:
            p.write_text(t.replace(MARK, a))
            n += 1
    print(f'private links: meeting icon added to {n} pages')


if __name__ == '__main__':
    main()
