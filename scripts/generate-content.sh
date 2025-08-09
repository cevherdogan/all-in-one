# scripts/generate-content.sh
#!/usr/bin/env bash
set -euo pipefail
python3 scripts/scaffold_article_meta.py
python3 scripts/build_articles_index.py
echo "✅ meta.json tarandı & /articles/index.html güncellendi."

