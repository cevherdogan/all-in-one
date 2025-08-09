.PHONY: build content preview

setup:
	python3 -m venv ~/.venv && source ~/.venv/bin/activate

install-deps:
	pip install jinja2 pyyaml markdown

build:
	python3 scripts/generate.py

content:
	python3 scripts/generate_content_readme.py

preview:
	python3 -m http.server 8000

