#!/usr/bin/env python3
"""
HypergraphQL Example Usage for Legal Framework

This example demonstrates how to use HypergraphQL to query and analyze
the legal framework in lex/ directory.
"""

import logging
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from models.ggmlex.hypergraphql import (
    HypergraphQLEngine, LegalNode, LegalHyperedge,
    LegalNodeType, LegalRelationType
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def example_basic_queries():
    """Demonstrate basic HypergraphQL queries."""
    logger.info("=" * 60)
    logger.info("Example 1: Basic Queries")
    logger.info("=" * 60)
    
    # Initialize engine
    engine = HypergraphQLEngine()
    
    # Create sample legal nodes
    constitution = LegalNode(
        node_id="statute_constitution",
        node_type=LegalNodeType.STATUTE,
        name="Constitution of South Africa, 1996",
        content="The supreme law of the Republic",
        jurisdiction="za",
        metadata={"year": 1996, "type": "constitution"}
    )
    
    bill_of_rights = LegalNode(
        node_id="section_bill_of_rights",
        node_type=LegalNodeType.SECTION,
        name="Bill of Rights",
        content="Chapter 2 of the Constitution",
        jurisdiction="za",
        properties={"chapter": 2, "parent_statute": "statute_constitution"}
    )
    
    right_to_equality = LegalNode(
        node_id="section_equality",
        node_type=LegalNodeType.SECTION,
        name="Equality",
        content="Section 9: Everyone is equal before the law",
        jurisdiction="za",
        properties={"section": 9, "parent": "section_bill_of_rights"}
    )
    
    case_makwanyane = LegalNode(
        node_id="case_makwanyane",
        node_type=LegalNodeType.CASE,
        name="S v Makwanyane",
        content="Constitutional Court case on death penalty",
        jurisdiction="za",
        properties={
            "court": "Constitutional Court",
            "year": 1995,
            "citation": "1995 (3) SA 391 (CC)"
        }
    )
    
    # Add nodes to engine
    for node in [constitution, bill_of_rights, right_to_equality, case_makwanyane]:
        engine.add_node(node)
    
    # Create relationships
    edge1 = LegalHyperedge(
        edge_id="edge_001",
        relation_type=LegalRelationType.CITES,
        nodes={case_makwanyane.node_id, constitution.node_id},
        metadata={"context": "Constitutional interpretation"}
    )
    
    edge2 = LegalHyperedge(
        edge_id="edge_002",
        relation_type=LegalRelationType.INTERPRETS,
        nodes={case_makwanyane.node_id, bill_of_rights.node_id},
        metadata={"context": "Right to life and human dignity"}
    )
    
    engine.add_edge(edge1)
    engine.add_edge(edge2)
    
    # Query 1: Find all cases
    logger.info("\nQuery 1: Find all cases")
    result = engine.query_nodes(node_type=LegalNodeType.CASE)
    for node in result.nodes:
        logger.info(f"  - {node.name} ({node.properties.get('year', 'N/A')})")
    
    # Query 2: Find neighbors of the constitution
    logger.info("\nQuery 2: Find what cites the Constitution")
    result = engine.query_neighbors(
        constitution.node_id,
        relation_type=LegalRelationType.CITES
    )
    for node in result.nodes:
        logger.info(f"  - {node.name}")
    
    # Query 3: Search by content
    logger.info("\nQuery 3: Search for 'equality'")
    result = engine.query_by_content("equality")
    for node in result.nodes:
        logger.info(f"  - {node.name}: {node.content[:50]}...")
    
    # Get statistics
    stats = engine.get_statistics()
    logger.info(f"\nHypergraph Statistics:")
    logger.info(f"  Total nodes: {stats['num_nodes']}")
    logger.info(f"  Total edges: {stats['num_edges']}")
    logger.info(f"  Node types: {stats['node_types']}")


def example_contract_law():
    """Demonstrate contract law queries."""
    logger.info("\n" + "=" * 60)
    logger.info("Example 2: Contract Law Framework")
    logger.info("=" * 60)
    
    engine = HypergraphQLEngine()
    
    # Contract law concepts
    concepts = [
        ("concept_offer", "Offer", "A proposal to enter into a contract"),
        ("concept_acceptance", "Acceptance", "Agreement to the terms of an offer"),
        ("concept_consideration", "Consideration", "Something of value exchanged"),
        ("concept_capacity", "Legal Capacity", "Ability to enter into a contract"),
        ("concept_consensus", "Consensus ad idem", "Meeting of minds")
    ]
    
    for node_id, name, content in concepts:
        node = LegalNode(
            node_id=node_id,
            node_type=LegalNodeType.CONCEPT,
            name=name,
            content=content,
            jurisdiction="za"
        )
        engine.add_node(node)
    
    # Create relationships between concepts
    relationships = [
        ("concept_offer", "concept_acceptance", "Formation requires both offer and acceptance"),
        ("concept_consensus", "concept_offer", "Consensus includes valid offer"),
        ("concept_consensus", "concept_acceptance", "Consensus includes valid acceptance")
    ]
    
    for idx, (source, target, context) in enumerate(relationships):
        edge = LegalHyperedge(
            edge_id=f"edge_contract_{idx}",
            relation_type=LegalRelationType.SUPPORTS,
            nodes={source, target},
            metadata={"context": context}
        )
        engine.add_edge(edge)
    
    # Query contract formation concepts
    logger.info("\nContract Formation Concepts:")
    result = engine.query_nodes(node_type=LegalNodeType.CONCEPT)
    for node in result.nodes:
        logger.info(f"  - {node.name}: {node.content}")
    
    # Query what supports consensus
    logger.info("\nWhat supports 'Consensus ad idem':")
    result = engine.query_neighbors(
        "concept_consensus",
        relation_type=LegalRelationType.SUPPORTS
    )
    for node in result.nodes:
        logger.info(f"  - {node.name}")


def example_case_law_network():
    """Demonstrate case law precedent network."""
    logger.info("\n" + "=" * 60)
    logger.info("Example 3: Case Law Precedent Network")
    logger.info("=" * 60)
    
    engine = HypergraphQLEngine()
    
    # Create a network of related cases
    cases = [
        ("case_union_govt", "Union Government v Fakir", 1923, "High Court"),
        ("case_regal", "Regal v African Superslate", 1963, "Appellate Division"),
        ("case_santam", "Santam v Lambert", 1983, "High Court"),
        ("case_jockey_club", "Jockey Club v Forbes", 1993, "Appellate Division"),
    ]
    
    for case_id, name, year, court in cases:
        node = LegalNode(
            node_id=case_id,
            node_type=LegalNodeType.CASE,
            name=name,
            content=f"Delict case decided in {year}",
            jurisdiction="za",
            properties={"year": year, "court": court}
        )
        engine.add_node(node)
    
    # Create precedent relationships
    precedent_edges = [
        ("case_regal", "case_union_govt", LegalRelationType.FOLLOWS),
        ("case_santam", "case_regal", LegalRelationType.CITES),
        ("case_jockey_club", "case_regal", LegalRelationType.FOLLOWS),
    ]
    
    for idx, (source, target, relation) in enumerate(precedent_edges):
        edge = LegalHyperedge(
            edge_id=f"edge_precedent_{idx}",
            relation_type=relation,
            nodes={source, target}
        )
        engine.add_edge(edge)
    
    # Query precedent chain
    logger.info("\nPrecedent Chain from Union Government:")
    result = engine.query_neighbors("case_union_govt", max_hops=3)
    for node in result.nodes:
        logger.info(f"  - {node.name} ({node.properties.get('year')})")
    
    # Find path between two cases
    logger.info("\nPath from Union Government to Jockey Club:")
    result = engine.query_path("case_union_govt", "case_jockey_club")
    if result.nodes:
        path = " -> ".join([n.name for n in result.nodes])
        logger.info(f"  {path}")
    else:
        logger.info("  No path found")


def example_legislation_integration():
    """Demonstrate integration with lex/ directory."""
    logger.info("\n" + "=" * 60)
    logger.info("Example 4: Legislation Framework Integration")
    logger.info("=" * 60)
    
    # Initialize engine (will load from lex/ directory)
    engine = HypergraphQLEngine()
    
    # Show loaded legal principles
    logger.info("\nLegal Principles loaded from lex/:")
    result = engine.query_nodes(node_type=LegalNodeType.PRINCIPLE)
    
    if result.nodes:
        logger.info(f"  Found {len(result.nodes)} legal principles")
        for node in result.nodes[:5]:  # Show first 5
            logger.info(f"  - {node.name}")
            logger.info(f"    {node.content[:80]}...")
    else:
        logger.info("  No principles loaded (lex/ directory may be empty)")
    
    # Show statistics
    stats = engine.get_statistics()
    logger.info(f"\nTotal Legal Entities: {stats['num_nodes']}")
    logger.info(f"Node Type Distribution: {stats['node_types']}")


def main():
    """Run all examples."""
    logger.info("HypergraphQL Legal Framework Examples")
    logger.info("=" * 60)
    
    try:
        example_basic_queries()
        example_contract_law()
        example_case_law_network()
        example_legislation_integration()
        
        logger.info("\n" + "=" * 60)
        logger.info("All examples completed successfully!")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"Error running examples: {e}", exc_info=True)


if __name__ == "__main__":
    main()
