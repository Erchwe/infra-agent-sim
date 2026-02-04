# events.py

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class Event:
    """
    Domain event produced by agents or environment.
    Time is assigned by the scheduler, not by agents.
    """
    event_type: str
    source: str
    payload: Dict[str, Any]
    scheduled_time: Optional[int] = None
