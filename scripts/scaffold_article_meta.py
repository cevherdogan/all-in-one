# scripts/scaffold_article_meta.py
import pathlib, re, json, html, datetime

ROOT = pathlib.Path(__file__).resolve().parents[1]
ART = ROOT / "articles"

TITLE_HTML_RE = re.compile(r"<title>(.*?)</title>", re.I | re.S)
TITLE_MD_H1_RE = re.compile(r"^\s*#\s+(.+)$", re.M)
FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.S)

def read(p): return p.read_text(encoding="utf-8", errors="ignore")

def load_front_matter(md_text: str) -> dict:
    m = FM_RE.match(md_text)
    if not m: return {}
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"\'')
    return meta

def guess_title(dirp: pathlib.Path) -> str:
    # 1) README.md front matter -> title
    md = dirp / "README.md"
    if md.exists():
        txt = read(md)
        fm = load_front_matter(txt)
        if "title" in fm: return fm["title"]
        m = TITLE_MD_H1_RE.search(txt)
        if m: return m.group(1).strip()
    # 2) en.html/index.html/tr.html <title>
    for name in ("en.html", "index.html", "tr.html"):
        f = dirp / name
        if f.exists():
            m = TITLE_HTML_RE.search(read(f))
            if m:
                return re.sub(r"\s+", " ", m.group(1)).strip()
    # 3) folder name
    return dirp.name.replace("-", " ").title()

def guess_summary(dirp: pathlib.Path) -> str:
    # 1) README.md front matter -> summary
    md = dirp / "README.md"
    if md.exists():
        txt = read(md)
        fm = load_front_matter(txt)
        if "summary" in fm:
            return fm["summary"]
        # 2) first paragraph after FM/H1
        body = FM_RE.sub("", txt, count=1)
        parts = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
        if parts:
            s = re.sub(r"[#>*_`~\-]+", "", parts[0])
            return re.sub(r"\s+", " ", s)[:200]
    # 3) en.html first <p>
    for name in ("en.html", "index.html", "tr.html"):
        f = dirp / name
        if f.exists():
            txt = read(f)
            m = re.search(r"<p[^>]*>(.*?)</p>", txt, re.I | re.S)
            if m:
                s = re.sub("<.*?>", "", m.group(1))
                return re.sub(r"\s+", " ", s).strip()[:200]
    return ""

def guess_thumb(dirp: pathlib.Path) -> str:
    # prefer existing thumb.*
    for ext in ("webp","jpg","jpeg","png"):
        f = dirp / f"thumb.{ext}"
        if f.exists(): return f.name
    # fallback placeholder name (kullanıcı sonra ekler)
    return "thumb.webp"

def scaffold_for(dirp: pathlib.Path) -> bool:
    j = dirp / "meta.json"
    if j.exists():  # idempotent; dokunma
        return False
    meta = {
        "title": guess_title(dirp),
        "summary": guess_summary(dirp),
        "thumb": guess_thumb(dirp)
    }
    j.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[meta] created {j.relative_to(ROOT)}")
    return True

def main():
    if not ART.exists():
        print("No articles/ directory; nothing to scaffold."); return
    created = 0
    for d in sorted([p for p in ART.iterdir() if p.is_dir() and not p.name.startswith(".")], key=lambda x: x.name):
        created += 1 if scaffold_for(d) else 0
    print(f"[done] meta files created: {created}")

if __name__ == "__main__":
    main()

