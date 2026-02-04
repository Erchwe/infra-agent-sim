# Multi-Agent Infrastructure Stress Simulator

## Problem
Public systems fail under stress not because of lack of intelligence,
but because of coordination breakdown.

## Why Simulation (Not Prediction)
We are not forecasting outcomes.
We are exploring failure modes under controlled stress.

## Status

This repository implements the core system contracts of an event-driven
multi-agent infrastructure stress simulator.

The current scope focuses on:
- explicit agent boundaries and decision contracts
- deterministic event scheduling and execution
- failure propagation through service dependency graphs

Scenarios, metrics, and environment-specific stressors are intentionally
introduced incrementally to preserve auditability and design clarity.

