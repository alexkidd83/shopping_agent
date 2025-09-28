"""
Stubbed interface for price comparisons using Idealo.de.  A real
implementation would likely perform HTTP requests to Idealo’s API (if
available) or scrape search results to find the lowest price for a given
product.  For demonstration purposes this module returns mocked prices
based on simple heuristics.
"""

from typing import Dict
import random


def get_lowest_price(item_name: str) -> Dict[str, str]:
    """
    Return a mocked lowest price for the given item.  The response
    includes the vendor name and the price as a string.  In practice,
    additional fields such as shipping cost and delivery time may be
    returned.
    """
    # Simulate a competitive price that is between 50% and 90% of the
    # original price.  This is a naive heuristic for demonstration.
    base_price = _extract_price(item_name)
    if base_price is None:
        price_eur = round(random.uniform(10.0, 100.0), 2)
    else:
        price_eur = round(base_price * random.uniform(0.5, 0.9), 2)
    return {
        "vendor": "Idealo Vendor",
        "price": f"€{price_eur:.2f}",
    }


def _extract_price(item_name: str) -> float | None:
    """
    Extract a numeric price from a string if it appears to contain one.
    This helper is purely for mocking and has no place in a production
    system.
    """
    # Attempt to parse a number in the item name (e.g., "€25.00").  This
    # will not work for most product names and will return None.
    digits = "".join(c for c in item_name if c.isdigit() or c in {".", ","})
    try:
        return float(digits.replace(",", "."))
    except ValueError:
        return None
