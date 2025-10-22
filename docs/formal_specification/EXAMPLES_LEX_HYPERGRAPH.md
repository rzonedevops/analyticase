# Lex Hypergraph and Inference Models: Practical Examples

## Overview

This document provides practical examples demonstrating how to use the Z++ formal specification for the lex hypergraph and the four primary inference models.

## Table of Contents

1. [Example 1: Loading Legal Framework into Hypergraph](#example-1-loading-legal-framework-into-hypergraph)
2. [Example 2: Deductive Inference](#example-2-deductive-inference)
3. [Example 3: Inductive Inference](#example-3-inductive-inference)
4. [Example 4: Abductive Inference](#example-4-abductive-inference)
5. [Example 5: Analogical Inference](#example-5-analogical-inference)
6. [Example 6: Building Inference Hierarchy](#example-6-building-inference-hierarchy)
7. [Example 7: Querying the Hypergraph](#example-7-querying-the-hypergraph)

## Example 1: Loading Legal Framework into Hypergraph

### Scenario

Load South African civil law framework from the `lex/civ/za/` directory into a lex hypergraph.

### Input

```scheme
;; From lex/civ/za/south_african_civil_law.scm

;; Essential Elements of a Contract
(define contract-valid? (lambda (contract)
  (and (offer-exists? contract)
       (acceptance-exists? contract)
       (consideration-exists? contract)
       (intention-to-create-legal-relations? contract)
       (capacity-of-parties? contract)
       (legality-of-object? contract))))

(define offer-exists? (lambda (contract)
  (has-attribute contract 'offer)))

(define acceptance-exists? (lambda (contract)
  (has-attribute contract 'acceptance)))
```

### Operation Sequence (per Z++ specification)

```
1. Create LegalNode for contract-valid?
   InitializeLegalNode(
     id: "sa_civil_contract-valid",
     type: principle,
     name: "Contract Valid",
     content: "(define contract-valid? ...)",
     jurisdiction: "za",
     branch: civil
   )
   
   Result:
     - nodeId = "sa_civil_contract-valid"
     - inferenceLevel = 0  (enumerated law)
     - Added to enumeratedNodes
     - Added to principleNodes (type = principle)

2. Create LegalNode for offer-exists?
   InitializeLegalNode(
     id: "sa_civil_offer-exists",
     type: principle,
     name: "Offer Exists",
     content: "(define offer-exists? ...)",
     jurisdiction: "za",
     branch: civil
   )

3. Create dependency edge (contract-valid depends on offer-exists)
   CreateLegalEdge(
     id: "civil_rel_contract-valid_to_offer-exists",
     type: depends_on,
     connectedNodes: {"sa_civil_contract-valid", "sa_civil_offer-exists"},
     edgeWeight: 1.0
   )
   
   Result:
     - confidence = 1.0 (explicit dependency)
     - inferenceType = null (not inferred)
     - Not added to inferredEdges
```

### Python Implementation

```python
from models.ggmlex.hypergraphql import HypergraphQLEngine

# Load the lex framework
engine = HypergraphQLEngine()

# Query loaded nodes
contract_nodes = engine.query_by_content("contract")
print(f"Loaded {len(contract_nodes)} contract-related principles")

# Get dependencies
contract_valid = next(n for n in contract_nodes if "contract-valid" in n.node_id)
dependencies = engine.get_dependencies(contract_valid.node_id)
print(f"Contract validity depends on {len(dependencies)} other principles")
```

### Output

```
Loaded 11 contract-related principles
Contract validity depends on 6 other principles:
  - offer-exists?
  - acceptance-exists?
  - consideration-exists?
  - intention-to-create-legal-relations?
  - capacity-of-parties?
  - legality-of-object?
```

## Example 2: Deductive Inference

### Scenario

Apply general contract formation principle to a specific employment agreement.

### Formal Specification (from LEX_HYPERGRAPH_SPEC.md)

```
DeductiveInference(premises: set of LNODEID, conclusion: LNODEID) 
  returns (valid: boolean, confidence: real)

  Pre-condition:
    - premises ⊆ domain(nodes)
    - conclusion in domain(nodes)
  
  Post-condition:
    - If valid = true:
        - New edge created with relationType = infers_from
        - Edge marked as inferenceType = deductive
        - confidence in range [0.8, 1.0]
```

### Application

```
Premise 1 (General Principle):
  Node: "za_general_contract_formation_principle"
  Content: "All contracts require mutual agreement through offer and acceptance"
  InferenceLevel: 1 (first-order principle)
  Confidence: 0.9

Premise 2 (Specific Case):
  Node: "employment_agreement_X"
  Content: "Employment agreement between employer and employee"
  Type: contract
  InferenceLevel: 0 (specific instance)
  Confidence: 1.0

Deductive Rule: Modus Ponens
  If P → Q (all contracts require offer + acceptance)
  And P (employment agreement is a contract)
  Then Q (employment agreement requires offer + acceptance)

Conclusion:
  Node: "employment_agreement_X_requires_offer_acceptance"
  Content: "Employment agreement X must have offer and acceptance"
  InferenceLevel: 1 (derived from level 1 principle)
  
Edge Creation:
  CreateLegalEdge(
    id: "deductive_employment_contract_formation",
    type: infers_from,
    nodes: {"za_general_contract_formation_principle", 
            "employment_agreement_X",
            "employment_agreement_X_requires_offer_acceptance"},
    weight: 1.0
  )
  
  MarkAsInferred(
    infType: deductive,
    conf: min(0.9, 1.0) = 0.9
  )
  
Result:
  - Conclusion derived with 0.9 confidence
  - Edge added to inferredEdges
  - High confidence due to deductive reasoning
```

### Python Implementation

```python
def apply_deductive_inference(general_principle, specific_case):
    """Apply deductive reasoning."""
    
    # Check if principle applies to case
    if not is_instance_of(specific_case, general_principle.domain):
        return None, 0.0
    
    # Create conclusion node
    conclusion = create_conclusion_node(
        principle=general_principle,
        case=specific_case,
        inference_level=general_principle.inference_level
    )
    
    # Calculate confidence (minimum of premises)
    confidence = min(
        general_principle.confidence,
        specific_case.confidence
    )
    
    # Create inference edge
    edge = create_inference_edge(
        sources=[general_principle, specific_case],
        target=conclusion,
        inference_type="deductive",
        confidence=confidence
    )
    
    return conclusion, confidence

# Apply to employment agreement
general_principle = get_node("za_general_contract_formation_principle")
employment_case = get_node("employment_agreement_X")

conclusion, confidence = apply_deductive_inference(general_principle, employment_case)
print(f"Conclusion: {conclusion.content}")
print(f"Confidence: {confidence:.2f}")
```

## Example 3: Inductive Inference

### Scenario

Generalize from multiple contract laws to form "Contract Formation Principle".

### Input Data

```
Enumerated Laws (Level 0):
1. sa_civil_contract-valid? - "Contracts require offer + acceptance + consideration"
2. sa_commercial_sale-agreement? - "Sale requires offer + acceptance"
3. sa_construction_contract-valid? - "Construction contracts require offer + acceptance"
4. sa_labour_employment-contract? - "Employment requires offer + acceptance"
```

### Formal Specification

```
InductiveInference(examples: set of LNODEID, generalPrinciple: LNODEID,
                   pattern: string) 
  returns (valid: boolean, confidence: real)

  Pre-condition:
    - examples ⊆ enumeratedNodes
    - size(examples) >= 2
    - All nodes in examples share common pattern
  
  Post-condition:
    - New edge with relationType = generalizes
    - Edge marked as inferenceType = inductive
    - confidence = min(0.95, (size(examples) / (size(examples) + 1)))
```

### Application

```
Step 1: Identify Pattern
  Pattern: "All contract types require offer and acceptance"
  Examples: 4 contract laws
  Pattern strength: Strong (appears in all examples)

Step 2: Create General Principle
  InitializeLegalNode(
    id: "za_general_contract_formation_principle",
    type: principle,
    name: "Contract Formation Principle",
    content: "All contracts require mutual agreement through offer and acceptance",
    jurisdiction: "za",
    branch: civil
  )
  
  SetInferenceLevel(level: 1)  // First-order principle from level 0 laws

Step 3: Calculate Confidence
  n = 4 (number of examples)
  confidence = min(0.95, 4 / (4 + 1))
            = min(0.95, 0.8)
            = 0.8

Step 4: Create Inductive Edge
  CreateLegalEdge(
    id: "inductive_contract_formation",
    type: generalizes,
    nodes: {
      "sa_civil_contract-valid",
      "sa_commercial_sale-agreement",
      "sa_construction_contract-valid",
      "sa_labour_employment-contract",
      "za_general_contract_formation_principle"
    },
    weight: 0.8
  )
  
  MarkAsInferred(
    infType: inductive,
    conf: 0.8
  )

Step 5: Add to Hypergraph
  AddLegalNode(generalPrinciple)
  AddLegalEdge(inductiveEdge)
  
  Result:
    - principleNodes' = principleNodes ∪ {za_general_contract_formation_principle}
    - inferredEdges' = inferredEdges ∪ {inductive_contract_formation}
```

### Python Implementation

```python
def inductive_inference(examples, pattern_description):
    """Perform inductive generalization."""
    
    # Verify preconditions
    assert len(examples) >= 2, "Need at least 2 examples"
    assert all(e.inference_level == 0 for e in examples), "Examples must be enumerated laws"
    
    # Calculate confidence
    n = len(examples)
    confidence = min(0.95, n / (n + 1))
    
    # Create general principle
    principle = LegalNode(
        node_id=f"principle_from_{len(examples)}_examples",
        node_type=LegalNodeType.PRINCIPLE,
        name=f"Generalized Principle: {pattern_description}",
        content=f"Pattern observed in {n} laws: {pattern_description}",
        jurisdiction="za",
        branch="general",
        metadata={"inference_type": "inductive", "num_examples": n}
    )
    principle.inference_level = max(e.inference_level for e in examples) + 1
    
    # Create inductive edge
    edge = LegalHyperedge(
        edge_id=f"inductive_{principle.node_id}",
        relation_type=LegalRelationType.GENERALIZES,
        nodes={e.node_id for e in examples} | {principle.node_id},
        weight=confidence
    )
    edge.inference_type = InferenceType.INDUCTIVE
    edge.confidence = confidence
    
    return principle, edge, confidence

# Apply to contract laws
contract_laws = [
    get_node("sa_civil_contract-valid"),
    get_node("sa_commercial_sale-agreement"),
    get_node("sa_construction_contract-valid"),
    get_node("sa_labour_employment-contract")
]

principle, edge, conf = inductive_inference(
    examples=contract_laws,
    pattern_description="All contracts require offer and acceptance"
)

print(f"Generalized Principle: {principle.name}")
print(f"Confidence: {conf:.2f}")
print(f"Based on {len(contract_laws)} examples")
```

## Example 4: Abductive Inference

### Scenario

Explain why multiple legal areas require a "mental element" by hypothesizing a fairness principle.

### Observations

```
1. Criminal Law: "Mens rea (guilty mind) required for criminal liability"
2. Contract Law: "Intention to create legal relations required"
3. Delict Law: "Fault (negligence or intent) required for liability"
4. Administrative Law: "Rational decision-making required"
```

### Formal Specification

```
AbductiveInference(observations: set of LNODEID, hypothesis: LNODEID,
                   explanatoryPower: real)
  returns (plausible: boolean, confidence: real)

  Post-condition:
    - New edge with relationType = supports
    - Edge marked as inferenceType = abductive
    - confidence = explanatoryPower * 0.7
```

### Application

```
Step 1: Generate Hypothesis
  Hypothesis: "Legal liability requires mental culpability to ensure fairness"
  
  This explains why all four areas require some form of mental element:
  - Criminal: Can't punish without guilty mind
  - Contract: Can't bind without intention
  - Delict: Can't impose liability without fault
  - Administrative: Can't justify decisions without rationality

Step 2: Evaluate Hypothesis
  
  Explanatory Power (0-1):
    - Explains criminal law: YES (0.25)
    - Explains contract law: YES (0.25)
    - Explains delict law: YES (0.25)
    - Explains admin law: PARTIAL (0.15)
    Total: 0.9
  
  Coherence with Existing Framework (0-1):
    - Consistent with fairness principles: 0.9
    - Consistent with rule of law: 0.8
    - Average: 0.85
  
  Simplicity (Occam's Razor) (0-1):
    - Single unifying principle: 0.8
    - Minimal assumptions: 0.7
    - Average: 0.75
  
  Combined Base Score:
    (0.9 * 0.5) + (0.85 * 0.3) + (0.75 * 0.2) = 0.855

Step 3: Create Hypothesis Node
  InitializeLegalNode(
    id: "za_mental_culpability_principle",
    type: principle,
    name: "Mental Culpability Principle",
    content: "Legal liability requires mental culpability to ensure fairness",
    jurisdiction: "za",
    branch: "general"
  )
  
  SetInferenceLevel(level: 1)

Step 4: Calculate Confidence
  # Abductive reasoning has inherent uncertainty
  confidence = 0.855 * 0.7 = 0.5985 ≈ 0.60

Step 5: Create Abductive Edge
  CreateLegalEdge(
    id: "abductive_mental_culpability",
    type: supports,
    nodes: {
      "sa_criminal_mens-rea",
      "sa_civil_intention",
      "sa_delict_fault",
      "sa_admin_rationality",
      "za_mental_culpability_principle"
    },
    weight: 0.60
  )
  
  MarkAsInferred(
    infType: abductive,
    conf: 0.60
  )
```

### Python Implementation

```python
def abductive_inference(observations, hypothesis_text):
    """Generate and evaluate abductive hypothesis."""
    
    # Create hypothesis node
    hypothesis = LegalNode(
        node_id="hypothesis_mental_culpability",
        node_type=LegalNodeType.PRINCIPLE,
        name="Mental Culpability Hypothesis",
        content=hypothesis_text,
        jurisdiction="za",
        branch="general"
    )
    
    # Evaluate explanatory power
    explanatory_power = sum(
        1.0 if explains(hypothesis, obs) else 0.0
        for obs in observations
    ) / len(observations)
    
    # Evaluate coherence with existing framework
    coherence = evaluate_coherence(hypothesis, existing_principles)
    
    # Evaluate simplicity
    simplicity = 1.0 / (1 + count_assumptions(hypothesis))
    
    # Combined score
    base_score = (
        explanatory_power * 0.5 +
        coherence * 0.3 +
        simplicity * 0.2
    )
    
    # Abductive discount
    confidence = base_score * 0.7
    
    # Create supporting edge
    edge = LegalHyperedge(
        edge_id="abductive_support",
        relation_type=LegalRelationType.SUPPORTS,
        nodes={o.node_id for o in observations} | {hypothesis.node_id},
        weight=confidence
    )
    edge.inference_type = InferenceType.ABDUCTIVE
    edge.confidence = confidence
    
    return hypothesis, edge, confidence

# Apply
observations = [
    get_node("sa_criminal_mens-rea"),
    get_node("sa_civil_intention"),
    get_node("sa_delict_fault"),
    get_node("sa_admin_rationality")
]

hypothesis, edge, conf = abductive_inference(
    observations=observations,
    hypothesis_text="Legal liability requires mental culpability for fairness"
)

print(f"Hypothesis: {hypothesis.content}")
print(f"Confidence: {conf:.2f} (medium - abductive)")
print(f"Explains {len(observations)} observations")
```

## Example 5: Analogical Inference

### Scenario

Transfer "frustration of purpose" principle from contract law to employment law.

### Input

```
Source Domain: Contract Law
  Principle: "Frustration of Purpose Doctrine"
  Content: "A contract is discharged when its fundamental purpose 
            becomes impossible to achieve through no fault of parties"
  Confidence: 0.9

Target Domain: Employment Law
  Context: Employment relationships are ongoing contractual relationships
```

### Formal Specification

```
AnalogicalInference(sourceNode: LNODEID, targetNode: LNODEID,
                    similarity: real, principle: LNODEID)
  returns (applicable: boolean, confidence: real)

  Post-condition:
    - New edge with relationType = applies_to
    - Edge marked as inferenceType = analogical
    - confidence = similarity * edges(source_edge).confidence
```

### Application

```
Step 1: Calculate Similarity

  Structural Similarity (0-1):
    - Both involve ongoing obligations: 0.9
    - Both have start/end points: 0.8
    - Both involve bilateral duties: 0.9
    Average: 0.87
  
  Functional Similarity (0-1):
    - Both protect reasonable expectations: 0.95
    - Both enforce promises: 0.85
    - Both allow for termination: 0.9
    Average: 0.90
  
  Domain Proximity (0-1):
    - Both in civil law: 0.9
    - Related subject matter: 0.8
    - Share common principles: 0.85
    Average: 0.85
  
  Overall Similarity:
    (0.87 + 0.90 + 0.85) / 3 = 0.873

Step 2: Create Transferred Principle
  InitializeLegalNode(
    id: "za_labour_frustration_of_purpose",
    type: principle,
    name: "Employment Frustration Principle",
    content: "Employment relationship is discharged when fundamental 
              purpose becomes impossible through no fault of parties",
    jurisdiction: "za",
    branch: labour
  )
  
  SetInferenceLevel(level: 1)

Step 3: Calculate Transfer Confidence
  source_confidence = 0.9
  similarity = 0.873
  transfer_discount = 0.9  # Slight uncertainty in transfer
  
  confidence = 0.873 * 0.9 * 0.9 = 0.707

Step 4: Create Analogical Edge
  CreateLegalEdge(
    id: "analogical_frustration_contract_to_labour",
    type: applies_to,
    nodes: {
      "sa_civil_frustration_of_purpose",
      "za_labour_frustration_of_purpose"
    },
    weight: 0.707
  )
  
  MarkAsInferred(
    infType: analogical,
    conf: 0.707
  )
  
  Metadata:
    similarity_score: 0.873
    structural_similarity: 0.87
    functional_similarity: 0.90
    domain_proximity: 0.85
```

### Python Implementation

```python
def analogical_inference(source_principle, target_domain):
    """Transfer principle by analogy."""
    
    # Calculate similarities
    structural_sim = calculate_structural_similarity(
        source_principle.domain,
        target_domain
    )
    
    functional_sim = calculate_functional_similarity(
        source_principle.purpose,
        target_domain.purpose
    )
    
    domain_proximity = calculate_domain_proximity(
        source_principle.branch,
        target_domain.branch
    )
    
    # Overall similarity
    similarity = (structural_sim + functional_sim + domain_proximity) / 3
    
    # Check threshold
    if similarity < 0.6:
        return None, None, 0.0
    
    # Create transferred principle
    transferred = LegalNode(
        node_id=f"{target_domain.branch}_{source_principle.node_id}",
        node_type=LegalNodeType.PRINCIPLE,
        name=f"{source_principle.name} (by analogy to {target_domain.name})",
        content=adapt_content(source_principle.content, target_domain),
        jurisdiction=source_principle.jurisdiction,
        branch=target_domain.branch
    )
    transferred.inference_level = source_principle.inference_level
    
    # Calculate confidence
    confidence = similarity * source_principle.confidence * 0.9
    
    # Create analogical edge
    edge = LegalHyperedge(
        edge_id=f"analogical_{source_principle.node_id}_to_{target_domain.branch}",
        relation_type=LegalRelationType.APPLIES_TO,
        nodes={source_principle.node_id, transferred.node_id},
        weight=confidence
    )
    edge.inference_type = InferenceType.ANALOGICAL
    edge.confidence = confidence
    edge.metadata = {
        "similarity": similarity,
        "structural_similarity": structural_sim,
        "functional_similarity": functional_sim,
        "domain_proximity": domain_proximity
    }
    
    return transferred, edge, confidence

# Apply
source = get_node("sa_civil_frustration_of_purpose")
target_domain = get_domain("labour")

transferred, edge, conf = analogical_inference(source, target_domain)

print(f"Transferred: {transferred.name}")
print(f"Confidence: {conf:.2f}")
print(f"Similarity: {edge.metadata['similarity']:.2f}")
```

## Example 6: Building Inference Hierarchy

### Scenario

Build a complete inference hierarchy showing how higher-level principles derive from enumerated laws.

### Hierarchy Structure

```
Level 0: Enumerated Laws (from lex/ framework)
  ├─ sa_civil_contract-valid?
  ├─ sa_civil_offer-exists?
  ├─ sa_commercial_sale-agreement?
  ├─ sa_construction_contract?
  ├─ sa_labour_employment-contract?
  └─ ...

Level 1: First-Order Principles (inferred from Level 0)
  ├─ Contract Formation Principle (inductive from multiple contract laws)
  ├─ Mental Culpability Principle (abductive from criminal/civil laws)
  ├─ Reasonable Person Standard (inductive from multiple areas)
  └─ ...

Level 2: Meta-Principles (inferred from Level 1)
  ├─ Legal Certainty Principle
  ├─ Fairness in Legal Process
  └─ ...
```

### Building Process

```
Step 1: Load Level 0 (Enumerated Laws)
  For each .scm file in lex/ directory:
    For each (define ...) in file:
      node = InitializeLegalNode(...)
      node.inferenceLevel = 0
      AddLegalNode(node)
      enumeratedNodes' = enumeratedNodes ∪ {node.nodeId}

Step 2: Infer Level 1 Principles
  # Inductive inference
  contract_laws = filter(enumeratedNodes, lambda n: "contract" in n.content)
  if size(contract_laws) >= 2:
    principle = InductiveInference(
      examples: contract_laws,
      pattern: "require offer and acceptance"
    )
    principle.inferenceLevel = 1
    AddLegalNode(principle)
  
  # Abductive inference
  mental_element_laws = filter(enumeratedNodes, lambda n: "intent" in n.content or "fault" in n.content)
  if size(mental_element_laws) >= 2:
    hypothesis = AbductiveInference(
      observations: mental_element_laws,
      hypothesis: "mental culpability required"
    )
    hypothesis.inferenceLevel = 1
    AddLegalNode(hypothesis)

Step 3: Infer Level 2 Meta-Principles
  level1_principles = filter(principleNodes, lambda n: n.inferenceLevel == 1)
  
  # Identify common themes
  fairness_principles = filter(level1_principles, lambda n: "fair" in n.content or "reasonable" in n.content)
  
  if size(fairness_principles) >= 2:
    meta_principle = InductiveInference(
      examples: fairness_principles,
      pattern: "promote fairness"
    )
    meta_principle.inferenceLevel = 2
    AddLegalNode(meta_principle)

Step 4: Query Hierarchy
  GetInferredPrinciples() returns {n | n ∈ principleNodes ∧ n.inferenceLevel > 0}
  
  For each level L from 0 to max:
    principles_at_level_L = filter(principleNodes, lambda n: n.inferenceLevel == L)
    display(principles_at_level_L)
```

### Python Implementation

```python
def build_inference_hierarchy(engine):
    """Build complete inference hierarchy."""
    
    hierarchy = {}
    
    # Level 0: Enumerated laws
    enumerated = engine.get_enumerated_laws()
    hierarchy[0] = enumerated
    print(f"Level 0: {len(enumerated)} enumerated laws")
    
    # Level 1: Infer first-order principles
    level1_principles = []
    
    # Group by topic
    topics = group_by_topic(enumerated)
    
    for topic, laws in topics.items():
        if len(laws) >= 2:
            # Try inductive inference
            principle, confidence = inductive_inference(laws, topic)
            if confidence >= 0.7:
                principle.inference_level = 1
                level1_principles.append(principle)
                engine.add_node(principle)
    
    hierarchy[1] = level1_principles
    print(f"Level 1: {len(level1_principles)} first-order principles")
    
    # Level 2: Infer meta-principles
    level2_principles = []
    
    if len(level1_principles) >= 2:
        meta_topics = group_by_theme(level1_principles)
        
        for theme, principles in meta_topics.items():
            if len(principles) >= 2:
                meta_principle, confidence = inductive_inference(principles, theme)
                if confidence >= 0.6:
                    meta_principle.inference_level = 2
                    level2_principles.append(meta_principle)
                    engine.add_node(meta_principle)
    
    hierarchy[2] = level2_principles
    print(f"Level 2: {len(level2_principles)} meta-principles")
    
    return hierarchy

# Build hierarchy
hierarchy = build_inference_hierarchy(engine)

# Display
for level in sorted(hierarchy.keys()):
    print(f"\nLevel {level}:")
    for node in hierarchy[level][:5]:  # Show first 5
        print(f"  - {node.name} (confidence: {node.confidence:.2f})")
```

## Example 7: Querying the Hypergraph

### Common Queries

```python
# Query 1: Find all principles related to "contract"
contract_nodes = engine.query_by_content("contract")
print(f"Found {len(contract_nodes)} contract-related nodes")

# Query 2: Find dependencies of a specific principle
dependencies = engine.get_dependencies("sa_civil_contract-valid")
print(f"Contract validity depends on: {[d.name for d in dependencies]}")

# Query 3: Find all inferred principles
inferred = engine.get_inferred_principles()
print(f"Found {len(inferred)} inferred principles")

# Query 4: Trace inference path
path = engine.trace_inference_path(
    start="sa_civil_contract-valid",
    end="za_general_contract_formation_principle"
)
print(f"Inference path: {' → '.join([n.name for n in path])}")

# Query 5: Find principles by inference type
deductive_principles = engine.query_by_inference_type("deductive")
inductive_principles = engine.query_by_inference_type("inductive")
abductive_principles = engine.query_by_inference_type("abductive")
analogical_principles = engine.query_by_inference_type("analogical")

print(f"Deductive: {len(deductive_principles)}")
print(f"Inductive: {len(inductive_principles)}")
print(f"Abductive: {len(abductive_principles)}")
print(f"Analogical: {len(analogical_principles)}")

# Query 6: Get statistics
stats = engine.get_statistics()
print(f"Total nodes: {stats['num_nodes']}")
print(f"Total edges: {stats['num_edges']}")
print(f"Enumerated laws: {stats['num_enumerated']}")
print(f"Inferred principles: {stats['num_inferred']}")
print(f"Average inference level: {stats['avg_inference_level']:.2f}")
```

## Conclusion

These examples demonstrate how the Z++ formal specification enables:

1. **Systematic Loading**: Legal frameworks are loaded and structured formally
2. **Deductive Reasoning**: Apply principles with high confidence
3. **Inductive Reasoning**: Discover patterns and generalize
4. **Abductive Reasoning**: Hypothesize explanatory principles
5. **Analogical Reasoning**: Transfer knowledge across domains
6. **Hierarchical Organization**: Build multi-level knowledge structures
7. **Powerful Querying**: Navigate and analyze legal relationships

The formal specification ensures that all operations maintain invariants, track confidence levels, and provide traceable inference paths.

## References

- [LEX_HYPERGRAPH_SPEC.md](LEX_HYPERGRAPH_SPEC.md) - Complete Z++ specification
- [INFERENCE_MODELS.md](INFERENCE_MODELS.md) - Inference model details
- [lex/README.md](../../lex/README.md) - Legal framework structure
