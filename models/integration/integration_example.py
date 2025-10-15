#!/usr/bin/env python3
"""
Lex-AD Hypergraph Integration Example

This example demonstrates the full integration of:
1. Lex hypergraph (legal framework from lex/ directory)
2. AD hypergraph (Agent-based + Discrete-event simulation models)
3. System Dynamics (Stocks and Flows)
4. HyperGNN (Hypergraph Neural Network)
5. Case-LLM Attention Mapping

This creates a unified framework for analyzing legal cases across multiple dimensions.
"""

import logging
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from integration.lex_ad_hypergraph_integration import (
    LexADIntegration,
    run_lex_ad_integration
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def example_basic_integration():
    """
    Run the basic Lex-AD integration pipeline.
    """
    logger.info("=" * 80)
    logger.info("EXAMPLE 1: Basic Lex-AD Hypergraph Integration")
    logger.info("=" * 80)
    
    # Run integration with default configuration
    results = run_lex_ad_integration()
    
    # Display key metrics
    print("\n" + "=" * 80)
    print("INTEGRATION RESULTS")
    print("=" * 80)
    print(f"\n1. LEX HYPERGRAPH (Legal Framework)")
    print(f"   - Total nodes: {results['lex_hypergraph']['num_nodes']}")
    print(f"   - Node types: {results['lex_hypergraph']['node_types']}")
    print(f"   - Legal branches loaded: civil, criminal, constitutional, etc.")
    
    print(f"\n2. AD HYPERGRAPH (Agent-based + Discrete-event)")
    print(f"   - Total nodes: {results['ad_hypergraph']['num_nodes']}")
    print(f"   - Agents: 8 (3 judges, 5 attorneys)")
    print(f"   - Events: 15 (case filings, hearings)")
    print(f"   - System stocks: 3 (case stages)")
    
    print(f"\n3. LEX-AD MAPPINGS")
    print(f"   - Mappings created: {results['mappings']['mappings_created']}")
    print(f"   - Agent-to-Legal mappings: {results['comprehensive_report']['mappings']['agent_to_legal']}")
    print(f"   - Event-to-Procedure mappings: {results['comprehensive_report']['mappings']['event_to_procedure']}")
    print(f"   - Stock-to-Stage mappings: {results['comprehensive_report']['mappings']['stock_to_stage']}")
    
    print(f"\n4. HYPERGNN INTEGRATION")
    print(f"   - Nodes embedded: {results['hypergnn_integration']['num_embeddings']}")
    print(f"   - Communities detected: {results['hypergnn_integration']['num_communities']}")
    print(f"   - Link predictions: {len(results['hypergnn_integration']['link_predictions'])}")
    print(f"   - Embedding dimension: {results['hypergnn_integration']['embedding_dim']}")
    
    print(f"\n5. CASE-LLM ATTENTION MAPPING")
    print(f"   - Attention heads: {results['attention_mapping']['num_heads']}")
    print(f"   - Embedding dimension: {results['attention_mapping']['embedding_dim']}")
    
    # Show sample attention head mappings
    print(f"\n   Sample Attention Head Mappings:")
    for mapping in results['attention_mapping']['mappings'][:3]:
        print(f"   - {mapping['head_id']} ({mapping['focus']}):")
        print(f"     Lex nodes: {len(mapping['lex_nodes'])}, AD nodes: {len(mapping['ad_nodes'])}")
    
    return results


def example_custom_configuration():
    """
    Run integration with custom configuration.
    """
    logger.info("\n" + "=" * 80)
    logger.info("EXAMPLE 2: Custom Configuration Integration")
    logger.info("=" * 80)
    
    # Custom configuration
    config = {
        'input_dim': 128,           # Larger embedding dimension
        'hidden_dim': 64,           # Larger hidden dimension
        'num_layers': 3,            # More GNN layers
        'num_attention_heads': 12,  # More attention heads
        'embedding_dim': 128
    }
    
    logger.info("\nCustom configuration:")
    logger.info(f"  - Input dimension: {config['input_dim']}")
    logger.info(f"  - Hidden dimension: {config['hidden_dim']}")
    logger.info(f"  - GNN layers: {config['num_layers']}")
    logger.info(f"  - Attention heads: {config['num_attention_heads']}")
    
    # Run with custom config
    results = run_lex_ad_integration(config)
    
    print("\n" + "=" * 80)
    print("CUSTOM CONFIGURATION RESULTS")
    print("=" * 80)
    print(f"HyperGNN Embedding Dimension: {results['hypergnn_integration']['embedding_dim']}")
    print(f"Attention Heads: {results['attention_mapping']['num_heads']}")
    print(f"Communities Detected: {results['hypergnn_integration']['num_communities']}")
    
    return results


def example_detailed_analysis():
    """
    Perform detailed analysis of the integrated hypergraph.
    """
    logger.info("\n" + "=" * 80)
    logger.info("EXAMPLE 3: Detailed Analysis of Integrated Hypergraph")
    logger.info("=" * 80)
    
    # Initialize integration
    integration = LexADIntegration()
    
    # Generate Lex hypergraph
    logger.info("\nAnalyzing Lex Hypergraph...")
    lex_stats = integration.generate_lex_hypergraph()
    
    # Query specific legal nodes
    from ggmlex.hypergraphql.schema import LegalNodeType
    
    # Get legal principles
    principles = integration.lex_engine.query_nodes(node_type=LegalNodeType.PRINCIPLE)
    logger.info(f"Found {len(principles.nodes)} legal principles")
    
    # Display some principles
    if principles.nodes:
        logger.info("\nSample Legal Principles:")
        for i, node in enumerate(principles.nodes[:5]):
            logger.info(f"  {i+1}. {node.name}")
            logger.info(f"     Content: {node.content[:80]}...")
    
    # Analyze node types
    logger.info(f"\nNode type distribution:")
    for node_type, count in lex_stats['node_types'].items():
        logger.info(f"  - {node_type}: {count}")
    
    print("\n" + "=" * 80)
    print("DETAILED ANALYSIS COMPLETE")
    print("=" * 80)
    print(f"The Lex hypergraph contains {lex_stats['num_nodes']} legal entities")
    print(f"spanning multiple branches of South African law.")
    
    return integration


def example_case_simulation():
    """
    Simulate a complete legal case using the integrated framework.
    """
    logger.info("\n" + "=" * 80)
    logger.info("EXAMPLE 4: Complete Legal Case Simulation")
    logger.info("=" * 80)
    
    from agent_based.case_agent_model import Agent, AgentType, AgentState, JudgeAgent
    from discrete_event.case_event_model import Event as CaseEvent, EventType
    from system_dynamics.case_dynamics_model import Stock
    
    # Create a realistic case scenario
    logger.info("\nCreating Case: 'Smith v. Jones Contract Dispute'")
    
    # Initialize integration
    integration = LexADIntegration()
    
    # Create case-specific agents
    judge = JudgeAgent(
        agent_id="judge_smith_v_jones",
        agent_type=AgentType.JUDGE,
        name="Judge Williams",
        state=AgentState.IDLE,
        efficiency=0.95
    )
    
    plaintiff_attorney = Agent(
        agent_id="attorney_plaintiff",
        agent_type=AgentType.ATTORNEY,
        name="Attorney Smith",
        state=AgentState.WORKING,
        workload=10
    )
    
    defendant_attorney = Agent(
        agent_id="attorney_defendant",
        agent_type=AgentType.ATTORNEY,
        name="Attorney Jones",
        state=AgentState.WORKING,
        workload=8
    )
    
    agents = [judge, plaintiff_attorney, defendant_attorney]
    
    # Create case timeline events
    events = [
        CaseEvent(time=0.0, event_type=EventType.CASE_FILED, case_id="smith_v_jones"),
        CaseEvent(time=30.0, event_type=EventType.DISCOVERY_COMPLETED, case_id="smith_v_jones"),
        CaseEvent(time=60.0, event_type=EventType.HEARING_SCHEDULED, case_id="smith_v_jones"),
        CaseEvent(time=90.0, event_type=EventType.HEARING_CONDUCTED, case_id="smith_v_jones"),
        CaseEvent(time=120.0, event_type=EventType.RULING_ISSUED, case_id="smith_v_jones"),
        CaseEvent(time=150.0, event_type=EventType.CASE_CLOSED, case_id="smith_v_jones")
    ]
    
    # Create system stocks for case
    stocks = {
        'filed_cases': Stock('filed_cases', 1.0, 1.0, [1.0]),
        'discovery_cases': Stock('discovery_cases', 1.0, 1.0, [1.0]),
        'trial_cases': Stock('trial_cases', 0.0, 0.0, [0.0]),
        'closed_cases': Stock('closed_cases', 0.0, 0.0, [0.0])
    }
    
    # Build AD hypergraph from case
    logger.info("\nBuilding AD hypergraph from case data...")
    ad_stats = integration.create_ad_hypergraph_from_agents(agents, events, stocks)
    
    # Map to legal framework
    logger.info("Mapping case to legal framework...")
    mapping_stats = integration.map_lex_to_ad()
    
    # Analyze with HyperGNN
    logger.info("Analyzing case with HyperGNN...")
    hypergnn_results = integration.integrate_with_hypergnn()
    
    # Map attention for Case-LLM
    logger.info("Mapping attention heads for legal analysis...")
    attention_results = integration.map_attention_heads_to_case_llm()
    
    print("\n" + "=" * 80)
    print("CASE SIMULATION COMPLETE: Smith v. Jones")
    print("=" * 80)
    print(f"\nCase Timeline: 6 events over 150 days")
    print(f"Participants: 3 agents (1 judge, 2 attorneys)")
    print(f"System stages: 4 (filing → discovery → trial → closure)")
    print(f"\nHyperGNN Analysis:")
    print(f"  - Communities detected: {hypergnn_results['num_communities']}")
    print(f"  - Link predictions: {len(hypergnn_results['link_predictions'])}")
    print(f"\nAttention Analysis:")
    print(f"  - Attention heads focused: {attention_results['num_heads']}")
    print(f"  - Key focus areas: legal entities, temporal events, case relationships")
    
    return integration


def main():
    """
    Run all integration examples.
    """
    print("=" * 80)
    print("LEX-AD HYPERGRAPH INTEGRATION EXAMPLES")
    print("=" * 80)
    print("\nDemonstrating integration of:")
    print("  1. Lex hypergraph (legal framework)")
    print("  2. AD hypergraph (agents + events)")
    print("  3. System Dynamics (stocks & flows)")
    print("  4. HyperGNN (neural network analysis)")
    print("  5. Case-LLM (attention mapping)")
    print("=" * 80)
    
    try:
        # Run examples
        print("\n\n")
        example_basic_integration()
        
        print("\n\n")
        example_custom_configuration()
        
        print("\n\n")
        example_detailed_analysis()
        
        print("\n\n")
        example_case_simulation()
        
        print("\n\n" + "=" * 80)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("\nKey Achievements:")
        print("  ✓ Lex hypergraph generated from legal framework")
        print("  ✓ AD hypergraph created from agents and events")
        print("  ✓ Lex-AD mapping established")
        print("  ✓ HyperGNN integration completed")
        print("  ✓ Attention heads mapped to Case-LLM")
        print("\nThe integrated framework is ready for:")
        print("  • Multi-dimensional case analysis")
        print("  • Legal precedent discovery")
        print("  • Agent behavior prediction")
        print("  • Timeline and workflow optimization")
        print("  • Attention-based legal reasoning")
        
    except Exception as e:
        logger.error(f"Error running examples: {e}", exc_info=True)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
