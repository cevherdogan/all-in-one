
import os, pathlib, re, sys
from datetime import datetime

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
ARTICLES = ROOT / "articles"

REPO_SLUG = "cevherdogan/all-in-one"

def parse_front_matter(text):
    t = text.lstrip()
    if not t.startswith('---'):
        return {}
    _, front, _ = t.split('---', 2)
    meta = {}
    for line in front.strip().splitlines():
        if ':' in line:
            k, v = line.split(':', 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if v.startswith('[') and v.endswith(']'):
                items = [i.strip().strip('"').strip("'") for i in v[1:-1].split(',') if i.strip()]
                meta[k] = items
            else:
                meta[k] = v
    return meta

def guess_lang(filename):
    mapping = {
        '.en.md': 'English', '.tr.md': 'Turkish', '.ar.md': 'Arabic',
        '.fa.md': 'Farsi', '.de.md': 'German', '.sv.md': 'Swedish',
        '.fr.md': 'French', '.el.md': 'Greek', '.ru.md': 'Russian'
    }
    for suf, name in mapping.items():
        if filename.endswith(suf):
            return name
    return 'Unknown'

def make_github_blob_url(path_rel):
    return 'https://github.com/{}/blob/main/{}'.format(REPO_SLUG, path_rel)

def make_public_html_url(meta, lang):
    slug = meta.get('slug','').strip()
    if not slug:
        return ''
    fname = 'en.html' if lang.lower().startswith('english') else 'tr.html'
    user, repo = REPO_SLUG.split('/')
    return 'https://{}.github.io/{}/articles/{}/{}'.format(user, repo, slug, fname)

def main():
    rows = []
    for p in sorted(CONTENT.glob('*.md')):
        rel = p.relative_to(ROOT).as_posix()
        meta = parse_front_matter(p.read_text(encoding='utf-8'))
        lang = guess_lang(p.name)
        title = meta.get('title', p.name)
        desc = meta.get('description', '').strip()
        blob = make_github_blob_url(rel)
        html = make_public_html_url(meta, lang)
        link_md = '[{}]({})'.format(p.name, blob)
        if html:
            link_md = '{} · [HTML]({})'.format(link_md, html)
        summary = desc if desc else '—'
        rows.append((p.name.lower(), '| `{}` | {} | **{}** — {} | {} |'.format(p.name, lang, title, summary, link_md)))

    rows.sort(key=lambda x: x[0])
    table_lines = ['| File | Language | Summary | Links |', '|------|----------|---------|-------|']
    table_lines += [r[1] for r in rows]

    last = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
    header = '# 📚 Content Index – All-in-One Project\n\n' +              'This directory contains bilingual guides and articles. The table below is **auto-generated**; do not edit manually.\n' +              '_Last updated: {}_\n\n'.format(last)
    footer = '\n\n## How to add content\n' +              '1) Create paired files like `my-topic.en.md` and `my-topic.tr.md` with front matter (title, description, slug, lang).\n' +              '2) Push to `main`. This README will auto-refresh via GitHub Actions.\n'

    md = header + '\n'.join(table_lines) + footer
    (ROOT / 'content' / 'README.md').write_text(md, encoding='utf-8')
    print('Generated content/README.md')

if __name__ == '__main__':
    main()
