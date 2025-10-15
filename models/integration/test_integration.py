#!/usr/bin/env python3
"""
Tests for Lex-AD Hypergraph Integration

This module contains comprehensive tests for the integration between
Lex hypergraph, AD hypergraph, HyperGNN, and Case-LLM attention mapping.
"""

import unittest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from integration.lex_ad_hypergraph_integration import (
    LexADIntegration,
    IntegratedHypergraph,
    run_lex_ad_integration
)
from agent_based.case_agent_model import Agent, AgentType, AgentState, JudgeAgent
from discrete_event.case_event_model import Event as CaseEvent, EventType
from system_dynamics.case_dynamics_model import Stock


class TestLexADIntegration(unittest.TestCase):
    """Test cases for Lex-AD integration."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.integration = LexADIntegration()
    
    def test_initialization(self):
        """Test that integration initializes properly."""
        self.assertIsNotNone(self.integration.lex_engine)
        self.assertIsNotNone(self.integration.ad_hypergraph)
        self.assertIsNotNone(self.integration.integrated)
    
    def test_lex_hypergraph_generation(self):
        """Test Lex hypergraph generation from legal framework."""
        stats = self.integration.generate_lex_hypergraph()
        
        self.assertIn('num_nodes', stats)
        self.assertIn('num_edges', stats)
        self.assertIn('node_types', stats)
        self.assertGreater(stats['num_nodes'], 0)
    
    def test_ad_hypergraph_creation(self):
        """Test AD hypergraph creation from agents and events."""
        # Create sample agents
        agents = [
            JudgeAgent(
                agent_id="test_judge",
                agent_type=AgentType.JUDGE,
                name="Test Judge",
                state=AgentState.IDLE,
                efficiency=0.9
            ),
            Agent(
                agent_id="test_attorney",
                agent_type=AgentType.ATTORNEY,
                name="Test Attorney",
                state=AgentState.WORKING,
                workload=5
            )
        ]
        
        # Create sample events
        events = [
            CaseEvent(time=0.0, event_type=EventType.CASE_FILED, case_id="test_case"),
            CaseEvent(time=10.0, event_type=EventType.HEARING_SCHEDULED, case_id="test_case")
        ]
        
        # Create sample stocks
        stocks = {
            'filed_cases': Stock('filed_cases', 10.0, 10.0, [10.0])
        }
        
        # Create AD hypergraph
        stats = self.integration.create_ad_hypergraph_from_agents(agents, events, stocks)
        
        self.assertIn('num_nodes', stats)
        self.assertIn('num_hyperedges', stats)
        self.assertGreater(stats['num_nodes'], 0)
    
    def test_lex_to_ad_mapping(self):
        """Test mapping between Lex and AD hypergraphs."""
        # First create AD hypergraph
        agents = [
            JudgeAgent(
                agent_id="test_judge",
                agent_type=AgentType.JUDGE,
                name="Test Judge",
                state=AgentState.IDLE,
                efficiency=0.9
            )
        ]
        
        events = [
            CaseEvent(time=0.0, event_type=EventType.CASE_FILED, case_id="test_case")
        ]
        
        self.integration.create_ad_hypergraph_from_agents(agents, events)
        
        # Create mappings
        mapping_stats = self.integration.map_lex_to_ad()
        
        self.assertIn('mappings_created', mapping_stats)
        self.assertIn('total_lex_to_ad', mapping_stats)
        self.assertIn('total_ad_to_lex', mapping_stats)
    
    def test_hypergnn_integration(self):
        """Test HyperGNN integration with the hypergraph."""
        # Create AD hypergraph
        agents = [
            Agent(
                agent_id=f"agent_{i}",
                agent_type=AgentType.ATTORNEY,
                name=f"Agent {i}",
                state=AgentState.IDLE
            )
            for i in range(5)
        ]
        
        events = [
            CaseEvent(time=float(i), event_type=EventType.CASE_FILED, case_id=f"case_{i}")
            for i in range(3)
        ]
        
        self.integration.create_ad_hypergraph_from_agents(agents, events)
        
        # Integrate with HyperGNN
        results = self.integration.integrate_with_hypergnn(
            input_dim=64,
            hidden_dim=32,
            num_layers=2
        )
        
        self.assertIn('num_embeddings', results)
        self.assertIn('num_communities', results)
        self.assertIn('communities', results)
        self.assertIn('link_predictions', results)
        self.assertGreater(results['num_embeddings'], 0)
    
    def test_attention_head_mapping(self):
        """Test attention head mapping to Case-LLM."""
        # Create AD hypergraph
        agents = [
            JudgeAgent(
                agent_id="test_judge",
                agent_type=AgentType.JUDGE,
                name="Test Judge",
                state=AgentState.IDLE,
                efficiency=0.9
            )
        ]
        
        events = [
            CaseEvent(time=0.0, event_type=EventType.CASE_FILED, case_id="test_case")
        ]
        
        self.integration.create_ad_hypergraph_from_agents(agents, events)
        
        # Map attention heads
        results = self.integration.map_attention_heads_to_case_llm(
            num_attention_heads=8,
            embedding_dim=64
        )
        
        self.assertIn('num_heads', results)
        self.assertIn('mappings', results)
        self.assertIn('embedding_dim', results)
        self.assertEqual(results['num_heads'], 8)
        self.assertEqual(len(results['mappings']), 8)
        
        # Check mapping structure
        for mapping in results['mappings']:
            self.assertIn('head_id', mapping)
            self.assertIn('focus', mapping)
            self.assertIn('lex_nodes', mapping)
            self.assertIn('ad_nodes', mapping)
    
    def test_integrated_statistics(self):
        """Test integrated hypergraph statistics."""
        # Create sample data
        agents = [
            Agent(
                agent_id=f"agent_{i}",
                agent_type=AgentType.ATTORNEY,
                name=f"Agent {i}",
                state=AgentState.IDLE
            )
            for i in range(3)
        ]
        
        events = [
            CaseEvent(time=0.0, event_type=EventType.CASE_FILED, case_id="test_case")
        ]
        
        stocks = {
            'filed_cases': Stock('filed_cases', 5.0, 5.0, [5.0])
        }
        
        self.integration.create_ad_hypergraph_from_agents(agents, events, stocks)
        
        # Get statistics
        stats = self.integration.integrated.get_statistics()
        
        self.assertIn('lex_nodes', stats)
        self.assertIn('lex_edges', stats)
        self.assertIn('ad_nodes', stats)
        self.assertIn('ad_edges', stats)
        self.assertIn('mappings', stats)
    
    def test_agent_to_legal_entity_mapping(self):
        """Test mapping of agents to legal entities."""
        agents = [
            JudgeAgent(
                agent_id="judge_1",
                agent_type=AgentType.JUDGE,
                name="Judge Smith",
                state=AgentState.IDLE,
                efficiency=0.9
            ),
            Agent(
                agent_id="attorney_1",
                agent_type=AgentType.ATTORNEY,
                name="Attorney Jones",
                state=AgentState.WORKING,
                workload=5
            )
        ]
        
        self.integration.create_ad_hypergraph_from_agents(agents, [])
        
        # Check agent mappings
        agent_mappings = self.integration.integrated.agent_to_legal_entity
        self.assertGreater(len(agent_mappings), 0)
        self.assertIn('agent_judge_1', agent_mappings)
        self.assertIn('agent_attorney_1', agent_mappings)
    
    def test_event_to_procedure_mapping(self):
        """Test mapping of events to legal procedures."""
        events = [
            CaseEvent(time=0.0, event_type=EventType.CASE_FILED, case_id="case_1"),
            CaseEvent(time=10.0, event_type=EventType.HEARING_SCHEDULED, case_id="case_1"),
            CaseEvent(time=20.0, event_type=EventType.RULING_ISSUED, case_id="case_1")
        ]
        
        self.integration.create_ad_hypergraph_from_agents([], events)
        
        # Check event mappings
        event_mappings = self.integration.integrated.event_to_legal_procedure
        self.assertGreater(len(event_mappings), 0)
    
    def test_stock_to_stage_mapping(self):
        """Test mapping of stocks to legal stages."""
        stocks = {
            'filed_cases': Stock('filed_cases', 10.0, 10.0, [10.0]),
            'discovery_cases': Stock('discovery_cases', 5.0, 5.0, [5.0]),
            'trial_cases': Stock('trial_cases', 3.0, 3.0, [3.0])
        }
        
        self.integration.create_ad_hypergraph_from_agents([], [], stocks)
        
        # Check stock mappings
        stock_mappings = self.integration.integrated.stock_to_legal_stage
        self.assertGreater(len(stock_mappings), 0)
        self.assertIn('stock_filed_cases', stock_mappings)
        self.assertEqual(stock_mappings['stock_filed_cases'], 'filing_stage')


class TestRunLexADIntegration(unittest.TestCase):
    """Test the complete integration pipeline."""
    
    def test_run_integration_default_config(self):
        """Test running integration with default configuration."""
        results = run_lex_ad_integration()
        
        # Check all expected keys are present
        self.assertIn('lex_hypergraph', results)
        self.assertIn('ad_hypergraph', results)
        self.assertIn('mappings', results)
        self.assertIn('hypergnn_integration', results)
        self.assertIn('attention_mapping', results)
        self.assertIn('comprehensive_report', results)
    
    def test_run_integration_custom_config(self):
        """Test running integration with custom configuration."""
        config = {
            'input_dim': 128,
            'hidden_dim': 64,
            'num_layers': 3,
            'num_attention_heads': 12,
            'embedding_dim': 128
        }
        
        results = run_lex_ad_integration(config)
        
        # Check custom config is applied
        self.assertEqual(results['hypergnn_integration']['embedding_dim'], 64)
        self.assertEqual(results['attention_mapping']['num_heads'], 12)
        self.assertEqual(results['attention_mapping']['embedding_dim'], 128)
    
    def test_integration_produces_valid_results(self):
        """Test that integration produces valid results."""
        results = run_lex_ad_integration()
        
        # Validate Lex hypergraph results
        self.assertGreater(results['lex_hypergraph']['num_nodes'], 0)
        
        # Validate AD hypergraph results
        self.assertGreater(results['ad_hypergraph']['num_nodes'], 0)
        
        # Validate mappings
        self.assertGreaterEqual(results['mappings']['mappings_created'], 0)
        
        # Validate HyperGNN results
        self.assertGreater(results['hypergnn_integration']['num_embeddings'], 0)
        self.assertGreater(results['hypergnn_integration']['num_communities'], 0)
        
        # Validate attention mapping
        self.assertEqual(results['attention_mapping']['num_heads'], 8)


class TestAttentionFocus(unittest.TestCase):
    """Test attention focus assignment."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.integration = LexADIntegration()
    
    def test_attention_focus_assignment(self):
        """Test that attention heads are assigned correct focus areas."""
        focuses = [
            self.integration._get_attention_focus(i)
            for i in range(8)
        ]
        
        expected_focuses = [
            'legal_entities',
            'temporal_events',
            'legal_framework',
            'case_relationships',
            'evidence_chain',
            'procedural_flow',
            'precedent_links',
            'multi_party'
        ]
        
        self.assertEqual(focuses, expected_focuses)
    
    def test_attention_focus_cycles(self):
        """Test that attention focus cycles correctly for head indices > 7."""
        focus_8 = self.integration._get_attention_focus(8)
        focus_0 = self.integration._get_attention_focus(0)
        self.assertEqual(focus_8, focus_0)


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestLexADIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestRunLexADIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestAttentionFocus))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
