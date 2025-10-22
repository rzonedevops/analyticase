#!/usr/bin/env python3
"""
Enhanced Neon Database Synchronization Script

This script synchronizes simulation results and enhanced legal frameworks
with the Neon database.
"""

import os
import json
import psycopg2
from datetime import datetime
from typing import Dict, Any, List

# Neon connection details (from environment or direct)
NEON_PROJECT_ID = "sweet-sea-69912135"
NEON_CONNECTION_STRING = os.getenv('NEON_CONNECTION_STRING', '')


def get_connection_string():
    """Get Neon connection string."""
    if NEON_CONNECTION_STRING:
        return NEON_CONNECTION_STRING
    
    # Construct from environment variables if available
    host = os.getenv('NEON_HOST', 'eastus2.azure.neon.tech')
    database = os.getenv('NEON_DATABASE', 'neondb')
    user = os.getenv('NEON_USER', '')
    password = os.getenv('NEON_PASSWORD', '')
    
    if user and password:
        return f"postgresql://{user}:{password}@{host}/{database}?sslmode=require"
    
    return None


def create_enhanced_tables(conn):
    """Create enhanced tables in Neon database."""
    print("Creating enhanced tables...")
    
    # Read schema file
    schema_file = os.path.join(os.path.dirname(__file__), '..', 'schema', 'enhanced_legal_principles.sql')
    
    try:
        with open(schema_file, 'r') as f:
            schema_sql = f.read()
        
        with conn.cursor() as cur:
            cur.execute(schema_sql)
            conn.commit()
        
        print("✓ Enhanced tables created successfully")
        return True
        
    except Exception as e:
        print(f"✗ Error creating tables: {e}")
        conn.rollback()
        return False


def sync_simulation_results(conn, results_file: str):
    """Sync simulation results to Neon database."""
    print(f"Syncing simulation results from {results_file}...")
    
    try:
        with open(results_file, 'r') as f:
            results = json.load(f)
        
        with conn.cursor() as cur:
            # Insert simulation run
            cur.execute("""
                INSERT INTO simulation_runs 
                (run_timestamp, simulation_type, version, configuration, status, completed_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING run_id
            """, (
                results.get('timestamp'),
                'agent_based_enhanced',
                results.get('version', '2.0'),
                json.dumps(results.get('config', {})),
                'completed',
                results.get('timestamp')
            ))
            
            run_id = cur.fetchone()[0]
            print(f"  - Created simulation run: {run_id}")
            
            # Insert metrics
            if 'agent_based' in results and 'metrics' in results['agent_based']:
                metrics = results['agent_based']['metrics']
                
                # Overall metrics
                metric_data = [
                    ('total_agents', metrics.get('total_agents', 0), 'count', None),
                    ('average_efficiency', metrics.get('average_efficiency', 0), 'efficiency', None),
                    ('average_expertise', metrics.get('average_expertise', 0), 'expertise', None),
                    ('average_stress', metrics.get('average_stress', 0), 'stress', None),
                    ('total_collaborations', metrics.get('total_collaborations', 0), 'collaboration', None),
                ]
                
                for name, value, mtype, agent_type in metric_data:
                    cur.execute("""
                        INSERT INTO simulation_metrics 
                        (run_id, metric_name, metric_value, metric_type, agent_type)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (run_id, name, value, mtype, agent_type))
                
                print(f"  - Inserted {len(metric_data)} metrics")
            
            # Insert agent performance
            if 'agent_based' in results and 'agent_summary' in results['agent_based']:
                agents = results['agent_based']['agent_summary']
                
                for agent in agents:
                    cur.execute("""
                        INSERT INTO agent_performance 
                        (run_id, agent_id, agent_type, agent_name, efficiency, 
                         expertise, stress_level, interactions_count, 
                         collaborations_count, performance_trend)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        run_id,
                        agent.get('id'),
                        agent.get('type'),
                        agent.get('name'),
                        agent.get('efficiency'),
                        agent.get('expertise'),
                        agent.get('stress'),
                        agent.get('interactions'),
                        agent.get('collaborations'),
                        agent.get('performance_trend')
                    ))
                
                print(f"  - Inserted {len(agents)} agent performance records")
            
            # Insert collaboration network
            if 'agent_based' in results and 'events' in results['agent_based']:
                events = results['agent_based']['events']
                
                for event in events:
                    if event.get('type') == 'case_collaboration':
                        cur.execute("""
                            INSERT INTO collaboration_network 
                            (run_id, agent_1_id, agent_2_id, interaction_type, 
                             outcome, outcome_score, timestamp, context)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """, (
                            run_id,
                            event.get('agent_1'),
                            event.get('agent_2'),
                            event.get('type'),
                            event.get('outcome'),
                            event.get('outcome_score'),
                            event.get('timestamp'),
                            json.dumps(event.get('context', {}))
                        ))
                
                print(f"  - Inserted {len(events)} collaboration records")
            
            # Insert case pipeline
            if 'agent_based' in results and 'case_pipeline' in results['agent_based']:
                cases = results['agent_based']['case_pipeline']
                
                for case in cases:
                    cur.execute("""
                        INSERT INTO case_pipeline 
                        (case_id, run_id, stage, complexity, time_in_system)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (
                        case.get('case_id'),
                        run_id,
                        case.get('stage'),
                        case.get('complexity'),
                        case.get('time_in_system')
                    ))
                
                print(f"  - Inserted {len(cases)} case records")
            
            conn.commit()
            print("✓ Simulation results synced successfully")
            return True
            
    except Exception as e:
        print(f"✗ Error syncing results: {e}")
        conn.rollback()
        return False


def sync_legal_principles(conn):
    """Sync enhanced legal principles to Neon database."""
    print("Syncing legal principles...")
    
    # Sample principles data (in production, this would parse the .scm files)
    principles = [
        {
            'name': 'pacta-sunt-servanda',
            'description': 'Agreements must be kept - the foundational principle of contract law',
            'domains': ['contract', 'civil', 'international'],
            'confidence': 1.0,
            'provenance': 'Roman law, universally recognized',
            'inference_level': 1,
            'inference_type': 'deductive',
            'application_context': 'Binding force of contracts between parties'
        },
        {
            'name': 'consensus-ad-idem',
            'description': 'Meeting of the minds - parties must have mutual agreement',
            'domains': ['contract', 'civil'],
            'confidence': 1.0,
            'provenance': 'Roman law, common law',
            'inference_level': 1,
            'inference_type': 'deductive',
            'application_context': 'Formation of valid contracts'
        },
        {
            'name': 'audi-alteram-partem',
            'description': 'Hear the other side - fundamental principle of natural justice',
            'domains': ['procedure', 'administrative', 'constitutional'],
            'confidence': 1.0,
            'provenance': 'Roman law, natural justice',
            'inference_level': 1,
            'inference_type': 'deductive',
            'application_context': 'Fair hearing rights in all proceedings'
        }
    ]
    
    try:
        with conn.cursor() as cur:
            for principle in principles:
                cur.execute("""
                    INSERT INTO lex_principles_enhanced 
                    (name, description, domains, confidence, provenance, 
                     inference_level, inference_type, application_context)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (name) DO UPDATE SET
                        description = EXCLUDED.description,
                        domains = EXCLUDED.domains,
                        confidence = EXCLUDED.confidence,
                        provenance = EXCLUDED.provenance,
                        inference_level = EXCLUDED.inference_level,
                        inference_type = EXCLUDED.inference_type,
                        application_context = EXCLUDED.application_context,
                        updated_at = CURRENT_TIMESTAMP
                """, (
                    principle['name'],
                    principle['description'],
                    principle['domains'],
                    principle['confidence'],
                    principle['provenance'],
                    principle['inference_level'],
                    principle['inference_type'],
                    principle['application_context']
                ))
            
            conn.commit()
            print(f"✓ Synced {len(principles)} legal principles")
            return True
            
    except Exception as e:
        print(f"✗ Error syncing principles: {e}")
        conn.rollback()
        return False


def main():
    """Main synchronization function."""
    print("\n" + "=" * 80)
    print("NEON DATABASE SYNCHRONIZATION")
    print("=" * 80 + "\n")
    
    # Get connection string
    conn_string = get_connection_string()
    
    if not conn_string:
        print("✗ No Neon connection string available")
        print("  Please set NEON_CONNECTION_STRING environment variable")
        print("  or configure NEON_HOST, NEON_DATABASE, NEON_USER, NEON_PASSWORD")
        return 1
    
    try:
        # Connect to database
        print("Connecting to Neon database...")
        conn = psycopg2.connect(conn_string)
        print("✓ Connected successfully\n")
        
        # Create enhanced tables
        if not create_enhanced_tables(conn):
            return 1
        
        print()
        
        # Sync legal principles
        if not sync_legal_principles(conn):
            return 1
        
        print()
        
        # Find latest simulation results
        results_dir = os.path.join(os.path.dirname(__file__), '..', 'simulations', 'results')
        if os.path.exists(results_dir):
            results_files = [f for f in os.listdir(results_dir) if f.endswith('.json')]
            if results_files:
                latest_file = sorted(results_files)[-1]
                results_file = os.path.join(results_dir, latest_file)
                
                if not sync_simulation_results(conn, results_file):
                    return 1
        
        print("\n" + "=" * 80)
        print("SYNCHRONIZATION COMPLETED SUCCESSFULLY")
        print("=" * 80 + "\n")
        
        conn.close()
        return 0
        
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())

