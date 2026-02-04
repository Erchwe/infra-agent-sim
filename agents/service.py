# service.py

from agents.base import BaseAgent, AgentState


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

    def perceive(self, global_state):
        self.current_load = global_state.get("service_loads", {}).get(self.agent_id, 0)

    def decide(self):
        overload = max(0.0, self.current_load - self.capacity)
        stress_delta = overload / self.capacity if self.capacity > 0 else 1.0

        return [
            {
                "type": "SERVICE_STRESS_UPDATE",
                "target": self.agent_id,
                "delta_stress": stress_delta,
            }
        ]
