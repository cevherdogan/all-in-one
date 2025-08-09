#!/usr/bin/env python3
from pathlib import Path
import yaml, urllib.request, urllib.error
from PIL import Image
from io import BytesIO

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "brewery.yaml"
OUT  = ROOT / "assets" / "brewery"
OUT.mkdir(parents=True, exist_ok=True)

def fetch_bytes(url:str)->bytes|None:
    try:
        with urllib.request.urlopen(url, timeout=25) as resp:
            return resp.read()
    except Exception as e:
        print(f"[warn] fetch: {url} -> {e}")
        return None

def save_webp(raw:bytes, dest:Path):
    im = Image.open(BytesIO(raw)).convert("RGB")
    im.thumbnail((640,360))
    dest = dest.with_suffix(".webp")
    im.save(dest, "WEBP", quality=70, method=6)
    return dest

def main():
    cfg = yaml.safe_load(DATA.read_text(encoding="utf-8"))
    ok = 0
    for r in cfg.get("repos", []):
        owner, name = r["owner"], r["name"]
        url   = f"https://opengraph.githubassets.com/1/{owner}/{name}"
        dest  = OUT / f"{owner}-{name}"
        if dest.with_suffix(".webp").exists():  # idempotent
            print(f"[skip] exists {dest.with_suffix('.webp').name}")
            ok += 1
            continue
        raw = fetch_bytes(url)
        if not raw:
            continue
        out = save_webp(raw, dest)
        print(f"[ok] {out.relative_to(ROOT)}")
        ok += 1
    print(f"[done] optimized thumbs: {ok}/{len(cfg.get('repos', []))}")

if __name__ == "__main__":
    main()

