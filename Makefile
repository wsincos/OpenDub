.PHONY: check docs-check format lint type test web-build web-check web-test

UV_INDEX_URL := https://pypi.org/simple
export UV_INDEX_URL

check: format lint type test web-check web-test web-build docs-check

format:
	uv run ruff format --check src tests

lint:
	uv run ruff check src tests

type:
	uv run mypy src/opendub

test:
	uv run pytest

web-check:
	npm exec --yes --package=pnpm@9.15.0 -- pnpm web:check

web-test:
	npm exec --yes --package=pnpm@9.15.0 -- pnpm --filter @opendub/web test -- --run

web-build:
	npm exec --yes --package=pnpm@9.15.0 -- pnpm --filter @opendub/web build

docs-check:
	uv run python scripts/check_docs_links.py
