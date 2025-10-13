#!/usr/bin/env python3
"""
Unified Simulation Runner for AnalytiCase

This module provides a unified interface to run all simulation models
and generate comprehensive analysis results.
"""

import sys
import os
import logging
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

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SimulationRunner:
    """Unified simulation runner for all models."""
    
    def __init__(self, output_dir: str = None):
        self.output_dir = output_dir or os.path.join(os.path.dirname(__file__), 'results')
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.results = {}
        self.timestamp = datetime.now().isoformat()
        
        logger.info(f"Initialized SimulationRunner (output: {self.output_dir})")
    
    def run_all_simulations(self, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Run all simulation models."""
        if config is None:
            config = {}
        
        logger.info("=" * 80)
        logger.info("Starting comprehensive simulation suite")
        logger.info("=" * 80)
        
        # Run Agent-Based Simulation
        logger.info("\n[1/5] Running Agent-Based Simulation...")
        try:
            agent_config = config.get('agent_based', {
                'num_investigators': 5,
                'num_attorneys': 8,
                'num_judges': 3,
                'num_steps': 100
            })
            self.results['agent_based'] = run_agent_simulation(agent_config)
            logger.info("✓ Agent-Based Simulation completed successfully")
        except Exception as e:
            logger.error(f"✗ Agent-Based Simulation failed: {e}")
            self.results['agent_based'] = {'error': str(e)}
        
        # Run Discrete-Event Simulation
        logger.info("\n[2/5] Running Discrete-Event Simulation...")
        try:
            des_config = config.get('discrete_event', {
                'num_cases': 50,
                'simulation_duration': 365.0
            })
            self.results['discrete_event'] = run_discrete_event_simulation(des_config)
            logger.info("✓ Discrete-Event Simulation completed successfully")
        except Exception as e:
            logger.error(f"✗ Discrete-Event Simulation failed: {e}")
            self.results['discrete_event'] = {'error': str(e)}
        
        # Run System Dynamics Simulation
        logger.info("\n[3/5] Running System Dynamics Simulation...")
        try:
            sd_config = config.get('system_dynamics', {
                'duration': 365.0,
                'dt': 1.0
            })
            self.results['system_dynamics'] = run_system_dynamics_simulation(sd_config)
            logger.info("✓ System Dynamics Simulation completed successfully")
        except Exception as e:
            logger.error(f"✗ System Dynamics Simulation failed: {e}")
            self.results['system_dynamics'] = {'error': str(e)}
        
        # Run HyperGNN Analysis
        logger.info("\n[4/5] Running HyperGNN Analysis...")
        try:
            hypergnn_config = config.get('hyper_gnn', {
                'input_dim': 64,
                'hidden_dim': 32,
                'num_layers': 2
            })
            case_data = generate_sample_case_data()
            self.results['hyper_gnn'] = run_hypergnn_analysis(case_data, hypergnn_config)
            logger.info("✓ HyperGNN Analysis completed successfully")
        except Exception as e:
            logger.error(f"✗ HyperGNN Analysis failed: {e}")
            self.results['hyper_gnn'] = {'error': str(e)}
        
        # Run Case-LLM Analysis
        logger.info("\n[5/5] Running Case-LLM Analysis...")
        try:
            llm_config = config.get('case_llm', {
                'model_name': 'gpt-4.1-mini',
                'generate_brief': True
            })
            case_data = generate_sample_case()
            self.results['case_llm'] = run_case_llm_analysis(case_data, llm_config)
            logger.info("✓ Case-LLM Analysis completed successfully")
        except Exception as e:
            logger.error(f"✗ Case-LLM Analysis failed: {e}")
            self.results['case_llm'] = {'error': str(e)}
        
        logger.info("\n" + "=" * 80)
        logger.info("All simulations completed")
        logger.info("=" * 80)
        
        # Generate summary
        summary = self.generate_summary()
        
        # Save results
        self.save_results()
        
        return {
            'timestamp': self.timestamp,
            'summary': summary,
            'results': self.results
        }
    
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
        results_file = os.path.join(self.output_dir, f'simulation_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
        
        with open(results_file, 'w') as f:
            json.dump({
                'timestamp': self.timestamp,
                'results': self.results
            }, f, indent=2, default=str)
        
        logger.info(f"Results saved to: {results_file}")
        
        # Save summary report
        summary_file = os.path.join(self.output_dir, f'simulation_summary_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')
        
        with open(summary_file, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("ANALYTICASE SIMULATION SUITE - COMPREHENSIVE REPORT\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Timestamp: {self.timestamp}\n\n")
            
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
        
        logger.info(f"Summary saved to: {summary_file}")


def main():
    """Main entry point for simulation runner."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Run AnalytiCase simulation suite')
    parser.add_argument('--config', type=str, help='Path to configuration JSON file')
    parser.add_argument('--output', type=str, help='Output directory for results')
    
    args = parser.parse_args()
    
    # Load configuration if provided
    config = {}
    if args.config and os.path.exists(args.config):
        with open(args.config, 'r') as f:
            config = json.load(f)
    
    # Run simulations
    runner = SimulationRunner(output_dir=args.output)
    results = runner.run_all_simulations(config)
    
    print("\n" + "=" * 80)
    print("SIMULATION SUITE COMPLETED")
    print("=" * 80)
    print(f"\nSuccessful: {results['summary']['successful']}/{results['summary']['total_simulations']}")
    print(f"Results saved to: {runner.output_dir}")


if __name__ == "__main__":
    main()

