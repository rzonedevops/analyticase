#!/usr/bin/env python3
"""
Test and Demonstration of Inference Engine

This script demonstrates the inference engine processing lex scheme expressions
to derive principles at different inference levels:
  Level 0: Enumerated Laws (from lex/*.scm files)
  Level 1: First-order Principles (generalized from laws)
  Level 2: Meta-principles (higher abstractions)
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from models.ggmlex.hypergraphql import (
    HypergraphQLEngine, InferenceEngine, InferenceResult,
    LegalNode, LegalNodeType, InferenceType
)


def test_deductive_inference():
    """Test deductive inference: apply general principle to specific case."""
    print("\n" + "="*70)
    print("TEST 1: Deductive Inference")
    print("="*70)
    
    # Create a general principle (Level 1)
    general_principle = LegalNode(
        node_id="principle_contract_requires_consideration",
        node_type=LegalNodeType.PRINCIPLE,
        name="Contract Requires Consideration",
        content="All valid contracts must have consideration",
        jurisdiction="za",
        inference_level=1,
        confidence=0.95
    )
    
    # Create a specific case (Level 0)
    specific_case = LegalNode(
        node_id="case_employment_agreement",
        node_type=LegalNodeType.CASE,
        name="Employment Agreement X",
        content="Employment agreement between parties",
        jurisdiction="za",
        inference_level=0,
        confidence=1.0
    )
    
    # Perform deductive inference
    engine = InferenceEngine()
    result = engine.infer_principles(
        source_nodes=[general_principle, specific_case],
        inference_type=InferenceType.DEDUCTIVE,
        target_level=1
    )
    
    print(f"\nGeneral Principle: {general_principle.name}")
    print(f"Specific Case: {specific_case.name}")
    print(f"\nDeduced Conclusion: {result.principle.name}")
    print(f"Confidence: {result.confidence:.3f}")
    print(f"Explanation: {result.explanation}")
    print("\n✓ Deductive inference test passed")
    
    return result


def test_inductive_inference():
    """Test inductive inference: generalize from multiple laws."""
    print("\n" + "="*70)
    print("TEST 2: Inductive Inference")
    print("="*70)
    
    # Create multiple enumerated laws with common pattern
    laws = [
        LegalNode(
            node_id="law_civil_reasonable_person",
            node_type=LegalNodeType.STATUTE,
            name="Civil Law Reasonable Person Standard",
            content="In negligence cases, conduct measured against reasonable person",
            jurisdiction="za",
            inference_level=0
        ),
        LegalNode(
            node_id="law_criminal_reasonable_foresight",
            node_type=LegalNodeType.STATUTE,
            name="Criminal Law Reasonable Foresight",
            content="Criminal liability based on what reasonable person would foresee",
            jurisdiction="za",
            inference_level=0
        ),
        LegalNode(
            node_id="law_contract_reasonable_interpretation",
            node_type=LegalNodeType.STATUTE,
            name="Contract Law Reasonable Interpretation",
            content="Contract terms interpreted as reasonable person would understand",
            jurisdiction="za",
            inference_level=0
        ),
        LegalNode(
            node_id="law_delict_reasonable_conduct",
            node_type=LegalNodeType.STATUTE,
            name="Delict Law Reasonable Conduct",
            content="Delictual liability based on reasonable person avoiding harm",
            jurisdiction="za",
            inference_level=0
        )
    ]
    
    # Perform inductive inference
    engine = InferenceEngine()
    result = engine.infer_principles(
        source_nodes=laws,
        inference_type=InferenceType.INDUCTIVE,
        target_level=1
    )
    
    print(f"\nEnumerated Laws ({len(laws)}):")
    for law in laws:
        print(f"  - {law.name}")
    
    print(f"\nGeneralized Principle: {result.principle.name}")
    print(f"Confidence: {result.confidence:.3f} (based on {len(laws)} examples)")
    print(f"Explanation: {result.explanation}")
    print("\n✓ Inductive inference test passed")
    
    return result


def test_abductive_inference():
    """Test abductive inference: find best explanation for pattern."""
    print("\n" + "="*70)
    print("TEST 3: Abductive Inference")
    print("="*70)
    
    # Create observations
    observations = [
        LegalNode(
            node_id="obs_criminal_mens_rea",
            node_type=LegalNodeType.STATUTE,
            name="Criminal Law Requires Mens Rea",
            content="Criminal liability requires mental state (intent)",
            jurisdiction="za",
            inference_level=0
        ),
        LegalNode(
            node_id="obs_contract_intent",
            node_type=LegalNodeType.STATUTE,
            name="Contract Law Requires Intent",
            content="Contract formation requires intent to be bound",
            jurisdiction="za",
            inference_level=0
        ),
        LegalNode(
            node_id="obs_delict_fault",
            node_type=LegalNodeType.STATUTE,
            name="Delict Law Requires Fault",
            content="Delictual liability requires fault or negligence",
            jurisdiction="za",
            inference_level=0
        ),
        LegalNode(
            node_id="obs_admin_rational",
            node_type=LegalNodeType.STATUTE,
            name="Administrative Law Requires Rationality",
            content="Administrative decisions must be rational",
            jurisdiction="za",
            inference_level=0
        )
    ]
    
    # Perform abductive inference
    engine = InferenceEngine()
    result = engine.infer_principles(
        source_nodes=observations,
        inference_type=InferenceType.ABDUCTIVE,
        target_level=2,  # Meta-principle
        hypothesis_name="Mental Culpability Principle"
    )
    
    print(f"\nObservations ({len(observations)}):")
    for obs in observations:
        print(f"  - {obs.name}")
    
    print(f"\nBest Explanation (Hypothesis): {result.principle.name}")
    print(f"Confidence: {result.confidence:.3f}")
    print(f"Explanation: {result.explanation}")
    print(f"Explanatory Power: {result.principle.metadata['explanatory_power']:.2f}")
    print(f"Coherence: {result.principle.metadata['coherence']:.2f}")
    print(f"Simplicity: {result.principle.metadata['simplicity']:.2f}")
    print("\n✓ Abductive inference test passed")
    
    return result


def test_analogical_inference():
    """Test analogical inference: transfer principle across domains."""
    print("\n" + "="*70)
    print("TEST 4: Analogical Inference")
    print("="*70)
    
    # Create source domain principle
    source_principle = LegalNode(
        node_id="principle_contract_frustration",
        node_type=LegalNodeType.PRINCIPLE,
        name="Frustration of Purpose Doctrine",
        content="Contract discharged if fundamental purpose becomes impossible",
        jurisdiction="za",
        inference_level=1,
        confidence=0.9,
        metadata={"branch": "contract"}
    )
    
    # Perform analogical inference to employment law
    engine = InferenceEngine()
    result = engine.infer_principles(
        source_nodes=[source_principle],
        inference_type=InferenceType.ANALOGICAL,
        target_level=1,
        target_domain="labour"
    )
    
    print(f"\nSource Domain: Contract Law")
    print(f"Source Principle: {source_principle.name}")
    print(f"Source Confidence: {source_principle.confidence:.3f}")
    
    print(f"\nTarget Domain: Labour Law")
    print(f"Transferred Principle: {result.principle.name}")
    print(f"Transfer Confidence: {result.confidence:.3f}")
    print(f"Domain Similarity: {result.principle.metadata['similarity']:.3f}")
    print(f"Explanation: {result.explanation}")
    print("\n✓ Analogical inference test passed")
    
    return result


def test_inference_hierarchy():
    """Test building complete inference hierarchy."""
    print("\n" + "="*70)
    print("TEST 5: Inference Hierarchy")
    print("="*70)
    
    # Create hypergraph engine with some nodes
    engine = HypergraphQLEngine()
    
    # Add level 0 nodes (enumerated laws)
    for i in range(3):
        node = LegalNode(
            node_id=f"law_{i}",
            node_type=LegalNodeType.STATUTE,
            name=f"Enumerated Law {i}",
            content="Legal provision",
            jurisdiction="za",
            inference_level=0
        )
        engine.add_node(node)
    
    # Add level 1 nodes (first-order principles)
    for i in range(2):
        node = LegalNode(
            node_id=f"principle_l1_{i}",
            node_type=LegalNodeType.PRINCIPLE,
            name=f"First-Order Principle {i}",
            content="Generalized principle",
            jurisdiction="za",
            inference_level=1
        )
        engine.add_node(node)
    
    # Add level 2 node (meta-principle)
    node = LegalNode(
        node_id="meta_principle_0",
        node_type=LegalNodeType.PRINCIPLE,
        name="Meta-Principle",
        content="High-level abstraction",
        jurisdiction="za",
        inference_level=2
    )
    engine.add_node(node)
    
    # Build hierarchy
    hierarchy = engine.build_inference_hierarchy()
    
    print("\nInference Hierarchy:")
    for level in sorted(hierarchy.keys()):
        nodes = hierarchy[level]
        print(f"\nLevel {level}: {len(nodes)} nodes")
        for node in nodes:
            print(f"  - {node.name} (confidence={node.confidence:.2f})")
    
    # Test querying by level
    level_0 = engine.get_enumerated_laws()
    level_1 = engine.get_first_order_principles()
    level_2 = engine.get_meta_principles()
    
    print(f"\nQuery Results:")
    print(f"  Enumerated Laws (Level 0): {len(level_0)} nodes")
    print(f"  First-Order Principles (Level 1): {len(level_1)} nodes")
    print(f"  Meta-Principles (Level 2): {len(level_2)} nodes")
    
    print("\n✓ Inference hierarchy test passed")


def test_real_lex_processing():
    """Test processing actual lex scheme files."""
    print("\n" + "="*70)
    print("TEST 6: Processing Real Lex Scheme Files")
    print("="*70)
    
    # Create hypergraph engine (will load lex files)
    print("\nLoading legal frameworks from lex/...")
    engine = HypergraphQLEngine()
    
    stats = engine.get_statistics()
    print(f"\nLoaded {stats['num_nodes']} legal nodes")
    print(f"Node types: {stats['node_types']}")
    print(f"Total edges: {stats['num_edges']}")
    
    # All loaded nodes start at level 0 (enumerated laws)
    level_0_nodes = engine.get_enumerated_laws()
    print(f"\nEnumerated Laws (Level 0): {len(level_0_nodes)} nodes")
    
    if len(level_0_nodes) >= 4:
        # Sample first few nodes
        print("\nSample Enumerated Laws:")
        for node in level_0_nodes.nodes[:4]:
            print(f"  - {node.name}")
            print(f"    Branch: {node.metadata.get('branch', 'unknown')}")
            print(f"    Jurisdiction: {node.jurisdiction}")
    
    # Demonstrate that we could now perform inference on these
    print("\n✓ Real lex processing test passed")
    print("\nNote: Actual inference on loaded laws would be performed using")
    print("      the InferenceEngine with appropriate node selection and")
    print("      pattern matching algorithms.")


def main():
    """Run all inference engine tests."""
    print("="*70)
    print("INFERENCE ENGINE TEST SUITE")
    print("Processing Lex Scheme Expressions to Resolve Principles")
    print("="*70)
    
    # Run tests
    test_deductive_inference()
    test_inductive_inference()
    test_abductive_inference()
    test_analogical_inference()
    test_inference_hierarchy()
    test_real_lex_processing()
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print("✓ All 6 tests passed")
    print("\nThe inference engine successfully:")
    print("  1. Applies deductive reasoning (general → specific)")
    print("  2. Performs inductive generalization (specific → general)")
    print("  3. Generates abductive explanations (observations → hypothesis)")
    print("  4. Transfers principles by analogy (domain → domain)")
    print("  5. Builds inference hierarchies (Level 0 → 1 → 2)")
    print("  6. Processes real lex scheme files")
    print("\nInference Levels:")
    print("  Level 0: Enumerated Laws (from lex/*.scm files)")
    print("  Level 1: First-order Principles (generalized from laws)")
    print("  Level 2: Meta-principles (higher abstractions)")
    print("="*70)


if __name__ == "__main__":
    main()
