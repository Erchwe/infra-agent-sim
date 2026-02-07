# Failure Analysis — Flood Overload Scenario

## Purpose

This document provides a post-hoc analysis of a single simulated failure episode.
It is not an evaluation report, performance benchmark, or predictive assessment.

The goal is to understand **how localized coordination failure emerges under stress**
within a controlled, deterministic system.

This analysis is aligned with the project’s stated intent:
to explore failure modes, not to forecast outcomes.

---

## Scenario Context

The scenario introduces a flood as an exogenous environmental stressor.
The flood does not directly impose institutional stress; instead, it perturbs
system conditions by reducing effective service capacity and increasing demand pressure.

Key characteristics:

- External shock is non-strategic and non-adaptive.
- All agents operate on partial, delayed information.
- System evolution is fully deterministic.
- No learning or optimization occurs during execution.

---

## Event Timeline

Based on the logged system state:

- **t = 1**  
  Flood impact degrades resource availability across affected services.

- **t = 1**  
  Normal citizen demand is issued under degraded conditions.

- **t = 2**  
  The emergency service reports a single overload event.

- **t > 2**  
  No additional overload events are emitted.

Overload reporting is edge-triggered and intentionally debounced.
Repeated signaling is suppressed to avoid artificial escalation.

---

## Service-Level Effects

The emergency service becomes overloaded due to the combined effect of:

- reduced available resources, and
- sustained baseline demand.

Other services remain operational and do not accumulate stress.

Observed properties:

- Stress accumulation is localized.
- No cross-service contagion occurs.
- No secondary failures are observed.

This episode therefore represents a **localized service failure**, not a systemic cascade.

---

## Policy Dynamics

The policy agent monitors aggregate system stress using coarse indicators.
At observed stress levels, the intervention threshold is not crossed.

As a result:

- No policy intervention is scheduled.
- No resources are reallocated.
- The system remains degraded but stable.

This behavior is intentional.
Policy latency and conservative thresholds are treated as structural features,
not deficiencies.

---

## Graph-Based Structural Reasoning

After simulation, a graph-based reasoning layer is applied to interpret the observed failure.

### Inputs

- A service dependency graph.
- Node features derived from logged stress and resource levels.

### Method

A Graph Attention Network (GAT) is used in inference-only mode
to highlight dominant structural dependencies and risk salience.

The reasoning model:

- does not predict outcomes,
- does not influence agent behavior,
- does not adapt across runs.

Its role is interpretive rather than authoritative.

### Observations

The reasoning output indicates:

- elevated salience at the emergency service node,
- low attention weights along dependency edges,
- minimal propagation of stress through the graph.

This supports the conclusion that the failure remains **structurally contained**.

---

## Failure Characterization

This episode is best described as:

- a **capacity bottleneck**, not a coordination collapse;
- a **localized overload**, not a systemic failure;
- a **recoverable stress state**, not irreversible breakdown.

The system fails locally before governance mechanisms are activated.
This mirrors real-world public systems, where institutional response often lags
behind operational strain.

---

## Key Insights

- Failure does not require system-wide collapse.
- Conservative policy thresholds delay intervention by design.
- Local overload can exist without cascading failure.
- Structural reasoning can distinguish localized stress from systemic risk
  without predictive claims.

---

## Limitations

- The scenario is intentionally constrained.
- No adaptive or learning behavior is present.
- Dependency structures are simplified.
- Results are illustrative rather than predictive.

These limitations are consistent with the system’s stated design boundaries.

---

## Conclusion

This failure episode demonstrates how **localized institutional stress can surface
under environmental pressure without escalating into systemic collapse**.

The absence of cascading failure is not treated as success or failure,
but as an observed structural outcome.

The value of the simulation lies in making such outcomes explicit,
traceable, and explainable — not in optimizing or predicting them.
