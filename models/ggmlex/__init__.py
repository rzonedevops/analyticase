"""
GGMLEX - GGML-based ML Framework with HypergraphQL Integration

This module provides a comprehensive ML framework for legal case analysis
using GGML (Georgi Gerganov Machine Learning) tensor library and HypergraphQL
for complex legal relationship querying.
"""

from .ggml import GGMLTensor, GGMLContext
from .llm import LegalLLM
from .transformers import LegalTransformer
from .hypergraphql import HypergraphQLEngine

__version__ = "0.1.0"

__all__ = [
    'GGMLTensor',
    'GGMLContext',
    'LegalLLM',
    'LegalTransformer',
    'HypergraphQLEngine',
]
