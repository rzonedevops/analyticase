# Lex Hypergraph and HyperGNN Model Enhancements

## Overview

This document describes the advanced enhancements made to the lex hypergraph query engine and the HyperGNN model, providing powerful new capabilities for legal case analysis and graph-based reasoning.

## Table of Contents

1. [Lex Hypergraph Query Enhancements](#lex-hypergraph-query-enhancements)
2. [Visualization Utilities](#visualization-utilities)
3. [Temporal Hypergraph Analysis](#temporal-hypergraph-analysis)
4. [Attention-Based HyperGNN](#attention-based-hypergnn)
5. [Hierarchical Hypergraph Structures](#hierarchical-hypergraph-structures)
6. [Usage Examples](#usage-examples)
7. [API Reference](#api-reference)

## Lex Hypergraph Query Enhancements

### 1. Subgraph Extraction

Extract subgraphs containing specific nodes with optional neighbor expansion.

**Method**: `query_subgraph(node_ids, include_edges=True, expand_neighbors=False)`

**Features**:
- Extract specified nodes and their connections
- Optionally expand to include immediate neighbors
- Filter edges to only those within the subgraph
- Useful for focused analysis on specific legal concepts

**Example**:
```python
from models.integration import LexADIntegration

integration = LexADIntegration()
integration.generate_lex_hypergraph()

# Extract subgraph around specific legal concepts
node_ids = ["statute_001", "case_123", "principle_456"]
result = integration.lex_engine.query_subgraph(
    node_ids,
    include_edges=True,
    expand_neighbors=True  # Include direct neighbors
)

print(f"Nodes in subgraph: {len(result.nodes)}")
print(f"Edges in subgraph: {len(result.edges)}")
```

### 2. Legal Reasoning Chains

Follow DEPENDS_ON relationships to build chains of legal reasoning.

**Method**: `query_legal_reasoning_chain(start_node_id, max_depth=5)`

**Features**:
- Traces dependencies between legal concepts
- Builds inference chains showing how concepts relate
- Finds the longest reasoning path
- Returns all nodes and edges in the chain

**Example**:
```python
# Find reasoning chain starting from a specific statute
result = integration.lex_engine.query_legal_reasoning_chain(
    "statute_contract_law",
    max_depth=5
)

print(f"Reasoning chain length: {result.metadata['chain_length']}")
for node in result.nodes:
    print(f"  -> {node.name}")
```

### 3. Similar Node Discovery

Find nodes similar to a given node based on content and structure.

**Method**: `query_similar_nodes(node_id, similarity_threshold=0.3, max_results=10)`

**Features**:
- Combines multiple similarity metrics:
  - Type similarity (0.3 weight)
  - Content similarity - Jaccard (0.4 weight)
  - Structural similarity - shared neighbors (0.3 weight)
- Configurable threshold and result limit
- Useful for finding related legal precedents

**Example**:
```python
# Find concepts similar to a specific principle
result = integration.lex_engine.query_similar_nodes(
    "principle_good_faith",
    similarity_threshold=0.3,
    max_results=5
)

# Get similarity scores
scores = result.metadata['similarity_scores']
for node in result.nodes:
    print(f"{node.name}: {scores[node.node_id]:.3f}")
```

## Visualization Utilities

### HypergraphVisualizer Class

Comprehensive visualization tools for legal hypergraphs.

**Module**: `models.ggmlex.hypergraphql.visualization`

### 1. Mermaid Diagram Generation

Generate Mermaid diagrams for rendering in GitHub, documentation, or web apps.

**Method**: `generate_mermaid_diagram(query_result, max_nodes=50, include_node_types=True)`

**Features**:
- Color-coded nodes by type (statutes, cases, principles, etc.)
- Handles hyperedges (connecting > 2 nodes) with hub nodes
- Configurable node limit
- GitHub-compatible output

**Example**:
```python
from models.ggmlex.hypergraphql.visualization import HypergraphVisualizer

visualizer = HypergraphVisualizer(integration.lex_engine)

# Get a subgraph to visualize
result = integration.lex_engine.query_subgraph(node_ids[:10])

# Generate Mermaid diagram
mermaid = visualizer.generate_mermaid_diagram(result, max_nodes=20)

# Save to file for viewing in GitHub
with open('legal_graph.mmd', 'w') as f:
    f.write(mermaid)
```

### 2. DOT/Graphviz Export

Export to DOT format for rendering with Graphviz tools.

**Method**: `generate_dot_graph(query_result, max_nodes=50)`

**Example**:
```python
dot_graph = visualizer.generate_dot_graph(result)

# Save and render with Graphviz
with open('legal_graph.dot', 'w') as f:
    f.write(dot_graph)

# Then use: dot -Tpng legal_graph.dot -o legal_graph.png
```

### 3. Network Statistics Summary

Compute comprehensive network statistics for analysis.

**Method**: `generate_network_stats_summary(query_result=None)`

**Returns**:
```python
{
    "num_nodes": 854,
    "num_edges": 74113,
    "degree_distribution": {0: 46, 1: 128, 2: 203, ...},
    "hyperedge_size_distribution": {2: 70000, 3: 4113},
    "avg_degree": 173.57,
    "max_degree": 450,
    "num_connected_components": 3,
    "top_connected_nodes": [
        {"node_id": "...", "name": "...", "degree": 450, "type": "statute"},
        ...
    ],
    "density": 0.123
}
```

### 4. JSON Export

Export graph data in JSON format for custom processing or web applications.

**Method**: `export_to_json(query_result, include_content=False)`

**Example**:
```python
json_data = visualizer.export_to_json(result, include_content=True)

# Parse and use
import json
graph = json.loads(json_data)
for node in graph['nodes']:
    print(f"{node['name']} ({node['type']})")
```

## Temporal Hypergraph Analysis

### TemporalHypergraph Class

Track changes in the hypergraph over time.

**Module**: `models.hyper_gnn.hypergnn_model`

**Features**:
- Track edge creation and removal timestamps
- Create snapshots at specific points in time
- Analyze temporal evolution patterns
- Model dynamic legal relationships

### Usage

```python
from models.hyper_gnn import TemporalHypergraph, Hyperedge

# Create temporal graph
temporal_graph = TemporalHypergraph()

# Add nodes (same as regular hypergraph)
for agent in agents:
    node = Node(node_id=agent.id, node_type="agent", ...)
    temporal_graph.add_node(node)

# Add edges with timestamps
edge1 = Hyperedge(
    edge_id="collaboration_1",
    nodes={"agent_1", "agent_2"},
    edge_type="collaboration"
)
temporal_graph.add_temporal_hyperedge(edge1, timestamp=10.0)

# Mark edge as removed at later time
temporal_graph.remove_temporal_hyperedge("collaboration_1", timestamp=20.0)

# Get snapshot at specific time
snapshot_15 = temporal_graph.snapshot_at_time(15.0)  # Edge exists
snapshot_25 = temporal_graph.snapshot_at_time(25.0)  # Edge removed

# Analyze evolution
evolution = temporal_graph.get_temporal_evolution()
print(f"Total events: {evolution['total_events']}")
for event in evolution['evolution']:
    print(f"  t={event['timestamp']}: {event['num_edges']} edges ({event['event']})")
```

## Attention-Based HyperGNN

### AttentionHyperGNNLayer Class

HyperGNN layer with learnable attention mechanism for better aggregation.

**Module**: `models.hyper_gnn.hypergnn_model`

**Features**:
- Learnable attention weights for node importance
- Softmax-normalized attention scores
- Better captures complex relationships
- Improves hyperedge aggregation

### Usage

```python
from models.hyper_gnn import AttentionHyperGNNLayer, Hypergraph

# Create attention-based layer
layer = AttentionHyperGNNLayer(input_dim=64, output_dim=32)

# Use in forward pass
hypergraph = Hypergraph()
# ... add nodes and edges ...

# Forward pass with attention
embeddings = layer.forward(hypergraph)

# Get attention weights for specific nodes
node_embeddings = [hypergraph.nodes[nid].embeddings for nid in ["n1", "n2", "n3"]]
attention_weights = layer.compute_attention_weights(node_embeddings)
print(f"Attention weights: {attention_weights}")  # Sums to 1.0
```

### Benefits

- **Better Node Importance**: Automatically learns which nodes are more important
- **Improved Aggregation**: Weighted aggregation vs simple mean/max
- **Interpretability**: Attention weights show which nodes influence results

## Hierarchical Hypergraph Structures

### HierarchicalHypergraph Class

Multi-level graph abstraction for analyzing structure at different scales.

**Module**: `models.hyper_gnn.hypergnn_model`

**Features**:
- Build hierarchies by coarsening graphs
- Multiple levels of abstraction
- Cluster-based node grouping
- Analyze at different granularities

### Usage

```python
from models.hyper_gnn import HierarchicalHypergraph

# Create hierarchy
hierarchy = HierarchicalHypergraph()

# Build from base graph
base_graph = Hypergraph()  # Your hypergraph
hierarchy.build_hierarchy(base_graph, num_levels=3)

# Access different levels
print(f"Level 0 (base): {len(hierarchy.levels[0].nodes)} nodes")
print(f"Level 1 (coarse): {len(hierarchy.levels[1].nodes)} nodes")
print(f"Level 2 (coarser): {len(hierarchy.levels[2].nodes)} nodes")

# Get statistics
stats = hierarchy.get_statistics()
for level_stat in stats['level_stats']:
    print(f"Level {level_stat['level']}: {level_stat['num_nodes']} nodes, {level_stat['num_edges']} edges")

# Manual coarsening with custom number of clusters
coarse_graph, mapping = hierarchy.coarsen_graph(base_graph, num_clusters=10)
print(f"Coarsened to {len(coarse_graph.nodes)} clusters")
```

### Use Cases

- **Case Clustering**: Group similar cases at different levels
- **Legal Domain Hierarchy**: Organize legal concepts hierarchically
- **Multi-Resolution Analysis**: Analyze at both detailed and summary levels
- **Scalability**: Work with large graphs by analyzing coarser versions

## Usage Examples

### Complete Workflow Example

```python
from models.integration import LexADIntegration
from models.ggmlex.hypergraphql.visualization import HypergraphVisualizer
from models.hyper_gnn import TemporalHypergraph, AttentionHyperGNNLayer, HierarchicalHypergraph

# 1. Load legal framework
integration = LexADIntegration()
integration.generate_lex_hypergraph()

# 2. Query for specific legal concepts
result = integration.lex_engine.query_nodes(
    node_type=LegalNodeType.STATUTE,
    jurisdiction="za"
)
print(f"Found {len(result)} statutes")

# 3. Find related concepts
statute_id = result.nodes[0].node_id
similar = integration.lex_engine.query_similar_nodes(statute_id, max_results=5)

# 4. Build reasoning chain
chain = integration.lex_engine.query_legal_reasoning_chain(statute_id, max_depth=4)
print(f"Reasoning chain: {' -> '.join([n.name for n in chain.nodes])}")

# 5. Visualize
visualizer = HypergraphVisualizer(integration.lex_engine)
mermaid = visualizer.generate_mermaid_diagram(chain, max_nodes=10)
with open('reasoning_chain.mmd', 'w') as f:
    f.write(mermaid)

# 6. Network analysis
stats = visualizer.generate_network_stats_summary()
print(f"Network density: {stats['density']:.4f}")
print(f"Average degree: {stats['avg_degree']:.2f}")
print("\nTop connected nodes:")
for node in stats['top_connected_nodes'][:5]:
    print(f"  {node['name']}: {node['degree']} connections")

# 7. Temporal analysis
temporal_graph = TemporalHypergraph()
# ... add temporal edges ...
evolution = temporal_graph.get_temporal_evolution()

# 8. Hierarchical analysis
hierarchy = HierarchicalHypergraph()
hierarchy.build_hierarchy(integration.ad_hypergraph, num_levels=3)
```

## API Reference

### HypergraphQLEngine

#### query_subgraph(node_ids, include_edges=True, expand_neighbors=False)

Extract subgraph containing specified nodes.

**Parameters**:
- `node_ids` (List[str]): Node IDs to include
- `include_edges` (bool): Include edges between nodes
- `expand_neighbors` (bool): Expand to immediate neighbors

**Returns**: `QueryResult` with nodes and edges

#### query_legal_reasoning_chain(start_node_id, max_depth=5)

Find legal reasoning chains via DEPENDS_ON relationships.

**Parameters**:
- `start_node_id` (str): Starting node
- `max_depth` (int): Maximum chain depth

**Returns**: `QueryResult` with longest chain found

#### query_similar_nodes(node_id, similarity_threshold=0.3, max_results=10)

Find nodes similar to given node.

**Parameters**:
- `node_id` (str): Source node
- `similarity_threshold` (float): Minimum similarity (0-1)
- `max_results` (int): Maximum results to return

**Returns**: `QueryResult` with similar nodes and scores

### HypergraphVisualizer

#### generate_mermaid_diagram(query_result, max_nodes=50, include_node_types=True)

Generate Mermaid diagram.

**Parameters**:
- `query_result` (QueryResult | None): Graph to visualize
- `max_nodes` (int): Maximum nodes to include
- `include_node_types` (bool): Show node types in labels

**Returns**: Mermaid diagram string

#### generate_network_stats_summary(query_result=None)

Compute network statistics.

**Returns**: Dictionary with comprehensive statistics

### TemporalHypergraph

Extends `Hypergraph` with temporal tracking.

#### add_temporal_hyperedge(hyperedge, timestamp)

Add edge with timestamp.

#### remove_temporal_hyperedge(edge_id, timestamp)

Mark edge as removed at time.

#### snapshot_at_time(timestamp)

Get graph snapshot at specific time.

#### get_temporal_evolution()

Get temporal evolution statistics.

### AttentionHyperGNNLayer

Extends `HyperGNNLayer` with attention.

#### compute_attention_weights(node_embeddings)

Compute softmax attention weights.

**Returns**: Normalized weights array

### HierarchicalHypergraph

Multi-level graph structure.

#### build_hierarchy(base_graph, num_levels=3)

Build hierarchy from base graph.

#### coarsen_graph(hypergraph, num_clusters)

Create coarser version via clustering.

**Returns**: (coarse_graph, mapping)

#### get_statistics()

Get statistics for all levels.

## Performance Considerations

- **Subgraph queries**: O(|nodes| + |edges|) for extraction
- **Reasoning chains**: DFS with visited tracking, O(|V| + |E|) worst case
- **Similarity**: O(|V|) comparisons, can be expensive for large graphs
- **Visualization**: Limited to max_nodes to prevent rendering issues
- **Temporal snapshots**: O(|temporal_events|) to reconstruct
- **Hierarchical coarsening**: O(|V| + |E|) per level

## Testing

All features have comprehensive test coverage (45 tests total):

```bash
# Run all tests
pytest models/integration/test_integration.py \
       models/integration/test_enhancements.py \
       models/integration/test_advanced_enhancements.py -v

# Run specific test suite
pytest models/integration/test_advanced_enhancements.py -v

# Run specific test
pytest models/integration/test_advanced_enhancements.py::TestLexHypergraphAdvancedQueries -v
```

## Future Enhancements

Potential areas for further development:

1. **Graph Neural Networks**: Full GNN training on legal graphs
2. **Embedding-based Similarity**: Use learned embeddings for better similarity
3. **Dynamic Graph Learning**: Learn from temporal patterns
4. **Multi-hop Reasoning**: Complex inference across multiple relationships
5. **Interactive Visualization**: Web-based graph explorer
6. **Graph Kernels**: Compare entire graphs for similarity

## References

- HypergraphQL Engine: `models/ggmlex/hypergraphql/engine.py`
- Visualization: `models/ggmlex/hypergraphql/visualization.py`
- HyperGNN Model: `models/hyper_gnn/hypergnn_model.py`
- Integration: `models/integration/lex_ad_hypergraph_integration.py`
- Tests: `models/integration/test_advanced_enhancements.py`

## Contributors

- Enhanced by: GitHub Copilot
- Date: October 2025
- Repository: rzonedevops/analyticase
