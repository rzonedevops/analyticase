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
        
        # Load all South African legal frameworks
        legal_branches = {
            "civ": "civil law",
            "cri": "criminal law",
            "con": "constitutional law",
            "const": "construction law",
            "admin": "administrative law",
            "lab": "labour law",
            "env": "environmental law",
            "intl": "international law"
        }
        
        loaded_count = 0
        for branch_code, branch_name in legal_branches.items():
            branch_dir = lex_dir / branch_code / "za"
            if branch_dir.exists():
                # Find all .scm files in this branch
                for scm_file in branch_dir.glob("*.scm"):
                    self._load_scheme_file(scm_file)
                    loaded_count += 1
                    logger.debug(f"Loaded {branch_name} from {scm_file.name}")
        
        logger.info(f"Loaded {loaded_count} legal framework(s) from {self.lex_path}")
    
    def _load_scheme_file(self, file_path: Path):
        """
        Load legal definitions from Scheme file with relationship extraction.
        
        Args:
            file_path: Path to Scheme file
        """
        try:
            content = file_path.read_text()
            
            # Parse Scheme definitions
            definitions = self._extract_scheme_definitions(content)
            
            # Determine branch from file path
            branch = "civil"
            if "cri" in str(file_path):
                branch = "criminal"
            elif "con" in str(file_path):
                branch = "constitutional"
            elif "admin" in str(file_path):
                branch = "administrative"
            elif "lab" in str(file_path):
                branch = "labour"
            elif "env" in str(file_path):
                branch = "environmental"
            elif "intl" in str(file_path):
                branch = "international"
            elif "const" in str(file_path):
                branch = "construction"
            
            # Track created nodes for relationship extraction
            created_nodes = []
            
            for def_name, def_content in definitions:
                # Determine node type based on name patterns
                node_type = self._infer_node_type(def_name)
                
                # Create a node for each legal definition
                node = LegalNode(
                    node_id=f"sa_{branch}_{def_name}",
                    node_type=node_type,
                    name=def_name.replace("-", " ").title(),
                    content=def_content,
                    jurisdiction="za",
                    metadata={
                        "source": str(file_path),
                        "branch": branch
                    }
                )
                self.add_node(node)
                created_nodes.append((def_name, node))
            
            # Extract relationships between definitions
            self._extract_relationships(created_nodes, content, branch)
            
            logger.debug(f"Loaded {len(definitions)} definitions from {file_path.name}")
            
        except Exception as e:
            logger.error(f"Error loading Scheme file {file_path}: {e}")
    
    def _infer_node_type(self, def_name: str) -> LegalNodeType:
        """
        Infer node type from definition name.
        
        Args:
            def_name: Definition name
            
        Returns:
            Inferred legal node type
        """
        name_lower = def_name.lower()
        
        if any(word in name_lower for word in ['contract', 'agreement', 'obligation']):
            return LegalNodeType.STATUTE
        elif any(word in name_lower for word in ['case', 'precedent', 'judgment']):
            return LegalNodeType.CASE
        elif any(word in name_lower for word in ['section', 'subsection', 'article']):
            return LegalNodeType.SECTION
        elif any(word in name_lower for word in ['principle', 'doctrine', 'test', 'rule']):
            return LegalNodeType.PRINCIPLE
        else:
            return LegalNodeType.CONCEPT
    
    def _extract_relationships(self, nodes: List[Tuple[str, LegalNode]], content: str, branch: str):
        """
        Extract relationships between legal definitions based on references.
        
        Args:
            nodes: List of (def_name, node) tuples
            content: Full Scheme file content
            branch: Legal branch name
        """
        # Create a mapping of definition names to node IDs
        name_to_node = {def_name: node for def_name, node in nodes}
        
        for def_name, node in nodes:
            # Find all references to other definitions in this definition's body
            for other_name, other_node in nodes:
                if other_name == def_name:
                    continue
                
                # Check if other definition is referenced
                # Look for patterns like (other-name ...) or other-name? 
                pattern = r'\(' + re.escape(other_name) + r'\s|' + re.escape(other_name) + r'\?'
                
                if re.search(pattern, content):
                    # Create a hyperedge representing the relationship
                    edge_id = f"{branch}_rel_{def_name}_to_{other_name}"
                    
                    # Avoid duplicate edges
                    if edge_id not in self.edges:
                        edge = LegalHyperedge(
                            edge_id=edge_id,
                            nodes={node.node_id, other_node.node_id},
                            relation_type=LegalRelationType.DEPENDS_ON,
                            metadata={
                                "source": def_name,
                                "target": other_name,
                                "branch": branch
                            }
                        )
                        self.add_edge(edge)
    
    def _extract_scheme_definitions(self, content: str) -> List[Tuple[str, str]]:
        """
        Extract Scheme definitions from content with enhanced metadata.
        
        Args:
            content: Scheme file content
            
        Returns:
            List of (definition_name, content) tuples
        """
        definitions = []
        
        # Match (define name ...) patterns with improved regex
        # Capture both lambda and non-lambda definitions
        patterns = [
            # Lambda definitions
            r'\(define\s+([^\s\)]+)\s+\(lambda\s*\([^)]*\)([^)]*(?:\([^)]*\)[^)]*)*)\)\)',
            # Simple definitions
            r'\(define\s+([^\s\)]+)\s+([^\(][^\)]*)\)',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)
            for match in matches:
                name = match.group(1)
                body = match.group(2).strip() if len(match.groups()) > 1 else ""
                
                # Skip if already defined
                if any(d[0] == name for d in definitions):
                    continue
                
                # Extract context (comment above definition if present)
                pos = match.start()
                lines_before = content[:pos].split('\n')
                context = ""
                
                # Look for comment lines above definition
                for line in reversed(lines_before[-5:]):
                    line = line.strip()
                    if line.startswith(';;'):
                        context = line[2:].strip() + " " + context
                    elif line:
                        break
                
                # Combine body and context
                full_content = context + " " + body if context else body
                definitions.append((name, full_content[:500]))  # Increased from 200 to 500
        
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
    
    def query_subgraph(
        self,
        node_ids: List[str],
        include_edges: bool = True,
        expand_neighbors: bool = False
    ) -> QueryResult:
        """
        Extract a subgraph containing specified nodes.
        
        Args:
            node_ids: List of node IDs to include
            include_edges: Whether to include edges between nodes
            expand_neighbors: Whether to expand to immediate neighbors
            
        Returns:
            Query result with subgraph
        """
        subgraph_nodes = []
        subgraph_edges = []
        
        # Collect specified nodes
        node_set = set(node_ids)
        if expand_neighbors:
            # Add immediate neighbors
            for node_id in node_ids:
                edge_ids = self.node_to_edges.get(node_id, set())
                for edge_id in edge_ids:
                    edge = self.edges.get(edge_id)
                    if edge:
                        node_set.update(edge.nodes)
        
        # Get nodes
        for node_id in node_set:
            node = self.nodes.get(node_id)
            if node:
                subgraph_nodes.append(node)
        
        # Get edges if requested
        if include_edges:
            for node_id in node_set:
                edge_ids = self.node_to_edges.get(node_id, set())
                for edge_id in edge_ids:
                    edge = self.edges.get(edge_id)
                    if edge and edge not in subgraph_edges:
                        # Only include edge if all nodes are in subgraph
                        if edge.nodes.issubset(node_set):
                            subgraph_edges.append(edge)
        
        return QueryResult(
            nodes=subgraph_nodes,
            edges=subgraph_edges,
            metadata={
                "query_type": "subgraph_query",
                "num_nodes": len(subgraph_nodes),
                "num_edges": len(subgraph_edges),
                "expanded": expand_neighbors
            }
        )
    
    def query_legal_reasoning_chain(
        self,
        start_node_id: str,
        max_depth: int = 5
    ) -> QueryResult:
        """
        Find legal reasoning chains starting from a node.
        
        This follows DEPENDS_ON relationships to build a chain of legal reasoning.
        
        Args:
            start_node_id: Starting node ID
            max_depth: Maximum chain depth
            
        Returns:
            Query result with reasoning chain
        """
        if start_node_id not in self.nodes:
            return QueryResult()
        
        reasoning_chains = []
        visited = set()
        
        def build_chain(node_id: str, depth: int, current_chain: List[LegalNode], current_edges: List[LegalHyperedge]):
            """Recursively build reasoning chain."""
            if depth >= max_depth or node_id in visited:
                if len(current_chain) > 1:
                    reasoning_chains.append((current_chain.copy(), current_edges.copy()))
                return
            
            visited.add(node_id)
            node = self.nodes.get(node_id)
            if not node:
                return
            
            current_chain.append(node)
            
            # Find outgoing DEPENDS_ON edges
            edge_ids = self.node_to_edges.get(node_id, set())
            has_dependencies = False
            
            for edge_id in edge_ids:
                edge = self.edges.get(edge_id)
                if edge and edge.relation_type == LegalRelationType.DEPENDS_ON:
                    # Find target nodes
                    for target_id in edge.nodes:
                        if target_id != node_id and target_id not in visited:
                            has_dependencies = True
                            build_chain(target_id, depth + 1, current_chain, current_edges + [edge])
            
            if not has_dependencies and len(current_chain) > 1:
                reasoning_chains.append((current_chain.copy(), current_edges.copy()))
            
            current_chain.pop()
            visited.discard(node_id)
        
        build_chain(start_node_id, 0, [], [])
        
        # Select the longest chain
        if reasoning_chains:
            best_chain = max(reasoning_chains, key=lambda x: len(x[0]))
            return QueryResult(
                nodes=best_chain[0],
                edges=best_chain[1],
                metadata={
                    "query_type": "reasoning_chain",
                    "start_node": start_node_id,
                    "chain_length": len(best_chain[0]),
                    "num_chains_found": len(reasoning_chains)
                }
            )
        
        return QueryResult(metadata={"query_type": "reasoning_chain", "chains_found": 0})
    
    def query_similar_nodes(
        self,
        node_id: str,
        similarity_threshold: float = 0.3,
        max_results: int = 10
    ) -> QueryResult:
        """
        Find nodes similar to a given node based on content and structure.
        
        Args:
            node_id: Source node ID
            similarity_threshold: Minimum similarity score (0-1)
            max_results: Maximum number of results
            
        Returns:
            Query result with similar nodes
        """
        source_node = self.nodes.get(node_id)
        if not source_node:
            return QueryResult()
        
        similar_nodes = []
        
        for other_id, other_node in self.nodes.items():
            if other_id == node_id:
                continue
            
            # Compute similarity score
            score = 0.0
            
            # Type similarity (0.3 weight)
            if source_node.node_type == other_node.node_type:
                score += 0.3
            
            # Content similarity (0.4 weight) - Jaccard similarity
            source_words = set(source_node.content.lower().split())
            other_words = set(other_node.content.lower().split())
            if source_words or other_words:
                intersection = source_words.intersection(other_words)
                union = source_words.union(other_words)
                content_sim = len(intersection) / len(union) if union else 0
                score += 0.4 * content_sim
            
            # Structural similarity (0.3 weight) - shared neighbors
            source_neighbors = set()
            for edge_id in self.node_to_edges.get(node_id, set()):
                edge = self.edges.get(edge_id)
                if edge:
                    source_neighbors.update(edge.nodes - {node_id})
            
            other_neighbors = set()
            for edge_id in self.node_to_edges.get(other_id, set()):
                edge = self.edges.get(edge_id)
                if edge:
                    other_neighbors.update(edge.nodes - {other_id})
            
            if source_neighbors or other_neighbors:
                neighbor_intersection = source_neighbors.intersection(other_neighbors)
                neighbor_union = source_neighbors.union(other_neighbors)
                structural_sim = len(neighbor_intersection) / len(neighbor_union) if neighbor_union else 0
                score += 0.3 * structural_sim
            
            if score >= similarity_threshold:
                similar_nodes.append((other_node, score))
        
        # Sort by score and limit results
        similar_nodes.sort(key=lambda x: x[1], reverse=True)
        similar_nodes = similar_nodes[:max_results]
        
        return QueryResult(
            nodes=[node for node, _ in similar_nodes],
            metadata={
                "query_type": "similarity_query",
                "source_node": node_id,
                "similarity_scores": {node.node_id: score for node, score in similar_nodes},
                "threshold": similarity_threshold
            }
        )
    
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
    
    def query_by_inference_level(self, level: int) -> QueryResult:
        """
        Query nodes by inference level.
        
        Args:
            level: Inference level (0=enumerated laws, 1=first-order principles, 2=meta-principles)
        
        Returns:
            Query result with nodes at specified level
        """
        matching_nodes = [
            node for node in self.nodes.values()
            if node.inference_level == level
        ]
        
        return QueryResult(
            nodes=matching_nodes,
            metadata={
                "query_type": "inference_level",
                "level": level,
                "count": len(matching_nodes)
            }
        )
    
    def get_enumerated_laws(self) -> QueryResult:
        """
        Get all enumerated laws (inference level 0).
        
        Returns:
            Query result with level 0 nodes
        """
        return self.query_by_inference_level(0)
    
    def get_first_order_principles(self) -> QueryResult:
        """
        Get all first-order principles (inference level 1).
        
        Returns:
            Query result with level 1 nodes
        """
        return self.query_by_inference_level(1)
    
    def get_meta_principles(self) -> QueryResult:
        """
        Get all meta-principles (inference level 2).
        
        Returns:
            Query result with level 2 nodes
        """
        return self.query_by_inference_level(2)
    
    def build_inference_hierarchy(self) -> Dict[int, List[LegalNode]]:
        """
        Build complete inference hierarchy.
        
        Returns:
            Dictionary mapping inference levels to list of nodes
        """
        hierarchy = {}
        
        for node in self.nodes.values():
            level = node.inference_level
            if level not in hierarchy:
                hierarchy[level] = []
            hierarchy[level].append(node)
        
        return hierarchy


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
