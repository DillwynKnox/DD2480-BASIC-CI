setup:
	uv sync --extra dev

# Run ruff check
lint:
	uv run ruff check .

# Run pytest
test:
	uv run pytest tests/

# Build the project
build:
	uv build

# Run everything
all: lint test build