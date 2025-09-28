"""
Orchestration logic for the shopping agent.  This module glues together
the various tools and the memory subsystem to perform a single run of
the workflow: fetch Amazon data, compare prices, decide on resale, create
eBay listings and send a summary email.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import List

from . import memory
from .tools import amazon_api, idealo_api, ebay_api, email


@dataclass
class Deal:
    item_name: str
    purchase_price: str
    competitor_price: str
    resale_price: str
    listing_id: str | None = None


class Orchestrator:
    def __init__(self, mem: memory.Memory, profit_margin: float = 0.15) -> None:
        self.mem = mem
        self.profit_margin = profit_margin

    def run(self) -> None:
        """
        Execute a single iteration of the agent workflow.  This method does
        not return anything; it performs side effects such as creating
        listings and sending emails.
        """
        timestamp = datetime.datetime.now().isoformat()
        episode = self.mem.start_episode(timestamp)
        self.mem.reset_working_memory()

        # Step 1: gather items from Amazon
        orders = amazon_api.get_recent_orders()
        cart = amazon_api.get_cart_items()
        wishlist = amazon_api.get_wishlist_items()
        all_items = []
        for collection in (orders, cart, wishlist):
            for item in collection:
                all_items.append(item)

        self.mem.remember("items_fetched", len(all_items))

        deals: List[Deal] = []
        for item in all_items:
            name = item["item"]
            purchase_price = item["price"]
            # Step 2: get competitor price
            comp = idealo_api.get_lowest_price(name)
            competitor_price = comp["price"]
            # Compute resale price: competitor price plus margin
            purchase_value = _parse_eur(purchase_price)
            competitor_value = _parse_eur(competitor_price)
            if purchase_value is None or competitor_value is None:
                continue
            target_price = competitor_value * (1 + self.profit_margin)
            resale_price_str = f"€{target_price:.2f}"
            # Step 3: decide whether to list (if profit is positive)
            if target_price > purchase_value:
                listing = ebay_api.create_listing(name, purchase_price, resale_price_str)
                deals.append(
                    Deal(
                        item_name=name,
                        purchase_price=purchase_price,
                        competitor_price=competitor_price,
                        resale_price=resale_price_str,
                        listing_id=listing["listing_id"],
                    )
                )
                episode.listings_created += 1
            episode.offers_evaluated += 1

        # Step 4: notify user
        self._notify_user(deals)
        # Step 5: finalize episode
        self.mem.end_episode(episode)

    def _notify_user(self, deals: List[Deal]) -> None:
        if not deals:
            subject = "Shopping Agent Report: No deals found"
            body = "No profitable resale opportunities were detected during this run."
        else:
            subject = "Shopping Agent Report: Deals Available"
            lines = [
                "The agent found the following items that can be resold for a profit:\n",
            ]
            for deal in deals:
                lines.append(
                    f"- {deal.item_name}: bought for {deal.purchase_price}, competitor price {deal.competitor_price}, listing at {deal.resale_price} (ID {deal.listing_id})"
                )
            body = "\n".join(lines)
        email.send_email(subject, body, recipients=["user@example.com"])


def _parse_eur(price_str: str) -> float | None:
    """
    Convert a price string like "€25.00" to a float.  Returns None on
    failure.
    """
    try:
        return float(price_str.replace("€", "").replace(",", "."))
    except ValueError:
        return None
