from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class MoodEntry:
    """Represents a single mood log entry."""

    timestamp: datetime
    rating: int              # 1–10
    tag: str | None = None   # e.g. "anxious", "content"
    note: str | None = None  # free text note

    def to_dict(self) -> dict:
        """Convert entry to a JSON-serializable dict."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "rating": self.rating,
            "tag": self.tag,
            "note": self.note,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "MoodEntry":
        """Create a MoodEntry from a dict."""
        return cls(
            timestamp=datetime.fromisoformat(data["timestamp"]),
            rating=int(data["rating"]),
            tag=data.get("tag"),
            note=data.get("note"),
        )