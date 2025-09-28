"""
Fake Amazon API for testing the shopping agent.

This module provides stub functions that return fake data for orders,
cart items, and wishlist items. In a real implementation, these functions
would access the Amazon API or scrape data.
"""
from typing import List, Dict
import datetime

def get_recent_orders() -> List[Dict]:
    """Return a list of recent Amazon orders with name, price, and date."""
    return [
        {"name": "PlayStation 5", "price": 499.0, "date": datetime.date.today().isoformat()},
        {"name": "Coffee Grinder", "price": 89.0, "date": datetime.date.today().isoformat()},
        {"name": "Kettlebell Set", "price": 120.0, "date": datetime.date.today().isoformat()},
    ]

def get_cart_items() -> List[Dict]:
    """Return the current items in the user's shopping cart."""
    return [
        {"name": "Wireless Mouse", "price": 25.0, "quantity": 1},
        {"name": "USB-C Cable", "price": 8.0, "quantity": 2},
    ]

def get_wishlist_items() -> List[str]:
    """Return a list of item names from the user's wishlist."""
    return ["Mechanical Keyboard", "Noise Cancelling Headphones", "Fitness Tracker"]
