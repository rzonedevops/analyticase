"""
HypergraphQL Module for Legal Framework Integration

This module provides HypergraphQL functionality for querying and analyzing
the legal framework structure in lex/.
"""

from .engine import HypergraphQLEngine, QueryResult
from .schema import (
    LegalSchema, LegalNode, LegalHyperedge,
    LegalNodeType, LegalRelationType
)

__all__ = [
    'HypergraphQLEngine',
    'QueryResult',
    'LegalSchema',
    'LegalNode',
    'LegalHyperedge',
    'LegalNodeType',
    'LegalRelationType',
]
