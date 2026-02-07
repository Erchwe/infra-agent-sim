# policy.py

from agents.base import BaseAgent, AgentState
from env.events import Event


class PolicyAgent(BaseAgent):
    def __init__(
        self,
        agent_id: str,
        intervention_delay: int,
        budget: float,
        stress_threshold: float = 1.0,

    ):
        super().__init__(
            agent_id=agent_id,
            role="policy",
            initial_state=AgentState(
                resource_level=budget,
                stress_level=0.0,
            ),
        )
        self.intervention_delay = intervention_delay
        self.stress_threshold = stress_threshold

        # Debounce flag: is an intervention already pending?        
        self._intervention_pending = False
        self.observed_system_stress = 0.0

    def perceive(self, global_state):
        """
        Policy observes aggregate system stress.
        """
        self.observed_system_stress = sum(
            state.stress_level
            for state in global_state["agents"].values()
            if state.is_active
        )

    def decide(self):
        """
        Emit intervention intent once per stress episode.
        """
        if self.observed_system_stress > self.stress_threshold:
            if not self._intervention_pending:
                self._intervention_pending = True
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

        return []

    def mark_intervention_executed(self):
        """
        Called by the system once intervention effects are applied.
        """
        self._intervention_pending = False

