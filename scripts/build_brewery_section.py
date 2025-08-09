#!/usr/bin/env python3
from pathlib import Path
import json, html, re

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "public_repos.json"
SITE = ROOT / "site" / "index.html"

BEGIN = "<!-- BREWERY:BEGIN -->"
END   = "<!-- BREWERY:END -->"

def render_cards(repos):
    repos = sorted(repos, key=lambda r: (r.get("updated_at") or ""), reverse=True)
    items=[]
    for r in repos:
        href  = r["html_url"]
        img   = f"/assets/brewery/{r['owner']}-{r['name']}.webp"
        title = r.get("title") or r["name"]
        desc  = r.get("summary","")
        items.append(f"""
<a class="card" href="{html.escape(href)}" target="_blank" rel="noopener">
  <img class="thumb" src="{html.escape(img)}" alt="{html.escape(title)}"
       loading="lazy" decoding="async" fetchpriority="low" width="640" height="360">
  <div class="content">
    <h3>{html.escape(title)}</h3>
    <p>{html.escape(desc)}</p>
  </div>
</a>""")
    return "\n".join(items) or "<p>No repositories yet.</p>"

def wrap(block:str)->str:
    css = """
<style>
.brewery-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px}
.brewery-grid .card{display:block;text-decoration:none;color:#0b0e14;background:#121722;border:1px solid #1f2633;border-radius:16px;overflow:hidden}
.brewery-grid .card:hover{border-color:#2b3547;transform:translateY(-2px)}
.brewery-grid .thumb{display:block;width:100%;height:160px;object-fit:cover;background:#0f141e}
.brewery-grid .content{padding:14px 16px}
.brewery-grid h3{margin:0 0 6px;font-size:16px;line-height:1.25;color:#eaeef2}
.brewery-grid p{margin:0;color:#a9b4c0;font-size:13px}
</style>
"""
    return f"""{BEGIN}
<section>
  <h2>🏭 In the Brewery — Constantly Evolving</h2>
  <div class="brewery-grid">
    {block}
  </div>
</section>
{END}
{css}
"""

def inject(html_text:str, block:str)->str:
    if BEGIN in html_text and END in html_text:
        pattern = re.compile(re.escape(BEGIN)+r".*?"+re.escape(END), re.S)
        return re.sub(pattern, block, html_text, count=1)
    # Insert after first <h1> if markers don’t exist yet
    return re.sub(r"(</h1>)", r"\1\n"+block, html_text, count=1)

def main():
    repos = json.loads(DATA.read_text(encoding="utf-8"))
    cards = render_cards(repos)
    section = wrap(cards)
    site = SITE.read_text(encoding="utf-8")
    SITE.write_text(inject(site, section), encoding="utf-8")
    print("[ok] Brewery section injected/replaced")

if __name__ == "__main__":
    main()

