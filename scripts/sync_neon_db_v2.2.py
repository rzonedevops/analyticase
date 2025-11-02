#!/usr/bin/env python3
"""
Neon Database Synchronization Script v2.2

This script synchronizes the enhanced legal frameworks (v2.2) and simulation results
with the Neon database for persistent storage and querying.

Usage:
    python3 scripts/sync_neon_db_v2.2.py

Requirements:
    - Neon MCP server configured
    - Environment variables: NEON_PROJECT_ID, NEON_DATABASE_NAME
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, Any, List


class NeonDBSync:
    """Synchronize AnalytiCase data with Neon database."""
    
    def __init__(self, project_id: str = "coginlex", database_name: str = "neondb"):
        """Initialize the Neon DB synchronization."""
        self.project_id = project_id
        self.database_name = database_name
        self.repo_root = Path("/home/ubuntu/analyticase")
        
    def run_mcp_command(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Run an MCP command and return the result."""
        input_json = json.dumps({"params": params})
        
        cmd = [
            "manus-mcp-cli", "tool", "call", tool_name,
            "--server", "neon",
            "--input", input_json
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error running {tool_name}: {result.stderr}")
            return {}
        
        # Parse the output to extract JSON
        output_lines = result.stdout.strip().split('\n')
        json_start = -1
        for i, line in enumerate(output_lines):
            if line.strip().startswith('{'):
                json_start = i
                break
        
        if json_start >= 0:
            json_str = '\n'.join(output_lines[json_start:])
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                print(f"Failed to parse JSON from {tool_name}")
                return {}
        
        return {}
    
    def create_legal_framework_table(self):
        """Create a table for storing legal framework principles."""
        sql = """
        CREATE TABLE IF NOT EXISTS legal_principles_v2_2 (
            id SERIAL PRIMARY KEY,
            level INTEGER NOT NULL,  -- 2 for meta-principles, 1 for first-order, 0 for jurisdiction-specific
            principle_id VARCHAR(255) NOT NULL UNIQUE,
            name TEXT NOT NULL,
            description TEXT,
            confidence DECIMAL(3, 2),
            influence DECIMAL(3, 2),
            jurisdiction VARCHAR(50),
            legal_domain VARCHAR(50),
            source_file TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_principle_level ON legal_principles_v2_2(level);
        CREATE INDEX IF NOT EXISTS idx_principle_jurisdiction ON legal_principles_v2_2(jurisdiction);
        CREATE INDEX IF NOT EXISTS idx_principle_domain ON legal_principles_v2_2(legal_domain);
        """
        
        result = self.run_mcp_command("run_sql", {
            "project_id": self.project_id,
            "database": self.database_name,
            "sql": sql
        })
        
        print("Created legal_principles_v2_2 table")
        return result
    
    def create_simulation_results_table(self):
        """Create a table for storing simulation results."""
        sql = """
        CREATE TABLE IF NOT EXISTS simulation_results_v2_2 (
            id SERIAL PRIMARY KEY,
            simulation_id VARCHAR(255) NOT NULL,
            model_name VARCHAR(100) NOT NULL,
            model_version VARCHAR(20) NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            status VARCHAR(50) NOT NULL,
            results JSONB,
            metrics JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_simulation_model ON simulation_results_v2_2(model_name);
        CREATE INDEX IF NOT EXISTS idx_simulation_timestamp ON simulation_results_v2_2(timestamp);
        CREATE INDEX IF NOT EXISTS idx_simulation_status ON simulation_results_v2_2(status);
        """
        
        result = self.run_mcp_command("run_sql", {
            "project_id": self.project_id,
            "database": self.database_name,
            "sql": sql
        })
        
        print("Created simulation_results_v2_2 table")
        return result
    
    def insert_meta_principles(self):
        """Insert Level 2 meta-principles into the database."""
        # This is a placeholder - in a full implementation, we would parse the .scm files
        meta_principles = [
            ("natural-law-theory", "Natural Law Theory", 0.95, 0.85),
            ("legal-positivism", "Legal Positivism", 0.95, 0.90),
            ("critical-legal-studies", "Critical Legal Studies", 0.85, 0.75),
            ("feminist-jurisprudence", "Feminist Jurisprudence", 0.85, 0.80),
            ("economic-analysis-law", "Economic Analysis of Law", 0.90, 0.90),
            ("ubuntu-jurisprudence", "Ubuntu Jurisprudence", 0.85, 0.85),
        ]
        
        for principle_id, name, confidence, influence in meta_principles:
            sql = f"""
            INSERT INTO legal_principles_v2_2 
            (level, principle_id, name, confidence, influence, source_file)
            VALUES (2, '{principle_id}', '{name}', {confidence}, {influence}, 
                    'lex/lv2/legal_foundations_v2.2.scm')
            ON CONFLICT (principle_id) DO UPDATE SET
                name = EXCLUDED.name,
                confidence = EXCLUDED.confidence,
                influence = EXCLUDED.influence,
                updated_at = CURRENT_TIMESTAMP;
            """
            
            self.run_mcp_command("run_sql", {
                "project_id": self.project_id,
                "database": self.database_name,
                "sql": sql
            })
        
        print(f"Inserted {len(meta_principles)} meta-principles")
    
    def insert_simulation_result(self, simulation_data: Dict[str, Any]):
        """Insert a simulation result into the database."""
        sql = f"""
        INSERT INTO simulation_results_v2_2 
        (simulation_id, model_name, model_version, timestamp, status, results, metrics)
        VALUES (
            '{simulation_data['simulation_id']}',
            '{simulation_data['model_name']}',
            '{simulation_data['model_version']}',
            '{simulation_data['timestamp']}',
            '{simulation_data['status']}',
            '{json.dumps(simulation_data.get('results', {}))}'::jsonb,
            '{json.dumps(simulation_data.get('metrics', {}))}'::jsonb
        );
        """
        
        result = self.run_mcp_command("run_sql", {
            "project_id": self.project_id,
            "database": self.database_name,
            "sql": sql
        })
        
        print(f"Inserted simulation result: {simulation_data['model_name']}")
        return result
    
    def sync_all(self):
        """Synchronize all data with Neon database."""
        print("=" * 80)
        print("Neon Database Synchronization v2.2")
        print("=" * 80)
        
        # Create tables
        print("\n1. Creating database tables...")
        self.create_legal_framework_table()
        self.create_simulation_results_table()
        
        # Insert legal principles
        print("\n2. Inserting legal principles...")
        self.insert_meta_principles()
        
        # Insert simulation results (if available)
        print("\n3. Checking for simulation results...")
        results_dir = self.repo_root / "simulation_results"
        if results_dir.exists():
            for result_file in results_dir.glob("*_v2.2_*.json"):
                try:
                    with open(result_file, 'r') as f:
                        data = json.load(f)
                        # Extract simulation metadata
                        simulation_data = {
                            'simulation_id': result_file.stem,
                            'model_name': result_file.stem.split('_')[0],
                            'model_version': '2.2',
                            'timestamp': data.get('timestamp', '2025-11-02T00:00:00'),
                            'status': 'success',
                            'results': data,
                            'metrics': data.get('metrics', {})
                        }
                        self.insert_simulation_result(simulation_data)
                except Exception as e:
                    print(f"Error processing {result_file}: {e}")
        
        print("\n" + "=" * 80)
        print("Synchronization complete!")
        print("=" * 80)


def main():
    """Main entry point."""
    sync = NeonDBSync(project_id="small-wave-37487125", database_name="neondb")
    sync.sync_all()


if __name__ == "__main__":
    main()
