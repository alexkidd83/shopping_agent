"""
Simple memory implementations for the shopping agent.

In a production system you would likely use a combination of in‑memory
structures, relational databases and vector stores to persist context
between runs.  This module provides lightweight placeholders to keep
track of the agent’s observations and decisions during a single session.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import json
import os


@dataclass
class Episode:
    """Represents a single run of the agent."""
    timestamp: str
    offers_evaluated: int = 0
    listings_created: int = 0
    notes: List[str] = field(default_factory=list)


class Memory:
    """
    Simple episodic and working memory.  Maintains a list of episodes
    and a working dictionary for the current run.
    """

    def __init__(self, persistence_path: Optional[str] = None) -> None:
        self.episodes: List[Episode] = []
        self.working_memory: Dict[str, Any] = {}
        self.persistence_path = persistence_path or os.path.join(
            os.getcwd(), "memory.json"
        )
        self._load()

    def _load(self) -> None:
        """Load persisted episodes from disk if available."""
        if os.path.exists(self.persistence_path):
            try:
                with open(self.persistence_path, "r") as f:
                    data = json.load(f)
                for ep_dict in data.get("episodes", []):
                    self.episodes.append(Episode(**ep_dict))
            except (IOError, json.JSONDecodeError):
                # If the file is corrupt or unreadable, start fresh
                self.episodes = []

    def _save(self) -> None:
        """Persist episodes to disk."""
        data = {"episodes": [ep.__dict__ for ep in self.episodes]}
        try:
            with open(self.persistence_path, "w") as f:
                json.dump(data, f)
        except IOError:
            pass

    def start_episode(self, timestamp: str) -> Episode:
        """Begin a new episode with the given timestamp."""
        episode = Episode(timestamp=timestamp)
        self.episodes.append(episode)
        return episode

    def end_episode(self, episode: Episode) -> None:
        """Finalize an episode and persist it to disk."""
        # In a more advanced system you might compute metrics here
        self._save()

    def remember(self, key: str, value: Any) -> None:
        """Store arbitrary data in working memory."""
        self.working_memory[key] = value

    def recall(self, key: str, default: Any = None) -> Any:
        """Retrieve data from working memory."""
        return self.working_memory.get(key, default)

    def reset_working_memory(self) -> None:
        """Clear the working memory for a new run."""
        self.working_memory = {}
