# scripts/build_articles_index.py
import pathlib, re, html

ROOT = pathlib.Path(__file__).resolve().parents[1]
ART = ROOT / "articles"
OUT = ART / "index.html"

def find_title(p: pathlib.Path) -> str | None:
    # README.md H1
    md = p / "README.md"
    if md.exists():
        m = re.search(r"^#\s+(.+)$", md.read_text(errors="ignore"), re.M)
        if m: return m.group(1).strip()
    # en.html or index.html <title>
    for name in ("en.html", "index.html", "tr.html"):
        f = p / name
        if f.exists():
            m = re.search(r"<title>(.*?)</title>", f.read_text(errors="ignore"), re.I|re.S)
            if m: return re.sub(r"\s+", " ", m.group(1)).strip()
    return None

def find_href(p: pathlib.Path) -> str:
    # prefer index.html if present
    for name in ("index.html", "en.html", "tr.html"):
        f = p / name
        if f.exists(): return f"{p.name}/{name}"
    # otherwise link to the folder (will 404 unless visitors pick a file)
    return f"{p.name}/"

def main():
    if not ART.exists():
        print("No articles/ directory found; skipping.")
        return
    cards = []
    for sub in sorted([d for d in ART.iterdir() if d.is_dir() and not d.name.startswith(".")], key=lambda x: x.name.lower()):
        title = find_title(sub) or sub.name.replace("-", " ").title()
        href = find_href(sub)
        cards.append((title, href))

    css = """
    body{font-family:ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Helvetica,Arial,sans-serif;margin:0;padding:32px;background:#0b0e14;color:#eaeef2}
    h1{font-size:28px;margin:0 0 16px 0}
    p.muted{color:#a9b4c0;margin:0 0 24px}
    .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px}
    .card{background:#121722;border:1px solid #1f2633;border-radius:16px;padding:16px;text-decoration:none;color:#eaeef2;display:block}
    .card:hover{border-color:#2b3547;transform:translateY(-2px)}
    .card h2{font-size:18px;margin:0 0 8px}
    .card span{font-size:13px;color:#a9b4c0}
    a.back{display:inline-block;margin-bottom:16px;color:#8ab4ff;text-decoration:none}
    """

    items = "\n".join(
        f'<a class="card" href="{html.escape(h)}"><h2>{html.escape(t)}</h2><span>{html.escape(h)}</span></a>'
        for t,h in cards
    )

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
{items or "<div class='card'><h2>No articles yet</h2><span>Add folders under /articles</span></div>"}
</div>
</body>
</html>
""", encoding="utf-8")
    print(f"[ok] wrote {OUT.relative_to(ROOT)} with {len(cards)} tile(s).")

if __name__ == "__main__":
    main()

