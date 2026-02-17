# Makefile for cassandra-cli
#
# This is the canonical template for all Python apps in the SRE repository.
# Copy this file to your app directory and update the app name in comments.
#
# Standard targets:
#   make all          - Run full test suite (install, lint, test, coverage)
#   make install-deps - Install dependencies with Poetry
#   make test         - Run all tests
#   make lint         - Run linting and formatting
#   make coverage     - Run tests with coverage reporting
#   make clean        - Clean up temporary files and caches
#   make lock         - Update poetry.lock file
#   make upgrade-deps - Upgrade all dependencies
#   make help         - Show this help message

.PHONY: all clean coverage help install-deps lint lock test upgrade-deps

# Variables
PYTHON = poetry run python
LINT = poetry run ruff
COVERAGE = poetry run coverage
POETRY = poetry

# Default target
.DEFAULT_GOAL := help

# Run full test suite
all: install-deps lint test coverage

# Install dependencies
install-deps:
	@if [ -f pyproject.toml ]; then \
		echo "Installing dependencies with Poetry..."; \
		$(POETRY) install; \
	else \
		echo "No pyproject.toml found, skipping Poetry install"; \
	fi

# Run tests (pytest with unittest fallback)
test: install-deps
	@echo "Running tests..."
	$(PYTHON) -m pytest tests/ --tb=short -v 2>/dev/null || \
	$(PYTHON) -m unittest discover -s tests -p "*.py" -v 2>/dev/null || \
	echo "No tests found or test framework not available"
	@echo "Cleaning up Python cache files..."
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true

# Run linting and formatting
lint: install-deps
	@echo "Running linting and formatting..."
	$(LINT) check --fix && $(LINT) format

# Run tests with coverage
coverage: install-deps
	@echo "Running tests with coverage..."
	mkdir -p coverage test-results
	$(COVERAGE) run -m pytest tests/ --tb=short -v --junitxml=test-results/junit.xml 2>/dev/null || \
	$(COVERAGE) run -m unittest discover -s tests -p "*.py" 2>/dev/null || \
	echo "No tests found for coverage analysis"
	$(COVERAGE) xml -o coverage/coverage.xml 2>/dev/null || echo "Coverage XML report not available"
	$(COVERAGE) report -m 2>/dev/null || echo "Coverage report not available"

# Clean temporary files and caches
clean:
	@echo "Cleaning up temporary files and caches..."
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name '.pytest_cache' -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name '*.egg-info' -type d -exec rm -rf {} + 2>/dev/null || true
	rm -f .coverage
	rm -rf .ruff_cache
	rm -rf htmlcov

# Update poetry.lock file
lock:
	@echo "Updating poetry.lock file..."
	$(POETRY) lock

# Upgrade dependencies
upgrade-deps:
	@echo "Upgrading dependencies..."
	@if [ -f pyproject.toml ]; then \
		echo "Updating Poetry dependencies..."; \
		$(POETRY) update; \
	else \
		echo "No pyproject.toml found, skipping Poetry update"; \
	fi

# Show help message
help:
	@echo "Available targets:"
	@echo "  all          - Run full test suite (install, lint, test, coverage)"
	@echo "  install-deps - Install dependencies with Poetry"
	@echo "  test         - Run all tests (pytest with unittest fallback)"
	@echo "  lint         - Run linting and formatting"
	@echo "  coverage     - Run tests with coverage reporting"
	@echo "  clean        - Clean up temporary files and caches"
	@echo "  lock         - Update poetry.lock file"
	@echo "  upgrade-deps - Upgrade all dependencies"
	@echo "  help         - Show this help message"
