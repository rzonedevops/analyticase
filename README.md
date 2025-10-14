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
├── lex/                      # Legal framework directory (legislation structure)
│   └── civ/za/               # South African civil law framework
├── simulations/              # Unified simulation runner and results
│   ├── simulation_runner.py  # Main script to run all simulations
│   └── results/              # Directory for simulation output
├── za_judiciary_integration/ # South African judiciary integration module
│   ├── api/                  # API implementation for ZA judiciary integration
│   ├── docs/                 # Documentation for ZA judiciary integration
│   └── schema/               # Database schema for ZA judiciary
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
- **Case-LLM**: Leverages large language models for advanced legal document analysis, summarization, entity extraction, and brief generation.
- **GGMLEX**: GGML-based ML framework with HypergraphQL integration for querying legal frameworks, featuring LlamaLex.cpp inference engine optimized for legal text processing.

### ZA Judiciary Integration

- **Court Online & CaseLines Integration**: Seamlessly connects with South African judiciary systems for e-filing, digital case management, and evidence handling.
- **Database Schema Alignment**: ZA-specific database schemas for compliance and efficient data management.
- **Enhanced API**: Specialized API endpoints for interacting with the ZA judiciary systems.

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
    python za_judiciary_integration/scripts/init_database.py
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

## Documentation

- **Simulation Models**: Detailed documentation for each model can be found in the `README.md` file within each model's directory (e.g., `models/agent_based/README.md`).
- **GGMLEX Framework**: See `models/ggmlex/README.md` for comprehensive documentation on the GGML-based ML framework, HypergraphQL, and LlamaLex.cpp inference engine.
- **ZA Judiciary Integration**: Refer to the `docs/` directory in the `za_judiciary_integration` module for detailed documentation on the integration architecture.

## Contact

For questions or support, please contact the development team.

