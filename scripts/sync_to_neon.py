#!/usr/bin/env python3
import subprocess, json

def run_sql(project_id, sql):
    cmd = ["manus-mcp-cli", "tool", "call", "run_sql", "--server", "neon", "--input", json.dumps({"params": {"projectId": project_id, "sql": sql}})]
    return subprocess.run(cmd, capture_output=True, text=True)

with open('/home/ubuntu/analyticase/schema/simulation_schema.sql') as f:
    statements = [s.strip() for s in f.read().split(';') if s.strip() and not s.strip().startswith('--')]

project_id, success, errors = "sweet-sea-69912135", 0, 0
print(f"Syncing {len(statements)} statements to Neon...")

for i, stmt in enumerate(statements, 1):
    if stmt:
        print(f"[{i}/{len(statements)}]", end=' ')
        result = run_sql(project_id, stmt)
        if result.returncode == 0:
            success += 1
            print("✓")
        else:
            errors += 1
            print(f"✗ {result.stderr[:100]}")

print(f"\nDone: {success} successful, {errors} errors")
