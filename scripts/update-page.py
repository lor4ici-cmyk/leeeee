#!/usr/bin/env python3
"""Refresh static profile content, share metadata and cache keys."""
import hashlib
import html
import json
import re
from pathlib import Path
from urllib.parse import urljoin, urlsplit


def main():
    root = Path(__file__).resolve().parents[1]
    p = json.loads((root / 'profile.json').read_text())
    esc = html.escape
    title = p.get('seoTitle') or p['name']
    desc = p.get('seoDescription') or p['bio']
    url = p['siteURL']
    image = urljoin(url, p['seoImage'])
    links = []
    for link in p['links']:
        href = link.get('url', '').strip()
        if link.get('hidden') or not href:
            continue
        if not urlsplit(href).scheme and not href.startswith(('/', '#')):
            href = 'https://' + href
        href = urljoin(url, href)
        if urlsplit(href).scheme not in ('https', 'http') or not urlsplit(href).hostname:
            continue
        links.append(f'<a href="{esc(href)}"><span class="link-icon">{esc(link.get("icon") or "↗")}</span><span class="link-label">{esc(link.get("label") or "Ссылка")}</span></a>')
    for page in ('index.html', 'editor.html'):
        path = root / page
        text = escaped_tags(path.read_text(), esc, title, desc, url, image)
        if page == 'index.html':
            for pattern, value in ((r'(<h1 id="name">).*?(</h1>)', esc(p['name'])),
                                   (r'(<span id="handle">).*?(</span>)', esc(p.get('handle', ''))),
                                   (r'(<p id="bio">).*?(</p>)', esc(p['bio'])),
                                   (r'(<div id="links">).*?(</div>)', ''.join(links))):
                text = re.sub(pattern, lambda m: m[1] + value + m[2], text, flags=re.S)
        text = re.sub(r'((?:src|href)=")([\w.-]+\.(?:js|css))(?:\?v=[^\"]+)?"',
                      lambda m: m[1] + m[2] + '?v=' + hashlib.sha256((root / m[2]).read_bytes()).hexdigest()[:12] + '"', text)
        path.write_text(text)


def escaped_tags(text, esc, title, desc, url, image):
    text = re.sub(r'<title>.*?</title>', lambda _: f'<title>{esc(title)}</title>', text)
    for attr, key, value in [('name', 'description', desc), ('property', 'og:title', title),
                             ('property', 'og:description', desc), ('property', 'og:url', url),
                             ('property', 'og:image', image), ('name', 'twitter:title', title),
                             ('name', 'twitter:description', desc), ('name', 'twitter:image', image)]:
        text = re.sub(rf'<meta {attr}="{key}" content="[^"]*">',
                      lambda _: f'<meta {attr}="{key}" content="{esc(value)}">', text)
    return text


if __name__ == '__main__':
    main()
