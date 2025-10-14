#!/usr/bin/env python3
"""
GGMLEX Integration Example

This example demonstrates how GGMLEX integrates with the existing
AnalytiCase framework, combining HypergraphQL with other models.
"""

import logging
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from models.ggmlex import (
    HypergraphQLEngine, LegalNode, LegalHyperedge,
    LegalNodeType, LegalRelationType,
    LegalTransformer, LegalLLM
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def example_legal_framework_analysis():
    """
    Demonstrate analyzing the legal framework with GGMLEX.
    """
    logger.info("=" * 70)
    logger.info("GGMLEX Integration: Legal Framework Analysis")
    logger.info("=" * 70)
    
    # Initialize HypergraphQL engine
    logger.info("\n1. Initializing HypergraphQL Engine...")
    engine = HypergraphQLEngine()
    
    # Get statistics
    stats = engine.get_statistics()
    logger.info(f"   Loaded {stats['num_nodes']} legal entities from lex/")
    logger.info(f"   Node types: {stats['node_types']}")
    
    # Query legal principles
    logger.info("\n2. Querying Legal Principles...")
    result = engine.query_nodes(node_type=LegalNodeType.PRINCIPLE)
    logger.info(f"   Found {len(result)} legal principles")
    
    if result.nodes:
        logger.info("\n   Sample principles:")
        for node in result.nodes[:5]:
            logger.info(f"   - {node.name}")
    
    # Search for contract-related principles
    logger.info("\n3. Searching for Contract Law Principles...")
    result = engine.query_by_content("contract")
    logger.info(f"   Found {len(result)} nodes mentioning 'contract'")
    
    if result.nodes:
        logger.info("\n   Contract-related principles:")
        for node in result.nodes[:3]:
            logger.info(f"   - {node.name}: {node.content[:60]}...")


def example_document_analysis_integration():
    """
    Demonstrate using GGMLEX transformers with legal documents.
    """
    logger.info("\n" + "=" * 70)
    logger.info("GGMLEX Integration: Document Analysis")
    logger.info("=" * 70)
    
    # Sample legal text
    legal_text = """
    In the matter of Smith v. Jones, the High Court considered whether
    the defendant breached the contract by failing to deliver goods on
    the agreed date. The court held that Section 9 of the Constitution
    guarantees equality before the law, and that the plaintiff was
    entitled to damages for the breach.
    """
    
    logger.info("\n1. Analyzing with LegalTransformer...")
    transformer = LegalTransformer()
    analysis = transformer.analyze_legal_text(legal_text)
    
    logger.info(f"   Text length: {analysis['text_length']} characters")
    logger.info(f"   Number of tokens: {analysis['num_tokens']}")
    logger.info(f"   Embedding dimension: {analysis['embedding_dim']}")
    logger.info(f"   Model: {analysis['model_config']['num_layers']} layers, "
                f"{analysis['model_config']['num_heads']} heads")
    
    transformer.cleanup()
    
    logger.info("\n2. Analyzing with LegalLLM...")
    llm = LegalLLM()
    llm_analysis = llm.analyze_case(legal_text)
    
    logger.info(f"   Document type: {llm_analysis['document_type']}")
    logger.info(f"   Number of tokens: {llm_analysis['num_tokens']}")
    logger.info(f"   Summary: {llm_analysis['summary']}")
    
    llm.cleanup()


def example_case_network_building():
    """
    Demonstrate building a case law network with HypergraphQL.
    """
    logger.info("\n" + "=" * 70)
    logger.info("GGMLEX Integration: Building Case Law Network")
    logger.info("=" * 70)
    
    # Initialize engine
    engine = HypergraphQLEngine()
    
    # Create case nodes representing South African case law
    logger.info("\n1. Creating Case Law Nodes...")
    
    cases = [
        {
            "id": "case_makwanyane",
            "name": "S v Makwanyane",
            "year": 1995,
            "court": "Constitutional Court",
            "citation": "1995 (3) SA 391 (CC)",
            "content": "Landmark case abolishing the death penalty"
        },
        {
            "id": "case_carmichele",
            "name": "Carmichele v Minister of Safety and Security",
            "year": 2001,
            "court": "Constitutional Court",
            "citation": "2001 (4) SA 938 (CC)",
            "content": "State's duty to protect against gender-based violence"
        },
        {
            "id": "case_grootboom",
            "name": "Government of RSA v Grootboom",
            "year": 2000,
            "court": "Constitutional Court",
            "citation": "2001 (1) SA 46 (CC)",
            "content": "Right to adequate housing"
        }
    ]
    
    for case_data in cases:
        node = LegalNode(
            node_id=case_data["id"],
            node_type=LegalNodeType.CASE,
            name=case_data["name"],
            content=case_data["content"],
            jurisdiction="za",
            properties={
                "year": case_data["year"],
                "court": case_data["court"],
                "citation": case_data["citation"]
            }
        )
        engine.add_node(node)
        logger.info(f"   Added: {case_data['name']} ({case_data['year']})")
    
    # Create relationships
    logger.info("\n2. Creating Case Relationships...")
    
    # Constitution node
    constitution = LegalNode(
        node_id="statute_constitution",
        node_type=LegalNodeType.STATUTE,
        name="Constitution of South Africa, 1996",
        content="The supreme law of the Republic",
        jurisdiction="za"
    )
    engine.add_node(constitution)
    
    # Link cases to constitution
    for case_id in ["case_makwanyane", "case_carmichele", "case_grootboom"]:
        edge = LegalHyperedge(
            edge_id=f"edge_{case_id}_constitution",
            relation_type=LegalRelationType.INTERPRETS,
            nodes={case_id, "statute_constitution"}
        )
        engine.add_edge(edge)
    
    logger.info("   Created constitutional interpretation links")
    
    # Query the network
    logger.info("\n3. Querying the Case Law Network...")
    
    # Find cases interpreting the constitution
    result = engine.query_neighbors(
        "statute_constitution",
        relation_type=LegalRelationType.INTERPRETS
    )
    
    logger.info(f"   Cases interpreting the Constitution:")
    for node in result.nodes:
        year = node.properties.get("year", "N/A")
        citation = node.properties.get("citation", "N/A")
        logger.info(f"   - {node.name} ({year})")
        logger.info(f"     {citation}")
    
    # Get updated statistics
    stats = engine.get_statistics()
    logger.info(f"\n   Network statistics:")
    logger.info(f"   - Total nodes: {stats['num_nodes']}")
    logger.info(f"   - Total edges: {stats['num_edges']}")
    logger.info(f"   - Node types: {stats['node_types']}")


def main():
    """
    Run all integration examples.
    """
    logger.info("GGMLEX Integration Examples")
    logger.info("=" * 70)
    logger.info("Demonstrating integration with AnalytiCase framework")
    logger.info("=" * 70)
    
    try:
        # Run examples
        example_legal_framework_analysis()
        example_document_analysis_integration()
        example_case_network_building()
        
        logger.info("\n" + "=" * 70)
        logger.info("All integration examples completed successfully!")
        logger.info("=" * 70)
        
        logger.info("\nNext steps:")
        logger.info("  1. Explore the lex/ directory for more legal frameworks")
        logger.info("  2. Run 'python models/ggmlex/hypergraphql/hypergraphql_example.py'")
        logger.info("  3. Run 'python -m pytest models/ggmlex/test_ggmlex.py -v'")
        logger.info("  4. See models/ggmlex/README.md for detailed documentation")
        
    except Exception as e:
        logger.error(f"Error running integration examples: {e}", exc_info=True)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
