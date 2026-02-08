# Monthly Cost Estimate (GCP)

This project uses a minimal VM-based setup for reproducible execution,
not continuous operation.

## Assumptions

- VM type: e2-standard-2
- Region: europe-west1
- Usage pattern: short-lived batch runs for testing and analysis

## Estimated Cost

- Approx. $0.067 per hour
- Typical usage: a few hours per month
- Estimated monthly cost: <$5

Costs are kept intentionally low by avoiding GPUs, autoscaling,
and long-running services.
