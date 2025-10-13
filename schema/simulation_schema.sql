-- ===================================================================
-- AnalytiCase Enhanced Database Schema
-- Simulation Models and Analysis Results
-- ===================================================================

-- Simulation Runs Table
CREATE TABLE IF NOT EXISTS simulation_runs (
    run_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    run_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    simulation_type VARCHAR(50) NOT NULL,
    configuration JSONB,
    status VARCHAR(20) DEFAULT 'completed',
    duration_seconds DECIMAL(10, 2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_simulation_runs_type ON simulation_runs(simulation_type);
CREATE INDEX idx_simulation_runs_timestamp ON simulation_runs(run_timestamp);

-- Agent-Based Simulation Results
CREATE TABLE IF NOT EXISTS agent_simulation_results (
    result_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    run_id UUID REFERENCES simulation_runs(run_id) ON DELETE CASCADE,
    time_steps INTEGER,
    total_agents INTEGER,
    total_workload INTEGER,
    average_efficiency DECIMAL(5, 4),
    total_interactions INTEGER,
    investigators_count INTEGER,
    attorneys_count INTEGER,
    judges_count INTEGER,
    metrics JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_agent_results_run ON agent_simulation_results(run_id);

-- Discrete-Event Simulation Results
CREATE TABLE IF NOT EXISTS discrete_event_results (
    result_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    run_id UUID REFERENCES simulation_runs(run_id) ON DELETE CASCADE,
    simulation_duration DECIMAL(10, 2),
    total_cases INTEGER,
    closed_cases INTEGER,
    average_duration DECIMAL(10, 2),
    closure_rate DECIMAL(5, 2),
    total_events INTEGER,
    hearings_conducted INTEGER,
    rulings_issued INTEGER,
    metrics JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_discrete_event_results_run ON discrete_event_results(run_id);

-- System Dynamics Simulation Results
CREATE TABLE IF NOT EXISTS system_dynamics_results (
    result_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    run_id UUID REFERENCES simulation_runs(run_id) ON DELETE CASCADE,
    simulation_duration DECIMAL(10, 2),
    time_step DECIMAL(5, 2),
    system_efficiency DECIMAL(5, 2),
    average_cycle_time DECIMAL(10, 2),
    total_cases_filed DECIMAL(10, 2),
    total_cases_closed DECIMAL(10, 2),
    average_wip DECIMAL(10, 2),
    final_stocks JSONB,
    metrics JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_system_dynamics_results_run ON system_dynamics_results(run_id);

-- HyperGNN Analysis Results
CREATE TABLE IF NOT EXISTS hypergnn_results (
    result_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    run_id UUID REFERENCES simulation_runs(run_id) ON DELETE CASCADE,
    num_nodes INTEGER,
    num_hyperedges INTEGER,
    num_communities INTEGER,
    avg_node_degree DECIMAL(10, 4),
    max_node_degree INTEGER,
    avg_edge_size DECIMAL(10, 4),
    max_edge_size INTEGER,
    communities JSONB,
    link_predictions JSONB,
    metrics JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_hypergnn_results_run ON hypergnn_results(run_id);

-- Case-LLM Analysis Results
CREATE TABLE IF NOT EXISTS case_llm_results (
    result_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    run_id UUID REFERENCES simulation_runs(run_id) ON DELETE CASCADE,
    case_id VARCHAR(100),
    model_name VARCHAR(50),
    predicted_outcome VARCHAR(50),
    confidence DECIMAL(5, 4),
    evidence_quality DECIMAL(5, 4),
    legal_merit DECIMAL(5, 4),
    precedent_support DECIMAL(5, 4),
    overall_strength DECIMAL(5, 4),
    entities JSONB,
    summary TEXT,
    brief TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_case_llm_results_run ON case_llm_results(run_id);
CREATE INDEX idx_case_llm_results_case ON case_llm_results(case_id);

-- Hypergraph Nodes Table
CREATE TABLE IF NOT EXISTS hypergraph_nodes (
    node_id VARCHAR(100) PRIMARY KEY,
    node_type VARCHAR(50),
    case_id VARCHAR(100),
    attributes JSONB,
    embedding FLOAT8[],
    community_id INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_hypergraph_nodes_type ON hypergraph_nodes(node_type);
CREATE INDEX idx_hypergraph_nodes_case ON hypergraph_nodes(case_id);
CREATE INDEX idx_hypergraph_nodes_community ON hypergraph_nodes(community_id);

-- Hypergraph Edges Table
CREATE TABLE IF NOT EXISTS hypergraph_edges (
    edge_id VARCHAR(100) PRIMARY KEY,
    edge_type VARCHAR(50),
    case_id VARCHAR(100),
    node_ids TEXT[],
    weight DECIMAL(5, 4),
    attributes JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_hypergraph_edges_type ON hypergraph_edges(edge_type);
CREATE INDEX idx_hypergraph_edges_case ON hypergraph_edges(case_id);

-- Case Analysis Metadata
CREATE TABLE IF NOT EXISTS case_analysis_metadata (
    analysis_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id VARCHAR(100) NOT NULL,
    case_number VARCHAR(100),
    analysis_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    analysis_types TEXT[],
    status VARCHAR(20) DEFAULT 'completed',
    summary TEXT,
    insights JSONB,
    recommendations JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_case_analysis_case ON case_analysis_metadata(case_id);
CREATE INDEX idx_case_analysis_timestamp ON case_analysis_metadata(analysis_timestamp);

-- Simulation Insights Table
CREATE TABLE IF NOT EXISTS simulation_insights (
    insight_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    run_id UUID REFERENCES simulation_runs(run_id) ON DELETE CASCADE,
    insight_type VARCHAR(50),
    insight_category VARCHAR(50),
    insight_text TEXT,
    confidence DECIMAL(5, 4),
    supporting_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_simulation_insights_run ON simulation_insights(run_id);
CREATE INDEX idx_simulation_insights_type ON simulation_insights(insight_type);

-- Performance Metrics Table
CREATE TABLE IF NOT EXISTS performance_metrics (
    metric_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(15, 4),
    metric_unit VARCHAR(50),
    measurement_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    context JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_performance_metrics_name ON performance_metrics(metric_name);
CREATE INDEX idx_performance_metrics_timestamp ON performance_metrics(measurement_timestamp);

-- Comments
COMMENT ON TABLE simulation_runs IS 'Stores metadata for each simulation run';
COMMENT ON TABLE agent_simulation_results IS 'Results from agent-based simulations';
COMMENT ON TABLE discrete_event_results IS 'Results from discrete-event simulations';
COMMENT ON TABLE system_dynamics_results IS 'Results from system dynamics simulations';
COMMENT ON TABLE hypergnn_results IS 'Results from HyperGNN analysis';
COMMENT ON TABLE case_llm_results IS 'Results from Case-LLM analysis';
COMMENT ON TABLE hypergraph_nodes IS 'Nodes in the hypergraph representation of cases';
COMMENT ON TABLE hypergraph_edges IS 'Hyperedges connecting multiple nodes';
COMMENT ON TABLE case_analysis_metadata IS 'Metadata for comprehensive case analyses';
COMMENT ON TABLE simulation_insights IS 'Insights extracted from simulation results';
COMMENT ON TABLE performance_metrics IS 'System performance metrics over time';

