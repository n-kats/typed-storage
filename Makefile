target = typed_storage tests

.PHONY: lint
lint:
	poetry run ruff check ${target}
	poetry run mypy ${target}

.PHONY: format
format:
	poetry run ruff format ${target}
	poetry run ruff check --fix ${target}

.PHONY: test
test:
	poetry run pytest
