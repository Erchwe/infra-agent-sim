# base.py

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict


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
        Read-only perception of the world.
        No mutation allowed.
        """
        pass

    @abstractmethod
    def decide(self) -> list:
        """
        Returns a list of Events.
        Agent does NOT apply effects directly.
        """
        pass

    def apply_local_effect(self, delta_resource: float, delta_stress: float):
        """
        Explicit, auditable state change.
        """
        self.state.resource_level += delta_resource
        self.state.stress_level += delta_stress
