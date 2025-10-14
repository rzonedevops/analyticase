#!/usr/bin/env python3
"""
Enhanced Unified Simulation Runner for AnalytiCase

This version includes comprehensive logging with timestamped folder organization.
"""

import sys
import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

# Add models to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'models'))

from agent_based.case_agent_model import run_agent_simulation
from discrete_event.case_event_model import run_discrete_event_simulation
from system_dynamics.case_dynamics_model import run_system_dynamics_simulation
from hyper_gnn.hypergnn_model import run_hypergnn_analysis, generate_sample_case_data
from case_llm.case_llm_model import run_case_llm_analysis, generate_sample_case

from logging_config import setup_logging


class EnhancedSimulationRunner:
    """Enhanced simulation runner with comprehensive logging."""
    
    def __init__(self, output_dir: str = None, run_name: str = None):
        # Set up logging
        self.logger_manager = setup_logging(output_dir, run_name)
        self.logger = self.logger_manager.main_logger
        
        self.results = {}
        self.timestamp = self.logger_manager.timestamp
        
        self.logger.info("Enhanced Simulation Runner initialized")
    
    def run_all_simulations(self, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Run all simulation models with comprehensive logging."""
        if config is None:
            config = {}
        
        self.logger.info("=" * 80)
        self.logger.info("Starting comprehensive simulation suite")
        self.logger.info("=" * 80)
        
        # Create manifest
        manifest_metadata = {
            'purpose': 'Comprehensive legal case analysis',
            'models': ['agent_based', 'discrete_event', 'system_dynamics', 
                      'hyper_gnn', 'case_llm'],
            'configuration': config
        }
        self.logger_manager.create_run_manifest(manifest_metadata)
        
        # Run Agent-Based Simulation
        self._run_agent_based_simulation(config)
        
        # Run Discrete-Event Simulation
        self._run_discrete_event_simulation(config)
        
        # Run System Dynamics Simulation
        self._run_system_dynamics_simulation(config)
        
        # Run HyperGNN Analysis
        self._run_hypergnn_analysis(config)
        
        # Run Case-LLM Analysis
        self._run_case_llm_analysis(config)
        
        # Generate summary
        summary = self.generate_summary()
        
        # Save results
        self.save_results()
        
        self.logger.info("\n" + "=" * 80)
        self.logger.info("All simulations completed")
        self.logger.info("=" * 80)
        
        return {
            'timestamp': self.timestamp,
            'run_directory': str(self.logger_manager.run_dir),
            'summary': summary,
            'results': self.results
        }
    
    def _run_agent_based_simulation(self, config: Dict[str, Any]):
        """Run agent-based simulation with logging."""
        model_name = 'agent_based'
        logger = self.logger_manager.get_model_logger(model_name)
        
        try:
            agent_config = config.get('agent_based', {
                'num_investigators': 5,
                'num_attorneys': 8,
                'num_judges': 3,
                'num_steps': 100
            })
            
            self.logger_manager.log_simulation_start(model_name, agent_config)
            
            results = run_agent_simulation(agent_config)
            self.results['agent_based'] = results
            
            # Save detailed results
            data_path = self.logger_manager.get_data_path('agent_based_results.json')
            with open(data_path, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            self.logger_manager.log_simulation_end(model_name, results)
            logger.info(f"Results saved to: {data_path}")
            
        except Exception as e:
            self.logger_manager.log_error(model_name, e)
            self.results['agent_based'] = {'error': str(e)}
    
    def _run_discrete_event_simulation(self, config: Dict[str, Any]):
        """Run discrete-event simulation with logging."""
        model_name = 'discrete_event'
        logger = self.logger_manager.get_model_logger(model_name)
        
        try:
            des_config = config.get('discrete_event', {
                'num_cases': 50,
                'simulation_duration': 365.0
            })
            
            self.logger_manager.log_simulation_start(model_name, des_config)
            
            results = run_discrete_event_simulation(des_config)
            self.results['discrete_event'] = results
            
            # Save detailed results
            data_path = self.logger_manager.get_data_path('discrete_event_results.json')
            with open(data_path, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            self.logger_manager.log_simulation_end(model_name, results)
            logger.info(f"Results saved to: {data_path}")
            
        except Exception as e:
            self.logger_manager.log_error(model_name, e)
            self.results['discrete_event'] = {'error': str(e)}
    
    def _run_system_dynamics_simulation(self, config: Dict[str, Any]):
        """Run system dynamics simulation with logging."""
        model_name = 'system_dynamics'
        logger = self.logger_manager.get_model_logger(model_name)
        
        try:
            sd_config = config.get('system_dynamics', {
                'duration': 365.0,
                'dt': 1.0
            })
            
            self.logger_manager.log_simulation_start(model_name, sd_config)
            
            results = run_system_dynamics_simulation(sd_config)
            self.results['system_dynamics'] = results
            
            # Save detailed results
            data_path = self.logger_manager.get_data_path('system_dynamics_results.json')
            with open(data_path, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            self.logger_manager.log_simulation_end(model_name, results)
            logger.info(f"Results saved to: {data_path}")
            
        except Exception as e:
            self.logger_manager.log_error(model_name, e)
            self.results['system_dynamics'] = {'error': str(e)}
    
    def _run_hypergnn_analysis(self, config: Dict[str, Any]):
        """Run HyperGNN analysis with logging."""
        model_name = 'hyper_gnn'
        logger = self.logger_manager.get_model_logger(model_name)
        
        try:
            hypergnn_config = config.get('hyper_gnn', {
                'input_dim': 64,
                'hidden_dim': 32,
                'num_layers': 2
            })
            
            self.logger_manager.log_simulation_start(model_name, hypergnn_config)
            
            case_data = generate_sample_case_data()
            results = run_hypergnn_analysis(case_data, hypergnn_config)
            self.results['hyper_gnn'] = results
            
            # Save detailed results
            data_path = self.logger_manager.get_data_path('hypergnn_results.json')
            with open(data_path, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            self.logger_manager.log_simulation_end(model_name, results)
            logger.info(f"Results saved to: {data_path}")
            
        except Exception as e:
            self.logger_manager.log_error(model_name, e)
            self.results['hyper_gnn'] = {'error': str(e)}
    
    def _run_case_llm_analysis(self, config: Dict[str, Any]):
        """Run Case-LLM analysis with logging."""
        model_name = 'case_llm'
        logger = self.logger_manager.get_model_logger(model_name)
        
        try:
            llm_config = config.get('case_llm', {
                'model_name': 'gpt-4.1-mini',
                'generate_brief': True
            })
            
            self.logger_manager.log_simulation_start(model_name, llm_config)
            
            case_data = generate_sample_case()
            results = run_case_llm_analysis(case_data, llm_config)
            self.results['case_llm'] = results
            
            # Save detailed results
            data_path = self.logger_manager.get_data_path('case_llm_results.json')
            with open(data_path, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            # Save brief separately if generated
            if results.get('brief'):
                brief_path = self.logger_manager.get_report_path('legal_brief.txt')
                with open(brief_path, 'w') as f:
                    f.write(results['brief'])
                logger.info(f"Legal brief saved to: {brief_path}")
            
            self.logger_manager.log_simulation_end(model_name, results)
            logger.info(f"Results saved to: {data_path}")
            
        except Exception as e:
            self.logger_manager.log_error(model_name, e)
            self.results['case_llm'] = {'error': str(e)}
    
    def generate_summary(self) -> Dict[str, Any]:
        """Generate a summary of all simulation results."""
        summary = {
            'total_simulations': len(self.results),
            'successful': sum(1 for r in self.results.values() if 'error' not in r),
            'failed': sum(1 for r in self.results.values() if 'error' in r),
            'key_insights': []
        }
        
        # Extract key insights from each simulation
        if 'agent_based' in self.results and 'error' not in self.results['agent_based']:
            ab_metrics = self.results['agent_based'].get('metrics', {})
            summary['key_insights'].append({
                'model': 'Agent-Based',
                'insight': f"Simulated {ab_metrics.get('total_agents', 0)} agents with {ab_metrics.get('total_interactions', 0)} interactions"
            })
        
        if 'discrete_event' in self.results and 'error' not in self.results['discrete_event']:
            de_metrics = self.results['discrete_event'].get('case_metrics', {})
            summary['key_insights'].append({
                'model': 'Discrete-Event',
                'insight': f"Processed {de_metrics.get('total_cases', 0)} cases with {de_metrics.get('closure_rate', 0):.1f}% closure rate"
            })
        
        if 'system_dynamics' in self.results and 'error' not in self.results['system_dynamics']:
            sd_metrics = self.results['system_dynamics'].get('metrics', {})
            summary['key_insights'].append({
                'model': 'System Dynamics',
                'insight': f"System efficiency: {sd_metrics.get('system_efficiency_percent', 0):.1f}%, avg cycle time: {sd_metrics.get('average_cycle_time_days', 0):.1f} days"
            })
        
        if 'hyper_gnn' in self.results and 'error' not in self.results['hyper_gnn']:
            hg_stats = self.results['hyper_gnn'].get('hypergraph_stats', {})
            summary['key_insights'].append({
                'model': 'HyperGNN',
                'insight': f"Analyzed hypergraph with {hg_stats.get('num_nodes', 0)} nodes and {hg_stats.get('num_hyperedges', 0)} hyperedges"
            })
        
        if 'case_llm' in self.results and 'error' not in self.results['case_llm']:
            llm_outcome = self.results['case_llm'].get('outcome_prediction', {})
            summary['key_insights'].append({
                'model': 'Case-LLM',
                'insight': f"Predicted outcome: {llm_outcome.get('predicted_outcome', 'unknown')} (confidence: {llm_outcome.get('confidence', 0):.2f})"
            })
        
        return summary
    
    def save_results(self):
        """Save simulation results to files."""
        # Save complete results as JSON
        results_file = self.logger_manager.get_data_path('complete_results.json')
        
        with open(results_file, 'w') as f:
            json.dump({
                'timestamp': self.timestamp,
                'results': self.results
            }, f, indent=2, default=str)
        
        self.logger.info(f"Complete results saved to: {results_file}")
        
        # Save summary report
        summary_file = self.logger_manager.get_report_path('summary_report.txt')
        
        with open(summary_file, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("ANALYTICASE SIMULATION SUITE - COMPREHENSIVE REPORT\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Timestamp: {self.timestamp}\n")
            f.write(f"Run Directory: {self.logger_manager.run_dir}\n\n")
            
            summary = self.generate_summary()
            f.write(f"Total Simulations: {summary['total_simulations']}\n")
            f.write(f"Successful: {summary['successful']}\n")
            f.write(f"Failed: {summary['failed']}\n\n")
            
            f.write("KEY INSIGHTS:\n")
            f.write("-" * 80 + "\n")
            for insight in summary['key_insights']:
                f.write(f"\n{insight['model']}:\n")
                f.write(f"  {insight['insight']}\n")
            
            f.write("\n" + "=" * 80 + "\n")
        
        self.logger.info(f"Summary report saved to: {summary_file}")
        
        # Finalize logging
        self.logger_manager.finalize()


def main():
    """Main entry point for enhanced simulation runner."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Run AnalytiCase simulation suite with enhanced logging')
    parser.add_argument('--config', type=str, help='Path to configuration JSON file')
    parser.add_argument('--output', type=str, help='Output directory for results')
    parser.add_argument('--name', type=str, help='Name for this simulation run')
    
    args = parser.parse_args()
    
    # Load configuration if provided
    config = {}
    if args.config and os.path.exists(args.config):
        with open(args.config, 'r') as f:
            config = json.load(f)
    
    # Run simulations
    runner = EnhancedSimulationRunner(output_dir=args.output, run_name=args.name)
    results = runner.run_all_simulations(config)
    
    print("\n" + "=" * 80)
    print("SIMULATION SUITE COMPLETED")
    print("=" * 80)
    print(f"\nSuccessful: {results['summary']['successful']}/{results['summary']['total_simulations']}")
    print(f"Run directory: {results['run_directory']}")
    print("\nDirectory structure:")
    print(f"  ├── logs/          (execution logs for each model)")
    print(f"  ├── data/          (JSON results and raw data)")
    print(f"  ├── reports/       (summary reports and briefs)")
    print(f"  └── visualizations/ (charts and graphs)")


if __name__ == "__main__":
    main()

