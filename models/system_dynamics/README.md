# System Dynamics Model for Legal Case Flow

## Overview

This model provides a high-level, aggregated view of the legal case flow using a system dynamics approach. It models the judicial system as a series of stocks (accumulations of cases) and flows (rates at which cases move between stages). This is useful for understanding the long-term behavior of the system and the impact of policy changes on case backlogs and processing times.

### Key Stocks

- **Filed Cases**: Cases that have been filed but not yet processed.
- **Discovery Cases**: Cases currently in the discovery phase.
- **Trial Cases**: Cases that are actively in trial.
- **Closed Cases**: Cases that have been resolved.

### Key Flows

- **Case Filing Rate**: The rate at which new cases enter the system.
- **Processing Rate**: The rate at which cases move from one stage to the next.
- **Closure Rate**: The rate at which cases are closed.

## How It Works

The simulation uses differential equations to model the changes in stocks over time. The rates of the flows are determined by the current levels of the stocks and a set of system parameters (e.g., processing capacity, efficiency).

## How to Run

The model can be run as a standalone script or as part of the unified simulation runner.

```bash
python models/system_dynamics/case_dynamics_model.py
```

This will run a sample simulation and print the results to the console.

