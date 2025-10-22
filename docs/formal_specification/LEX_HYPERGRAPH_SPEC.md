# Z++ Formal Specification: Lex Hypergraph

## Overview

This document provides the Z++ formal specification for the **Lex Hypergraph** - a hypergraph structure that represents legal frameworks, principles, statutes, and their interdependencies. The lex hypergraph enables formal reasoning about legal systems and supports inference of general principles from enumerated laws.

## Table of Contents

1. [Introduction](#introduction)
2. [Basic Types for Lex Hypergraph](#basic-types-for-lex-hypergraph)
3. [Legal Node Schema](#legal-node-schema)
4. [Legal Hyperedge Schema](#legal-hyperedge-schema)
5. [Lex Hypergraph Structure](#lex-hypergraph-structure)
6. [Inference Models](#inference-models)
7. [Operations](#operations)
8. [Invariants](#invariants)
9. [Examples](#examples)

## Introduction

### Purpose

The Lex Hypergraph formal specification defines:
- The structure of legal frameworks as hypergraphs
- Relationships between legal principles, statutes, and concepts
- Formal operations for legal reasoning and inference
- Models for inferring general principles from specific enumerated laws

### Scope

This specification covers:
- Legal nodes (principles, statutes, concepts, sections)
- Legal hyperedges (dependencies, citations, interpretations)
- The complete hypergraph structure for legal frameworks
- Inference operations (deductive, inductive, abductive)
- Primary models for legal reasoning

## Basic Types for Lex Hypergraph

### Given Sets

```
LNODEID       -- Legal node identifiers
LEDGEID       -- Legal edge identifiers  
JURISDICTION  -- Legal jurisdictions (za, uk, us, etc.)
BRANCH        -- Legal branches (civil, criminal, constitutional, etc.)
CONTENT       -- Legal text content
```

### Enumerated Types

**Legal Node Types:**
```
LNODETYPE ::= statute | section | subsection | case | precedent | 
              principle | concept | party | court | judge
```

**Legal Relation Types:**
```
LRELTYPE ::= cites | interprets | overrules | follows | distinguishes |
             amends | repeals | applies_to | conflicts_with | supports |
             depends_on | infers_from | generalizes | specializes
```

**Inference Types:**
```
INFERENCETYPE ::= deductive | inductive | abductive | analogical
```

**Legal Branches:**
```
LEGALBRANCH ::= civil | criminal | constitutional | administrative |
                labour | environmental | construction | international
```

## Legal Node Schema

### LegalNode Class

Represents a legal entity in the hypergraph.

**State:**
- `nodeId: LNODEID` - Unique identifier for the legal node
- `nodeType: LNODETYPE` - Type of legal entity
- `name: string` - Human-readable name
- `content: CONTENT` - Full legal text content
- `jurisdiction: JURISDICTION` - Legal jurisdiction
- `branch: LEGALBRANCH` - Legal branch this node belongs to
- `metadata: map from string to string` - Additional metadata
- `properties: map from string to any` - Node-specific properties
- `inferenceLevel: natural number` - Depth in inference hierarchy (0 = enumerated law)

**Invariants:**
```
length(name) > 0
length(content) >= 0
inferenceLevel >= 0
```

**Operations:**

```
InitializeLegalNode(id: LNODEID, type: LNODETYPE, name: string, 
                    content: CONTENT, jurisdiction: JURISDICTION,
                    branch: LEGALBRANCH)
  Pre-condition:
    - length(name) > 0
  Post-condition:
    - nodeId' = id
    - nodeType' = type
    - name' = name
    - content' = content
    - jurisdiction' = jurisdiction
    - branch' = branch
    - metadata' = ∅
    - properties' = ∅
    - inferenceLevel' = 0

SetInferenceLevel(level: natural number)
  Pre-condition:
    - level >= 0
  Post-condition:
    - inferenceLevel' = level
    - All other fields unchanged

AddMetadata(key: string, value: string)
  Pre-condition:
    - length(key) > 0
    - key not in domain(metadata)
  Post-condition:
    - metadata' = metadata ∪ {key → value}
    - nodeId, nodeType, name, content unchanged
```

## Legal Hyperedge Schema

### LegalHyperedge Class

Represents a relationship between multiple legal entities.

**State:**
- `edgeId: LEDGEID` - Unique identifier for the edge
- `relationType: LRELTYPE` - Type of legal relationship
- `nodes: set of LNODEID` - Connected legal nodes
- `weight: real number` - Relationship strength
- `confidence: real number` - Confidence in the relationship (for inferred edges)
- `inferenceType: optional INFERENCETYPE` - How this relationship was inferred
- `metadata: map from string to string` - Additional metadata
- `properties: map from string to any` - Edge-specific properties

**Invariants:**
```
size(nodes) >= 2                    -- At least two nodes
0 <= weight <= 1                    -- Normalized weight
0 <= confidence <= 1                -- Normalized confidence
weight > 0                          -- Positive weight
inferenceType ≠ null implies confidence < 1  -- Inferred edges have uncertainty
```

**Operations:**

```
CreateLegalEdge(id: LEDGEID, type: LRELTYPE, connectedNodes: set of LNODEID,
                edgeWeight: real)
  Pre-condition:
    - size(connectedNodes) >= 2
    - 0 < edgeWeight <= 1
  Post-condition:
    - edgeId' = id
    - relationType' = type
    - nodes' = connectedNodes
    - weight' = edgeWeight
    - confidence' = 1.0
    - inferenceType' = null
    - metadata' = ∅

MarkAsInferred(infType: INFERENCETYPE, conf: real)
  Pre-condition:
    - 0 < conf < 1
  Post-condition:
    - inferenceType' = infType
    - confidence' = conf
    - edgeId, relationType, nodes, weight unchanged
```

## Lex Hypergraph Structure

### LexHypergraph Class

Manages the complete legal framework as a hypergraph.

**State:**
- `nodes: map from LNODEID to LegalNode` - All legal nodes
- `edges: map from LEDGEID to LegalHyperedge` - All legal relationships
- `nodeToEdges: map from LNODEID to set of LEDGEID` - Node-to-edge index
- `branchNodes: map from LEGALBRANCH to set of LNODEID` - Branch-to-nodes index
- `jurisdictionNodes: map from JURISDICTION to set of LNODEID` - Jurisdiction index
- `inferredEdges: set of LEDGEID` - Edges created through inference
- `enumeratedNodes: set of LNODEID` - Nodes representing enumerated laws (inferenceLevel = 0)
- `principleNodes: set of LNODEID` - Nodes representing general principles

**Invariants:**

```
-- Index consistency
domain(nodeToEdges) = domain(nodes)

-- Edge node existence  
For all e in domain(edges):
  edges(e).nodes ⊆ domain(nodes)

-- Node-to-edge mapping consistency
For all n in domain(nodes):
  nodeToEdges(n) = {e in domain(edges) | n in edges(e).nodes}

-- Branch index consistency
For all b in domain(branchNodes):
  branchNodes(b) = {n in domain(nodes) | nodes(n).branch = b}

-- Jurisdiction index consistency
For all j in domain(jurisdictionNodes):
  jurisdictionNodes(j) = {n in domain(nodes) | nodes(n).jurisdiction = j}

-- Inferred edges tracking
inferredEdges = {e in domain(edges) | edges(e).inferenceType ≠ null}

-- Enumerated nodes definition
enumeratedNodes = {n in domain(nodes) | nodes(n).inferenceLevel = 0}

-- Principle nodes definition
principleNodes = {n in domain(nodes) | nodes(n).nodeType = principle}
```

**Operations:**

```
AddLegalNode(node: LegalNode)
  Pre-condition:
    - node.nodeId not in domain(nodes)
  Post-condition:
    - nodes' = nodes ∪ {node.nodeId → node}
    - nodeToEdges' = nodeToEdges ∪ {node.nodeId → ∅}
    - branchNodes'(node.branch) = branchNodes(node.branch) ∪ {node.nodeId}
    - jurisdictionNodes'(node.jurisdiction) = 
        jurisdictionNodes(node.jurisdiction) ∪ {node.nodeId}
    - If node.inferenceLevel = 0:
        enumeratedNodes' = enumeratedNodes ∪ {node.nodeId}
    - If node.nodeType = principle:
        principleNodes' = principleNodes ∪ {node.nodeId}
    - edges unchanged

AddLegalEdge(edge: LegalHyperedge)
  Pre-condition:
    - edge.edgeId not in domain(edges)
    - edge.nodes ⊆ domain(nodes)
  Post-condition:
    - edges' = edges ∪ {edge.edgeId → edge}
    - For each n in edge.nodes:
        nodeToEdges'(n) = nodeToEdges(n) ∪ {edge.edgeId}
    - If edge.inferenceType ≠ null:
        inferredEdges' = inferredEdges ∪ {edge.edgeId}
    - nodes, branchNodes, jurisdictionNodes unchanged

GetNodesByBranch(branch: LEGALBRANCH) returns set of LegalNode
  Pre-condition: branch in domain(branchNodes)
  Returns: {nodes(n) | n in branchNodes(branch)}

GetNodesByJurisdiction(jurisdiction: JURISDICTION) returns set of LegalNode
  Pre-condition: jurisdiction in domain(jurisdictionNodes)
  Returns: {nodes(n) | n in jurisdictionNodes(jurisdiction)}

GetConnectedNodes(nodeId: LNODEID) returns set of LNODEID
  Pre-condition: nodeId in domain(nodes)
  Returns: union of (edges(e).nodes \ {nodeId}) for all e in nodeToEdges(nodeId)

GetDependencies(nodeId: LNODEID) returns set of LNODEID
  Pre-condition: nodeId in domain(nodes)
  Returns: {n | exists e in nodeToEdges(nodeId) where 
           edges(e).relationType = depends_on and n in edges(e).nodes and n ≠ nodeId}

GetEnumeratedLaws() returns set of LegalNode
  Returns: {nodes(n) | n in enumeratedNodes}

GetInferredPrinciples() returns set of LegalNode
  Returns: {nodes(n) | n in principleNodes and nodes(n).inferenceLevel > 0}
```

## Inference Models

### Primary Inference Models for Legal Reasoning

This section defines the primary models for inferring general principles from enumerated laws.

### Model 1: Deductive Inference

**Purpose:** Derive specific conclusions from general principles and enumerated laws.

**Formal Definition:**

```
DeductiveInference(premises: set of LNODEID, conclusion: LNODEID) 
  returns (valid: boolean, confidence: real)

  Pre-condition:
    - premises ⊆ domain(nodes)
    - conclusion in domain(nodes)
    - All nodes in premises have inferenceLevel <= nodes(conclusion).inferenceLevel
  
  Post-condition:
    - If valid = true:
        - New edge created: premises ∪ {conclusion} with relationType = infers_from
        - Edge marked as inferenceType = deductive
        - confidence in range [0.8, 1.0] for deductive reasoning
    - nodes unchanged
```

**Deductive Rules:**

1. **Modus Ponens**: If A → B and A, then B
2. **Syllogism**: If A → B and B → C, then A → C
3. **Subsumption**: If concept A is a specialization of B, then rules for B apply to A

### Model 2: Inductive Inference

**Purpose:** Generalize patterns from multiple enumerated laws to form principles.

**Formal Definition:**

```
InductiveInference(examples: set of LNODEID, generalPrinciple: LNODEID,
                   pattern: string) 
  returns (valid: boolean, confidence: real)

  Pre-condition:
    - examples ⊆ enumeratedNodes
    - size(examples) >= 2
    - generalPrinciple in principleNodes
    - generalPrinciple.inferenceLevel > 0
    - All nodes in examples share common pattern
  
  Post-condition:
    - If valid = true:
        - New edge created: examples ∪ {generalPrinciple} with relationType = generalizes
        - Edge marked as inferenceType = inductive
        - confidence = min(0.95, (size(examples) / (size(examples) + 1)))
        - generalPrinciple.inferenceLevel' = max inference level of examples + 1
    - enumeratedNodes unchanged
```

**Inductive Patterns:**

1. **Common Elements**: Multiple laws share common requirements or elements
2. **Similar Outcomes**: Different laws lead to similar legal consequences
3. **Parallel Structure**: Laws have analogous logical structures
4. **Consistent Application**: Laws applied consistently across cases

### Model 3: Abductive Inference

**Purpose:** Hypothesize the best explanation or principle that accounts for observed legal rules.

**Formal Definition:**

```
AbductiveInference(observations: set of LNODEID, hypothesis: LNODEID,
                   explanatoryPower: real)
  returns (plausible: boolean, confidence: real)

  Pre-condition:
    - observations ⊆ domain(nodes)
    - size(observations) >= 1
    - hypothesis.nodeType = principle
    - 0 < explanatoryPower <= 1
  
  Post-condition:
    - If plausible = true:
        - New edge created: observations ∪ {hypothesis} with relationType = supports
        - Edge marked as inferenceType = abductive
        - confidence = explanatoryPower * 0.7  -- Abductive reasoning has inherent uncertainty
        - hypothesis added to principleNodes if not already present
```

**Abductive Criteria:**

1. **Explanatory Power**: How well the principle explains the observations
2. **Simplicity**: Preference for simpler explanations (Occam's Razor)
3. **Coherence**: Consistency with existing legal framework
4. **Predictive Value**: Ability to predict outcomes in new cases

### Model 4: Analogical Inference

**Purpose:** Apply principles from one legal domain to another by analogy.

**Formal Definition:**

```
AnalogicalInference(sourceNode: LNODEID, targetNode: LNODEID,
                    similarity: real, principle: LNODEID)
  returns (applicable: boolean, confidence: real)

  Pre-condition:
    - sourceNode, targetNode in domain(nodes)
    - sourceNode ≠ targetNode
    - 0 < similarity <= 1
    - principle in principleNodes
    - Exists edge connecting sourceNode and principle
  
  Post-condition:
    - If applicable = true:
        - New edge created: {targetNode, principle} with relationType = applies_to
        - Edge marked as inferenceType = analogical
        - confidence = similarity * edges(source_edge).confidence
```

**Analogical Criteria:**

1. **Structural Similarity**: Similar logical structure of laws
2. **Functional Similarity**: Similar purposes or goals
3. **Domain Proximity**: Related legal branches or jurisdictions
4. **Precedential Value**: Strength of analogy based on case law

### Inference Confidence Calculation

**Formula for Combined Confidence:**

```
CombinedConfidence(edges: set of LEDGEID) returns real

  Pre-condition:
    - edges ⊆ domain(edges)
    - size(edges) > 0
  
  Returns:
    - If size(edges) = 1: edges(first(edges)).confidence
    - Otherwise: 1 - product of (1 - edges(e).confidence) for all e in edges
    
  Explanation: Uses noisy-OR combination for multiple evidence sources
```

## Operations

### Inference Operations

```
InferGeneralPrinciple(laws: set of LNODEID, principleType: LNODETYPE,
                     method: INFERENCETYPE)
  returns (principle: LegalNode, confidence: real)
  
  Pre-condition:
    - laws ⊆ enumeratedNodes
    - size(laws) >= 1
    - method in {deductive, inductive, abductive, analogical}
  
  Post-condition:
    - New principle node created with:
        - nodeType' = principleType
        - inferenceLevel' = max({nodes(n).inferenceLevel | n in laws}) + 1
    - New edge created connecting laws and principle
    - Edge marked with appropriate inferenceType
    - principle added to principleNodes'

FindSimilarPrinciples(targetPrinciple: LNODEID, threshold: real)
  returns set of (LNODEID, real)  -- (node, similarity score)
  
  Pre-condition:
    - targetPrinciple in principleNodes
    - 0 < threshold <= 1
  
  Returns:
    - Set of (nodeId, similarity) pairs where:
        - nodeId in principleNodes
        - similarity >= threshold
        - Similarity based on content, dependencies, and metadata

ValidateInference(sourceNodes: set of LNODEID, targetNode: LNODEID,
                 inferenceType: INFERENCETYPE)
  returns (valid: boolean, confidence: real, explanation: string)
  
  Pre-condition:
    - sourceNodes ⊆ domain(nodes)
    - targetNode in domain(nodes)
  
  Returns:
    - valid: whether the inference is logically sound
    - confidence: degree of certainty in the inference
    - explanation: textual justification for the inference
```

### Query Operations

```
QueryByContent(searchText: string) returns set of LegalNode
  Pre-condition: length(searchText) > 0
  Returns: {nodes(n) | n in domain(nodes) and searchText appears in nodes(n).content}

QueryByType(nodeType: LNODETYPE) returns set of LegalNode
  Returns: {nodes(n) | n in domain(nodes) and nodes(n).nodeType = nodeType}

QueryByRelation(nodeId: LNODEID, relationType: LRELTYPE) returns set of LegalNode
  Pre-condition: nodeId in domain(nodes)
  Returns: {nodes(n) | exists e in nodeToEdges(nodeId) where
           edges(e).relationType = relationType and n in edges(e).nodes and n ≠ nodeId}

TraceInferencePath(startNode: LNODEID, endNode: LNODEID)
  returns sequence of (LNODEID, LEDGEID)  -- Path of nodes and edges
  
  Pre-condition:
    - startNode, endNode in domain(nodes)
  
  Returns:
    - Shortest path from startNode to endNode through inference edges
    - Empty sequence if no path exists
```

## Invariants

### Lex Hypergraph Invariants

```
-- All edges connect existing nodes
For all e in domain(edges):
  edges(e).nodes ⊆ domain(nodes)

-- Inferred edges have valid inference types
For all e in inferredEdges:
  edges(e).inferenceType ≠ null

-- Inferred edges have confidence < 1
For all e in inferredEdges:
  edges(e).confidence < 1.0

-- Enumerated laws have inference level 0
For all n in enumeratedNodes:
  nodes(n).inferenceLevel = 0

-- Inferred principles have positive inference level
For all n in principleNodes:
  nodes(n).inferenceLevel > 0 implies n not in enumeratedNodes

-- Branch index is complete
For all n in domain(nodes):
  n in branchNodes(nodes(n).branch)

-- Inference edges point from lower to higher inference levels
For all e in inferredEdges where edges(e).relationType in {infers_from, generalizes}:
  Let sourceNodes = edges(e).nodes \ principleNodes
  Let targetNodes = edges(e).nodes ∩ principleNodes
  For all s in sourceNodes, t in targetNodes:
    nodes(s).inferenceLevel <= nodes(t).inferenceLevel
```

### Consistency Invariants

```
-- No self-referential edges
For all e in domain(edges):
  size(edges(e).nodes) >= 2

-- Dependency acyclicity (for depends_on edges)
No cycles in the directed graph formed by depends_on edges

-- Jurisdiction coherence
For all e in domain(edges) where edges(e).relationType = cites:
  All nodes in edges(e).nodes share same jurisdiction or
  one is international law

-- Branch coherence  
For all e in domain(edges) where edges(e).relationType in {depends_on, supports}:
  All nodes in edges(e).nodes belong to same or related branches
```

## Examples

### Example 1: Loading Enumerated Laws from Lex Framework

```
Input:
  South African Civil Law Framework with contract law principles

Process:
  1. Load south_african_civil_law.scm
  2. Parse definitions: contract-valid?, offer-exists?, acceptance-exists?, etc.
  
Operation: AddLegalNode for each definition
  - nodeId: "sa_civil_contract-valid"
  - nodeType: principle
  - name: "Contract Valid"
  - content: "(define contract-valid? (lambda (contract) ...))"
  - jurisdiction: "za"
  - branch: civil
  - inferenceLevel: 0  (enumerated law)

Result:
  Node added to:
    - nodes
    - nodeToEdges (with empty edge set)
    - branchNodes(civil)
    - jurisdictionNodes(za)
    - enumeratedNodes
    - principleNodes
```

### Example 2: Creating Dependencies Between Legal Principles

```
Input:
  Two principles:
    - contract-valid? depends on offer-exists?
    - contract-valid? depends on acceptance-exists?

Operation: AddLegalEdge for each dependency
  Edge 1:
    - edgeId: "civil_rel_contract-valid_to_offer-exists"
    - relationType: depends_on
    - nodes: {"sa_civil_contract-valid", "sa_civil_offer-exists"}
    - weight: 1.0
    - confidence: 1.0
    - inferenceType: null  (explicitly stated dependency)

Result:
  Edge added to:
    - edges
    - nodeToEdges for both connected nodes
  Not added to inferredEdges (not inferred)
```

### Example 3: Inductive Inference - Generalizing from Multiple Contract Laws

```
Input:
  Enumerated laws from different branches:
    - Civil: contract-valid? requires offer + acceptance
    - Commercial: sale-agreement-valid? requires offer + acceptance  
    - Construction: construction-contract-valid? requires offer + acceptance
    - Labour: employment-contract-valid? requires offer + acceptance

Operation: InductiveInference
  - examples: {civil_contract, commercial_sale, construction_contract, labour_contract}
  - pattern: "All require offer and acceptance"
  
Process:
  1. Identify common pattern: offer + acceptance
  2. Create general principle node:
      - nodeId: "za_general_contract_formation_principle"
      - nodeType: principle
      - name: "Contract Formation Principle"
      - content: "A valid contract requires mutual agreement through offer and acceptance"
      - inferenceLevel: 1
  3. Create inductive edge:
      - relationType: generalizes
      - inferenceType: inductive
      - confidence: 0.8  (4 examples: 4/(4+1) = 0.8)

Result:
  - New principle added to principleNodes
  - Inferred edge added to inferredEdges
  - Principle can be applied to new contract types
```

### Example 4: Abductive Inference - Explaining Legal Patterns

```
Input:
  Observations:
    - Multiple laws require "reasonable person" standard
    - Negligence law uses reasonable person test
    - Contract law uses reasonable expectation
    - Delict law uses reasonable foreseeability

Operation: AbductiveInference
  - observations: {negligence_reasonable, contract_reasonable, delict_reasonable}
  - hypothesis: "Reasonable Person Principle"
  
Process:
  1. Hypothesize general principle that explains all observations
  2. Calculate explanatory power: 0.9 (explains most legal contexts)
  3. Create principle node:
      - nodeType: principle
      - content: "Legal standards should be based on what a reasonable person 
                 would do or expect in similar circumstances"
      - inferenceLevel: 1
  4. Create abductive edge:
      - relationType: supports
      - inferenceType: abductive
      - confidence: 0.9 * 0.7 = 0.63

Result:
  - Principle explains observed pattern
  - Lower confidence than deductive or inductive inference
  - Can be tested against new cases
```

### Example 5: Querying Inference Paths

```
Operation: TraceInferencePath
  - startNode: "sa_civil_contract-valid"
  - endNode: "za_general_contract_formation_principle"

Process:
  1. Find path through edges:
      sa_civil_contract-valid 
        → (generalizes edge, inductive)
      → za_general_contract_formation_principle
  
  2. Return path with inference metadata

Result:
  Path: [
    (sa_civil_contract-valid, civil_generalization_edge),
    (za_general_contract_formation_principle, null)
  ]
  Confidence: 0.8 (from inductive inference)
  Inference type: inductive
```

## Conclusion

This Z++ formal specification provides a rigorous foundation for:

1. **Legal Framework Representation**: Formalizes how legal frameworks are structured as hypergraphs
2. **Inference Models**: Defines four primary models for legal reasoning (deductive, inductive, abductive, analogical)
3. **Principle Discovery**: Enables systematic inference of general principles from enumerated laws
4. **Verification**: Provides invariants and pre/post-conditions for validation
5. **Traceability**: Supports tracking how principles were derived from laws

The specification supports the implementation of legal reasoning systems that can:
- Load and structure legal frameworks from the lex/ directory
- Automatically discover relationships between legal principles
- Infer general principles from specific laws
- Validate legal reasoning with formal guarantees
- Query and navigate complex legal relationships

## References

1. Spivey, J. M. (1992). *The Z Notation: A Reference Manual*. Prentice Hall.
2. Duke, R., Rose, G., & Smith, G. (1995). *Object-Z Specification Language*. Computer Standards & Interfaces.
3. Bench-Capon, T., & Prakken, H. (2010). *Using Argument Schemes for Hypothetical Reasoning in Law*. Artificial Intelligence and Law.
4. Sartor, G. (2005). *Legal Reasoning: A Cognitive Approach to the Law*. Springer.
5. Prakken, H., & Sartor, G. (2015). *Law and Logic: A Review from an Argumentation Perspective*. Artificial Intelligence.
