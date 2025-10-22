# Z++ Notation Quick Reference

This document provides a quick reference for the Z++ notation used in the AnalytiCase formal specification.

## Table of Contents

1. [Basic Z Notation](#basic-z-notation)
2. [Z++ Object-Oriented Extensions](#z-object-oriented-extensions)
3. [Schemas](#schemas)
4. [Logic and Predicates](#logic-and-predicates)
5. [Common Patterns](#common-patterns)

## Basic Z Notation

### Sets

| Notation | Meaning | Example |
|----------|---------|---------|
| `{x, y, z}` | Set enumeration | `{1, 2, 3}` |
| `∅` | Empty set | Empty collection |
| `∈` | Element of | `x ∈ S` (x is in set S) |
| `∉` | Not element of | `x ∉ S` (x is not in S) |
| `⊆` | Subset | `A ⊆ B` (A is subset of B) |
| `∪` | Union | `A ∪ B` |
| `∩` | Intersection | `A ∩ B` |
| `\` | Set difference | `A \ B` (elements in A but not B) |
| `℘(S)` or `power S` | Power set | All subsets of S |
| `#S` | Cardinality | Number of elements in S |
| `⋃` | Distributed union | Union of all sets in a collection |

### Numbers

| Notation | Meaning |
|----------|---------|
| `ℕ` or `nat` | Natural numbers {0, 1, 2, ...} |
| `ℤ` | Integers {..., -1, 0, 1, ...} |
| `ℝ` or `real` | Real numbers |
| `ℕ₁` | Positive natural numbers {1, 2, 3, ...} |

### Relations and Functions

| Notation | Meaning | Example |
|----------|---------|---------|
| `A ↔ B` | Relation | `NODEID ↔ Node` |
| `A ⇸ B` | Partial function | `NODEID ⇸ Node` (not all mapped) |
| `A → B` | Total function | Every element of A mapped to B |
| `A ⤖ B` | Injection | One-to-one mapping |
| `A ↠ B` | Surjection | Onto mapping |
| `A ⤕ B` | Bijection | One-to-one and onto |
| `dom f` | Domain | `{x | ∃y • (x, y) ∈ f}` |
| `ran f` | Range | `{y | ∃x • (x, y) ∈ f}` |
| `f(x)` | Function application | Value of f at x |
| `{x ↦ y}` | Maplet | Single mapping x to y |

### Sequences

| Notation | Meaning | Example |
|----------|---------|---------|
| `seq A` | Sequences over A | Ordered lists |
| `⟨⟩` | Empty sequence | No elements |
| `⟨x, y, z⟩` | Sequence | Ordered list |
| `s ⌢ t` or `s ++ t` | Concatenation | Join sequences |
| `head s` | First element | First item |
| `tail s` | Rest | All but first |
| `#s` | Length | Number of elements |
| `s(i)` | Indexing | Element at position i |

### Logic

| Notation | Meaning | Example |
|----------|---------|---------|
| `∧` | And | `P ∧ Q` |
| `∨` | Or | `P ∨ Q` |
| `¬` | Not | `¬P` |
| `⇒` | Implies | `P ⇒ Q` |
| `⇔` or `iff` | If and only if | `P ⇔ Q` |
| `∀` | For all | `∀x: S • P(x)` |
| `∃` | There exists | `∃x: S • P(x)` |
| `∃!` | Unique existence | `∃!x: S • P(x)` |

### Schema Operators

| Notation | Meaning |
|----------|---------|
| `Δ S` | Change of state | Before and after (S and S') |
| `Ξ S` | No change | All variables unchanged (S = S') |
| `S'` | After state | Primed variables |

## Z++ Object-Oriented Extensions

### Class Definition

```
class ClassName
  attribute1: Type1
  attribute2: Type2
where
  invariant1
  invariant2
end
```

**Example:**
```
class Node
  nodeId: NODEID
  nodeType: NODETYPE
  embedding: seq ℝ
where
  #embedding > 0
end
```

### Inheritance

```
class DerivedClass extends BaseClass
  newAttribute: Type
where
  additional_invariants
end
```

### Object Creation

```
schema CreateObject
  Δ ClassName
  input?: Type
where
  preconditions
  postconditions
end
```

## Schemas

### Basic Schema Structure

```
schema SchemaName
  declarations
where
  predicates
end
```

**Example:**
```
schema AddNode
  Δ Hypergraph
  node?: Node
where
  node?.nodeId ∉ dom nodes
  nodes' = nodes ∪ {node?.nodeId ↦ node?}
end
```

### Schema Components

| Component | Purpose |
|-----------|---------|
| **Declaration part** | Declare variables and their types |
| **Predicate part** | State constraints and conditions |
| **?** suffix | Input variable |
| **!** suffix | Output variable |
| **'** suffix | After-state variable |

### State Schemas

```
schema State
  variable1: Type1
  variable2: Type2
where
  invariant1
  invariant2
end
```

### Operation Schemas

```
schema OperationName
  Δ State  // or Ξ State for read-only
  inputs?: InputTypes
  outputs!: OutputTypes
where
  preconditions
  postconditions
end
```

## Logic and Predicates

### Quantification

**Universal quantification:**
```
∀ x: Type • predicate(x)
```
Example: `∀ n: dom nodes • n ∈ dom nodeToEdges`

**Existential quantification:**
```
∃ x: Type • predicate(x)
```
Example: `∃ e: dom hyperedges • n ∈ hyperedges(e).nodes`

**Set comprehension:**
```
{x: Type | condition • expression}
```
Example: `{n: dom nodes | #nodeToEdges(n) > 2 • n}`

### Conditionals

**Implication:**
```
P ⇒ Q
```
Example: `status = completed ⇒ #events > 0`

**If-and-only-if:**
```
P ⇔ Q
```
Example: `eFilingEnabled = true ⇔ eFilingStatus = enabled`

## Common Patterns

### Adding to a Set

```
set' = set ∪ {element}
```

### Removing from a Set

```
set' = set \ {element}
```

### Updating a Function/Map

```
function' = function ⊕ {key ↦ value}
```
(Override: add or update mapping)

### Function Composition

```
f ∘ g
```
Apply g then f

### Range Restriction

```
S ◁ f  // Domain restriction
f ▷ S  // Range restriction
S ⩤ f  // Domain subtraction
f ⩥ S  // Range subtraction
```

### Distributed Operations

**Distributed union:**
```
⋃ {set1, set2, set3} = set1 ∪ set2 ∪ set3
```

**Sum:**
```
∑ {1, 2, 3} = 6
```

**Product:**
```
∏ {2, 3, 4} = 24
```

### Sequence Operations

**Append:**
```
seq' = seq ⌢ ⟨element⟩
```

**Filter:**
```
seq ↾ predicate
```

**Map over sequence:**
```
⟨| expression | x: seq •⟩
```

## Mathematical Symbols Reference

### Set Theory

- `∈` - element of
- `∉` - not element of
- `⊆` - subset
- `⊂` - proper subset
- `∪` - union
- `∩` - intersection
- `\` - difference
- `℘` - power set
- `×` - cartesian product
- `∅` - empty set
- `⋃` - distributed union
- `⋂` - distributed intersection

### Functions

- `→` - total function
- `⇸` - partial function (pfun)
- `↣` - total injection
- `⤔` - partial injection
- `↠` - total surjection
- `⤀` - partial surjection
- `⤖` - bijection
- `⊕` - function override
- `↦` - maplet

### Logic

- `∧` - and
- `∨` - or
- `¬` - not
- `⇒` - implies
- `⇔` - iff (if and only if)
- `∀` - for all
- `∃` - there exists
- `∃!` - exists unique
- `⊤` - true
- `⊥` - false

### Numbers

- `ℕ` - natural numbers
- `ℤ` - integers
- `ℝ` - real numbers
- `≤` - less than or equal
- `≥` - greater than or equal
- `<` - less than
- `>` - greater than

### Sequences

- `seq` - sequence type
- `⟨⟩` - empty sequence
- `⟨x⟩` - singleton sequence
- `⌢` - concatenation
- `↾` - sequence filter
- `↿` - domain restriction
- `⤏` - range restriction

### Schema Calculus

- `Δ` - delta (state change)
- `Ξ` - xi (no state change)
- `'` - prime (after state)
- `?` - input decoration
- `!` - output decoration

## Examples

### Example 1: Set Operations

```
Given:
  A = {1, 2, 3}
  B = {2, 3, 4}

Then:
  A ∪ B = {1, 2, 3, 4}
  A ∩ B = {2, 3}
  A \ B = {1}
  #A = 3
  2 ∈ A = true
  5 ∉ A = true
```

### Example 2: Function Definition

```
nodes: NODEID ⇸ Node

Means:
  - nodes is a partial function
  - Maps NODEID to Node
  - Not all NODEIDs need to be mapped

Example:
  nodes = {n1 ↦ Node1, n2 ↦ Node2}
  dom nodes = {n1, n2}
  ran nodes = {Node1, Node2}
  nodes(n1) = Node1
```

### Example 3: Quantification

```
∀ e: dom hyperedges • hyperedges(e).nodes ⊆ dom nodes

Means:
  For every hyperedge e in the domain of hyperedges,
  the nodes of that hyperedge are a subset of all nodes
```

### Example 4: State Change

```
schema AddDocument
  Δ LegalCase
  doc?: FILEPATH
where
  doc? ∉ documents
  documents' = documents ∪ {doc?}
  caseId' = caseId
end

Means:
  - Input: a filepath doc?
  - Precondition: doc is not already in documents
  - Postcondition: documents now includes doc
  - caseId remains unchanged
```

### Example 5: Invariant

```
class CaseLinesBundle
  totalPages: ℕ
  documents: seq Document
where
  totalPages = ∑{d: ran documents • d.pageCount}
end

Means:
  - totalPages must always equal the sum of page counts
  - This is checked after every operation
```

## Tips for Reading Z++ Specifications

1. **Read declarations first**: Understand what variables exist and their types
2. **Check invariants**: These must always be true
3. **Identify inputs/outputs**: Variables with ? are inputs, ! are outputs
4. **Trace state changes**: Primed (') variables are after-state
5. **Check preconditions**: Conditions that must be true before operation
6. **Check postconditions**: What changes after operation
7. **Look for Δ vs Ξ**: Δ means state changes, Ξ means read-only

## Additional Resources

- **Z Notation Reference**: Spivey, J.M. "The Z Notation: A Reference Manual"
- **Object-Z**: Duke, R., et al. "Object-Z: A Specification Language"
- **Tutorial**: "Using Z: Specification, Refinement, and Proof" by Woodcock & Davies
- **Online Tools**: CZT (Community Z Tools) for type checking

## LaTeX Packages for Z Notation

When compiling the LaTeX specification:

```latex
\usepackage{zed-csp}  % Z notation support
\usepackage{amsmath}  % Mathematical symbols
\usepackage{amssymb}  % Additional symbols
```

Alternative packages:
- `\usepackage{z-eves}` - Z/EVES theorem prover style
- `\usepackage{fuzz}` - Fuzz type checker style
- `\usepackage{oz}` - Object-Z support

## Converting Between Notations

### ASCII to Mathematical

When writing specifications in plain text:

| ASCII | Symbol | Meaning |
|-------|--------|---------|
| `/in` | `∈` | element of |
| `/notin` | `∉` | not element of |
| `\subseteq` | `⊆` | subset |
| `\cup` | `∪` | union |
| `\cap` | `∩` | intersection |
| `\forall` | `∀` | for all |
| `\exists` | `∃` | there exists |
| `\implies` | `⇒` | implies |
| `\iff` | `⇔` | if and only if |
| `\land` | `∧` | and |
| `\lor` | `∨` | or |
| `\neg` | `¬` | not |

### Unicode Support

Most modern editors support direct Unicode input of mathematical symbols. This makes specifications more readable while still being processable as plain text.
