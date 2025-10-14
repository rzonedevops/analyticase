#!/usr/bin/env python3
"""
Legal LLM Interface for GGMLEX Framework

This module provides a high-level interface for running large language models
optimized for legal document analysis using the GGML backend.
"""

import logging
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path

from .ggml import GGMLContext, GGMLTensor, create_embedding_tensor, create_weight_tensor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class LegalLLMConfig:
    """Configuration for Legal LLM."""
    
    vocab_size: int = 50000
    embedding_dim: int = 768
    hidden_dim: int = 3072
    num_layers: int = 12
    num_heads: int = 12
    max_seq_length: int = 2048
    dropout: float = 0.1
    
    # Legal-specific parameters
    legal_vocab_boost: bool = True
    case_law_embeddings: bool = True
    statute_embeddings: bool = True


@dataclass
class LegalDocument:
    """Represents a legal document for processing."""
    
    text: str
    doc_type: str = "general"  # case_law, statute, contract, brief, etc.
    metadata: Dict[str, Any] = field(default_factory=dict)
    tokens: Optional[List[int]] = None
    embeddings: Optional[np.ndarray] = None


class LegalTokenizer:
    """
    Tokenizer specialized for legal text.
    
    This tokenizer handles legal-specific vocabulary including Latin phrases,
    statutory references, and case citations.
    """
    
    def __init__(self, vocab_size: int = 50000):
        """Initialize tokenizer."""
        self.vocab_size = vocab_size
        self.vocab = {}
        self.inverse_vocab = {}
        
        # Special tokens
        self.pad_token = "<PAD>"
        self.unk_token = "<UNK>"
        self.bos_token = "<BOS>"
        self.eos_token = "<EOS>"
        
        # Legal-specific tokens
        self.legal_tokens = [
            "<CASE_REF>", "<STATUTE>", "<SECTION>", "<SUBSECTION>",
            "<PLAINTIFF>", "<DEFENDANT>", "<JUDGE>", "<COURT>",
            "<LATIN>", "<DATE>", "<AMOUNT>"
        ]
        
        self._build_vocab()
        
        logger.info(f"Initialized LegalTokenizer with vocab size {vocab_size}")
    
    def _build_vocab(self):
        """Build vocabulary with special and legal tokens."""
        # Add special tokens
        special = [self.pad_token, self.unk_token, self.bos_token, self.eos_token]
        special.extend(self.legal_tokens)
        
        for i, token in enumerate(special):
            self.vocab[token] = i
            self.inverse_vocab[i] = token
        
        # Add common legal words (simplified)
        common_legal_words = [
            "court", "judge", "plaintiff", "defendant", "contract", "breach",
            "damages", "negligence", "statute", "law", "case", "appeal",
            "evidence", "witness", "testimony", "verdict", "judgment",
            "rights", "liability", "jurisdiction", "precedent", "doctrine"
        ]
        
        next_id = len(special)
        for word in common_legal_words:
            if word not in self.vocab:
                self.vocab[word] = next_id
                self.inverse_vocab[next_id] = word
                next_id += 1
    
    def tokenize(self, text: str) -> List[int]:
        """
        Tokenize text into token IDs.
        
        Args:
            text: Input text
            
        Returns:
            List of token IDs
        """
        # Simple word-level tokenization (in production, use BPE or WordPiece)
        words = text.lower().split()
        
        tokens = [self.vocab[self.bos_token]]
        for word in words:
            token_id = self.vocab.get(word, self.vocab[self.unk_token])
            tokens.append(token_id)
        tokens.append(self.vocab[self.eos_token])
        
        return tokens
    
    def detokenize(self, tokens: List[int]) -> str:
        """
        Convert token IDs back to text.
        
        Args:
            tokens: List of token IDs
            
        Returns:
            Reconstructed text
        """
        words = []
        for token_id in tokens:
            word = self.inverse_vocab.get(token_id, self.unk_token)
            if word not in [self.bos_token, self.eos_token, self.pad_token]:
                words.append(word)
        
        return " ".join(words)


class LegalLLM:
    """
    Legal Large Language Model using GGML backend.
    
    This model is optimized for legal document understanding, including:
    - Case law analysis
    - Statutory interpretation
    - Contract review
    - Legal brief generation
    """
    
    def __init__(self, config: Optional[LegalLLMConfig] = None):
        """
        Initialize Legal LLM.
        
        Args:
            config: Model configuration
        """
        self.config = config or LegalLLMConfig()
        self.tokenizer = LegalTokenizer(vocab_size=self.config.vocab_size)
        self.context = GGMLContext(memory_size=512 * 1024 * 1024)  # 512MB
        
        # Initialize model parameters
        self._init_model()
        
        logger.info(f"Initialized LegalLLM with {self.config.num_layers} layers")
    
    def _init_model(self):
        """Initialize model weights and embeddings."""
        # Token embeddings
        self.token_embeddings = create_embedding_tensor(
            vocab_size=self.config.vocab_size,
            embedding_dim=self.config.embedding_dim,
            name="token_embeddings"
        )
        
        # Position embeddings
        self.position_embeddings = create_embedding_tensor(
            vocab_size=self.config.max_seq_length,
            embedding_dim=self.config.embedding_dim,
            name="position_embeddings"
        )
        
        # Store in context
        self.context.tensors["token_embeddings"] = self.token_embeddings
        self.context.tensors["position_embeddings"] = self.position_embeddings
        
        # Initialize transformer layers (simplified)
        for i in range(self.config.num_layers):
            # Query, Key, Value projections
            self.context.tensors[f"layer_{i}_q_proj"] = create_weight_tensor(
                self.config.embedding_dim,
                self.config.embedding_dim,
                f"layer_{i}_q_proj"
            )
            self.context.tensors[f"layer_{i}_k_proj"] = create_weight_tensor(
                self.config.embedding_dim,
                self.config.embedding_dim,
                f"layer_{i}_k_proj"
            )
            self.context.tensors[f"layer_{i}_v_proj"] = create_weight_tensor(
                self.config.embedding_dim,
                self.config.embedding_dim,
                f"layer_{i}_v_proj"
            )
            
            # Feed-forward layers
            self.context.tensors[f"layer_{i}_ff1"] = create_weight_tensor(
                self.config.embedding_dim,
                self.config.hidden_dim,
                f"layer_{i}_ff1"
            )
            self.context.tensors[f"layer_{i}_ff2"] = create_weight_tensor(
                self.config.hidden_dim,
                self.config.embedding_dim,
                f"layer_{i}_ff2"
            )
        
        logger.debug(f"Initialized {len(self.context.tensors)} tensors")
    
    def encode(self, document: LegalDocument) -> np.ndarray:
        """
        Encode a legal document into embeddings.
        
        Args:
            document: Legal document to encode
            
        Returns:
            Document embeddings
        """
        # Tokenize text
        if document.tokens is None:
            document.tokens = self.tokenizer.tokenize(document.text)
        
        # Truncate if necessary
        max_len = min(len(document.tokens), self.config.max_seq_length)
        token_ids = document.tokens[:max_len]
        
        # Get token embeddings
        embeddings = []
        for i, token_id in enumerate(token_ids):
            if token_id < self.token_embeddings.shape[0]:
                token_emb = self.token_embeddings.data[token_id]
                pos_emb = self.position_embeddings.data[i]
                combined = token_emb + pos_emb
                embeddings.append(combined)
        
        embeddings = np.array(embeddings)
        
        # Store embeddings
        document.embeddings = embeddings
        
        logger.debug(f"Encoded document with {len(token_ids)} tokens")
        
        return embeddings
    
    def forward(self, input_ids: List[int]) -> np.ndarray:
        """
        Forward pass through the model.
        
        Args:
            input_ids: Input token IDs
            
        Returns:
            Output logits
        """
        # Truncate if necessary
        max_len = min(len(input_ids), self.config.max_seq_length)
        input_ids = input_ids[:max_len]
        
        # Get embeddings
        embeddings = []
        for i, token_id in enumerate(input_ids):
            if token_id < self.token_embeddings.shape[0]:
                token_emb = self.token_embeddings.data[token_id]
                pos_emb = self.position_embeddings.data[i]
                embeddings.append(token_emb + pos_emb)
        
        hidden_states = np.array(embeddings)
        
        # Simplified transformer forward pass
        for layer_idx in range(self.config.num_layers):
            # Self-attention (simplified)
            q_proj = self.context.tensors[f"layer_{layer_idx}_q_proj"]
            k_proj = self.context.tensors[f"layer_{layer_idx}_k_proj"]
            v_proj = self.context.tensors[f"layer_{layer_idx}_v_proj"]
            
            # Project Q, K, V
            Q = np.matmul(hidden_states, q_proj.data)
            K = np.matmul(hidden_states, k_proj.data)
            V = np.matmul(hidden_states, v_proj.data)
            
            # Attention
            d_k = Q.shape[-1]
            scores = np.matmul(Q, K.T) / np.sqrt(d_k)
            attn_weights = np.exp(scores - np.max(scores, axis=-1, keepdims=True))
            attn_weights /= np.sum(attn_weights, axis=-1, keepdims=True)
            attn_output = np.matmul(attn_weights, V)
            
            # Residual connection
            hidden_states = hidden_states + attn_output
            
            # Layer norm (simplified)
            mean = np.mean(hidden_states, axis=-1, keepdims=True)
            var = np.var(hidden_states, axis=-1, keepdims=True)
            hidden_states = (hidden_states - mean) / np.sqrt(var + 1e-5)
            
            # Feed-forward
            ff1 = self.context.tensors[f"layer_{layer_idx}_ff1"]
            ff2 = self.context.tensors[f"layer_{layer_idx}_ff2"]
            
            ff_out = np.matmul(hidden_states, ff1.data)
            ff_out = np.maximum(0, ff_out)  # ReLU
            ff_out = np.matmul(ff_out, ff2.data)
            
            # Residual connection
            hidden_states = hidden_states + ff_out
        
        # Output projection (simplified - return hidden states)
        return hidden_states
    
    def generate(
        self,
        prompt: str,
        max_length: int = 100,
        temperature: float = 0.7
    ) -> str:
        """
        Generate text from a prompt.
        
        Args:
            prompt: Input prompt
            max_length: Maximum generation length
            temperature: Sampling temperature
            
        Returns:
            Generated text
        """
        # Tokenize prompt
        input_ids = self.tokenizer.tokenize(prompt)
        
        logger.info(f"Generating text from prompt: '{prompt[:50]}...'")
        
        # Generate tokens (simplified)
        generated_ids = input_ids.copy()
        
        for _ in range(max_length):
            # Forward pass
            logits = self.forward(generated_ids)
            
            # Get next token (simplified - use last hidden state)
            # In a real implementation, this would be a proper language model head
            next_token_id = np.random.randint(0, self.config.vocab_size)
            
            generated_ids.append(next_token_id)
            
            # Stop if we generate EOS token
            if next_token_id == self.tokenizer.vocab[self.tokenizer.eos_token]:
                break
        
        # Detokenize
        generated_text = self.tokenizer.detokenize(generated_ids)
        
        return generated_text
    
    def analyze_case(self, case_text: str) -> Dict[str, Any]:
        """
        Analyze a legal case document.
        
        Args:
            case_text: Case document text
            
        Returns:
            Analysis results
        """
        document = LegalDocument(text=case_text, doc_type="case_law")
        embeddings = self.encode(document)
        
        # Perform analysis (simplified)
        analysis = {
            "document_type": "case_law",
            "num_tokens": len(document.tokens),
            "embedding_dim": embeddings.shape[1] if len(embeddings.shape) > 1 else 0,
            "summary": "Case analysis using GGMLEX LLM",
            "key_entities": [],
            "legal_issues": [],
            "precedents": []
        }
        
        logger.info(f"Analyzed case with {analysis['num_tokens']} tokens")
        
        return analysis
    
    def cleanup(self):
        """Clean up model resources."""
        self.context.cleanup()
        logger.info("LegalLLM cleaned up")


if __name__ == "__main__":
    # Example usage
    logger.info("Testing LegalLLM")
    
    # Initialize model
    config = LegalLLMConfig(
        vocab_size=5000,  # Smaller for testing
        embedding_dim=256,
        num_layers=4
    )
    
    llm = LegalLLM(config)
    
    # Test encoding
    doc = LegalDocument(
        text="The court held that the contract was valid and enforceable.",
        doc_type="case_law"
    )
    
    embeddings = llm.encode(doc)
    logger.info(f"Document embeddings shape: {embeddings.shape}")
    
    # Test case analysis
    analysis = llm.analyze_case("The plaintiff sued the defendant for breach of contract.")
    logger.info(f"Case analysis: {analysis}")
    
    # Cleanup
    llm.cleanup()
    
    logger.info("LegalLLM testing completed")
