#!/usr/bin/env python3
"""
Deploy Lex Scheme schema to Neon database using run_sql_transaction
"""

import subprocess
import json
import sys

PROJECT_ID = "sweet-sea-69912135"
DATABASE_NAME = "neondb"
SCHEMA_FILE = "schema/lex_scheme_enhanced.sql"

def read_schema_file():
    """Read and return the schema file content."""
    try:
        with open(SCHEMA_FILE, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Schema file not found: {SCHEMA_FILE}")
        sys.exit(1)

def split_sql_statements(sql_content):
    """Split SQL content into individual statements."""
    # Simple split by semicolon (not perfect but works for most cases)
    statements = []
    current = []
    
    for line in sql_content.split('\n'):
        # Skip comments and empty lines
        line = line.strip()
        if not line or line.startswith('--'):
            continue
        
        current.append(line)
        
        if line.endswith(';'):
            statements.append(' '.join(current))
            current = []
    
    return [s for s in statements if s.strip()]

def deploy_schema():
    """Deploy schema to Neon database."""
    print(f"Reading schema from {SCHEMA_FILE}...")
    schema_content = read_schema_file()
    
    print(f"Splitting SQL statements...")
    statements = split_sql_statements(schema_content)
    print(f"Found {len(statements)} SQL statements")
    
    # Group statements into batches (Neon has limits)
    batch_size = 20
    batches = [statements[i:i+batch_size] for i in range(0, len(statements), batch_size)]
    
    print(f"\nDeploying in {len(batches)} batches...")
    
    for i, batch in enumerate(batches, 1):
        print(f"\nBatch {i}/{len(batches)} ({len(batch)} statements)...")
        
        # Prepare input for MCP CLI
        input_data = {
            "params": {
                "projectId": PROJECT_ID,
                "databaseName": DATABASE_NAME,
                "sqlStatements": batch
            }
        }
        
        # Call MCP CLI
        try:
            result = subprocess.run(
                [
                    'manus-mcp-cli', 'tool', 'call', 'run_sql_transaction',
                    '--server', 'neon',
                    '--input', json.dumps(input_data)
                ],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print(f"✓ Batch {i} deployed successfully")
            else:
                print(f"✗ Batch {i} failed:")
                print(result.stderr)
                
        except subprocess.TimeoutExpired:
            print(f"✗ Batch {i} timed out")
        except Exception as e:
            print(f"✗ Batch {i} error: {e}")
    
    print("\nDeployment completed!")

if __name__ == "__main__":
    deploy_schema()
