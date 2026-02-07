# ASSUMPTIONS

- Agents act on partial, delayed information.
  This intentionally models institutional latency and information asymmetry
  common in public systems, where no single actor has a complete or current
  view of system state at decision time.

- All events are processed deterministically.
  This allows full replayability and post-hoc audit of failure sequences,
  at the cost of reduced stochastic realism and behavioral variance.

- Timing is treated as a system-level concern.
  Agents may express desired delays as part of domain intent, but have no
  authority over scheduling or execution order.

- This system prioritizes explainability over realism.
  Complex behaviors are simplified or omitted if their effects cannot be
  causally traced through explicit state transitions and events.

- Machine learning is used strictly for post-hoc interpretation.
  Graph-based models analyze observed failure episodes to highlight
  structural risk propagation, but do not influence agent decisions,
  event scheduling, or system evolution.
