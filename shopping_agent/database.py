"""
Database layer for the shopping agent.

This module uses SQLite to persist orders and metrics.
"""
import sqlite3
from contextlib import closing
from typing import List, Dict, Tuple
from datetime import datetime

# Path to the SQLite database file. This will create the file in the working directory.
DB_PATH = "shopping_agent.db"

def initialize_db() -> None:
    """Create required tables if they do not exist."""
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.cursor()
        # create orders table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                date TEXT NOT NULL
            )
            """
        )
        # create metrics table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                count INTEGER,
                avg_margin REAL
            )
            """
        )
        conn.commit()


def insert_orders(orders: List[Dict]) -> None:
    """Insert a list of orders into the database.

    Each order should be a dict with keys: name, price, date.
    """
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.cursor()
        for order in orders:
            cur.execute(
                "INSERT INTO orders (name, price, date) VALUES (?, ?, ?)",
                (order["name"], float(order["price"]), order.get("date", "")),
            )
        conn.commit()


def insert_metrics(count: int, avg_margin: float) -> None:
    """Insert a metrics record into the database."""
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO metrics (timestamp, count, avg_margin) VALUES (?, ?, ?)",
            (datetime.utcnow().isoformat(), count, avg_margin),
        )
        conn.commit()


def fetch_metrics() -> List[Tuple]:
    """Return all metrics records as a list of tuples."""
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.cursor()
        return cur.execute("SELECT * FROM metrics").fetchall()
