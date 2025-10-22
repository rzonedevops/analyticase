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

### Simulation & Analysis Models

- **Agent-Based Model**: Simulates the behavior and interactions of legal case participants (investigators, attorneys, judges) to understand system dynamics from the ground up.
- **Discrete-Event Model**: Models the legal case lifecycle as a series of discrete events, allowing for analysis of bottlenecks and process optimization.
- **System Dynamics Model**: Provides a high-level view of case flow through the judicial system using stock-and-flow diagrams to identify systemic issues.
- **HyperGNN Model**: Utilizes hypergraph neural networks to uncover complex, higher-order relationships between entities in a case that traditional graph models might miss.
- **Case-LLM**: Leverages large language models for advanced legal document analysis, summarization, entity extraction, and brief generation. Now features a Retrieval-Augmented Generation (RAG) implementation for more context-aware analysis.
- **GGMLEX**: GGML-based ML framework with HypergraphQL integration for querying legal frameworks, featuring:
  - LlamaLex.cpp inference engine optimized for legal text processing
  - **Inference Engine**: Processes lex scheme expressions to derive legal principles at multiple abstraction levels (enumerated laws → first-order principles → meta-principles) using deductive, inductive, abductive, and analogical inference models
- **Attention-based HyperGNN**: The HyperGNN model now includes an advanced attention mechanism for more accurate hyperedge aggregation.

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

#### Local Execution

To run the full suite of simulations locally:

```bash
python simulations/simulation_runner_v2.py
```

For advanced usage with custom configurations:

```bash
# Run with custom configuration
python simulations/simulation_runner_v2.py --config simulations/example_config.json --name "my_analysis"

# Run with custom output directory
python simulations/simulation_runner_v2.py --output /path/to/custom/output --name "production_run"
```

Results will be saved in timestamped directories under `simulations/results/`.

#### GitHub Actions (Recommended)

You can also run simulations directly from GitHub using our manual workflow:

1. Go to the **Actions** tab in this repository
2. Select **"Run AnalytiCase Simulations"**
3. Click **"Run workflow"** and configure your simulation parameters
4. Download results as artifacts when complete

This approach requires no local setup and provides automatic result archiving. See the [GitHub Actions Guide](docs/GITHUB_ACTIONS_GUIDE.md) for detailed instructions.

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

