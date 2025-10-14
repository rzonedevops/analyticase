# GGMLEX - GGML-based ML Framework with HypergraphQL

GGMLEX is a comprehensive machine learning framework designed for legal document analysis, combining GGML (Georgi Gerganov Machine Learning) tensor operations with HypergraphQL for complex legal relationship querying.

## Overview

This framework provides:

- **GGML Python Bindings**: Efficient tensor operations for ML models
- **Legal LLM**: Large language model optimized for legal text
- **Legal Transformers**: Transformer architectures for legal document processing
- **HypergraphQL**: Query engine for legal framework relationships
- **LlamaLex.cpp**: C++ inference engine for high-performance legal text processing

## Architecture

```
ggmlex/
├── __init__.py              # Main module interface
├── ggml.py                  # GGML tensor operations
├── llm.py                   # Legal LLM implementation
├── transformers.py          # Transformer models
├── cpp/                     # C++ implementation
│   └── llamalex.cpp         # LlamaLex inference engine
└── hypergraphql/            # HypergraphQL module
    ├── __init__.py
    ├── schema.py            # Legal schema definitions
    ├── engine.py            # Query engine
    └── hypergraphql_example.py  # Usage examples
```

## Components

### 1. GGML Module (`ggml.py`)

Provides Python bindings for GGML tensor operations:

- `GGMLTensor`: Tensor data structure
- `GGMLContext`: Context manager for tensor operations
- Matrix operations (matmul, add, layer_norm, softmax)
- Attention mechanism implementation

**Example:**
```python
from models.ggmlex import GGMLContext

with GGMLContext() as ctx:
    a = ctx.create_tensor("tensor_a", (3, 4))
    b = ctx.create_tensor("tensor_b", (4, 5))
    c = ctx.matmul(a, b)
```

### 2. Legal LLM (`llm.py`)

Large language model for legal document analysis:

- `LegalTokenizer`: Tokenizer with legal vocabulary
- `LegalLLM`: LLM optimized for legal text
- Support for case law, statutes, contracts, and legal briefs
- Document encoding and analysis capabilities

**Example:**
```python
from models.ggmlex import LegalLLM, LegalDocument

llm = LegalLLM()
doc = LegalDocument(
    text="The court held that the contract was valid.",
    doc_type="case_law"
)
embeddings = llm.encode(doc)
analysis = llm.analyze_case(doc.text)
```

### 3. Legal Transformers (`transformers.py`)

Transformer models for legal text processing:

- `MultiHeadAttention`: Multi-head attention mechanism
- `FeedForward`: Feed-forward network
- `TransformerLayer`: Complete transformer layer
- `LegalTransformer`: Full transformer model for legal documents

**Example:**
```python
from models.ggmlex import LegalTransformer, TransformerConfig

config = TransformerConfig(
    vocab_size=50000,
    embedding_dim=768,
    num_layers=12
)
transformer = LegalTransformer(config)
analysis = transformer.analyze_legal_text("The plaintiff sued for breach...")
```

### 4. HypergraphQL (`hypergraphql/`)

Query engine for legal framework relationships:

#### Schema Definition (`schema.py`)

- `LegalNodeType`: Defines types of legal entities (statute, case, principle, etc.)
- `LegalRelationType`: Defines relationships (cites, interprets, overrules, etc.)
- `LegalNode`: Represents legal entities in the hypergraph
- `LegalHyperedge`: Represents relationships between entities
- `LegalSchema`: Schema validation and constraints

#### Query Engine (`engine.py`)

- `HypergraphQLEngine`: Main query engine
- Node and edge management
- Graph traversal and querying
- Integration with lex/ legal framework
- Pattern matching and path finding

**Example:**
```python
from models.ggmlex import HypergraphQLEngine, LegalNode, LegalNodeType

# Initialize engine (loads from lex/ directory)
engine = HypergraphQLEngine()

# Query nodes
result = engine.query_nodes(
    node_type=LegalNodeType.CASE,
    jurisdiction="za"
)

# Query neighbors
result = engine.query_neighbors(
    node_id="statute_001",
    relation_type=LegalRelationType.CITES
)

# Find path between entities
result = engine.query_path("case_001", "statute_001")
```

### 5. LlamaLex C++ Engine (`cpp/llamalex.cpp`)

High-performance C++ inference engine:

- Optimized for legal document processing
- Memory-efficient inference
- C interface for Python bindings
- Support for long-form legal documents

**Building:**
```bash
# Compile (requires C++11 or later)
g++ -std=c++11 -O3 cpp/llamalex.cpp -o llamalex

# Run example
./llamalex
```

## Integration with Legal Framework

GGMLEX integrates with the legal framework in `lex/` directory:

- Automatically loads legal definitions from `lex/civ/za/south_african_civil_law.scm`
- Parses Scheme-based legal rules and principles
- Creates hypergraph nodes for each legal entity
- Enables querying of legal relationships

**Supported Legal Areas:**
- Contract Law
- Delict Law (Tort Law)
- Property Law
- Family Law
- Labour Law
- Constitutional Law
- Evidence Law
- Procedural Law

## Usage Examples

### Example 1: Basic HypergraphQL Queries

```python
from models.ggmlex.hypergraphql import HypergraphQLEngine

# Initialize and load legal framework
engine = HypergraphQLEngine()

# Query legal principles
result = engine.query_nodes(node_type=LegalNodeType.PRINCIPLE)
for node in result.nodes:
    print(f"{node.name}: {node.content[:80]}...")

# Search by content
result = engine.query_by_content("contract")
print(f"Found {len(result)} nodes mentioning 'contract'")
```

### Example 2: Legal Document Analysis

```python
from models.ggmlex import LegalLLM, LegalTransformer

# Using LegalLLM
llm = LegalLLM()
analysis = llm.analyze_case("""
    The court found that the defendant breached the contract
    by failing to deliver the goods on the agreed date.
""")
print(analysis)

# Using Transformer
transformer = LegalTransformer()
analysis = transformer.analyze_legal_text("""
    Section 9 of the Constitution guarantees equality before the law.
""")
print(analysis)
```

### Example 3: Case Law Network Analysis

```python
from models.ggmlex.hypergraphql import (
    HypergraphQLEngine, LegalNode, LegalHyperedge,
    LegalNodeType, LegalRelationType
)

engine = HypergraphQLEngine()

# Create case nodes
case1 = LegalNode(
    node_id="case_001",
    node_type=LegalNodeType.CASE,
    name="Smith v. Jones",
    jurisdiction="za"
)
engine.add_node(case1)

# Create precedent relationship
edge = LegalHyperedge(
    edge_id="edge_001",
    relation_type=LegalRelationType.FOLLOWS,
    nodes={"case_001", "case_002"}
)
engine.add_edge(edge)

# Query precedent chain
result = engine.query_neighbors("case_001", max_hops=3)
```

## Running Examples

To run the comprehensive examples:

```bash
cd /home/runner/work/analyticase/analyticase
python models/ggmlex/hypergraphql/hypergraphql_example.py
```

This will demonstrate:
1. Basic HypergraphQL queries
2. Contract law framework queries
3. Case law precedent network analysis
4. Integration with lex/ directory

## Testing

Test individual components:

```bash
# Test GGML operations
python models/ggmlex/ggml.py

# Test Legal LLM
python models/ggmlex/llm.py

# Test Transformers
python models/ggmlex/transformers.py

# Test HypergraphQL
python models/ggmlex/hypergraphql/engine.py
python models/ggmlex/hypergraphql/schema.py
```

## Future Enhancements

- [ ] Load pretrained legal language models
- [ ] Support for more legal jurisdictions
- [ ] Enhanced Scheme parser for legal rules
- [ ] GGML C library integration for better performance
- [ ] GraphQL API for remote querying
- [ ] Integration with ZA Judiciary systems
- [ ] Support for legal reasoning and inference
- [ ] Multi-lingual legal document support

## Dependencies

- NumPy: Numerical operations
- Python 3.8+: Core language
- (Optional) GGML C library: For optimized operations
- (Optional) g++: For building C++ inference engine

## License

This module is part of the AnalytiCase framework and follows the same license.

## References

- GGML: https://github.com/ggerganov/ggml
- LLaMA: Large Language Model Meta AI
- HypergraphQL: Query language for hypergraphs
- South African Legal Framework: lex/civ/za/

## Contact

For questions or contributions, please refer to the main AnalytiCase repository.
