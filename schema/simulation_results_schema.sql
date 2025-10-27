-- Simulation Results Schema for Analyticase
-- This schema supports tracking simulation runs and their results across all model types

-- Simulation Runs Table
CREATE TABLE IF NOT EXISTS simulation_runs (
    id SERIAL PRIMARY KEY,
    run_id VARCHAR(100) UNIQUE NOT NULL,
    model_type VARCHAR(50) NOT NULL CHECK (model_type IN ('agent_based', 'discrete_event', 'system_dynamics', 'hypergnn', 'case_llm')),
    run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    configuration JSONB,
    status VARCHAR(20) DEFAULT 'running' CHECK (status IN ('running', 'completed', 'failed')),
    duration_seconds NUMERIC(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Agent-Based Simulation Results
CREATE TABLE IF NOT EXISTS agent_simulation_results (
    id SERIAL PRIMARY KEY,
    run_id VARCHAR(100) REFERENCES simulation_runs(run_id) ON DELETE CASCADE,
    agent_id VARCHAR(100) NOT NULL,
    agent_type VARCHAR(50) NOT NULL CHECK (agent_type IN ('attorney', 'judge', 'investigator', 'party')),
    reputation_score NUMERIC(5, 4),
    expertise_level NUMERIC(5, 4),
    principle_application_accuracy NUMERIC(5, 4),
    cases_handled INTEGER DEFAULT 0,
    collaborations_count INTEGER DEFAULT 0,
    stress_level NUMERIC(5, 4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Discrete-Event Simulation Results
CREATE TABLE IF NOT EXISTS discrete_event_results (
    id SERIAL PRIMARY KEY,
    run_id VARCHAR(100) REFERENCES simulation_runs(run_id) ON DELETE CASCADE,
    case_id VARCHAR(100) NOT NULL,
    case_type VARCHAR(50),
    case_complexity INTEGER,
    filing_time TIMESTAMP,
    closing_time TIMESTAMP,
    duration_days NUMERIC(10, 2),
    outcome VARCHAR(50),
    settlement_amount NUMERIC(15, 2),
    principles_invoked TEXT[],
    resource_utilization JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- HyperGNN Simulation Results
CREATE TABLE IF NOT EXISTS hypergnn_results (
    id SERIAL PRIMARY KEY,
    run_id VARCHAR(100) REFERENCES simulation_runs(run_id) ON DELETE CASCADE,
    node_id VARCHAR(100) NOT NULL,
    node_type VARCHAR(50) NOT NULL,
    importance_score NUMERIC(10, 8),
    embedding JSONB,
    connected_nodes TEXT[],
    hyperedge_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Legal Principle Application Tracking
CREATE TABLE IF NOT EXISTS principle_applications (
    id SERIAL PRIMARY KEY,
    run_id VARCHAR(100) REFERENCES simulation_runs(run_id) ON DELETE CASCADE,
    principle_id VARCHAR(100) NOT NULL,
    principle_name VARCHAR(200) NOT NULL,
    application_context VARCHAR(50),
    invocation_count INTEGER DEFAULT 0,
    success_rate NUMERIC(5, 4),
    case_types TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Simulation Events Log
CREATE TABLE IF NOT EXISTS simulation_events (
    id SERIAL PRIMARY KEY,
    run_id VARCHAR(100) REFERENCES simulation_runs(run_id) ON DELETE CASCADE,
    event_timestamp TIMESTAMP NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB,
    agents_involved TEXT[],
    principles_invoked TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Performance Metrics
CREATE TABLE IF NOT EXISTS simulation_metrics (
    id SERIAL PRIMARY KEY,
    run_id VARCHAR(100) REFERENCES simulation_runs(run_id) ON DELETE CASCADE,
    metric_name VARCHAR(100) NOT NULL,
    metric_value NUMERIC(15, 4),
    metric_unit VARCHAR(50),
    metric_category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_simulation_runs_model_type ON simulation_runs(model_type);
CREATE INDEX IF NOT EXISTS idx_simulation_runs_timestamp ON simulation_runs(run_timestamp);
CREATE INDEX IF NOT EXISTS idx_agent_results_run_id ON agent_simulation_results(run_id);
CREATE INDEX IF NOT EXISTS idx_agent_results_type ON agent_simulation_results(agent_type);
CREATE INDEX IF NOT EXISTS idx_discrete_event_run_id ON discrete_event_results(run_id);
CREATE INDEX IF NOT EXISTS idx_discrete_event_case_type ON discrete_event_results(case_type);
CREATE INDEX IF NOT EXISTS idx_hypergnn_run_id ON hypergnn_results(run_id);
CREATE INDEX IF NOT EXISTS idx_hypergnn_node_type ON hypergnn_results(node_type);
CREATE INDEX IF NOT EXISTS idx_principle_apps_run_id ON principle_applications(run_id);
CREATE INDEX IF NOT EXISTS idx_principle_apps_principle_id ON principle_applications(principle_id);
CREATE INDEX IF NOT EXISTS idx_simulation_events_run_id ON simulation_events(run_id);
CREATE INDEX IF NOT EXISTS idx_simulation_events_type ON simulation_events(event_type);
CREATE INDEX IF NOT EXISTS idx_simulation_metrics_run_id ON simulation_metrics(run_id);

-- GIN indexes for JSONB columns
CREATE INDEX IF NOT EXISTS idx_simulation_runs_config ON simulation_runs USING GIN (configuration);
CREATE INDEX IF NOT EXISTS idx_discrete_event_resource ON discrete_event_results USING GIN (resource_utilization);
CREATE INDEX IF NOT EXISTS idx_hypergnn_embedding ON hypergnn_results USING GIN (embedding);
CREATE INDEX IF NOT EXISTS idx_simulation_events_data ON simulation_events USING GIN (event_data);

-- Views for common queries

-- Simulation Summary View
CREATE OR REPLACE VIEW simulation_summary AS
SELECT 
    sr.run_id,
    sr.model_type,
    sr.run_timestamp,
    sr.status,
    sr.duration_seconds,
    COUNT(DISTINCT CASE WHEN sr.model_type = 'agent_based' THEN asr.agent_id END) as agent_count,
    COUNT(DISTINCT CASE WHEN sr.model_type = 'discrete_event' THEN der.case_id END) as case_count,
    COUNT(DISTINCT CASE WHEN sr.model_type = 'hypergnn' THEN hr.node_id END) as node_count,
    AVG(CASE WHEN sr.model_type = 'agent_based' THEN asr.reputation_score END) as avg_reputation,
    AVG(CASE WHEN sr.model_type = 'discrete_event' THEN der.duration_days END) as avg_case_duration
FROM simulation_runs sr
LEFT JOIN agent_simulation_results asr ON sr.run_id = asr.run_id
LEFT JOIN discrete_event_results der ON sr.run_id = der.run_id
LEFT JOIN hypergnn_results hr ON sr.run_id = hr.run_id
GROUP BY sr.run_id, sr.model_type, sr.run_timestamp, sr.status, sr.duration_seconds;

-- Principle Usage View
CREATE OR REPLACE VIEW principle_usage_summary AS
SELECT 
    pa.principle_id,
    pa.principle_name,
    COUNT(DISTINCT pa.run_id) as simulation_count,
    SUM(pa.invocation_count) as total_invocations,
    AVG(pa.success_rate) as avg_success_rate,
    ARRAY_AGG(DISTINCT unnest(pa.case_types)) as all_case_types
FROM principle_applications pa
GROUP BY pa.principle_id, pa.principle_name;

-- Agent Performance View
CREATE OR REPLACE VIEW agent_performance_summary AS
SELECT 
    asr.agent_id,
    asr.agent_type,
    COUNT(DISTINCT asr.run_id) as simulation_count,
    AVG(asr.reputation_score) as avg_reputation,
    AVG(asr.expertise_level) as avg_expertise,
    AVG(asr.principle_application_accuracy) as avg_accuracy,
    SUM(asr.cases_handled) as total_cases_handled,
    SUM(asr.collaborations_count) as total_collaborations
FROM agent_simulation_results asr
GROUP BY asr.agent_id, asr.agent_type;

-- Comments
COMMENT ON TABLE simulation_runs IS 'Tracks all simulation runs across different model types';
COMMENT ON TABLE agent_simulation_results IS 'Stores results from agent-based simulations';
COMMENT ON TABLE discrete_event_results IS 'Stores results from discrete-event simulations';
COMMENT ON TABLE hypergnn_results IS 'Stores results from HyperGNN simulations';
COMMENT ON TABLE principle_applications IS 'Tracks legal principle applications across simulations';
COMMENT ON TABLE simulation_events IS 'Logs all events that occur during simulations';
COMMENT ON TABLE simulation_metrics IS 'Stores performance and analytical metrics from simulations';

