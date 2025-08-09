.PHONY: setup install-deps build content articles preview all brewery

setup:
	python3 -m venv .venv && . .venv/bin/activate

install-deps:
	pip3 install jinja2 pyyaml markdown

build:
	python3 scripts/generate.py

content:
	python3 scripts/generate_content_readme.py

# (re)build the Articles index
articles:
	python3 scripts/build_articles_index.py

preview:
	python3 -m http.server 8000

brewery:
	python3 scripts/fetch_brewery_thumbs.py
	python3 scripts/build_brewery_section.py

# one-shot everything you'd usually run
all: content articles brewery build

