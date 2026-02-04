# service.py

from agents.base import BaseAgent, AgentState
from env.events import Event


class ServiceAgent(BaseAgent):
    def __init__(
        self,
        agent_id: str,
        capacity: float,
        dependencies: list[str],
    ):
        super().__init__(
            agent_id=agent_id,
            role="service",
            initial_state=AgentState(resource_level=capacity, stress_level=0.0),
        )
        self.capacity = capacity
        self.dependencies = dependencies
        self.current_load = 0.0

    def perceive(self, global_state):
        self.current_load = global_state.get("service_loads", {}).get(self.agent_id, 0.0)

    def decide(self):
        overload = max(0.0, self.current_load - self.capacity)

        if overload <= 0:
            return []

        stress_delta = overload / self.capacity

        return [
            Event(
                event_type="SERVICE_OVERLOAD",
                source=self.agent_id,
                payload={"delta_stress": stress_delta},
            )
        ]
