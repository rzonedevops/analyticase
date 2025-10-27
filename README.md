# AnalytiCase: Comprehensive Legal Case Analysis & Simulation Framework

## Overview

This repository provides a comprehensive framework for legal case analysis, simulation, and data integration. It combines the HyperGNN Analysis Framework with South African judiciary systems (Court Online and CaseLines) and introduces a powerful suite of simulation models for in-depth case analysis.

## Repository Structure

```
analyticase/
├── models/                   # Core simulation and analysis models
│   ├── agent_based/          # Agent-based model for case participant interactions
│   ├── discrete_event/       # Discrete-event model for case lifecycle simulation
│   ├── system_dynamics/      # System dynamics model for case flow analysis
│   ├── hyper_gnn/            # HyperGNN model for complex relationship analysis
│   ├── case_llm/             # Case-LLM for legal document analysis and generation
│   └── ggmlex/               # GGML-based ML framework with HypergraphQL
├── case_studies/             # Real-world and synthetic case studies
│   └── trust_fraud_analysis/ # Trust fraud case with agent centrality analysis
├── lex/                      # Legal framework directory (legislation structure)
│   ├── lv2/                  # Inference level 2 - meta-principles (legal foundations/theories)
│   ├── lv1/                  # Inference level 1 - first-order principles (legal maxims)
│   └── civ/za/               # South African civil law framework
├── simulation_results/       # Simulation analysis reports and raw data
├── simulations/              # Unified simulation runner and results
│   ├── simulation_runner.py  # Main script to run all simulations
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

### Enhanced Simulation & Analysis Models

- **Enhanced Agent-Based Model**: Simulates legal actors with principle-aware decision-making, Bayesian belief networks, and game-theoretic strategy selection. Now integrates directly with the `lex/` legal framework.
- **Enhanced Discrete-Event Model**: Models the case lifecycle with legal principle tracking, resource constraints, and process mining capabilities for bottleneck identification.
- **Enhanced HyperGNN Model**: Features legal-specific node/hyperedge types, temporal hyperedges, multi-head attention, and hierarchical attention (principle → statute → case) for sophisticated legal relationship analysis.
- **Enhanced Case-LLM**: Integrates with legal principles from `.scm` files and features Hypergraph-Augmented Generation (HAG) for context-aware analysis, multi-agent collaboration, and principle-aware reasoning.
- **GGMLEX**: GGML-based ML framework with HypergraphQL integration for querying legal frameworks, featuring:
  - LlamaLex.cpp inference engine optimized for legal text processing
  - **Inference Engine**: Processes lex scheme expressions to derive legal principles at multiple abstraction levels (enumerated laws → first-order principles → meta-principles) using deductive, inductive, abductive, and analogical inference models

### ZA Judiciary Integration

- **Court Online & CaseLines Integration**: Seamlessly connects with South African judiciary systems for e-filing, digital case management, and evidence handling.
- **Database Schema Alignment**: ZA-specific database schemas for compliance and efficient data management.
- **Enhanced API**: Specialized API endpoints for interacting with the ZA judiciary systems.

### Case Studies

- **Trust Fraud Analysis**: Comprehensive case study demonstrating HyperGNN analysis with agent centrality scoring, temporal pattern detection, and narrative extraction. Features a sophisticated fraud investigation with 5 agents, 10 key events, and 7 hyperedges with attention weights. Includes interactive Mermaid visualizations and complete analysis pipeline.

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

To run the enhanced simulations:

```bash
# Run Agent-Based Simulation
python3 models/agent_based/case_agent_model_enhanced.py

# Run Discrete-Event Simulation
python3 models/discrete_event/case_event_model_enhanced.py

# Run HyperGNN Simulation
python3 models/hyper_gnn/hypergnn_model_enhanced.py
```

### Simulation Analysis

A comprehensive analysis of the simulation results is available in the [Simulation Analysis Report](simulation_results/SIMULATION_ANALYSIS_REPORT_2025-10-27.md). This report details the findings from the Agent-Based, Discrete-Event, and HyperGNN models, providing insights into legal system dynamics, resource utilization, and principle application.

### Docker Deployment

For production deployment of the API:

```bash
# Build and run with Docker Compose
docker-compose up -d
```

## Using GGMLEX with HypergraphQL

The GGMLEX framework provides advanced ML capabilities and legal framework querying:

```bash
# Run HypergraphQL examples
python models/ggmlex/hypergraphql/hypergraphql_example.py

# Test GGMLEX components
python -m pytest models/ggmlex/test_ggmlex.py -v
```

Example usage in Python:

```python
from models.ggmlex import (
    HypergraphQLEngine, LegalNode, LegalNodeType,
    LegalTransformer, LegalLLM
)

# Query legal framework
engine = HypergraphQLEngine()
cases = engine.query_nodes(node_type=LegalNodeType.CASE, jurisdiction="za")

# Analyze legal text
transformer = LegalTransformer()
analysis = transformer.analyze_legal_text("The contract was breached...")

# Use Legal LLM
llm = LegalLLM()
result = llm.analyze_case("Plaintiff v. Defendant case text...")
```

## Running Case Studies

The repository includes comprehensive case studies demonstrating the application of various analysis models:

### Trust Fraud Analysis

Explore the trust fraud case study with agent centrality analysis:

```bash
# View the case data
python case_studies/trust_fraud_analysis/case_data.py

# Run the complete analysis
python case_studies/trust_fraud_analysis/analyze_case.py
```

The analysis will:
- Build a hypergraph from the case data (5 agents, 10 events, 7 hyperedges)
- Compute agent centrality scores and compare with ground truth
- Detect communities using HyperGNN
- Analyze temporal patterns and causal chains
- Extract hidden narratives
- Generate comprehensive insights

**Visualization**: View the agent centrality graph at `case_studies/trust_fraud_analysis/agent_centrality_graph.mmd` using:
- GitHub (auto-renders Mermaid diagrams)
- [Mermaid Live Editor](https://mermaid.live/)
- VSCode with Mermaid plugin

See the [case study README](case_studies/trust_fraud_analysis/README.md) for detailed documentation.

## Documentation

- **Formal Specification**: See `docs/formal_specification/README.md` for the Z++ formal specification of the system, including core data structures, operations, and invariants.
- **Simulation Models**: Detailed documentation for each model can be found in the `README.md` file within each model's directory (e.g., `models/agent_based/README.md`).
- **Case Studies**: See `case_studies/trust_fraud_analysis/README.md` for the trust fraud analysis case study documentation.
- **Legal Framework**: See `lex/README.md` for the comprehensive legal framework documentation. The framework includes:
  - `lex/lv2/` - Inference level 2: Meta-principles (known legal foundations and jurisprudential theories from which first-order principles are derived)
  - `lex/lv1/` - Inference level 1: First-order principles (60+ fundamental legal maxims and principles)
  - `lex/civ/`, `lex/cri/`, etc. - Jurisdiction-specific legal frameworks derived from first-order principles
- **GGMLEX Framework**: See `models/ggmlex/README.md` for comprehensive documentation on the GGML-based ML framework, HypergraphQL, and LlamaLex.cpp inference engine.
- **ZA Judiciary Integration**: Refer to the `docs/` directory in the `za_judiciary_integration` module for detailed documentation on the integration architecture.
- **Revenue Stream Hijacking Case**: See `Revenue_Stream_Hijacking_by_Rynette/README.md` for comprehensive case documentation demonstrating the viability and transparency of POPIA-compliant systems with clear audit trails, secure portals, and proper oversight mechanisms.

## Contact

For questions or support, please contact the development team.


## Lex Scheme Database

The **Lex Scheme** is a comprehensive legal framework management system integrated into AnalytiCase. It provides a hypergraph-based database for storing and querying legal information.

### Features

- **14 Core Tables** for legal entities (statutes, cases, courts, judges, parties)
- **Hypergraph Relationships** supporting 13 relationship types
- **Full-Text Search** across legal documents using PostgreSQL GIN indexes
- **Integration** with Agent-Based, Discrete-Event, and System Dynamics models
- **Versioning & Audit Trail** for tracking legal entity changes
- **Analytics & Tracking** for usage monitoring

### Database Schema

The Lex Scheme schema is located in `schema/lex_scheme_enhanced.sql` and has been deployed to the Neon database.

### Management Tools

- **lex_db_manager.py**: Python tool for database management
- **deploy_lex_schema.py**: Deployment script for schema updates

### Documentation

- [Lex Scheme Design Document](docs/lex_scheme_design.md)
- [Enhancement Report](LEX_SCHEME_ENHANCEMENT_REPORT.md)

