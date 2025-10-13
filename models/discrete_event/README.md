# Discrete-Event Model for Legal Case Processing

## Overview

This model simulates the lifecycle of a legal case as it moves through the judicial system. It treats the case lifecycle as a sequence of discrete events, such as `CASE_FILED`, `HEARING_SCHEDULED`, and `CASE_CLOSED`. This approach is ideal for analyzing process flows, identifying bottlenecks, and measuring the time spent in each stage of the legal process.

### Key Events

- **CASE_FILED**: A new case enters the system.
- **EVIDENCE_SUBMITTED**: Evidence is added to a case.
- **HEARING_SCHEDULED**: A hearing is scheduled for a case.
- **RULING_ISSUED**: A judge issues a ruling.
- **CASE_CLOSED**: The case is resolved and closed.

## How It Works

The simulation is driven by an event queue. Events are scheduled and processed in chronological order. When an event is processed, it can trigger new events to be scheduled in the future. For example, a `CASE_FILED` event will schedule a future `EVIDENCE_SUBMITTED` event.

## How to Run

The model can be run as a standalone script or as part of the unified simulation runner.

```bash
python models/discrete_event/case_event_model.py
```

This will run a sample simulation and print the results to the console.

