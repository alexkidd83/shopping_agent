import pytest
from shopping_agent.tools import amazon_api, idealo_api, email, ebay_api
import shopping_agent.database as db
from shopping_agent.memory import Memory
from shopping_agent.orchestrator import Orchestrator


def test_amazon_recent_orders():
    orders = amazon_api.get_recent_orders()
    assert isinstance(orders, list)
    assert orders, "No orders returned"
    for order in orders:
        assert "name" in order and "price" in order and "date" in order


def test_idealo_find_lowest_price():
    price = idealo_api.find_lowest_price("PlayStation 5")
    assert isinstance(price, float)
    assert price > 0


def test_email_send(capsys):
    email.send_email("Test Subject", "Test Body")
    captured = capsys.readouterr()
    assert "Test Subject" in captured.out
    assert "Test Body" in captured.out


def test_database_in_memory(monkeypatch):
    # use in-memory SQLite database
    monkeypatch.setattr(db, "DB_PATH", ":memory:")
    db.initialize_db()
    orders = [{"name": "Test Item", "price": "10.0", "date": "2025-01-01"}]
    db.insert_orders(orders)
    db.insert_metrics(1, 15.5)
    metrics = db.fetch_metrics()
    assert metrics[-1][2] == 1
    assert metrics[-1][3] == 15.5


def test_orchestrator_run(monkeypatch, capsys):
    # stub Amazon functions to return predictable data
    monkeypatch.setattr(amazon_api, "get_recent_orders", lambda: [{"name": "Test Item", "price": "€100.00"}])
    monkeypatch.setattr(amazon_api, "get_cart_items", lambda: [])
    monkeypatch.setattr(amazon_api, "get_wishlist_items", lambda: [])
    # stub Idealo to return 50.0 price
    monkeypatch.setattr(idealo_api, "get_lowest_price", lambda name: {"vendor": "Mock Vendor", "price": "50.0"})
    # stub eBay create_listing
    monkeypatch.setattr(ebay_api, "create_listing", lambda title, purchase_price, resale_price: {
        "listing_id": "abc123",
        "title": title,
        "purchase_price": purchase_price,
        "resale_price": resale_price,
        "status": "listed"
    })
    mem = Memory()
    orchestrator = Orchestrator(mem)
    orchestrator.run()
    captured = capsys.readouterr()
    assert "Test Item" in captured.out
