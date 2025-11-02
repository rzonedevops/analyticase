# System Dynamics Model for Legal Case Flow v2.2

## Overview

This model provides a high-level, aggregated view of the legal case flow using a system dynamics approach. It models the judicial system as a series of stocks (accumulations of cases) and flows (rates at which cases move between stages). This is useful for understanding the long-term behavior of the system and the impact of policy changes on case backlogs and processing times.

## Enhancements in v2.2

- **Legal Framework Integration**: The model now integrates with the enhanced legal framework (v2.2) from the `lex/` directory. Legal principles are loaded and used to modulate flow rates and influence the quality of justice.
- **Quality-of-Justice Metric**: A new stock has been added to track the overall quality of justice in the system. This metric is influenced by processing times, backlog sizes, and the application of legal principles.
- **Enhanced Feedback Loops**: The model now includes more sophisticated feedback loops, such as the impact of backlog pressure on processing rates and the effect of settlement rates on case closures.
- **Jurisdiction-Specific Configuration**: The model can be configured to simulate specific legal jurisdictions by loading the corresponding legal framework from the `lex/` directory.

### Key Stocks

- **Filed Cases**: Cases that have been filed but not yet processed.
- **Preliminary Cases**: Cases undergoing initial review.
- **Discovery Cases**: Cases currently in the discovery phase.
- **Trial Cases**: Cases that are actively in trial.
- **Judgment Cases**: Cases awaiting a final judgment.
- **Appeal Cases**: Cases that have been appealed.
- **Closed Cases**: Cases that have been resolved.
- **Justice Quality**: A stock representing the overall quality of justice.

### Key Flows

- **Case Filing Rate**: The rate at which new cases enter the system.
- **Processing Rates**: The rates at which cases move between stages, now modulated by legal principles.
- **Closure Rate**: The rate at which cases are closed, influenced by settlement rates.

## How It Works

The simulation uses differential equations to model the changes in stocks over time. The rates of the flows are determined by the current levels of the stocks, a set of system parameters (e.g., processing capacity, efficiency), and the influence of the loaded legal framework.

## How to Run

The model can be run as a standalone script or as part of the unified simulation runner.

```bash
# Run the enhanced system dynamics model
python3 models/system_dynamics/case_dynamics_model_enhanced_v2.2.py
```

This will run a sample simulation and print the results to the console, as well as export the detailed results to a JSON file in the `simulation_results` directory.
