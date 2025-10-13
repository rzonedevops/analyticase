#!/usr/bin/env python3
"""
Case-LLM Model for Legal Case Analysis

This module implements a Large Language Model-based framework for analyzing
legal cases, generating insights, and providing recommendations.
"""

import logging
import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import datetime
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CaseDocument:
    """Represents a legal case document."""
    doc_id: str
    doc_type: str
    content: str
    metadata: Dict[str, Any]
    
    def get_summary(self, max_length: int = 200) -> str:
        """Get a summary of the document."""
        if len(self.content) <= max_length:
            return self.content
        return self.content[:max_length] + "..."


@dataclass
class LLMAnalysis:
    """Represents an LLM analysis result."""
    analysis_id: str
    case_id: str
    analysis_type: str
    findings: List[str]
    recommendations: List[str]
    confidence: float
    timestamp: str


class CaseLLM:
    """Case-LLM model for legal case analysis."""
    
    def __init__(self, model_name: str = "gpt-4.1-mini"):
        self.model_name = model_name
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.client = None
        
        # Initialize OpenAI client if available
        if self.api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI()
                logger.info(f"Initialized Case-LLM with model: {model_name}")
            except ImportError:
                logger.warning("OpenAI client not available, using mock mode")
        else:
            logger.warning("OpenAI API key not found, using mock mode")
    
    def analyze_case_summary(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a case and generate a summary."""
        case_id = case_data.get('case_id', 'unknown')
        case_description = case_data.get('description', '')
        
        if self.client:
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a legal case analyst. Provide concise, structured analysis of legal cases."
                        },
                        {
                            "role": "user",
                            "content": f"Analyze this legal case and provide key findings:\n\n{case_description}"
                        }
                    ],
                    temperature=0.3,
                    max_tokens=500
                )
                
                analysis_text = response.choices[0].message.content
                
                return {
                    'case_id': case_id,
                    'summary': analysis_text,
                    'model': self.model_name,
                    'timestamp': datetime.datetime.now().isoformat()
                }
            except Exception as e:
                logger.error(f"LLM analysis failed: {e}")
                return self._mock_analysis(case_id, case_description)
        else:
            return self._mock_analysis(case_id, case_description)
    
    def _mock_analysis(self, case_id: str, case_description: str) -> Dict[str, Any]:
        """Generate mock analysis when LLM is not available."""
        return {
            'case_id': case_id,
            'summary': f"Mock analysis for case {case_id}. The case involves complex legal matters requiring detailed investigation. Key areas of focus include evidence analysis, witness testimony evaluation, and legal precedent research.",
            'model': 'mock',
            'timestamp': datetime.datetime.now().isoformat()
        }
    
    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extract legal entities from text."""
        if self.client:
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {
                            "role": "system",
                            "content": "Extract legal entities (people, organizations, locations, dates) from the text. Return as JSON array."
                        },
                        {
                            "role": "user",
                            "content": text
                        }
                    ],
                    temperature=0.1,
                    max_tokens=300
                )
                
                entities_text = response.choices[0].message.content
                
                # Try to parse as JSON
                try:
                    entities = json.loads(entities_text)
                    return entities if isinstance(entities, list) else []
                except json.JSONDecodeError:
                    return self._mock_entities()
                
            except Exception as e:
                logger.error(f"Entity extraction failed: {e}")
                return self._mock_entities()
        else:
            return self._mock_entities()
    
    def _mock_entities(self) -> List[Dict[str, Any]]:
        """Generate mock entities."""
        return [
            {'type': 'person', 'name': 'John Doe', 'role': 'defendant'},
            {'type': 'person', 'name': 'Jane Smith', 'role': 'plaintiff'},
            {'type': 'organization', 'name': 'ABC Corporation', 'role': 'third_party'},
            {'type': 'location', 'name': 'Johannesburg', 'role': 'jurisdiction'},
            {'type': 'date', 'value': '2025-01-15', 'role': 'incident_date'}
        ]
    
    def generate_legal_brief(self, case_data: Dict[str, Any]) -> str:
        """Generate a legal brief for a case."""
        case_id = case_data.get('case_id', 'unknown')
        case_facts = case_data.get('facts', '')
        legal_issues = case_data.get('legal_issues', [])
        
        if self.client:
            try:
                prompt = f"""Generate a legal brief for the following case:

Case ID: {case_id}
Facts: {case_facts}
Legal Issues: {', '.join(legal_issues)}

Include:
1. Case Summary
2. Legal Issues
3. Analysis
4. Recommendations
"""
                
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a legal brief writer. Generate professional, structured legal briefs."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.4,
                    max_tokens=1000
                )
                
                return response.choices[0].message.content
                
            except Exception as e:
                logger.error(f"Brief generation failed: {e}")
                return self._mock_brief(case_id)
        else:
            return self._mock_brief(case_id)
    
    def _mock_brief(self, case_id: str) -> str:
        """Generate mock legal brief."""
        return f"""LEGAL BRIEF - Case {case_id}

1. CASE SUMMARY
This matter involves complex legal issues requiring careful analysis and consideration of applicable law.

2. LEGAL ISSUES
- Issue 1: Determination of liability
- Issue 2: Assessment of damages
- Issue 3: Application of relevant statutes

3. ANALYSIS
The facts of this case present several key considerations. The evidence suggests multiple parties may bear responsibility. Legal precedent supports a thorough examination of all relevant factors.

4. RECOMMENDATIONS
- Conduct comprehensive discovery
- Engage expert witnesses
- Prepare for potential settlement negotiations
- Develop robust trial strategy

Prepared by Case-LLM Analysis System
Date: {datetime.datetime.now().strftime('%Y-%m-%d')}
"""
    
    def assess_case_strength(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess the strength of a legal case."""
        evidence_quality = case_data.get('evidence_quality', 0.5)
        legal_merit = case_data.get('legal_merit', 0.5)
        precedent_support = case_data.get('precedent_support', 0.5)
        
        # Calculate overall strength
        weights = {'evidence': 0.4, 'legal_merit': 0.35, 'precedent': 0.25}
        
        overall_strength = (
            evidence_quality * weights['evidence'] +
            legal_merit * weights['legal_merit'] +
            precedent_support * weights['precedent']
        )
        
        # Determine rating
        if overall_strength >= 0.75:
            rating = 'strong'
        elif overall_strength >= 0.5:
            rating = 'moderate'
        else:
            rating = 'weak'
        
        return {
            'overall_strength': overall_strength,
            'rating': rating,
            'components': {
                'evidence_quality': evidence_quality,
                'legal_merit': legal_merit,
                'precedent_support': precedent_support
            },
            'recommendations': self._generate_strength_recommendations(rating)
        }
    
    def _generate_strength_recommendations(self, rating: str) -> List[str]:
        """Generate recommendations based on case strength."""
        recommendations = {
            'strong': [
                'Proceed with confidence to trial',
                'Consider aggressive settlement position',
                'Prepare comprehensive evidence presentation'
            ],
            'moderate': [
                'Strengthen evidence collection',
                'Explore settlement opportunities',
                'Consider expert witness testimony',
                'Review legal strategy'
            ],
            'weak': [
                'Conduct thorough case review',
                'Seek additional evidence',
                'Consider alternative dispute resolution',
                'Evaluate settlement options carefully'
            ]
        }
        
        return recommendations.get(rating, [])
    
    def predict_outcome(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict likely case outcome."""
        case_strength = self.assess_case_strength(case_data)
        
        # Simple prediction based on strength
        strength_score = case_strength['overall_strength']
        
        if strength_score >= 0.7:
            predicted_outcome = 'favorable'
            confidence = 0.75 + (strength_score - 0.7) * 0.5
        elif strength_score >= 0.4:
            predicted_outcome = 'uncertain'
            confidence = 0.5
        else:
            predicted_outcome = 'unfavorable'
            confidence = 0.6 + (0.4 - strength_score) * 0.5
        
        return {
            'predicted_outcome': predicted_outcome,
            'confidence': min(confidence, 0.95),
            'case_strength': case_strength,
            'factors': [
                'Evidence quality',
                'Legal precedent',
                'Jurisdiction considerations',
                'Witness credibility'
            ]
        }


def run_case_llm_analysis(case_data: Dict[str, Any], config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Run Case-LLM analysis on case data."""
    if config is None:
        config = {}
    
    model_name = config.get('model_name', 'gpt-4.1-mini')
    
    logger.info("Starting Case-LLM analysis")
    
    # Initialize model
    llm = CaseLLM(model_name)
    
    # Perform various analyses
    summary = llm.analyze_case_summary(case_data)
    entities = llm.extract_entities(case_data.get('description', ''))
    strength_assessment = llm.assess_case_strength(case_data)
    outcome_prediction = llm.predict_outcome(case_data)
    
    # Generate brief if requested
    brief = None
    if config.get('generate_brief', False):
        brief = llm.generate_legal_brief(case_data)
    
    logger.info("Case-LLM analysis completed")
    
    return {
        'simulation_type': 'case_llm',
        'model': model_name,
        'case_id': case_data.get('case_id', 'unknown'),
        'summary': summary,
        'entities': entities,
        'strength_assessment': strength_assessment,
        'outcome_prediction': outcome_prediction,
        'brief': brief,
        'timestamp': datetime.datetime.now().isoformat()
    }


def generate_sample_case() -> Dict[str, Any]:
    """Generate sample case data for testing."""
    return {
        'case_id': 'CASE-2025-001',
        'case_number': '(GP) 12345/2025',
        'description': 'This case involves a commercial dispute between two parties regarding breach of contract. The plaintiff alleges that the defendant failed to deliver goods as specified in the agreement dated January 15, 2025. The defendant contests the allegations and claims force majeure.',
        'facts': 'Contract signed on January 15, 2025. Delivery deadline was March 1, 2025. Defendant failed to deliver. Plaintiff suffered financial losses.',
        'legal_issues': ['Breach of contract', 'Force majeure defense', 'Damages calculation'],
        'evidence_quality': 0.75,
        'legal_merit': 0.70,
        'precedent_support': 0.65
    }


if __name__ == "__main__":
    # Run sample analysis
    case_data = generate_sample_case()
    results = run_case_llm_analysis(case_data, {'generate_brief': True})
    print(f"Analysis completed for case: {results['case_id']}")
    print(f"Predicted outcome: {results['outcome_prediction']['predicted_outcome']}")

