#!/usr/bin/env python3
import os, json, html, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "articles"
OUT = ART / "index.html"
PLACEHOLDER = ROOT / "assets/img/thumb-placeholder.webp"

def first_existing(*paths: Path) -> Path | None:
    for p in paths:
        if p.exists():
            return p
    return None

def detect_href(dirp: Path) -> str:
    for name in ("en.html", "index.html", "tr.html"):
        f = dirp / name
        if f.exists():
            return f"{dirp.name}/{name}"
    # last resort: folder (not ideal, but avoids crashing)
    return f"{dirp.name}/"

def normalize_meta(dirp: Path) -> dict:
    meta_path = dirp / "meta.json"
    data = {}
    if meta_path.exists():
        try:
            data = json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception:
            data = {}

    title = data.get("title") or dirp.name.replace("-", " ").title()
    desc  = data.get("description") or data.get("summary") or ""

    # thumb: allow "thumb.webp" or "folder/thumb.webp" or full path
    thumb = data.get("thumb", "").strip()
    if thumb and "/" not in thumb:
        # store as "<slug>/thumb.webp" for Pages
        thumb = f"{dirp.name}/{thumb}"
    elif not thumb:
        # no thumb in meta; try conventional file names
        for ext in ("webp", "jpg", "jpeg", "png"):
            candidate = dirp / f"thumb.{ext}"
            if candidate.exists():
                thumb = f"{dirp.name}/{candidate.name}"
                break

    # cache-busting query (mtime) if file exists; else placeholder
    thumb_src = None
    if thumb:
        disk = ROOT / "articles" / thumb.split("/", 1)[0] / thumb.split("/", 1)[1]
        if disk.exists():
            ver = int(disk.stat().st_mtime)
            thumb_src = f"{thumb}?v={ver}"
    if not thumb_src:
        # ensure placeholder exists
        if not PLACEHOLDER.exists():
            PLACEHOLDER.parent.mkdir(parents=True, exist_ok=True)
            # write a tiny blank placeholder to avoid 404s
            PLACEHOLDER.write_bytes(b"")  # you can replace with a real image later
        ver = int(time.time())
        thumb_src = f"/assets/img/thumb-placeholder.webp?v={ver}"

    href = detect_href(dirp)
    return {
        "title": title,
        "desc":  desc,
        "thumb": thumb_src,
        "href":  href,
        "slug":  dirp.name,
    }

def build_cards():
    dirs = [d for d in ART.iterdir() if d.is_dir() and not d.name.startswith(".")]
    cards = [normalize_meta(d) for d in sorted(dirs, key=lambda x: x.name.lower())]
    return cards

def render(cards: list[dict]) -> str:
    css = """
    body{font-family:ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Helvetica,Arial,sans-serif;margin:0;padding:32px;background:#0b0e14;color:#eaeef2}
    h1{font-size:28px;margin:0 0 16px}
    p.muted{color:#a9b4c0;margin:0 0 24px}
    .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:18px}
    .card{background:#121722;border:1px solid #1f2633;border-radius:16px;overflow:hidden;text-decoration:none;color:#eaeef2;display:block}
    .card:hover{border-color:#2b3547;transform:translateY(-2px)}
    .thumb{display:block;width:100%;height:160px;object-fit:cover;background:#0f141e}
    .content{padding:14px 16px}
    .title{font-size:18px;margin:0 0 6px;line-height:1.25}
    .desc{font-size:13px;color:#a9b4c0;margin:0}
    .href{font-size:12px;color:#7f8b99;margin-top:8px}
    a.back{display:inline-block;margin-bottom:16px;color:#8ab4ff;text-decoration:none}
    """
    items = []
    for c in cards:
        desc = f'<p class="desc">{html.escape(c["desc"])}</p>' if c["desc"] else ""
        items.append(f"""
<a class="card" href="{html.escape(c["href"])}">
  <img class="thumb" src="{html.escape(c["thumb"])}" alt="{html.escape(c["title"])}">
  <div class="content">
    <h2 class="title">{html.escape(c["title"])}</h2>
    {desc}
    <div class="href">{html.escape(c["href"])}</div>
  </div>
</a>""")
    items_html = "\n".join(items) or "<div class='card'><div class='content'><h2 class='title'>No articles yet</h2></div></div>"
    return f"""<!doctype html>
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
</html>"""

def main():
    if not ART.exists():
        print("No articles/ directory found; nothing to do.")
        return
    cards = build_cards()
    OUT.write_text(render(cards), encoding="utf-8")
    print(f"[ok] wrote {OUT.relative_to(ROOT)} with {len(cards)} tiles.")

if __name__ == "__main__":
    main()

