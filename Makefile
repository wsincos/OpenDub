.PHONY: check format lint type test web-check

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
	corepack pnpm --dir apps/web lint
	corepack pnpm --dir apps/web typecheck
	corepack pnpm --dir apps/web test
