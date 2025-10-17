#!/usr/bin/env python3
"""
Trust Fraud Case Analysis Script

This script demonstrates how to use the trust fraud case data with the
HyperGNN model for analysis and generate insights about agent centrality,
community detection, and relationship patterns.
"""

import sys
import os
import json

# Add parent directory to path to import models
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from models.hyper_gnn.hypergnn_model import (
    HyperGNN, Hypergraph, Node, Hyperedge,
    run_hypergnn_analysis
)
from case_data import (
    get_case_data, get_centrality_scores, get_attention_weights
)


def create_trust_fraud_hypergraph() -> Hypergraph:
    """
    Create a hypergraph from the trust fraud case data.
    
    Returns:
        Hypergraph populated with agents, events, and relationships
    """
    case_data = get_case_data()
    hg = Hypergraph()
    
    # Add all entities (agents and events) as nodes
    for entity in case_data['entities']:
        node = Node(
            node_id=entity['id'],
            node_type=entity['type'],
            attributes={
                'name': entity.get('name', entity.get('id')),
                'role': entity.get('role', entity.get('category', 'N/A')),
                'centrality': entity.get('centrality', 0.0)
            }
        )
        node.initialize_embedding(dim=64)
        hg.add_node(node)
    
    # Add hyperedges from relationships
    for rel in case_data['relationships']:
        hyperedge = Hyperedge(
            edge_id=rel['id'],
            nodes=set(rel['participants']),
            edge_type=rel['type'],
            weight=rel['weight'],
            attributes={'description': rel['description']}
        )
        hg.add_hyperedge(hyperedge)
    
    return hg


def analyze_agent_centrality(hypergraph: Hypergraph, model: HyperGNN):
    """
    Analyze and compare computed centrality with ground truth.
    
    Args:
        hypergraph: The hypergraph structure
        model: Trained HyperGNN model
    """
    print("\n" + "="*70)
    print("AGENT CENTRALITY ANALYSIS")
    print("="*70)
    
    ground_truth = get_centrality_scores()
    
    # Compute degree centrality from hypergraph structure
    computed_centrality = {}
    for node_id, edges in hypergraph.node_to_edges.items():
        if node_id in ground_truth:  # Only for agents
            # Compute weighted degree centrality
            total_weight = sum(
                hypergraph.hyperedges[edge_id].weight 
                for edge_id in edges
            )
            computed_centrality[node_id] = total_weight / 10.0  # Normalize
    
    # Print comparison
    print(f"\n{'Agent':<15} {'Ground Truth':<15} {'Computed':<15} {'Degree':<10}")
    print("-" * 70)
    
    for agent_id in sorted(ground_truth.keys(), 
                          key=lambda x: ground_truth[x], 
                          reverse=True):
        gt_score = ground_truth[agent_id]
        comp_score = computed_centrality.get(agent_id, 0.0)
        degree = len(hypergraph.node_to_edges.get(agent_id, set()))
        
        print(f"{agent_id:<15} {gt_score:>14.2f} {comp_score:>14.2f} {degree:>9}")


def analyze_hyperedges(hypergraph: Hypergraph):
    """
    Analyze hyperedge patterns and attention weights.
    
    Args:
        hypergraph: The hypergraph structure
    """
    print("\n" + "="*70)
    print("HYPEREDGE ANALYSIS")
    print("="*70)
    
    attention_weights = get_attention_weights()
    
    print(f"\n{'Hyperedge Type':<40} {'Weight':<10} {'Size':<10}")
    print("-" * 70)
    
    for edge_id, edge in hypergraph.hyperedges.items():
        edge_type = edge.edge_type
        weight = edge.weight
        size = len(edge.nodes)
        
        print(f"{edge_type:<40} {weight:>9.2f} {size:>9}")
    
    print(f"\nAverage hyperedge size: {sum(len(e.nodes) for e in hypergraph.hyperedges.values()) / len(hypergraph.hyperedges):.2f}")
    print(f"Maximum hyperedge size: {max(len(e.nodes) for e in hypergraph.hyperedges.values())}")


def analyze_narratives(hypergraph: Hypergraph):
    """
    Analyze the hidden narratives (subgraphs).
    
    Args:
        hypergraph: The hypergraph structure
    """
    print("\n" + "="*70)
    print("HIDDEN NARRATIVE ANALYSIS")
    print("="*70)
    
    case_data = get_case_data()
    
    for narrative in case_data['narratives']:
        print(f"\nNarrative: {narrative['name']}")
        print(f"Description: {narrative['description']}")
        print(f"Key nodes: {', '.join(narrative['nodes'])}")
        
        # Find edges connecting narrative nodes
        narrative_set = set(narrative['nodes'])
        connecting_edges = []
        
        for edge_id, edge in hypergraph.hyperedges.items():
            if len(edge.nodes.intersection(narrative_set)) >= 2:
                connecting_edges.append((edge_id, edge))
        
        print(f"Connected by {len(connecting_edges)} hyperedges")


def analyze_temporal_patterns():
    """
    Analyze temporal patterns and causal chains.
    """
    print("\n" + "="*70)
    print("TEMPORAL PATTERN ANALYSIS")
    print("="*70)
    
    case_data = get_case_data()
    
    print("\nCausal Chains:")
    for chain in case_data['causal_chains']:
        print(f"  {chain['from']} → {chain['to']}")
        print(f"    Relationship: {chain['relationship']}")
        print(f"    Delay: {chain['delay_hours']} hours")


def generate_insights(hypergraph: Hypergraph, communities: dict):
    """
    Generate high-level insights from the analysis.
    
    Args:
        hypergraph: The hypergraph structure
        communities: Community detection results
    """
    print("\n" + "="*70)
    print("KEY INSIGHTS")
    print("="*70)
    
    stats = hypergraph.get_statistics()
    centrality = get_centrality_scores()
    
    print(f"\n1. Network Structure:")
    print(f"   - {stats['num_nodes']} total nodes (agents + events)")
    print(f"   - {stats['num_hyperedges']} hyperedges")
    print(f"   - Average node degree: {stats['avg_node_degree']:.2f}")
    print(f"   - Maximum node degree: {stats['max_node_degree']}")
    
    print(f"\n2. Agent Hierarchy:")
    print(f"   - Central orchestrator (BANTJIES): Centrality 1.0")
    print(f"   - Key enablers (RYNETTE, JACQUI): Centrality 0.36-0.46")
    print(f"   - Manipulated participant (PETER): Centrality 0.15")
    print(f"   - Marginalized whistleblower (DANIEL): Centrality -0.15")
    
    print(f"\n3. Community Structure:")
    if communities:
        num_communities = len(set(communities.values()))
        print(f"   - {num_communities} distinct communities detected")
        for comm_id in set(communities.values()):
            members = [node_id for node_id, comm in communities.items() if comm == comm_id]
            print(f"   - Community {comm_id}: {', '.join(members)}")
    
    print(f"\n4. Critical Patterns:")
    print(f"   - Financial motivation (R18M payout) drives all actions")
    print(f"   - Systematic whistleblower neutralization")
    print(f"   - Tight temporal coordination (24-48 hour response times)")
    print(f"   - Dual-layer operations (institutional + legal)")
    
    print(f"\n5. Risk Indicators:")
    print(f"   - Highest attention weight (1.0) on payout motivation")
    print(f"   - Negative centrality indicates active marginalization")
    print(f"   - Rapid retaliation against fraud reporting")
    print(f"   - Use of legal system as weapon (ex parte interdict)")


def main():
    """
    Main analysis function.
    """
    print("="*70)
    print("TRUST FRAUD CASE ANALYSIS")
    print("Using HyperGNN Model for Agent Centrality and Pattern Detection")
    print("="*70)
    
    # Create hypergraph
    print("\nBuilding hypergraph from case data...")
    hypergraph = create_trust_fraud_hypergraph()
    
    # Initialize and train HyperGNN
    print("Initializing HyperGNN model...")
    model = HyperGNN(input_dim=64, hidden_dim=32, num_layers=2)
    
    print("Running forward pass...")
    embeddings = model.forward(hypergraph)
    
    # Detect communities
    print("Detecting communities...")
    communities = model.detect_communities(hypergraph, num_communities=3)
    
    # Run analyses
    analyze_agent_centrality(hypergraph, model)
    analyze_hyperedges(hypergraph)
    analyze_narratives(hypergraph)
    analyze_temporal_patterns()
    generate_insights(hypergraph, communities)
    
    # Save results
    results = {
        'hypergraph_stats': hypergraph.get_statistics(),
        'communities': communities,
        'centrality_scores': get_centrality_scores(),
        'attention_weights': get_attention_weights()
    }
    
    output_file = os.path.join(os.path.dirname(__file__), 'analysis_results.json')
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n" + "="*70)
    print(f"Analysis complete! Results saved to: {output_file}")
    print("="*70)


if __name__ == "__main__":
    main()
