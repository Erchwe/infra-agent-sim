# policy.py

from agents.base import BaseAgent, AgentState
from env.events import Event


class PolicyAgent(BaseAgent):
    def __init__(
        self,
        agent_id: str,
        intervention_delay: int,
        budget: float,
    ):
        super().__init__(
            agent_id=agent_id,
            role="policy",
            initial_state=AgentState(resource_level=budget, stress_level=0.0),
        )
        self.intervention_delay = intervention_delay
        self.observed_system_stress = 0.0

    def perceive(self, global_state):
        # Still simplified; partial observability can come later
        self.observed_system_stress = sum(
            a.stress_level for a in global_state["agents"].values()
        )

    def decide(self):
        if self.observed_system_stress <= 1.0:
            return []

        if self.state.resource_level <= 0:
            return []

        return [
            Event(
                event_type="POLICY_INTENT",
                source=self.agent_id,
                payload={
                    "desired_delay": self.intervention_delay,
                    "budget_release": 0.2,
                },
            )
        ]
