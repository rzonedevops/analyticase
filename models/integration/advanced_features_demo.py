#!/usr/bin/env python3
"""
Advanced Lex Hypergraph and HyperGNN Features Demonstration

This script demonstrates the new advanced features added to the lex hypergraph
query engine and HyperGNN model, including:
- Advanced query capabilities
- Visualization utilities
- Temporal graph analysis
- Attention-based aggregation
- Hierarchical graph structures
"""

import logging
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from integration.lex_ad_hypergraph_integration import LexADIntegration
from ggmlex.hypergraphql.visualization import HypergraphVisualizer
from ggmlex.hypergraphql.schema import LegalNodeType
from hyper_gnn.hypergnn_model import (
    TemporalHypergraph, AttentionHyperGNNLayer, HierarchicalHypergraph,
    Node, Hyperedge
)
import numpy as np

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def demonstrate_advanced_queries():
    """Demonstrate advanced query capabilities."""
    logger.info("=" * 70)
    logger.info("DEMONSTRATING ADVANCED QUERY CAPABILITIES")
    logger.info("=" * 70)
    
    # Initialize integration
    integration = LexADIntegration()
    integration.generate_lex_hypergraph()
    
    # 1. Subgraph extraction
    logger.info("\n1. Subgraph Extraction")
    logger.info("-" * 70)
    
    node_ids = list(integration.lex_engine.nodes.keys())[:5]
    result = integration.lex_engine.query_subgraph(
        node_ids,
        include_edges=True,
        expand_neighbors=False
    )
    logger.info(f"Extracted subgraph with {len(result.nodes)} nodes, {len(result.edges)} edges")
    
    # With neighbor expansion
    result_expanded = integration.lex_engine.query_subgraph(
        node_ids,
        include_edges=True,
        expand_neighbors=True
    )
    logger.info(f"With neighbor expansion: {len(result_expanded.nodes)} nodes, {len(result_expanded.edges)} edges")
    
    # 2. Legal reasoning chains
    logger.info("\n2. Legal Reasoning Chains")
    logger.info("-" * 70)
    
    if node_ids:
        chain_result = integration.lex_engine.query_legal_reasoning_chain(
            node_ids[0],
            max_depth=5
        )
        logger.info(f"Found reasoning chain with {len(chain_result.nodes)} concepts")
        logger.info(f"Chain metadata: {chain_result.metadata}")
        
        if chain_result.nodes:
            logger.info("Reasoning path:")
            for i, node in enumerate(chain_result.nodes[:5]):  # Show first 5
                logger.info(f"  {i+1}. {node.name} ({node.node_type.value})")
    
    # 3. Similar nodes
    logger.info("\n3. Similar Node Discovery")
    logger.info("-" * 70)
    
    if node_ids:
        similar_result = integration.lex_engine.query_similar_nodes(
            node_ids[0],
            similarity_threshold=0.2,
            max_results=5
        )
        logger.info(f"Found {len(similar_result.nodes)} similar nodes")
        
        if 'similarity_scores' in similar_result.metadata:
            logger.info("Top similar nodes:")
            scores = similar_result.metadata['similarity_scores']
            for node in similar_result.nodes[:3]:
                logger.info(f"  - {node.name}: {scores[node.node_id]:.3f}")


def demonstrate_visualization():
    """Demonstrate visualization utilities."""
    logger.info("\n" + "=" * 70)
    logger.info("DEMONSTRATING VISUALIZATION UTILITIES")
    logger.info("=" * 70)
    
    integration = LexADIntegration()
    integration.generate_lex_hypergraph()
    
    visualizer = HypergraphVisualizer(integration.lex_engine)
    
    # Get a small subgraph for visualization
    node_ids = list(integration.lex_engine.nodes.keys())[:10]
    query_result = integration.lex_engine.query_subgraph(node_ids, expand_neighbors=False)
    
    # 1. Mermaid diagram
    logger.info("\n1. Mermaid Diagram Generation")
    logger.info("-" * 70)
    
    mermaid = visualizer.generate_mermaid_diagram(query_result, max_nodes=10)
    logger.info(f"Generated Mermaid diagram ({len(mermaid)} characters)")
    logger.info("First 200 characters:")
    logger.info(mermaid[:200])
    
    # Save to file
    mermaid_file = Path("/tmp/legal_graph.mmd")
    with open(mermaid_file, 'w') as f:
        f.write(mermaid)
    logger.info(f"Saved Mermaid diagram to {mermaid_file}")
    
    # 2. DOT graph
    logger.info("\n2. DOT/Graphviz Export")
    logger.info("-" * 70)
    
    dot_graph = visualizer.generate_dot_graph(query_result, max_nodes=10)
    logger.info(f"Generated DOT graph ({len(dot_graph)} characters)")
    
    dot_file = Path("/tmp/legal_graph.dot")
    with open(dot_file, 'w') as f:
        f.write(dot_graph)
    logger.info(f"Saved DOT graph to {dot_file}")
    
    # 3. Network statistics
    logger.info("\n3. Network Statistics Summary")
    logger.info("-" * 70)
    
    stats = visualizer.generate_network_stats_summary()
    logger.info(f"Total nodes: {stats['num_nodes']}")
    logger.info(f"Total edges: {stats['num_edges']}")
    logger.info(f"Average degree: {stats['avg_degree']:.2f}")
    logger.info(f"Max degree: {stats['max_degree']}")
    logger.info(f"Connected components: {stats['num_connected_components']}")
    logger.info(f"Network density: {stats['density']:.6f}")
    
    logger.info("\nTop 5 connected nodes:")
    for node in stats['top_connected_nodes'][:5]:
        logger.info(f"  - {node['name'][:40]}: {node['degree']} connections ({node['type']})")
    
    # 4. JSON export
    logger.info("\n4. JSON Export")
    logger.info("-" * 70)
    
    json_output = visualizer.export_to_json(query_result, include_content=False)
    logger.info(f"Generated JSON export ({len(json_output)} characters)")
    
    json_file = Path("/tmp/legal_graph.json")
    with open(json_file, 'w') as f:
        f.write(json_output)
    logger.info(f"Saved JSON to {json_file}")


def demonstrate_temporal_hypergraph():
    """Demonstrate temporal hypergraph capabilities."""
    logger.info("\n" + "=" * 70)
    logger.info("DEMONSTRATING TEMPORAL HYPERGRAPH")
    logger.info("=" * 70)
    
    # Create temporal graph
    temporal_graph = TemporalHypergraph()
    
    # Add nodes
    logger.info("\n1. Creating Temporal Graph")
    logger.info("-" * 70)
    
    for i in range(10):
        node = Node(
            node_id=f"agent_{i}",
            node_type="agent",
            attributes={'name': f"Agent {i}"}
        )
        node.initialize_embedding(dim=32)
        temporal_graph.add_node(node)
    
    logger.info(f"Added {len(temporal_graph.nodes)} nodes")
    
    # Add temporal edges
    logger.info("\n2. Adding Temporal Edges")
    logger.info("-" * 70)
    
    # Early collaborations (t=5.0)
    edge1 = Hyperedge(
        edge_id="collab_1",
        nodes={"agent_0", "agent_1", "agent_2"},
        edge_type="early_collaboration"
    )
    temporal_graph.add_temporal_hyperedge(edge1, timestamp=5.0)
    logger.info("Added collaboration at t=5.0: agent_0, agent_1, agent_2")
    
    # Later collaboration (t=10.0)
    edge2 = Hyperedge(
        edge_id="collab_2",
        nodes={"agent_3", "agent_4"},
        edge_type="later_collaboration"
    )
    temporal_graph.add_temporal_hyperedge(edge2, timestamp=10.0)
    logger.info("Added collaboration at t=10.0: agent_3, agent_4")
    
    # Remove first collaboration (t=15.0)
    temporal_graph.remove_temporal_hyperedge("collab_1", timestamp=15.0)
    logger.info("Removed collab_1 at t=15.0")
    
    # 3. Snapshots at different times
    logger.info("\n3. Creating Snapshots")
    logger.info("-" * 70)
    
    snapshot_7 = temporal_graph.snapshot_at_time(7.0)
    logger.info(f"Snapshot at t=7.0: {len(snapshot_7.hyperedges)} edges (collab_1 exists)")
    
    snapshot_12 = temporal_graph.snapshot_at_time(12.0)
    logger.info(f"Snapshot at t=12.0: {len(snapshot_12.hyperedges)} edges (both exist)")
    
    snapshot_20 = temporal_graph.snapshot_at_time(20.0)
    logger.info(f"Snapshot at t=20.0: {len(snapshot_20.hyperedges)} edges (collab_1 removed)")
    
    # 4. Temporal evolution
    logger.info("\n4. Temporal Evolution Analysis")
    logger.info("-" * 70)
    
    evolution = temporal_graph.get_temporal_evolution()
    logger.info(f"Total temporal events: {evolution['total_events']}")
    logger.info("Evolution timeline:")
    for event in evolution['evolution']:
        logger.info(f"  t={event['timestamp']:6.1f}: {event['num_edges']} edges ({event['event']})")


def demonstrate_attention_hypergnn():
    """Demonstrate attention-based HyperGNN."""
    logger.info("\n" + "=" * 70)
    logger.info("DEMONSTRATING ATTENTION-BASED HYPERGNN")
    logger.info("=" * 70)
    
    # Create layer
    layer = AttentionHyperGNNLayer(input_dim=32, output_dim=16)
    
    logger.info("\n1. Attention Weight Computation")
    logger.info("-" * 70)
    
    # Create sample embeddings
    embeddings = [np.random.randn(32) for _ in range(5)]
    weights = layer.compute_attention_weights(embeddings)
    
    logger.info(f"Computed attention weights for 5 nodes:")
    for i, w in enumerate(weights):
        logger.info(f"  Node {i}: {w:.4f}")
    logger.info(f"Sum of weights: {np.sum(weights):.6f} (should be ~1.0)")
    
    logger.info("\n2. Attention-Based Aggregation")
    logger.info("-" * 70)
    
    # Compare different aggregation types
    aggregation_types = ['mean', 'sum', 'max', 'attention']
    
    for agg_type in aggregation_types:
        aggregated = layer.aggregate_to_hyperedge(embeddings, agg_type)
        norm = np.linalg.norm(aggregated)
        logger.info(f"{agg_type:10s} aggregation -> norm: {norm:.4f}")


def demonstrate_hierarchical_hypergraph():
    """Demonstrate hierarchical hypergraph structures."""
    logger.info("\n" + "=" * 70)
    logger.info("DEMONSTRATING HIERARCHICAL HYPERGRAPH")
    logger.info("=" * 70)
    
    # Create base graph
    from hyper_gnn.hypergnn_model import Hypergraph
    
    base_graph = Hypergraph()
    
    logger.info("\n1. Creating Base Graph")
    logger.info("-" * 70)
    
    # Add 30 nodes
    for i in range(30):
        node = Node(
            node_id=f"case_{i}",
            node_type="legal_case",
            attributes={'case_number': i}
        )
        node.initialize_embedding(dim=32)
        base_graph.add_node(node)
    
    # Add edges
    for i in range(25):
        edge = Hyperedge(
            edge_id=f"connection_{i}",
            nodes={f"case_{i}", f"case_{(i+1)%30}", f"case_{(i+2)%30}"},
            edge_type="related_cases"
        )
        base_graph.add_hyperedge(edge)
    
    logger.info(f"Created base graph: {len(base_graph.nodes)} nodes, {len(base_graph.hyperedges)} edges")
    
    # 2. Build hierarchy
    logger.info("\n2. Building Hierarchy")
    logger.info("-" * 70)
    
    hierarchy = HierarchicalHypergraph()
    hierarchy.build_hierarchy(base_graph, num_levels=4)
    
    logger.info(f"Built {len(hierarchy.levels)} level hierarchy:")
    for i, level in enumerate(hierarchy.levels):
        logger.info(f"  Level {i}: {len(level.nodes)} nodes, {len(level.hyperedges)} edges")
    
    # 3. Hierarchy statistics
    logger.info("\n3. Hierarchy Statistics")
    logger.info("-" * 70)
    
    stats = hierarchy.get_statistics()
    logger.info(f"Total levels: {stats['num_levels']}")
    
    for level_stat in stats['level_stats']:
        reduction = 100 * (1 - level_stat['num_nodes'] / stats['level_stats'][0]['num_nodes'])
        logger.info(f"Level {level_stat['level']}: {level_stat['num_nodes']} nodes "
                   f"({reduction:.1f}% reduction from base)")


def main():
    """Run all demonstrations."""
    logger.info("🚀 Advanced Lex Hypergraph and HyperGNN Features Demo")
    logger.info("=" * 70)
    
    try:
        # Run demonstrations
        demonstrate_advanced_queries()
        demonstrate_visualization()
        demonstrate_temporal_hypergraph()
        demonstrate_attention_hypergnn()
        demonstrate_hierarchical_hypergraph()
        
        # Summary
        logger.info("\n" + "=" * 70)
        logger.info("✅ ALL DEMONSTRATIONS COMPLETED SUCCESSFULLY")
        logger.info("=" * 70)
        
        logger.info("\nGenerated files:")
        logger.info("  - /tmp/legal_graph.mmd (Mermaid diagram)")
        logger.info("  - /tmp/legal_graph.dot (Graphviz DOT)")
        logger.info("  - /tmp/legal_graph.json (JSON export)")
        
        logger.info("\nView Mermaid diagram:")
        logger.info("  - Upload to https://mermaid.live/")
        logger.info("  - View in GitHub (supports .mmd files)")
        
        logger.info("\nRender DOT graph:")
        logger.info("  - dot -Tpng /tmp/legal_graph.dot -o /tmp/legal_graph.png")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error during demonstration: {e}", exc_info=True)
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
