#!/usr/bin/env python3
"""
Hypergraph Visualization Utilities

This module provides utilities for visualizing legal hypergraphs including:
- Mermaid diagram generation
- DOT/Graphviz export
- Network statistics visualization
- Interactive graph layouts
"""

import logging
from typing import Dict, Any, List, Optional, Set, Tuple
from dataclasses import dataclass
import json

from .schema import LegalNode, LegalHyperedge, LegalNodeType, LegalRelationType
from .engine import HypergraphQLEngine, QueryResult

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HypergraphVisualizer:
    """
    Visualizer for legal hypergraphs.
    """
    
    def __init__(self, engine: HypergraphQLEngine):
        """
        Initialize visualizer.
        
        Args:
            engine: HypergraphQL engine instance
        """
        self.engine = engine
    
    def generate_mermaid_diagram(
        self,
        query_result: Optional[QueryResult] = None,
        max_nodes: int = 50,
        include_node_types: bool = True
    ) -> str:
        """
        Generate Mermaid diagram from query result or full graph.
        
        Args:
            query_result: Optional query result to visualize (None = full graph)
            max_nodes: Maximum number of nodes to include
            include_node_types: Whether to show node types
            
        Returns:
            Mermaid diagram as string
        """
        # Get nodes and edges
        if query_result:
            nodes = query_result.nodes[:max_nodes]
            edges = query_result.edges
        else:
            nodes = list(self.engine.nodes.values())[:max_nodes]
            edges = list(self.engine.edges.values())
        
        # Start diagram
        lines = ["graph TD"]
        
        # Define node styles
        node_styles = {
            LegalNodeType.STATUTE: "fill:#e1f5ff,stroke:#01579b",
            LegalNodeType.CASE: "fill:#fff3e0,stroke:#e65100",
            LegalNodeType.PRINCIPLE: "fill:#f3e5f5,stroke:#4a148c",
            LegalNodeType.SECTION: "fill:#e8f5e9,stroke:#1b5e20",
            LegalNodeType.CONCEPT: "fill:#fce4ec,stroke:#880e4f"
        }
        
        # Add nodes
        node_ids = {node.node_id for node in nodes}
        for node in nodes:
            label = self._escape_mermaid_text(node.name[:30])
            if include_node_types:
                label = f"{node.node_type.value}: {label}"
            
            # Format node based on type
            if node.node_type == LegalNodeType.STATUTE:
                lines.append(f'    {self._safe_id(node.node_id)}["{label}"]')
            elif node.node_type == LegalNodeType.CASE:
                lines.append(f'    {self._safe_id(node.node_id)}("{label}")')
            elif node.node_type == LegalNodeType.PRINCIPLE:
                lines.append(f'    {self._safe_id(node.node_id)}{{"{label}"}}')
            else:
                lines.append(f'    {self._safe_id(node.node_id)}["{label}"]')
        
        # Add edges (only between visible nodes)
        edge_count = 0
        for edge in edges:
            # Check if edge connects visible nodes
            visible_nodes = [nid for nid in edge.nodes if nid in node_ids]
            if len(visible_nodes) < 2:
                continue
            
            # For hyperedges with more than 2 nodes, create a hub
            if len(visible_nodes) > 2:
                hub_id = f"hub_{edge_count}"
                lines.append(f'    {hub_id}(( ))')
                
                for node_id in visible_nodes:
                    lines.append(f'    {self._safe_id(node_id)} --> {hub_id}')
                
                edge_count += 1
            else:
                # Simple edge between two nodes
                node_list = list(visible_nodes)
                label = edge.relation_type.value.replace("_", " ")
                lines.append(f'    {self._safe_id(node_list[0])} -->|{label}| {self._safe_id(node_list[1])}')
        
        # Add styling
        for node in nodes:
            style = node_styles.get(node.node_type, "fill:#f5f5f5,stroke:#666")
            lines.append(f'    style {self._safe_id(node.node_id)} {style}')
        
        return "\n".join(lines)
    
    def generate_dot_graph(
        self,
        query_result: Optional[QueryResult] = None,
        max_nodes: int = 50
    ) -> str:
        """
        Generate DOT/Graphviz representation.
        
        Args:
            query_result: Optional query result to visualize
            max_nodes: Maximum number of nodes
            
        Returns:
            DOT graph as string
        """
        # Get nodes and edges
        if query_result:
            nodes = query_result.nodes[:max_nodes]
            edges = query_result.edges
        else:
            nodes = list(self.engine.nodes.values())[:max_nodes]
            edges = list(self.engine.edges.values())
        
        lines = ["digraph LegalHypergraph {"]
        lines.append("    rankdir=TB;")
        lines.append("    node [shape=box, style=rounded];")
        
        # Define node styles
        node_colors = {
            LegalNodeType.STATUTE: "lightblue",
            LegalNodeType.CASE: "lightyellow",
            LegalNodeType.PRINCIPLE: "lavender",
            LegalNodeType.SECTION: "lightgreen",
            LegalNodeType.CONCEPT: "pink"
        }
        
        # Add nodes
        node_ids = {node.node_id for node in nodes}
        for node in nodes:
            label = self._escape_dot_text(node.name[:40])
            color = node_colors.get(node.node_type, "white")
            lines.append(f'    "{node.node_id}" [label="{label}", fillcolor={color}, style=filled];')
        
        # Add edges
        edge_count = 0
        for edge in edges:
            visible_nodes = [nid for nid in edge.nodes if nid in node_ids]
            if len(visible_nodes) < 2:
                continue
            
            if len(visible_nodes) > 2:
                # Create hyperedge hub
                hub_id = f"edge_{edge_count}"
                lines.append(f'    "{hub_id}" [label="", shape=circle, width=0.3, fillcolor=gray, style=filled];')
                
                for node_id in visible_nodes:
                    lines.append(f'    "{node_id}" -> "{hub_id}" [dir=none];')
                
                edge_count += 1
            else:
                # Simple edge
                node_list = list(visible_nodes)
                label = edge.relation_type.value
                lines.append(f'    "{node_list[0]}" -> "{node_list[1]}" [label="{label}"];')
        
        lines.append("}")
        
        return "\n".join(lines)
    
    def generate_network_stats_summary(
        self,
        query_result: Optional[QueryResult] = None
    ) -> Dict[str, Any]:
        """
        Generate network statistics summary.
        
        Args:
            query_result: Optional query result to analyze
            
        Returns:
            Statistics dictionary
        """
        # Get nodes and edges
        if query_result:
            nodes = {n.node_id: n for n in query_result.nodes}
            edges = query_result.edges
        else:
            nodes = self.engine.nodes
            edges = list(self.engine.edges.values())
        
        # Compute degree distribution
        degree_dist = {}
        for node_id in nodes:
            degree = len(self.engine.node_to_edges.get(node_id, set()))
            degree_dist[degree] = degree_dist.get(degree, 0) + 1
        
        # Compute hyperedge size distribution
        edge_size_dist = {}
        for edge in edges:
            size = len(edge.nodes)
            edge_size_dist[size] = edge_size_dist.get(size, 0) + 1
        
        # Find most connected nodes
        node_degrees = [
            (node_id, len(self.engine.node_to_edges.get(node_id, set())))
            for node_id in nodes
        ]
        node_degrees.sort(key=lambda x: x[1], reverse=True)
        top_nodes = [
            {
                "node_id": nid,
                "name": nodes[nid].name,
                "degree": deg,
                "type": nodes[nid].node_type.value
            }
            for nid, deg in node_degrees[:10]
        ]
        
        # Compute connected components (simple approximation)
        visited = set()
        num_components = 0
        
        def dfs(node_id):
            if node_id in visited:
                return
            visited.add(node_id)
            for edge_id in self.engine.node_to_edges.get(node_id, set()):
                edge = self.engine.edges.get(edge_id)
                if edge:
                    for neighbor_id in edge.nodes:
                        if neighbor_id != node_id:
                            dfs(neighbor_id)
        
        for node_id in nodes:
            if node_id not in visited:
                dfs(node_id)
                num_components += 1
        
        return {
            "num_nodes": len(nodes),
            "num_edges": len(edges),
            "degree_distribution": degree_dist,
            "hyperedge_size_distribution": edge_size_dist,
            "avg_degree": sum(deg for _, deg in node_degrees) / max(len(nodes), 1),
            "max_degree": node_degrees[0][1] if node_degrees else 0,
            "num_connected_components": num_components,
            "top_connected_nodes": top_nodes,
            "density": len(edges) / max(len(nodes) * (len(nodes) - 1) / 2, 1)
        }
    
    def export_to_json(
        self,
        query_result: Optional[QueryResult] = None,
        include_content: bool = False
    ) -> str:
        """
        Export graph to JSON format.
        
        Args:
            query_result: Optional query result to export
            include_content: Whether to include full content
            
        Returns:
            JSON string
        """
        # Get nodes and edges
        if query_result:
            nodes = query_result.nodes
            edges = query_result.edges
        else:
            nodes = list(self.engine.nodes.values())
            edges = list(self.engine.edges.values())
        
        # Build JSON structure
        graph_data = {
            "nodes": [],
            "edges": []
        }
        
        for node in nodes:
            node_data = {
                "id": node.node_id,
                "type": node.node_type.value,
                "name": node.name,
                "jurisdiction": node.jurisdiction
            }
            
            if include_content:
                node_data["content"] = node.content
                node_data["metadata"] = node.metadata
            
            graph_data["nodes"].append(node_data)
        
        for edge in edges:
            edge_data = {
                "id": edge.edge_id,
                "type": edge.relation_type.value,
                "nodes": list(edge.nodes),
                "weight": edge.weight
            }
            
            if include_content:
                edge_data["metadata"] = edge.metadata
            
            graph_data["edges"].append(edge_data)
        
        return json.dumps(graph_data, indent=2)
    
    def _safe_id(self, node_id: str) -> str:
        """Convert node ID to Mermaid-safe identifier."""
        return node_id.replace('-', '_').replace('.', '_').replace('/', '_')
    
    def _escape_mermaid_text(self, text: str) -> str:
        """Escape text for Mermaid diagram."""
        return text.replace('"', "'").replace('\n', ' ')
    
    def _escape_dot_text(self, text: str) -> str:
        """Escape text for DOT format."""
        return text.replace('"', '\\"').replace('\n', '\\n')


def visualize_query_result(
    engine: HypergraphQLEngine,
    query_result: QueryResult,
    output_format: str = "mermaid"
) -> str:
    """
    Helper function to visualize a query result.
    
    Args:
        engine: HypergraphQL engine
        query_result: Query result to visualize
        output_format: Output format ('mermaid', 'dot', 'json')
        
    Returns:
        Visualization string
    """
    visualizer = HypergraphVisualizer(engine)
    
    if output_format == "mermaid":
        return visualizer.generate_mermaid_diagram(query_result)
    elif output_format == "dot":
        return visualizer.generate_dot_graph(query_result)
    elif output_format == "json":
        return visualizer.export_to_json(query_result)
    else:
        raise ValueError(f"Unknown output format: {output_format}")
