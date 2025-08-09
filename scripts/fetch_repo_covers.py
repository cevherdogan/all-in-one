#!/usr/bin/env python3
OVR = ROOT / "data" / "cover_overrides.yaml"
import yaml
OV = {}
if OVR.exists():
    OV = { (o["owner"], o["name"]): o for o in yaml.safe_load(OVR.read_text())["overrides"] }

from pathlib import Path
from io import BytesIO
import os, re, json, urllib.request, urllib.error
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "public_repos.json"
OUT  = ROOT / "assets" / "brewery"
OUT.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "infograpture-cover-fetch",
}
if os.environ.get("GITHUB_TOKEN"):
    HEADERS["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"

IMG_MD_RE  = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
IMG_HTML_RE= re.compile(r'<img\s+[^>]*src=["\']([^"\']+)["\']', re.I)

COMMON_NAMES = (
    "article_cover", "cover", "hero", "banner", "logo", "thumb", "og"
)
COMMON_EXTS  = (".webp",".png",".jpg",".jpeg")

def http_get(url: str) -> bytes | None:
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read()
    except Exception as e:
        print(f"[warn] GET {url} -> {e}")
        return None

def save_webp(raw: bytes, dest: Path):
    im = Image.open(BytesIO(raw)).convert("RGB")
    im.thumbnail((640,360))
    dest = dest.with_suffix(".webp")
    im.save(dest, "WEBP", quality=70, method=6)
    return dest

def raw_base(owner: str, repo: str, branch: str) -> str:
    return f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}"

def first_image_from_readme(owner: str, repo: str, branch: str) -> str | None:
    # Try GitHub API for README first (gives download_url), fallback to raw path
    api = f"https://api.github.com/repos/{owner}/{repo}/readme"
    try:
        req = urllib.request.Request(api, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=20) as r:
            jr = json.loads(r.read().decode("utf-8"))
            if "download_url" in jr:
                readme_url = jr["download_url"]
            else:
                readme_url = f"{raw_base(owner, repo, branch)}/README.md"
    except Exception:
        readme_url = f"{raw_base(owner, repo, branch)}/README.md"

    raw = http_get(readme_url)
    if not raw:
        return None
    txt = raw.decode("utf-8", errors="ignore")

    # Try Markdown image
    m = IMG_MD_RE.search(txt)
    if m:
        return resolve_path(m.group(1).strip(), owner, repo, branch)

    # Try HTML <img>
    m = IMG_HTML_RE.search(txt)
    if m:
        return resolve_path(m.group(1).strip(), owner, repo, branch)

    return None

def resolve_path(src: str, owner: str, repo: str, branch: str) -> str:
    if src.startswith("http://") or src.startswith("https://"):
        return src
    # treat as repo-relative
    return f"{raw_base(owner, repo, branch)}/{src.lstrip('./')}"

def first_common_file(owner: str, repo: str, branch: str) -> str | None:
    base = raw_base(owner, repo, branch)
    # Try common filenames in repo root
    for stem in COMMON_NAMES:
        for ext in COMMON_EXTS:
            url = f"{base}/{stem}{ext}"
            if http_get_head_ok(url):
                return url
    return None

def http_get_head_ok(url: str) -> bool:
    try:
        req = urllib.request.Request(url, method="HEAD", headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as r:
            return (200 <= r.status < 400)
    except Exception:
        return False

def og_image(owner: str, repo: str) -> str:
    return f"https://opengraph.githubassets.com/1/{owner}/{repo}"

def pick_cover(owner: str, repo: str, branch: str) -> tuple[str, str]:
    ov = OV.get((owner, repo))
    if ov:
        br = ov.get("branch", branch)
        url = resolve_path(ov["path"], owner, repo, br)
        return url, br
    u = first_image_from_readme(owner, repo, branch)
    if u: return u, branch
    u = first_common_file(owner, repo, branch)
    if u: return u, branch
    return og_image(owner, repo), branch


def main():
    repos = json.loads(DATA.read_text(encoding="utf-8"))
    ok = 0
    for r in repos:
        owner, name, branch = r["owner"], r["name"], r.get("default_branch") or "main"
        out = OUT / f"{owner}-{name}.webp"
        if out.exists():
            print(f"[skip] exists {out.name}")
            ok += 1
            continue
        src, used_branch = pick_cover(owner, name, branch)
        raw = http_get(src)
        if not raw:
            print(f"[warn] no image for {owner}/{name}")
            continue
        out_path = save_webp(raw, OUT / f"{owner}-{name}")
        print(f"[ok] {owner}/{name} → {out_path.relative_to(ROOT)}")
        ok += 1
    print(f"[done] covers prepared: {ok}/{len(repos)}")

if __name__ == "__main__":
    main()


