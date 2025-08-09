#!/usr/bin/env python3
from pathlib import Path
import json, html, re

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "data" / "brewery.cache.json"
SITE = ROOT / "site" / "index.html"
MARK = "<!-- BREWERY -->"

def render(repos):
    cards = []
    for r in repos:
        href = f"https://github.com/{r['owner']}/{r['name']}"
        img = html.escape(r.get("thumb","/assets/img/thumb-placeholder.webp"))
        title = html.escape(r.get("title", r["name"]))
        desc = html.escape(r.get("summary",""))
        cards.append(f"""
<a class="card" href="{href}" target="_blank" rel="noopener">
  <img class="thumb" src="{img}" alt="{title}">
  <div class="content">
    <h3>{title}</h3>
    <p>{desc}</p>
  </div>
</a>""")
    items = "\n".join(cards) or "<p>No repos yet.</p>"
    # Minimal stil; site stilin varsa ona yaslanır
    return f"""
<section style="margin:28px 0">
  <h2>🏭 In the Brewery — Constantly Evolving</h2>
  <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px">
    {items}
  </div>
</section>
"""

def main():
    repos = json.loads(CACHE.read_text(encoding="utf-8"))
    html_block = render(repos)
    src = SITE.read_text(encoding="utf-8")
    if MARK not in src:
        # bir defalık yerleştirme: başlıktan sonra ekle
        src = re.sub(r"</h1>(?![\s\S]*</h1>)", "</h1>\n" + MARK, src, count=1)
    SITE.write_text(src.replace(MARK, html_block), encoding="utf-8")
    print("[ok] injected brewery section into site/index.html")

if __name__ == "__main__":
    main()

