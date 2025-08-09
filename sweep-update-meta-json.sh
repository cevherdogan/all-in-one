# just to be sure
grep -H '"thumb"' articles/*/meta.json
# if any still show webm.png, fix:
sed -i '' 's/webm\.png/thumb.webp/g' articles/*/meta.json


