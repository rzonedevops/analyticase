#!/usr/bin/env python3
"""
Example: Using Inference Engine with Lex Framework

This example demonstrates how to use the inference engine to process
lex scheme expressions and derive legal principles at different levels.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from models.ggmlex.hypergraphql import (
    HypergraphQLEngine, InferenceEngine, InferenceResult,
    LegalNode, LegalNodeType, InferenceType, LegalRelationType
)


def example_1_inductive_generalization():
    """
    Example 1: Inductive Generalization
    
    Generalize from multiple civil law concepts to derive a first-order principle.
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: Inductive Generalization from Civil Law Concepts")
    print("="*70)
    
    # Load legal framework (this will load all lex/*.scm files)
    print("\nLoading legal framework...")
    engine = HypergraphQLEngine()
    
    # Get enumerated laws from civil law
    all_laws = engine.get_enumerated_laws()
    print(f"Found {len(all_laws)} enumerated laws total")
    
    # Find laws related to "reasonable person" standard
    reasonable_person_laws = []
    for node in all_laws.nodes:
        if "reasonable" in node.name.lower() or "reasonable" in node.content.lower():
            reasonable_person_laws.append(node)
            if len(reasonable_person_laws) >= 5:  # Limit to 5 for example
                break
    
    if len(reasonable_person_laws) >= 2:
        print(f"\nFound {len(reasonable_person_laws)} laws with 'reasonable person' concept:")
        for law in reasonable_person_laws:
            print(f"  - {law.name}")
        
        # Perform inductive inference
        inf_engine = InferenceEngine(engine)
        result = inf_engine.infer_principles(
            source_nodes=reasonable_person_laws,
            inference_type=InferenceType.INDUCTIVE,
            target_level=1,
            pattern_name="Reasonable Person Standard Principle"
        )
        
        print(f"\n✓ Inferred Principle (Level 1):")
        print(f"  Name: {result.principle.name}")
        print(f"  Confidence: {result.confidence:.3f}")
        print(f"  Based on: {len(reasonable_person_laws)} enumerated laws")
        print(f"  Inference Type: {result.inference_type.value}")
        
        # Add the inferred principle to the graph
        engine.add_node(result.principle)
        for edge in result.supporting_edges:
            engine.add_edge(edge)
        
        print(f"\n✓ Added principle to hypergraph")
    else:
        print("\n⚠ Not enough matching laws found for demonstration")


def example_2_abductive_explanation():
    """
    Example 2: Abductive Explanation
    
    Find the best explanation for why multiple legal branches require intent.
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: Abductive Explanation - Mental Culpability")
    print("="*70)
    
    # Create sample observations from different legal branches
    observations = [
        LegalNode(
            node_id="obs_criminal_intent",
            node_type=LegalNodeType.STATUTE,
            name="Criminal Law - Mens Rea Requirement",
            content="Criminal liability requires mens rea (guilty mind/intent)",
            jurisdiction="za",
            inference_level=0,
            metadata={"branch": "criminal"}
        ),
        LegalNode(
            node_id="obs_contract_intent",
            node_type=LegalNodeType.STATUTE,
            name="Contract Law - Intent to Contract",
            content="Contract formation requires intent to create legal relations",
            jurisdiction="za",
            inference_level=0,
            metadata={"branch": "civil"}
        ),
        LegalNode(
            node_id="obs_delict_fault",
            node_type=LegalNodeType.STATUTE,
            name="Delict Law - Fault Requirement",
            content="Delictual liability requires fault (intentional or negligent conduct)",
            jurisdiction="za",
            inference_level=0,
            metadata={"branch": "civil"}
        ),
        LegalNode(
            node_id="obs_admin_rationality",
            node_type=LegalNodeType.STATUTE,
            name="Administrative Law - Rationality",
            content="Administrative decisions must be rational and made with proper purpose",
            jurisdiction="za",
            inference_level=0,
            metadata={"branch": "administrative"}
        )
    ]
    
    print("\nObservations across legal branches:")
    for obs in observations:
        print(f"  - {obs.name} ({obs.metadata['branch']})")
    
    # Perform abductive inference to find best explanation
    inf_engine = InferenceEngine()
    result = inf_engine.infer_principles(
        source_nodes=observations,
        inference_type=InferenceType.ABDUCTIVE,
        target_level=2,  # Meta-principle level
        hypothesis_name="Mental Culpability Meta-Principle"
    )
    
    print(f"\n✓ Best Explanation (Meta-Principle - Level 2):")
    print(f"  Name: {result.principle.name}")
    print(f"  Content: {result.principle.content}")
    print(f"  Confidence: {result.confidence:.3f}")
    print(f"  Explanatory Power: {result.principle.metadata['explanatory_power']:.2f}")
    print(f"  Coherence: {result.principle.metadata['coherence']:.2f}")
    print(f"  Simplicity: {result.principle.metadata['simplicity']:.2f}")


def example_3_analogical_transfer():
    """
    Example 3: Analogical Transfer
    
    Transfer a principle from contract law to employment law by analogy.
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Analogical Transfer - Contract to Employment Law")
    print("="*70)
    
    # Create a principle from contract law
    contract_principle = LegalNode(
        node_id="principle_contract_frustration",
        node_type=LegalNodeType.PRINCIPLE,
        name="Doctrine of Frustration",
        content="A contract is discharged when its fundamental purpose becomes impossible to achieve due to unforeseen circumstances",
        jurisdiction="za",
        inference_level=1,
        confidence=0.92,
        metadata={"branch": "contract", "source": "Contract Law"}
    )
    
    print(f"\nSource Principle (Contract Law):")
    print(f"  Name: {contract_principle.name}")
    print(f"  Confidence: {contract_principle.confidence:.3f}")
    
    # Transfer to employment law by analogy
    inf_engine = InferenceEngine()
    result = inf_engine.infer_principles(
        source_nodes=[contract_principle],
        inference_type=InferenceType.ANALOGICAL,
        target_level=1,
        target_domain="labour"
    )
    
    print(f"\n✓ Transferred Principle (Labour/Employment Law):")
    print(f"  Name: {result.principle.name}")
    print(f"  Content: {result.principle.content}")
    print(f"  Confidence: {result.confidence:.3f}")
    print(f"  Domain Similarity: {result.principle.metadata['similarity']:.2f}")
    print(f"\n  Interpretation for Employment:")
    print(f"    An employment relationship may be terminated if the fundamental")
    print(f"    purpose of employment becomes impossible to achieve due to")
    print(f"    unforeseen circumstances (e.g., business closure, regulatory change)")


def example_4_build_hierarchy():
    """
    Example 4: Build Complete Inference Hierarchy
    
    Demonstrate building a complete hierarchy from Level 0 to Level 2.
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: Building Complete Inference Hierarchy")
    print("="*70)
    
    # Create a mini hypergraph with principles at different levels
    engine = HypergraphQLEngine(lex_path="/nonexistent")  # Don't load real files
    
    # Level 0: Enumerated laws
    laws = [
        ("contract_offer", "Contract requires offer"),
        ("contract_acceptance", "Contract requires acceptance"),
        ("sale_offer", "Sale requires offer"),
        ("lease_acceptance", "Lease requires acceptance"),
    ]
    
    for law_id, law_name in laws:
        node = LegalNode(
            node_id=f"law_{law_id}",
            node_type=LegalNodeType.STATUTE,
            name=law_name,
            content=f"{law_name} - enumerated law",
            jurisdiction="za",
            inference_level=0
        )
        engine.add_node(node)
    
    print(f"\nLevel 0: Enumerated Laws ({len(laws)} laws)")
    for _, name in laws:
        print(f"  - {name}")
    
    # Level 1: First-order principle (inferred from laws)
    principle_l1 = LegalNode(
        node_id="principle_contractual_agreement",
        node_type=LegalNodeType.PRINCIPLE,
        name="Contractual Agreement Principle",
        content="All contractual agreements require both offer and acceptance",
        jurisdiction="za",
        inference_level=1,
        inference_type=InferenceType.INDUCTIVE,
        confidence=0.85
    )
    engine.add_node(principle_l1)
    
    print(f"\nLevel 1: First-Order Principles (1 principle)")
    print(f"  - {principle_l1.name} (confidence: {principle_l1.confidence:.2f})")
    
    # Level 2: Meta-principle (inferred from principles)
    meta_principle = LegalNode(
        node_id="meta_mutual_assent",
        node_type=LegalNodeType.PRINCIPLE,
        name="Meta-Principle of Mutual Assent",
        content="Legal relationships require mutual assent of parties",
        jurisdiction="za",
        inference_level=2,
        inference_type=InferenceType.ABDUCTIVE,
        confidence=0.72
    )
    engine.add_node(meta_principle)
    
    print(f"\nLevel 2: Meta-Principles (1 meta-principle)")
    print(f"  - {meta_principle.name} (confidence: {meta_principle.confidence:.2f})")
    
    # Build and display hierarchy
    hierarchy = engine.build_inference_hierarchy()
    
    print(f"\n✓ Complete Inference Hierarchy:")
    for level in sorted(hierarchy.keys()):
        nodes = hierarchy[level]
        level_name = {0: "Enumerated Laws", 1: "First-Order Principles", 2: "Meta-Principles"}.get(level, f"Level {level}")
        print(f"\n  {level_name}: {len(nodes)} node(s)")
        
        # Show average confidence at this level
        if nodes:
            avg_conf = sum(n.confidence for n in nodes) / len(nodes)
            print(f"    Average confidence: {avg_conf:.3f}")


def main():
    """Run all examples."""
    print("="*70)
    print("INFERENCE ENGINE EXAMPLES")
    print("Processing Lex Scheme Expressions to Resolve Principles")
    print("="*70)
    
    # Run examples
    # Note: Example 1 loads real lex files and may take time
    # Uncomment to run:
    # example_1_inductive_generalization()
    
    example_2_abductive_explanation()
    example_3_analogical_transfer()
    example_4_build_hierarchy()
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print("\nThe inference engine provides:")
    print("  1. Deductive Inference: Apply principles to specific cases")
    print("  2. Inductive Inference: Generalize from laws to principles")
    print("  3. Abductive Inference: Find best explanations for patterns")
    print("  4. Analogical Inference: Transfer principles across domains")
    print("\nInference Levels:")
    print("  Level 0: Enumerated Laws (from lex/*.scm files)")
    print("  Level 1: First-order Principles (generalized from Level 0)")
    print("  Level 2: Meta-principles (higher abstractions from Level 1)")
    print("\nConfidence Ranges:")
    print("  Deductive: 0.9-1.0 (high certainty)")
    print("  Inductive: 0.7-0.95 (increases with examples)")
    print("  Abductive: 0.5-0.8 (medium, explanatory)")
    print("  Analogical: 0.6-0.9 (varies with similarity)")
    print("="*70)


if __name__ == "__main__":
    main()
