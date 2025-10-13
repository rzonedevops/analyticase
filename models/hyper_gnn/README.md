# HyperGNN Model for Legal Case Analysis

## Overview

This model uses a Hypergraph Neural Network (HyperGNN) to analyze the complex, multi-way relationships within a legal case. Traditional graphs can only represent pairwise relationships, but hypergraphs can model interactions between any number of entities. This is particularly useful in legal cases where events, documents, and individuals are often interconnected in complex ways.

### Key Concepts

- **Node**: Represents an entity in the case (e.g., a person, a piece of evidence, a location).
- **Hyperedge**: Represents a relationship that connects a set of nodes (e.g., a meeting involving several people, a document referencing multiple pieces of evidence).

## How It Works

The model first constructs a hypergraph from the case data. Then, the HyperGNN learns embeddings (vector representations) for each node by passing messages along the hyperedges. These embeddings can then be used for a variety of downstream tasks, such as:

- **Community Detection**: Identifying clusters of closely related entities.
- **Link Prediction**: Predicting missing or future relationships between entities.
- **Node Classification**: Classifying entities based on their role or importance.

## How to Run

The model can be run as a standalone script or as part of the unified simulation runner.

```bash
python models/hyper_gnn/hypergnn_model.py
```

This will run a sample analysis on generated data and print the results.

