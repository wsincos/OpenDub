.PHONY: check format lint type test web-check

UV_INDEX_URL := https://pypi.org/simple
export UV_INDEX_URL

check: format lint type test

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
