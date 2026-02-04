# citizen.py

from agents.base import BaseAgent, AgentState
from env.events import Event


class CitizenAgent(BaseAgent):
    def __init__(
        self,
        agent_id: str,
        demand_profile: float,
        panic_threshold: float,
    ):
        super().__init__(
            agent_id=agent_id,
            role="citizen",
            initial_state=AgentState(resource_level=1.0, stress_level=0.0),
        )
        self.demand_profile = demand_profile
        self.panic_threshold = panic_threshold
        self.perceived_stress = 0.0

    def perceive(self, global_state):
        self.perceived_stress = global_state["agents"][self.agent_id].stress_level

    def decide(self):
        if self.perceived_stress >= self.panic_threshold:
            intensity = self.demand_profile * 2
            event_type = "DEMAND_SPIKE"
        else:
            intensity = self.demand_profile
            event_type = "NORMAL_DEMAND"

        return [
            Event(
                event_type=event_type,
                source=self.agent_id,
                payload={"intensity": intensity},
            )
        ]
