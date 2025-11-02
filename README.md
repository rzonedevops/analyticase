# AnalytiCase: Comprehensive Legal Case Analysis & Simulation Framework v2.2

## Overview

This repository provides a comprehensive framework for legal case analysis, simulation, and data integration. It combines the HyperGNN Analysis Framework with South African judiciary systems (Court Online and CaseLines) and introduces a powerful suite of simulation models for in-depth case analysis, now powered by an enhanced legal framework (v2.2).

## Repository Structure

```
analyticase/
├── models/                   # Core simulation and analysis models
│   ├── agent_based/          # Agent-based model for case participant interactions
│   ├── discrete_event/       # Discrete-event model for case lifecycle simulation
│   ├── system_dynamics/      # System dynamics model for case flow analysis
│   ├── hyper_gnn/            # HyperGNN model for complex relationship analysis
│   ├── case_llm/             # Case-LLM for legal document analysis and generation
│   └── integration/          # Unified simulation runner and integration tests
├── case_studies/             # Real-world and synthetic case studies
│   └── trust_fraud_analysis/ # Trust fraud case with agent centrality analysis
├── lex/                      # Legal framework directory (legislation structure)
│   ├── lv2/                  # Inference level 2 - meta-principles (v2.2)
│   ├── lv1/                  # Inference level 1 - first-order principles
│   └── civ/za/               # South African civil law framework (v2.2)
├── simulation_results/       # Simulation analysis reports and raw data
├── simulations/              # Unified simulation runner and results
│   ├── unified_simulation_runner_v2.2.py  # Main script to run all simulations
│   └── results/              # Directory for simulation output
├── za_judiciary_integration/ # South African judiciary integration module
│   ├── api/                  # API implementation for ZA judiciary integration
│   ├── docs/                 # Documentation for ZA judiciary integration
│   └── schema/               # Database schema for ZA judiciary
├── Revenue_Stream_Hijacking_by_Rynette/ # Case documentation for revenue stream hijacking
│   └── Comprehensive legal documentation demonstrating system transparency
├── DEPLOYMENT.md             # Deployment instructions
├── README.md                 # This file
└── ...
```

## Key Features

### Enhanced Legal Framework (v2.2)

- **Expanded Meta-Principles**: The Level 2 framework has been expanded from 15 to 22 jurisprudential theories, including Critical Legal Studies, Feminist Jurisprudence, Economic Analysis of Law, and Ubuntu Jurisprudence.
- **Improved Integration**: Jurisdiction-specific frameworks now directly integrate with Level 1 first-order principles, with explicit case law and statutory references.
- **Quantitative Metrics**: The framework includes confidence scores, influence metrics, and temporal evolution tracking for all principles.

### Enhanced Simulation & Analysis Models (v2.2)

- **Principle-Aware Models**: All simulation models now integrate with the enhanced legal framework (v2.2), enabling more sophisticated and realistic analysis.
- **Unified Simulation Runner**: A new unified runner (`unified_simulation_runner_v2.2.py`) executes all models and generates a comprehensive comparative analysis.
- **Enhanced System Dynamics Model**: The system dynamics model now includes principle-aware flow modulation, quality-of-justice metrics, and enhanced feedback loops.

### ZA Judiciary Integration

- **Court Online & CaseLines Integration**: Seamlessly connects with South African judiciary systems for e-filing, digital case management, and evidence handling.
- **Database Schema Alignment**: ZA-specific database schemas for compliance and efficient data management.

### Case Studies

- **Trust Fraud Analysis**: Comprehensive case study demonstrating HyperGNN analysis with agent centrality scoring, temporal pattern detection, and narrative extraction.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Docker & Docker Compose
- PostgreSQL database (or Supabase/Neon account)
- OpenAI API Key (for Case-LLM)

### Installation

1.  **Clone this repository**
    ```bash
    git clone https://github.com/rzonedevops/analyticase.git
    cd analyticase
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up environment variables**
    Create a `.env` file with your database and API credentials. You can use `.env.example` as a template.

4.  **Initialize the database**
    ```bash
    python scripts/sync_db.py
    ```

### Running Simulations

To run the unified multi-model simulation:

```bash
# Run all simulations and generate a comparative analysis
python3 models/integration/unified_simulation_runner_v2.2.py
```

To run individual models for targeted analysis:

```bash
# Run Enhanced System Dynamics Simulation
python3 models/system_dynamics/case_dynamics_model_enhanced_v2.2.py

# (Other individual model run commands can be added here)
```

### Simulation Analysis

A comprehensive analysis of the latest simulation results is available in the [Comprehensive Simulation Insights Report v2.2](SIMULATION_INSIGHTS_V2.2_2025-11-02.md). This report details the findings from all five simulation models, providing insights into legal system dynamics, principle application, and cross-model validation.

## Documentation

- **Legal Framework Refinement**: See [Scheme Legal Framework Refinement Progress](SCHEME_REFINEMENT_PROGRESS_2025-11-02.md) for a detailed log of the v2.2 enhancements.
- **Simulation Insights**: See [Comprehensive Simulation Insights Report v2.2](SIMULATION_INSIGHTS_V2.2_2025-11-02.md) for the latest simulation analysis.
- **Legal Framework**: See `lex/README.md` for the comprehensive legal framework documentation. The framework includes:
  - `lex/lv2/` - Inference level 2: Meta-principles (22 jurisprudential theories)
  - `lex/lv1/` - Inference level 1: First-order principles (60+ fundamental legal maxims)
  - `lex/civ/`, `lex/cri/`, etc. - Jurisdiction-specific legal frameworks
- **ZA Judiciary Integration**: Refer to the `docs/` directory in the `za_judiciary_integration` module for detailed documentation on the integration architecture.

## Contact

For questions or support, please contact the development team.
