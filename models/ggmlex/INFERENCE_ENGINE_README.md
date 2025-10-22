# Inference Engine for Legal Principles

## Overview

The Inference Engine processes lex scheme expressions to derive general legal principles at different inference levels. It implements four primary inference models to transform enumerated laws into higher-order abstractions.

## Inference Hierarchy

```
Level 0: Enumerated Laws
         ↓ (Inductive/Abductive inference)
Level 1: First-order Principles
         ↓ (Further inference)
Level 2: Meta-principles
         ↓
Level N: Higher abstractions
```

### Levels Explained

- **Level 0 (Enumerated Laws)**: Laws directly stated in `lex/*.scm` files
  - Example: "Criminal law requires mens rea"
  - Confidence: 1.0 (stated explicitly)

- **Level 1 (First-Order Principles)**: Generalizations from multiple Level 0 laws
  - Example: "Legal standards use reasonable person test"
  - Confidence: 0.7-0.95 (depends on number of supporting laws)

- **Level 2 (Meta-Principles)**: Higher abstractions explaining Level 1 principles
  - Example: "Legal liability requires mental culpability for fairness"
  - Confidence: 0.5-0.8 (explanatory hypotheses)

## Inference Models

### 1. Deductive Inference

**Purpose**: Apply general principles to specific cases

**Confidence**: 0.9-1.0 (high)

**Example**:
```python
from models.ggmlex.hypergraphql import InferenceEngine, InferenceType

# General principle (Level 1)
general = LegalNode(
    name="All contracts require consideration",
    inference_level=1,
    confidence=0.95
)

# Specific case (Level 0)
specific = LegalNode(
    name="Employment agreement X",
    inference_level=0
)

# Apply deduction
engine = InferenceEngine()
result = engine.infer_principles(
    [general, specific],
    InferenceType.DEDUCTIVE,
    target_level=1
)
# Result: "Employment agreement X requires consideration"
# Confidence: 0.95
```

### 2. Inductive Inference

**Purpose**: Generalize from multiple specific laws to form principles

**Confidence**: n/(n+1), capped at 0.95 (increases with examples)

**Example**:
```python
# Multiple laws with common pattern
laws = [
    LegalNode(name="Civil law uses reasonable person standard"),
    LegalNode(name="Criminal law uses reasonable foresight"),
    LegalNode(name="Contract law uses reasonable interpretation"),
    LegalNode(name="Delict law uses reasonable conduct")
]

# Perform induction
result = engine.infer_principles(
    laws,
    InferenceType.INDUCTIVE,
    target_level=1
)
# Result: "Legal standards are based on reasonable person test"
# Confidence: 4/(4+1) = 0.80
```

### 3. Abductive Inference

**Purpose**: Hypothesize best explanation for observed patterns

**Confidence**: 0.5-0.8 (based on explanatory power, coherence, simplicity)

**Example**:
```python
# Observations across legal branches
observations = [
    LegalNode(name="Criminal law requires mens rea"),
    LegalNode(name="Contract law requires intent"),
    LegalNode(name="Delict law requires fault"),
    LegalNode(name="Administrative law requires rationality")
]

# Find best explanation
result = engine.infer_principles(
    observations,
    InferenceType.ABDUCTIVE,
    target_level=2
)
# Result: "Legal liability requires mental culpability for fairness"
# Confidence: ~0.55 (abductive hypothesis)
```

### 4. Analogical Inference

**Purpose**: Transfer principles from one domain to another by similarity

**Confidence**: similarity × source_confidence × 0.9

**Example**:
```python
# Source principle from contract law
source = LegalNode(
    name="Frustration of purpose doctrine",
    metadata={"branch": "contract"},
    confidence=0.9
)

# Transfer to labour law
result = engine.infer_principles(
    [source],
    InferenceType.ANALOGICAL,
    target_level=1,
    target_domain="labour"
)
# Result: "Employment frustrated if fundamental purpose impossible"
# Confidence: 0.6 × 0.9 × 0.9 = 0.486
```

## Usage

### Basic Usage

```python
from models.ggmlex.hypergraphql import (
    HypergraphQLEngine,
    InferenceEngine,
    InferenceType
)

# Load legal framework
hypergraph = HypergraphQLEngine()

# Create inference engine
inference = InferenceEngine(hypergraph)

# Get enumerated laws (Level 0)
laws = hypergraph.get_enumerated_laws()

# Select laws with common pattern
selected_laws = [law for law in laws.nodes 
                 if "reasonable" in law.content.lower()]

# Infer principle
result = inference.infer_principles(
    source_nodes=selected_laws,
    inference_type=InferenceType.INDUCTIVE,
    target_level=1
)

# Add to hypergraph
hypergraph.add_node(result.principle)
for edge in result.supporting_edges:
    hypergraph.add_edge(edge)
```

### Query by Inference Level

```python
# Get all enumerated laws (Level 0)
level_0 = hypergraph.get_enumerated_laws()

# Get first-order principles (Level 1)
level_1 = hypergraph.get_first_order_principles()

# Get meta-principles (Level 2)
level_2 = hypergraph.get_meta_principles()

# Build complete hierarchy
hierarchy = hypergraph.build_inference_hierarchy()
for level, nodes in hierarchy.items():
    print(f"Level {level}: {len(nodes)} nodes")
```

### Trace Inference Chain

```python
# Get inference chain for a principle
chain = inference.get_inference_chain("principle_id")

# Chain shows derivation path:
# [law1, law2, law3] → principle1 → meta_principle1
for i, node in enumerate(chain):
    print(f"Level {node.inference_level}: {node.name}")
```

## Confidence Calibration

| Confidence Range | Interpretation | Typical Model |
|-----------------|----------------|---------------|
| 0.95 - 1.0 | Near certain | Deductive with verified premises |
| 0.85 - 0.95 | Very confident | Inductive with many examples |
| 0.75 - 0.85 | Confident | Inductive with few examples |
| 0.65 - 0.75 | Moderately confident | Analogical with high similarity |
| 0.55 - 0.65 | Somewhat confident | Abductive with good explanation |
| 0.45 - 0.55 | Uncertain | Weak abductive or analogical |
| < 0.45 | Not confident | Insufficient evidence |

## Model Selection Guide

```
Need to apply existing principle to case?
  → Use DEDUCTIVE inference

Have multiple similar laws?
  → Use INDUCTIVE inference

Need to explain why laws share pattern?
  → Use ABDUCTIVE inference

Want to apply principle from one domain to another?
  → Use ANALOGICAL inference
```

## Schema Extensions

The inference engine adds these fields to the schema:

### LegalNode
- `inference_level: int` - Inference level (0, 1, 2, ...)
- `inference_type: InferenceType` - How node was inferred
- `confidence: float` - Confidence score (0.0-1.0)

### LegalHyperedge
- `confidence: float` - Confidence in relationship
- `inference_type: InferenceType` - How edge was inferred

### LegalRelationType (new types)
- `INFERS_FROM` - Edge from inferred principle to source
- `GENERALIZES` - Edge from specific law to general principle

## Testing

### Quick Test
```bash
python models/ggmlex/test_inference_quick.py
```

### Full Test Suite
```bash
python models/ggmlex/test_inference_engine.py
```

### Examples
```bash
python models/ggmlex/inference_examples.py
```

## Implementation Details

### Pattern Recognition

The engine recognizes common legal patterns:

- **Reasonable Person Standard**: Keywords like "reasonable", "reasonable person"
- **Mental Element**: Keywords like "intent", "mens rea", "fault", "negligence"
- **Contract Formation**: Keywords like "offer", "acceptance", "consideration"
- **Procedural Fairness**: Keywords like "fair", "fairness", "procedural", "hearing"

### Domain Similarity

Domain similarity for analogical inference:

- Same domain: 1.0
- Same group (e.g., both civil): 0.8
- Related groups: 0.6
- Different groups: 0.4

Domain groups:
- Civil: civil, contract, delict, property
- Public: constitutional, administrative, criminal
- Specialized: labour, environmental, construction, international

## Files

- `models/ggmlex/hypergraphql/inference.py` - Inference engine implementation
- `models/ggmlex/hypergraphql/schema.py` - Updated schema with inference fields
- `models/ggmlex/hypergraphql/engine.py` - Updated engine with inference queries
- `models/ggmlex/test_inference_engine.py` - Comprehensive test suite
- `models/ggmlex/test_inference_quick.py` - Quick validation tests
- `models/ggmlex/inference_examples.py` - Usage examples

## References

See `docs/formal_specification/INFERENCE_MODELS.md` for:
- Formal specifications of inference models
- Mathematical foundations
- Confidence calculations
- Validation methods
