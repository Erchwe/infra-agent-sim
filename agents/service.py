# service.py

from agents.base import BaseAgent, AgentState
from env.events import Event


class ServiceAgent(BaseAgent):
    def __init__(
        self,
        agent_id: str,
        capacity: float,
        dependencies: list[str],
        overload_threshold: float = 1.0,
        stress_increment: float = 0.3333333333333333,
    ):
        super().__init__(
            agent_id=agent_id,
            role="service",
            initial_state=AgentState(
                resource_level=capacity,
                stress_level=0.0,
            ),
        )
        self.capacity = capacity
        self.dependencies = dependencies
        self.overload_threshold = overload_threshold
        self.stress_increment = stress_increment

        # Debounce flag: has overload already been reported?
        self._overload_reported = False

    def perceive(self, global_state):
        self.current_load = global_state.get("service_loads", {}).get(self.agent_id, 0.0)

    def decide(self):
        if self.current_load > self.capacity:
            if not self._overload_reported:
                self._overload_reported = True
                return [
                    Event(
                        event_type="SERVICE_OVERLOAD",
                        source=self.agent_id,
                        payload={"delta_stress": self.stress_increment},
                    )
                ]
        return []


    
    def apply_local_effect(self, delta_resource: float, delta_stress: float):
        """
        Apply state mutation as a result of system-level events.
        """
        self.state.resource_level += delta_resource
        self.state.stress_level += delta_stress

        # Reset debounce only if service has recovered
        if self.state.stress_level < self.overload_threshold:
            self._overload_reported = False