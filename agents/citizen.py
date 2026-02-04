# citizen.py

from agents.base import BaseAgent, AgentState
from env.events import Event
import random


class CitizenAgent(BaseAgent):
    def __init__(
        self,
        agent_id: str,
        demand_profile: float,
        panic_threshold: float,
        compliance_probability: float,
    ):
        super().__init__(
            agent_id=agent_id,
            role="citizen",
            initial_state=AgentState(resource_level=1.0, stress_level=0.0),
        )
        self.demand_profile = demand_profile
        self.panic_threshold = panic_threshold
        self.compliance_probability = compliance_probability

    def perceive(self, global_state):
        self.perceived_stress = global_state["agents"][self.agent_id].stress_level

    def decide(self):
        events = []

        if self.perceived_stress >= self.panic_threshold:
            events.append(
                Event(
                    timestamp=global_state["time"] + 1,
                    event_type="DEMAND_SPIKE",
                    source=self.agent_id,
                    payload={"intensity": self.demand_profile * 2},
                )
            )
        else:
            events.append(
                Event(
                    timestamp=global_state["time"] + 1,
                    event_type="NORMAL_DEMAND",
                    source=self.agent_id,
                    payload={"intensity": self.demand_profile},
                )
            )

        return events
