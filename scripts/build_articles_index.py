#!/usr/bin/env python3
import os
import json
from datetime import datetime

ARTICLES_DIR = "articles"
OUTPUT_FILE = os.path.join(ARTICLES_DIR, "index.html")

# Default meta.json template
DEFAULT_META = {
    "title": "",
    "description": "",
    "thumb": "",
    "tags": [],
    "lang": [],
    "created": datetime.now().strftime("%Y-%m-%d"),
    "updated": datetime.now().strftime("%Y-%m-%d"),
    "version": "1.0.0"
}

def ensure_meta(article_path):
    meta_path = os.path.join(article_path, "meta.json")
    if not os.path.exists(meta_path):
        # Auto-generate title from folder name
        folder_name = os.path.basename(article_path)
        meta = DEFAULT_META.copy()
        meta["title"] = folder_name.replace("-", " ").title()
        meta["description"] = f"Auto-generated metadata for {meta['title']}."
        meta["thumb"] = f"{article_path}/thumb.webp"
        meta["tags"] = ["auto-generated"]
        meta["lang"] = detect_langs(article_path)
        with open(meta_path, "w") as f:
            json.dump(meta, f, indent=2)
        print(f"✅ Created default meta.json for {folder_name}")
    else:
        print(f"ℹ Found meta.json for {os.path.basename(article_path)}")

def detect_langs(article_path):
    langs = []
    for f in os.listdir(article_path):
        if f.endswith(".html"):
            langs.append(f.split(".")[0])
    return sorted(list(set(langs)))

def load_meta(article_path):
    meta_path = os.path.join(article_path, "meta.json")
    with open(meta_path, "r") as f:
        return json.load(f)

def build_index():
    articles = []
    for name in sorted(os.listdir(ARTICLES_DIR)):
        path = os.path.join(ARTICLES_DIR, name)
        if os.path.isdir(path) and not name.startswith("."):
            ensure_meta(path)
            meta = load_meta(path)
            articles.append(meta)

    # Generate HTML index
    html_parts = [
        "<!DOCTYPE html>",
        "<html><head><meta charset='UTF-8'><title>Articles Index</title></head><body>",
        "<h1>Articles</h1>",
        "<ul>"
    ]
    for meta in articles:
        thumb_html = f"<img src='{meta['thumb']}' alt='{meta['title']}' style='width:120px;height:auto;'>"
        html_parts.append(
            f"<li>{thumb_html}<br><strong>{meta['title']}</strong><br>{meta['description']}</li>"
        )
    html_parts.extend(["</ul>", "</body></html>"])

    with open(OUTPUT_FILE, "w") as f:
        f.write("\n".join(html_parts))
    print(f"📄 Index generated at {OUTPUT_FILE}")

if __name__ == "__main__":
    build_index()

