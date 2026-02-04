# event_loop.py

import heapq

class EventLoop:
    def __init__(self, sim_state):
        self.state = sim_state
        self.event_queue = []

    def schedule(self, event):
        heapq.heappush(self.event_queue, (event.timestamp, event))

    def run(self, until: int):
        while self.event_queue and self.state.time <= until:
            _, event = heapq.heappop(self.event_queue)
            self.state.time = event.timestamp
            self._dispatch(event)

    def _dispatch(self, event):
        # Placeholder
        pass
