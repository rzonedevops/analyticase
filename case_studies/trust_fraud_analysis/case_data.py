#!/usr/bin/env python3
"""
Trust Fraud Analysis Case Data

This module provides the structured case data for the trust fraud analysis,
ready to be used with the HyperGNN model for analysis and visualization.
"""

from typing import Dict, Any, List


def get_case_data() -> Dict[str, Any]:
    """
    Returns structured case data for the trust fraud analysis.
    
    Returns:
        Dictionary containing agents, events, and relationships
    """
    
    # Define agents with their attributes
    agents = [
        {
            'id': 'BANTJIES',
            'type': 'agent',
            'name': 'Bantjies',
            'role': 'Central Orchestrator',
            'centrality': 1.0,
            'attributes': {
                'influence_level': 'highest',
                'role_type': 'orchestrator'
            }
        },
        {
            'id': 'RYNETTE',
            'type': 'agent',
            'name': 'Rynette',
            'role': 'Revenue Coordinator',
            'centrality': 0.46,
            'attributes': {
                'influence_level': 'high',
                'role_type': 'coordinator'
            }
        },
        {
            'id': 'JACQUI',
            'type': 'agent',
            'name': 'Jacqui',
            'role': 'Signature Authority',
            'centrality': 0.36,
            'attributes': {
                'influence_level': 'medium-high',
                'role_type': 'authority'
            }
        },
        {
            'id': 'PETER',
            'type': 'agent',
            'name': 'Peter',
            'role': 'Manipulated Puppet',
            'centrality': 0.15,
            'attributes': {
                'influence_level': 'low',
                'role_type': 'puppet'
            }
        },
        {
            'id': 'DANIEL',
            'type': 'agent',
            'name': 'Daniel',
            'role': 'Marginalized Whistleblower',
            'centrality': -0.15,
            'attributes': {
                'influence_level': 'negative',
                'role_type': 'marginalized'
            }
        }
    ]
    
    # Define key events
    events = [
        {
            'id': 'TRUSTEE',
            'type': 'event',
            'name': 'Trustee Appointment',
            'date': '2024-07-01',
            'category': 'positioning',
            'description': 'Initial trustee appointment to establish control'
        },
        {
            'id': 'AUTHORITY',
            'type': 'event',
            'name': 'Authority Appointment',
            'date': '2024-10-01',
            'category': 'positioning',
            'description': 'Authority appointment to consolidate oversight'
        },
        {
            'id': 'REPORTS',
            'type': 'event',
            'name': 'Daniel Fraud Reports',
            'date': '2025-06-06',
            'category': 'whistleblowing',
            'description': 'Daniel reports suspected fraud activities'
        },
        {
            'id': 'CARDS',
            'type': 'event',
            'name': 'Card Cancellations',
            'date': '2025-06-07',
            'category': 'crisis',
            'description': 'Strategic card cancellations in response to reports'
        },
        {
            'id': 'R10M',
            'type': 'event',
            'name': 'R10M Identification',
            'date': '2025-06-10T09:00:00',
            'category': 'threat',
            'description': 'R10M financial discrepancy identified'
        },
        {
            'id': 'HOLIDAY',
            'type': 'event',
            'name': 'Holiday Dismissal',
            'date': '2025-06-10T14:00:00',
            'category': 'abandonment',
            'description': 'Daniel dismissed during holiday period'
        },
        {
            'id': 'MAIN',
            'type': 'event',
            'name': 'Main Trustee Appointment',
            'date': '2025-08-11',
            'category': 'bypassing',
            'description': 'Main trustee appointment to bypass oversight'
        },
        {
            'id': 'INTERDICT',
            'type': 'event',
            'name': 'Ex Parte Interdict',
            'date': '2025-08-13',
            'category': 'weaponization',
            'description': 'Ex parte interdict filed against whistleblower'
        },
        {
            'id': 'AFFIDAVIT',
            'type': 'event',
            'name': 'Supporting Affidavit',
            'date': '2025-08-15',
            'category': 'perjury',
            'description': 'Supporting affidavit with false statements'
        },
        {
            'id': 'R18M',
            'type': 'event',
            'name': 'R18M Payout Target',
            'date': '2026-05-01',
            'category': 'extraction',
            'description': 'Target R18M payout - ultimate goal'
        }
    ]
    
    # Define hyperedge relationships with attention weights
    relationships = [
        {
            'id': 'edge_1',
            'type': 'Financial Information Control',
            'participants': ['BANTJIES', 'TRUSTEE', 'AUTHORITY', 'R18M'],
            'weight': 0.95,
            'description': 'Control of financial information and authority'
        },
        {
            'id': 'edge_2',
            'type': 'Trust Governance Manipulation',
            'participants': ['BANTJIES', 'TRUSTEE', 'MAIN'],
            'weight': 0.92,
            'description': 'Manipulation of trust governance structure'
        },
        {
            'id': 'edge_3',
            'type': 'Oversight Authority Abuse',
            'participants': ['BANTJIES', 'AUTHORITY', 'HOLIDAY'],
            'weight': 0.89,
            'description': 'Abuse of oversight authority for dismissal'
        },
        {
            'id': 'edge_4',
            'type': 'Whistleblower Neutralization',
            'participants': ['DANIEL', 'REPORTS', 'BANTJIES', 'HOLIDAY', 'INTERDICT'],
            'weight': 0.87,
            'description': 'Systematic neutralization of whistleblower'
        },
        {
            'id': 'edge_5',
            'type': 'Puppet Orchestration',
            'participants': ['BANTJIES', 'PETER', 'CARDS', 'INTERDICT'],
            'weight': 0.85,
            'description': 'Using Peter as puppet to execute actions'
        },
        {
            'id': 'edge_6',
            'type': 'Timeline Coordination',
            'participants': ['MAIN', 'INTERDICT', 'AFFIDAVIT'],
            'weight': 0.83,
            'description': 'Temporal coordination of legal actions'
        },
        {
            'id': 'edge_7',
            'type': 'Payout Motivation',
            'participants': ['R18M', 'BANTJIES', 'TRUSTEE', 'AUTHORITY', 'HOLIDAY', 'MAIN', 'INTERDICT'],
            'weight': 1.0,
            'description': 'R18M payout as universal motivation for all actions'
        }
    ]
    
    # Define temporal causality chains
    causal_chains = [
        {
            'from': 'REPORTS',
            'to': 'CARDS',
            'relationship': 'next day',
            'delay_hours': 24
        },
        {
            'from': 'R10M',
            'to': 'HOLIDAY',
            'relationship': 'same day PM',
            'delay_hours': 5
        },
        {
            'from': 'MAIN',
            'to': 'INTERDICT',
            'relationship': '2 days later',
            'delay_hours': 48
        }
    ]
    
    # Define hidden narratives (subgraphs)
    narratives = [
        {
            'id': 'narrative_1',
            'name': 'Financial Control Architecture',
            'nodes': ['TRUSTEE', 'AUTHORITY', 'R18M'],
            'description': 'Building systematic control over trust finances'
        },
        {
            'id': 'narrative_2',
            'name': 'Whistleblower Neutralization',
            'nodes': ['REPORTS', 'HOLIDAY', 'INTERDICT'],
            'description': 'Systematic suppression of fraud reporting'
        },
        {
            'id': 'narrative_3',
            'name': 'Dual-Layer Operations',
            'nodes': ['CARDS', 'MAIN', 'AFFIDAVIT'],
            'description': 'Operating through both institutional and legal channels'
        }
    ]
    
    # Combine all entities
    entities = agents + events
    
    return {
        'case_id': 'trust_fraud_2024_2026',
        'case_name': 'Trust Fraud Analysis',
        'entities': entities,
        'agents': agents,
        'events': events,
        'relationships': relationships,
        'causal_chains': causal_chains,
        'narratives': narratives,
        'metadata': {
            'analysis_date': '2025-10-17',
            'num_agents': len(agents),
            'num_events': len(events),
            'num_hyperedges': len(relationships),
            'temporal_span': '2024-07-01 to 2026-05-01'
        }
    }


def get_centrality_scores() -> Dict[str, float]:
    """
    Returns centrality scores for all agents.
    
    Returns:
        Dictionary mapping agent IDs to centrality scores
    """
    return {
        'BANTJIES': 1.0,
        'RYNETTE': 0.46,
        'JACQUI': 0.36,
        'PETER': 0.15,
        'DANIEL': -0.15
    }


def get_attention_weights() -> Dict[str, float]:
    """
    Returns attention weights for all hyperedges.
    
    Returns:
        Dictionary mapping hyperedge types to attention weights
    """
    return {
        'Financial Information Control': 0.95,
        'Trust Governance Manipulation': 0.92,
        'Oversight Authority Abuse': 0.89,
        'Whistleblower Neutralization': 0.87,
        'Puppet Orchestration': 0.85,
        'Timeline Coordination': 0.83,
        'Payout Motivation': 1.0
    }


def get_agent_by_id(agent_id: str) -> Dict[str, Any]:
    """
    Get agent data by ID.
    
    Args:
        agent_id: Agent identifier
        
    Returns:
        Agent data dictionary or None if not found
    """
    case_data = get_case_data()
    for agent in case_data['agents']:
        if agent['id'] == agent_id:
            return agent
    return None


def get_event_by_id(event_id: str) -> Dict[str, Any]:
    """
    Get event data by ID.
    
    Args:
        event_id: Event identifier
        
    Returns:
        Event data dictionary or None if not found
    """
    case_data = get_case_data()
    for event in case_data['events']:
        if event['id'] == event_id:
            return event
    return None


if __name__ == "__main__":
    # Example usage
    case_data = get_case_data()
    
    print(f"Case: {case_data['case_name']}")
    print(f"Number of agents: {case_data['metadata']['num_agents']}")
    print(f"Number of events: {case_data['metadata']['num_events']}")
    print(f"Number of hyperedges: {case_data['metadata']['num_hyperedges']}")
    print()
    
    print("Agent Centrality Scores:")
    centrality = get_centrality_scores()
    for agent_id, score in sorted(centrality.items(), key=lambda x: x[1], reverse=True):
        agent = get_agent_by_id(agent_id)
        print(f"  {agent_id} ({agent['role']}): {score}")
    print()
    
    print("Attention Weights:")
    weights = get_attention_weights()
    for edge_type, weight in sorted(weights.items(), key=lambda x: x[1], reverse=True):
        print(f"  {edge_type}: {weight}")
