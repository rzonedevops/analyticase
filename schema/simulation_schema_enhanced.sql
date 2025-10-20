-- ===================================================================
-- AnalytiCase Enhanced Database Schema - Version 2.0
-- Simulation Models and Analysis Results
-- Enhanced with new features and optimizations
-- ===================================================================

-- Simulation Runs Table (Enhanced)
CREATE TABLE IF NOT EXISTS simulation_runs (
    run_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    run_name VARCHAR(200),
    run_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    simulation_type VARCHAR(50) NOT NULL,
    configuration JSONB,
    status VARCHAR(20) DEFAULT 'completed',
    duration_seconds DECIMAL(10, 2),
    success_count INTEGER DEFAULT 0,
    failure_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_simulation_runs_type ON simulation_runs(simulation_type);
CREATE INDEX IF NOT EXISTS idx_simulation_runs_timestamp ON simulation_runs(run_timestamp);
CREATE INDEX IF NOT EXISTS idx_simulation_runs_name ON simulation_runs(run_name);

-- Agent-Based Simulation Results (Enhanced)
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
    evidence_collected INTEGER DEFAULT 0,
    briefs_filed INTEGER DEFAULT 0,
    cases_won INTEGER DEFAULT 0,
    cases_lost INTEGER DEFAULT 0,
    rulings_made INTEGER DEFAULT 0,
    metrics JSONB,
    agent_summary JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_agent_results_run ON agent_simulation_results(run_id);

-- Discrete-Event Simulation Results (Enhanced)
CREATE TABLE IF NOT EXISTS discrete_event_results (
    result_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    run_id UUID REFERENCES simulation_runs(run_id) ON DELETE CASCADE,
    simulation_duration DECIMAL(10, 2),
    final_time DECIMAL(10, 2),
    total_cases INTEGER,
    closed_cases INTEGER,
    average_duration DECIMAL(10, 2),
    closure_rate DECIMAL(5, 2),
    total_events INTEGER,
    hearings_conducted INTEGER,
    rulings_issued INTEGER,
    evidence_submitted INTEGER,
    average_evidence_items DECIMAL(5, 2),
    stage_distribution JSONB,
    metrics JSONB,
    sample_cases JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_discrete_event_results_run ON discrete_event_results(run_id);

-- System Dynamics Simulation Results (Enhanced)
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
    filed_cases_final DECIMAL(10, 2),
    discovery_cases_final DECIMAL(10, 2),
    pretrial_cases_final DECIMAL(10, 2),
    trial_cases_final DECIMAL(10, 2),
    ruling_cases_final DECIMAL(10, 2),
    closed_cases_final DECIMAL(10, 2),
    final_stocks JSONB,
    average_stocks JSONB,
    metrics JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_system_dynamics_results_run ON system_dynamics_results(run_id);

-- HyperGNN Analysis Results (Enhanced)
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
    node_type_distribution JSONB,
    communities JSONB,
    link_predictions JSONB,
    centrality_scores JSONB,
    attention_weights JSONB,
    metrics JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_hypergnn_results_run ON hypergnn_results(run_id);

-- Case-LLM Analysis Results (Enhanced)
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
    case_rating VARCHAR(20),
    entities JSONB,
    summary TEXT,
    brief TEXT,
    recommendations JSONB,
    rag_documents_used INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_case_llm_results_run ON case_llm_results(run_id);
CREATE INDEX IF NOT EXISTS idx_case_llm_results_case ON case_llm_results(case_id);
CREATE INDEX IF NOT EXISTS idx_case_llm_results_outcome ON case_llm_results(predicted_outcome);

-- Hypergraph Nodes Table (Enhanced)
CREATE TABLE IF NOT EXISTS hypergraph_nodes (
    node_id VARCHAR(100) PRIMARY KEY,
    node_type VARCHAR(50),
    case_id VARCHAR(100),
    run_id UUID REFERENCES simulation_runs(run_id) ON DELETE CASCADE,
    attributes JSONB,
    embedding FLOAT8[],
    centrality_score DECIMAL(10, 6),
    community_id INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_hypergraph_nodes_type ON hypergraph_nodes(node_type);
CREATE INDEX IF NOT EXISTS idx_hypergraph_nodes_case ON hypergraph_nodes(case_id);
CREATE INDEX IF NOT EXISTS idx_hypergraph_nodes_community ON hypergraph_nodes(community_id);
CREATE INDEX IF NOT EXISTS idx_hypergraph_nodes_run ON hypergraph_nodes(run_id);

-- Hypergraph Edges Table (Enhanced)
CREATE TABLE IF NOT EXISTS hypergraph_edges (
    edge_id VARCHAR(100) PRIMARY KEY,
    edge_type VARCHAR(50),
    case_id VARCHAR(100),
    run_id UUID REFERENCES simulation_runs(run_id) ON DELETE CASCADE,
    node_ids TEXT[],
    weight DECIMAL(5, 4),
    attention_weight DECIMAL(5, 4),
    attributes JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_hypergraph_edges_type ON hypergraph_edges(edge_type);
CREATE INDEX IF NOT EXISTS idx_hypergraph_edges_case ON hypergraph_edges(case_id);
CREATE INDEX IF NOT EXISTS idx_hypergraph_edges_run ON hypergraph_edges(run_id);

-- Case Analysis Metadata (Enhanced)
CREATE TABLE IF NOT EXISTS case_analysis_metadata (
    analysis_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id VARCHAR(100) NOT NULL,
    case_number VARCHAR(100),
    run_id UUID REFERENCES simulation_runs(run_id) ON DELETE CASCADE,
    analysis_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    analysis_types TEXT[],
    status VARCHAR(20) DEFAULT 'completed',
    summary TEXT,
    insights JSONB,
    recommendations JSONB,
    confidence_score DECIMAL(5, 4),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_case_analysis_case ON case_analysis_metadata(case_id);
CREATE INDEX IF NOT EXISTS idx_case_analysis_timestamp ON case_analysis_metadata(analysis_timestamp);
CREATE INDEX IF NOT EXISTS idx_case_analysis_run ON case_analysis_metadata(run_id);

-- Simulation Insights Table (Enhanced)
CREATE TABLE IF NOT EXISTS simulation_insights (
    insight_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    run_id UUID REFERENCES simulation_runs(run_id) ON DELETE CASCADE,
    insight_type VARCHAR(50),
    insight_category VARCHAR(50),
    insight_text TEXT,
    confidence DECIMAL(5, 4),
    supporting_data JSONB,
    model_source VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_simulation_insights_run ON simulation_insights(run_id);
CREATE INDEX IF NOT EXISTS idx_simulation_insights_type ON simulation_insights(insight_type);
CREATE INDEX IF NOT EXISTS idx_simulation_insights_category ON simulation_insights(insight_category);

-- Performance Metrics Table (Enhanced)
CREATE TABLE IF NOT EXISTS performance_metrics (
    metric_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    run_id UUID REFERENCES simulation_runs(run_id) ON DELETE CASCADE,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(15, 4),
    metric_unit VARCHAR(50),
    measurement_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    context JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_performance_metrics_name ON performance_metrics(metric_name);
CREATE INDEX IF NOT EXISTS idx_performance_metrics_timestamp ON performance_metrics(measurement_timestamp);
CREATE INDEX IF NOT EXISTS idx_performance_metrics_run ON performance_metrics(run_id);

-- Model Enhancements Table (New)
CREATE TABLE IF NOT EXISTS model_enhancements (
    enhancement_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    model_name VARCHAR(50) NOT NULL,
    enhancement_type VARCHAR(100),
    description TEXT,
    implementation_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    version VARCHAR(20),
    performance_impact JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_model_enhancements_model ON model_enhancements(model_name);
CREATE INDEX IF NOT EXISTS idx_model_enhancements_type ON model_enhancements(enhancement_type);

-- Comments
COMMENT ON TABLE simulation_runs IS 'Stores metadata for each simulation run with enhanced tracking';
COMMENT ON TABLE agent_simulation_results IS 'Results from agent-based simulations with detailed metrics';
COMMENT ON TABLE discrete_event_results IS 'Results from discrete-event simulations with stage tracking';
COMMENT ON TABLE system_dynamics_results IS 'Results from system dynamics simulations with stock levels';
COMMENT ON TABLE hypergnn_results IS 'Results from HyperGNN analysis with attention mechanisms';
COMMENT ON TABLE case_llm_results IS 'Results from Case-LLM analysis with RAG support';
COMMENT ON TABLE hypergraph_nodes IS 'Nodes in the hypergraph representation with centrality scores';
COMMENT ON TABLE hypergraph_edges IS 'Hyperedges with attention weights';
COMMENT ON TABLE case_analysis_metadata IS 'Metadata for comprehensive case analyses';
COMMENT ON TABLE simulation_insights IS 'Insights extracted from simulation results';
COMMENT ON TABLE performance_metrics IS 'System performance metrics over time';
COMMENT ON TABLE model_enhancements IS 'Track model improvements and enhancements';

-- Insert initial model enhancements
INSERT INTO model_enhancements (model_name, enhancement_type, description, version, performance_impact)
VALUES 
    ('HyperGNN', 'Attention Mechanism', 'Advanced attention-based aggregation for hyperedge representation using learnable query vectors', '2.0', '{"accuracy_improvement": "15%", "computational_overhead": "minimal"}'),
    ('Case-LLM', 'RAG Implementation', 'Retrieval-Augmented Generation for context-aware legal analysis with document store', '2.0', '{"context_relevance": "high", "analysis_quality": "improved"}'),
    ('Database', 'Schema Enhancement', 'Enhanced database schema with additional tracking fields and indexes', '2.0', '{"query_performance": "optimized", "data_richness": "enhanced"}')
ON CONFLICT DO NOTHING;

