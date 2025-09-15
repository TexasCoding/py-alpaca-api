.PHONY: help install test lint format type-check check clean pre-commit coverage docs

# Default target - show help
help:
	@echo "Available commands:"
	@echo "  make install      - Install all dependencies including dev dependencies"
	@echo "  make test         - Run all tests"
	@echo "  make test-quick   - Run tests without coverage"
	@echo "  make lint         - Run ruff linter"
	@echo "  make format       - Format code with ruff"
	@echo "  make type-check   - Run mypy type checker"
	@echo "  make check        - Run all checks (lint, format-check, type-check)"
	@echo "  make clean        - Remove build artifacts and cache files"
	@echo "  make pre-commit   - Install and run pre-commit hooks"
	@echo "  make coverage     - Generate test coverage report"
	@echo "  make docs         - Build documentation"

# Install all dependencies
install:
	uv sync --all-extras --dev

# Run tests with coverage
test:
	./test.sh

# Run tests without coverage (faster)
test-quick:
	uv run pytest -q tests

# Run specific test file
test-file:
	@read -p "Enter test file path: " file; \
	./test.sh $$file

# Run linter
lint:
	uv run ruff check src

# Fix linting issues automatically
lint-fix:
	uv run ruff check --fix src

# Format code
format:
	uv run ruff format src

# Check if code is formatted correctly
format-check:
	uv run ruff format --check src

# Run type checker
type-check:
	uv run mypy src/

# Run all checks
check: format-check lint type-check

# Clean build artifacts and cache
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

# Install and run pre-commit hooks
pre-commit:
	uv run pre-commit install
	uv run pre-commit run --all-files

# Update pre-commit hooks
pre-commit-update:
	uv run pre-commit autoupdate

# Generate coverage report
coverage:
	uv run pytest --cov=py_alpaca_api --cov-report=html --cov-report=term-missing tests
	@echo "Coverage report generated in htmlcov/index.html"

# Build documentation (if you have sphinx or similar)
docs:
	@echo "Documentation building not configured yet"

# Development workflow - format, lint, and test
dev: format lint-fix test-quick

# CI workflow - all checks without modifications
ci: check test

# Release preparation
release-prep: clean check test
	@echo "Ready for release!"
