import requests

# Configuration - Replace with your actual eBay API access token
ACCESS_TOKEN = "YOUR_EBAY_ACCESS_TOKEN"


# Fetch stock using Inventory API
def get_stock(item_id):
    url = f"https://api.ebay.com/sell/inventory/v1/inventory_item/{item_id}"
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json',
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()  # Stock Data
    else:
        raise Exception(f"Error fetching stock: {response.text}")


# Update stock for an item
def update_stock(item_id, quantity):
    url = f"https://api.ebay.com/sell/inventory/v1/inventory_item/{item_id}"
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json',
    }
    data = {
        "availability": {
            "ship_to_location_availability": {
                "quantity": quantity
            }
        }
    }

    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 200 or response.status_code == 204:
        print("Stock updated successfully!")
    else:
        raise Exception(f"Error updating stock: {response.text}")
