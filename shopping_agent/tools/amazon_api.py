"""
Stubbed interface for interacting with Amazon.  In a real implementation
this module would authenticate via Amazon’s API (if available) or use
web scraping techniques to retrieve order history, current cart items and
wishlist data.  The functions below return static data to illustrate
the expected shape of responses.
"""

from typing import List, Dict
import datetime


def get_recent_orders() -> List[Dict[str, str]]:
    """
    Return a list of recent orders.  Each order includes an item name and
    the purchase price.  In practice, you would include order date,
    quantity, ASIN and other relevant metadata.
    """
    # Mocked data
    return [
        {
            "order_id": "123-4567890-1234567",
            "item": "Wireless Mouse",
            "price": "€25.00",
            "purchase_date": (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat(),
        },
        {
            "order_id": "123-4567890-7654321",
            "item": "USB-C Cable",
            "price": "€8.99",
            "purchase_date": (datetime.datetime.now() - datetime.timedelta(days=3)).isoformat(),
        },
    ]


def get_cart_items() -> List[Dict[str, str]]:
    """
    Return a list of items currently in the user's Amazon cart.  Each item
    includes a name and current Amazon price.
    """
    return [
        {
            "asin": "B08CFSZLQ4",
            "item": "Bluetooth Headphones",
            "price": "€59.99",
        },
        {
            "asin": "B07PGL2N7J",
            "item": "Portable SSD",
            "price": "€129.95",
        },
    ]


def get_wishlist_items() -> List[Dict[str, str]]:
    """
    Return a list of items saved for later or on the wishlist.  This
    provides additional candidates for deal hunting.
    """
    return [
        {
            "asin": "B09G3HRMVB",
            "item": "Smartwatch",
            "price": "€199.99",
        }
    ]
