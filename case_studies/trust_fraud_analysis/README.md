# Trust Fraud Analysis: Agent Centrality Graph

## Overview

This case study demonstrates the application of HyperGNN analysis to a complex trust fraud investigation. The visualization shows a hypergraph representation of agents, events, and their relationships, with centrality scores computed for each agent based on their role and influence in the network.

## Visualization Files

- `agent_centrality_graph.mmd` - Mermaid diagram showing the complete agent centrality graph

## Case Summary

This analysis reveals a sophisticated fraud scheme involving multiple agents with varying levels of involvement and influence:

### Key Agents

1. **BANTJIES** (Centrality: 1.0)
   - Central orchestrator of the operation
   - Highest centrality score indicating maximum influence
   - Connected to all major events and decisions

2. **RYNETTE** (Centrality: 0.46)
   - Revenue coordinator
   - Second-highest centrality, key operational role
   - Manages financial flows

3. **JACQUI** (Centrality: 0.36)
   - Signature authority
   - Controls authorization and approval processes

4. **PETER** (Centrality: 0.15)
   - Manipulated puppet
   - Low positive centrality, executes instructions
   - Used to execute critical actions (card cancellations, interdict)

5. **DANIEL** (Centrality: -0.15)
   - Marginalized whistleblower
   - Negative centrality indicates isolation and opposition
   - Attempted to report fraud but was neutralized

### Key Events Timeline

1. **July 2024**: Trustee Appointment - Initial positioning
2. **October 2024**: Authority Appointment - Establishing control
3. **June 6, 2025**: Daniel Fraud Reports - Whistleblower action
4. **June 7, 2025**: Card Cancellations - Next-day retaliation
5. **June 10, 2025 AM**: R10M Identification - Financial threat detected
6. **June 10, 2025 PM**: Holiday Dismissal - Same-day abandonment
7. **August 11, 2025**: Main Trustee Appointment - Bypassing oversight
8. **August 13, 2025**: Ex Parte Interdict - Legal weaponization
9. **August 2025**: Supporting Affidavit - Perjury
10. **May 2026**: R18M Payout Target - Ultimate extraction goal

## Hypergraph Structure

### Hyperedge Types and Attention Weights

The graph includes seven major hyperedges representing different relationship patterns:

1. **Financial Information Control** (Weight: 0.95)
   - Connects: BANTJIES → TRUSTEE → AUTHORITY → R18M
   - Highest attention weight, critical path

2. **Trust Governance Manipulation** (Weight: 0.92)
   - Connects: BANTJIES → TRUSTEE → MAIN
   - Controls trust structure

3. **Oversight Authority Abuse** (Weight: 0.89)
   - Connects: BANTJIES → AUTHORITY → HOLIDAY
   - Misuse of oversight powers

4. **Whistleblower Neutralization** (Weight: 0.87)
   - Connects: DANIEL → REPORTS → BANTJIES → HOLIDAY → INTERDICT
   - Systematic suppression of fraud reporting

5. **Puppet Orchestration** (Weight: 0.85)
   - Connects: BANTJIES → PETER → CARDS/INTERDICT
   - Using subordinates to execute actions

6. **Timeline Coordination** (Weight: 0.83)
   - Connects: MAIN → INTERDICT → AFFIDAVIT
   - Temporal coordination of legal actions

7. **Payout Motivation** (Weight: 1.0)
   - Universal driver: R18M payout connects to all major actions
   - Highest weight indicating primary motivation

### Hidden Narratives

The analysis reveals three parallel hidden narratives:

1. **Financial Control Architecture**
   - Building systematic control over trust finances
   - Key nodes: TRUSTEE, AUTHORITY, R18M

2. **Whistleblower Neutralization**
   - Systematic suppression of fraud reporting
   - Key nodes: REPORTS, HOLIDAY, INTERDICT

3. **Dual-Layer Operations**
   - Operating through both institutional and legal channels
   - Key nodes: CARDS, MAIN, AFFIDAVIT

## Centrality Analysis

The centrality scores reveal the power structure and influence hierarchy:

- **Positive High Centrality** (0.36-1.0): Core orchestrators and enablers
- **Positive Low Centrality** (0.15): Manipulated participants
- **Negative Centrality** (-0.15): Marginalized opponents

The negative centrality of DANIEL indicates active isolation and marginalization within the network, consistent with whistleblower suppression patterns.

## Using This Visualization

### Viewing the Diagram

The Mermaid diagram can be viewed in:
- GitHub (automatically renders .mmd files)
- Mermaid Live Editor: https://mermaid.live/
- VSCode with Mermaid plugin
- Any Markdown viewer with Mermaid support

### Integration with HyperGNN Model

This visualization can be used with the HyperGNN model in the repository:

```python
from models.hyper_gnn import HyperGNN, Hypergraph, Node, Hyperedge

# Create hypergraph from case data
hg = Hypergraph()

# Add agent nodes
agents = ['BANTJIES', 'PETER', 'DANIEL', 'RYNETTE', 'JACQUI']
for agent in agents:
    node = Node(node_id=agent, node_type='agent')
    hg.add_node(node)

# Add event nodes and hyperedges
# (See hypergnn_model.py for complete implementation)

# Run analysis
model = HyperGNN(input_dim=64, hidden_dim=32, num_layers=2)
embeddings = model.forward(hg)
communities = model.detect_communities(hg)
```

## Analytical Insights

This case study demonstrates:

1. **Network Centrality in Fraud Detection**: Central actors have highest influence and control
2. **Temporal Coordination**: Events are tightly coordinated with specific timing patterns
3. **Hypergraph Superiority**: Traditional pairwise graphs cannot capture the multi-way relationships
4. **Whistleblower Isolation**: Negative centrality quantifies marginalization
5. **Motivation Tracing**: Financial incentive (R18M) connects all actions

## References

- HyperGNN Model: `/models/hyper_gnn/`
- Agent-Based Simulation: `/models/agent_based/`
- Case Analysis Framework: Main repository README

## License

This case study is part of the AnalytiCase framework and follows the same license terms as the main repository.
