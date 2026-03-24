.PHONY: fmt check test mr

fmt:
	poetry run ruff format .

check:
	poetry run ruff check .
	poetry run flake8 app core tests
	poetry run mypy app core tests

test:
	poetry run pytest

mr: fmt check test
