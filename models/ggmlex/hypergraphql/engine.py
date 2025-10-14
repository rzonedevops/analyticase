#!/usr/bin/env python3
"""
HypergraphQL Query Engine for Legal Framework

This module implements a query engine for traversing and querying the legal
hypergraph, including support for complex queries over legislation, cases,
and legal principles.
"""

import logging
from typing import Dict, Any, List, Optional, Set, Callable, Tuple
from dataclasses import dataclass, field
import re
from pathlib import Path

from .schema import (
    LegalSchema, LegalNode, LegalHyperedge,
    LegalNodeType, LegalRelationType
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class QueryResult:
    """Result of a HypergraphQL query."""
    
    nodes: List[LegalNode] = field(default_factory=list)
    edges: List[LegalHyperedge] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "nodes": [n.to_dict() for n in self.nodes],
            "edges": [e.to_dict() for e in self.edges],
            "metadata": self.metadata
        }
    
    def __len__(self) -> int:
        """Return number of nodes in result."""
        return len(self.nodes)


class HypergraphQLEngine:
    """
    HypergraphQL query engine for legal framework.
    
    This engine provides:
    - Graph traversal and querying
    - Pattern matching over legal structures
    - Integration with lex/ directory legal framework
    - Support for complex legal reasoning queries
    """
    
    def __init__(self, lex_path: Optional[str] = None):
        """
        Initialize HypergraphQL engine.
        
        Args:
            lex_path: Path to lex/ directory containing legal framework
        """
        self.schema = LegalSchema()
        self.nodes: Dict[str, LegalNode] = {}
        self.edges: Dict[str, LegalHyperedge] = {}
        self.node_to_edges: Dict[str, Set[str]] = {}
        
        # Path to legal framework
        self.lex_path = lex_path or "/home/runner/work/analyticase/analyticase/lex"
        
        # Load legal framework
        self._load_legal_framework()
        
        logger.info(f"Initialized HypergraphQLEngine with {len(self.nodes)} nodes")
    
    def _load_legal_framework(self):
        """Load legal framework from lex/ directory."""
        lex_dir = Path(self.lex_path)
        
        if not lex_dir.exists():
            logger.warning(f"Legal framework directory not found: {self.lex_path}")
            return
        
        # Load South African civil law
        civil_law_file = lex_dir / "civ" / "za" / "south_african_civil_law.scm"
        if civil_law_file.exists():
            self._load_scheme_file(civil_law_file)
        
        logger.info(f"Loaded legal framework from {self.lex_path}")
    
    def _load_scheme_file(self, file_path: Path):
        """
        Load legal definitions from Scheme file.
        
        Args:
            file_path: Path to Scheme file
        """
        try:
            content = file_path.read_text()
            
            # Parse Scheme definitions (simplified parsing)
            # In production, use a proper Scheme parser
            definitions = self._extract_scheme_definitions(content)
            
            for def_name, def_content in definitions:
                # Create a node for each legal definition
                node = LegalNode(
                    node_id=f"sa_civil_{def_name}",
                    node_type=LegalNodeType.PRINCIPLE,
                    name=def_name.replace("-", " ").title(),
                    content=def_content,
                    jurisdiction="za",
                    metadata={"source": str(file_path)}
                )
                self.add_node(node)
            
            logger.debug(f"Loaded {len(definitions)} definitions from {file_path.name}")
            
        except Exception as e:
            logger.error(f"Error loading Scheme file {file_path}: {e}")
    
    def _extract_scheme_definitions(self, content: str) -> List[Tuple[str, str]]:
        """
        Extract Scheme definitions from content.
        
        Args:
            content: Scheme file content
            
        Returns:
            List of (definition_name, content) tuples
        """
        definitions = []
        
        # Match (define name ...) patterns
        pattern = r'\(define\s+([^\s\)]+)\s+\(lambda[^\)]*\)([^)]*(?:\([^)]*\)[^)]*)*)\)'
        matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)
        
        for match in matches:
            name = match.group(1)
            body = match.group(2).strip()
            definitions.append((name, body[:200]))  # Truncate long definitions
        
        return definitions
    
    def add_node(self, node: LegalNode):
        """
        Add a node to the hypergraph.
        
        Args:
            node: Legal node to add
        """
        # Validate node
        is_valid, errors = self.schema.validate_node(node)
        if not is_valid:
            logger.warning(f"Node validation failed: {errors}")
        
        self.nodes[node.node_id] = node
        if node.node_id not in self.node_to_edges:
            self.node_to_edges[node.node_id] = set()
        
        logger.debug(f"Added node: {node.node_id}")
    
    def add_edge(self, edge: LegalHyperedge):
        """
        Add a hyperedge to the hypergraph.
        
        Args:
            edge: Legal hyperedge to add
        """
        self.edges[edge.edge_id] = edge
        
        # Update node-to-edge mapping
        for node_id in edge.nodes:
            if node_id not in self.node_to_edges:
                self.node_to_edges[node_id] = set()
            self.node_to_edges[node_id].add(edge.edge_id)
        
        logger.debug(f"Added edge: {edge.edge_id}")
    
    def get_node(self, node_id: str) -> Optional[LegalNode]:
        """Get node by ID."""
        return self.nodes.get(node_id)
    
    def query_nodes(
        self,
        node_type: Optional[LegalNodeType] = None,
        jurisdiction: Optional[str] = None,
        name_pattern: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> QueryResult:
        """
        Query nodes by various criteria.
        
        Args:
            node_type: Filter by node type
            jurisdiction: Filter by jurisdiction
            name_pattern: Filter by name pattern (regex)
            properties: Filter by properties
            
        Returns:
            Query result with matching nodes
        """
        matching_nodes = []
        
        for node in self.nodes.values():
            # Filter by node type
            if node_type and node.node_type != node_type:
                continue
            
            # Filter by jurisdiction
            if jurisdiction and node.jurisdiction != jurisdiction:
                continue
            
            # Filter by name pattern
            if name_pattern:
                if not re.search(name_pattern, node.name, re.IGNORECASE):
                    continue
            
            # Filter by properties
            if properties:
                match = True
                for key, value in properties.items():
                    if node.properties.get(key) != value:
                        match = False
                        break
                if not match:
                    continue
            
            matching_nodes.append(node)
        
        result = QueryResult(
            nodes=matching_nodes,
            metadata={"query_type": "node_query", "count": len(matching_nodes)}
        )
        
        logger.debug(f"Query returned {len(result)} nodes")
        
        return result
    
    def query_neighbors(
        self,
        node_id: str,
        relation_type: Optional[LegalRelationType] = None,
        max_hops: int = 1
    ) -> QueryResult:
        """
        Query neighbors of a node.
        
        Args:
            node_id: Starting node ID
            relation_type: Filter by relationship type
            max_hops: Maximum number of hops (default 1)
            
        Returns:
            Query result with neighbor nodes
        """
        if node_id not in self.nodes:
            logger.warning(f"Node not found: {node_id}")
            return QueryResult()
        
        visited = set()
        neighbors = []
        edges_included = []
        
        def traverse(current_id: str, hops: int):
            """Recursive traversal helper."""
            if hops > max_hops or current_id in visited:
                return
            
            visited.add(current_id)
            
            # Get edges for current node
            edge_ids = self.node_to_edges.get(current_id, set())
            
            for edge_id in edge_ids:
                edge = self.edges.get(edge_id)
                if not edge:
                    continue
                
                # Filter by relation type
                if relation_type and edge.relation_type != relation_type:
                    continue
                
                edges_included.append(edge)
                
                # Get neighbor nodes
                for neighbor_id in edge.nodes:
                    if neighbor_id != current_id and neighbor_id not in visited:
                        neighbor = self.nodes.get(neighbor_id)
                        if neighbor:
                            neighbors.append(neighbor)
                            if hops < max_hops:
                                traverse(neighbor_id, hops + 1)
        
        # Start traversal
        traverse(node_id, 0)
        
        result = QueryResult(
            nodes=neighbors,
            edges=edges_included,
            metadata={
                "query_type": "neighbor_query",
                "source_node": node_id,
                "max_hops": max_hops,
                "count": len(neighbors)
            }
        )
        
        logger.debug(f"Found {len(result)} neighbors for node {node_id}")
        
        return result
    
    def query_path(
        self,
        source_id: str,
        target_id: str,
        max_depth: int = 5
    ) -> QueryResult:
        """
        Find path between two nodes.
        
        Args:
            source_id: Source node ID
            target_id: Target node ID
            max_depth: Maximum search depth
            
        Returns:
            Query result with nodes and edges in path
        """
        if source_id not in self.nodes or target_id not in self.nodes:
            logger.warning("Source or target node not found")
            return QueryResult()
        
        # BFS to find shortest path
        from collections import deque
        
        queue = deque([(source_id, [source_id], [])])
        visited = {source_id}
        
        while queue:
            current_id, path, edges = queue.popleft()
            
            if len(path) > max_depth:
                continue
            
            if current_id == target_id:
                # Found path
                path_nodes = [self.nodes[nid] for nid in path if nid in self.nodes]
                result = QueryResult(
                    nodes=path_nodes,
                    edges=edges,
                    metadata={
                        "query_type": "path_query",
                        "source": source_id,
                        "target": target_id,
                        "path_length": len(path)
                    }
                )
                logger.debug(f"Found path of length {len(path)}")
                return result
            
            # Explore neighbors
            edge_ids = self.node_to_edges.get(current_id, set())
            for edge_id in edge_ids:
                edge = self.edges.get(edge_id)
                if not edge:
                    continue
                
                for neighbor_id in edge.nodes:
                    if neighbor_id not in visited:
                        visited.add(neighbor_id)
                        queue.append((
                            neighbor_id,
                            path + [neighbor_id],
                            edges + [edge]
                        ))
        
        # No path found
        logger.debug(f"No path found between {source_id} and {target_id}")
        return QueryResult(metadata={"query_type": "path_query", "path_found": False})
    
    def query_by_content(self, content_pattern: str) -> QueryResult:
        """
        Query nodes by content pattern.
        
        Args:
            content_pattern: Regex pattern to match in content
            
        Returns:
            Query result with matching nodes
        """
        matching_nodes = []
        
        for node in self.nodes.values():
            if re.search(content_pattern, node.content, re.IGNORECASE):
                matching_nodes.append(node)
        
        result = QueryResult(
            nodes=matching_nodes,
            metadata={"query_type": "content_query", "count": len(matching_nodes)}
        )
        
        logger.debug(f"Content query returned {len(result)} nodes")
        
        return result
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get hypergraph statistics.
        
        Returns:
            Statistics dictionary
        """
        node_type_counts = {}
        for node in self.nodes.values():
            node_type = node.node_type.value
            node_type_counts[node_type] = node_type_counts.get(node_type, 0) + 1
        
        edge_type_counts = {}
        for edge in self.edges.values():
            edge_type = edge.relation_type.value
            edge_type_counts[edge_type] = edge_type_counts.get(edge_type, 0) + 1
        
        return {
            "num_nodes": len(self.nodes),
            "num_edges": len(self.edges),
            "node_types": node_type_counts,
            "edge_types": edge_type_counts,
            "avg_node_degree": sum(len(edges) for edges in self.node_to_edges.values()) / max(len(self.nodes), 1)
        }


if __name__ == "__main__":
    # Example usage
    logger.info("Testing HypergraphQLEngine")
    
    # Initialize engine
    engine = HypergraphQLEngine()
    
    # Add some test nodes
    statute = LegalNode(
        node_id="statute_001",
        node_type=LegalNodeType.STATUTE,
        name="Constitution of South Africa",
        content="The supreme law of the Republic",
        jurisdiction="za"
    )
    engine.add_node(statute)
    
    case = LegalNode(
        node_id="case_001",
        node_type=LegalNodeType.CASE,
        name="Smith v. Jones",
        content="A landmark case on constitutional rights",
        jurisdiction="za"
    )
    engine.add_node(case)
    
    # Add an edge
    edge = LegalHyperedge(
        edge_id="edge_001",
        relation_type=LegalRelationType.CITES,
        nodes={statute.node_id, case.node_id}
    )
    engine.add_edge(edge)
    
    # Query nodes
    result = engine.query_nodes(node_type=LegalNodeType.CASE, jurisdiction="za")
    logger.info(f"Found {len(result)} cases")
    
    # Query neighbors
    result = engine.query_neighbors(statute.node_id)
    logger.info(f"Found {len(result)} neighbors")
    
    # Get statistics
    stats = engine.get_statistics()
    logger.info(f"Hypergraph statistics: {stats}")
    
    logger.info("HypergraphQLEngine testing completed")
