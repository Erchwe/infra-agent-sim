# Multi-Agent Infrastructure Stress Simulator

## Problem
Public systems fail under stress not because of lack of intelligence,
but because of coordination breakdown.

## Why Simulation (Not Prediction)
We are not forecasting outcomes.
We are exploring failure modes under controlled stress.

## System Design

The system is designed around explicit boundaries between agents,
events, and execution authority. Agents express intent through events,
while all state mutation and temporal ordering is handled centrally
by the simulation engine.

### Timing and Latency

Timing is treated as a property of the system, not of individual agents.
Agents may express intent and desired delays, but scheduling authority
remains centralized and deterministic.

This design reflects real-world public systems, where outcomes are shaped
not only by decisions, but by institutional latency and coordination delay.


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


