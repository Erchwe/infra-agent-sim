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

    def perceive(self, global_state):
        self.system_stress = sum(
            a.stress_level for a in global_state["agents"].values()
        )

    def decide(self):
        if self.system_stress > 1.0 and self.state.resource_level > 0:
            return [
                Event(
                    timestamp=global_state["time"] + self.intervention_delay,
                    event_type="POLICY_INTERVENTION",
                    source=self.agent_id,
                    payload={"budget_release": 0.2},
                )
            ]
        return []
