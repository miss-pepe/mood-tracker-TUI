from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import json
from typing import List, Dict, Any

DATA_PATH = Path.home() / ".mood_tracker"
DATA_FILE = DATA_PATH / "moods.json"


@dataclass
class MoodEntry:
    timestamp: datetime
    score: int             # 1–10
    tag: str | None = None
    note: str | None = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "score": self.score,
            "tag": self.tag,
            "note": self.note,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MoodEntry":
        return cls(
            timestamp=datetime.fromisoformat(data["timestamp"]),
            score=int(data["score"]),
            tag=data.get("tag"),
            note=data.get("note"),
        )


def init_storage() -> None:
    """Ensure data folder/file exist."""
    DATA_PATH.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf-8")


def load_moods() -> List[MoodEntry]:
    init_storage()
    raw = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return [MoodEntry.from_dict(item) for item in raw]


def save_moods(entries: List[MoodEntry]) -> None:
    init_storage()
    payload = [entry.to_dict() for entry in entries]
    DATA_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")
