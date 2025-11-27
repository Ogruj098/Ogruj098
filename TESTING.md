# Testing Guide for eBay Inventory Management

## Overview
This document describes how to run the comprehensive unit tests for the eBay inventory management system.

## Test Coverage
The test suite (`test_ebay_inventory.py`) covers:

### get_stock() function tests:
- ✅ Successful stock retrieval with valid item IDs
- ✅ Various item ID formats (numeric, special characters, unicode)
- ✅ HTTP error codes (404, 401, 403, 500, 503)
- ✅ Network failures (timeouts, connection errors)
- ✅ Invalid JSON responses
- ✅ Complex nested response data
- ✅ Zero quantity (out of stock) scenarios
- ✅ Header and URL format validation
- ✅ Edge cases (empty strings, None values, extremely long IDs)

### update_stock() function tests:
- ✅ Successful updates (200 and 204 responses)
- ✅ Various quantity values (zero, negative, large numbers, floats)
- ✅ HTTP error codes (400, 401, 404, 409, 500)
- ✅ Network failures (timeouts, connection errors)
- ✅ Request body structure validation
- ✅ Header and URL format validation
- ✅ Edge cases (empty item IDs, special characters)

### Integration tests:
- ✅ Get-then-update workflow
- ✅ Multiple items management
- ✅ Error recovery patterns

### Edge cases:
- ✅ Extremely long item IDs
- ✅ Unicode characters
- ✅ None values for parameters
- ✅ Missing response fields
- ✅ Rate limiting (429 errors)
- ✅ Empty response bodies
- ✅ URL-breaking characters

### Security tests:
- ✅ ACCESS_TOKEN inclusion verification
- ✅ Authorization header format validation

## Installation

### Install dependencies:
```bash
pip install -r requirements-test.txt
```

Or install individually:
```bash
pip install pytest pytest-cov pytest-mock requests
```

## Running Tests

### Run all tests:
```bash
pytest test_ebay_inventory.py -v
```

### Run with coverage report:
```bash
pytest test_ebay_inventory.py --cov=ebay_inventory --cov-report=html --cov-report=term
```

### Run specific test class:
```bash
pytest test_ebay_inventory.py::TestGetStock -v
pytest test_ebay_inventory.py::TestUpdateStock -v
```

### Run specific test:
```bash
pytest test_ebay_inventory.py::TestGetStock::test_get_stock_success_with_valid_item_id -v
```

### Run tests with output:
```bash
pytest test_ebay_inventory.py -v -s
```

### Run tests and stop at first failure:
```bash
pytest test_ebay_inventory.py -x
```

## Test Organization

The tests are organized into the following classes:

1. **TestGetStock**: Tests for the `get_stock()` function
2. **TestUpdateStock**: Tests for the `update_stock()` function
3. **TestIntegration**: Integration tests for combined operations
4. **TestEdgeCases**: Edge cases and boundary conditions
5. **TestAccessTokenHandling**: Security and token validation tests

## Mocking Strategy

All tests use `unittest.mock` to mock external API calls:
- `requests.get()` is mocked for `get_stock()` tests
- `requests.put()` is mocked for `update_stock()` tests
- No actual API calls are made during testing
- All external dependencies are isolated

## Expected Test Results

With proper mocking, all tests should pass. The test suite includes comprehensive coverage.

## Continuous Integration

To integrate with CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    pip install -r requirements-test.txt
    pytest test_ebay_inventory.py --cov=ebay_inventory --cov-report=xml
```

## Troubleshooting

### Import Errors
If you encounter import errors, ensure:
- The test file is in the same directory as `ebay_inventory.py`
- Python can find the module (check PYTHONPATH)

### Mock Issues
If mocks aren't working:
- Verify the patch path matches the import path
- Use `patch('ebay_inventory.requests.get')` not `patch('requests.get')`