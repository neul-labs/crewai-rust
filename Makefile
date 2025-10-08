# Makefile for CrewAI Accelerate
# Provides convenient commands for development and testing

.PHONY: help install install-dev build test test-fast test-coverage clean lint format docs

# Default target
help:
	@echo "CrewAI Accelerate - Available Commands:"
	@echo "======================================"
	@echo ""
	@echo "Setup:"
	@echo "  install      - Install package in development mode"
	@echo "  install-dev  - Install with development dependencies"
	@echo "  build        - Build the Rust extension"
	@echo ""
	@echo "Testing:"
	@echo "  test         - Run all tests"
	@echo "  test-fast    - Run fast tests only"
	@echo "  test-coverage- Run tests with coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint         - Run linting checks"
	@echo "  format       - Format code with black and isort"
	@echo ""
	@echo "Documentation:"
	@echo "  docs         - Build documentation"
	@echo ""
	@echo "Cleanup:"
	@echo "  clean        - Clean build artifacts"

# Installation
install:
	pip install -r requirements.txt
	maturin develop

install-dev:
	pip install -r requirements-dev.txt
	maturin develop

# Building
build:
	maturin develop

# Testing
test:
	pytest -v

test-fast:
	pytest -m "not slow and not integration and not performance" -v

test-coverage:
	pytest --cov=crewai_accelerate --cov-report=html --cov-report=term

# Code quality
lint:
	flake8 crewai_accelerate tests examples
	mypy crewai_accelerate

format:
	black crewai_accelerate tests examples
	isort crewai_accelerate tests examples

# Documentation
docs:
	cd docs && make html

# Cleanup
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
