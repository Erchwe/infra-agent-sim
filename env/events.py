# events.py

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class Event:
    timestamp: int
    event_type: str
    source: str
    payload: Dict[str, Any]
