# Primary Models for Inference of General Principles from Enumerated Laws

## Overview

This document identifies and describes the **primary inference models** used in the AnalytiCase system to derive general legal principles from specific enumerated laws in the lex framework. These models enable automated legal reasoning and knowledge discovery.

## Table of Contents

1. [Introduction](#introduction)
2. [Model Classification](#model-classification)
3. [Primary Inference Models](#primary-inference-models)
4. [Model Selection Guide](#model-selection-guide)
5. [Implementation Mapping](#implementation-mapping)
6. [Evaluation Criteria](#evaluation-criteria)
7. [Examples](#examples)

## Introduction

### Purpose

The lex framework contains enumerated laws and legal principles across 8 legal branches (civil, criminal, constitutional, administrative, labour, environmental, construction, and international law). This document defines the models used to:

1. **Extract patterns** from enumerated laws
2. **Infer general principles** that explain multiple specific laws
3. **Discover relationships** between legal concepts
4. **Generate new legal knowledge** through formal reasoning

### Inference Hierarchy

```
Level 0: Enumerated Laws (directly stated in lex framework)
         ↓ (inference)
Level 1: First-order Principles (generalized from laws)
         ↓ (inference)
Level 2: Meta-principles (generalized from principles)
         ↓ (inference)
Level N: Higher-order abstractions
```

## Model Classification

### By Reasoning Type

| Model Type | Direction | Certainty | Use Case |
|------------|-----------|-----------|----------|
| Deductive | General → Specific | High (>0.9) | Apply known principles to new cases |
| Inductive | Specific → General | Medium (0.7-0.9) | Generalize from multiple examples |
| Abductive | Effects → Causes | Low-Medium (0.5-0.8) | Hypothesize explanatory principles |
| Analogical | Domain A → Domain B | Variable (0.6-0.9) | Transfer principles across domains |

### By Application Domain

| Domain | Primary Models | Secondary Models |
|--------|---------------|------------------|
| Contract Law | Deductive, Inductive | Analogical |
| Criminal Law | Deductive, Abductive | Inductive |
| Constitutional Law | Deductive, Abductive | Analogical |
| Case Law | Inductive, Analogical | Abductive |

## Primary Inference Models

### Model 1: Deductive Inference Model

**Type:** Top-down reasoning  
**Confidence:** High (0.8 - 1.0)  
**Complexity:** Low

#### Description

Deductive inference applies general principles to specific cases, deriving necessary conclusions. If the premises are true and the logic is valid, the conclusion must be true.

#### Formal Structure

```
Premises:
  P1: General principle (e.g., "All contracts require consideration")
  P2: Specific case (e.g., "X is a contract")
  
Conclusion:
  C: Specific application (e.g., "X requires consideration")

Confidence = min(confidence(P1), confidence(P2))
```

#### Deductive Rules

1. **Modus Ponens**
   ```
   If A → B (rule)
   And A (fact)
   Then B (conclusion)
   
   Example:
   If breach-of-contract → damages
   And breach-of-contract occurred
   Then damages are warranted
   ```

2. **Universal Instantiation**
   ```
   For all X, P(X) (universal rule)
   a is an X (specific instance)
   Therefore P(a) (conclusion)
   
   Example:
   For all contracts, offer + acceptance required
   Employment agreement is a contract
   Therefore employment agreement requires offer + acceptance
   ```

3. **Syllogism**
   ```
   If A → B
   And B → C
   Then A → C
   
   Example:
   If criminal-act → mens-rea-required
   And mens-rea-required → intent-or-negligence
   Then criminal-act → intent-or-negligence
   ```

#### Implementation

```python
def deductive_inference(general_principle: LegalNode, 
                       specific_case: LegalNode,
                       rule_type: str) -> (LegalNode, float):
    """
    Apply deductive reasoning.
    
    Args:
        general_principle: Higher-level principle node
        specific_case: Specific case or law node
        rule_type: Type of deductive rule (modus_ponens, syllogism, etc.)
    
    Returns:
        (conclusion_node, confidence)
    """
    if rule_type == "modus_ponens":
        # If general_principle applies to specific_case
        if is_applicable(general_principle, specific_case):
            conclusion = create_conclusion(general_principle, specific_case)
            confidence = min(
                general_principle.confidence,
                specific_case.confidence
            )
            return (conclusion, confidence)
    
    # ... other rule types
```

#### Advantages

- High certainty in conclusions
- Logically sound reasoning
- Easy to verify and explain
- Suitable for rule-based systems

#### Limitations

- Requires well-established general principles
- Cannot discover new principles
- Limited to what can be logically derived

### Model 2: Inductive Inference Model

**Type:** Bottom-up reasoning  
**Confidence:** Medium-High (0.7 - 0.9)  
**Complexity:** Medium

#### Description

Inductive inference generalizes from multiple specific cases to form general principles. The more supporting cases, the higher the confidence.

#### Formal Structure

```
Examples:
  E1, E2, E3, ..., En: Specific laws or cases with common pattern P
  
General Principle:
  G: All cases with characteristics similar to E1...En satisfy pattern P

Confidence = n / (n + 1)  where n = number of supporting examples
```

#### Inductive Patterns

1. **Enumerative Induction**
   ```
   Observation: Contract law requires offer + acceptance
   Observation: Sale law requires offer + acceptance
   Observation: Employment law requires offer + acceptance
   Observation: Lease law requires offer + acceptance
   
   Generalization: All contractual agreements require offer + acceptance
   Confidence: 4 / (4 + 1) = 0.80
   ```

2. **Property Induction**
   ```
   Multiple laws share property: "reasonable person standard"
   Examples:
     - Negligence: reasonable person would foresee harm
     - Contract: reasonable person would understand terms
     - Delict: reasonable person would avoid causing harm
   
   Generalization: Legal standards use reasonable person benchmark
   Confidence: 3 / (3 + 1) = 0.75
   ```

3. **Structural Induction**
   ```
   Multiple laws share structure: requirement → consequence
   Examples:
     - If actus reus + mens rea → criminal liability
     - If offer + acceptance → binding contract
     - If wrongful act + damages → delictual liability
   
   Generalization: Legal rules follow requirement → consequence pattern
   ```

#### Implementation

```python
def inductive_inference(examples: List[LegalNode],
                       pattern_matcher: Callable,
                       confidence_threshold: float = 0.7) -> (LegalNode, float):
    """
    Perform inductive inference from examples.
    
    Args:
        examples: List of specific law nodes
        pattern_matcher: Function to identify common patterns
        confidence_threshold: Minimum confidence to accept generalization
    
    Returns:
        (general_principle_node, confidence)
    """
    # Identify common pattern
    pattern = pattern_matcher(examples)
    
    if pattern is None:
        return (None, 0.0)
    
    # Calculate confidence
    n = len(examples)
    confidence = min(0.95, n / (n + 1))  # Cap at 0.95 for inductive reasoning
    
    if confidence < confidence_threshold:
        return (None, confidence)
    
    # Create general principle
    principle = create_general_principle(
        pattern=pattern,
        examples=examples,
        inference_level=max(e.inference_level for e in examples) + 1
    )
    
    return (principle, confidence)
```

#### Advantages

- Discovers new patterns and principles
- Confidence increases with more examples
- Natural fit for legal reasoning
- Handles multiple sources of evidence

#### Limitations

- Never provides absolute certainty
- Vulnerable to counterexamples
- Requires sufficient examples
- Pattern identification can be subjective

### Model 3: Abductive Inference Model

**Type:** Inference to best explanation  
**Confidence:** Medium (0.5 - 0.8)  
**Complexity:** High

#### Description

Abductive inference hypothesizes the best explanation for observed legal rules or patterns. It answers "why" questions about the law.

#### Formal Structure

```
Observations:
  O1, O2, O3, ..., On: Observed legal rules or patterns
  
Hypotheses:
  H1, H2, ..., Hm: Possible explanatory principles
  
Best Explanation:
  H*: Hypothesis that best explains all observations
  
Confidence = explanatory_power(H*) × coherence(H*) × simplicity(H*)
```

#### Abductive Criteria

1. **Explanatory Power**
   ```
   How well does the hypothesis explain the observations?
   
   Example:
   Observations: 
     - Criminal law requires mens rea
     - Contract law requires intent
     - Tort law requires fault
   
   Hypothesis: "Law requires mental element for liability"
   Explanatory power: 1.0 (explains all observations)
   ```

2. **Coherence**
   ```
   How well does the hypothesis fit with existing legal framework?
   
   Coherence score = overlap with established principles / total principles
   ```

3. **Simplicity (Occam's Razor)**
   ```
   Prefer simpler explanations with fewer assumptions
   
   Simplicity score = 1 / (number of required assumptions)
   ```

4. **Predictive Value**
   ```
   Can the hypothesis predict outcomes in new cases?
   
   Predictive score = correct predictions / total predictions
   ```

#### Implementation

```python
def abductive_inference(observations: List[LegalNode],
                       hypothesis_generator: Callable,
                       evaluator: Callable) -> (LegalNode, float):
    """
    Perform abductive inference to find best explanation.
    
    Args:
        observations: Observed legal rules or patterns
        hypothesis_generator: Function to generate candidate hypotheses
        evaluator: Function to evaluate hypothesis quality
    
    Returns:
        (best_hypothesis_node, confidence)
    """
    # Generate candidate hypotheses
    hypotheses = hypothesis_generator(observations)
    
    best_hypothesis = None
    best_score = 0.0
    
    for hypothesis in hypotheses:
        # Evaluate hypothesis
        explanatory_power = evaluator.explanatory_power(hypothesis, observations)
        coherence = evaluator.coherence(hypothesis)
        simplicity = evaluator.simplicity(hypothesis)
        
        # Combined score
        score = (explanatory_power * 0.5 +
                coherence * 0.3 +
                simplicity * 0.2)
        
        if score > best_score:
            best_score = score
            best_hypothesis = hypothesis
    
    # Confidence is lower for abductive reasoning
    confidence = best_score * 0.7  # Scale down for uncertainty
    
    return (best_hypothesis, confidence)
```

#### Advantages

- Generates explanatory principles
- Helps understand "why" laws exist
- Can handle incomplete information
- Useful for legal theory development

#### Limitations

- Lower confidence than deductive/inductive
- Multiple competing explanations possible
- Subjective evaluation criteria
- Computationally expensive

### Model 4: Analogical Inference Model

**Type:** Cross-domain reasoning  
**Confidence:** Variable (0.6 - 0.9)  
**Complexity:** Medium-High

#### Description

Analogical inference applies principles from one legal domain to another based on structural or functional similarities.

#### Formal Structure

```
Source Domain:
  S: Legal domain with established principle P
  
Target Domain:
  T: Legal domain without principle P
  
Similarity:
  sim(S, T): Measure of similarity between domains
  
Transfer:
  Apply P to T if sim(S, T) > threshold
  
Confidence = sim(S, T) × confidence(P in S)
```

#### Similarity Measures

1. **Structural Similarity**
   ```
   Compare logical structure of laws
   
   Example:
   Contract law: offer + acceptance → binding agreement
   Treaty law: proposal + ratification → binding treaty
   
   Structural similarity: 0.9 (nearly identical structure)
   ```

2. **Functional Similarity**
   ```
   Compare purpose or goals
   
   Example:
   Consumer protection law: protect weaker party
   Employment law: protect weaker party (employee)
   
   Functional similarity: 0.8 (same underlying purpose)
   ```

3. **Domain Proximity**
   ```
   How related are the legal branches?
   
   Same branch: 1.0
   Related branches (civil-commercial): 0.8
   Different branches (civil-criminal): 0.4
   ```

#### Implementation

```python
def analogical_inference(source_node: LegalNode,
                        target_node: LegalNode,
                        principle: LegalNode,
                        similarity_calculator: Callable) -> (LegalNode, float):
    """
    Transfer principle from source to target by analogy.
    
    Args:
        source_node: Source domain where principle is established
        target_node: Target domain for principle transfer
        principle: Principle to transfer
        similarity_calculator: Function to calculate domain similarity
    
    Returns:
        (transferred_principle_node, confidence)
    """
    # Calculate similarity
    similarity = similarity_calculator(source_node, target_node)
    
    if similarity < 0.6:  # Threshold for analogy
        return (None, 0.0)
    
    # Transfer principle
    transferred_principle = create_analogical_principle(
        source=source_node,
        target=target_node,
        original_principle=principle
    )
    
    # Confidence based on similarity and source confidence
    confidence = similarity * principle.confidence * 0.9  # Slight discount for transfer
    
    return (transferred_principle, confidence)
```

#### Advantages

- Enables cross-domain knowledge transfer
- Leverages existing legal knowledge
- Identifies novel applications of principles
- Supports legal innovation

#### Limitations

- Analogies may be imperfect
- Requires careful similarity assessment
- Can lead to inappropriate transfers
- Needs domain expertise validation

## Model Selection Guide

### Decision Tree

```
Start: Need to infer legal principle

Question 1: Do you have a general principle to apply?
  YES → Use DEDUCTIVE inference
  NO → Continue to Question 2

Question 2: Do you have multiple similar specific laws?
  YES → Use INDUCTIVE inference
  NO → Continue to Question 3

Question 3: Do you need to explain observed patterns?
  YES → Use ABDUCTIVE inference
  NO → Continue to Question 4

Question 4: Can you apply principle from similar domain?
  YES → Use ANALOGICAL inference
  NO → Collect more data or combine multiple models
```

### Use Case Matrix

| Scenario | Primary Model | Secondary Model | Confidence Range |
|----------|---------------|-----------------|------------------|
| Apply statute to case | Deductive | - | 0.9 - 1.0 |
| Generalize from cases | Inductive | Abductive | 0.7 - 0.9 |
| Understand legal policy | Abductive | Inductive | 0.5 - 0.8 |
| Transfer contract principle to treaty | Analogical | Deductive | 0.6 - 0.9 |
| Predict case outcome | Deductive + Inductive | Analogical | 0.7 - 0.95 |
| Discover new principle | Inductive + Abductive | - | 0.6 - 0.8 |

## Implementation Mapping

### Current Implementation

| Component | File | Models Supported |
|-----------|------|------------------|
| HypergraphQL Engine | `models/ggmlex/hypergraphql/engine.py` | All (basic support) |
| Legal Schema | `models/ggmlex/hypergraphql/schema.py` | Schema definitions |
| Inference Operations | To be implemented | Deductive, Inductive |
| Similarity Metrics | To be implemented | Analogical |
| Explanation Generator | To be implemented | Abductive |

### Recommended Implementation

```python
# File: models/ggmlex/hypergraphql/inference.py

class InferenceEngine:
    """Engine for legal inference operations."""
    
    def __init__(self, hypergraph: LexHypergraph):
        self.hypergraph = hypergraph
        self.deductive_reasoner = DeductiveReasoner()
        self.inductive_reasoner = InductiveReasoner()
        self.abductive_reasoner = AbductiveReasoner()
        self.analogical_reasoner = AnalogicalReasoner()
    
    def infer(self, 
              sources: List[LegalNode],
              inference_type: InferenceType,
              **kwargs) -> InferenceResult:
        """
        Perform inference using specified model.
        
        Args:
            sources: Source nodes for inference
            inference_type: Type of inference to perform
            **kwargs: Model-specific parameters
        
        Returns:
            InferenceResult with conclusion and confidence
        """
        if inference_type == InferenceType.DEDUCTIVE:
            return self.deductive_reasoner.infer(sources, **kwargs)
        elif inference_type == InferenceType.INDUCTIVE:
            return self.inductive_reasoner.infer(sources, **kwargs)
        elif inference_type == InferenceType.ABDUCTIVE:
            return self.abductive_reasoner.infer(sources, **kwargs)
        elif inference_type == InferenceType.ANALOGICAL:
            return self.analogical_reasoner.infer(sources, **kwargs)
```

## Evaluation Criteria

### Confidence Calibration

| Confidence Range | Interpretation | Typical Model |
|------------------|----------------|---------------|
| 0.95 - 1.0 | Near certain | Deductive with verified premises |
| 0.85 - 0.95 | Very confident | Inductive with many examples |
| 0.75 - 0.85 | Confident | Inductive with few examples |
| 0.65 - 0.75 | Moderately confident | Analogical with high similarity |
| 0.55 - 0.65 | Somewhat confident | Abductive with good explanation |
| 0.45 - 0.55 | Uncertain | Weak abductive or analogical |
| < 0.45 | Not confident | Insufficient evidence |

### Validation Methods

1. **Cross-validation**
   - Hold out some enumerated laws
   - Infer principles from remaining laws
   - Check if held-out laws are consistent with inferred principles

2. **Expert Review**
   - Legal experts validate inferred principles
   - Check against established legal theory
   - Verify practical applicability

3. **Consistency Check**
   - Ensure inferred principles don't conflict with existing framework
   - Check for logical contradictions
   - Verify coherence across branches

4. **Predictive Testing**
   - Use inferred principles to predict legal outcomes
   - Compare predictions with actual case outcomes
   - Measure accuracy and calibration

## Examples

### Example 1: Deductive Inference in Contract Law

```
General Principle (Level 1):
  "All contracts require consideration"
  (Inferred from multiple contract laws)
  Confidence: 0.95

Specific Case:
  "Employment agreement X"
  Type: Contract
  Confidence: 1.0

Deductive Inference:
  Application: Employment agreement X requires consideration
  Method: Modus Ponens
  Confidence: min(0.95, 1.0) = 0.95
  
Conclusion:
  Create node: "Employment agreement X requires consideration"
  Create edge: X → consideration requirement
  Edge type: applies_to
  Inference type: deductive
```

### Example 2: Inductive Inference Across Branches

```
Enumerated Laws (Level 0):
  1. Civil law: reasonable-person-standard for negligence
  2. Criminal law: reasonable-person would foresee harm
  3. Contract law: reasonable-person interpretation
  4. Delict law: reasonable-person causation test
  5. Employment law: reasonable-employer standard

Common Pattern:
  All use "reasonable person" or similar standard

Inductive Inference:
  Generalization: "Legal standards are based on reasonable person test"
  Method: Enumerative induction
  Confidence: 5 / (5 + 1) = 0.833
  Inference level: 1
  
Conclusion:
  Create principle node: "Reasonable Person Principle"
  Create edges: Each enumerated law → principle
  Edge type: generalizes
  Inference type: inductive
```

### Example 3: Abductive Inference for Legal Policy

```
Observations (Level 0):
  1. Criminal law requires intent (mens rea)
  2. Contract law requires meeting of minds
  3. Delict law requires fault
  4. Administrative law requires rational decision

Pattern:
  All require mental/intentional element

Abductive Hypothesis:
  "Legal liability requires mental culpability to be fair"
  
Evaluation:
  Explanatory power: 0.9 (explains most observations)
  Coherence: 0.8 (fits with fairness principles)
  Simplicity: 0.7 (one central concept)
  
Confidence Calculation:
  Base score: (0.9 × 0.5) + (0.8 × 0.3) + (0.7 × 0.2) = 0.83
  Abductive discount: 0.83 × 0.7 = 0.581
  
Conclusion:
  Create principle node: "Mental Culpability Principle"
  Create edges: Observations → principle
  Edge type: supports
  Inference type: abductive
  Confidence: 0.58
```

### Example 4: Analogical Inference Between Branches

```
Source Domain: Contract Law
  Principle: "Frustration of purpose doctrine"
  Content: "Contract discharged if fundamental purpose frustrated"
  Confidence: 0.9

Target Domain: Employment Law
  Context: Employment relationships

Similarity Analysis:
  Structural: Both involve ongoing obligations (0.8)
  Functional: Both protect reasonable expectations (0.9)
  Domain proximity: Related (civil law branches) (0.8)
  
Overall Similarity: (0.8 + 0.9 + 0.8) / 3 = 0.833

Analogical Transfer:
  Transferred Principle: "Employment frustrated if fundamental purpose impossible"
  Confidence: 0.833 × 0.9 × 0.9 = 0.675
  
Conclusion:
  Create principle node in employment law
  Create edge: contract principle → employment principle
  Edge type: applies_to
  Inference type: analogical
  
Requires Validation:
  - Legal expert review
  - Case law analysis
  - Statutory interpretation
```

## Conclusion

The four primary inference models provide a comprehensive framework for deriving general legal principles from enumerated laws:

1. **Deductive Inference**: High-confidence application of established principles
2. **Inductive Inference**: Pattern discovery and generalization from examples
3. **Abductive Inference**: Explanatory hypothesis generation
4. **Analogical Inference**: Cross-domain knowledge transfer

These models, working together, enable the AnalytiCase system to:
- Automatically discover legal patterns
- Build hierarchical knowledge structures
- Support legal reasoning and decision-making
- Facilitate legal research and analysis

The formal specifications in [LEX_HYPERGRAPH_SPEC.md](LEX_HYPERGRAPH_SPEC.md) provide the mathematical foundation, while this document provides the practical guidance for implementation and application.

## References

1. Prakken, H., & Sartor, G. (2015). Law and Logic: A Review from an Argumentation Perspective. *Artificial Intelligence*, 227, 214-245.
2. Bench-Capon, T. (2020). Representing Popov v Hayashi with Dimensions and Factors. *Artificial Intelligence and Law*, 28, 89-117.
3. Walton, D. (2014). *Abductive Reasoning*. University of Alabama Press.
4. Ashley, K. D. (2017). *Artificial Intelligence and Legal Analytics*. Cambridge University Press.
5. Holyoak, K. J., & Thagard, P. (1995). *Mental Leaps: Analogy in Creative Thought*. MIT Press.
