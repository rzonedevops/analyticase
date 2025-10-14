#!/usr/bin/env python3
"""
Tests for GGMLEX framework

This module contains basic tests for the GGMLEX ML framework components.
"""

import sys
import os
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pytest
import numpy as np

from models.ggmlex import (
    GGMLContext, GGMLTensor,
    LegalLLM, LegalLLMConfig, LegalDocument,
    LegalTransformer, TransformerConfig,
    HypergraphQLEngine, LegalNode, LegalHyperedge,
    LegalNodeType, LegalRelationType
)

logging.basicConfig(level=logging.WARNING)


class TestGGML:
    """Tests for GGML module."""
    
    def test_tensor_creation(self):
        """Test creating a GGML tensor."""
        tensor = GGMLTensor(name="test", shape=(3, 4))
        assert tensor.name == "test"
        assert tensor.shape == (3, 4)
        assert tensor.size() == 12
    
    def test_context_creation(self):
        """Test creating a GGML context."""
        ctx = GGMLContext()
        assert ctx._initialized
        assert len(ctx.tensors) == 0
    
    def test_matmul(self):
        """Test matrix multiplication."""
        ctx = GGMLContext()
        a = ctx.create_tensor("a", (3, 4))
        a.data = np.ones((3, 4))
        
        b = ctx.create_tensor("b", (4, 5))
        b.data = np.ones((4, 5))
        
        c = ctx.matmul(a, b)
        assert c.shape == (3, 5)
        assert np.allclose(c.data, np.ones((3, 5)) * 4)
    
    def test_attention(self):
        """Test attention mechanism."""
        ctx = GGMLContext()
        q = ctx.create_tensor("q", (10, 64))
        q.data = np.random.randn(10, 64).astype(np.float32)
        
        k = ctx.create_tensor("k", (10, 64))
        k.data = np.random.randn(10, 64).astype(np.float32)
        
        v = ctx.create_tensor("v", (10, 64))
        v.data = np.random.randn(10, 64).astype(np.float32)
        
        output = ctx.attention(q, k, v)
        assert output.shape == (10, 64)


class TestLegalLLM:
    """Tests for Legal LLM."""
    
    def test_llm_initialization(self):
        """Test LLM initialization."""
        config = LegalLLMConfig(
            vocab_size=1000,
            embedding_dim=128,
            num_layers=2
        )
        llm = LegalLLM(config)
        assert llm.config.vocab_size == 1000
        assert llm.config.embedding_dim == 128
        assert llm.config.num_layers == 2
        llm.cleanup()
    
    def test_document_encoding(self):
        """Test document encoding."""
        config = LegalLLMConfig(vocab_size=1000, embedding_dim=128, num_layers=2)
        llm = LegalLLM(config)
        
        doc = LegalDocument(
            text="The court held that the contract was valid.",
            doc_type="case_law"
        )
        
        embeddings = llm.encode(doc)
        assert embeddings.shape[1] == 128  # embedding dimension
        assert len(doc.tokens) > 0
        llm.cleanup()
    
    def test_case_analysis(self):
        """Test case analysis."""
        config = LegalLLMConfig(vocab_size=1000, embedding_dim=128, num_layers=2)
        llm = LegalLLM(config)
        
        analysis = llm.analyze_case("The plaintiff sued for breach of contract.")
        assert "document_type" in analysis
        assert analysis["document_type"] == "case_law"
        assert "num_tokens" in analysis
        llm.cleanup()


class TestLegalTransformer:
    """Tests for Legal Transformer."""
    
    def test_transformer_initialization(self):
        """Test transformer initialization."""
        config = TransformerConfig(
            vocab_size=1000,
            embedding_dim=128,
            num_heads=4,
            num_layers=2
        )
        transformer = LegalTransformer(config)
        assert transformer.config.vocab_size == 1000
        assert len(transformer.layers) == 2
        transformer.cleanup()
    
    def test_text_encoding(self):
        """Test text encoding."""
        config = TransformerConfig(
            vocab_size=1000,
            embedding_dim=128,
            num_heads=4,
            num_layers=2
        )
        transformer = LegalTransformer(config)
        
        embeddings = transformer.encode("The contract is binding.")
        assert embeddings.shape[1] == 128
        transformer.cleanup()
    
    def test_legal_text_analysis(self):
        """Test legal text analysis."""
        config = TransformerConfig(
            vocab_size=1000,
            embedding_dim=128,
            num_heads=4,
            num_layers=2
        )
        transformer = LegalTransformer(config)
        
        analysis = transformer.analyze_legal_text("The statute requires notice.")
        assert "text_length" in analysis
        assert "num_tokens" in analysis
        transformer.cleanup()


class TestHypergraphQL:
    """Tests for HypergraphQL engine."""
    
    def test_engine_initialization(self):
        """Test engine initialization."""
        engine = HypergraphQLEngine()
        assert engine.schema is not None
        assert isinstance(engine.nodes, dict)
        assert isinstance(engine.edges, dict)
    
    def test_add_node(self):
        """Test adding a node."""
        engine = HypergraphQLEngine()
        
        node = LegalNode(
            node_id="test_001",
            node_type=LegalNodeType.STATUTE,
            name="Test Statute",
            jurisdiction="za"
        )
        engine.add_node(node)
        
        assert "test_001" in engine.nodes
        assert engine.get_node("test_001") == node
    
    def test_add_edge(self):
        """Test adding an edge."""
        engine = HypergraphQLEngine()
        
        node1 = LegalNode(
            node_id="node_001",
            node_type=LegalNodeType.CASE,
            name="Case 1",
            jurisdiction="za"
        )
        node2 = LegalNode(
            node_id="node_002",
            node_type=LegalNodeType.STATUTE,
            name="Statute 1",
            jurisdiction="za"
        )
        
        engine.add_node(node1)
        engine.add_node(node2)
        
        edge = LegalHyperedge(
            edge_id="edge_001",
            relation_type=LegalRelationType.CITES,
            nodes={node1.node_id, node2.node_id}
        )
        engine.add_edge(edge)
        
        assert "edge_001" in engine.edges
    
    def test_query_nodes(self):
        """Test querying nodes."""
        engine = HypergraphQLEngine()
        
        # Add test nodes
        for i in range(5):
            node = LegalNode(
                node_id=f"case_{i}",
                node_type=LegalNodeType.CASE,
                name=f"Case {i}",
                jurisdiction="za"
            )
            engine.add_node(node)
        
        result = engine.query_nodes(node_type=LegalNodeType.CASE)
        # Should find at least our 5 test cases
        assert len(result) >= 5
    
    def test_query_neighbors(self):
        """Test querying neighbors."""
        engine = HypergraphQLEngine()
        
        # Create nodes
        node1 = LegalNode(
            node_id="statute_test",
            node_type=LegalNodeType.STATUTE,
            name="Test Statute",
            jurisdiction="za"
        )
        node2 = LegalNode(
            node_id="case_test",
            node_type=LegalNodeType.CASE,
            name="Test Case",
            jurisdiction="za"
        )
        
        engine.add_node(node1)
        engine.add_node(node2)
        
        # Create edge
        edge = LegalHyperedge(
            edge_id="edge_test",
            relation_type=LegalRelationType.CITES,
            nodes={node1.node_id, node2.node_id}
        )
        engine.add_edge(edge)
        
        # Query neighbors
        result = engine.query_neighbors(node1.node_id)
        assert len(result) >= 1
    
    def test_query_path(self):
        """Test path finding."""
        engine = HypergraphQLEngine()
        
        # Create a chain of nodes
        nodes = []
        for i in range(3):
            node = LegalNode(
                node_id=f"node_{i}",
                node_type=LegalNodeType.CASE,
                name=f"Case {i}",
                jurisdiction="za"
            )
            engine.add_node(node)
            nodes.append(node)
        
        # Create edges
        for i in range(2):
            edge = LegalHyperedge(
                edge_id=f"edge_{i}",
                relation_type=LegalRelationType.FOLLOWS,
                nodes={nodes[i].node_id, nodes[i+1].node_id}
            )
            engine.add_edge(edge)
        
        # Find path
        result = engine.query_path(nodes[0].node_id, nodes[2].node_id)
        assert len(result) >= 2  # Should find a path
    
    def test_legal_framework_loading(self):
        """Test loading legal framework from lex/."""
        engine = HypergraphQLEngine()
        
        # Should have loaded principles from lex/
        result = engine.query_nodes(node_type=LegalNodeType.PRINCIPLE)
        # The engine loads from lex/ so should have some principles
        assert len(result) > 0
    
    def test_statistics(self):
        """Test getting statistics."""
        engine = HypergraphQLEngine()
        
        stats = engine.get_statistics()
        assert "num_nodes" in stats
        assert "num_edges" in stats
        assert "node_types" in stats


def run_tests():
    """Run all tests."""
    print("Running GGMLEX tests...")
    
    # Run tests using pytest
    exit_code = pytest.main([__file__, "-v", "-s"])
    
    return exit_code


if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
