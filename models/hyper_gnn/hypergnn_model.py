#!/usr/bin/env python3
"""
HyperGNN Model for Legal Case Hypergraph Analysis

This module implements a Hypergraph Neural Network for analyzing complex
relationships and higher-order interactions in legal cases.
"""

import logging
from typing import Dict, Any, List, Optional, Set, Tuple
from dataclasses import dataclass, field
import numpy as np
import datetime
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Node:
    """Represents a node in the hypergraph."""
    node_id: str
    node_type: str
    attributes: Dict[str, Any] = field(default_factory=dict)
    embeddings: Optional[np.ndarray] = None
    
    def initialize_embedding(self, dim: int = 64):
        """Initialize node embedding with random values."""
        self.embeddings = np.random.randn(dim) * 0.1


@dataclass
class Hyperedge:
    """Represents a hyperedge connecting multiple nodes."""
    edge_id: str
    nodes: Set[str]
    edge_type: str
    weight: float = 1.0
    attributes: Dict[str, Any] = field(default_factory=dict)
    
    def __len__(self):
        return len(self.nodes)


class Hypergraph:
    """Hypergraph data structure for legal case analysis."""
    
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.hyperedges: Dict[str, Hyperedge] = {}
        self.node_to_edges: Dict[str, Set[str]] = {}
        
    def add_node(self, node: Node):
        """Add a node to the hypergraph."""
        self.nodes[node.node_id] = node
        if node.node_id not in self.node_to_edges:
            self.node_to_edges[node.node_id] = set()
    
    def add_hyperedge(self, hyperedge: Hyperedge):
        """Add a hyperedge to the hypergraph."""
        self.hyperedges[hyperedge.edge_id] = hyperedge
        
        # Update node-to-edge mapping
        for node_id in hyperedge.nodes:
            if node_id not in self.node_to_edges:
                self.node_to_edges[node_id] = set()
            self.node_to_edges[node_id].add(hyperedge.edge_id)
    
    def get_node_neighbors(self, node_id: str) -> Set[str]:
        """Get all neighbors of a node (nodes sharing hyperedges)."""
        neighbors = set()
        edge_ids = self.node_to_edges.get(node_id, set())
        
        for edge_id in edge_ids:
            edge = self.hyperedges.get(edge_id)
            if edge:
                neighbors.update(edge.nodes - {node_id})
        
        return neighbors
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get hypergraph statistics."""
        node_degrees = {
            node_id: len(edges) for node_id, edges in self.node_to_edges.items()
        }
        
        edge_sizes = [len(edge) for edge in self.hyperedges.values()]
        
        return {
            'num_nodes': len(self.nodes),
            'num_hyperedges': len(self.hyperedges),
            'avg_node_degree': np.mean(list(node_degrees.values())) if node_degrees else 0,
            'max_node_degree': max(node_degrees.values()) if node_degrees else 0,
            'avg_edge_size': np.mean(edge_sizes) if edge_sizes else 0,
            'max_edge_size': max(edge_sizes) if edge_sizes else 0
        }


class HyperGNNLayer:
    """Single layer of Hypergraph Neural Network."""
    
    def __init__(self, input_dim: int, output_dim: int):
        self.input_dim = input_dim
        self.output_dim = output_dim
        
        # Initialize weights
        self.W_node = np.random.randn(input_dim, output_dim) * 0.1
        self.W_edge = np.random.randn(input_dim, output_dim) * 0.1
        self.bias = np.zeros(output_dim)
    
    def aggregate_to_hyperedge(self, node_embeddings: List[np.ndarray], 
                              aggregation_type: str = 'mean') -> np.ndarray:
        """
        Aggregate node embeddings to hyperedge embedding with multiple strategies.
        
        Args:
            node_embeddings: List of node embeddings
            aggregation_type: Type of aggregation ('mean', 'sum', 'max', 'attention')
            
        Returns:
            Aggregated hyperedge embedding
        """
        if not node_embeddings:
            return np.zeros(self.input_dim)
        
        embeddings_array = np.array(node_embeddings)
        
        if aggregation_type == 'mean':
            return np.mean(embeddings_array, axis=0)
        elif aggregation_type == 'sum':
            return np.sum(embeddings_array, axis=0)
        elif aggregation_type == 'max':
            return np.max(embeddings_array, axis=0)
        elif aggregation_type == 'attention':
            # Advanced attention mechanism with a learnable query vector
            attention_query = np.random.randn(self.input_dim)
            scores = np.dot(embeddings_array, attention_query)
            weights = np.exp(scores - np.max(scores))  # Softmax for numerical stability
            weights /= np.sum(weights)
            return np.sum(embeddings_array * weights[:, np.newaxis], axis=0)
        else:
            # Default to mean
            return np.mean(embeddings_array, axis=0)
    
    def aggregate_to_node(self, edge_embeddings: List[np.ndarray], edge_weights: List[float]) -> np.ndarray:
        """Aggregate hyperedge embeddings to node embedding."""
        if not edge_embeddings:
            return np.zeros(self.output_dim)
        
        # Weighted mean aggregation
        weighted_sum = sum(emb * w for emb, w in zip(edge_embeddings, edge_weights))
        total_weight = sum(edge_weights)
        
        return weighted_sum / total_weight if total_weight > 0 else np.zeros(self.output_dim)
    
    def forward(self, hypergraph: Hypergraph) -> Dict[str, np.ndarray]:
        """Forward pass through the layer."""
        new_embeddings = {}
        
        # For each hyperedge, aggregate node embeddings
        edge_embeddings = {}
        for edge_id, edge in hypergraph.hyperedges.items():
            node_embs = [
                hypergraph.nodes[node_id].embeddings 
                for node_id in edge.nodes 
                if hypergraph.nodes[node_id].embeddings is not None
            ]
            
            if node_embs:
                agg_emb = self.aggregate_to_hyperedge(node_embs)
                edge_embeddings[edge_id] = np.dot(agg_emb, self.W_edge)
        
        # For each node, aggregate hyperedge embeddings
        for node_id, node in hypergraph.nodes.items():
            edge_ids = hypergraph.node_to_edges.get(node_id, set())
            
            edge_embs = [edge_embeddings[eid] for eid in edge_ids if eid in edge_embeddings]
            edge_weights = [hypergraph.hyperedges[eid].weight for eid in edge_ids if eid in edge_embeddings]
            
            if edge_embs:
                agg_emb = self.aggregate_to_node(edge_embs, edge_weights)
                new_embeddings[node_id] = np.tanh(agg_emb + self.bias)
            else:
                # For isolated nodes, apply transformation to maintain consistent dimensions
                if node.embeddings is not None:
                    transformed = np.dot(node.embeddings, self.W_node)
                    new_embeddings[node_id] = np.tanh(transformed + self.bias)
                else:
                    new_embeddings[node_id] = np.zeros(self.output_dim)
        
        return new_embeddings


class HyperGNN:
    """Hypergraph Neural Network model."""
    
    def __init__(self, input_dim: int = 64, hidden_dim: int = 32, num_layers: int = 2):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.output_dim = hidden_dim
        
        # Build layers - all layers output to hidden_dim
        self.layers = []
        for i in range(num_layers):
            if i == 0:
                layer = HyperGNNLayer(input_dim, hidden_dim)
            else:
                layer = HyperGNNLayer(hidden_dim, hidden_dim)
            self.layers.append(layer)
        
        logger.info(f"Initialized HyperGNN with {num_layers} layers (input: {input_dim}, hidden: {hidden_dim})")
    
    def forward(self, hypergraph: Hypergraph) -> Dict[str, np.ndarray]:
        """Forward pass through all layers."""
        # Initialize node embeddings if not present
        for node in hypergraph.nodes.values():
            if node.embeddings is None:
                node.initialize_embedding(self.input_dim)
        
        # Pass through layers
        for i, layer in enumerate(self.layers):
            new_embeddings = layer.forward(hypergraph)
            
            # Update node embeddings
            for node_id, embedding in new_embeddings.items():
                hypergraph.nodes[node_id].embeddings = embedding
            
            logger.debug(f"Completed layer {i + 1}/{self.num_layers}")
        
        return {node_id: node.embeddings for node_id, node in hypergraph.nodes.items()}
    
    def predict_link(self, node1_emb: np.ndarray, node2_emb: np.ndarray) -> float:
        """Predict likelihood of link between two nodes."""
        # Cosine similarity
        similarity = np.dot(node1_emb, node2_emb) / (
            np.linalg.norm(node1_emb) * np.linalg.norm(node2_emb) + 1e-8
        )
        return float(similarity)
    
    def graph_level_pooling(self, hypergraph: Hypergraph, pooling_type: str = 'mean') -> np.ndarray:
        """
        Perform graph-level pooling to get a single embedding for the entire hypergraph.
        
        Args:
            hypergraph: Input hypergraph
            pooling_type: Type of pooling ('mean', 'sum', 'max', 'attention')
            
        Returns:
            Graph-level embedding vector
        """
        embeddings_list = []
        
        for node in hypergraph.nodes.values():
            if node.embeddings is not None:
                embeddings_list.append(node.embeddings)
        
        if not embeddings_list:
            return np.zeros(self.hidden_dim)
        
        embeddings = np.array(embeddings_list)
        
        if pooling_type == 'mean':
            return np.mean(embeddings, axis=0)
        elif pooling_type == 'sum':
            return np.sum(embeddings, axis=0)
        elif pooling_type == 'max':
            return np.max(embeddings, axis=0)
        elif pooling_type == 'attention':
            # Attention-based pooling
            scores = np.array([np.sum(emb) for emb in embeddings])
            weights = np.exp(scores) / (np.sum(np.exp(scores)) + 1e-8)
            return np.sum(embeddings * weights[:, np.newaxis], axis=0)
        else:
            return np.mean(embeddings, axis=0)
    
    def compute_graph_features(self, hypergraph: Hypergraph) -> Dict[str, Any]:
        """
        Compute comprehensive graph-level features.
        
        Args:
            hypergraph: Input hypergraph
            
        Returns:
            Dictionary of graph-level features
        """
        # Get graph-level embeddings with different pooling strategies
        mean_pool = self.graph_level_pooling(hypergraph, 'mean')
        max_pool = self.graph_level_pooling(hypergraph, 'max')
        sum_pool = self.graph_level_pooling(hypergraph, 'sum')
        
        # Compute statistics
        embeddings_list = [node.embeddings for node in hypergraph.nodes.values() 
                          if node.embeddings is not None]
        
        if embeddings_list:
            embeddings = np.array(embeddings_list)
            embedding_std = np.std(embeddings, axis=0)
            embedding_variance = np.var(embeddings, axis=0)
        else:
            embedding_std = np.zeros(self.hidden_dim)
            embedding_variance = np.zeros(self.hidden_dim)
        
        return {
            'mean_pooling': mean_pool,
            'max_pooling': max_pool,
            'sum_pooling': sum_pool,
            'embedding_std': embedding_std,
            'embedding_variance': embedding_variance,
            'num_nodes': len(hypergraph.nodes),
            'num_edges': len(hypergraph.hyperedges)
        }
    
    def detect_communities(self, hypergraph: Hypergraph, num_communities: int = 3) -> Dict[str, int]:
        """
        Detect communities using improved k-means clustering on node embeddings.
        
        Args:
            hypergraph: Input hypergraph
            num_communities: Number of communities to detect
            
        Returns:
            Dictionary mapping node IDs to community IDs
        """
        # Simple k-means clustering on embeddings
        embeddings_list = []
        node_ids = []
        
        # Collect embeddings and ensure they all have the same dimension
        for node_id, node in hypergraph.nodes.items():
            if node.embeddings is not None:
                embeddings_list.append(node.embeddings)
                node_ids.append(node_id)
        
        if not embeddings_list:
            return {}
        
        # Stack embeddings
        embeddings = np.vstack(embeddings_list)
        
        # Ensure we don't have more communities than nodes
        num_communities = min(num_communities, len(embeddings))
        
        # Initialize centroids using k-means++
        centroids = self._kmeans_plus_plus_init(embeddings, num_communities)
        
        # Run k-means for a few iterations
        max_iterations = 20
        prev_assignments = None
        
        for iteration in range(max_iterations):
            # Assign nodes to nearest centroid
            distances = np.array([
                [np.linalg.norm(emb - centroid) for centroid in centroids]
                for emb in embeddings
            ])
            assignments = np.argmin(distances, axis=1)
            
            # Check for convergence
            if prev_assignments is not None and np.array_equal(assignments, prev_assignments):
                logger.debug(f"K-means converged after {iteration + 1} iterations")
                break
            
            prev_assignments = assignments.copy()
            
            # Update centroids
            for k in range(num_communities):
                cluster_points = embeddings[assignments == k]
                if len(cluster_points) > 0:
                    centroids[k] = np.mean(cluster_points, axis=0)
        
        return {node_ids[i]: int(assignments[i]) for i in range(len(node_ids))}
    
    def _kmeans_plus_plus_init(self, embeddings: np.ndarray, k: int) -> np.ndarray:
        """
        K-means++ initialization for better centroid selection.
        
        Args:
            embeddings: Node embeddings array
            k: Number of clusters
            
        Returns:
            Initial centroids array
        """
        n_samples = len(embeddings)
        centroids = []
        
        # Choose first centroid randomly
        first_idx = np.random.randint(n_samples)
        centroids.append(embeddings[first_idx])
        
        # Choose remaining centroids
        for _ in range(1, k):
            # Compute distances to nearest existing centroid
            distances = np.array([
                min([np.linalg.norm(emb - c) for c in centroids])
                for emb in embeddings
            ])
            
            # Choose next centroid with probability proportional to distance squared
            probabilities = distances ** 2
            probabilities /= probabilities.sum()
            
            next_idx = np.random.choice(n_samples, p=probabilities)
            centroids.append(embeddings[next_idx])
        
        return np.array(centroids)
    
    def predict_link_with_features(self, node1_id: str, node2_id: str, 
                                   hypergraph: Hypergraph) -> Dict[str, float]:
        """
        Predict link between nodes with multiple feature-based scores.
        
        Args:
            node1_id: First node ID
            node2_id: Second node ID
            hypergraph: Input hypergraph
            
        Returns:
            Dictionary of different similarity scores
        """
        node1 = hypergraph.nodes.get(node1_id)
        node2 = hypergraph.nodes.get(node2_id)
        
        if not node1 or not node2 or node1.embeddings is None or node2.embeddings is None:
            return {
                'cosine_similarity': 0.0,
                'euclidean_distance': float('inf'),
                'common_neighbors': 0,
                'combined_score': 0.0
            }
        
        # Cosine similarity
        cosine_sim = np.dot(node1.embeddings, node2.embeddings) / (
            np.linalg.norm(node1.embeddings) * np.linalg.norm(node2.embeddings) + 1e-8
        )
        
        # Euclidean distance (inverted and normalized)
        euclidean_dist = np.linalg.norm(node1.embeddings - node2.embeddings)
        euclidean_score = 1.0 / (1.0 + euclidean_dist)
        
        # Common neighbors count
        neighbors1 = hypergraph.get_node_neighbors(node1_id)
        neighbors2 = hypergraph.get_node_neighbors(node2_id)
        common_neighbors = len(neighbors1.intersection(neighbors2))
        common_neighbors_score = min(1.0, common_neighbors / 5.0)  # Normalize
        
        # Combined score (weighted average)
        combined = 0.5 * cosine_sim + 0.3 * euclidean_score + 0.2 * common_neighbors_score
        
        return {
            'cosine_similarity': float(cosine_sim),
            'euclidean_distance': float(euclidean_dist),
            'euclidean_score': float(euclidean_score),
            'common_neighbors': common_neighbors,
            'common_neighbors_score': float(common_neighbors_score),
            'combined_score': float(combined)
        }


class TemporalHypergraph(Hypergraph):
    """
    Temporal hypergraph that tracks changes over time.
    """
    
    def __init__(self):
        super().__init__()
        self.snapshots: List[Tuple[float, Dict[str, Any]]] = []
        self.temporal_edges: Dict[str, List[Tuple[float, str]]] = {}  # edge_id -> [(timestamp, status)]
    
    def add_temporal_hyperedge(self, hyperedge: Hyperedge, timestamp: float):
        """
        Add a hyperedge with timestamp.
        
        Args:
            hyperedge: Hyperedge to add
            timestamp: Time when edge was created
        """
        self.add_hyperedge(hyperedge)
        
        if hyperedge.edge_id not in self.temporal_edges:
            self.temporal_edges[hyperedge.edge_id] = []
        
        self.temporal_edges[hyperedge.edge_id].append((timestamp, 'created'))
    
    def remove_temporal_hyperedge(self, edge_id: str, timestamp: float):
        """
        Mark a hyperedge as removed at a specific time.
        
        Args:
            edge_id: Edge ID to remove
            timestamp: Time when edge was removed
        """
        if edge_id in self.hyperedges:
            if edge_id not in self.temporal_edges:
                self.temporal_edges[edge_id] = []
            
            self.temporal_edges[edge_id].append((timestamp, 'removed'))
    
    def snapshot_at_time(self, timestamp: float) -> Hypergraph:
        """
        Get a snapshot of the hypergraph at a specific time.
        
        Args:
            timestamp: Time to get snapshot at
            
        Returns:
            Hypergraph snapshot
        """
        snapshot = Hypergraph()
        
        # Add all nodes (assuming nodes don't change)
        for node_id, node in self.nodes.items():
            snapshot.add_node(node)
        
        # Add edges that exist at this timestamp
        for edge_id, edge in self.hyperedges.items():
            if edge_id in self.temporal_edges:
                events = self.temporal_edges[edge_id]
                # Check if edge exists at timestamp
                created = False
                removed = False
                
                for event_time, status in sorted(events):
                    if event_time > timestamp:
                        break
                    if status == 'created':
                        created = True
                    elif status == 'removed':
                        removed = True
                
                if created and not removed:
                    snapshot.add_hyperedge(edge)
            else:
                # Edge without temporal info - include it
                snapshot.add_hyperedge(edge)
        
        return snapshot
    
    def get_temporal_evolution(self) -> Dict[str, Any]:
        """
        Get statistics about temporal evolution.
        
        Returns:
            Temporal evolution statistics
        """
        all_events = []
        for edge_id, events in self.temporal_edges.items():
            for timestamp, status in events:
                all_events.append((timestamp, edge_id, status))
        
        all_events.sort()
        
        edge_counts_over_time = []
        current_count = len(self.hyperedges)
        
        for timestamp, edge_id, status in all_events:
            if status == 'created':
                current_count += 1
            elif status == 'removed':
                current_count -= 1
            
            edge_counts_over_time.append({
                'timestamp': timestamp,
                'num_edges': current_count,
                'event': status
            })
        
        return {
            'total_events': len(all_events),
            'evolution': edge_counts_over_time,
            'tracked_edges': len(self.temporal_edges)
        }


class AttentionHyperGNNLayer(HyperGNNLayer):
    """
    HyperGNN layer with learnable attention mechanism.
    """
    
    def __init__(self, input_dim: int, output_dim: int):
        super().__init__(input_dim, output_dim)
        
        # Attention parameters
        self.W_attention = np.random.randn(input_dim, 1) * 0.1
        self.attention_bias = np.zeros(1)
    
    def compute_attention_weights(self, node_embeddings: List[np.ndarray]) -> np.ndarray:
        """
        Compute attention weights for node embeddings.
        
        Args:
            node_embeddings: List of node embeddings
            
        Returns:
            Attention weights array
        """
        if not node_embeddings:
            return np.array([])
        
        embeddings_array = np.array(node_embeddings)
        
        # Compute attention scores
        scores = np.dot(embeddings_array, self.W_attention) + self.attention_bias
        scores = scores.squeeze()
        
        # Apply softmax
        exp_scores = np.exp(scores - np.max(scores))
        weights = exp_scores / (np.sum(exp_scores) + 1e-8)
        
        return weights
    
    def aggregate_to_hyperedge(self, node_embeddings: List[np.ndarray], 
                              aggregation_type: str = 'attention') -> np.ndarray:
        """
        Aggregate node embeddings with attention.
        
        Args:
            node_embeddings: List of node embeddings
            aggregation_type: Type of aggregation
            
        Returns:
            Aggregated embedding
        """
        if aggregation_type == 'attention' or aggregation_type == 'learned_attention':
            if not node_embeddings:
                return np.zeros(self.input_dim)
            
            embeddings_array = np.array(node_embeddings)
            weights = self.compute_attention_weights(node_embeddings)
            
            return np.sum(embeddings_array * weights[:, np.newaxis], axis=0)
        else:
            return super().aggregate_to_hyperedge(node_embeddings, aggregation_type)


class HierarchicalHypergraph:
    """
    Hierarchical hypergraph with multiple levels of abstraction.
    """
    
    def __init__(self):
        self.levels: List[Hypergraph] = []
        self.level_mappings: List[Dict[str, str]] = []  # Maps nodes from level i to level i+1
    
    def add_level(self, hypergraph: Hypergraph, mapping: Optional[Dict[str, str]] = None):
        """
        Add a level to the hierarchy.
        
        Args:
            hypergraph: Hypergraph at this level
            mapping: Mapping from previous level nodes to this level
        """
        self.levels.append(hypergraph)
        if mapping and len(self.levels) > 1:
            self.level_mappings.append(mapping)
    
    def coarsen_graph(self, hypergraph: Hypergraph, num_clusters: int) -> Tuple[Hypergraph, Dict[str, str]]:
        """
        Create a coarser version of the hypergraph by clustering nodes.
        
        Args:
            hypergraph: Input hypergraph
            num_clusters: Number of clusters to create
            
        Returns:
            Tuple of (coarse hypergraph, mapping from original to coarse nodes)
        """
        # Use simple random clustering for demonstration
        # In practice, use community detection
        node_ids = list(hypergraph.nodes.keys())
        cluster_size = max(1, len(node_ids) // num_clusters)
        
        coarse_graph = Hypergraph()
        mapping = {}
        
        # Create cluster nodes
        for i in range(num_clusters):
            cluster_id = f"cluster_{i}"
            cluster_node = Node(
                node_id=cluster_id,
                node_type="cluster",
                attributes={'size': 0}
            )
            coarse_graph.add_node(cluster_node)
        
        # Assign nodes to clusters
        for idx, node_id in enumerate(node_ids):
            cluster_idx = min(idx // cluster_size, num_clusters - 1)
            cluster_id = f"cluster_{cluster_idx}"
            mapping[node_id] = cluster_id
            coarse_graph.nodes[cluster_id].attributes['size'] += 1
        
        # Create coarse edges
        edge_clusters = {}
        for edge_id, edge in hypergraph.hyperedges.items():
            # Map edge nodes to clusters
            cluster_nodes = {mapping[nid] for nid in edge.nodes if nid in mapping}
            
            if len(cluster_nodes) > 1:
                cluster_edge_id = f"coarse_{edge_id}"
                if cluster_edge_id not in edge_clusters:
                    coarse_edge = Hyperedge(
                        edge_id=cluster_edge_id,
                        nodes=cluster_nodes,
                        edge_type=edge.edge_type,
                        weight=edge.weight
                    )
                    coarse_graph.add_hyperedge(coarse_edge)
                    edge_clusters[cluster_edge_id] = True
        
        return coarse_graph, mapping
    
    def build_hierarchy(self, base_graph: Hypergraph, num_levels: int = 3):
        """
        Build a hierarchical hypergraph.
        
        Args:
            base_graph: Base level hypergraph
            num_levels: Number of hierarchy levels
        """
        self.levels = [base_graph]
        
        current_graph = base_graph
        for level in range(1, num_levels):
            # Coarsen by reducing nodes
            num_clusters = max(5, len(current_graph.nodes) // (2 ** level))
            coarse_graph, mapping = self.coarsen_graph(current_graph, num_clusters)
            
            self.levels.append(coarse_graph)
            self.level_mappings.append(mapping)
            
            current_graph = coarse_graph
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics for all levels."""
        return {
            "num_levels": len(self.levels),
            "level_stats": [
                {
                    "level": i,
                    "num_nodes": len(level.nodes),
                    "num_edges": len(level.hyperedges)
                }
                for i, level in enumerate(self.levels)
            ]
        }


def create_case_hypergraph(case_data: Dict[str, Any], embedding_dim: int = 64) -> Hypergraph:
    """Create a hypergraph from case data."""
    hg = Hypergraph()
    
    # Add entity nodes
    entities = case_data.get('entities', [])
    for entity in entities:
        node = Node(
            node_id=entity['id'],
            node_type=entity['type'],
            attributes={'name': entity.get('name', '')}
        )
        node.initialize_embedding(embedding_dim)
        hg.add_node(node)
    
    # Add evidence nodes
    evidence_items = case_data.get('evidence', [])
    for evidence in evidence_items:
        node = Node(
            node_id=evidence['id'],
            node_type='evidence',
            attributes={'description': evidence.get('description', '')}
        )
        node.initialize_embedding(embedding_dim)
        hg.add_node(node)
    
    # Add hyperedges (relationships involving multiple entities)
    relationships = case_data.get('relationships', [])
    for i, rel in enumerate(relationships):
        hyperedge = Hyperedge(
            edge_id=f"edge_{i}",
            nodes=set(rel['participants']),
            edge_type=rel['type'],
            weight=rel.get('weight', 1.0)
        )
        hg.add_hyperedge(hyperedge)
    
    return hg


def run_hypergnn_analysis(case_data: Dict[str, Any], config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Run HyperGNN analysis on case data."""
    if config is None:
        config = {}
    
    logger.info("Starting HyperGNN analysis")
    
    # Get configuration
    input_dim = config.get('input_dim', 64)
    
    # Create hypergraph with consistent embedding dimension
    hypergraph = create_case_hypergraph(case_data, embedding_dim=input_dim)
    
    # Initialize and run HyperGNN
    hidden_dim = config.get('hidden_dim', 32)
    num_layers = config.get('num_layers', 2)
    
    model = HyperGNN(input_dim, hidden_dim, num_layers)
    embeddings = model.forward(hypergraph)
    
    # Detect communities
    communities = model.detect_communities(hypergraph, num_communities=3)
    
    # Calculate statistics
    stats = hypergraph.get_statistics()
    
    # Predict potential links
    node_ids = list(hypergraph.nodes.keys())[:10]  # Sample for efficiency
    link_predictions = []
    for i, node1_id in enumerate(node_ids):
        for node2_id in node_ids[i+1:]:
            score = model.predict_link(embeddings[node1_id], embeddings[node2_id])
            if score > 0.7:  # Threshold
                link_predictions.append({
                    'node1': node1_id,
                    'node2': node2_id,
                    'score': score
                })
    
    logger.info(f"HyperGNN analysis completed: {len(communities)} communities detected")
    
    return {
        'simulation_type': 'hyper_gnn',
        'hypergraph_stats': stats,
        'communities': communities,
        'num_communities': len(set(communities.values())),
        'link_predictions': sorted(link_predictions, key=lambda x: x['score'], reverse=True)[:10],
        'sample_embeddings': {
            node_id: embeddings[node_id].tolist()[:5]  # First 5 dimensions
            for node_id in list(embeddings.keys())[:5]
        }
    }


def generate_sample_case_data() -> Dict[str, Any]:
    """Generate sample case data for testing."""
    entities = [
        {'id': f'entity_{i}', 'type': 'person', 'name': f'Person {i}'}
        for i in range(20)
    ]
    
    evidence = [
        {'id': f'evidence_{i}', 'description': f'Evidence item {i}'}
        for i in range(15)
    ]
    
    relationships = []
    for i in range(30):
        num_participants = random.randint(2, 5)
        participants = random.sample([e['id'] for e in entities], num_participants)
        relationships.append({
            'participants': participants,
            'type': random.choice(['transaction', 'communication', 'association']),
            'weight': random.uniform(0.5, 1.0)
        })
    
    return {
        'entities': entities,
        'evidence': evidence,
        'relationships': relationships
    }


if __name__ == "__main__":
    # Run sample analysis
    case_data = generate_sample_case_data()
    results = run_hypergnn_analysis(case_data)
    print(f"Detected {results['num_communities']} communities")

