#!/usr/bin/env python3
"""
Legal Schema Definitions for HypergraphQL

This module defines the schema for legal documents, statutes, cases,
and their relationships in a hypergraph structure.
"""

import logging
from typing import Dict, Any, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LegalNodeType(Enum):
    """Types of legal nodes in the hypergraph."""
    STATUTE = "statute"
    SECTION = "section"
    SUBSECTION = "subsection"
    CASE = "case"
    PRECEDENT = "precedent"
    PRINCIPLE = "principle"
    CONCEPT = "concept"
    PARTY = "party"
    COURT = "court"
    JUDGE = "judge"


class InferenceType(Enum):
    """Types of inference used to derive principles."""
    DEDUCTIVE = "deductive"
    INDUCTIVE = "inductive"
    ABDUCTIVE = "abductive"
    ANALOGICAL = "analogical"


class LegalRelationType(Enum):
    """Types of relationships between legal entities."""
    CITES = "cites"
    INTERPRETS = "interprets"
    OVERRULES = "overrules"
    FOLLOWS = "follows"
    DISTINGUISHES = "distinguishes"
    AMENDS = "amends"
    REPEALS = "repeals"
    APPLIES_TO = "applies_to"
    CONFLICTS_WITH = "conflicts_with"
    SUPPORTS = "supports"
    DEPENDS_ON = "depends_on"  # For dependencies between legal definitions
    INFERS_FROM = "infers_from"  # For inferred principles from laws
    GENERALIZES = "generalizes"  # For generalization relationships


@dataclass
class LegalNode:
    """
    Represents a node in the legal hypergraph.
    
    This can be a statute, case, legal principle, or any other
    legal entity that can be referenced and queried.
    """
    
    node_id: str
    node_type: LegalNodeType
    name: str
    content: str = ""
    jurisdiction: str = "za"  # South Africa by default
    metadata: Dict[str, Any] = field(default_factory=dict)
    properties: Dict[str, Any] = field(default_factory=dict)
    inference_level: int = 0  # 0=enumerated law, 1=first-order principle, 2=meta-principle
    inference_type: Optional['InferenceType'] = None  # How this node was inferred (if applicable)
    confidence: float = 1.0  # Confidence score for inferred nodes
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert node to dictionary representation."""
        return {
            "id": self.node_id,
            "type": self.node_type.value,
            "name": self.name,
            "content": self.content,
            "jurisdiction": self.jurisdiction,
            "metadata": self.metadata,
            "properties": self.properties,
            "inference_level": self.inference_level,
            "inference_type": self.inference_type.value if self.inference_type else None,
            "confidence": self.confidence
        }


@dataclass
class LegalHyperedge:
    """
    Represents a hyperedge in the legal hypergraph.
    
    Hyperedges can connect multiple legal entities with a specific
    relationship type, allowing for complex multi-party relationships.
    """
    
    edge_id: str
    relation_type: LegalRelationType
    nodes: Set[str]  # Set of node IDs
    weight: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    properties: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0  # Confidence in the relationship (for inferred edges)
    inference_type: Optional['InferenceType'] = None  # How this relationship was inferred
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert hyperedge to dictionary representation."""
        return {
            "id": self.edge_id,
            "relation_type": self.relation_type.value,
            "nodes": list(self.nodes),
            "weight": self.weight,
            "metadata": self.metadata,
            "properties": self.properties,
            "confidence": self.confidence,
            "inference_type": self.inference_type.value if self.inference_type else None
        }


class LegalSchema:
    """
    Schema definition for the legal hypergraph.
    
    This defines the structure, types, and constraints for legal entities
    and their relationships within the hypergraph.
    """
    
    def __init__(self):
        """Initialize legal schema."""
        self.node_types = {nt.value: nt for nt in LegalNodeType}
        self.relation_types = {rt.value: rt for rt in LegalRelationType}
        
        # Define valid relationships between node types
        self.valid_relationships = self._init_valid_relationships()
        
        logger.info("Initialized LegalSchema")
    
    def _init_valid_relationships(self) -> Dict[str, Set[str]]:
        """
        Initialize valid relationships between node types.
        
        Returns:
            Dictionary mapping node type pairs to valid relationship types
        """
        valid = {}
        
        # Case -> Case relationships
        valid[("case", "case")] = {
            LegalRelationType.CITES,
            LegalRelationType.FOLLOWS,
            LegalRelationType.DISTINGUISHES,
            LegalRelationType.OVERRULES
        }
        
        # Case -> Statute relationships
        valid[("case", "statute")] = {
            LegalRelationType.CITES,
            LegalRelationType.INTERPRETS,
            LegalRelationType.APPLIES_TO
        }
        
        # Statute -> Statute relationships
        valid[("statute", "statute")] = {
            LegalRelationType.AMENDS,
            LegalRelationType.REPEALS,
            LegalRelationType.CONFLICTS_WITH
        }
        
        # Section -> Section relationships
        valid[("section", "section")] = {
            LegalRelationType.SUPPORTS,
            LegalRelationType.CONFLICTS_WITH
        }
        
        # Principle -> Principle relationships
        valid[("principle", "principle")] = {
            LegalRelationType.SUPPORTS,
            LegalRelationType.CONFLICTS_WITH
        }
        
        return valid
    
    def is_valid_relationship(
        self,
        source_type: LegalNodeType,
        target_type: LegalNodeType,
        relation_type: LegalRelationType
    ) -> bool:
        """
        Check if a relationship is valid between two node types.
        
        Args:
            source_type: Source node type
            target_type: Target node type
            relation_type: Relationship type
            
        Returns:
            True if relationship is valid, False otherwise
        """
        key = (source_type.value, target_type.value)
        valid_relations = self.valid_relationships.get(key, set())
        
        return relation_type in valid_relations
    
    def get_node_schema(self, node_type: LegalNodeType) -> Dict[str, Any]:
        """
        Get schema definition for a specific node type.
        
        Args:
            node_type: Node type
            
        Returns:
            Schema definition
        """
        schemas = {
            LegalNodeType.STATUTE: {
                "required_fields": ["name", "jurisdiction"],
                "optional_fields": ["content", "enactment_date", "effective_date"],
                "properties": {
                    "enactment_date": "date",
                    "effective_date": "date",
                    "status": "string"
                }
            },
            LegalNodeType.CASE: {
                "required_fields": ["name", "jurisdiction"],
                "optional_fields": ["content", "court", "date", "parties"],
                "properties": {
                    "court": "string",
                    "date": "date",
                    "case_number": "string",
                    "citation": "string"
                }
            },
            LegalNodeType.SECTION: {
                "required_fields": ["name", "content"],
                "optional_fields": ["section_number", "parent_statute"],
                "properties": {
                    "section_number": "string",
                    "parent_statute": "string"
                }
            }
        }
        
        return schemas.get(node_type, {})
    
    def validate_node(self, node: LegalNode) -> Tuple[bool, List[str]]:
        """
        Validate a legal node against the schema.
        
        Args:
            node: Node to validate
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        schema = self.get_node_schema(node.node_type)
        
        if not schema:
            return True, []  # No schema defined, skip validation
        
        # Check required fields
        required = schema.get("required_fields", [])
        for field in required:
            if field == "name" and not node.name:
                errors.append(f"Required field 'name' is missing")
            elif field == "jurisdiction" and not node.jurisdiction:
                errors.append(f"Required field 'jurisdiction' is missing")
            elif field == "content" and not node.content:
                errors.append(f"Required field 'content' is missing")
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    def get_schema_info(self) -> Dict[str, Any]:
        """
        Get complete schema information.
        
        Returns:
            Schema information dictionary
        """
        return {
            "node_types": [nt.value for nt in LegalNodeType],
            "relation_types": [rt.value for rt in LegalRelationType],
            "valid_relationships": {
                f"{k[0]}->{k[1]}": [rt.value for rt in v]
                for k, v in self.valid_relationships.items()
            }
        }


if __name__ == "__main__":
    # Example usage
    logger.info("Testing LegalSchema")
    
    schema = LegalSchema()
    
    # Create a statute node
    statute = LegalNode(
        node_id="statute_001",
        node_type=LegalNodeType.STATUTE,
        name="Constitution of South Africa",
        content="The supreme law of the Republic",
        jurisdiction="za",
        metadata={"year": 1996}
    )
    
    # Validate node
    is_valid, errors = schema.validate_node(statute)
    logger.info(f"Statute validation: valid={is_valid}, errors={errors}")
    
    # Create a case node
    case = LegalNode(
        node_id="case_001",
        node_type=LegalNodeType.CASE,
        name="Smith v. Jones",
        jurisdiction="za",
        properties={"court": "High Court", "date": "2024-01-15"}
    )
    
    is_valid, errors = schema.validate_node(case)
    logger.info(f"Case validation: valid={is_valid}, errors={errors}")
    
    # Check valid relationships
    is_valid = schema.is_valid_relationship(
        LegalNodeType.CASE,
        LegalNodeType.STATUTE,
        LegalRelationType.CITES
    )
    logger.info(f"Case -> Statute CITES relationship valid: {is_valid}")
    
    # Get schema info
    info = schema.get_schema_info()
    logger.info(f"Schema node types: {info['node_types']}")
    
    logger.info("LegalSchema testing completed")
