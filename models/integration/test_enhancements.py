#!/usr/bin/env python3
"""
Tests for enhanced Lex hypergraph and model improvements.
"""

import unittest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from integration.lex_ad_hypergraph_integration import LexADIntegration
from agent_based.case_agent_model import Agent, AgentType, AgentState, JudgeAgent
from discrete_event.case_event_model import Event as CaseEvent, EventType
from system_dynamics.case_dynamics_model import Stock


class TestLexHypergraphEnhancements(unittest.TestCase):
    """Test enhancements to Lex hypergraph loading and parsing."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.integration = LexADIntegration()
    
    def test_enhanced_scheme_parsing(self):
        """Test that enhanced Scheme parsing extracts more metadata."""
        stats = self.integration.generate_lex_hypergraph()
        
        # Should have loaded legal entities
        self.assertGreater(stats['num_nodes'], 0)
        
        # Check that nodes have proper metadata
        for node_id, node in self.integration.lex_engine.nodes.items():
            self.assertIsNotNone(node.content)
            self.assertIn('metadata', node.__dict__)
            self.assertIsNotNone(node.jurisdiction)
    
    def test_relationship_extraction(self):
        """Test that relationships between legal concepts are extracted."""
        self.integration.generate_lex_hypergraph()
        
        # Should have extracted some edges representing relationships
        num_edges = len(self.integration.lex_engine.edges)
        self.assertGreater(num_edges, 0, "Should have extracted relationships between legal concepts")
    
    def test_node_type_inference(self):
        """Test that node types are properly inferred from definition names."""
        from ggmlex.hypergraphql.schema import LegalNodeType
        
        # Test the _infer_node_type method
        test_cases = [
            ('contract-valid?', [LegalNodeType.STATUTE, LegalNodeType.CONCEPT]),
            ('case-precedent', [LegalNodeType.CASE, LegalNodeType.CONCEPT]),
            ('section-123', [LegalNodeType.SECTION, LegalNodeType.CONCEPT]),
            ('negligence-principle', [LegalNodeType.PRINCIPLE, LegalNodeType.CONCEPT]),
        ]
        
        for name, expected_types in test_cases:
            inferred = self.integration.lex_engine._infer_node_type(name)
            self.assertIn(inferred, expected_types, 
                         f"Node type for '{name}' should be one of {expected_types}")


class TestHyperGNNEnhancements(unittest.TestCase):
    """Test enhancements to HyperGNN model."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.integration = LexADIntegration()
        
        # Create sample agents and events
        self.agents = [
            JudgeAgent(
                agent_id=f"judge_{i}",
                agent_type=AgentType.JUDGE,
                name=f"Judge {i}",
                state=AgentState.IDLE,
                efficiency=0.9
            )
            for i in range(3)
        ]
        
        self.events = [
            CaseEvent(
                time=float(i * 10),
                event_type=EventType.CASE_FILED,
                case_id=f"case_{i}"
            )
            for i in range(5)
        ]
        
        # Create AD hypergraph
        self.integration.create_ad_hypergraph_from_agents(
            self.agents, self.events, embedding_dim=64
        )
    
    def test_graph_level_pooling(self):
        """Test graph-level pooling functionality."""
        # Initialize HyperGNN
        results = self.integration.integrate_with_hypergnn(
            input_dim=64, hidden_dim=32, num_layers=2
        )
        
        # Test different pooling strategies
        pooling_types = ['mean', 'sum', 'max', 'attention']
        
        for pool_type in pooling_types:
            pooled = self.integration.hyper_gnn.graph_level_pooling(
                self.integration.ad_hypergraph, pool_type
            )
            
            # Should return embedding of correct dimension
            self.assertEqual(len(pooled), 32)  # hidden_dim
            self.assertFalse((pooled == 0).all(), 
                           f"Pooled embedding for {pool_type} should not be all zeros")
    
    def test_compute_graph_features(self):
        """Test comprehensive graph feature computation."""
        # Initialize HyperGNN
        self.integration.integrate_with_hypergnn(
            input_dim=64, hidden_dim=32, num_layers=2
        )
        
        # Compute graph features
        features = self.integration.hyper_gnn.compute_graph_features(
            self.integration.ad_hypergraph
        )
        
        # Check required features
        required_keys = [
            'mean_pooling', 'max_pooling', 'sum_pooling',
            'embedding_std', 'embedding_variance',
            'num_nodes', 'num_edges'
        ]
        
        for key in required_keys:
            self.assertIn(key, features, f"Graph features should include {key}")
        
        # Check dimensions
        self.assertEqual(len(features['mean_pooling']), 32)
        self.assertEqual(len(features['max_pooling']), 32)
        self.assertEqual(len(features['sum_pooling']), 32)
    
    def test_enhanced_link_prediction(self):
        """Test enhanced link prediction with multiple features."""
        # Initialize HyperGNN
        results = self.integration.integrate_with_hypergnn(
            input_dim=64, hidden_dim=32, num_layers=2
        )
        
        # Get link predictions
        predictions = results['link_predictions']
        
        if predictions:
            # Check that predictions have enhanced features
            pred = predictions[0]
            
            # Should have multiple similarity scores
            self.assertIn('cosine_similarity', pred)
            self.assertIn('euclidean_score', pred)
            self.assertIn('common_neighbors', pred)
            self.assertIn('combined_score', pred)
            
            # Scores should be in valid ranges
            self.assertGreaterEqual(pred['cosine_similarity'], -1)
            self.assertLessEqual(pred['cosine_similarity'], 1)
            self.assertGreaterEqual(pred['combined_score'], 0)
            self.assertLessEqual(pred['combined_score'], 1)
    
    def test_improved_community_detection(self):
        """Test improved k-means++ community detection."""
        # Initialize HyperGNN
        results = self.integration.integrate_with_hypergnn(
            input_dim=64, hidden_dim=32, num_layers=2
        )
        
        communities = results['communities']
        
        # Should have detected communities
        self.assertGreater(len(communities), 0)
        
        # Check that community IDs are valid
        community_ids = set(communities.values())
        self.assertGreater(len(community_ids), 0)
        self.assertLessEqual(len(community_ids), 5)  # num_communities=5


class TestIntegrationEnhancements(unittest.TestCase):
    """Test enhancements to the integration module."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.integration = LexADIntegration()
        
        # Create sample data
        self.agents = [
            JudgeAgent(
                agent_id=f"judge_{i}",
                agent_type=AgentType.JUDGE,
                name=f"Judge {i}",
                state=AgentState.IDLE,
                efficiency=0.9
            )
            for i in range(3)
        ]
        
        self.events = [
            CaseEvent(
                time=float(i * 10),
                event_type=EventType.CASE_FILED,
                case_id=f"case_{i}"
            )
            for i in range(5)
        ]
        
        # Add some variety to events
        self.events.extend([
            CaseEvent(
                time=55.0,
                event_type=EventType.HEARING_SCHEDULED,
                case_id="case_1"
            ),
            CaseEvent(
                time=90.0,
                event_type=EventType.HEARING_CONDUCTED,
                case_id="case_1"
            )
        ])
        
        # Create hypergraphs
        self.integration.generate_lex_hypergraph()
        self.integration.create_ad_hypergraph_from_agents(
            self.agents, self.events, embedding_dim=64
        )
        self.integration.map_lex_to_ad()
    
    def test_mapping_validation(self):
        """Test bidirectional mapping validation."""
        validation = self.integration.validate_mappings()
        
        # Check validation result structure
        self.assertIn('total_lex_to_ad', validation)
        self.assertIn('total_ad_to_lex', validation)
        self.assertIn('bidirectional_count', validation)
        self.assertIn('orphaned_mappings', validation)
        self.assertIn('validation_passed', validation)
        
        # Validation results should be consistent
        self.assertGreaterEqual(validation['total_lex_to_ad'], 0)
        self.assertGreaterEqual(validation['total_ad_to_lex'], 0)
        self.assertGreaterEqual(validation['bidirectional_count'], 0)
    
    def test_semantic_similarity_computation(self):
        """Test semantic similarity computation."""
        # Test with similar texts
        sim1 = self.integration.compute_semantic_similarity(
            "contract law and legal obligations",
            "legal contracts and obligations under law"
        )
        self.assertGreater(sim1, 0.3, "Similar texts should have positive similarity")
        
        # Test with dissimilar texts
        sim2 = self.integration.compute_semantic_similarity(
            "contract law",
            "criminal procedure"
        )
        self.assertLess(sim2, sim1, "Dissimilar texts should have lower similarity")
        
        # Test with empty text
        sim3 = self.integration.compute_semantic_similarity("", "some text")
        self.assertEqual(sim3, 0.0, "Empty text should have zero similarity")
    
    def test_temporal_sequence_analysis(self):
        """Test temporal event sequence analysis."""
        analysis = self.integration.analyze_temporal_sequences(self.events)
        
        # Check analysis structure
        self.assertIn('num_events', analysis)
        self.assertIn('event_types', analysis)
        self.assertIn('event_type_distribution', analysis)
        self.assertIn('avg_time_between_events', analysis)
        self.assertIn('common_sequences', analysis)
        
        # Check values
        self.assertEqual(analysis['num_events'], len(self.events))
        self.assertGreater(len(analysis['event_types']), 0)
        self.assertGreater(analysis['avg_time_between_events'], 0)
        
        # Should have detected some sequential patterns
        self.assertIsInstance(analysis['common_sequences'], list)
    
    def test_enhanced_attention_mapping(self):
        """Test enhanced attention head mapping with learned weights."""
        # First integrate with HyperGNN to get embeddings
        self.integration.integrate_with_hypergnn(
            input_dim=64, hidden_dim=32, num_layers=2
        )
        
        # Map attention heads with learned weights
        attention = self.integration.map_attention_heads_to_case_llm(
            num_attention_heads=8,
            embedding_dim=64,
            use_learned_weights=True
        )
        
        # Check structure
        self.assertEqual(attention['num_heads'], 8)
        self.assertIn('mappings', attention)
        
        # Check that learned weights are computed
        for mapping in attention['mappings']:
            self.assertIn('learned_weights', mapping)
            
            # If there are AD nodes, should have learned weights
            if mapping['ad_nodes']:
                self.assertEqual(len(mapping['learned_weights']), 
                               len(mapping['ad_nodes']))
                
                # Weights should be normalized (sum to ~1)
                if mapping['learned_weights']:
                    weight_sum = sum(mapping['learned_weights'])
                    self.assertAlmostEqual(weight_sum, 1.0, places=5)


class TestGraphFeatureAggregation(unittest.TestCase):
    """Test enhanced aggregation methods in HyperGNN."""
    
    def test_aggregation_types(self):
        """Test different aggregation strategies."""
        from hyper_gnn.hypergnn_model import HyperGNNLayer
        import numpy as np
        
        layer = HyperGNNLayer(input_dim=64, output_dim=32)
        
        # Create sample embeddings
        embeddings = [
            np.random.randn(64) for _ in range(5)
        ]
        
        # Test different aggregation types
        agg_types = ['mean', 'sum', 'max', 'attention']
        
        for agg_type in agg_types:
            result = layer.aggregate_to_hyperedge(embeddings, agg_type)
            
            # Result should have correct dimension
            self.assertEqual(len(result), 64)
            
            # Result should not be all zeros (with high probability)
            self.assertFalse((result == 0).all(), 
                           f"Aggregation result for {agg_type} should not be all zeros")


if __name__ == '__main__':
    unittest.main()
