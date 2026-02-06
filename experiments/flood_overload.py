from agents.citizen import CitizenAgent
from agents.service import ServiceAgent
from agents.policy import PolicyAgent
from engine.event_loop import EventLoop
from engine.state import SimulationState
from env.flood import FloodEnvironment
from env.events import Event

# --- Setup state ---
state = SimulationState()

# Services (kecil, bermakna)
services = {
    "transport": ServiceAgent("transport", capacity=5.0, dependencies=[]),
    "emergency": ServiceAgent("emergency", capacity=3.0, dependencies=["transport"]),
    "power": ServiceAgent("power", capacity=4.0, dependencies=[]),
}

for s in services.values():
    state.register_agent(s)
    state.service_loads[s.agent_id] = 0.0

# Citizens
citizen = CitizenAgent(
    agent_id="citizen:1",
    demand_profile=1.0,
    panic_threshold=1.5,
)
state.register_agent(citizen)

# Policy (intentionally delayed)
policy = PolicyAgent(
    agent_id="policy:central",
    intervention_delay=3,
    budget=1.0,
)
state.register_agent(policy)

# --- Event loop ---
loop = EventLoop(state)

# Flood environment
flood = FloodEnvironment(
    intensity=1.0,
    duration=3,
    affected_services=["transport", "emergency"],
)

# Schedule flood events explicitly
for ev in flood.emit_events():
    loop.schedule(ev, delay=1)  # explicit delay: environment impact cadence

# Initial demand tick
loop.schedule(
    Event(
        event_type="NORMAL_DEMAND",
        source="citizen:1",
        payload={"intensity": 1.0},
    ),
    delay=1,
)

# Run
loop.run(until=10)
