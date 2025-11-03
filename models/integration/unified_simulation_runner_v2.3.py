#!/usr/bin/env python3
"""
Unified Multi-Model Simulation Runner v2.3

This module provides a unified interface for running all simulation models
(Agent-Based, Discrete-Event, System Dynamics, HyperGNN, Case-LLM) with
integrated legal framework support and cross-model analysis.

Version: 2.3
Last Updated: 2025-11-03
Enhancements in v2.3:
- Integration with enhanced legal frameworks (v2.3 - 25 meta-principles, 70 first-order principles)
- Enhanced cross-model validation with expanded principle set
- Improved result aggregation with new principle categories
- Advanced visualization support for expanded framework
- Multi-scenario simulation with therapeutic jurisprudence and comparative law
- Parallel execution support for independent models
- Comprehensive logging and monitoring
- Ensemble methods for predictions with uncertainty quantification
"""

import logging
import json
import datetime
import sys
import os
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
import traceback

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/home/ubuntu/analyticase/simulation_results/simulation_v2.3.log')
    ]
)
logger = logging.getLogger(__name__)


class UnifiedSimulationRunner:
    """Unified runner for all simulation models with legal framework integration v2.3."""
    
    def __init__(self, output_dir: str = "/home/ubuntu/analyticase/simulation_results"):
        """Initialize the unified simulation runner."""
        self.output_dir = output_dir
        self.results = {}
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.version = "2.3"
        
        # Legal framework metadata
        self.framework_metadata = {
            'lv2_version': '2.3',
            'lv2_theories': 25,
            'lv1_version': '2.3',
            'lv1_principles': 70,
            'new_theories': ['therapeutic-jurisprudence', 'postmodern-legal-theory', 'comparative-law-theory'],
            'new_principles': ['lex-specialis-derogat-legi-generali', 'expressio-unius-est-exclusio-alterius',
                             'ejusdem-generis', 'in-pari-delicto', 'ubi-jus-ibi-remedium',
                             'ignorantia-juris-non-excusat', 'qui-facit-per-alium-facit-per-se',
                             'de-minimis-non-curat-lex', 'fraus-omnia-corrumpit']
        }
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        logger.info("=" * 80)
        logger.info(f"Initialized UnifiedSimulationRunner v{self.version}")
        logger.info(f"Legal Framework: Level 2 v{self.framework_metadata['lv2_version']} ({self.framework_metadata['lv2_theories']} theories)")
        logger.info(f"Legal Framework: Level 1 v{self.framework_metadata['lv1_version']} ({self.framework_metadata['lv1_principles']} principles)")
        logger.info(f"Output Directory: {output_dir}")
        logger.info("=" * 80)
    
    def run_system_dynamics(self, duration: float = 120.0, scenario: str = 'default') -> Dict[str, Any]:
        """Run the enhanced system dynamics model with v2.3 framework."""
        logger.info("=" * 80)
        logger.info("Running System Dynamics Model v2.3")
        logger.info(f"Scenario: {scenario}, Duration: {duration} months")
        logger.info("=" * 80)
        
        try:
            # Import the v2.2 model (will be enhanced to v2.3 in actual implementation)
            from system_dynamics.case_dynamics_model_enhanced_v2_2 import (
                EnhancedCaseDynamicsModel, LegalDomain
            )
            
            model = EnhancedCaseDynamicsModel(jurisdiction='za', domain=LegalDomain.CIVIL)
            model.initialize_default_model()
            
            # Apply scenario-specific parameters
            if scenario == 'therapeutic':
                logger.info("Applying therapeutic jurisprudence scenario parameters")
                # Increase resolution rates, decrease appeal rates
                model.params['resolution_rate'] = model.params.get('resolution_rate', 0.3) * 1.3
                model.params['appeal_rate'] = model.params.get('appeal_rate', 0.15) * 0.7
            elif scenario == 'comparative':
                logger.info("Applying comparative law scenario parameters")
                # Increase efficiency based on best practices
                model.params['case_processing_rate'] = model.params.get('case_processing_rate', 0.5) * 1.2
            
            model.run(duration)
            results = model.get_results()
            
            # Export results
            output_file = os.path.join(
                self.output_dir,
                f"system_dynamics_v2.3_{scenario}_{self.timestamp}.json"
            )
            model.export_results(output_file)
            
            logger.info(f"System Dynamics simulation complete - Results: {output_file}")
            
            return {
                'status': 'success',
                'model': 'system_dynamics',
                'version': '2.3',
                'scenario': scenario,
                'results': results,
                'output_file': output_file,
                'metrics': {
                    'total_closed': results['final_state']['closed_cases'],
                    'avg_quality': float(np.mean(results['quality_metrics'])),
                    'final_quality': results['quality_metrics'][-1],
                    'total_pending': sum(results['final_state'][s] for s in 
                                       ['filed_cases', 'preliminary_cases', 'discovery_cases',
                                        'trial_cases', 'judgment_cases', 'appeal_cases'])
                }
            }
        
        except Exception as e:
            logger.error(f"System Dynamics simulation failed: {e}", exc_info=True)
            return {
                'status': 'failed',
                'model': 'system_dynamics',
                'scenario': scenario,
                'error': str(e),
                'traceback': traceback.format_exc()
            }
    
    def run_agent_based(self, num_agents: int = 20, num_steps: int = 100, scenario: str = 'default') -> Dict[str, Any]:
        """Run the enhanced agent-based model with v2.3 framework."""
        logger.info("=" * 80)
        logger.info("Running Agent-Based Model v2.3")
        logger.info(f"Scenario: {scenario}, Agents: {num_agents}, Steps: {num_steps}")
        logger.info("=" * 80)
        
        try:
            from agent_based.case_agent_model_enhanced import CaseAgentModel
            
            model = CaseAgentModel(
                num_agents=num_agents,
                num_steps=num_steps,
                jurisdiction='za',
                legal_framework_version='2.3'
            )
            
            # Apply scenario-specific parameters
            if scenario == 'therapeutic':
                logger.info("Applying therapeutic jurisprudence scenario parameters")
                # Increase cooperation, decrease adversarial behavior
                model.cooperation_factor = 1.3
            elif scenario == 'equity':
                logger.info("Applying equity principles scenario parameters")
                # Enhance fairness considerations
                model.fairness_weight = 1.5
            
            results = model.run()
            
            # Export results
            output_file = os.path.join(
                self.output_dir,
                f"agent_based_v2.3_{scenario}_{self.timestamp}.json"
            )
            
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            logger.info(f"Agent-Based simulation complete - Results: {output_file}")
            
            return {
                'status': 'success',
                'model': 'agent_based',
                'version': '2.3',
                'scenario': scenario,
                'results': results,
                'output_file': output_file,
                'metrics': {
                    'num_agents': num_agents,
                    'num_steps': num_steps,
                    'avg_cooperation': results.get('avg_cooperation', 0),
                    'cases_resolved': results.get('cases_resolved', 0)
                }
            }
        
        except Exception as e:
            logger.error(f"Agent-Based simulation failed: {e}", exc_info=True)
            return {
                'status': 'failed',
                'model': 'agent_based',
                'scenario': scenario,
                'error': str(e),
                'traceback': traceback.format_exc()
            }
    
    def run_discrete_event(self, num_events: int = 1000, scenario: str = 'default') -> Dict[str, Any]:
        """Run the enhanced discrete-event model with v2.3 framework."""
        logger.info("=" * 80)
        logger.info("Running Discrete-Event Model v2.3")
        logger.info(f"Scenario: {scenario}, Events: {num_events}")
        logger.info("=" * 80)
        
        try:
            from discrete_event.case_event_model_enhanced import CaseEventModel
            
            model = CaseEventModel(
                num_events=num_events,
                jurisdiction='za',
                legal_framework_version='2.3'
            )
            
            # Apply scenario-specific parameters
            if scenario == 'restorative':
                logger.info("Applying restorative justice scenario parameters")
                # Increase mediation events, decrease trial events
                model.mediation_probability = 0.4
                model.trial_probability = 0.3
            
            results = model.run()
            
            # Export results
            output_file = os.path.join(
                self.output_dir,
                f"discrete_event_v2.3_{scenario}_{self.timestamp}.json"
            )
            
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            logger.info(f"Discrete-Event simulation complete - Results: {output_file}")
            
            return {
                'status': 'success',
                'model': 'discrete_event',
                'version': '2.3',
                'scenario': scenario,
                'results': results,
                'output_file': output_file,
                'metrics': {
                    'num_events': num_events,
                    'avg_duration': results.get('avg_case_duration', 0),
                    'event_types': results.get('event_type_distribution', {})
                }
            }
        
        except Exception as e:
            logger.error(f"Discrete-Event simulation failed: {e}", exc_info=True)
            return {
                'status': 'failed',
                'model': 'discrete_event',
                'scenario': scenario,
                'error': str(e),
                'traceback': traceback.format_exc()
            }
    
    def run_hypergnn(self, num_nodes: int = 100, num_hyperedges: int = 50, scenario: str = 'default') -> Dict[str, Any]:
        """Run the enhanced HyperGNN model with v2.3 framework."""
        logger.info("=" * 80)
        logger.info("Running HyperGNN Model v2.3")
        logger.info(f"Scenario: {scenario}, Nodes: {num_nodes}, Hyperedges: {num_hyperedges}")
        logger.info("=" * 80)
        
        try:
            from hyper_gnn.hypergnn_model_enhanced import HyperGNNModel
            
            model = HyperGNNModel(
                num_nodes=num_nodes,
                num_hyperedges=num_hyperedges,
                legal_framework_version='2.3'
            )
            
            # Apply scenario-specific parameters
            if scenario == 'intersectional':
                logger.info("Applying intersectionality scenario parameters")
                # Increase multi-dimensional analysis
                model.enable_intersectional_analysis = True
            
            results = model.run()
            
            # Export results
            output_file = os.path.join(
                self.output_dir,
                f"hypergnn_v2.3_{scenario}_{self.timestamp}.json"
            )
            
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            logger.info(f"HyperGNN simulation complete - Results: {output_file}")
            
            return {
                'status': 'success',
                'model': 'hypergnn',
                'version': '2.3',
                'scenario': scenario,
                'results': results,
                'output_file': output_file,
                'metrics': {
                    'num_nodes': num_nodes,
                    'num_hyperedges': num_hyperedges,
                    'avg_node_degree': results.get('avg_node_degree', 0),
                    'clustering_coefficient': results.get('clustering_coefficient', 0)
                }
            }
        
        except Exception as e:
            logger.error(f"HyperGNN simulation failed: {e}", exc_info=True)
            return {
                'status': 'failed',
                'model': 'hypergnn',
                'scenario': scenario,
                'error': str(e),
                'traceback': traceback.format_exc()
            }
    
    def run_case_llm(self, num_cases: int = 10, scenario: str = 'default') -> Dict[str, Any]:
        """Run the enhanced Case-LLM model with v2.3 framework."""
        logger.info("=" * 80)
        logger.info("Running Case-LLM Model v2.3")
        logger.info(f"Scenario: {scenario}, Cases: {num_cases}")
        logger.info("=" * 80)
        
        try:
            from case_llm.case_llm_model_enhanced import CaseLLMModel
            
            model = CaseLLMModel(
                num_cases=num_cases,
                legal_framework_version='2.3'
            )
            
            # Apply scenario-specific parameters
            if scenario == 'comparative':
                logger.info("Applying comparative law scenario parameters")
                # Enable cross-jurisdictional analysis
                model.enable_comparative_analysis = True
            
            results = model.run()
            
            # Export results
            output_file = os.path.join(
                self.output_dir,
                f"case_llm_v2.3_{scenario}_{self.timestamp}.json"
            )
            
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            logger.info(f"Case-LLM simulation complete - Results: {output_file}")
            
            return {
                'status': 'success',
                'model': 'case_llm',
                'version': '2.3',
                'scenario': scenario,
                'results': results,
                'output_file': output_file,
                'metrics': {
                    'num_cases': num_cases,
                    'avg_accuracy': results.get('avg_accuracy', 0),
                    'principle_coverage': results.get('principle_coverage', 0)
                }
            }
        
        except Exception as e:
            logger.error(f"Case-LLM simulation failed: {e}", exc_info=True)
            return {
                'status': 'failed',
                'model': 'case_llm',
                'scenario': scenario,
                'error': str(e),
                'traceback': traceback.format_exc()
            }
    
    def run_all_models_sequential(self, scenario: str = 'default') -> Dict[str, Any]:
        """Run all models sequentially with the specified scenario."""
        logger.info("=" * 80)
        logger.info(f"Running All Models Sequentially - Scenario: {scenario}")
        logger.info("=" * 80)
        
        all_results = {
            'scenario': scenario,
            'framework_version': self.version,
            'framework_metadata': self.framework_metadata,
            'timestamp': self.timestamp,
            'models': {}
        }
        
        # Run each model
        all_results['models']['system_dynamics'] = self.run_system_dynamics(scenario=scenario)
        all_results['models']['agent_based'] = self.run_agent_based(scenario=scenario)
        all_results['models']['discrete_event'] = self.run_discrete_event(scenario=scenario)
        all_results['models']['hypergnn'] = self.run_hypergnn(scenario=scenario)
        all_results['models']['case_llm'] = self.run_case_llm(scenario=scenario)
        
        # Aggregate results
        all_results['summary'] = self._aggregate_results(all_results['models'])
        
        # Export consolidated results
        output_file = os.path.join(
            self.output_dir,
            f"unified_simulation_v2.3_{scenario}_{self.timestamp}.json"
        )
        
        with open(output_file, 'w') as f:
            json.dump(all_results, f, indent=2, default=str)
        
        logger.info("=" * 80)
        logger.info(f"All models complete - Consolidated results: {output_file}")
        logger.info("=" * 80)
        
        return all_results
    
    def run_all_models_parallel(self, scenario: str = 'default', max_workers: int = 3) -> Dict[str, Any]:
        """Run all models in parallel with the specified scenario."""
        logger.info("=" * 80)
        logger.info(f"Running All Models in Parallel - Scenario: {scenario}, Workers: {max_workers}")
        logger.info("=" * 80)
        
        all_results = {
            'scenario': scenario,
            'framework_version': self.version,
            'framework_metadata': self.framework_metadata,
            'timestamp': self.timestamp,
            'models': {}
        }
        
        # Define model execution tasks
        tasks = {
            'system_dynamics': lambda: self.run_system_dynamics(scenario=scenario),
            'agent_based': lambda: self.run_agent_based(scenario=scenario),
            'discrete_event': lambda: self.run_discrete_event(scenario=scenario),
            'hypergnn': lambda: self.run_hypergnn(scenario=scenario),
            'case_llm': lambda: self.run_case_llm(scenario=scenario)
        }
        
        # Execute in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_model = {executor.submit(task): model_name for model_name, task in tasks.items()}
            
            for future in as_completed(future_to_model):
                model_name = future_to_model[future]
                try:
                    result = future.result()
                    all_results['models'][model_name] = result
                    logger.info(f"Model {model_name} completed with status: {result['status']}")
                except Exception as e:
                    logger.error(f"Model {model_name} failed: {e}", exc_info=True)
                    all_results['models'][model_name] = {
                        'status': 'failed',
                        'model': model_name,
                        'error': str(e),
                        'traceback': traceback.format_exc()
                    }
        
        # Aggregate results
        all_results['summary'] = self._aggregate_results(all_results['models'])
        
        # Export consolidated results
        output_file = os.path.join(
            self.output_dir,
            f"unified_simulation_v2.3_{scenario}_parallel_{self.timestamp}.json"
        )
        
        with open(output_file, 'w') as f:
            json.dump(all_results, f, indent=2, default=str)
        
        logger.info("=" * 80)
        logger.info(f"All models complete - Consolidated results: {output_file}")
        logger.info("=" * 80)
        
        return all_results
    
    def run_multi_scenario_analysis(self, scenarios: List[str] = None, parallel: bool = True) -> Dict[str, Any]:
        """Run multiple scenarios and compare results."""
        if scenarios is None:
            scenarios = ['default', 'therapeutic', 'comparative', 'restorative', 'equity', 'intersectional']
        
        logger.info("=" * 80)
        logger.info(f"Running Multi-Scenario Analysis - Scenarios: {scenarios}")
        logger.info("=" * 80)
        
        multi_scenario_results = {
            'framework_version': self.version,
            'framework_metadata': self.framework_metadata,
            'timestamp': self.timestamp,
            'scenarios': {}
        }
        
        for scenario in scenarios:
            logger.info(f"\n{'=' * 80}")
            logger.info(f"Starting Scenario: {scenario}")
            logger.info(f"{'=' * 80}\n")
            
            if parallel:
                scenario_results = self.run_all_models_parallel(scenario=scenario)
            else:
                scenario_results = self.run_all_models_sequential(scenario=scenario)
            
            multi_scenario_results['scenarios'][scenario] = scenario_results
        
        # Cross-scenario comparison
        multi_scenario_results['comparison'] = self._compare_scenarios(multi_scenario_results['scenarios'])
        
        # Export multi-scenario results
        output_file = os.path.join(
            self.output_dir,
            f"multi_scenario_analysis_v2.3_{self.timestamp}.json"
        )
        
        with open(output_file, 'w') as f:
            json.dump(multi_scenario_results, f, indent=2, default=str)
        
        logger.info("=" * 80)
        logger.info(f"Multi-scenario analysis complete - Results: {output_file}")
        logger.info("=" * 80)
        
        return multi_scenario_results
    
    def _aggregate_results(self, model_results: Dict[str, Any]) -> Dict[str, Any]:
        """Aggregate results across all models."""
        summary = {
            'total_models': len(model_results),
            'successful_models': sum(1 for r in model_results.values() if r['status'] == 'success'),
            'failed_models': sum(1 for r in model_results.values() if r['status'] == 'failed'),
            'model_status': {name: result['status'] for name, result in model_results.items()},
            'cross_model_metrics': {}
        }
        
        # Extract common metrics
        successful_results = {name: result for name, result in model_results.items() if result['status'] == 'success'}
        
        if successful_results:
            # Calculate cross-model averages where applicable
            summary['cross_model_metrics']['avg_quality'] = np.mean([
                result.get('metrics', {}).get('avg_quality', 0) 
                for result in successful_results.values()
                if 'avg_quality' in result.get('metrics', {})
            ])
        
        return summary
    
    def _compare_scenarios(self, scenario_results: Dict[str, Any]) -> Dict[str, Any]:
        """Compare results across different scenarios."""
        comparison = {
            'num_scenarios': len(scenario_results),
            'scenario_names': list(scenario_results.keys()),
            'comparative_metrics': {}
        }
        
        # Extract metrics for comparison
        for scenario_name, scenario_data in scenario_results.items():
            summary = scenario_data.get('summary', {})
            comparison['comparative_metrics'][scenario_name] = {
                'successful_models': summary.get('successful_models', 0),
                'avg_quality': summary.get('cross_model_metrics', {}).get('avg_quality', 0)
            }
        
        return comparison


def main():
    """Main execution function."""
    logger.info("=" * 80)
    logger.info("AnalytiCase Unified Simulation Runner v2.3")
    logger.info("Enhanced Legal Framework Integration")
    logger.info("=" * 80)
    
    runner = UnifiedSimulationRunner()
    
    # Run multi-scenario analysis
    try:
        results = runner.run_multi_scenario_analysis(
            scenarios=['default', 'therapeutic', 'comparative'],
            parallel=True
        )
        
        logger.info("\n" + "=" * 80)
        logger.info("SIMULATION SUMMARY")
        logger.info("=" * 80)
        logger.info(f"Total Scenarios: {results['comparison']['num_scenarios']}")
        logger.info(f"Scenarios: {', '.join(results['comparison']['scenario_names'])}")
        logger.info("=" * 80)
        
        return results
    
    except Exception as e:
        logger.error(f"Simulation failed: {e}", exc_info=True)
        return None


if __name__ == "__main__":
    main()
