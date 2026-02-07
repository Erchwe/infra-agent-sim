# event_loop.py

import heapq
import csv
from env.events import Event
from pathlib import Path


class EventLoop:
    def __init__(self, sim_state):
        self.state = sim_state
        self._queue = []
        self._counter = 0

        results_dir = Path("results")
        results_dir.mkdir(exist_ok=True)

        self._metrics_file = open(results_dir / "metrics.csv", "w", newline="")
        self._metrics_writer = csv.writer(self._metrics_file)
        self._metrics_writer.writerow(
            ["time", "event_type", "source", "service_id", "stress_level", "resource_level"]
        )

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

    REACTION_EVENTS = {
        "FLOOD_IMPACT",
        "NORMAL_DEMAND",
        "DEMAND_SPIKE",
        "POLICY_INTERVENTION",
    }

    def run(self, until: int):
        while self._queue and self.state.time <= until:
            time, _, event = heapq.heappop(self._queue)
            self.state.time = time
            self._dispatch(event)

            if event.event_type in self.REACTION_EVENTS:
                snapshot = self.state.snapshot()
                for agent in self.state.agents.values():
                    agent.perceive(snapshot)
                    for intent in agent.decide():
                        self._schedule_intent(intent)

            self._log_metrics(event)
            self._log_state(event)

    def _log_state(self, event):
        print(f"[t={self.state.time}] {event.event_type} from {event.source}")
        for aid, agent in self.state.agents.items():
            print(aid, agent.state)
    
    def _log_metrics(self, event: Event):
        """
        Record post-event system state for audit and failure analysis.
        One row per service per event.
        """
        for agent_id, agent in self.state.agents.items():
            if agent.role != "service":
                continue

            self._metrics_writer.writerow([
                self.state.time,
                event.event_type,
                event.source,
                agent_id,
                agent.state.stress_level,
                agent.state.resource_level,
            ])

        self._metrics_file.flush()



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

        elif event.event_type == "POLICY_INTERVENTION":
            self._handle_policy_intervention(event)

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

    def _schedule_intent(self, event: Event):
        if event.event_type == "SERVICE_OVERLOAD":
            self.schedule(event, delay=1)

        elif event.event_type == "POLICY_INTENT":
            self.schedule(event, delay=event.payload["desired_delay"])

    def _handle_policy_intervention(self, event: Event):
        """
        Apply policy intervention effects and mark the intervention as completed.

        Policy interventions do not resolve failures directly.
        They inject limited resources into the system, after which
        recovery (or further failure) depends on service dynamics.
        """
        policy_agent = self.state.agents.get(event.source)
        if policy_agent is None:
            return

        budget_release = event.payload.get("budget_release", 0.0)

        # Distribute released budget uniformly to active services
        service_agents = [
            agent for agent in self.state.agents.values()
            if agent.role == "service" and agent.state.is_active
        ]

        if service_agents:
            per_service_boost = budget_release / len(service_agents)
            for service in service_agents:
                service.apply_local_effect(
                    delta_resource=per_service_boost,
                    delta_stress=0.0,
                )

        # Mark that the policy intervention has materialized
        policy_agent.mark_intervention_executed()



