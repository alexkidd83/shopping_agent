"""
Evaluation hooks for the shopping agent.  This module provides simple
utilities to log performance metrics and could be expanded to include
automatic evaluation using a language model or analytics framework.
"""

from typing import Dict, Any
import csv
import os
import datetime


METRICS_FILE = os.path.join(os.getcwd(), "agent_metrics.csv")


def log_metrics(metrics: Dict[str, Any]) -> None:
    """
    Append a row of metrics to a CSV file.  Each run should call this
    function after the episode ends.
    """
    file_exists = os.path.exists(METRICS_FILE)
    with open(METRICS_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp"] + list(metrics.keys()))
        if not file_exists:
            writer.writeheader()
        row = {"timestamp": datetime.datetime.now().isoformat()}
        row.update(metrics)
        writer.writerow(row)


def compute_statistics() -> Dict[str, Any]:
    """
    Compute simple statistics over the collected metrics.  Returns a
    dictionary with aggregates such as average offers evaluated per run.
    """
    if not os.path.exists(METRICS_FILE):
        return {}
    counts = 0
    total_offers = 0
    total_listings = 0
    with open(METRICS_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            counts += 1
            total_offers += int(row.get("offers_evaluated", 0))
            total_listings += int(row.get("listings_created", 0))
    if counts == 0:
        return {}
    return {
        "runs": counts,
        "avg_offers_evaluated": total_offers / counts,
        "avg_listings_created": total_listings / counts,
    }
