# base.py

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class AgentState:
    resource_level: float
    stress_level: float
    is_active: bool = True


class BaseAgent(ABC):
    def __init__(self, agent_id: str, role: str, initial_state: AgentState):
        self.agent_id = agent_id
        self.role = role
        self.state = initial_state

    @abstractmethod
    def perceive(self, global_state: Dict[str, Any]) -> None:
        """
        Read-only perception.
        """
        pass

    @abstractmethod
    def decide(self) -> List["Event"]:
        """
        Produce intent as domain events.
        NO timing. NO side effects.
        """
        pass

    def apply_local_effect(self, delta_resource: float, delta_stress: float):
        self.state.resource_level += delta_resource
        self.state.stress_level += delta_stress
