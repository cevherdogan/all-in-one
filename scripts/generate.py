
import os, pathlib, re, json

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
TEMPLATES = ROOT / "templates"
ARTICLES = ROOT / "articles"

def load(path):
    return path.read_text(encoding="utf-8")

def render_template(tpl_str, **ctx):
    # Very small, safe-ish renderer (no logic)
    out = tpl_str
    for k, v in ctx.items():
        if k == "content":
            out = out.replace("{{ content|safe }}", v)
        else:
            out = out.replace("{{ " + k + " }}", str(v))
    # Remove badges block if not present
    if "{{ badges }}" in out or "{% if badges %}" in out:
        # crude removal of templating lines
        out = out.replace("{% if badges %}", "").replace("{% endif %}", "")
        # no loop needed; badges already injected as string
    return out

def tiny_md_to_html(md):
    # Very small subset: headings, bold, lists, paragraphs
    html_lines = []
    lines = md.splitlines()
    in_list = False
    buf_par = []

    def flush_par():
        nonlocal buf_par, html_lines
        if buf_par:
            html_lines.append("<p>" + " ".join(buf_par) + "</p>")
            buf_par = []

    for line in lines:
        if line.strip().startswith("## "):
            flush_par()
            html_lines.append(f"<h2>{line.strip()[3:]}</h2>")
            continue
        if line.strip().startswith("- "):
            if not in_list:
                flush_par()
                html_lines.append("<ul>")
                in_list = True
            html_lines.append(f"<li>{line.strip()[2:]}</li>")
            continue
        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False

        # bold **text**
        line = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", line)
        if line.strip():
            buf_par.append(line.strip())
        else:
            flush_par()

    if in_list:
        html_lines.append("</ul>")
    flush_par()
    return "\n".join(html_lines)

def parse_with_front_matter(text):
    text = text.lstrip()
    if text.startswith('---'):
        _, front, body = text.split('---', 2)
        # Minimal front matter parser (key: value, lists as [a, b, c])
        meta = {}
        for line in front.strip().splitlines():
            if ':' in line:
                k, v = line.split(':', 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                # list support: [a, b, c]
                if v.startswith('[') and v.endswith(']'):
                    items = [i.strip().strip('"').strip("'") for i in v[1:-1].split(',') if i.strip()]
                    meta[k] = items
                else:
                    meta[k] = v
        return meta, body.strip()
    raise ValueError('Missing front matter')

def build_one(en_md_path, tr_md_path, tpl_en_path, tpl_tr_path, out_dir):
    en_meta, en_body = parse_with_front_matter(load(en_md_path))
    tr_meta, tr_body = parse_with_front_matter(load(tr_md_path))

    en_html_body = tiny_md_to_html(en_body)
    tr_html_body = tiny_md_to_html(tr_body)

    tpl_en = load(tpl_en_path)
    tpl_tr = load(tpl_tr_path)

    badges_en = "".join([f'<span class="badge">{b}</span>' for b in en_meta.get("badges", [])])
    badges_tr = "".join([f'<span class="badge">{b}</span>' for b in tr_meta.get("badges", [])])

    en_page = tpl_en
    en_page = en_page.replace("{{ title }}", en_meta.get("title",""))
    en_page = en_page.replace("{{ description }}", en_meta.get("description",""))
    en_page = en_page.replace("{{ tr_href }}", "tr.html")
    en_page = en_page.replace("{% if badges %}", "").replace("{% endif %}", "")
    en_page = en_page.replace("{% for b in badges %}<span class=\"badge\">{{ b }}</span>{% endfor %}", badges_en)
    en_page = en_page.replace("{{ content|safe }}", en_html_body)

    tr_page = tpl_tr
    tr_page = tr_page.replace("{{ title }}", tr_meta.get("title",""))
    tr_page = tr_page.replace("{{ description }}", tr_meta.get("description",""))
    tr_page = tr_page.replace("{{ en_href }}", "en.html")
    tr_page = tr_page.replace("{% if badges %}", "").replace("{% endif %}", "")
    tr_page = tr_page.replace("{% for b in badges %}<span class=\"badge\">{{ b }}</span>{% endfor %}", badges_tr)
    tr_page = tr_page.replace("{{ content|safe }}", tr_html_body)

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "en.html").write_text(en_page, encoding="utf-8")
    (out_dir / "tr.html").write_text(tr_page, encoding="utf-8")

def main():
    # Find pairs by slug
    content_dir = CONTENT
    files = list(content_dir.glob("*.md"))
    slugs = {}
    for p in files:
        meta, _ = parse_with_front_matter(load(p))
        slug = meta.get("slug")
        lang = meta.get("lang")
        if not slug or lang not in ("en","tr"):
            print(f"Skip {p.name} (need slug + lang)")
            continue
        slugs.setdefault(slug, {})[lang] = p

    for slug, pair in slugs.items():
        if "en" in pair and "tr" in pair:
            out_dir = ARTICLES / slug
            build_one(pair["en"], pair["tr"], TEMPLATES / "article_en.html", TEMPLATES / "article_tr.html", out_dir)
            print(f"Built: {slug}")
        else:
            print(f"Missing counterpart for slug '{slug}'")

if __name__ == "__main__":
    main()
