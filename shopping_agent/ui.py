# Simple command-line interface (CLI) for the shopping agent.

import sys
from .memory import Memory
from .orchestrator import Orchestrator
from .eval import log_metrics, compute_statistics


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print("Usage: python3 -m shopping_agent.ui [run|stats]")
        return
    cmd = argv[0]
    if cmd == "run":
        # Execute a single iteration
        mem = Memory()
        orchestrator = Orchestrator(mem)
        orchestrator.run()
        # Log metrics
        if mem.episodes:
            ep = mem.episodes[-1]
            log_metrics(
                {
                    "offers_evaluated": ep.offers_evaluated,
                    "listings_created": ep.listings_created,
                }
            )
    elif cmd == "stats":
        stats = compute_statistics()
        if not stats:
            print("No metrics available yet.")
        else:
            print("Run statistics:")
            for k, v in stats.items():
                print(f"{k}: {v}")
    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
