# event_loop.py

import heapq
from env.events import Event


class EventLoop:
    def __init__(self, sim_state):
        self.state = sim_state
        self._queue = []
        self._counter = 0  # deterministic tie-breaker

    def schedule(self, event: Event, delay: int):
        if delay is None or delay < 0:
            raise ValueError(
                "Explicit, non-negative delay is required. "
                "Timing must originate from domain intent."
            )
        
        scheduled = Event(
            event_type=event.event_type,
            source=event.source,
            payload=event.payload,
            scheduled_time=self.state.time + delay,
        )

        heapq.heappush(
            self._queue,
            (scheduled.scheduled_time, self._counter, scheduled),
        )
        self._counter += 1

    def run(self, until: int):
        while self._queue and self.state.time <= until:
            time, _, event = heapq.heappop(self._queue)
            self.state.time = time
            self._dispatch(event)
            self._log_state(event)

    def _log_state(self, event):
        print(f"[t={self.state.time}] {event.event_type} from {event.source}")
        for aid, agent in self.state.agents.items():
            print(aid, agent.state)

    def _handle_demand(self, event: Event):
        for service_id in self.state.service_loads:
            self.state.service_loads[service_id] += event.payload["intensity"]

    def _handle_service_overload(self, event: Event):
        agent = self.state.agents[event.source]
        agent.apply_local_effect(
            delta_resource=0.0,
            delta_stress=event.payload["delta_stress"],
        )

    def _handle_policy_intent(self, event: Event):
        delay = event.payload["desired_delay"]

        intervention_event = Event(
            event_type="POLICY_INTERVENTION",
            source=event.source,
            payload={"budget_release": event.payload["budget_release"]},
        )

        self.schedule(intervention_event, delay=delay)

    def _dispatch(self, event: Event):
        if event.event_type in ("NORMAL_DEMAND", "DEMAND_SPIKE"):
            self._handle_demand(event)

        elif event.event_type == "SERVICE_OVERLOAD":
            self._handle_service_overload(event)

        elif event.event_type == "POLICY_INTENT":
            self._handle_policy_intent(event)

        elif event.event_type == "FLOOD_IMPACT":
            self._handle_flood_impact(event)

    def _handle_flood_impact(self, event: Event):
        intensity = event.payload["intensity"]
        affected = event.payload["affected_services"]

        # Flood does NOT directly increase stress.
        # It perturbs capacity and load; stress emerges via overload.
        for sid in affected:
            # Increase load (e.g., evacuation, emergency calls)
            self.state.service_loads[sid] = (
                self.state.service_loads.get(sid, 0.0) + intensity
            )

            # Temporary capacity degradation (modeled as resource drain)
            service = self.state.agents.get(sid)
            if service:
                service.apply_local_effect(
                    delta_resource=-0.1 * intensity,  # simple, explicit
                    delta_stress=0.0,
                )



