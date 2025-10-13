# Agent-Based Model for Legal Case Analysis

## Overview

This model simulates the behavior and interactions of various agents involved in a legal case. By modeling individual actors, we can understand the emergent, system-level dynamics of the judicial process. This is particularly useful for identifying bottlenecks, resource allocation issues, and the impact of individual agent behavior on case outcomes.

### Key Agents

- **InvestigatorAgent**: Responsible for collecting evidence and following leads.
- **AttorneyAgent**: Represents clients, prepares briefs, and argues cases.
- **JudgeAgent**: Reviews cases and makes judicial rulings.

## How It Works

The simulation proceeds in discrete time steps. At each step, agents can be in one of several states (e.g., `IDLE`, `WORKING`). They are assigned tasks, interact with other agents, and update their state based on their workload and efficiency.

## How to Run

The model can be run as a standalone script or as part of the unified simulation runner.

```bash
python models/agent_based/case_agent_model.py
```

This will run a sample simulation and print the results to the console.

