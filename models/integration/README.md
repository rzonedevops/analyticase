# Lex-AD Hypergraph Integration

## Overview

This module provides comprehensive integration between:

1. **Lex Hypergraph**: Legal framework entities (statutes, cases, principles) from the `lex/` directory
2. **AD Hypergraph**: Agent-based and Discrete-event simulation models
3. **System Dynamics**: Stock-and-flow models for case progression
4. **HyperGNN**: Hypergraph neural network for relationship analysis
5. **Case-LLM**: Attention head mapping for semantic legal analysis

The integration enables multi-dimensional analysis of legal cases, combining structural knowledge (legal framework), behavioral dynamics (agents), temporal progression (events), system-level flows (stocks), neural embeddings (HyperGNN), and semantic attention (Case-LLM).

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Lex-AD Integration Layer                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐      ┌──────────────┐                    │
│  │     Lex      │◄────►│      AD      │                    │
│  │  Hypergraph  │      │  Hypergraph  │                    │
│  │              │      │              │                    │
│  │  • Statutes  │      │  • Agents    │                    │
│  │  • Cases     │      │  • Events    │                    │
│  │  • Principles│      │  • Stocks    │                    │
│  └──────────────┘      └──────────────┘                    │
│         │                     │                             │
│         │                     │                             │
│         └──────────┬──────────┘                             │
│                    │                                        │
│         ┌──────────▼──────────┐                            │
│         │     HyperGNN        │                            │
│         │   • Embeddings      │                            │
│         │   • Communities     │                            │
│         │   • Link Prediction │                            │
│         └──────────┬──────────┘                            │
│                    │                                        │
│         ┌──────────▼──────────┐                            │
│         │   Attention Heads   │                            │
│         │   • Legal Entities  │                            │
│         │   • Temporal Events │                            │
│         │   • Case Relations  │                            │
│         └─────────────────────┘                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Key Components

### 1. IntegratedHypergraph

A dataclass that maintains the integrated structure:

```python
@dataclass
class IntegratedHypergraph:
    lex_hypergraph: HypergraphQLEngine      # Legal framework
    ad_hypergraph: Hypergraph               # Agents + Events + Stocks
    
    # Mappings between components
    lex_to_ad_mapping: Dict[str, str]       # Lex → AD mappings
    ad_to_lex_mapping: Dict[str, str]       # AD → Lex mappings
    agent_to_legal_entity: Dict[str, str]   # Agents → Legal entities
    event_to_legal_procedure: Dict[str, str]# Events → Legal procedures
    stock_to_legal_stage: Dict[str, str]    # Stocks → Legal stages
```

### 2. LexADIntegration

Main integration class that orchestrates the entire process:

- **generate_lex_hypergraph()**: Loads legal framework from `lex/` directory
- **create_ad_hypergraph_from_agents()**: Builds AD hypergraph from agents, events, and stocks
- **map_lex_to_ad()**: Creates semantic mappings between Lex and AD entities
- **integrate_with_hypergnn()**: Applies HyperGNN for embeddings and community detection
- **map_attention_heads_to_case_llm()**: Maps attention heads to legal components
- **generate_comprehensive_report()**: Produces complete integration analysis

## Usage

### Basic Integration

```python
from models.integration import run_lex_ad_integration

# Run with default configuration
results = run_lex_ad_integration()

print(f"Lex nodes: {results['lex_hypergraph']['num_nodes']}")
print(f"AD nodes: {results['ad_hypergraph']['num_nodes']}")
print(f"Mappings: {results['mappings']['mappings_created']}")
print(f"Communities: {results['hypergnn_integration']['num_communities']}")
```

### Custom Configuration

```python
from models.integration import run_lex_ad_integration

config = {
    'input_dim': 128,           # Embedding dimension
    'hidden_dim': 64,           # Hidden layer dimension
    'num_layers': 3,            # Number of GNN layers
    'num_attention_heads': 12,  # Number of attention heads
    'embedding_dim': 128        # Attention embedding dimension
}

results = run_lex_ad_integration(config)
```

### Advanced Usage

```python
from models.integration import LexADIntegration
from models.agent_based.case_agent_model import Agent, AgentType, AgentState
from models.discrete_event.case_event_model import Event, EventType
from models.system_dynamics.case_dynamics_model import Stock

# Initialize integration
integration = LexADIntegration()

# Create custom agents for your case
agents = [
    Agent(
        agent_id="judge_1",
        agent_type=AgentType.JUDGE,
        name="Judge Smith",
        state=AgentState.IDLE,
        efficiency=0.95
    )
]

# Create case timeline
events = [
    Event(time=0.0, event_type=EventType.CASE_FILED, case_id="my_case"),
    Event(time=30.0, event_type=EventType.HEARING_SCHEDULED, case_id="my_case")
]

# Create system stocks
stocks = {
    'filed_cases': Stock('filed_cases', 10.0, 10.0, [10.0])
}

# Build integrated hypergraph
ad_stats = integration.create_ad_hypergraph_from_agents(agents, events, stocks)
mapping_stats = integration.map_lex_to_ad()
hypergnn_results = integration.integrate_with_hypergnn()
attention_results = integration.map_attention_heads_to_case_llm()

# Generate report
report = integration.generate_comprehensive_report()
```

## Mappings

### Agent to Legal Entity Mappings

Agents in the simulation are mapped to legal entities:

- **Judge** → Legal decision-maker entity
- **Attorney** → Legal representative entity
- **Investigator** → Evidence collection entity

### Event to Legal Procedure Mappings

Discrete events are mapped to legal procedures:

- **CASE_FILED** → filing_procedure
- **HEARING_SCHEDULED** → hearing_procedure
- **HEARING_CONDUCTED** → trial_procedure
- **RULING_ISSUED** → judgment_procedure
- **APPEAL_FILED** → appeal_procedure
- **CASE_CLOSED** → closure_procedure

### Stock to Legal Stage Mappings

System dynamics stocks are mapped to legal stages:

- **filed_cases** → filing_stage
- **discovery_cases** → discovery_stage
- **pre_trial_cases** → pre_trial_stage
- **trial_cases** → trial_stage
- **ruling_cases** → ruling_stage
- **closed_cases** → closure_stage

## Attention Head Focus Areas

The integration creates 8 attention heads, each focusing on different aspects:

1. **legal_entities**: Judges, attorneys, parties
2. **temporal_events**: Event timeline and sequencing
3. **legal_framework**: Statutes and legal structure
4. **case_relationships**: Entity relationships and interactions
5. **evidence_chain**: Evidence connections and chains
6. **procedural_flow**: Procedural steps and requirements
7. **precedent_links**: Case precedents and citations
8. **multi_party**: Multi-party interactions and dynamics

## HyperGNN Features

The HyperGNN integration provides:

- **Node Embeddings**: Dense vector representations of all entities
- **Community Detection**: Identification of related entity clusters
- **Link Prediction**: Prediction of potential relationships
- **Multi-layer Processing**: Deep learning over hypergraph structure

## Examples

Run the included examples:

```bash
# Basic integration example
python models/integration/integration_example.py

# Run integration module directly
python models/integration/lex_ad_hypergraph_integration.py
```

## Testing

Run the comprehensive test suite:

```bash
# Run all integration tests
python -m pytest models/integration/test_integration.py -v

# Run specific test class
python -m pytest models/integration/test_integration.py::TestLexADIntegration -v

# Run with coverage
python -m pytest models/integration/test_integration.py --cov=models.integration
```

## Results

The integration produces comprehensive results including:

```python
{
    'lex_hypergraph': {
        'num_nodes': 823,           # Legal entities loaded
        'num_edges': 0,             # Relationships between entities
        'node_types': {...}         # Distribution of entity types
    },
    'ad_hypergraph': {
        'num_nodes': 26,            # Agents + Events + Stocks
        'num_hyperedges': 0         # Interactions between entities
    },
    'mappings': {
        'mappings_created': 823,    # Total mappings
        'total_lex_to_ad': 823,     # Lex → AD mappings
        'total_ad_to_lex': 1        # AD → Lex mappings
    },
    'hypergnn_integration': {
        'num_embeddings': 26,       # Embedded nodes
        'num_communities': 5,       # Detected communities
        'communities': {...},       # Community assignments
        'link_predictions': [...]   # Predicted relationships
    },
    'attention_mapping': {
        'num_heads': 8,             # Attention heads
        'mappings': [...],          # Head-to-node mappings
        'embedding_dim': 64         # Embedding dimension
    }
}
```

## Use Cases

1. **Multi-dimensional Case Analysis**: Analyze cases from legal, behavioral, temporal, and systemic perspectives simultaneously

2. **Legal Precedent Discovery**: Use HyperGNN embeddings to find similar cases and relevant precedents

3. **Agent Behavior Prediction**: Predict how different legal actors will behave based on historical patterns and legal framework constraints

4. **Timeline Optimization**: Identify bottlenecks and optimize case progression through the system

5. **Attention-based Legal Reasoning**: Use attention mappings to understand which legal entities and concepts are most relevant to specific cases

## Integration with Other Components

### With Simulation Runner

```python
from simulations.simulation_runner import SimulationRunner
from models.integration import run_lex_ad_integration

# Run simulations
runner = SimulationRunner()
sim_results = runner.run_all_simulations()

# Integrate with Lex-AD framework
integration_results = run_lex_ad_integration()

# Combine results for comprehensive analysis
combined_analysis = {
    'simulations': sim_results,
    'integration': integration_results
}
```

### With Case-LLM

```python
from models.case_llm.case_llm_model import run_case_llm_analysis
from models.integration import LexADIntegration

# Get attention mappings
integration = LexADIntegration()
attention_results = integration.map_attention_heads_to_case_llm()

# Use with Case-LLM for enhanced analysis
case_data = {...}
llm_results = run_case_llm_analysis(case_data)

# Combine attention mappings with LLM results
enhanced_analysis = {
    'llm_analysis': llm_results,
    'attention_mapping': attention_results
}
```

## Future Enhancements

Potential areas for expansion:

1. **Real-time Integration**: Stream live case data into the integrated framework
2. **Multi-repository Support**: Integrate with external legal repositories (as mentioned in the problem statement)
3. **Advanced Attention Mechanisms**: Implement transformer-based attention with learned weights
4. **Temporal Graph Neural Networks**: Add temporal dynamics to HyperGNN
5. **Interactive Visualization**: Create visual interface for exploring the integrated hypergraph

## References

- HyperGNN Model: `models/hyper_gnn/hypergnn_model.py`
- HypergraphQL Engine: `models/ggmlex/hypergraphql/engine.py`
- Agent-based Model: `models/agent_based/case_agent_model.py`
- Discrete-event Model: `models/discrete_event/case_event_model.py`
- System Dynamics Model: `models/system_dynamics/case_dynamics_model.py`
- Case-LLM: `models/case_llm/case_llm_model.py`

## License

Part of the AnalytiCase framework. See main repository license for details.
