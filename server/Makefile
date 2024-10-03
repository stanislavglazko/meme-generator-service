check: lint test

lint: ruff

test:
	pytest -n auto -vv --dist loadscope --cov=. tests/

format:
	ruff check . --fix-only --exit-zero

ruff:
	ruff check . --exclude migrations
