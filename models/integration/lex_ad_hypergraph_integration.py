#!/usr/bin/env python3
"""
Lex-AD Hypergraph Integration Module

This module integrates the Lex hypergraph (legal framework) with the AD hypergraph
(Agent-based + Discrete-event models) and synchronizes with HyperGNN and Case-LLM.

The integration enables:
1. Mapping legal framework entities to case simulation agents and events
2. Synchronizing agent behaviors with legal precedents and statutes
3. Tracking discrete events against legal timelines and procedures
4. Analyzing case dynamics using HyperGNN on the integrated hypergraph
5. Mapping Case-LLM attention heads to legal entities and case elements
"""

import logging
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional, Set, Tuple
from dataclasses import dataclass, field
import numpy as np

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ggmlex.hypergraphql.engine import HypergraphQLEngine
from ggmlex.hypergraphql.schema import (
    LegalNode, LegalHyperedge, LegalNodeType, LegalRelationType
)
from hyper_gnn.hypergnn_model import Hypergraph, Node, Hyperedge, HyperGNN
from agent_based.case_agent_model import Agent, AgentType, JudgeAgent
from discrete_event.case_event_model import Event as CaseEvent, EventType, CaseStatus
from system_dynamics.case_dynamics_model import Stock, Flow

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class IntegratedHypergraph:
    """
    Integrated hypergraph combining Lex (legal framework) and AD (agent-based + discrete-event).
    """
    lex_hypergraph: HypergraphQLEngine
    ad_hypergraph: Hypergraph
    
    # Mapping between Lex and AD nodes
    lex_to_ad_mapping: Dict[str, str] = field(default_factory=dict)
    ad_to_lex_mapping: Dict[str, str] = field(default_factory=dict)
    
    # Agent to legal entity mappings
    agent_to_legal_entity: Dict[str, str] = field(default_factory=dict)
    
    # Event to legal procedure mappings
    event_to_legal_procedure: Dict[str, str] = field(default_factory=dict)
    
    # Stock/Flow to legal framework mappings
    stock_to_legal_stage: Dict[str, str] = field(default_factory=dict)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the integrated hypergraph."""
        lex_stats = self.lex_hypergraph.get_statistics()
        ad_stats = self.ad_hypergraph.get_statistics()
        
        return {
            'lex_nodes': lex_stats['num_nodes'],
            'lex_edges': lex_stats['num_edges'],
            'ad_nodes': ad_stats['num_nodes'],
            'ad_edges': ad_stats['num_hyperedges'],
            'mappings': len(self.lex_to_ad_mapping),
            'agent_mappings': len(self.agent_to_legal_entity),
            'event_mappings': len(self.event_to_legal_procedure),
            'stock_mappings': len(self.stock_to_legal_stage)
        }


class LexADIntegration:
    """
    Main integration class for connecting Lex and AD hypergraphs with HyperGNN and Case-LLM.
    """
    
    def __init__(self, lex_path: Optional[str] = None):
        """
        Initialize the Lex-AD integration.
        
        Args:
            lex_path: Path to lex/ directory containing legal framework
        """
        self.lex_path = lex_path or "/home/runner/work/analyticase/analyticase/lex"
        
        # Initialize components
        self.lex_engine = HypergraphQLEngine(lex_path=self.lex_path)
        self.ad_hypergraph = Hypergraph()
        
        # Initialize HyperGNN for the integrated graph
        self.hyper_gnn: Optional[HyperGNN] = None
        
        # Create integrated hypergraph
        self.integrated = IntegratedHypergraph(
            lex_hypergraph=self.lex_engine,
            ad_hypergraph=self.ad_hypergraph
        )
        
        logger.info("Initialized Lex-AD Integration")
    
    def generate_lex_hypergraph(self) -> Dict[str, Any]:
        """
        Generate and return statistics about the Lex hypergraph.
        
        Returns:
            Dictionary with Lex hypergraph statistics
        """
        logger.info("Generating Lex hypergraph from legal framework...")
        stats = self.lex_engine.get_statistics()
        
        logger.info(f"Lex hypergraph generated:")
        logger.info(f"  - Nodes: {stats['num_nodes']}")
        logger.info(f"  - Edges: {stats['num_edges']}")
        logger.info(f"  - Node types: {stats['node_types']}")
        
        return stats
    
    def create_ad_hypergraph_from_agents(
        self, 
        agents: List[Agent],
        events: List[CaseEvent],
        stocks: Optional[Dict[str, Stock]] = None,
        embedding_dim: int = 64
    ) -> Dict[str, Any]:
        """
        Create AD hypergraph from agent-based model agents, discrete events, and stocks.
        
        Args:
            agents: List of agents from agent-based model
            events: List of events from discrete-event simulation
            stocks: Optional dictionary of stocks from system dynamics
            embedding_dim: Dimension for node embeddings (default: 64)
            
        Returns:
            Statistics about the created AD hypergraph
        """
        logger.info("Creating AD hypergraph from agents, events, and stocks...")
        
        # Store embedding dimension for later use
        self._embedding_dim = embedding_dim
        
        # Add agent nodes
        for agent in agents:
            node = Node(
                node_id=f"agent_{agent.agent_id}",
                node_type=agent.agent_type.value,
                attributes={
                    'name': agent.name,
                    'state': agent.state.value,
                    'workload': agent.workload,
                    'efficiency': agent.efficiency,
                    'cases_handled': len(agent.cases_handled)
                }
            )
            node.initialize_embedding(dim=embedding_dim)
            self.ad_hypergraph.add_node(node)
            
            # Map agent to legal entity if it's a judge, attorney, etc.
            if agent.agent_type in [AgentType.JUDGE, AgentType.ATTORNEY]:
                legal_entity_id = f"legal_entity_{agent.agent_type.value}_{agent.agent_id}"
                self.integrated.agent_to_legal_entity[f"agent_{agent.agent_id}"] = legal_entity_id
        
        # Add event nodes
        for event in events:
            node = Node(
                node_id=f"event_{event.event_type.value}_{event.case_id}",
                node_type=event.event_type.value,
                attributes={
                    'case_id': event.case_id,
                    'time': event.time,
                    'data': event.data
                }
            )
            node.initialize_embedding(dim=embedding_dim)
            self.ad_hypergraph.add_node(node)
            
            # Map event to legal procedure
            procedure_mapping = {
                EventType.CASE_FILED: "filing_procedure",
                EventType.HEARING_SCHEDULED: "hearing_procedure",
                EventType.HEARING_CONDUCTED: "trial_procedure",
                EventType.RULING_ISSUED: "judgment_procedure",
                EventType.APPEAL_FILED: "appeal_procedure",
                EventType.CASE_CLOSED: "closure_procedure"
            }
            
            if event.event_type in procedure_mapping:
                legal_proc = procedure_mapping[event.event_type]
                self.integrated.event_to_legal_procedure[
                    f"event_{event.event_type.value}_{event.case_id}"
                ] = legal_proc
        
        # Add stock nodes if provided
        if stocks:
            for stock_name, stock in stocks.items():
                node = Node(
                    node_id=f"stock_{stock_name}",
                    node_type="system_stock",
                    attributes={
                        'name': stock.name,
                        'current_value': stock.current_value,
                        'initial_value': stock.initial_value
                    }
                )
                node.initialize_embedding(dim=embedding_dim)
                self.ad_hypergraph.add_node(node)
                
                # Map stock to legal stage
                stage_mapping = {
                    'filed_cases': 'filing_stage',
                    'discovery_cases': 'discovery_stage',
                    'pre_trial_cases': 'pre_trial_stage',
                    'trial_cases': 'trial_stage',
                    'ruling_cases': 'ruling_stage',
                    'closed_cases': 'closure_stage'
                }
                
                if stock_name in stage_mapping:
                    self.integrated.stock_to_legal_stage[f"stock_{stock_name}"] = stage_mapping[stock_name]
        
        # Create hyperedges for agent interactions
        for agent in agents:
            if hasattr(agent, 'interactions') and agent.interactions:
                for interaction in agent.interactions:
                    agent1_id = f"agent_{interaction['agent_1']}"
                    agent2_id = f"agent_{interaction['agent_2']}"
                    
                    # Only create edge if both nodes exist
                    if agent1_id in self.ad_hypergraph.nodes and agent2_id in self.ad_hypergraph.nodes:
                        edge = Hyperedge(
                            edge_id=f"interaction_{agent1_id}_{agent2_id}",
                            nodes={agent1_id, agent2_id},
                            edge_type=interaction['type'],
                            weight=1.0 if interaction['outcome'] == 'success' else 0.5
                        )
                        self.ad_hypergraph.add_hyperedge(edge)
        
        stats = self.ad_hypergraph.get_statistics()
        logger.info(f"AD hypergraph created:")
        logger.info(f"  - Nodes: {stats['num_nodes']}")
        logger.info(f"  - Hyperedges: {stats['num_hyperedges']}")
        
        return stats
    
    def map_lex_to_ad(self) -> Dict[str, Any]:
        """
        Map Lex hypergraph nodes to AD hypergraph nodes based on semantic relationships.
        
        Returns:
            Mapping statistics
        """
        logger.info("Mapping Lex hypergraph to AD hypergraph...")
        
        mappings_created = 0
        
        # Map legal principles to agent behaviors
        principles = self.lex_engine.query_nodes(node_type=LegalNodeType.PRINCIPLE)
        for principle in principles.nodes:
            # Find related agents (e.g., judges should be aware of legal principles)
            for node_id in self.ad_hypergraph.nodes:
                if 'judge' in node_id.lower():
                    self.integrated.lex_to_ad_mapping[principle.node_id] = node_id
                    self.integrated.ad_to_lex_mapping[node_id] = principle.node_id
                    mappings_created += 1
                    break
        
        # Map statutes to legal procedures
        statutes = self.lex_engine.query_nodes(node_type=LegalNodeType.STATUTE)
        for statute in statutes.nodes:
            # Map to relevant event types
            for event_id, procedure in self.integrated.event_to_legal_procedure.items():
                if 'procedure' in procedure:
                    self.integrated.lex_to_ad_mapping[statute.node_id] = event_id
                    mappings_created += 1
        
        # Map cases to events
        cases = self.lex_engine.query_nodes(node_type=LegalNodeType.CASE)
        for case in cases.nodes:
            # Map to case events in AD hypergraph
            for node_id in self.ad_hypergraph.nodes:
                if 'event' in node_id and 'case' in node_id:
                    self.integrated.lex_to_ad_mapping[case.node_id] = node_id
                    self.integrated.ad_to_lex_mapping[node_id] = case.node_id
                    mappings_created += 1
                    break
        
        logger.info(f"Created {mappings_created} mappings between Lex and AD hypergraphs")
        
        return {
            'mappings_created': mappings_created,
            'total_lex_to_ad': len(self.integrated.lex_to_ad_mapping),
            'total_ad_to_lex': len(self.integrated.ad_to_lex_mapping)
        }
    
    def integrate_with_hypergnn(
        self,
        input_dim: int = 64,
        hidden_dim: int = 32,
        num_layers: int = 2
    ) -> Dict[str, Any]:
        """
        Integrate the combined Lex-AD hypergraph with HyperGNN.
        
        Args:
            input_dim: Input embedding dimension
            hidden_dim: Hidden layer dimension
            num_layers: Number of GNN layers
            
        Returns:
            HyperGNN analysis results including embeddings and communities
        """
        logger.info("Integrating with HyperGNN...")
        
        # Initialize HyperGNN
        self.hyper_gnn = HyperGNN(input_dim, hidden_dim, num_layers)
        
        # Forward pass through HyperGNN on AD hypergraph
        embeddings = self.hyper_gnn.forward(self.ad_hypergraph)
        
        # Detect communities in the integrated graph
        communities = self.hyper_gnn.detect_communities(self.ad_hypergraph, num_communities=5)
        
        # Update node embeddings in AD hypergraph
        for node_id, embedding in embeddings.items():
            if node_id in self.ad_hypergraph.nodes:
                self.ad_hypergraph.nodes[node_id].embeddings = embedding
        
        # Predict potential links
        predictions = []
        node_ids = list(self.ad_hypergraph.nodes.keys())
        if len(node_ids) >= 2:
            for i in range(min(10, len(node_ids))):
                for j in range(i + 1, min(10, len(node_ids))):
                    node1_id = node_ids[i]
                    node2_id = node_ids[j]
                    
                    if node1_id in embeddings and node2_id in embeddings:
                        score = self.hyper_gnn.predict_link(
                            embeddings[node1_id],
                            embeddings[node2_id]
                        )
                        
                        if score > 0.7:  # High confidence threshold
                            predictions.append({
                                'node1': node1_id,
                                'node2': node2_id,
                                'score': score
                            })
        
        logger.info(f"HyperGNN integration complete:")
        logger.info(f"  - Nodes embedded: {len(embeddings)}")
        logger.info(f"  - Communities detected: {len(set(communities.values()))}")
        logger.info(f"  - Link predictions: {len(predictions)}")
        
        return {
            'num_embeddings': len(embeddings),
            'num_communities': len(set(communities.values())),
            'communities': communities,
            'link_predictions': predictions,
            'embedding_dim': hidden_dim
        }
    
    def map_attention_heads_to_case_llm(
        self,
        num_attention_heads: int = 8,
        embedding_dim: int = 64
    ) -> Dict[str, Any]:
        """
        Map HyperGNN attention heads to Case-LLM components.
        
        This creates a mapping between the structural attention in HyperGNN
        (which entities are related) and the semantic attention in Case-LLM
        (which words/concepts are important).
        
        Args:
            num_attention_heads: Number of attention heads to simulate
            embedding_dim: Dimension of embeddings
            
        Returns:
            Attention mapping information
        """
        logger.info("Mapping attention heads to Case-LLM...")
        
        attention_mappings = []
        
        # Get nodes from both Lex and AD hypergraphs
        lex_nodes = list(self.lex_engine.nodes.keys())[:20]  # Limit for efficiency
        ad_nodes = list(self.ad_hypergraph.nodes.keys())[:20]
        
        # Create attention head mappings
        for head_idx in range(num_attention_heads):
            # Each attention head focuses on different aspects
            head_mapping = {
                'head_id': f"attention_head_{head_idx}",
                'focus': self._get_attention_focus(head_idx),
                'lex_nodes': [],
                'ad_nodes': [],
                'attention_weights': []
            }
            
            # Map head to relevant nodes
            focus = head_mapping['focus']
            
            if focus == 'legal_entities':
                # Focus on legal entities (judges, attorneys, parties)
                for node_id in ad_nodes:
                    if any(entity in node_id for entity in ['judge', 'attorney', 'agent']):
                        head_mapping['ad_nodes'].append(node_id)
                        head_mapping['attention_weights'].append(
                            float(np.random.beta(2, 5))  # Higher weights for relevant nodes
                        )
                
                # Map to legal nodes (cases, principles)
                for node_id in lex_nodes:
                    if any(entity in self.lex_engine.nodes[node_id].node_type.value 
                           for entity in ['case', 'principle']):
                        head_mapping['lex_nodes'].append(node_id)
            
            elif focus == 'temporal_events':
                # Focus on events and timeline
                for node_id in ad_nodes:
                    if 'event' in node_id or 'stock' in node_id:
                        head_mapping['ad_nodes'].append(node_id)
                        head_mapping['attention_weights'].append(
                            float(np.random.beta(2, 5))
                        )
            
            elif focus == 'legal_framework':
                # Focus on statutes, sections, and legal structure
                for node_id in lex_nodes:
                    if any(entity in self.lex_engine.nodes[node_id].node_type.value
                           for entity in ['statute', 'section']):
                        head_mapping['lex_nodes'].append(node_id)
            
            elif focus == 'case_relationships':
                # Focus on relationships between entities
                for node_id in ad_nodes:
                    if node_id in self.ad_hypergraph.node_to_edges:
                        # Nodes with many connections get higher attention
                        num_connections = len(self.ad_hypergraph.node_to_edges[node_id])
                        if num_connections > 0:
                            head_mapping['ad_nodes'].append(node_id)
                            head_mapping['attention_weights'].append(
                                float(min(1.0, num_connections / 5.0))
                            )
            
            attention_mappings.append(head_mapping)
        
        logger.info(f"Created {len(attention_mappings)} attention head mappings")
        for mapping in attention_mappings:
            logger.info(f"  - {mapping['head_id']} ({mapping['focus']}): "
                       f"{len(mapping['lex_nodes'])} Lex nodes, "
                       f"{len(mapping['ad_nodes'])} AD nodes")
        
        return {
            'num_heads': num_attention_heads,
            'mappings': attention_mappings,
            'embedding_dim': embedding_dim
        }
    
    def _get_attention_focus(self, head_idx: int) -> str:
        """Get the focus area for an attention head."""
        focuses = [
            'legal_entities',      # Head 0: Focus on judges, attorneys, parties
            'temporal_events',     # Head 1: Focus on event timeline
            'legal_framework',     # Head 2: Focus on statutes and laws
            'case_relationships',  # Head 3: Focus on entity relationships
            'evidence_chain',      # Head 4: Focus on evidence connections
            'procedural_flow',     # Head 5: Focus on procedural steps
            'precedent_links',     # Head 6: Focus on case precedents
            'multi_party'          # Head 7: Focus on multi-party interactions
        ]
        return focuses[head_idx % len(focuses)]
    
    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive report of the integrated Lex-AD hypergraph.
        
        Returns:
            Complete integration report
        """
        logger.info("Generating comprehensive integration report...")
        
        import datetime
        
        report = {
            'timestamp': datetime.datetime.now().isoformat(),
            'lex_hypergraph': self.generate_lex_hypergraph(),
            'ad_hypergraph': self.ad_hypergraph.get_statistics(),
            'integrated_statistics': self.integrated.get_statistics(),
            'mappings': {
                'lex_to_ad': len(self.integrated.lex_to_ad_mapping),
                'ad_to_lex': len(self.integrated.ad_to_lex_mapping),
                'agent_to_legal': len(self.integrated.agent_to_legal_entity),
                'event_to_procedure': len(self.integrated.event_to_legal_procedure),
                'stock_to_stage': len(self.integrated.stock_to_legal_stage)
            }
        }
        
        logger.info("=" * 70)
        logger.info("COMPREHENSIVE INTEGRATION REPORT")
        logger.info("=" * 70)
        logger.info(f"\nLex Hypergraph: {report['lex_hypergraph']['num_nodes']} nodes, "
                   f"{report['lex_hypergraph']['num_edges']} edges")
        logger.info(f"AD Hypergraph: {report['ad_hypergraph']['num_nodes']} nodes, "
                   f"{report['ad_hypergraph']['num_hyperedges']} hyperedges")
        logger.info(f"\nMappings:")
        logger.info(f"  - Lex to AD: {report['mappings']['lex_to_ad']}")
        logger.info(f"  - AD to Lex: {report['mappings']['ad_to_lex']}")
        logger.info(f"  - Agent to Legal Entity: {report['mappings']['agent_to_legal']}")
        logger.info(f"  - Event to Legal Procedure: {report['mappings']['event_to_procedure']}")
        logger.info(f"  - Stock to Legal Stage: {report['mappings']['stock_to_stage']}")
        
        return report


def run_lex_ad_integration(config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Run the complete Lex-AD hypergraph integration pipeline.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Complete integration results
    """
    if config is None:
        config = {}
    
    logger.info("=" * 70)
    logger.info("STARTING LEX-AD HYPERGRAPH INTEGRATION")
    logger.info("=" * 70)
    
    # Initialize integration
    integration = LexADIntegration()
    
    # Step 1: Generate Lex hypergraph
    logger.info("\n[Step 1/6] Generating Lex hypergraph...")
    lex_stats = integration.generate_lex_hypergraph()
    
    # Step 2: Create sample agents, events, and stocks for AD hypergraph
    logger.info("\n[Step 2/6] Creating AD hypergraph from simulation data...")
    
    # Import and create sample data
    from agent_based.case_agent_model import Agent, AgentType, AgentState, JudgeAgent
    from discrete_event.case_event_model import Event as CaseEvent, EventType
    from system_dynamics.case_dynamics_model import Stock
    
    # Create sample agents
    agents = [
        JudgeAgent(
            agent_id=f"judge_{i}",
            agent_type=AgentType.JUDGE,
            name=f"Judge {i}",
            state=AgentState.IDLE,
            efficiency=0.9
        )
        for i in range(3)
    ]
    
    agents.extend([
        Agent(
            agent_id=f"attorney_{i}",
            agent_type=AgentType.ATTORNEY,
            name=f"Attorney {i}",
            state=AgentState.WORKING,
            workload=5
        )
        for i in range(5)
    ])
    
    # Create sample events
    events = [
        CaseEvent(
            time=float(i * 10),
            event_type=EventType.CASE_FILED,
            case_id=f"case_{i}"
        )
        for i in range(10)
    ]
    
    events.extend([
        CaseEvent(
            time=float(i * 10 + 5),
            event_type=EventType.HEARING_SCHEDULED,
            case_id=f"case_{i}"
        )
        for i in range(5)
    ])
    
    # Create sample stocks
    stocks = {
        'filed_cases': Stock('filed_cases', 50.0, 50.0, [50.0]),
        'discovery_cases': Stock('discovery_cases', 30.0, 30.0, [30.0]),
        'trial_cases': Stock('trial_cases', 20.0, 20.0, [20.0])
    }
    
    ad_stats = integration.create_ad_hypergraph_from_agents(
        agents, events, stocks, 
        embedding_dim=config.get('input_dim', 64)
    )
    
    # Step 3: Map Lex to AD
    logger.info("\n[Step 3/6] Mapping Lex hypergraph to AD hypergraph...")
    mapping_stats = integration.map_lex_to_ad()
    
    # Step 4: Integrate with HyperGNN
    logger.info("\n[Step 4/6] Integrating with HyperGNN...")
    hypergnn_results = integration.integrate_with_hypergnn(
        input_dim=config.get('input_dim', 64),
        hidden_dim=config.get('hidden_dim', 32),
        num_layers=config.get('num_layers', 2)
    )
    
    # Step 5: Map attention heads to Case-LLM
    logger.info("\n[Step 5/6] Mapping attention heads to Case-LLM...")
    attention_results = integration.map_attention_heads_to_case_llm(
        num_attention_heads=config.get('num_attention_heads', 8),
        embedding_dim=config.get('embedding_dim', 64)
    )
    
    # Step 6: Generate comprehensive report
    logger.info("\n[Step 6/6] Generating comprehensive report...")
    report = integration.generate_comprehensive_report()
    
    # Compile final results
    results = {
        'lex_hypergraph': lex_stats,
        'ad_hypergraph': ad_stats,
        'mappings': mapping_stats,
        'hypergnn_integration': hypergnn_results,
        'attention_mapping': attention_results,
        'comprehensive_report': report
    }
    
    logger.info("\n" + "=" * 70)
    logger.info("LEX-AD HYPERGRAPH INTEGRATION COMPLETE")
    logger.info("=" * 70)
    logger.info(f"\nIntegration Summary:")
    logger.info(f"  - Lex nodes: {lex_stats['num_nodes']}")
    logger.info(f"  - AD nodes: {ad_stats['num_nodes']}")
    logger.info(f"  - Mappings created: {mapping_stats['mappings_created']}")
    logger.info(f"  - HyperGNN communities: {hypergnn_results['num_communities']}")
    logger.info(f"  - Attention heads: {attention_results['num_heads']}")
    logger.info(f"  - Link predictions: {len(hypergnn_results['link_predictions'])}")
    
    return results


if __name__ == "__main__":
    # Run the integration
    results = run_lex_ad_integration()
    
    # Print key results
    print("\n" + "=" * 70)
    print("KEY RESULTS")
    print("=" * 70)
    print(f"Lex Hypergraph: {results['lex_hypergraph']['num_nodes']} nodes")
    print(f"AD Hypergraph: {results['ad_hypergraph']['num_nodes']} nodes")
    print(f"Total Mappings: {results['mappings']['mappings_created']}")
    print(f"HyperGNN Communities: {results['hypergnn_integration']['num_communities']}")
    print(f"Attention Heads Mapped: {results['attention_mapping']['num_heads']}")
