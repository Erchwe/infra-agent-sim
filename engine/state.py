# state.py

class SimulationState:
    def __init__(self):
        self.time = 0
        self.agents = {}
        self.service_loads = {}

    def register_agent(self, agent):
        self.agents[agent.agent_id] = agent

    def snapshot(self):
        return {
            "time": self.time,
            "agents": {
                aid: agent.state for aid, agent in self.agents.items()
            },
            "service_loads": dict(self.service_loads),
        }
