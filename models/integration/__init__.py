"""
Integration Module for Lex-AD Hypergraph

This module provides integration between:
- Lex hypergraph (legal framework)
- AD hypergraph (Agent-based + Discrete-event models)
- HyperGNN (hypergraph neural network)
- Case-LLM (legal language model with attention mapping)
"""

from .lex_ad_hypergraph_integration import (
    LexADIntegration,
    IntegratedHypergraph,
    run_lex_ad_integration
)

__all__ = [
    'LexADIntegration',
    'IntegratedHypergraph',
    'run_lex_ad_integration'
]
