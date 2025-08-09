#!/usr/bin/env python3
from pathlib import Path
import json, html, re

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "data" / "public_repos.json"     # from sync_public_repos.py
SITE  = ROOT / "site" / "index.html"

BEGIN = "<!-- BREWERY:BEGIN -->"
END   = "<!-- BREWERY:END -->"

def render_cards(repos):
    # keep only those with a summary (optional) and sort by updated desc
    repos = sorted(repos, key=lambda r: (r.get("updated_at") or ""), reverse=True)
    cards=[]
    for r in repos:
        href  = r["html_url"]
        img   = f"/assets/brewery/{r['owner']}-{r['name']}.webp"  # we will create webp below
        title = r.get("title") or r["name"]
        desc  = r.get("summary","")
        cards.append(f"""
<a class="card" href="{html.escape(href)}" target="_blank" rel="noopener">
  <img class="thumb" src="{html.escape(img)}" alt="{html.escape(title)}"
       loading="lazy" decoding="async" fetchpriority="low" width="640" height="360">
  <div class="content">
    <h3>{html.escape(title)}</h3>
    <p>{html.escape(desc)}</p>
  </div>
</a>""")
    return "\n".join(cards) or "<p>No repositories yet.</p>"

def wrap_section(inner_html:str)->str:
    # inline, resilient styles
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
    {inner_html}
  </div>
</section>
{END}
{css}
"""

def inject(html_text:str, block:str)->str:
    if BEGIN in html_text and END in html_text:
        # replace existing block
        pattern = re.compile(re.escape(BEGIN)+r".*?"+re.escape(END), re.S)
        return re.sub(pattern, block, html_text, count=1)
    # otherwise insert after first <h1>
    return re.sub(r"(</h1>)", r"\1\n"+block, html_text, count=1)

def main():
    repos = json.loads((ROOT/"data/public_repos.json").read_text(encoding="utf-8"))
    cards = render_cards(repos)
    block = wrap_section(cards)
    site_html = SITE.read_text(encoding="utf-8")
    SITE.write_text(inject(site_html, block), encoding="utf-8")
    print("[ok] Brewery section injected/replaced in site/index.html")

if __name__ == "__main__":
    main()


