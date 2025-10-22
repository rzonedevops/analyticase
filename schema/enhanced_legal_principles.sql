-- Enhanced Legal Principles Schema for Neon Database
-- Version: 2.0
-- Date: 2025-10-22
-- Description: Schema for storing enhanced legal principles with metadata, inference chains, and relationships

-- ============================================================================
-- LEGAL PRINCIPLES TABLE (Enhanced)
-- ============================================================================

-- Drop existing table if needed (commented out for safety)
-- DROP TABLE IF EXISTS public.lex_principles CASCADE;

-- Create enhanced principles table
CREATE TABLE IF NOT EXISTS public.lex_principles_enhanced (
    principle_id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT NOT NULL,
    domains TEXT[] NOT NULL,  -- Array of legal domains (contract, civil, criminal, etc.)
    confidence DECIMAL(3,2) NOT NULL DEFAULT 1.0 CHECK (confidence >= 0 AND confidence <= 1),
    provenance TEXT,  -- Historical/jurisdictional origin
    inference_level INTEGER NOT NULL DEFAULT 1,  -- 1 = first-order, 2+ = derived
    inference_type VARCHAR(50),  -- deductive, inductive, abductive, analogical
    application_context TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB  -- Additional flexible metadata
);

-- Create indexes for efficient querying
CREATE INDEX IF NOT EXISTS idx_principles_name ON public.lex_principles_enhanced(name);
CREATE INDEX IF NOT EXISTS idx_principles_domains ON public.lex_principles_enhanced USING GIN(domains);
CREATE INDEX IF NOT EXISTS idx_principles_inference_level ON public.lex_principles_enhanced(inference_level);
CREATE INDEX IF NOT EXISTS idx_principles_confidence ON public.lex_principles_enhanced(confidence);
CREATE INDEX IF NOT EXISTS idx_principles_metadata ON public.lex_principles_enhanced USING GIN(metadata);

-- ============================================================================
-- PRINCIPLE RELATIONSHIPS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS public.lex_principle_relationships (
    relationship_id SERIAL PRIMARY KEY,
    source_principle_id INTEGER NOT NULL REFERENCES public.lex_principles_enhanced(principle_id) ON DELETE CASCADE,
    target_principle_id INTEGER NOT NULL REFERENCES public.lex_principles_enhanced(principle_id) ON DELETE CASCADE,
    relationship_type VARCHAR(50) NOT NULL,  -- related, derives-from, supports, contradicts
    strength DECIMAL(3,2) DEFAULT 0.5 CHECK (strength >= 0 AND strength <= 1),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source_principle_id, target_principle_id, relationship_type)
);

CREATE INDEX IF NOT EXISTS idx_rel_source ON public.lex_principle_relationships(source_principle_id);
CREATE INDEX IF NOT EXISTS idx_rel_target ON public.lex_principle_relationships(target_principle_id);
CREATE INDEX IF NOT EXISTS idx_rel_type ON public.lex_principle_relationships(relationship_type);

-- ============================================================================
-- INFERENCE CHAINS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS public.lex_inference_chains (
    chain_id SERIAL PRIMARY KEY,
    start_principle_id INTEGER NOT NULL REFERENCES public.lex_principles_enhanced(principle_id) ON DELETE CASCADE,
    end_principle_id INTEGER NOT NULL REFERENCES public.lex_principles_enhanced(principle_id) ON DELETE CASCADE,
    intermediate_steps JSONB,  -- Array of principle IDs in the chain
    inference_types TEXT[],  -- Types of inference at each step
    confidence_score DECIMAL(3,2) CHECK (confidence_score >= 0 AND confidence_score <= 1),
    chain_length INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

CREATE INDEX IF NOT EXISTS idx_chain_start ON public.lex_inference_chains(start_principle_id);
CREATE INDEX IF NOT EXISTS idx_chain_end ON public.lex_inference_chains(end_principle_id);
CREATE INDEX IF NOT EXISTS idx_chain_confidence ON public.lex_inference_chains(confidence_score);

-- ============================================================================
-- SIMULATION RUNS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS public.simulation_runs (
    run_id SERIAL PRIMARY KEY,
    run_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    simulation_type VARCHAR(50) NOT NULL,  -- agent_based, discrete_event, etc.
    version VARCHAR(20) NOT NULL,
    configuration JSONB NOT NULL,
    status VARCHAR(20) DEFAULT 'running',  -- running, completed, failed
    completed_at TIMESTAMP,
    duration_seconds INTEGER,
    metadata JSONB
);

CREATE INDEX IF NOT EXISTS idx_sim_timestamp ON public.simulation_runs(run_timestamp);
CREATE INDEX IF NOT EXISTS idx_sim_type ON public.simulation_runs(simulation_type);
CREATE INDEX IF NOT EXISTS idx_sim_status ON public.simulation_runs(status);

-- ============================================================================
-- SIMULATION METRICS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS public.simulation_metrics (
    metric_id SERIAL PRIMARY KEY,
    run_id INTEGER NOT NULL REFERENCES public.simulation_runs(run_id) ON DELETE CASCADE,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(10,4),
    metric_type VARCHAR(50),  -- efficiency, completion_rate, collaboration, etc.
    agent_type VARCHAR(50),  -- investigator, attorney, judge, etc.
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

CREATE INDEX IF NOT EXISTS idx_metrics_run ON public.simulation_metrics(run_id);
CREATE INDEX IF NOT EXISTS idx_metrics_name ON public.simulation_metrics(metric_name);
CREATE INDEX IF NOT EXISTS idx_metrics_type ON public.simulation_metrics(metric_type);
CREATE INDEX IF NOT EXISTS idx_metrics_agent ON public.simulation_metrics(agent_type);

-- ============================================================================
-- AGENT PERFORMANCE TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS public.agent_performance (
    performance_id SERIAL PRIMARY KEY,
    run_id INTEGER NOT NULL REFERENCES public.simulation_runs(run_id) ON DELETE CASCADE,
    agent_id VARCHAR(50) NOT NULL,
    agent_type VARCHAR(50) NOT NULL,
    agent_name VARCHAR(100),
    efficiency DECIMAL(5,4),
    expertise DECIMAL(5,4),
    stress_level DECIMAL(5,4),
    workload INTEGER,
    interactions_count INTEGER,
    collaborations_count INTEGER,
    performance_trend VARCHAR(20),  -- improving, stable, declining
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    performance_history JSONB,  -- Array of historical performance scores
    metadata JSONB
);

CREATE INDEX IF NOT EXISTS idx_perf_run ON public.agent_performance(run_id);
CREATE INDEX IF NOT EXISTS idx_perf_agent_id ON public.agent_performance(agent_id);
CREATE INDEX IF NOT EXISTS idx_perf_agent_type ON public.agent_performance(agent_type);
CREATE INDEX IF NOT EXISTS idx_perf_efficiency ON public.agent_performance(efficiency);

-- ============================================================================
-- COLLABORATION NETWORK TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS public.collaboration_network (
    collaboration_id SERIAL PRIMARY KEY,
    run_id INTEGER NOT NULL REFERENCES public.simulation_runs(run_id) ON DELETE CASCADE,
    agent_1_id VARCHAR(50) NOT NULL,
    agent_2_id VARCHAR(50) NOT NULL,
    interaction_type VARCHAR(50),
    outcome VARCHAR(20),  -- success, pending, failed
    outcome_score DECIMAL(3,2),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    context JSONB
);

CREATE INDEX IF NOT EXISTS idx_collab_run ON public.collaboration_network(run_id);
CREATE INDEX IF NOT EXISTS idx_collab_agent1 ON public.collaboration_network(agent_1_id);
CREATE INDEX IF NOT EXISTS idx_collab_agent2 ON public.collaboration_network(agent_2_id);
CREATE INDEX IF NOT EXISTS idx_collab_outcome ON public.collaboration_network(outcome);

-- ============================================================================
-- CASE PIPELINE TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS public.case_pipeline (
    case_id VARCHAR(50) PRIMARY KEY,
    run_id INTEGER NOT NULL REFERENCES public.simulation_runs(run_id) ON DELETE CASCADE,
    stage VARCHAR(50) NOT NULL,  -- investigation, litigation, adjudication, completed
    complexity INTEGER,
    time_in_system INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    metadata JSONB
);

CREATE INDEX IF NOT EXISTS idx_case_run ON public.case_pipeline(run_id);
CREATE INDEX IF NOT EXISTS idx_case_stage ON public.case_pipeline(stage);
CREATE INDEX IF NOT EXISTS idx_case_complexity ON public.case_pipeline(complexity);

-- ============================================================================
-- INSIGHTS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS public.simulation_insights (
    insight_id SERIAL PRIMARY KEY,
    run_id INTEGER NOT NULL REFERENCES public.simulation_runs(run_id) ON DELETE CASCADE,
    insight_type VARCHAR(50) NOT NULL,  -- efficiency, collaboration, performance, etc.
    severity VARCHAR(20),  -- high, moderate, low
    status VARCHAR(20),  -- positive, warning, negative
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    recommendation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

CREATE INDEX IF NOT EXISTS idx_insights_run ON public.simulation_insights(run_id);
CREATE INDEX IF NOT EXISTS idx_insights_type ON public.simulation_insights(insight_type);
CREATE INDEX IF NOT EXISTS idx_insights_severity ON public.simulation_insights(severity);

-- ============================================================================
-- VIEWS FOR ANALYTICS
-- ============================================================================

-- View: Latest simulation runs
CREATE OR REPLACE VIEW public.v_latest_simulations AS
SELECT 
    run_id,
    run_timestamp,
    simulation_type,
    version,
    status,
    duration_seconds,
    configuration->>'num_steps' as num_steps,
    configuration->>'num_investigators' as num_investigators,
    configuration->>'num_attorneys' as num_attorneys,
    configuration->>'num_judges' as num_judges
FROM public.simulation_runs
ORDER BY run_timestamp DESC
LIMIT 20;

-- View: Agent performance summary
CREATE OR REPLACE VIEW public.v_agent_performance_summary AS
SELECT 
    run_id,
    agent_type,
    COUNT(*) as agent_count,
    AVG(efficiency) as avg_efficiency,
    AVG(expertise) as avg_expertise,
    AVG(stress_level) as avg_stress,
    AVG(collaborations_count) as avg_collaborations,
    COUNT(CASE WHEN performance_trend = 'improving' THEN 1 END) as improving_count,
    COUNT(CASE WHEN performance_trend = 'stable' THEN 1 END) as stable_count,
    COUNT(CASE WHEN performance_trend = 'declining' THEN 1 END) as declining_count
FROM public.agent_performance
GROUP BY run_id, agent_type;

-- View: Collaboration network summary
CREATE OR REPLACE VIEW public.v_collaboration_summary AS
SELECT 
    run_id,
    COUNT(*) as total_collaborations,
    AVG(outcome_score) as avg_outcome_score,
    COUNT(CASE WHEN outcome = 'success' THEN 1 END) as successful_collaborations,
    COUNT(CASE WHEN outcome = 'pending' THEN 1 END) as pending_collaborations,
    COUNT(CASE WHEN outcome = 'failed' THEN 1 END) as failed_collaborations
FROM public.collaboration_network
GROUP BY run_id;

-- View: Case processing summary
CREATE OR REPLACE VIEW public.v_case_processing_summary AS
SELECT 
    run_id,
    COUNT(*) as total_cases,
    COUNT(CASE WHEN stage = 'completed' THEN 1 END) as completed_cases,
    COUNT(CASE WHEN stage = 'investigation' THEN 1 END) as cases_in_investigation,
    COUNT(CASE WHEN stage = 'litigation' THEN 1 END) as cases_in_litigation,
    COUNT(CASE WHEN stage = 'adjudication' THEN 1 END) as cases_in_adjudication,
    AVG(time_in_system) as avg_time_in_system,
    AVG(complexity) as avg_complexity
FROM public.case_pipeline
GROUP BY run_id;

-- View: Principle relationships network
CREATE OR REPLACE VIEW public.v_principle_network AS
SELECT 
    p1.name as source_principle,
    p2.name as target_principle,
    r.relationship_type,
    r.strength,
    p1.domains as source_domains,
    p2.domains as target_domains
FROM public.lex_principle_relationships r
JOIN public.lex_principles_enhanced p1 ON r.source_principle_id = p1.principle_id
JOIN public.lex_principles_enhanced p2 ON r.target_principle_id = p2.principle_id;

-- ============================================================================
-- FUNCTIONS
-- ============================================================================

-- Function: Get related principles
CREATE OR REPLACE FUNCTION public.get_related_principles(p_principle_name VARCHAR)
RETURNS TABLE (
    related_principle VARCHAR,
    relationship_type VARCHAR,
    strength DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p2.name,
        r.relationship_type,
        r.strength
    FROM public.lex_principle_relationships r
    JOIN public.lex_principles_enhanced p1 ON r.source_principle_id = p1.principle_id
    JOIN public.lex_principles_enhanced p2 ON r.target_principle_id = p2.principle_id
    WHERE p1.name = p_principle_name
    ORDER BY r.strength DESC;
END;
$$ LANGUAGE plpgsql;

-- Function: Calculate simulation performance score
CREATE OR REPLACE FUNCTION public.calculate_performance_score(p_run_id INTEGER)
RETURNS DECIMAL AS $$
DECLARE
    v_efficiency DECIMAL;
    v_completion_rate DECIMAL;
    v_collaboration_score DECIMAL;
    v_performance_score DECIMAL;
BEGIN
    -- Get average efficiency
    SELECT AVG(efficiency) INTO v_efficiency
    FROM public.agent_performance
    WHERE run_id = p_run_id;
    
    -- Get case completion rate
    SELECT 
        CAST(COUNT(CASE WHEN stage = 'completed' THEN 1 END) AS DECIMAL) / 
        NULLIF(COUNT(*), 0)
    INTO v_completion_rate
    FROM public.case_pipeline
    WHERE run_id = p_run_id;
    
    -- Get collaboration success rate
    SELECT AVG(outcome_score) INTO v_collaboration_score
    FROM public.collaboration_network
    WHERE run_id = p_run_id;
    
    -- Calculate weighted performance score
    v_performance_score := (
        COALESCE(v_efficiency, 0) * 0.4 +
        COALESCE(v_completion_rate, 0) * 0.4 +
        COALESCE(v_collaboration_score, 0) * 0.2
    );
    
    RETURN v_performance_score;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- COMMENTS
-- ============================================================================

COMMENT ON TABLE public.lex_principles_enhanced IS 'Enhanced legal principles with structured metadata and inference tracking';
COMMENT ON TABLE public.lex_principle_relationships IS 'Relationships between legal principles';
COMMENT ON TABLE public.lex_inference_chains IS 'Inference chains showing how principles derive from each other';
COMMENT ON TABLE public.simulation_runs IS 'Record of simulation executions';
COMMENT ON TABLE public.simulation_metrics IS 'Detailed metrics from simulation runs';
COMMENT ON TABLE public.agent_performance IS 'Performance tracking for individual agents';
COMMENT ON TABLE public.collaboration_network IS 'Network of agent collaborations';
COMMENT ON TABLE public.case_pipeline IS 'Case processing pipeline tracking';
COMMENT ON TABLE public.simulation_insights IS 'Generated insights and recommendations from simulations';

-- ============================================================================
-- GRANTS (Adjust as needed for your security model)
-- ============================================================================

-- Grant appropriate permissions
-- GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO your_app_user;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO your_app_user;

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================

