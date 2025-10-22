# Database Synchronization Guide

**Version:** 2.0  
**Date:** October 22, 2025  
**Status:** Ready for Deployment

## Overview

This guide provides instructions for synchronizing the enhanced AnalytiCase legal frameworks and simulation results with Supabase and Neon databases.

## Table of Contents

1. [Database Schema](#database-schema)
2. [Neon Integration](#neon-integration)
3. [Supabase Integration](#supabase-integration)
4. [Synchronization Scripts](#synchronization-scripts)
5. [Manual Deployment](#manual-deployment)
6. [Verification](#verification)
7. [Troubleshooting](#troubleshooting)

---

## Database Schema

### Enhanced Tables

The enhanced schema includes the following tables:

#### Legal Framework Tables

**lex_principles_enhanced**
- Stores enhanced legal principles with structured metadata
- Fields: principle_id, name, description, domains, confidence, provenance, inference_level, inference_type, application_context
- Indexes on: name, domains (GIN), inference_level, confidence, metadata (GIN)

**lex_principle_relationships**
- Stores relationships between legal principles
- Fields: relationship_id, source_principle_id, target_principle_id, relationship_type, strength, description
- Relationship types: related, derives-from, supports, contradicts

**lex_inference_chains**
- Stores inference chains showing how principles derive from each other
- Fields: chain_id, start_principle_id, end_principle_id, intermediate_steps (JSONB), inference_types, confidence_score, chain_length

#### Simulation Tables

**simulation_runs**
- Records simulation executions
- Fields: run_id, run_timestamp, simulation_type, version, configuration (JSONB), status, completed_at, duration_seconds

**simulation_metrics**
- Detailed metrics from simulation runs
- Fields: metric_id, run_id, metric_name, metric_value, metric_type, agent_type, timestamp

**agent_performance**
- Performance tracking for individual agents
- Fields: performance_id, run_id, agent_id, agent_type, agent_name, efficiency, expertise, stress_level, workload, interactions_count, collaborations_count, performance_trend, performance_history (JSONB)

**collaboration_network**
- Network of agent collaborations
- Fields: collaboration_id, run_id, agent_1_id, agent_2_id, interaction_type, outcome, outcome_score, timestamp, context (JSONB)

**case_pipeline**
- Case processing pipeline tracking
- Fields: case_id, run_id, stage, complexity, time_in_system, created_at, updated_at, completed_at

**simulation_insights**
- Generated insights and recommendations from simulations
- Fields: insight_id, run_id, insight_type, severity, status, title, description, recommendation

#### Analytics Views

**v_latest_simulations**
- Shows the 20 most recent simulation runs with key configuration

**v_agent_performance_summary**
- Aggregates agent performance by run and type

**v_collaboration_summary**
- Summarizes collaboration metrics by run

**v_case_processing_summary**
- Summarizes case processing metrics by run

**v_principle_network**
- Shows principle relationships network

### Schema File

The complete schema is available in: `schema/enhanced_legal_principles.sql`

---

## Neon Integration

### Project Information

**Project ID:** sweet-sea-69912135  
**Organization:** zone (org-billowing-mountain-51013486)  
**Region:** Azure East US 2  
**PostgreSQL Version:** 17

### Existing Legal Tables

The Neon database already contains several legal tables:
- lex_ad_mappings
- lex_case_parties
- lex_cases
- lex_citations
- lex_concepts
- lex_courts
- lex_hyperedges
- lex_judges
- lex_nodes
- lex_parties
- lex_principles (original)
- lex_procedures
- lex_sections
- lex_statutes

### Deployment Steps

#### Option 1: Using MCP CLI

```bash
# List available tools
manus-mcp-cli tool list --server neon

# Execute schema deployment
manus-mcp-cli tool call run_sql_transaction --server neon --input '{
  "params": {
    "projectId": "sweet-sea-69912135",
    "sqlStatements": ["<SQL from schema file>"]
  }
}'
```

#### Option 2: Using Python Script

```bash
# Set connection string
export NEON_CONNECTION_STRING="postgresql://user:pass@host/db?sslmode=require"

# Run synchronization
python3 scripts/sync_to_neon_enhanced.py
```

#### Option 3: Manual Deployment

1. Access Neon Console: https://console.neon.tech
2. Select project: sweet-sea-69912135
3. Open SQL Editor
4. Copy contents of `schema/enhanced_legal_principles.sql`
5. Execute SQL statements
6. Verify table creation

### Data Population

After schema deployment, populate with:

1. **Legal Principles**: Parse `lex/lv1/known_laws.scm` and insert principles
2. **Simulation Results**: Load from `simulations/results/simulation_results_*.json`
3. **Agent Performance**: Extract from simulation results
4. **Insights**: Parse insights reports

---

## Supabase Integration

### Configuration

**Environment Variables Required:**
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase API key (service role key for admin operations)

### Deployment Steps

#### Option 1: Using Supabase Dashboard

1. Log in to Supabase Dashboard
2. Navigate to SQL Editor
3. Create new query
4. Paste contents of `schema/enhanced_legal_principles.sql`
5. Execute query
6. Verify table creation in Table Editor

#### Option 2: Using Python Script

```bash
# Set environment variables
export SUPABASE_URL="https://your-project.supabase.co"
export SUPABASE_KEY="your-service-role-key"

# Run synchronization
python3 scripts/sync_to_supabase_enhanced.py
```

#### Option 3: Using Supabase CLI

```bash
# Install Supabase CLI
npm install -g supabase

# Login
supabase login

# Link project
supabase link --project-ref your-project-ref

# Deploy schema
supabase db push

# Or execute SQL file
supabase db execute -f schema/enhanced_legal_principles.sql
```

### Row Level Security (RLS)

After creating tables, configure RLS policies:

```sql
-- Enable RLS on all tables
ALTER TABLE lex_principles_enhanced ENABLE ROW LEVEL SECURITY;
ALTER TABLE simulation_runs ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_performance ENABLE ROW LEVEL SECURITY;
-- ... (repeat for all tables)

-- Create policies (example)
CREATE POLICY "Public read access" ON lex_principles_enhanced
  FOR SELECT USING (true);

CREATE POLICY "Authenticated write access" ON simulation_runs
  FOR INSERT WITH CHECK (auth.role() = 'authenticated');
```

---

## Synchronization Scripts

### Neon Synchronization Script

**Location:** `scripts/sync_to_neon_enhanced.py`

**Features:**
- Creates enhanced tables if they don't exist
- Syncs legal principles from .scm files
- Syncs simulation results from JSON files
- Handles agent performance data
- Manages collaboration networks
- Tracks case pipeline

**Usage:**
```bash
python3 scripts/sync_to_neon_enhanced.py
```

### Supabase Synchronization Script

**Location:** `scripts/sync_to_supabase_enhanced.py`

**Features:**
- Documents required schema
- Syncs legal principles
- Syncs simulation runs and metrics
- Syncs agent performance data
- Generates and syncs insights
- Handles JSONB metadata

**Usage:**
```bash
python3 scripts/sync_to_supabase_enhanced.py
```

### Automated Synchronization

To automate synchronization after each simulation run:

```bash
# Add to simulation runner
cd /home/ubuntu/analyticase
python3 simulations/run_enhanced_simulations.py
python3 scripts/sync_to_neon_enhanced.py
python3 scripts/sync_to_supabase_enhanced.py
```

Or create a combined script:

```bash
#!/bin/bash
# run_and_sync.sh

echo "Running simulations..."
python3 simulations/run_enhanced_simulations.py

echo "Syncing to Neon..."
python3 scripts/sync_to_neon_enhanced.py

echo "Syncing to Supabase..."
python3 scripts/sync_to_supabase_enhanced.py

echo "Complete!"
```

---

## Manual Deployment

### Step-by-Step Manual Deployment

#### 1. Prepare Schema File

```bash
cd /home/ubuntu/analyticase
cat schema/enhanced_legal_principles.sql
```

#### 2. Deploy to Neon

**Via Neon Console:**
1. Go to https://console.neon.tech
2. Select project: sweet-sea-69912135
3. Click "SQL Editor"
4. Paste schema SQL
5. Click "Run"

**Via psql:**
```bash
psql "postgresql://user:pass@host/db?sslmode=require" -f schema/enhanced_legal_principles.sql
```

#### 3. Deploy to Supabase

**Via Supabase Dashboard:**
1. Go to your Supabase project dashboard
2. Navigate to "SQL Editor"
3. Click "New query"
4. Paste schema SQL
5. Click "Run"

**Via Supabase CLI:**
```bash
supabase db execute -f schema/enhanced_legal_principles.sql
```

#### 4. Verify Deployment

**Neon:**
```bash
manus-mcp-cli tool call get_database_tables --server neon --input '{
  "params": {"projectId": "sweet-sea-69912135"}
}'
```

**Supabase:**
- Check Table Editor in dashboard
- Or query via API:
```python
from supabase import create_client
supabase = create_client(url, key)
tables = supabase.table('lex_principles_enhanced').select('*').limit(1).execute()
```

#### 5. Populate Data

Run synchronization scripts or manually insert data:

```sql
-- Example: Insert a legal principle
INSERT INTO lex_principles_enhanced 
(name, description, domains, confidence, provenance, inference_level, inference_type)
VALUES 
('pacta-sunt-servanda', 
 'Agreements must be kept', 
 ARRAY['contract', 'civil'], 
 1.0, 
 'Roman law', 
 1, 
 'deductive');
```

---

## Verification

### Verify Schema Deployment

**Check Tables Exist:**
```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name LIKE 'lex_%' OR table_name LIKE 'simulation_%';
```

**Check Indexes:**
```sql
SELECT indexname, tablename 
FROM pg_indexes 
WHERE schemaname = 'public' 
AND tablename IN ('lex_principles_enhanced', 'simulation_runs', 'agent_performance');
```

**Check Views:**
```sql
SELECT viewname 
FROM pg_views 
WHERE schemaname = 'public' 
AND viewname LIKE 'v_%';
```

### Verify Data Population

**Check Principle Count:**
```sql
SELECT COUNT(*) as principle_count 
FROM lex_principles_enhanced;
```

**Check Latest Simulation:**
```sql
SELECT * FROM v_latest_simulations LIMIT 1;
```

**Check Agent Performance:**
```sql
SELECT agent_type, COUNT(*) as count, AVG(efficiency) as avg_efficiency
FROM agent_performance
GROUP BY agent_type;
```

### Verify Relationships

**Check Principle Relationships:**
```sql
SELECT COUNT(*) as relationship_count 
FROM lex_principle_relationships;
```

**Check Collaboration Network:**
```sql
SELECT COUNT(*) as collaboration_count,
       AVG(outcome_score) as avg_score
FROM collaboration_network;
```

---

## Troubleshooting

### Common Issues

#### Issue: Connection Refused

**Symptom:** `[Errno -2] Name or service not known` or connection timeout

**Solution:**
- Verify environment variables are set correctly
- Check network connectivity
- Ensure database is running and accessible
- Verify firewall rules allow connections

#### Issue: Table Already Exists

**Symptom:** `ERROR: relation "table_name" already exists`

**Solution:**
- Use `CREATE TABLE IF NOT EXISTS` (already in schema)
- Or drop existing tables first (careful with data loss):
```sql
DROP TABLE IF EXISTS table_name CASCADE;
```

#### Issue: Permission Denied

**Symptom:** `ERROR: permission denied for schema public`

**Solution:**
- Ensure user has CREATE privileges
- Grant necessary permissions:
```sql
GRANT CREATE ON SCHEMA public TO your_user;
GRANT ALL ON ALL TABLES IN SCHEMA public TO your_user;
```

#### Issue: Invalid JSON

**Symptom:** `ERROR: invalid input syntax for type json`

**Solution:**
- Validate JSON data before insertion
- Use JSONB validation functions:
```sql
SELECT jsonb_typeof(column_name) FROM table_name;
```

#### Issue: Foreign Key Constraint Violation

**Symptom:** `ERROR: insert or update on table violates foreign key constraint`

**Solution:**
- Ensure referenced records exist first
- Insert in correct order (parent tables before child tables)
- Or temporarily disable constraints:
```sql
SET session_replication_role = replica;
-- Insert data
SET session_replication_role = DEFAULT;
```

### Debug Mode

Enable detailed logging in synchronization scripts:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Manual Data Inspection

**Neon:**
```bash
manus-mcp-cli tool call run_sql --server neon --input '{
  "params": {
    "projectId": "sweet-sea-69912135",
    "sql": "SELECT * FROM lex_principles_enhanced LIMIT 5"
  }
}'
```

**Supabase:**
```python
from supabase import create_client
supabase = create_client(url, key)
result = supabase.table('lex_principles_enhanced').select('*').limit(5).execute()
print(result.data)
```

---

## Next Steps

After successful deployment:

1. **Populate Legal Principles**: Parse all .scm files and insert principles
2. **Run Regular Simulations**: Schedule periodic simulation runs
3. **Automate Synchronization**: Set up automated sync after each simulation
4. **Create Dashboards**: Build analytics dashboards using the views
5. **Set Up Monitoring**: Monitor database performance and query patterns
6. **Implement Backups**: Configure automated backups
7. **Document API**: Create API documentation for accessing the data

---

## References

- Neon Documentation: https://neon.tech/docs
- Supabase Documentation: https://supabase.com/docs
- PostgreSQL Documentation: https://www.postgresql.org/docs/
- AnalytiCase Repository: https://github.com/rzonedevops/analyticase

---

**Document Version:** 2.0  
**Last Updated:** October 22, 2025  
**Maintained By:** AnalytiCase Enhancement Team

