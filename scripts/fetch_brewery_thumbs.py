#!/usr/bin/env python3
from pathlib import Path
import json, yaml, urllib.request, urllib.error, time

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "brewery.yaml"
OUTDIR = ROOT / "assets" / "brewery"
OUTDIR.mkdir(parents=True, exist_ok=True)

def og_url(owner, name):
    # GitHub Open Graph: token gerektirmez; sorgu paramı değiştirerek cache-bust yaparız
    return f"https://opengraph.githubassets.com/1/{owner}/{name}?t={int(time.time())}"

def fetch_png(url, dest: Path):
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            data = r.read()
        dest.write_bytes(data)
        return True
    except urllib.error.HTTPError as e:
        print(f"[warn] {dest.name}: {e}")
    except Exception as e:
        print(f"[warn] {dest.name}: {e}")
    return False

def main():
    cfg = yaml.safe_load(DATA.read_text(encoding="utf-8"))
    results = []
    for repo in cfg.get("repos", []):
        owner, name = repo["owner"], repo["name"]
        fn = OUTDIR / f"{owner}-{name}.png"
        ok = fetch_png(og_url(owner, name), fn)
        repo["thumb"] = f"/assets/brewery/{fn.name}" if ok else "/assets/img/thumb-placeholder.webp"
        results.append(repo)
        print(("[ok] " if ok else "[skip] ") + f"{owner}/{name}")
    (ROOT / "data" / "brewery.cache.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"[done] thumbs -> {OUTDIR}")

if __name__ == "__main__":
    main()


