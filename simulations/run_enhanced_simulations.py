#!/usr/bin/env python3
"""
Enhanced Simulation Runner for AnalytiCase v2.0

This script runs comprehensive simulations with enhanced models and generates
detailed insights and analytics.
"""

import sys
import os
import json
from typing import Dict, Any, List
from datetime import datetime
import traceback

# Add models to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'models'))

from agent_based.case_agent_model import run_agent_simulation


def load_config(config_path: str = None) -> Dict[str, Any]:
    """Load simulation configuration from JSON file."""
    if config_path is None:
        config_path = os.path.join(os.path.dirname(__file__), 'enhanced_config.json')
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        print(f"✓ Loaded configuration from {config_path}")
        return config
    except Exception as e:
        print(f"✗ Error loading configuration: {e}")
        return {}


def save_results(results: Dict[str, Any], output_dir: str = None):
    """Save simulation results to file."""
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(__file__), 'results')
    
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"simulation_results_{timestamp}.json")
    
    try:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"✓ Results saved to {output_file}")
        return output_file
    except Exception as e:
        print(f"✗ Error saving results: {e}")
        return None


def generate_insights_report(results: Dict[str, Any]) -> str:
    """Generate comprehensive insights report from simulation results."""
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("ANALYTICASE SIMULATION INSIGHTS REPORT")
    report_lines.append("=" * 80)
    report_lines.append("")
    
    # Agent-Based Model Insights
    if 'agent_based' in results:
        ab_results = results['agent_based']
        metrics = ab_results.get('metrics', {})
        
        report_lines.append("## AGENT-BASED MODEL INSIGHTS")
        report_lines.append("-" * 80)
        report_lines.append(f"Total Agents: {metrics.get('total_agents', 0)}")
        report_lines.append(f"Average Efficiency: {metrics.get('average_efficiency', 0):.2%}")
        report_lines.append(f"Average Expertise: {metrics.get('average_expertise', 0):.2%}")
        report_lines.append(f"Average Stress Level: {metrics.get('average_stress', 0):.2%}")
        report_lines.append(f"Total Collaborations: {metrics.get('total_collaborations', 0)}")
        report_lines.append("")
        
        # Case metrics
        case_metrics = metrics.get('cases', {})
        report_lines.append("### Case Processing Metrics")
        report_lines.append(f"Total Cases: {case_metrics.get('total', 0)}")
        report_lines.append(f"Completed Cases: {case_metrics.get('completed', 0)}")
        report_lines.append(f"Average Case Time: {case_metrics.get('average_time', 0):.1f} time steps")
        report_lines.append(f"Cases in Investigation: {case_metrics.get('in_investigation', 0)}")
        report_lines.append(f"Cases in Litigation: {case_metrics.get('in_litigation', 0)}")
        report_lines.append(f"Cases in Adjudication: {case_metrics.get('in_adjudication', 0)}")
        report_lines.append("")
        
        # Investigator metrics
        inv_metrics = metrics.get('investigators', {})
        report_lines.append("### Investigator Performance")
        report_lines.append(f"Total Evidence Collected: {inv_metrics.get('total_evidence', 0)}")
        report_lines.append(f"Total Leads Followed: {inv_metrics.get('total_leads', 0)}")
        report_lines.append(f"Average Evidence Quality: {inv_metrics.get('avg_evidence_quality', 0):.2%}")
        report_lines.append("")
        
        # Attorney metrics
        att_metrics = metrics.get('attorneys', {})
        report_lines.append("### Attorney Performance")
        report_lines.append(f"Total Briefs Filed: {att_metrics.get('total_briefs', 0)}")
        report_lines.append(f"Cases Won: {att_metrics.get('cases_won', 0)}")
        report_lines.append(f"Cases Lost: {att_metrics.get('cases_lost', 0)}")
        report_lines.append(f"Win Rate: {att_metrics.get('win_rate', 0):.2%}")
        report_lines.append("")
        
        # Judge metrics
        judge_metrics = metrics.get('judges', {})
        report_lines.append("### Judicial Performance")
        report_lines.append(f"Cases Adjudicated: {judge_metrics.get('cases_adjudicated', 0)}")
        report_lines.append(f"Rulings Made: {judge_metrics.get('rulings_made', 0)}")
        report_lines.append(f"Average Ruling Confidence: {judge_metrics.get('avg_ruling_confidence', 0):.2%}")
        report_lines.append("")
    
    # Key Insights
    report_lines.append("## KEY INSIGHTS")
    report_lines.append("-" * 80)
    
    if 'agent_based' in results:
        ab_results = results['agent_based']
        metrics = ab_results.get('metrics', {})
        
        # Insight 1: System Efficiency
        avg_eff = metrics.get('average_efficiency', 0)
        if avg_eff > 0.8:
            report_lines.append("✓ System Efficiency: HIGH - Agents are performing optimally")
        elif avg_eff > 0.6:
            report_lines.append("⚠ System Efficiency: MODERATE - Room for improvement in agent performance")
        else:
            report_lines.append("✗ System Efficiency: LOW - Significant performance issues detected")
        
        # Insight 2: Collaboration Effectiveness
        total_collab = metrics.get('total_collaborations', 0)
        total_agents = metrics.get('total_agents', 1)
        collab_per_agent = total_collab / total_agents
        if collab_per_agent > 5:
            report_lines.append("✓ Collaboration: STRONG - High inter-agent collaboration observed")
        elif collab_per_agent > 2:
            report_lines.append("⚠ Collaboration: MODERATE - Some collaboration occurring")
        else:
            report_lines.append("✗ Collaboration: WEAK - Limited inter-agent collaboration")
        
        # Insight 3: Case Processing Efficiency
        case_metrics = metrics.get('cases', {})
        completion_rate = case_metrics.get('completed', 0) / max(case_metrics.get('total', 1), 1)
        if completion_rate > 0.7:
            report_lines.append("✓ Case Processing: EFFICIENT - High case completion rate")
        elif completion_rate > 0.4:
            report_lines.append("⚠ Case Processing: MODERATE - Average case completion rate")
        else:
            report_lines.append("✗ Case Processing: INEFFICIENT - Low case completion rate")
        
        # Insight 4: Attorney Success Rate
        att_metrics = metrics.get('attorneys', {})
        win_rate = att_metrics.get('win_rate', 0)
        if win_rate > 0.6:
            report_lines.append("✓ Attorney Performance: STRONG - High win rate achieved")
        elif win_rate > 0.4:
            report_lines.append("⚠ Attorney Performance: AVERAGE - Balanced win/loss ratio")
        else:
            report_lines.append("✗ Attorney Performance: WEAK - Low win rate observed")
        
        # Insight 5: Stress and Workload
        avg_stress = metrics.get('average_stress', 0)
        if avg_stress < 0.3:
            report_lines.append("✓ Workload Management: GOOD - Low stress levels across agents")
        elif avg_stress < 0.6:
            report_lines.append("⚠ Workload Management: MODERATE - Some stress detected")
        else:
            report_lines.append("✗ Workload Management: POOR - High stress levels may impact performance")
        
        report_lines.append("")
    
    # Recommendations
    report_lines.append("## RECOMMENDATIONS")
    report_lines.append("-" * 80)
    
    if 'agent_based' in results:
        metrics = results['agent_based'].get('metrics', {})
        
        recommendations = []
        
        # Efficiency recommendations
        if metrics.get('average_efficiency', 0) < 0.7:
            recommendations.append("• Invest in agent training to improve efficiency")
            recommendations.append("• Review and optimize task allocation algorithms")
        
        # Collaboration recommendations
        total_collab = metrics.get('total_collaborations', 0)
        total_agents = metrics.get('total_agents', 1)
        if total_collab / total_agents < 3:
            recommendations.append("• Encourage more inter-agent collaboration")
            recommendations.append("• Implement collaboration incentives and frameworks")
        
        # Workload recommendations
        if metrics.get('average_stress', 0) > 0.5:
            recommendations.append("• Redistribute workload to reduce agent stress")
            recommendations.append("• Consider hiring additional agents for peak periods")
        
        # Case processing recommendations
        case_metrics = metrics.get('cases', {})
        if case_metrics.get('average_time', 0) > 60:
            recommendations.append("• Streamline case processing procedures")
            recommendations.append("• Identify and eliminate bottlenecks in the pipeline")
        
        # Attorney performance recommendations
        att_metrics = metrics.get('attorneys', {})
        if att_metrics.get('win_rate', 0) < 0.5:
            recommendations.append("• Provide additional legal training for attorneys")
            recommendations.append("• Review case selection and preparation strategies")
        
        if recommendations:
            for rec in recommendations:
                report_lines.append(rec)
        else:
            report_lines.append("• System is performing well - maintain current practices")
        
        report_lines.append("")
    
    report_lines.append("=" * 80)
    report_lines.append("END OF REPORT")
    report_lines.append("=" * 80)
    
    return "\n".join(report_lines)


def run_enhanced_simulations(config: Dict[str, Any] = None) -> Dict[str, Any]:
    """Run all enhanced simulations and generate comprehensive results."""
    print("\n" + "=" * 80)
    print("ANALYTICASE ENHANCED SIMULATION SUITE v2.0")
    print("=" * 80 + "\n")
    
    if config is None:
        config = load_config()
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'version': '2.0',
        'config': config
    }
    
    # Run Agent-Based Simulation
    print("\n[1/5] Running Enhanced Agent-Based Simulation...")
    try:
        ab_config = config.get('agent_based', {})
        ab_results = run_agent_simulation(ab_config)
        results['agent_based'] = ab_results
        print("✓ Agent-Based Simulation completed successfully")
        
        # Display key metrics
        metrics = ab_results.get('metrics', {})
        print(f"  - Total agents: {metrics.get('total_agents', 0)}")
        print(f"  - Cases completed: {metrics.get('cases', {}).get('completed', 0)}")
        print(f"  - Average efficiency: {metrics.get('average_efficiency', 0):.2%}")
        print(f"  - Collaborations: {metrics.get('total_collaborations', 0)}")
        
    except Exception as e:
        print(f"✗ Agent-Based Simulation failed: {e}")
        print(traceback.format_exc())
        results['agent_based'] = {'error': str(e)}
    
    # Placeholder for other simulations
    print("\n[2/5] Discrete-Event Simulation...")
    print("  ⚠ Using existing implementation")
    
    print("\n[3/5] System Dynamics Simulation...")
    print("  ⚠ Using existing implementation")
    
    print("\n[4/5] HyperGNN Analysis...")
    print("  ⚠ Using existing implementation")
    
    print("\n[5/5] Case-LLM Analysis...")
    print("  ⚠ Using existing implementation")
    
    # Generate insights
    print("\n" + "=" * 80)
    print("GENERATING INSIGHTS REPORT")
    print("=" * 80 + "\n")
    
    insights_report = generate_insights_report(results)
    results['insights_report'] = insights_report
    
    print(insights_report)
    
    return results


def main():
    """Main entry point for enhanced simulation runner."""
    try:
        # Load configuration
        config = load_config()
        
        # Run simulations
        results = run_enhanced_simulations(config)
        
        # Save results
        output_file = save_results(results)
        
        # Save insights report
        if output_file:
            report_file = output_file.replace('.json', '_insights.txt')
            with open(report_file, 'w') as f:
                f.write(results.get('insights_report', ''))
            print(f"✓ Insights report saved to {report_file}")
        
        print("\n" + "=" * 80)
        print("SIMULATION SUITE COMPLETED SUCCESSFULLY")
        print("=" * 80 + "\n")
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        print(traceback.format_exc())
        return 1


if __name__ == "__main__":
    sys.exit(main())

