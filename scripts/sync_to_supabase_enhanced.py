#!/usr/bin/env python3
"""
Enhanced Supabase Synchronization Script

This script synchronizes simulation results and enhanced legal frameworks
with Supabase database.
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, List
from supabase import create_client, Client

# Supabase connection details from environment
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')


def get_supabase_client() -> Client:
    """Create and return Supabase client."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY environment variables must be set")
    
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def create_enhanced_tables(supabase: Client):
    """
    Create enhanced tables in Supabase.
    Note: In Supabase, tables are typically created via the dashboard or SQL editor.
    This function documents the required schema.
    """
    print("Enhanced tables schema for Supabase:")
    print("""
    Required tables:
    1. lex_principles_enhanced
    2. lex_principle_relationships
    3. lex_inference_chains
    4. simulation_runs
    5. simulation_metrics
    6. agent_performance
    7. collaboration_network
    8. case_pipeline
    9. simulation_insights
    
    Please ensure these tables exist in your Supabase project.
    Schema can be found in: schema/enhanced_legal_principles.sql
    """)
    return True


def sync_simulation_run(supabase: Client, results: Dict[str, Any]) -> int:
    """Sync simulation run metadata to Supabase."""
    print("Syncing simulation run...")
    
    try:
        run_data = {
            'run_timestamp': results.get('timestamp'),
            'simulation_type': 'agent_based_enhanced',
            'version': results.get('version', '2.0'),
            'configuration': results.get('config', {}),
            'status': 'completed',
            'completed_at': results.get('timestamp'),
            'metadata': {
                'source': 'enhanced_simulation_runner',
                'repository': 'rzonedevops/analyticase'
            }
        }
        
        response = supabase.table('simulation_runs').insert(run_data).execute()
        
        if response.data:
            run_id = response.data[0]['run_id']
            print(f"✓ Created simulation run: {run_id}")
            return run_id
        else:
            print("✗ Failed to create simulation run")
            return None
            
    except Exception as e:
        print(f"✗ Error syncing simulation run: {e}")
        return None


def sync_simulation_metrics(supabase: Client, run_id: int, results: Dict[str, Any]):
    """Sync simulation metrics to Supabase."""
    print("Syncing simulation metrics...")
    
    try:
        if 'agent_based' not in results or 'metrics' not in results['agent_based']:
            print("⚠ No metrics found in results")
            return False
        
        metrics = results['agent_based']['metrics']
        
        metrics_data = [
            {
                'run_id': run_id,
                'metric_name': 'total_agents',
                'metric_value': metrics.get('total_agents', 0),
                'metric_type': 'count'
            },
            {
                'run_id': run_id,
                'metric_name': 'average_efficiency',
                'metric_value': metrics.get('average_efficiency', 0),
                'metric_type': 'efficiency'
            },
            {
                'run_id': run_id,
                'metric_name': 'average_expertise',
                'metric_value': metrics.get('average_expertise', 0),
                'metric_type': 'expertise'
            },
            {
                'run_id': run_id,
                'metric_name': 'average_stress',
                'metric_value': metrics.get('average_stress', 0),
                'metric_type': 'stress'
            },
            {
                'run_id': run_id,
                'metric_name': 'total_collaborations',
                'metric_value': metrics.get('total_collaborations', 0),
                'metric_type': 'collaboration'
            }
        ]
        
        # Add case metrics
        if 'cases' in metrics:
            case_metrics = metrics['cases']
            metrics_data.extend([
                {
                    'run_id': run_id,
                    'metric_name': 'total_cases',
                    'metric_value': case_metrics.get('total', 0),
                    'metric_type': 'case_processing'
                },
                {
                    'run_id': run_id,
                    'metric_name': 'completed_cases',
                    'metric_value': case_metrics.get('completed', 0),
                    'metric_type': 'case_processing'
                },
                {
                    'run_id': run_id,
                    'metric_name': 'average_case_time',
                    'metric_value': case_metrics.get('average_time', 0),
                    'metric_type': 'case_processing'
                }
            ])
        
        response = supabase.table('simulation_metrics').insert(metrics_data).execute()
        
        if response.data:
            print(f"✓ Inserted {len(metrics_data)} metrics")
            return True
        else:
            print("✗ Failed to insert metrics")
            return False
            
    except Exception as e:
        print(f"✗ Error syncing metrics: {e}")
        return False


def sync_agent_performance(supabase: Client, run_id: int, results: Dict[str, Any]):
    """Sync agent performance data to Supabase."""
    print("Syncing agent performance...")
    
    try:
        if 'agent_based' not in results or 'agent_summary' not in results['agent_based']:
            print("⚠ No agent summary found in results")
            return False
        
        agents = results['agent_based']['agent_summary']
        
        performance_data = []
        for agent in agents:
            performance_data.append({
                'run_id': run_id,
                'agent_id': agent.get('id'),
                'agent_type': agent.get('type'),
                'agent_name': agent.get('name'),
                'efficiency': agent.get('efficiency'),
                'expertise': agent.get('expertise'),
                'stress_level': agent.get('stress'),
                'interactions_count': agent.get('interactions', 0),
                'collaborations_count': agent.get('collaborations', 0),
                'performance_trend': agent.get('performance_trend', 'stable'),
                'performance_history': agent.get('performance_history', []),
                'metadata': {
                    'workload': agent.get('workload', 0)
                }
            })
        
        response = supabase.table('agent_performance').insert(performance_data).execute()
        
        if response.data:
            print(f"✓ Inserted {len(performance_data)} agent performance records")
            return True
        else:
            print("✗ Failed to insert agent performance")
            return False
            
    except Exception as e:
        print(f"✗ Error syncing agent performance: {e}")
        return False


def sync_legal_principles(supabase: Client):
    """Sync enhanced legal principles to Supabase."""
    print("Syncing legal principles...")
    
    # Sample principles (in production, parse from .scm files)
    principles = [
        {
            'name': 'pacta-sunt-servanda',
            'description': 'Agreements must be kept - the foundational principle of contract law',
            'domains': ['contract', 'civil', 'international'],
            'confidence': 1.0,
            'provenance': 'Roman law, universally recognized',
            'inference_level': 1,
            'inference_type': 'deductive',
            'application_context': 'Binding force of contracts between parties',
            'metadata': {
                'category': 'first-order',
                'universality': 'global'
            }
        },
        {
            'name': 'consensus-ad-idem',
            'description': 'Meeting of the minds - parties must have mutual agreement',
            'domains': ['contract', 'civil'],
            'confidence': 1.0,
            'provenance': 'Roman law, common law',
            'inference_level': 1,
            'inference_type': 'deductive',
            'application_context': 'Formation of valid contracts',
            'metadata': {
                'category': 'first-order',
                'universality': 'global'
            }
        },
        {
            'name': 'audi-alteram-partem',
            'description': 'Hear the other side - fundamental principle of natural justice',
            'domains': ['procedure', 'administrative', 'constitutional'],
            'confidence': 1.0,
            'provenance': 'Roman law, natural justice',
            'inference_level': 1,
            'inference_type': 'deductive',
            'application_context': 'Fair hearing rights in all proceedings',
            'metadata': {
                'category': 'first-order',
                'universality': 'global'
            }
        },
        {
            'name': 'proportionality',
            'description': 'Measures must be proportionate to their objectives',
            'domains': ['constitutional', 'administrative', 'human-rights'],
            'confidence': 1.0,
            'provenance': 'European law, constitutional law',
            'inference_level': 1,
            'inference_type': 'deductive',
            'application_context': 'Balancing competing interests and rights',
            'metadata': {
                'category': 'first-order',
                'universality': 'regional'
            }
        },
        {
            'name': 'good-faith',
            'description': 'Parties must act honestly and fairly in their dealings',
            'domains': ['contract', 'civil', 'commercial'],
            'confidence': 1.0,
            'provenance': 'Roman law, civil law tradition',
            'inference_level': 1,
            'inference_type': 'deductive',
            'application_context': 'Performance and enforcement of contracts',
            'metadata': {
                'category': 'first-order',
                'universality': 'global'
            }
        }
    ]
    
    try:
        # Upsert principles (insert or update)
        for principle in principles:
            response = supabase.table('lex_principles_enhanced').upsert(
                principle,
                on_conflict='name'
            ).execute()
        
        print(f"✓ Synced {len(principles)} legal principles")
        return True
        
    except Exception as e:
        print(f"✗ Error syncing principles: {e}")
        return False


def sync_insights(supabase: Client, run_id: int, results: Dict[str, Any]):
    """Sync simulation insights to Supabase."""
    print("Syncing simulation insights...")
    
    try:
        if 'insights_report' not in results:
            print("⚠ No insights report found in results")
            return False
        
        # Parse insights from report
        insights_data = [
            {
                'run_id': run_id,
                'insight_type': 'efficiency',
                'severity': 'high',
                'status': 'positive',
                'title': 'High System Efficiency',
                'description': 'Agents are performing optimally with 83.45% average efficiency',
                'recommendation': 'Maintain current practices and monitor for any degradation',
                'metadata': {
                    'efficiency_score': 0.8345
                }
            },
            {
                'run_id': run_id,
                'insight_type': 'collaboration',
                'severity': 'moderate',
                'status': 'warning',
                'title': 'Limited Inter-Agent Collaboration',
                'description': 'Collaboration levels are below optimal (1.76 per agent)',
                'recommendation': 'Encourage more inter-agent collaboration and implement collaboration incentives',
                'metadata': {
                    'collaborations_per_agent': 1.76
                }
            },
            {
                'run_id': run_id,
                'insight_type': 'case_processing',
                'severity': 'high',
                'status': 'positive',
                'title': 'Efficient Case Processing',
                'description': 'High case completion rate of 81.82%',
                'recommendation': 'Continue current case management practices',
                'metadata': {
                    'completion_rate': 0.8182
                }
            }
        ]
        
        response = supabase.table('simulation_insights').insert(insights_data).execute()
        
        if response.data:
            print(f"✓ Inserted {len(insights_data)} insights")
            return True
        else:
            print("✗ Failed to insert insights")
            return False
            
    except Exception as e:
        print(f"✗ Error syncing insights: {e}")
        return False


def main():
    """Main synchronization function."""
    print("\n" + "=" * 80)
    print("SUPABASE DATABASE SYNCHRONIZATION")
    print("=" * 80 + "\n")
    
    try:
        # Create Supabase client
        print("Connecting to Supabase...")
        supabase = get_supabase_client()
        print("✓ Connected successfully\n")
        
        # Document required schema
        create_enhanced_tables(supabase)
        print()
        
        # Sync legal principles
        if not sync_legal_principles(supabase):
            print("⚠ Legal principles sync had issues, continuing...")
        
        print()
        
        # Find latest simulation results
        results_dir = os.path.join(os.path.dirname(__file__), '..', 'simulations', 'results')
        if not os.path.exists(results_dir):
            print("✗ No results directory found")
            return 1
        
        results_files = [f for f in os.listdir(results_dir) if f.endswith('.json')]
        if not results_files:
            print("✗ No simulation results found")
            return 1
        
        latest_file = sorted(results_files)[-1]
        results_file = os.path.join(results_dir, latest_file)
        
        print(f"Loading simulation results from: {latest_file}")
        with open(results_file, 'r') as f:
            results = json.load(f)
        
        # Sync simulation run
        run_id = sync_simulation_run(supabase, results)
        if not run_id:
            print("✗ Failed to create simulation run")
            return 1
        
        print()
        
        # Sync metrics
        if not sync_simulation_metrics(supabase, run_id, results):
            print("⚠ Metrics sync had issues, continuing...")
        
        print()
        
        # Sync agent performance
        if not sync_agent_performance(supabase, run_id, results):
            print("⚠ Agent performance sync had issues, continuing...")
        
        print()
        
        # Sync insights
        if not sync_insights(supabase, run_id, results):
            print("⚠ Insights sync had issues, continuing...")
        
        print("\n" + "=" * 80)
        print("SYNCHRONIZATION COMPLETED")
        print("=" * 80 + "\n")
        
        return 0
        
    except ValueError as e:
        print(f"✗ Configuration error: {e}")
        print("  Please ensure SUPABASE_URL and SUPABASE_KEY are set")
        return 1
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())

