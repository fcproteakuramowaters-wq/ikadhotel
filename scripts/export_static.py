#!/usr/bin/env python3
"""
Export dynamic Django pages to a static site (public/).

Usage: from project root run:
  python scripts/export_static.py

This will:
- crawl the site starting from /
- save HTML pages to public/<path>/index.html
- copy `static/` and `staticfiles/` into public/static/

Note: this script imports your Django settings; make sure virtualenv is active.
"""
import os
import re
import shutil
import sys
from urllib.parse import urljoin, urlparse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ikadhotel.settings')
import django

django.setup()

from django.test import Client


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PUBLIC = os.path.join(ROOT, 'public')
STATIC_SRC1 = os.path.join(ROOT, 'static')
STATIC_SRC2 = os.path.join(ROOT, 'staticfiles')
STATIC_DST = os.path.join(PUBLIC, 'static')


def ensure_public():
    if os.path.exists(PUBLIC):
        print('Removing existing public/ folder...')
        shutil.rmtree(PUBLIC)
    os.makedirs(PUBLIC, exist_ok=True)


def save_response(path, content):
    # normalize path to file path inside PUBLIC
    if path.endswith('/') or path == '':
        out_dir = os.path.join(PUBLIC, path.lstrip('/'))
        out_file = os.path.join(out_dir, 'index.html')
    else:
        # if path has an extension (like .html), keep it
        parsed = urlparse(path)
        out_path = parsed.path
        if out_path.endswith('/'):
            out_dir = os.path.join(PUBLIC, out_path.lstrip('/'))
            out_file = os.path.join(out_dir, 'index.html')
        else:
            out_dir = os.path.join(PUBLIC, os.path.dirname(out_path.lstrip('/')))
            filename = os.path.basename(out_path)
            if filename == '':
                filename = 'index.html'
            out_file = os.path.join(out_dir, filename)

    os.makedirs(out_dir, exist_ok=True)
    with open(out_file, 'wb') as f:
        f.write(content)
    print('Saved', out_file)


def copy_static():
    os.makedirs(STATIC_DST, exist_ok=True)
    for src in (STATIC_SRC1, STATIC_SRC2):
        if os.path.exists(src):
            print('Copying', src, '->', STATIC_DST)
            for item in os.listdir(src):
                s = os.path.join(src, item)
                d = os.path.join(STATIC_DST, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)


def extract_links(html, base_url='/'):
    # find hrefs
    urls = set()
    for match in re.findall(r'href=["\']([^"\']+)["\']', html, flags=re.IGNORECASE):
        # ignore anchors and mailto/tel
        if match.startswith('#') or match.startswith('mailto:') or match.startswith('tel:'):
            continue
        # ignore external links
        parsed = urlparse(match)
        if parsed.netloc and parsed.netloc != '':
            # external
            continue
        # make absolute path
        joined = urljoin(base_url, match)
        # keep only paths (strip query)
        joined = urlparse(joined).path
        if joined.endswith('.css') or joined.endswith('.js') or joined.endswith('.png') or joined.endswith('.jpg'):
            continue
        urls.add(joined)
    return urls


def crawl(start_paths=None, max_pages=300):
    client = Client()
    to_visit = list(start_paths or ['/'])
    visited = set()
    pages = 0

    while to_visit and pages < max_pages:
        path = to_visit.pop(0)
        if path in visited:
            continue
        print('Fetching', path)
        try:
            resp = client.get(path)
        except Exception as e:
            print('Error fetching', path, e)
            visited.add(path)
            continue

        if resp.status_code != 200:
            print('Skipping', path, 'status', resp.status_code)
            visited.add(path)
            continue

        save_response(path, resp.content)
        visited.add(path)
        pages += 1

        # find more links
        html = resp.content.decode('utf-8', errors='ignore')
        links = extract_links(html, base_url=path)
        for l in sorted(links):
            if l not in visited and l not in to_visit:
                to_visit.append(l)

    print('Crawled', pages, 'pages')


if __name__ == '__main__':
    ensure_public()
    copy_static()

    # initial paths to ensure main pages are included
    initial = [
        '/',
        '/hotels/victoria-island/',
        '/hotels/cooli-hotel/',
        '/about/',
        '/contact/',
        '/services/',
        '/portfolio/',
        '/blog/',
    ]

    crawl(start_paths=initial, max_pages=500)

    print('\nStatic export complete. The `public/` folder is ready for deployment (Vercel, Netlify, etc.).')
