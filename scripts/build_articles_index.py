# scripts/build_articles_index.py
import pathlib, re, html, json

ROOT = pathlib.Path(__file__).resolve().parents[1]
ART = ROOT / "articles"
OUT = ART / "index.html"

TITLE_RE = re.compile(r"^#\s+(.+)$", re.M)
TITLE_HTML_RE = re.compile(r"<title>(.*?)</title>", re.I | re.S)
FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.S)

def read(p: pathlib.Path) -> str:
    return p.read_text(encoding="utf-8", errors="ignore")

def load_meta_from_json(dirp: pathlib.Path):
    j = dirp / "meta.json"
    if j.exists():
        try:
            return json.loads(read(j))
        except Exception:
            return {}
    return {}

def load_front_matter(md_path: pathlib.Path):
    if not md_path.exists():
        return {}
    m = FM_RE.match(read(md_path))
    if not m:
        return {}
    block = m.group(1)
    meta = {}
    for line in block.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"\'')
    return meta

def find_title(dirp: pathlib.Path) -> str | None:
    md = dirp / "README.md"
    if md.exists():
        # front matter title?
        fm = load_front_matter(md)
        if "title" in fm:
            return fm["title"]
        # H1 fallback
        m = TITLE_RE.search(read(md))
        if m: return m.group(1).strip()
    for name in ("index.html", "en.html", "tr.html"):
        f = dirp / name
        if f.exists():
            m = TITLE_HTML_RE.search(read(f))
            if m: return re.sub(r"\s+", " ", m.group(1)).strip()
    return None

def find_summary(dirp: pathlib.Path) -> str | None:
    # meta.json or front matter summary
    fm = load_meta_from_json(dirp)
    if "summary" in fm: return fm["summary"]
    md = dirp / "README.md"
    if md.exists():
        fmm = load_front_matter(md)
        if "summary" in fmm: return fmm["summary"]
        # first paragraph after front matter / H1 as loose fallback
        txt = read(md)
        txt = FM_RE.sub("", txt, count=1)
        paras = [p.strip() for p in re.split(r"\n\s*\n", txt) if p.strip()]
        if paras:
            # strip markdown noise a bit
            s = re.sub(r"[*_#>`~-]+", "", paras[0])
            return re.sub(r"\s+", " ", s)[:180]
    return None

def find_thumb(dirp: pathlib.Path) -> str | None:
    fm = load_meta_from_json(dirp)
    if "thumb" in fm:
        return f"{dirp.name}/{fm['thumb']}"
    fmm = load_front_matter(dirp / "README.md")
    if "thumb" in fmm:
        return f"{dirp.name}/{fmm['thumb']}"
    for ext in ("webp", "jpg", "jpeg", "png"):
        f = dirp / f"thumb.{ext}"
        if f.exists():
            return f"{dirp.name}/{f.name}"
    return None

def find_href(dirp: pathlib.Path) -> str:
    for name in ("index.html", "en.html", "tr.html"):
        f = dirp / name
        if f.exists(): return f"{dirp.name}/{name}"
    return f"{dirp.name}/"

def main():
    if not ART.exists():
        print("No articles/ directory found; skipping."); return

    cards = []
    for sub in sorted([d for d in ART.iterdir() if d.is_dir() and not d.name.startswith(".")], key=lambda x: x.name.lower()):
        title = find_title(sub) or sub.name.replace("-", " ").title()
        href = find_href(sub)
        thumb = find_thumb(sub)
        summary = find_summary(sub) or ""
        cards.append({"title": title, "href": href, "thumb": thumb, "summary": summary})

    css = """
    body{font-family:ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Helvetica,Arial,sans-serif;margin:0;padding:32px;background:#0b0e14;color:#eaeef2}
    h1{font-size:28px;margin:0 0 16px}
    p.muted{color:#a9b4c0;margin:0 0 24px}
    .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:18px}
    .card{background:#121722;border:1px solid #1f2633;border-radius:16px;overflow:hidden;text-decoration:none;color:#eaeef2;display:block}
    .card:hover{border-color:#2b3547;transform:translateY(-2px)}
    .thumb{display:block;width:100%;height:150px;object-fit:cover;background:#0f141e}
    .content{padding:14px 16px}
    .title{font-size:18px;margin:0 0 6px;line-height:1.25}
    .desc{font-size:13px;color:#a9b4c0;margin:0}
    .href{font-size:12px;color:#7f8b99;margin-top:8px}
    a.back{display:inline-block;margin-bottom:16px;color:#8ab4ff;text-decoration:none}
    """

    items = []
    for c in cards:
        img = f'<img class="thumb" src="{html.escape(c["thumb"])}" alt="{html.escape(c["title"])}">' if c["thumb"] else '<div class="thumb"></div>'
        desc = f'<p class="desc">{html.escape(c["summary"])}</p>' if c["summary"] else ''
        items.append(f'''
<a class="card" href="{html.escape(c["href"])}">
  {img}
  <div class="content">
    <h2 class="title">{html.escape(c["title"])}</h2>
    {desc}
    <div class="href">{html.escape(c["href"])}</div>
  </div>
</a>
''')
    items_html = "\n".join(items) or "<div class='card'><div class='content'><h2 class='title'>No articles yet</h2></div></div>"

    OUT.write_text(f"""<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Articles · all-in-one</title>
<style>{css}</style>
<body>
<a class="back" href="/"><span>←</span> Back to Home</a>
<h1>Articles</h1>
<p class="muted">Auto-generated index of article guides.</p>
<div class="grid">
{items_html}
</div>
</body>
</html>
""", encoding="utf-8")
    print(f"[ok] wrote {OUT.relative_to(ROOT)} with {len(cards)} tile(s).")

if __name__ == "__main__":
    main()


