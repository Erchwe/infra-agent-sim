# flood.py

from env.events import Event


class FloodEnvironment:
    """
    Non-agent stressor.
    Emits flood impact events for a fixed duration.
    """

    def __init__(self, intensity: float, duration: int, affected_services: list[str]):
        self.intensity = intensity
        self.duration = duration
        self.affected_services = affected_services

    def emit_events(self):
        """
        Yield intent-only events. Scheduling is handled by EventLoop.
        """
        for t in range(self.duration):
            yield Event(
                event_type="FLOOD_IMPACT",
                source="environment:flood",
                payload={
                    "intensity": self.intensity,
                    "affected_services": self.affected_services,
                },
            )
