#!/bin/bash
# Development setup script for CrewAI Accelerate

set -e

echo "CrewAI Accelerate - Development Setup"
echo "===================================="

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  No virtual environment detected."
    echo "   It's recommended to use a virtual environment."
    echo "   Create one with: python3 -m venv venv && source venv/bin/activate"
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check Python version
echo "Checking Python version..."
python3 -c "import sys; assert sys.version_info >= (3, 8), f'Python 3.8+ required, got {sys.version}'; print(f'✅ Python {sys.version.split()[0]}')"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if maturin is available
echo ""
echo "Checking maturin..."
if ! command -v maturin &> /dev/null; then
    echo "Installing maturin..."
    pip install maturin
fi

# Build the Rust extension
echo ""
echo "Building Rust extension..."
maturin develop

# Run basic tests
echo ""
echo "Running basic tests..."
python3 run_tests.py fast

echo ""
echo "✅ Development setup completed!"
echo ""
echo "Available commands:"
echo "  python run_tests.py        - Run all tests"
echo "  python run_tests.py fast   - Run fast tests"
echo "  make test                  - Run tests with make"
echo "  make install-dev          - Install dev dependencies"
echo ""
echo "Happy coding! 🚀"
