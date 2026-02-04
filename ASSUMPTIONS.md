# ASSUMPTIONS

- Agents act on partial, delayed information.
  This intentionally models institutional latency and information asymmetry
  common in public systems, where no single actor has a complete or current view
  of system state.

- All events are processed deterministically.
  This enables post-hoc auditability and reproducible failure analysis,
  at the cost of reduced stochastic realism and behavioral variance.

- This system prioritizes explainability over realism.
  Complex behaviors are simplified or omitted if their effects cannot be
  causally traced through explicit state transitions.
