#!/usr/bin/env python3
import os, json, urllib.request, urllib.error
from pathlib import Path

USER = os.environ.get("GITHUB_USER", "cevherdogan")
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(parents=True, exist_ok=True)

API = f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner&sort=updated"
HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "infograpture-repo-sync",
}
if os.environ.get("GITHUB_TOKEN"):
    HEADERS["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"

def fetch_json(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 401 and "Authorization" in HEADERS:
            # retry unauthenticated
            hdr = {k:v for k,v in HEADERS.items() if k != "Authorization"}
            req = urllib.request.Request(url, headers=hdr)
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        raise


def og_img(owner, name):
    return f"https://opengraph.githubassets.com/1/{owner}/{name}"

def main():
    repos = fetch_json(API)
    items = []
    for r in repos:
        if r.get("private") or r.get("fork"):
            continue
        owner = r["owner"]["login"]
        name = r["name"]
        items.append({
            "owner": owner,
            "name": name,
            "title": (r.get("name") or name).replace("-", " ").title(),
            "summary": (r.get("description") or "").strip(),
            "default_branch": r.get("default_branch") or "main",
            "html_url": r.get("html_url"),
            "homepage": r.get("homepage") or "",
            "topics": r.get("topics", []),
            "language": r.get("language"),
            "stars": r.get("stargazers_count", 0),
            "updated_at": r.get("pushed_at") or r.get("updated_at"),
            "og_image": og_img(owner, name),
        })
    (DATA / "public_repos.json").write_text(
        json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"[ok] repos: {len(items)} → data/public_repos.json")

if __name__ == "__main__":
    main()


