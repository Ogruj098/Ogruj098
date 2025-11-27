"""
Comprehensive unit tests for ebay_inventory.py

This test suite covers:
- Happy path scenarios for get_stock and update_stock
- Edge cases (empty responses, malformed data)
- Error handling (HTTP errors, network failures)
- Input validation
- Mock external API calls to avoid real network requests
"""

import json
import pytest
from unittest.mock import patch, Mock, MagicMock
import requests

# Import functions to test
from ebay_inventory import get_stock, update_stock, ACCESS_TOKEN


class TestGetStock:
    """Test suite for the get_stock function"""
    
    def test_get_stock_success_with_valid_item_id(self):
        """Test successful stock retrieval with valid item ID"""
        item_id = "TEST123"
        expected_data = {
            "sku": item_id,
            "availability": {
                "ship_to_location_availability": {
                    "quantity": 10
                }
            }
        }
        
        with patch('ebay_inventory.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = expected_data
            mock_get.return_value = mock_response
            
            result = get_stock(item_id)
            
            assert result == expected_data
            mock_get.assert_called_once_with(
                f"https://api.ebay.com/sell/inventory/v1/inventory_item/{item_id}",
                headers={
                    'Authorization': f'Bearer {ACCESS_TOKEN}',
                    'Content-Type': 'application/json',
                }
            )
    
    def test_get_stock_with_empty_string_item_id(self):
        """Test get_stock with empty string item ID"""
        item_id = ""
        expected_data = {"error": "Invalid item ID"}
        
        with patch('ebay_inventory.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = expected_data
            mock_get.return_value = mock_response
            
            result = get_stock(item_id)
            
            assert result == expected_data
    
    def test_get_stock_with_special_characters_in_item_id(self):
        """Test get_stock with special characters in item ID"""
        item_id = "ITEM-123_ABC@test"
        expected_data = {"sku": item_id, "quantity": 5}
        
        with patch('ebay_inventory.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = expected_data
            mock_get.return_value = mock_response
            
            result = get_stock(item_id)
            
            assert result == expected_data
    
    def test_get_stock_with_numeric_item_id(self):
        """Test get_stock with numeric item ID"""
        item_id = "12345678"
        expected_data = {"sku": item_id, "quantity": 100}
        
        with patch('ebay_inventory.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = expected_data
            mock_get.return_value = mock_response
            
            result = get_stock(item_id)
            
            assert result == expected_data
    
    def test_get_stock_404_not_found(self):
        """Test get_stock when item is not found (404)"""
        item_id = "NONEXISTENT"
        
        with patch('ebay_inventory.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 404
            mock_response.text = "Item not found"
            mock_get.return_value = mock_response
            
            with pytest.raises(Exception) as exc_info:
                get_stock(item_id)
            
            assert "Error fetching stock: Item not found" in str(exc_info.value)
    
    def test_get_stock_401_unauthorized(self):
        """Test get_stock with unauthorized access (401)"""
        item_id = "TEST123"
        
        with patch('ebay_inventory.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 401
            mock_response.text = "Unauthorized access"
            mock_get.return_value = mock_response
            
            with pytest.raises(Exception) as exc_info:
                get_stock(item_id)
            
            assert "Error fetching stock: Unauthorized access" in str(exc_info.value)
    
    def test_get_stock_403_forbidden(self):
        """Test get_stock with forbidden access (403)"""
        item_id = "TEST123"
        
        with patch('ebay_inventory.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 403
            mock_response.text = "Forbidden"
            mock_get.return_value = mock_response
            
            with pytest.raises(Exception) as exc_info:
                get_stock(item_id)
            
            assert "Error fetching stock: Forbidden" in str(exc_info.value)
    
    def test_get_stock_500_server_error(self):
        """Test get_stock with server error (500)"""
        item_id = "TEST123"
        
        with patch('ebay_inventory.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 500
            mock_response.text = "Internal server error"
            mock_get.return_value = mock_response
            
            with pytest.raises(Exception) as exc_info:
                get_stock(item_id)
            
            assert "Error fetching stock: Internal server error" in str(exc_info.value)
    
    def test_get_stock_503_service_unavailable(self):
        """Test get_stock when service is unavailable (503)"""
        item_id = "TEST123"
        
        with patch('ebay_inventory.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 503
            mock_response.text = "Service unavailable"
            mock_get.return_value = mock_response
            
            with pytest.raises(Exception) as exc_info:
                get_stock(item_id)
            
            assert "Error fetching stock: Service unavailable" in str(exc_info.value)
    
    def test_get_stock_network_timeout(self):
        """Test get_stock with network timeout"""
        item_id = "TEST123"
        
        with patch('ebay_inventory.requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.Timeout("Request timeout")
            
            with pytest.raises(requests.exceptions.Timeout):
                get_stock(item_id)
    
    def test_get_stock_connection_error(self):
        """Test get_stock with connection error"""
        item_id = "TEST123"
        
        with patch('ebay_inventory.requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")
            
            with pytest.raises(requests.exceptions.ConnectionError):
                get_stock(item_id)
    
    def test_get_stock_invalid_json_response(self):
        """Test get_stock with invalid JSON in response"""
        item_id = "TEST123"
        
        with patch('ebay_inventory.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
            mock_get.return_value = mock_response
            
            with pytest.raises(json.JSONDecodeError):
                get_stock(item_id)
    
    def test_get_stock_with_complex_response_data(self):
        """Test get_stock with complex nested response data"""
        item_id = "COMPLEX123"
        expected_data = {
            "sku": item_id,
            "availability": {
                "ship_to_location_availability": {
                    "quantity": 25,
                    "allocation_by_format": {
                        "auction": 5,
                        "fixed_price": 20
                    }
                }
            },
            "product": {
                "title": "Test Product",
                "aspects": {
                    "Brand": ["TestBrand"],
                    "Type": ["TestType"]
                }
            }
        }
        
        with patch('ebay_inventory.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = expected_data
            mock_get.return_value = mock_response
            
            result = get_stock(item_id)
            
            assert result == expected_data
            assert result["availability"]["ship_to_location_availability"]["quantity"] == 25
    
    def test_get_stock_with_zero_quantity(self):
        """Test get_stock with zero quantity (out of stock)"""
        item_id = "OUTOFSTOCK"
        expected_data = {
            "sku": item_id,
            "availability": {
                "ship_to_location_availability": {
                    "quantity": 0
                }
            }
        }
        
        with patch('ebay_inventory.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = expected_data
            mock_get.return_value = mock_response
            
            result = get_stock(item_id)
            
            assert result == expected_data
            assert result["availability"]["ship_to_location_availability"]["quantity"] == 0
    
    def test_get_stock_headers_are_set_correctly(self):
        """Test that get_stock sets the correct headers"""
        item_id = "TEST123"
        
        with patch('ebay_inventory.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"sku": item_id}
            mock_get.return_value = mock_response
            
            get_stock(item_id)
            
            # Verify headers are correct
            call_args = mock_get.call_args
            headers = call_args[1]['headers']
            assert 'Authorization' in headers
            assert headers['Authorization'].startswith('Bearer ')
            assert headers['Content-Type'] == 'application/json'
    
    def test_get_stock_url_format(self):
        """Test that get_stock constructs the URL correctly"""
        item_id = "TEST123"
        
        with patch('ebay_inventory.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"sku": item_id}
            mock_get.return_value = mock_response
            
            get_stock(item_id)
            
            # Verify URL format
            call_args = mock_get.call_args
            url = call_args[0][0]
            assert url == f"https://api.ebay.com/sell/inventory/v1/inventory_item/{item_id}"
            assert "inventory_item" in url
            assert item_id in url


class TestUpdateStock:
    """Test suite for the update_stock function"""
    
    def test_update_stock_success_200(self):
        """Test successful stock update with 200 response"""
        item_id = "TEST123"
        quantity = 50
        
        with patch('ebay_inventory.requests.put') as mock_put:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_put.return_value = mock_response
            
            # Capture print output
            with patch('builtins.print') as mock_print:
                update_stock(item_id, quantity)
                mock_print.assert_called_once_with("Stock updated successfully!")
            
            mock_put.assert_called_once()
    
    def test_update_stock_success_204(self):
        """Test successful stock update with 204 response (no content)"""
        item_id = "TEST123"
        quantity = 30
        
        with patch('ebay_inventory.requests.put') as mock_put:
            mock_response = Mock()
            mock_response.status_code = 204
            mock_put.return_value = mock_response
            
            with patch('builtins.print') as mock_print:
                update_stock(item_id, quantity)
                mock_print.assert_called_once_with("Stock updated successfully!")
    
    def test_update_stock_with_zero_quantity(self):
        """Test update_stock with zero quantity"""
        item_id = "TEST123"
        quantity = 0
        
        with patch('ebay_inventory.requests.put') as mock_put:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_put.return_value = mock_response
            
            with patch('builtins.print') as mock_print:
                update_stock(item_id, quantity)
                mock_print.assert_called_once()
    
    def test_update_stock_with_large_quantity(self):
        """Test update_stock with very large quantity"""
        item_id = "TEST123"
        quantity = 999999
        
        with patch('ebay_inventory.requests.put') as mock_put:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_put.return_value = mock_response
            
            with patch('builtins.print') as mock_print:
                update_stock(item_id, quantity)
                mock_print.assert_called_once()
    
    def test_update_stock_with_negative_quantity(self):
        """Test update_stock with negative quantity (should still make request)"""
        item_id = "TEST123"
        quantity = -5
        
        with patch('ebay_inventory.requests.put') as mock_put:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_put.return_value = mock_response
            
            with patch('builtins.print') as mock_print:
                update_stock(item_id, quantity)
                mock_print.assert_called_once()
    
    def test_update_stock_request_body_structure(self):
        """Test that update_stock sends correct request body structure"""
        item_id = "TEST123"
        quantity = 42
        
        with patch('ebay_inventory.requests.put') as mock_put:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_put.return_value = mock_response
            
            update_stock(item_id, quantity)
            
            # Verify request body
            call_args = mock_put.call_args
            data = call_args[1]['json']
            assert 'availability' in data
            assert 'ship_to_location_availability' in data['availability']
            assert data['availability']['ship_to_location_availability']['quantity'] == quantity
    
    def test_update_stock_headers_are_set_correctly(self):
        """Test that update_stock sets the correct headers"""
        item_id = "TEST123"
        quantity = 10
        
        with patch('ebay_inventory.requests.put') as mock_put:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_put.return_value = mock_response
            
            update_stock(item_id, quantity)
            
            # Verify headers
            call_args = mock_put.call_args
            headers = call_args[1]['headers']
            assert 'Authorization' in headers
            assert headers['Authorization'].startswith('Bearer ')
            assert headers['Content-Type'] == 'application/json'
    
    def test_update_stock_url_format(self):
        """Test that update_stock constructs the URL correctly"""
        item_id = "TEST123"
        quantity = 10
        
        with patch('ebay_inventory.requests.put') as mock_put:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_put.return_value = mock_response
            
            update_stock(item_id, quantity)
            
            # Verify URL
            call_args = mock_put.call_args
            url = call_args[0][0]
            assert url == f"https://api.ebay.com/sell/inventory/v1/inventory_item/{item_id}"
    
    def test_update_stock_400_bad_request(self):
        """Test update_stock with bad request (400)"""
        item_id = "TEST123"
        quantity = 10
        
        with patch('ebay_inventory.requests.put') as mock_put:
            mock_response = Mock()
            mock_response.status_code = 400
            mock_response.text = "Bad request: Invalid quantity"
            mock_put.return_value = mock_response
            
            with pytest.raises(Exception) as exc_info:
                update_stock(item_id, quantity)
            
            assert "Error updating stock: Bad request: Invalid quantity" in str(exc_info.value)
    
    def test_update_stock_401_unauthorized(self):
        """Test update_stock with unauthorized access (401)"""
        item_id = "TEST123"
        quantity = 10
        
        with patch('ebay_inventory.requests.put') as mock_put:
            mock_response = Mock()
            mock_response.status_code = 401
            mock_response.text = "Unauthorized"
            mock_put.return_value = mock_response
            
            with pytest.raises(Exception) as exc_info:
                update_stock(item_id, quantity)
            
            assert "Error updating stock: Unauthorized" in str(exc_info.value)
    
    def test_update_stock_404_not_found(self):
        """Test update_stock when item is not found (404)"""
        item_id = "NONEXISTENT"
        quantity = 10
        
        with patch('ebay_inventory.requests.put') as mock_put:
            mock_response = Mock()
            mock_response.status_code = 404
            mock_response.text = "Item not found"
            mock_put.return_value = mock_response
            
            with pytest.raises(Exception) as exc_info:
                update_stock(item_id, quantity)
            
            assert "Error updating stock: Item not found" in str(exc_info.value)
    
    def test_update_stock_409_conflict(self):
        """Test update_stock with conflict error (409)"""
        item_id = "TEST123"
        quantity = 10
        
        with patch('ebay_inventory.requests.put') as mock_put:
            mock_response = Mock()
            mock_response.status_code = 409
            mock_response.text = "Conflict: Stock already updated"
            mock_put.return_value = mock_response
            
            with pytest.raises(Exception) as exc_info:
                update_stock(item_id, quantity)
            
            assert "Error updating stock: Conflict: Stock already updated" in str(exc_info.value)
    
    def test_update_stock_500_server_error(self):
        """Test update_stock with server error (500)"""
        item_id = "TEST123"
        quantity = 10
        
        with patch('ebay_inventory.requests.put') as mock_put:
            mock_response = Mock()
            mock_response.status_code = 500
            mock_response.text = "Internal server error"
            mock_put.return_value = mock_response
            
            with pytest.raises(Exception) as exc_info:
                update_stock(item_id, quantity)
            
            assert "Error updating stock: Internal server error" in str(exc_info.value)
    
    def test_update_stock_network_timeout(self):
        """Test update_stock with network timeout"""
        item_id = "TEST123"
        quantity = 10
        
        with patch('ebay_inventory.requests.put') as mock_put:
            mock_put.side_effect = requests.exceptions.Timeout("Request timeout")
            
            with pytest.raises(requests.exceptions.Timeout):
                update_stock(item_id, quantity)
    
    def test_update_stock_connection_error(self):
        """Test update_stock with connection error"""
        item_id = "TEST123"
        quantity = 10
        
        with patch('ebay_inventory.requests.put') as mock_put:
            mock_put.side_effect = requests.exceptions.ConnectionError("Connection failed")
            
            with pytest.raises(requests.exceptions.ConnectionError):
                update_stock(item_id, quantity)
    
    def test_update_stock_with_empty_item_id(self):
        """Test update_stock with empty item ID"""
        item_id = ""
        quantity = 10
        
        with patch('ebay_inventory.requests.put') as mock_put:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_put.return_value = mock_response
            
            with patch('builtins.print') as mock_print:
                update_stock(item_id, quantity)
                mock_print.assert_called_once()
    
    def test_update_stock_with_special_characters_in_item_id(self):
        """Test update_stock with special characters in item ID"""
        item_id = "ITEM-123_ABC@test"
        quantity = 15
        
        with patch('ebay_inventory.requests.put') as mock_put:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_put.return_value = mock_response
            
            with patch('builtins.print') as mock_print:
                update_stock(item_id, quantity)
                mock_print.assert_called_once()
    
    def test_update_stock_with_float_quantity(self):
        """Test update_stock with float quantity (edge case)"""
        item_id = "TEST123"
        quantity = 10.5
        
        with patch('ebay_inventory.requests.put') as mock_put:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_put.return_value = mock_response
            
            with patch('builtins.print') as mock_print:
                update_stock(item_id, quantity)
                mock_print.assert_called_once()
            
            # Verify the float is passed through
            call_args = mock_put.call_args
            data = call_args[1]['json']
            assert data['availability']['ship_to_location_availability']['quantity'] == 10.5


class TestIntegration:
    """Integration tests for combined operations"""
    
    def test_get_then_update_stock_workflow(self):
        """Test typical workflow: get stock, then update it"""
        item_id = "TEST123"
        original_quantity = 10
        new_quantity = 20
        
        # Mock get_stock
        with patch('ebay_inventory.requests.get') as mock_get:
            mock_get_response = Mock()
            mock_get_response.status_code = 200
            mock_get_response.json.return_value = {
                "sku": item_id,
                "availability": {
                    "ship_to_location_availability": {
                        "quantity": original_quantity
                    }
                }
            }
            mock_get.return_value = mock_get_response
            
            stock_data = get_stock(item_id)
            assert stock_data["availability"]["ship_to_location_availability"]["quantity"] == original_quantity
        
        # Mock update_stock
        with patch('ebay_inventory.requests.put') as mock_put:
            mock_put_response = Mock()
            mock_put_response.status_code = 200
            mock_put.return_value = mock_put_response
            
            with patch('builtins.print') as mock_print:
                update_stock(item_id, new_quantity)
                mock_print.assert_called_once_with("Stock updated successfully!")
    
    def test_multiple_items_stock_management(self):
        """Test managing stock for multiple items"""
        items = [
            {"id": "ITEM001", "quantity": 10},
            {"id": "ITEM002", "quantity": 20},
            {"id": "ITEM003", "quantity": 30}
        ]
        
        with patch('ebay_inventory.requests.get') as mock_get:
            for item in items:
                mock_response = Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    "sku": item["id"],
                    "availability": {
                        "ship_to_location_availability": {
                            "quantity": item["quantity"]
                        }
                    }
                }
                mock_get.return_value = mock_response
                
                result = get_stock(item["id"])
                assert result["availability"]["ship_to_location_availability"]["quantity"] == item["quantity"]
    
    def test_error_recovery_pattern(self):
        """Test error handling and recovery pattern"""
        item_id = "TEST123"
        
        # First attempt fails
        with patch('ebay_inventory.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 503
            mock_response.text = "Service temporarily unavailable"
            mock_get.return_value = mock_response
            
            with pytest.raises(Exception):
                get_stock(item_id)
        
        # Second attempt succeeds
        with patch('ebay_inventory.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"sku": item_id, "quantity": 10}
            mock_get.return_value = mock_response
            
            result = get_stock(item_id)
            assert result["quantity"] == 10


class TestEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def test_extremely_long_item_id(self):
        """Test with extremely long item ID"""
        item_id = "A" * 1000
        
        with patch('ebay_inventory.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"sku": item_id}
            mock_get.return_value = mock_response
            
            result = get_stock(item_id)
            assert result["sku"] == item_id
    
    def test_unicode_characters_in_item_id(self):
        """Test with unicode characters in item ID"""
        item_id = "测试物品123"
        
        with patch('ebay_inventory.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"sku": item_id}
            mock_get.return_value = mock_response
            
            result = get_stock(item_id)
            assert result["sku"] == item_id
    
    def test_get_stock_with_none_item_id(self):
        """Test get_stock with None as item ID"""
        item_id = None
        
        with patch('ebay_inventory.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {}
            mock_get.return_value = mock_response
            
            # This will construct URL with None, which might be handled by requests
            result = get_stock(item_id)
            assert result == {}
    
    def test_update_stock_with_none_quantity(self):
        """Test update_stock with None as quantity"""
        item_id = "TEST123"
        quantity = None
        
        with patch('ebay_inventory.requests.put') as mock_put:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_put.return_value = mock_response
            
            with patch('builtins.print') as mock_print:
                update_stock(item_id, quantity)
                mock_print.assert_called_once()
    
    def test_response_with_missing_expected_fields(self):
        """Test handling of response with missing expected fields"""
        item_id = "TEST123"
        incomplete_data = {"sku": item_id}  # Missing availability field
        
        with patch('ebay_inventory.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = incomplete_data
            mock_get.return_value = mock_response
            
            result = get_stock(item_id)
            assert result == incomplete_data
            assert "availability" not in result
    
    def test_rate_limiting_response(self):
        """Test handling of rate limiting (429 Too Many Requests)"""
        item_id = "TEST123"
        
        with patch('ebay_inventory.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 429
            mock_response.text = "Rate limit exceeded"
            mock_get.return_value = mock_response
            
            with pytest.raises(Exception) as exc_info:
                get_stock(item_id)
            
            assert "Error fetching stock: Rate limit exceeded" in str(exc_info.value)
    
    def test_empty_response_body(self):
        """Test handling of empty response body"""
        item_id = "TEST123"
        
        with patch('ebay_inventory.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {}
            mock_get.return_value = mock_response
            
            result = get_stock(item_id)
            assert result == {}
    
    def test_malformed_url_characters(self):
        """Test with characters that might break URL encoding"""
        item_id = "test%20item&foo=bar"
        
        with patch('ebay_inventory.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"sku": item_id}
            mock_get.return_value = mock_response
            
            result = get_stock(item_id)
            assert result["sku"] == item_id


class TestAccessTokenHandling:
    """Test ACCESS_TOKEN usage and security"""
    
    def test_access_token_is_included_in_request(self):
        """Test that ACCESS_TOKEN is included in the authorization header"""
        item_id = "TEST123"
        
        with patch('ebay_inventory.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {}
            mock_get.return_value = mock_response
            
            get_stock(item_id)
            
            call_args = mock_get.call_args
            headers = call_args[1]['headers']
            assert 'Authorization' in headers
            assert f'Bearer {ACCESS_TOKEN}' == headers['Authorization']
    
    def test_access_token_format_in_update_request(self):
        """Test ACCESS_TOKEN format in update stock request"""
        item_id = "TEST123"
        quantity = 10
        
        with patch('ebay_inventory.requests.put') as mock_put:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_put.return_value = mock_response
            
            update_stock(item_id, quantity)
            
            call_args = mock_put.call_args
            headers = call_args[1]['headers']
            assert headers['Authorization'] == f'Bearer {ACCESS_TOKEN}'
            assert headers['Authorization'].startswith('Bearer ')