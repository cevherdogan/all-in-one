#!/usr/bin/env python3
import os
import sys
import shutil
import datetime
from pathlib import Path
import markdown
import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
ARTICLES_DIR = ROOT / "articles"
SITE_DIR = ROOT / "site"
BUILD_DIR = ROOT / "build"

MARKDOWN_EXTS = {".md", ".mdx"}
HTML_EXTS = {".html", ".htm"}


def load(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def save(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def is_markdown(path: Path) -> bool:
    return path.suffix.lower() in MARKDOWN_EXTS


def is_html(path: Path) -> bool:
    return path.suffix.lower() in HTML_EXTS


def is_hidden(path: Path) -> bool:
    # skip hidden files like .DS_Store, .gitkeep, etc.
    return any(part.startswith(".") for part in path.parts)


def parse_with_front_matter(text: str):
    """Parse YAML front matter at the start of the file."""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            meta_text = parts[1]
            body = parts[2]
            try:
                meta = yaml.safe_load(meta_text) or {}
            except yaml.YAMLError as e:
                raise ValueError(f"Invalid front matter YAML: {e}")
            return meta, body
    raise ValueError("Missing front matter")


def markdown_to_html(md_text: str) -> str:
    return markdown.markdown(md_text, extensions=["fenced_code", "tables", "toc"])


def process_source(path: Path):
    """Process a single source file and output to build directory."""
    if is_hidden(path):
        print(f"[skip] Hidden: {path.relative_to(ROOT)}")
        return None

    # HTML files: copy as-is
    if is_html(path):
        html_text = load(path)
        rel = path.relative_to(ROOT)
        out = BUILD_DIR / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        save(out, html_text)
        print(f"[copy] HTML: {rel}")
        return None

    # Markdown files: require front matter
    if is_markdown(path):
        try:
            meta, body = parse_with_front_matter(load(path))
        except ValueError as e:
            print(f"[warn] Skipping {path.relative_to(ROOT)}: {e}")
            return None
        html_text = markdown_to_html(body)
        rel_html = path.with_suffix(".html").relative_to(ROOT)
        out = BUILD_DIR / rel_html
        out.parent.mkdir(parents=True, exist_ok=True)
        save(out, html_text)
        print(f"[ok] Markdown→HTML: {rel_html}")
        return {"meta": meta, "html": rel_html}

    # Other assets (images, CSS, JS, etc.)
    rel = path.relative_to(ROOT)
    out = BUILD_DIR / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, out)
    print(f"[copy] Other: {rel}")
    return None


def main():
    print(f"Build started at {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    BUILD_DIR.mkdir()

    # Walk through content/, articles/, site/
    for base_dir in (CONTENT_DIR, ARTICLES_DIR, SITE_DIR):
        for path in base_dir.rglob("*"):
            if path.is_file():
                process_source(path)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

