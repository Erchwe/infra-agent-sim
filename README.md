# Multi-Agent Infrastructure Stress Simulator

## Problem
Public systems fail under stress not because of lack of intelligence,
but because of coordination breakdown.

Failures often emerge from delayed responses, partial information,
and misaligned institutional incentives rather than from incorrect decisions.

---

## Why Simulation (Not Prediction)
We are not forecasting outcomes.  
We are exploring failure modes under controlled stress.

Machine learning is used to analyze failures after they occur,
not to predict or prevent them.

Simulation is chosen to make system boundaries, delays, and
coordination breakdowns explicit and auditable.

---

## System Design

The system is designed around explicit boundaries between agents,
events, and execution authority.

Agents express intent through domain events.
They do not mutate global state and do not control time.

All state mutation, event ordering, and scheduling decisions
are handled centrally by the simulation engine.

This separation ensures determinism, traceability, and
post-hoc auditability.

---

## Graph Reasoning (Post-hoc Analysis)

This system includes an optional graph-based reasoning layer to interpret
observed failure episodes.

A service dependency graph is constructed from the simulated system state.
Node features derived from logged stress and resource levels are analyzed
using a Graph Attention Network (GAT) to highlight dominant dependency paths
and structural risk propagation.

This model is not trained, does not predict outcomes, and does not influence
agent behavior or event scheduling.

Its role is interpretive rather than authoritative, supporting
post-mortem analysis rather than decision-making.

---

### Timing and Latency

Timing is treated as a property of the system, not of individual agents.

Agents may express intent and desired delays, but scheduling authority
remains centralized and deterministic.

This design reflects real-world public systems, where outcomes are shaped
not only by decisions, but by institutional latency and coordination delay.

---

## Running the Simulation

This repository is designed to be executed as a deterministic simulation,
not as a long-running service.

### Requirements

Python 3.10+ is recommended.

Install dependencies:

    pip install -r requirements.txt

### Run a Scenario

The reference scenario can be executed directly:

    python -m experiments.flood_overload

Execution completes automatically once no further events are scheduled.
There is no interactive loop and no real-time progression.

---

## Outputs and Artifacts

Simulation outputs are written to disk for inspection and post-hoc analysis.

### Console Output

During execution, the event loop prints:

- the logical time of each event,
- the event type and source,
- the post-event state of all agents.

This output is intended for trace inspection and debugging,
not for quantitative evaluation.

### Metrics Log

A structured event-aligned log is written to:

    results/metrics.csv

Each row records the system state after a single event execution.
The file serves as an audit trail and as input for post-hoc analysis
and graph-based reasoning.

---

### Failure Analysis

An example post-mortem analysis of a completed simulation run is provided in:

    results/failure_analysis.md

This document interprets observed system behavior using logged system state
and structural graph reasoning.

It does not evaluate performance, benchmark policies,
or predict future outcomes.

---

## Status

This repository implements the core system contracts of an event-driven
multi-agent infrastructure stress simulator.

The current scope focuses on:

- explicit agent boundaries and decision contracts
- centralized, deterministic event scheduling
- explicit modeling of latency as a system-level concern
- failure propagation through service dependency graphs

Scenarios, metrics, and environment-specific stressors are introduced
incrementally to preserve auditability and design clarity.

---

## What This Is Not

- This is not a predictive model.
- This is not an optimization framework.
- This is not a real-time decision system.
- This is not calibrated to real-world data.

The system is intentionally scoped to explore structural failure modes,
not to recommend or automate policy decisions.
