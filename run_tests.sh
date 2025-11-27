#!/bin/bash
# Quick start script for running tests

set -e

echo "🧪 eBay Inventory Test Runner"
echo "=============================="
echo ""

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "❌ pytest not found. Installing dependencies..."
    pip install -r requirements-test.txt
else
    echo "✅ pytest found"
fi

echo ""
echo "Running tests..."
echo ""

# Run tests with verbose output and coverage
pytest test_ebay_inventory.py -v --cov=ebay_inventory --cov-report=term-missing

echo ""
echo "✅ Test run complete!"