#!/usr/bin/env python3
"""
GGML Python Bindings for Legal ML Framework

This module provides Python bindings for GGML (Georgi Gerganov Machine Learning)
tensor operations optimized for legal document processing and analysis.
"""

import logging
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
import ctypes
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class GGMLTensor:
    """Represents a GGML tensor for ML operations."""
    
    name: str
    shape: Tuple[int, ...]
    dtype: str = "float32"
    data: Optional[np.ndarray] = None
    
    def __post_init__(self):
        """Initialize tensor data if not provided."""
        if self.data is None:
            self.data = np.zeros(self.shape, dtype=self.dtype)
    
    def size(self) -> int:
        """Return total number of elements in tensor."""
        return int(np.prod(self.shape))
    
    def reshape(self, new_shape: Tuple[int, ...]) -> 'GGMLTensor':
        """Reshape tensor to new dimensions."""
        if np.prod(new_shape) != self.size():
            raise ValueError(f"Cannot reshape tensor of size {self.size()} to {new_shape}")
        
        return GGMLTensor(
            name=self.name,
            shape=new_shape,
            dtype=self.dtype,
            data=self.data.reshape(new_shape)
        )
    
    def __repr__(self) -> str:
        return f"GGMLTensor(name='{self.name}', shape={self.shape}, dtype='{self.dtype}')"


class GGMLContext:
    """
    GGML Context manager for tensor operations and memory management.
    
    This provides a high-level interface to GGML operations optimized
    for legal document processing.
    """
    
    def __init__(self, memory_size: int = 128 * 1024 * 1024):
        """
        Initialize GGML context.
        
        Args:
            memory_size: Memory allocation size in bytes (default 128MB)
        """
        self.memory_size = memory_size
        self.tensors: Dict[str, GGMLTensor] = {}
        self._initialized = False
        logger.info(f"Initialized GGML context with {memory_size / (1024*1024):.1f}MB memory")
        self._initialized = True
    
    def create_tensor(self, name: str, shape: Tuple[int, ...], dtype: str = "float32") -> GGMLTensor:
        """
        Create a new tensor in the context.
        
        Args:
            name: Tensor name
            shape: Tensor dimensions
            dtype: Data type
            
        Returns:
            Created tensor
        """
        if name in self.tensors:
            logger.warning(f"Tensor '{name}' already exists, overwriting")
        
        tensor = GGMLTensor(name=name, shape=shape, dtype=dtype)
        self.tensors[name] = tensor
        logger.debug(f"Created tensor: {tensor}")
        
        return tensor
    
    def get_tensor(self, name: str) -> Optional[GGMLTensor]:
        """Get tensor by name."""
        return self.tensors.get(name)
    
    def matmul(self, a: GGMLTensor, b: GGMLTensor, name: str = "matmul_result") -> GGMLTensor:
        """
        Matrix multiplication operation.
        
        Args:
            a: First tensor
            b: Second tensor
            name: Result tensor name
            
        Returns:
            Result tensor
        """
        if len(a.shape) != 2 or len(b.shape) != 2:
            raise ValueError("Matrix multiplication requires 2D tensors")
        
        if a.shape[1] != b.shape[0]:
            raise ValueError(f"Incompatible shapes for matmul: {a.shape} and {b.shape}")
        
        result_data = np.matmul(a.data, b.data)
        result = GGMLTensor(
            name=name,
            shape=result_data.shape,
            dtype=a.dtype,
            data=result_data
        )
        
        self.tensors[name] = result
        logger.debug(f"Matmul: {a.shape} @ {b.shape} = {result.shape}")
        
        return result
    
    def add(self, a: GGMLTensor, b: GGMLTensor, name: str = "add_result") -> GGMLTensor:
        """Element-wise addition."""
        if a.shape != b.shape:
            raise ValueError(f"Shape mismatch for addition: {a.shape} vs {b.shape}")
        
        result_data = a.data + b.data
        result = GGMLTensor(name=name, shape=a.shape, dtype=a.dtype, data=result_data)
        self.tensors[name] = result
        
        return result
    
    def layer_norm(self, x: GGMLTensor, eps: float = 1e-5, name: str = "norm_result") -> GGMLTensor:
        """
        Layer normalization operation.
        
        Args:
            x: Input tensor
            eps: Epsilon for numerical stability
            name: Result tensor name
            
        Returns:
            Normalized tensor
        """
        mean = np.mean(x.data, axis=-1, keepdims=True)
        var = np.var(x.data, axis=-1, keepdims=True)
        normalized = (x.data - mean) / np.sqrt(var + eps)
        
        result = GGMLTensor(name=name, shape=x.shape, dtype=x.dtype, data=normalized)
        self.tensors[name] = result
        
        return result
    
    def softmax(self, x: GGMLTensor, axis: int = -1, name: str = "softmax_result") -> GGMLTensor:
        """
        Softmax operation.
        
        Args:
            x: Input tensor
            axis: Axis along which to compute softmax
            name: Result tensor name
            
        Returns:
            Softmax tensor
        """
        exp_x = np.exp(x.data - np.max(x.data, axis=axis, keepdims=True))
        softmax_data = exp_x / np.sum(exp_x, axis=axis, keepdims=True)
        
        result = GGMLTensor(name=name, shape=x.shape, dtype=x.dtype, data=softmax_data)
        self.tensors[name] = result
        
        return result
    
    def attention(
        self,
        query: GGMLTensor,
        key: GGMLTensor,
        value: GGMLTensor,
        name: str = "attention_result"
    ) -> GGMLTensor:
        """
        Scaled dot-product attention mechanism.
        
        Args:
            query: Query tensor (batch, seq_len, d_model)
            key: Key tensor (batch, seq_len, d_model)
            value: Value tensor (batch, seq_len, d_model)
            name: Result tensor name
            
        Returns:
            Attention output tensor
        """
        # Compute attention scores: Q @ K^T / sqrt(d_k)
        d_k = query.shape[-1]
        
        # Simplified attention for 2D tensors
        if len(query.shape) == 2:
            scores = np.matmul(query.data, key.data.T) / np.sqrt(d_k)
            attention_weights = np.exp(scores - np.max(scores, axis=-1, keepdims=True))
            attention_weights /= np.sum(attention_weights, axis=-1, keepdims=True)
            output_data = np.matmul(attention_weights, value.data)
        else:
            raise NotImplementedError("Batch attention not yet implemented")
        
        result = GGMLTensor(name=name, shape=output_data.shape, dtype=query.dtype, data=output_data)
        self.tensors[name] = result
        
        return result
    
    def cleanup(self):
        """Clean up context and release memory."""
        self.tensors.clear()
        logger.info("GGML context cleaned up")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()


def create_embedding_tensor(vocab_size: int, embedding_dim: int, name: str = "embeddings") -> GGMLTensor:
    """
    Create an embedding tensor for legal vocabulary.
    
    Args:
        vocab_size: Size of vocabulary
        embedding_dim: Embedding dimension
        name: Tensor name
        
    Returns:
        Embedding tensor
    """
    # Initialize with small random values
    data = np.random.randn(vocab_size, embedding_dim).astype(np.float32) * 0.01
    
    return GGMLTensor(
        name=name,
        shape=(vocab_size, embedding_dim),
        dtype="float32",
        data=data
    )


def create_weight_tensor(
    in_features: int,
    out_features: int,
    name: str = "weights"
) -> GGMLTensor:
    """
    Create a weight tensor for linear layers.
    
    Args:
        in_features: Input feature dimension
        out_features: Output feature dimension
        name: Tensor name
        
    Returns:
        Weight tensor
    """
    # Xavier initialization
    limit = np.sqrt(6.0 / (in_features + out_features))
    data = np.random.uniform(-limit, limit, (in_features, out_features)).astype(np.float32)
    
    return GGMLTensor(
        name=name,
        shape=(in_features, out_features),
        dtype="float32",
        data=data
    )


if __name__ == "__main__":
    # Example usage
    logger.info("Testing GGML operations")
    
    with GGMLContext() as ctx:
        # Create tensors
        a = ctx.create_tensor("tensor_a", (3, 4))
        a.data = np.random.randn(3, 4).astype(np.float32)
        
        b = ctx.create_tensor("tensor_b", (4, 5))
        b.data = np.random.randn(4, 5).astype(np.float32)
        
        # Matrix multiplication
        c = ctx.matmul(a, b, "tensor_c")
        logger.info(f"Result shape: {c.shape}")
        
        # Test attention
        q = ctx.create_tensor("query", (10, 64))
        q.data = np.random.randn(10, 64).astype(np.float32)
        
        k = ctx.create_tensor("key", (10, 64))
        k.data = np.random.randn(10, 64).astype(np.float32)
        
        v = ctx.create_tensor("value", (10, 64))
        v.data = np.random.randn(10, 64).astype(np.float32)
        
        attn_out = ctx.attention(q, k, v)
        logger.info(f"Attention output shape: {attn_out.shape}")
    
    logger.info("GGML testing completed")
