
# DPP Bilingual Articles (EN/TR)

Public, SEO-friendly, bilingual article site (English ↔ Türkçe) with reusable templates and GitHub Pages deployment.

## Features
- 🧩 Reusable HTML templates (EN/TR) and shared CSS
- 🌐 Bilingual navigation (each article links to the other language)
- 🧪 Local generator (`scripts/generate.py`) to build from Markdown + front matter
- 🚀 Auto deploy to GitHub Pages via Actions
- 🤝 Issue template for new article requests
- 🧠 Optional AI prompt skeleton to standardize article drafting

## Quick Start
```bash
# 1) Create and activate a virtualenv (optional but recommended)
python3 -m venv .venv && source .venv/bin/activate

# 2) Install dependencies
pip install jinja2 pyyaml markdown

# 3) Generate static pages from /content using templates
python scripts/generate.py

# 4) Preview locally (simple server)
python -m http.server 8000

# 5) Visit
open http://localhost:8000/site/index.html
```

## New Article
1. Add `content/<slug>.en.md` and `content/<slug>.tr.md` with YAML front matter.
2. Run `python scripts/generate.py`.
3. Commit changes—GitHub Actions will deploy to Pages.

## Repository Layout
```
.
├── .github
│   ├── ISSUE_TEMPLATE
│   │   └── article.md
│   └── workflows
│       └── deploy.yml
├── ai
│   └── prompts
│       └── drafting_prompt.md
├── assets
│   └── css
│       └── style.css
├── articles
│   └── dpp
│       ├── en.html
│       └── tr.html
├── content
│   ├── dpp.en.md
│   └── dpp.tr.md
├── scripts
│   └── generate.py
├── site
│   └── index.html
├── templates
│   ├── article_en.html
│   └── article_tr.html
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

## Enable GitHub Pages
- Repository → Settings → Pages → Build and deployment: "GitHub Actions".
- The included workflow publishes the `site/` folder automatically.
