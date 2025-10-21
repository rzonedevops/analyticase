"""
HyperGNN Model for Legal Case Hypergraph Analysis

This module implements a Hypergraph Neural Network for analyzing complex
relationships and higher-order interactions in legal cases.
"""

from .hypergnn_model import (
    Hypergraph,
    Node,
    Hyperedge,
    HyperGNN,
    HyperGNNLayer,
    TemporalHypergraph,
    AttentionHyperGNNLayer,
    HierarchicalHypergraph,
    create_case_hypergraph
)

__all__ = [
    'Hypergraph',
    'Node',
    'Hyperedge',
    'HyperGNN',
    'HyperGNNLayer',
    'TemporalHypergraph',
    'AttentionHyperGNNLayer',
    'HierarchicalHypergraph',
    'create_case_hypergraph',
]
