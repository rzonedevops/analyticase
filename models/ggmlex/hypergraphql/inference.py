#!/usr/bin/env python3
"""
Inference Engine for Legal Principles

This module implements inference operations to derive general legal principles
from enumerated laws in the lex framework. It supports multiple inference models:
- Deductive: Apply general principles to specific cases
- Inductive: Generalize from multiple specific laws to form principles
- Abductive: Hypothesize best explanations for observed legal patterns
- Analogical: Transfer principles across legal domains by similarity

Inference Levels:
  Level 0: Enumerated Laws (from lex/*.scm files, inferenceLevel=0)
  Level 1: First-order Principles (generalized from laws)
  Level 2: Meta-principles (higher abstractions)
"""

import logging
from typing import Dict, Any, List, Optional, Set, Tuple, Callable
from dataclasses import dataclass
import re

from .schema import (
    LegalNode, LegalHyperedge,
    LegalNodeType, LegalRelationType, InferenceType
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class InferenceResult:
    """Result of an inference operation."""
    
    principle: Optional[LegalNode] = None
    confidence: float = 0.0
    inference_type: Optional[InferenceType] = None
    supporting_nodes: List[LegalNode] = None
    supporting_edges: List[LegalHyperedge] = None
    explanation: str = ""
    
    def __post_init__(self):
        if self.supporting_nodes is None:
            self.supporting_nodes = []
        if self.supporting_edges is None:
            self.supporting_edges = []


class InferenceEngine:
    """
    Engine for legal inference operations.
    
    This engine processes lex scheme expressions to derive general principles
    at different inference levels.
    """
    
    def __init__(self, hypergraph_engine=None):
        """
        Initialize inference engine.
        
        Args:
            hypergraph_engine: HypergraphQL engine instance (optional)
        """
        self.hypergraph = hypergraph_engine
        self.inferred_principles: Dict[str, LegalNode] = {}
        logger.info("Initialized InferenceEngine")
    
    def infer_principles(
        self,
        source_nodes: List[LegalNode],
        inference_type: InferenceType,
        target_level: int = 1,
        **kwargs
    ) -> InferenceResult:
        """
        Infer general principles from source nodes.
        
        Args:
            source_nodes: Source legal nodes (typically level 0 laws)
            inference_type: Type of inference to perform
            target_level: Target inference level (1=first-order, 2=meta)
            **kwargs: Additional parameters for specific inference types
        
        Returns:
            InferenceResult with inferred principle and metadata
        """
        if inference_type == InferenceType.DEDUCTIVE:
            return self._deductive_inference(source_nodes, target_level, **kwargs)
        elif inference_type == InferenceType.INDUCTIVE:
            return self._inductive_inference(source_nodes, target_level, **kwargs)
        elif inference_type == InferenceType.ABDUCTIVE:
            return self._abductive_inference(source_nodes, target_level, **kwargs)
        elif inference_type == InferenceType.ANALOGICAL:
            return self._analogical_inference(source_nodes, target_level, **kwargs)
        else:
            logger.error(f"Unknown inference type: {inference_type}")
            return InferenceResult()
    
    def _deductive_inference(
        self,
        source_nodes: List[LegalNode],
        target_level: int,
        **kwargs
    ) -> InferenceResult:
        """
        Perform deductive inference.
        
        Apply general principles to specific cases using logical deduction.
        Confidence is high (0.9-1.0) when premises are valid.
        
        Args:
            source_nodes: Source nodes (general principle + specific case)
            target_level: Target inference level
            **kwargs: Additional parameters
        
        Returns:
            InferenceResult with deduced conclusion
        """
        if len(source_nodes) < 2:
            return InferenceResult(
                explanation="Deductive inference requires at least 2 nodes (general + specific)"
            )
        
        # First node should be general principle (higher level)
        general_principle = source_nodes[0]
        specific_case = source_nodes[1]
        
        # Apply modus ponens: if P→Q and P, then Q
        # Confidence is minimum of both premises
        confidence = min(
            general_principle.confidence,
            specific_case.confidence
        )
        
        # Create conclusion node
        principle_id = f"deductive_{general_principle.node_id}_{specific_case.node_id}"
        principle = LegalNode(
            node_id=principle_id,
            node_type=LegalNodeType.PRINCIPLE,
            name=f"{general_principle.name} applied to {specific_case.name}",
            content=f"By deduction: {general_principle.content} applies to {specific_case.content}",
            jurisdiction=general_principle.jurisdiction,
            inference_level=target_level,
            inference_type=InferenceType.DEDUCTIVE,
            confidence=confidence,
            metadata={
                "general_principle": general_principle.node_id,
                "specific_case": specific_case.node_id,
                "rule_type": "modus_ponens"
            }
        )
        
        # Create supporting edges
        edges = [
            LegalHyperedge(
                edge_id=f"deductive_edge_{principle_id}_from_{general_principle.node_id}",
                relation_type=LegalRelationType.INFERS_FROM,
                nodes={principle.node_id, general_principle.node_id},
                confidence=confidence,
                inference_type=InferenceType.DEDUCTIVE
            ),
            LegalHyperedge(
                edge_id=f"deductive_edge_{principle_id}_applies_to_{specific_case.node_id}",
                relation_type=LegalRelationType.APPLIES_TO,
                nodes={principle.node_id, specific_case.node_id},
                confidence=confidence,
                inference_type=InferenceType.DEDUCTIVE
            )
        ]
        
        return InferenceResult(
            principle=principle,
            confidence=confidence,
            inference_type=InferenceType.DEDUCTIVE,
            supporting_nodes=source_nodes,
            supporting_edges=edges,
            explanation=f"Deduced from general principle '{general_principle.name}' applied to '{specific_case.name}'"
        )
    
    def _inductive_inference(
        self,
        source_nodes: List[LegalNode],
        target_level: int,
        pattern_name: Optional[str] = None,
        **kwargs
    ) -> InferenceResult:
        """
        Perform inductive inference.
        
        Generalize from multiple specific laws to form general principles.
        Confidence increases with more examples: n / (n + 1), capped at 0.95.
        
        Args:
            source_nodes: Multiple specific law nodes (level 0)
            target_level: Target inference level
            pattern_name: Name of the pattern being generalized
            **kwargs: Additional parameters
        
        Returns:
            InferenceResult with generalized principle
        """
        if len(source_nodes) < 2:
            return InferenceResult(
                explanation="Inductive inference requires at least 2 examples"
            )
        
        # Identify common pattern
        pattern = self._identify_common_pattern(source_nodes)
        
        if not pattern:
            return InferenceResult(
                explanation="No common pattern found in source nodes"
            )
        
        # Calculate confidence: n / (n + 1), capped at 0.95
        n = len(source_nodes)
        confidence = min(0.95, n / (n + 1))
        
        # Create generalized principle
        principle_name = pattern_name or pattern.get("name", "Generalized Principle")
        principle_id = f"inductive_{pattern.get('id', 'principle')}_{target_level}"
        
        principle = LegalNode(
            node_id=principle_id,
            node_type=LegalNodeType.PRINCIPLE,
            name=principle_name,
            content=pattern.get("description", ""),
            jurisdiction=source_nodes[0].jurisdiction,
            inference_level=target_level,
            inference_type=InferenceType.INDUCTIVE,
            confidence=confidence,
            metadata={
                "num_examples": n,
                "example_nodes": [node.node_id for node in source_nodes],
                "pattern": pattern
            }
        )
        
        # Create edges from each source to principle
        edges = []
        for source in source_nodes:
            edge = LegalHyperedge(
                edge_id=f"inductive_edge_{source.node_id}_to_{principle_id}",
                relation_type=LegalRelationType.GENERALIZES,
                nodes={source.node_id, principle.node_id},
                confidence=confidence,
                inference_type=InferenceType.INDUCTIVE
            )
            edges.append(edge)
        
        return InferenceResult(
            principle=principle,
            confidence=confidence,
            inference_type=InferenceType.INDUCTIVE,
            supporting_nodes=source_nodes,
            supporting_edges=edges,
            explanation=f"Generalized from {n} examples: {principle_name}"
        )
    
    def _abductive_inference(
        self,
        source_nodes: List[LegalNode],
        target_level: int,
        hypothesis_name: Optional[str] = None,
        **kwargs
    ) -> InferenceResult:
        """
        Perform abductive inference.
        
        Hypothesize the best explanation for observed legal patterns.
        Confidence is medium (0.5-0.8) based on explanatory power, coherence, and simplicity.
        
        Args:
            source_nodes: Observed legal rules or patterns
            target_level: Target inference level
            hypothesis_name: Name of the hypothesis
            **kwargs: Additional parameters
        
        Returns:
            InferenceResult with best explanatory hypothesis
        """
        if len(source_nodes) < 2:
            return InferenceResult(
                explanation="Abductive inference requires at least 2 observations"
            )
        
        # Generate hypothesis that best explains the observations
        hypothesis = self._generate_best_hypothesis(source_nodes)
        
        if not hypothesis:
            return InferenceResult(
                explanation="No suitable hypothesis found for observations"
            )
        
        # Evaluate hypothesis quality
        explanatory_power = self._evaluate_explanatory_power(hypothesis, source_nodes)
        coherence = self._evaluate_coherence(hypothesis)
        simplicity = self._evaluate_simplicity(hypothesis)
        
        # Calculate confidence: weighted combination, scaled for abductive uncertainty
        base_score = (
            explanatory_power * 0.5 +
            coherence * 0.3 +
            simplicity * 0.2
        )
        confidence = base_score * 0.7  # Abductive discount
        
        # Create hypothesis node
        hypothesis_name = hypothesis_name or hypothesis.get("name", "Explanatory Principle")
        principle_id = f"abductive_{hypothesis.get('id', 'hypothesis')}_{target_level}"
        
        principle = LegalNode(
            node_id=principle_id,
            node_type=LegalNodeType.PRINCIPLE,
            name=hypothesis_name,
            content=hypothesis.get("description", ""),
            jurisdiction=source_nodes[0].jurisdiction,
            inference_level=target_level,
            inference_type=InferenceType.ABDUCTIVE,
            confidence=confidence,
            metadata={
                "observations": [node.node_id for node in source_nodes],
                "explanatory_power": explanatory_power,
                "coherence": coherence,
                "simplicity": simplicity,
                "hypothesis": hypothesis
            }
        )
        
        # Create supporting edges
        edges = []
        for source in source_nodes:
            edge = LegalHyperedge(
                edge_id=f"abductive_edge_{source.node_id}_supports_{principle_id}",
                relation_type=LegalRelationType.SUPPORTS,
                nodes={source.node_id, principle.node_id},
                confidence=confidence,
                inference_type=InferenceType.ABDUCTIVE
            )
            edges.append(edge)
        
        return InferenceResult(
            principle=principle,
            confidence=confidence,
            inference_type=InferenceType.ABDUCTIVE,
            supporting_nodes=source_nodes,
            supporting_edges=edges,
            explanation=f"Best explanation: {hypothesis_name} (power={explanatory_power:.2f}, coherence={coherence:.2f})"
        )
    
    def _analogical_inference(
        self,
        source_nodes: List[LegalNode],
        target_level: int,
        target_domain: Optional[str] = None,
        **kwargs
    ) -> InferenceResult:
        """
        Perform analogical inference.
        
        Transfer principles from one legal domain to another by similarity.
        Confidence varies (0.6-0.9) based on domain similarity.
        
        Args:
            source_nodes: Source domain principle(s)
            target_level: Target inference level
            target_domain: Target legal domain
            **kwargs: Additional parameters
        
        Returns:
            InferenceResult with transferred principle
        """
        if len(source_nodes) < 1:
            return InferenceResult(
                explanation="Analogical inference requires at least 1 source principle"
            )
        
        source_principle = source_nodes[0]
        
        if not target_domain:
            return InferenceResult(
                explanation="Target domain required for analogical inference"
            )
        
        # Calculate similarity between domains
        source_domain = source_principle.metadata.get("branch", "unknown")
        similarity = self._calculate_domain_similarity(source_domain, target_domain)
        
        if similarity < 0.6:
            return InferenceResult(
                explanation=f"Domain similarity too low: {similarity:.2f} < 0.6"
            )
        
        # Transfer principle with confidence adjustment
        confidence = similarity * source_principle.confidence * 0.9
        
        # Create transferred principle
        principle_id = f"analogical_{source_principle.node_id}_to_{target_domain}"
        
        principle = LegalNode(
            node_id=principle_id,
            node_type=LegalNodeType.PRINCIPLE,
            name=f"{source_principle.name} (by analogy to {target_domain})",
            content=f"By analogy from {source_domain}: {source_principle.content}",
            jurisdiction=source_principle.jurisdiction,
            inference_level=target_level,
            inference_type=InferenceType.ANALOGICAL,
            confidence=confidence,
            metadata={
                "source_principle": source_principle.node_id,
                "source_domain": source_domain,
                "target_domain": target_domain,
                "similarity": similarity
            }
        )
        
        # Create edge
        edge = LegalHyperedge(
            edge_id=f"analogical_edge_{source_principle.node_id}_to_{principle_id}",
            relation_type=LegalRelationType.APPLIES_TO,
            nodes={source_principle.node_id, principle.node_id},
            confidence=confidence,
            inference_type=InferenceType.ANALOGICAL
        )
        
        return InferenceResult(
            principle=principle,
            confidence=confidence,
            inference_type=InferenceType.ANALOGICAL,
            supporting_nodes=source_nodes,
            supporting_edges=[edge],
            explanation=f"Transferred from {source_domain} to {target_domain} (similarity={similarity:.2f})"
        )
    
    def _identify_common_pattern(self, nodes: List[LegalNode]) -> Optional[Dict[str, Any]]:
        """
        Identify common pattern across nodes.
        
        Args:
            nodes: Legal nodes to analyze
        
        Returns:
            Pattern dictionary or None
        """
        # Look for common keywords in node names and content
        all_text = " ".join([node.name + " " + node.content for node in nodes])
        
        # Common legal patterns
        patterns = {
            "reasonable_person": {
                "keywords": ["reasonable person", "reasonable", "reasonableness"],
                "name": "Reasonable Person Standard",
                "description": "Legal standards are based on the reasonable person test"
            },
            "mental_element": {
                "keywords": ["intent", "mens rea", "fault", "negligence", "mental"],
                "name": "Mental Culpability Principle",
                "description": "Legal liability requires mental culpability for fairness"
            },
            "contract_formation": {
                "keywords": ["offer", "acceptance", "consideration", "contract"],
                "name": "Contract Formation Principle",
                "description": "Contracts require offer, acceptance, and consideration"
            },
            "procedural_fairness": {
                "keywords": ["fair", "fairness", "procedural", "hearing", "notice"],
                "name": "Procedural Fairness Principle",
                "description": "Legal processes must be procedurally fair"
            }
        }
        
        for pattern_id, pattern_info in patterns.items():
            # Check if pattern keywords appear in multiple nodes
            matches = sum(
                1 for node in nodes
                if any(keyword in (node.name + " " + node.content).lower()
                       for keyword in pattern_info["keywords"])
            )
            
            # Pattern found if >50% of nodes match
            if matches >= len(nodes) * 0.5:
                pattern_info["id"] = pattern_id
                pattern_info["matches"] = matches
                return pattern_info
        
        # Generic pattern if no specific pattern found
        return {
            "id": "generic",
            "name": "Common Legal Principle",
            "description": "Generalized principle from multiple legal rules",
            "matches": len(nodes)
        }
    
    def _generate_best_hypothesis(self, nodes: List[LegalNode]) -> Optional[Dict[str, Any]]:
        """
        Generate best explanatory hypothesis for nodes.
        
        Args:
            nodes: Observed legal nodes
        
        Returns:
            Hypothesis dictionary or None
        """
        # Use pattern identification as basis for hypothesis
        pattern = self._identify_common_pattern(nodes)
        
        if pattern and pattern.get("id") != "generic":
            # Return pattern with matches preserved
            return {
                "id": pattern["id"],
                "name": pattern["name"],
                "description": pattern["description"],
                "type": "pattern_based",
                "matches": pattern.get("matches", len(nodes))
            }
        
        # Fallback: generic hypothesis
        return {
            "id": "generic_explanation",
            "name": "General Legal Framework Principle",
            "description": "These rules share a common underlying legal principle",
            "type": "generic"
        }
    
    def _evaluate_explanatory_power(
        self,
        hypothesis: Dict[str, Any],
        observations: List[LegalNode]
    ) -> float:
        """
        Evaluate how well hypothesis explains observations.
        
        Args:
            hypothesis: Hypothesis dictionary
            observations: Observed nodes
        
        Returns:
            Explanatory power score (0.0-1.0)
        """
        # Simple heuristic: how many observations does it explain?
        if hypothesis.get("type") == "pattern_based":
            matches = hypothesis.get("matches", 0)
            return min(1.0, matches / len(observations))
        else:
            return 0.7  # Default for generic hypotheses
    
    def _evaluate_coherence(self, hypothesis: Dict[str, Any]) -> float:
        """
        Evaluate coherence with existing legal framework.
        
        Args:
            hypothesis: Hypothesis dictionary
        
        Returns:
            Coherence score (0.0-1.0)
        """
        # Pattern-based hypotheses are more coherent
        if hypothesis.get("type") == "pattern_based":
            return 0.8
        else:
            return 0.6
    
    def _evaluate_simplicity(self, hypothesis: Dict[str, Any]) -> float:
        """
        Evaluate simplicity of hypothesis (Occam's Razor).
        
        Args:
            hypothesis: Hypothesis dictionary
        
        Returns:
            Simplicity score (0.0-1.0)
        """
        # Simpler hypotheses score higher
        # Could be based on description length, assumptions, etc.
        description_length = len(hypothesis.get("description", ""))
        
        # Shorter descriptions are simpler
        if description_length < 100:
            return 0.9
        elif description_length < 200:
            return 0.7
        else:
            return 0.5
    
    def _calculate_domain_similarity(self, source: str, target: str) -> float:
        """
        Calculate similarity between legal domains.
        
        Args:
            source: Source domain
            target: Target domain
        
        Returns:
            Similarity score (0.0-1.0)
        """
        # Domain proximity mapping
        civil_domains = {"civil", "contract", "delict", "property"}
        public_domains = {"constitutional", "administrative", "criminal"}
        specialized_domains = {"labour", "environmental", "construction", "international"}
        
        source_lower = source.lower()
        target_lower = target.lower()
        
        # Same domain
        if source_lower == target_lower:
            return 1.0
        
        # Within same group
        if (source_lower in civil_domains and target_lower in civil_domains):
            return 0.8
        if (source_lower in public_domains and target_lower in public_domains):
            return 0.8
        if (source_lower in specialized_domains and target_lower in specialized_domains):
            return 0.7
        
        # Cross-group but related
        if (source_lower in civil_domains and target_lower in specialized_domains) or \
           (source_lower in specialized_domains and target_lower in civil_domains):
            return 0.6
        
        # Different groups
        return 0.4
    
    def build_inference_hierarchy(self) -> Dict[int, List[LegalNode]]:
        """
        Build complete inference hierarchy from hypergraph.
        
        Returns:
            Dictionary mapping inference levels to nodes
        """
        hierarchy = {}
        
        if not self.hypergraph:
            return hierarchy
        
        # Organize nodes by inference level
        for node in self.hypergraph.nodes.values():
            level = node.inference_level
            if level not in hierarchy:
                hierarchy[level] = []
            hierarchy[level].append(node)
        
        return hierarchy
    
    def query_by_inference_level(self, level: int) -> List[LegalNode]:
        """
        Query nodes by inference level.
        
        Args:
            level: Inference level (0=laws, 1=principles, 2=meta)
        
        Returns:
            List of nodes at specified level
        """
        if not self.hypergraph:
            return []
        
        return [
            node for node in self.hypergraph.nodes.values()
            if node.inference_level == level
        ]
    
    def get_inference_chain(self, node_id: str) -> List[LegalNode]:
        """
        Get the inference chain for a node (how it was derived).
        
        Args:
            node_id: Node ID to trace
        
        Returns:
            List of nodes in inference chain, ordered from base to derived
        """
        if not self.hypergraph:
            return []
        
        node = self.hypergraph.get_node(node_id)
        if not node:
            return []
        
        chain = [node]
        
        # Follow INFERS_FROM edges backwards
        current = node
        visited = {node_id}
        
        while current:
            # Find edges where current node infers from others
            parent_found = False
            
            for edge_id in self.hypergraph.node_to_edges.get(current.node_id, []):
                edge = self.hypergraph.edges.get(edge_id)
                
                if not edge or edge.relation_type != LegalRelationType.INFERS_FROM:
                    continue
                
                # Find parent node in edge
                for other_id in edge.nodes:
                    if other_id != current.node_id and other_id not in visited:
                        parent = self.hypergraph.get_node(other_id)
                        if parent:
                            chain.insert(0, parent)
                            visited.add(other_id)
                            current = parent
                            parent_found = True
                            break
                
                if parent_found:
                    break
            
            if not parent_found:
                break
        
        return chain
