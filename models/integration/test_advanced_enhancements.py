#!/usr/bin/env python3
"""
Tests for advanced enhancements to Lex hypergraph and HyperGNN model.
"""

import unittest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from integration.lex_ad_hypergraph_integration import LexADIntegration
from ggmlex.hypergraphql.visualization import HypergraphVisualizer, visualize_query_result
from hyper_gnn.hypergnn_model import (
    TemporalHypergraph, AttentionHyperGNNLayer, HierarchicalHypergraph,
    Node, Hyperedge, HyperGNN
)
from agent_based.case_agent_model import Agent, AgentType, AgentState, JudgeAgent
from discrete_event.case_event_model import Event as CaseEvent, EventType


class TestLexHypergraphAdvancedQueries(unittest.TestCase):
    """Test advanced query capabilities for Lex hypergraph."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.integration = LexADIntegration()
        self.integration.generate_lex_hypergraph()
    
    def test_subgraph_query(self):
        """Test subgraph extraction."""
        # Get some node IDs
        node_ids = list(self.integration.lex_engine.nodes.keys())[:5]
        
        # Query subgraph
        result = self.integration.lex_engine.query_subgraph(
            node_ids,
            include_edges=True,
            expand_neighbors=False
        )
        
        self.assertGreater(len(result.nodes), 0)
        self.assertIn('subgraph_query', result.metadata['query_type'])
    
    def test_subgraph_with_neighbors(self):
        """Test subgraph with neighbor expansion."""
        node_ids = list(self.integration.lex_engine.nodes.keys())[:3]
        
        result = self.integration.lex_engine.query_subgraph(
            node_ids,
            include_edges=True,
            expand_neighbors=True
        )
        
        # Should have more nodes than original due to expansion
        self.assertGreaterEqual(len(result.nodes), len(node_ids))
    
    def test_legal_reasoning_chain(self):
        """Test legal reasoning chain extraction."""
        # Get a node to start from
        node_ids = list(self.integration.lex_engine.nodes.keys())
        if node_ids:
            result = self.integration.lex_engine.query_legal_reasoning_chain(
                node_ids[0],
                max_depth=3
            )
            
            self.assertIsNotNone(result)
            self.assertEqual(result.metadata['query_type'], 'reasoning_chain')
    
    def test_similar_nodes_query(self):
        """Test finding similar nodes."""
        node_ids = list(self.integration.lex_engine.nodes.keys())
        if node_ids:
            result = self.integration.lex_engine.query_similar_nodes(
                node_ids[0],
                similarity_threshold=0.1,
                max_results=5
            )
            
            self.assertIsNotNone(result)
            self.assertEqual(result.metadata['query_type'], 'similarity_query')
            self.assertLessEqual(len(result.nodes), 5)


class TestHypergraphVisualization(unittest.TestCase):
    """Test hypergraph visualization utilities."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.integration = LexADIntegration()
        self.integration.generate_lex_hypergraph()
        self.visualizer = HypergraphVisualizer(self.integration.lex_engine)
    
    def test_mermaid_diagram_generation(self):
        """Test Mermaid diagram generation."""
        # Get a small subgraph
        node_ids = list(self.integration.lex_engine.nodes.keys())[:10]
        query_result = self.integration.lex_engine.query_subgraph(node_ids)
        
        diagram = self.visualizer.generate_mermaid_diagram(query_result, max_nodes=10)
        
        self.assertIsInstance(diagram, str)
        self.assertIn('graph TD', diagram)
        self.assertGreater(len(diagram), 0)
    
    def test_dot_graph_generation(self):
        """Test DOT/Graphviz generation."""
        node_ids = list(self.integration.lex_engine.nodes.keys())[:10]
        query_result = self.integration.lex_engine.query_subgraph(node_ids)
        
        dot_graph = self.visualizer.generate_dot_graph(query_result, max_nodes=10)
        
        self.assertIsInstance(dot_graph, str)
        self.assertIn('digraph LegalHypergraph', dot_graph)
        self.assertGreater(len(dot_graph), 0)
    
    def test_network_stats_summary(self):
        """Test network statistics generation."""
        stats = self.visualizer.generate_network_stats_summary()
        
        self.assertIn('num_nodes', stats)
        self.assertIn('num_edges', stats)
        self.assertIn('degree_distribution', stats)
        self.assertIn('top_connected_nodes', stats)
        self.assertGreater(stats['num_nodes'], 0)
    
    def test_json_export(self):
        """Test JSON export."""
        node_ids = list(self.integration.lex_engine.nodes.keys())[:5]
        query_result = self.integration.lex_engine.query_subgraph(node_ids)
        
        json_str = self.visualizer.export_to_json(query_result)
        
        self.assertIsInstance(json_str, str)
        self.assertIn('"nodes"', json_str)
        self.assertIn('"edges"', json_str)
    
    def test_visualize_query_result_helper(self):
        """Test helper function for visualization."""
        node_ids = list(self.integration.lex_engine.nodes.keys())[:5]
        query_result = self.integration.lex_engine.query_subgraph(node_ids)
        
        # Test different formats
        mermaid = visualize_query_result(self.integration.lex_engine, query_result, "mermaid")
        self.assertIn('graph TD', mermaid)
        
        dot = visualize_query_result(self.integration.lex_engine, query_result, "dot")
        self.assertIn('digraph', dot)
        
        json_output = visualize_query_result(self.integration.lex_engine, query_result, "json")
        self.assertIn('"nodes"', json_output)


class TestTemporalHypergraph(unittest.TestCase):
    """Test temporal hypergraph capabilities."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temporal_graph = TemporalHypergraph()
        
        # Add some nodes
        for i in range(5):
            node = Node(
                node_id=f"node_{i}",
                node_type="test",
                attributes={'index': i}
            )
            node.initialize_embedding(dim=32)
            self.temporal_graph.add_node(node)
    
    def test_temporal_edge_creation(self):
        """Test adding temporal hyperedges."""
        edge = Hyperedge(
            edge_id="temp_edge_1",
            nodes={"node_0", "node_1"},
            edge_type="temporal_link",
            weight=1.0
        )
        
        self.temporal_graph.add_temporal_hyperedge(edge, timestamp=1.0)
        
        self.assertIn("temp_edge_1", self.temporal_graph.hyperedges)
        self.assertIn("temp_edge_1", self.temporal_graph.temporal_edges)
    
    def test_temporal_edge_removal(self):
        """Test removing temporal edges."""
        edge = Hyperedge(
            edge_id="temp_edge_2",
            nodes={"node_0", "node_1"},
            edge_type="temporal_link"
        )
        
        self.temporal_graph.add_temporal_hyperedge(edge, timestamp=1.0)
        self.temporal_graph.remove_temporal_hyperedge("temp_edge_2", timestamp=2.0)
        
        events = self.temporal_graph.temporal_edges["temp_edge_2"]
        self.assertEqual(len(events), 2)
        self.assertEqual(events[1][1], 'removed')
    
    def test_snapshot_at_time(self):
        """Test getting snapshot at specific time."""
        # Add edges at different times
        edge1 = Hyperedge(edge_id="e1", nodes={"node_0", "node_1"}, edge_type="link")
        edge2 = Hyperedge(edge_id="e2", nodes={"node_2", "node_3"}, edge_type="link")
        
        self.temporal_graph.add_temporal_hyperedge(edge1, timestamp=1.0)
        self.temporal_graph.add_temporal_hyperedge(edge2, timestamp=3.0)
        
        # Snapshot at t=2.0 should only have edge1
        snapshot = self.temporal_graph.snapshot_at_time(2.0)
        self.assertEqual(len(snapshot.hyperedges), 1)
        self.assertIn("e1", snapshot.hyperedges)
        
        # Snapshot at t=4.0 should have both edges
        snapshot = self.temporal_graph.snapshot_at_time(4.0)
        self.assertEqual(len(snapshot.hyperedges), 2)
    
    def test_temporal_evolution(self):
        """Test temporal evolution tracking."""
        edge = Hyperedge(edge_id="e_evolve", nodes={"node_0", "node_1"}, edge_type="link")
        self.temporal_graph.add_temporal_hyperedge(edge, timestamp=1.0)
        self.temporal_graph.remove_temporal_hyperedge("e_evolve", timestamp=5.0)
        
        evolution = self.temporal_graph.get_temporal_evolution()
        
        self.assertEqual(evolution['total_events'], 2)
        self.assertGreater(len(evolution['evolution']), 0)


class TestAttentionHyperGNN(unittest.TestCase):
    """Test attention-based HyperGNN layer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.layer = AttentionHyperGNNLayer(input_dim=32, output_dim=16)
    
    def test_attention_weight_computation(self):
        """Test attention weight computation."""
        embeddings = [
            np.random.randn(32) for _ in range(5)
        ]
        
        weights = self.layer.compute_attention_weights(embeddings)
        
        self.assertEqual(len(weights), 5)
        # Weights should sum to approximately 1
        self.assertAlmostEqual(np.sum(weights), 1.0, places=5)
        # All weights should be non-negative
        self.assertTrue(np.all(weights >= 0))
    
    def test_attention_aggregation(self):
        """Test attention-based aggregation."""
        embeddings = [
            np.random.randn(32) for _ in range(5)
        ]
        
        aggregated = self.layer.aggregate_to_hyperedge(embeddings, 'attention')
        
        self.assertEqual(aggregated.shape, (32,))
        self.assertFalse(np.all(aggregated == 0))


class TestHierarchicalHypergraph(unittest.TestCase):
    """Test hierarchical hypergraph structures."""
    
    def setUp(self):
        """Set up test fixtures."""
        from hyper_gnn.hypergnn_model import Hypergraph
        
        # Create base graph
        self.base_graph = Hypergraph()
        for i in range(20):
            node = Node(node_id=f"node_{i}", node_type="base", attributes={})
            node.initialize_embedding(dim=32)
            self.base_graph.add_node(node)
        
        # Add some edges
        for i in range(15):
            edge = Hyperedge(
                edge_id=f"edge_{i}",
                nodes={f"node_{i}", f"node_{(i+1)%20}"},
                edge_type="link"
            )
            self.base_graph.add_hyperedge(edge)
    
    def test_hierarchical_graph_creation(self):
        """Test creating hierarchical structure."""
        hierarchy = HierarchicalHypergraph()
        hierarchy.build_hierarchy(self.base_graph, num_levels=3)
        
        self.assertEqual(len(hierarchy.levels), 3)
        self.assertGreater(len(hierarchy.levels[0].nodes), len(hierarchy.levels[1].nodes))
    
    def test_graph_coarsening(self):
        """Test coarsening operation."""
        hierarchy = HierarchicalHypergraph()
        coarse_graph, mapping = hierarchy.coarsen_graph(self.base_graph, num_clusters=5)
        
        self.assertEqual(len(coarse_graph.nodes), 5)
        self.assertEqual(len(mapping), 20)  # All base nodes should be mapped
    
    def test_hierarchy_statistics(self):
        """Test getting hierarchy statistics."""
        hierarchy = HierarchicalHypergraph()
        hierarchy.build_hierarchy(self.base_graph, num_levels=3)
        
        stats = hierarchy.get_statistics()
        
        self.assertEqual(stats['num_levels'], 3)
        self.assertEqual(len(stats['level_stats']), 3)


# Import numpy for attention tests
import numpy as np


if __name__ == '__main__':
    unittest.main()
