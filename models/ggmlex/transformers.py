#!/usr/bin/env python3
"""
Legal Transformer Models for GGMLEX Framework

This module implements transformer architectures optimized for legal document
processing using the GGML backend.
"""

import logging
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass

from .ggml import GGMLContext, GGMLTensor, create_weight_tensor
from .llm import LegalLLMConfig, LegalTokenizer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class TransformerConfig:
    """Configuration for Transformer model."""
    
    vocab_size: int = 50000
    embedding_dim: int = 768
    num_heads: int = 12
    num_layers: int = 12
    ff_dim: int = 3072
    max_seq_length: int = 2048
    dropout: float = 0.1


class MultiHeadAttention:
    """
    Multi-head attention mechanism for transformers.
    
    This implements scaled dot-product attention with multiple attention heads
    for parallel processing of different representation subspaces.
    """
    
    def __init__(
        self,
        context: GGMLContext,
        embedding_dim: int,
        num_heads: int,
        name_prefix: str = "mha"
    ):
        """
        Initialize multi-head attention.
        
        Args:
            context: GGML context
            embedding_dim: Embedding dimension
            num_heads: Number of attention heads
            name_prefix: Prefix for tensor names
        """
        self.context = context
        self.embedding_dim = embedding_dim
        self.num_heads = num_heads
        self.head_dim = embedding_dim // num_heads
        
        if embedding_dim % num_heads != 0:
            raise ValueError(f"Embedding dim {embedding_dim} not divisible by num_heads {num_heads}")
        
        # Create projection matrices
        self.q_proj = create_weight_tensor(embedding_dim, embedding_dim, f"{name_prefix}_q_proj")
        self.k_proj = create_weight_tensor(embedding_dim, embedding_dim, f"{name_prefix}_k_proj")
        self.v_proj = create_weight_tensor(embedding_dim, embedding_dim, f"{name_prefix}_v_proj")
        self.out_proj = create_weight_tensor(embedding_dim, embedding_dim, f"{name_prefix}_out_proj")
        
        # Store in context
        self.context.tensors[f"{name_prefix}_q_proj"] = self.q_proj
        self.context.tensors[f"{name_prefix}_k_proj"] = self.k_proj
        self.context.tensors[f"{name_prefix}_v_proj"] = self.v_proj
        self.context.tensors[f"{name_prefix}_out_proj"] = self.out_proj
        
        logger.debug(f"Initialized MultiHeadAttention with {num_heads} heads")
    
    def forward(self, x: np.ndarray, mask: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Forward pass through multi-head attention.
        
        Args:
            x: Input tensor (seq_len, embedding_dim)
            mask: Optional attention mask
            
        Returns:
            Output tensor
        """
        seq_len = x.shape[0]
        
        # Project to Q, K, V
        Q = np.matmul(x, self.q_proj.data)
        K = np.matmul(x, self.k_proj.data)
        V = np.matmul(x, self.v_proj.data)
        
        # Reshape for multi-head attention: (seq_len, num_heads, head_dim)
        Q = Q.reshape(seq_len, self.num_heads, self.head_dim)
        K = K.reshape(seq_len, self.num_heads, self.head_dim)
        V = V.reshape(seq_len, self.num_heads, self.head_dim)
        
        # Transpose for batched matrix multiplication: (num_heads, seq_len, head_dim)
        Q = Q.transpose(1, 0, 2)
        K = K.transpose(1, 0, 2)
        V = V.transpose(1, 0, 2)
        
        # Scaled dot-product attention for each head
        attention_outputs = []
        for head_idx in range(self.num_heads):
            q_head = Q[head_idx]  # (seq_len, head_dim)
            k_head = K[head_idx]  # (seq_len, head_dim)
            v_head = V[head_idx]  # (seq_len, head_dim)
            
            # Attention scores
            scores = np.matmul(q_head, k_head.T) / np.sqrt(self.head_dim)
            
            # Apply mask if provided
            if mask is not None:
                scores = scores + mask
            
            # Softmax
            attn_weights = np.exp(scores - np.max(scores, axis=-1, keepdims=True))
            attn_weights /= np.sum(attn_weights, axis=-1, keepdims=True)
            
            # Apply attention to values
            attn_output = np.matmul(attn_weights, v_head)
            attention_outputs.append(attn_output)
        
        # Concatenate heads: (seq_len, embedding_dim)
        concat_output = np.concatenate(attention_outputs, axis=-1)
        
        # Output projection
        output = np.matmul(concat_output, self.out_proj.data)
        
        return output


class FeedForward:
    """
    Feed-forward network for transformer.
    
    Two-layer MLP with GELU activation.
    """
    
    def __init__(
        self,
        context: GGMLContext,
        embedding_dim: int,
        ff_dim: int,
        name_prefix: str = "ff"
    ):
        """
        Initialize feed-forward network.
        
        Args:
            context: GGML context
            embedding_dim: Embedding dimension
            ff_dim: Feed-forward hidden dimension
            name_prefix: Prefix for tensor names
        """
        self.context = context
        self.embedding_dim = embedding_dim
        self.ff_dim = ff_dim
        
        # Create weight matrices
        self.w1 = create_weight_tensor(embedding_dim, ff_dim, f"{name_prefix}_w1")
        self.w2 = create_weight_tensor(ff_dim, embedding_dim, f"{name_prefix}_w2")
        
        # Store in context
        self.context.tensors[f"{name_prefix}_w1"] = self.w1
        self.context.tensors[f"{name_prefix}_w2"] = self.w2
        
        logger.debug(f"Initialized FeedForward with ff_dim={ff_dim}")
    
    def gelu(self, x: np.ndarray) -> np.ndarray:
        """GELU activation function."""
        return 0.5 * x * (1.0 + np.tanh(np.sqrt(2.0 / np.pi) * (x + 0.044715 * np.power(x, 3))))
    
    def forward(self, x: np.ndarray) -> np.ndarray:
        """
        Forward pass through feed-forward network.
        
        Args:
            x: Input tensor
            
        Returns:
            Output tensor
        """
        # First layer with GELU
        hidden = np.matmul(x, self.w1.data)
        hidden = self.gelu(hidden)
        
        # Second layer
        output = np.matmul(hidden, self.w2.data)
        
        return output


class TransformerLayer:
    """
    Single transformer layer with self-attention and feed-forward network.
    """
    
    def __init__(
        self,
        context: GGMLContext,
        config: TransformerConfig,
        layer_idx: int
    ):
        """
        Initialize transformer layer.
        
        Args:
            context: GGML context
            config: Transformer configuration
            layer_idx: Layer index
        """
        self.context = context
        self.config = config
        self.layer_idx = layer_idx
        
        name_prefix = f"layer_{layer_idx}"
        
        # Multi-head attention
        self.attention = MultiHeadAttention(
            context=context,
            embedding_dim=config.embedding_dim,
            num_heads=config.num_heads,
            name_prefix=f"{name_prefix}_attn"
        )
        
        # Feed-forward network
        self.feed_forward = FeedForward(
            context=context,
            embedding_dim=config.embedding_dim,
            ff_dim=config.ff_dim,
            name_prefix=f"{name_prefix}_ff"
        )
        
        logger.debug(f"Initialized TransformerLayer {layer_idx}")
    
    def layer_norm(self, x: np.ndarray, eps: float = 1e-5) -> np.ndarray:
        """Layer normalization."""
        mean = np.mean(x, axis=-1, keepdims=True)
        var = np.var(x, axis=-1, keepdims=True)
        return (x - mean) / np.sqrt(var + eps)
    
    def forward(self, x: np.ndarray, mask: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Forward pass through transformer layer.
        
        Args:
            x: Input tensor
            mask: Optional attention mask
            
        Returns:
            Output tensor
        """
        # Self-attention with residual connection and layer norm
        attn_output = self.attention.forward(x, mask)
        x = self.layer_norm(x + attn_output)
        
        # Feed-forward with residual connection and layer norm
        ff_output = self.feed_forward.forward(x)
        x = self.layer_norm(x + ff_output)
        
        return x


class LegalTransformer:
    """
    Complete transformer model for legal document processing.
    
    This model is optimized for understanding legal text, including:
    - Long-range dependencies in legal documents
    - Complex legal reasoning patterns
    - Domain-specific vocabulary and syntax
    """
    
    def __init__(self, config: Optional[TransformerConfig] = None):
        """
        Initialize Legal Transformer.
        
        Args:
            config: Transformer configuration
        """
        self.config = config or TransformerConfig()
        self.context = GGMLContext(memory_size=512 * 1024 * 1024)  # 512MB
        self.tokenizer = LegalTokenizer(vocab_size=self.config.vocab_size)
        
        # Initialize model
        self._init_model()
        
        logger.info(f"Initialized LegalTransformer with {self.config.num_layers} layers")
    
    def _init_model(self):
        """Initialize model parameters."""
        # Token embeddings
        embedding_data = np.random.randn(
            self.config.vocab_size,
            self.config.embedding_dim
        ).astype(np.float32) * 0.01
        
        self.token_embeddings = GGMLTensor(
            name="token_embeddings",
            shape=(self.config.vocab_size, self.config.embedding_dim),
            dtype="float32",
            data=embedding_data
        )
        
        # Position embeddings
        position_data = np.random.randn(
            self.config.max_seq_length,
            self.config.embedding_dim
        ).astype(np.float32) * 0.01
        
        self.position_embeddings = GGMLTensor(
            name="position_embeddings",
            shape=(self.config.max_seq_length, self.config.embedding_dim),
            dtype="float32",
            data=position_data
        )
        
        # Store in context
        self.context.tensors["token_embeddings"] = self.token_embeddings
        self.context.tensors["position_embeddings"] = self.position_embeddings
        
        # Create transformer layers
        self.layers = []
        for i in range(self.config.num_layers):
            layer = TransformerLayer(
                context=self.context,
                config=self.config,
                layer_idx=i
            )
            self.layers.append(layer)
        
        logger.debug(f"Initialized {len(self.context.tensors)} tensors")
    
    def encode(self, text: str) -> np.ndarray:
        """
        Encode text into embeddings.
        
        Args:
            text: Input text
            
        Returns:
            Text embeddings
        """
        # Tokenize
        token_ids = self.tokenizer.tokenize(text)
        
        # Truncate if necessary
        max_len = min(len(token_ids), self.config.max_seq_length)
        token_ids = token_ids[:max_len]
        
        # Get embeddings
        embeddings = []
        for i, token_id in enumerate(token_ids):
            if token_id < self.token_embeddings.shape[0]:
                token_emb = self.token_embeddings.data[token_id]
                pos_emb = self.position_embeddings.data[i]
                embeddings.append(token_emb + pos_emb)
        
        embeddings = np.array(embeddings)
        
        return embeddings
    
    def forward(self, input_ids: List[int]) -> np.ndarray:
        """
        Forward pass through transformer.
        
        Args:
            input_ids: Input token IDs
            
        Returns:
            Output embeddings
        """
        # Truncate if necessary
        max_len = min(len(input_ids), self.config.max_seq_length)
        input_ids = input_ids[:max_len]
        
        # Get initial embeddings
        embeddings = []
        for i, token_id in enumerate(input_ids):
            if token_id < self.token_embeddings.shape[0]:
                token_emb = self.token_embeddings.data[token_id]
                pos_emb = self.position_embeddings.data[i]
                embeddings.append(token_emb + pos_emb)
        
        hidden_states = np.array(embeddings)
        
        # Pass through transformer layers
        for layer in self.layers:
            hidden_states = layer.forward(hidden_states)
        
        return hidden_states
    
    def analyze_legal_text(self, text: str) -> Dict[str, Any]:
        """
        Analyze legal text using the transformer.
        
        Args:
            text: Legal text to analyze
            
        Returns:
            Analysis results
        """
        # Encode text
        embeddings = self.encode(text)
        
        # Perform forward pass
        token_ids = self.tokenizer.tokenize(text)
        output = self.forward(token_ids[:self.config.max_seq_length])
        
        # Aggregate analysis
        analysis = {
            "text_length": len(text),
            "num_tokens": len(token_ids),
            "embedding_dim": embeddings.shape[1] if len(embeddings.shape) > 1 else 0,
            "processed_tokens": output.shape[0],
            "model_config": {
                "num_layers": self.config.num_layers,
                "num_heads": self.config.num_heads,
                "embedding_dim": self.config.embedding_dim
            }
        }
        
        logger.info(f"Analyzed legal text with {analysis['num_tokens']} tokens")
        
        return analysis
    
    def cleanup(self):
        """Clean up model resources."""
        self.context.cleanup()
        logger.info("LegalTransformer cleaned up")


if __name__ == "__main__":
    # Example usage
    logger.info("Testing LegalTransformer")
    
    # Initialize model
    config = TransformerConfig(
        vocab_size=5000,
        embedding_dim=256,
        num_heads=8,
        num_layers=4,
        ff_dim=1024
    )
    
    transformer = LegalTransformer(config)
    
    # Test encoding
    text = "The court held that the contract was valid and enforceable under South African law."
    embeddings = transformer.encode(text)
    logger.info(f"Encoded text to embeddings of shape: {embeddings.shape}")
    
    # Test analysis
    analysis = transformer.analyze_legal_text(text)
    logger.info(f"Legal text analysis: {analysis}")
    
    # Cleanup
    transformer.cleanup()
    
    logger.info("LegalTransformer testing completed")
