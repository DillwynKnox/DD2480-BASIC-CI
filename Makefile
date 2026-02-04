setup:
	uv sync --extra dev

# Run ruff check
lint:
	uv run ruff check .

lint_fix:
	uv run ruff check --fix .

# Run pytest
test:
	uv run pytest tests/

# Build the project
build:
	uv build

# Run everything
all: lint test build

dev:
	uv run fastapi dev src/basic_ci/main.py --host 0.0.0.0 --port 8000