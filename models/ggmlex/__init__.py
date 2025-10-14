"""
GGMLEX - GGML-based ML Framework with HypergraphQL Integration

This module provides a comprehensive ML framework for legal case analysis
using GGML (Georgi Gerganov Machine Learning) tensor library and HypergraphQL
for complex legal relationship querying.
"""

from .ggml import GGMLTensor, GGMLContext
from .llm import LegalLLM, LegalLLMConfig, LegalDocument
from .transformers import LegalTransformer, TransformerConfig
from .hypergraphql import (
    HypergraphQLEngine, LegalNode, LegalHyperedge,
    LegalNodeType, LegalRelationType
)

__version__ = "0.1.0"

__all__ = [
    'GGMLTensor',
    'GGMLContext',
    'LegalLLM',
    'LegalLLMConfig',
    'LegalDocument',
    'LegalTransformer',
    'TransformerConfig',
    'HypergraphQLEngine',
    'LegalNode',
    'LegalHyperedge',
    'LegalNodeType',
    'LegalRelationType',
]
