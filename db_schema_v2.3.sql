-- AnalytiCase Legal Framework v2.3 Database Schema
-- Created: 2025-11-03
-- Database: Neon PostgreSQL

-- ============================================================================
-- META-PRINCIPLES TABLE (Level 2 - Jurisprudential Theories)
-- ============================================================================

CREATE TABLE IF NOT EXISTS meta_principles (
    id SERIAL PRIMARY KEY,
    principle_id VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    historical_origin TEXT,
    contemporary_relevance TEXT,
    influence_score DECIMAL(3,2) CHECK (influence_score >= 0 AND influence_score <= 1),
    jurisdictional_adoption JSONB,
    case_law_applications JSONB,
    cross_references TEXT[],
    temporal_evolution JSONB,
    version VARCHAR(10) DEFAULT '2.3',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for fast lookups
CREATE INDEX idx_meta_principles_id ON meta_principles(principle_id);
CREATE INDEX idx_meta_principles_version ON meta_principles(version);
CREATE INDEX idx_meta_principles_influence ON meta_principles(influence_score DESC);

-- ============================================================================
-- FIRST-ORDER PRINCIPLES TABLE (Level 1 - Fundamental Legal Maxims)
-- ============================================================================

CREATE TABLE IF NOT EXISTS first_order_principles (
    id SERIAL PRIMARY KEY,
    principle_id VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    latin_maxim VARCHAR(255),
    english_translation TEXT,
    description TEXT NOT NULL,
    legal_domain VARCHAR(100),
    derivation_chain TEXT[],
    applicability_scores JSONB,
    case_law_references JSONB,
    cross_references TEXT[],
    conflict_priority INTEGER,
    temporal_evolution JSONB,
    version VARCHAR(10) DEFAULT '2.3',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for fast lookups
CREATE INDEX idx_first_order_principles_id ON first_order_principles(principle_id);
CREATE INDEX idx_first_order_principles_domain ON first_order_principles(legal_domain);
CREATE INDEX idx_first_order_principles_version ON first_order_principles(version);
CREATE INDEX idx_first_order_principles_priority ON first_order_principles(conflict_priority DESC);

-- ============================================================================
-- PRINCIPLE RELATIONSHIPS TABLE (Hypergraph Edges)
-- ============================================================================

CREATE TABLE IF NOT EXISTS principle_relationships (
    id SERIAL PRIMARY KEY,
    relationship_type VARCHAR(50) NOT NULL,
    source_principle_id VARCHAR(100) NOT NULL,
    target_principle_id VARCHAR(100) NOT NULL,
    relationship_strength DECIMAL(3,2) CHECK (relationship_strength >= 0 AND relationship_strength <= 1),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for relationship queries
CREATE INDEX idx_relationships_source ON principle_relationships(source_principle_id);
CREATE INDEX idx_relationships_target ON principle_relationships(target_principle_id);
CREATE INDEX idx_relationships_type ON principle_relationships(relationship_type);

-- ============================================================================
-- HYPEREDGES TABLE (Multi-way Relationships)
-- ============================================================================

CREATE TABLE IF NOT EXISTS hyperedges (
    id SERIAL PRIMARY KEY,
    hyperedge_id VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    principle_ids TEXT[] NOT NULL,
    relationship_strength DECIMAL(3,2) CHECK (relationship_strength >= 0 AND relationship_strength <= 1),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for hyperedge lookups
CREATE INDEX idx_hyperedges_id ON hyperedges(hyperedge_id);

-- ============================================================================
-- CASE LAW TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS case_law (
    id SERIAL PRIMARY KEY,
    case_id VARCHAR(100) UNIQUE NOT NULL,
    case_name VARCHAR(500) NOT NULL,
    citation VARCHAR(255),
    jurisdiction VARCHAR(100),
    year INTEGER,
    court VARCHAR(255),
    principles_applied TEXT[],
    summary TEXT,
    url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for case law queries
CREATE INDEX idx_case_law_id ON case_law(case_id);
CREATE INDEX idx_case_law_jurisdiction ON case_law(jurisdiction);
CREATE INDEX idx_case_law_year ON case_law(year DESC);

-- ============================================================================
-- SIMULATION RESULTS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS simulation_results (
    id SERIAL PRIMARY KEY,
    simulation_id VARCHAR(100) UNIQUE NOT NULL,
    model_type VARCHAR(50) NOT NULL,
    scenario VARCHAR(50) NOT NULL,
    framework_version VARCHAR(10) NOT NULL,
    parameters JSONB,
    results JSONB,
    metrics JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for simulation queries
CREATE INDEX idx_simulation_id ON simulation_results(simulation_id);
CREATE INDEX idx_simulation_model ON simulation_results(model_type);
CREATE INDEX idx_simulation_scenario ON simulation_results(scenario);
CREATE INDEX idx_simulation_timestamp ON simulation_results(timestamp DESC);

-- ============================================================================
-- VIEWS FOR COMMON QUERIES
-- ============================================================================

-- View: High influence meta-principles
CREATE OR REPLACE VIEW high_influence_meta_principles AS
SELECT principle_id, name, influence_score, contemporary_relevance
FROM meta_principles
WHERE influence_score >= 0.85
ORDER BY influence_score DESC;

-- View: Recent case law (2024-2025)
CREATE OR REPLACE VIEW recent_case_law AS
SELECT case_id, case_name, citation, jurisdiction, year, principles_applied
FROM case_law
WHERE year >= 2024
ORDER BY year DESC, case_name;

-- View: Principle network (all relationships)
CREATE OR REPLACE VIEW principle_network AS
SELECT 
    pr.relationship_type,
    pr.source_principle_id,
    mp1.name AS source_name,
    pr.target_principle_id,
    mp2.name AS target_name,
    pr.relationship_strength
FROM principle_relationships pr
LEFT JOIN meta_principles mp1 ON pr.source_principle_id = mp1.principle_id
LEFT JOIN meta_principles mp2 ON pr.target_principle_id = mp2.principle_id
UNION ALL
SELECT 
    pr.relationship_type,
    pr.source_principle_id,
    fp1.name AS source_name,
    pr.target_principle_id,
    fp2.name AS target_name,
    pr.relationship_strength
FROM principle_relationships pr
LEFT JOIN first_order_principles fp1 ON pr.source_principle_id = fp1.principle_id
LEFT JOIN first_order_principles fp2 ON pr.target_principle_id = fp2.principle_id;

-- ============================================================================
-- FUNCTIONS FOR DATA INTEGRITY
-- ============================================================================

-- Function: Update timestamp on row modification
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers for automatic timestamp updates
CREATE TRIGGER update_meta_principles_updated_at
    BEFORE UPDATE ON meta_principles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_first_order_principles_updated_at
    BEFORE UPDATE ON first_order_principles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- COMMENTS FOR DOCUMENTATION
-- ============================================================================

COMMENT ON TABLE meta_principles IS 'Level 2 jurisprudential theories (v2.3 - 25 theories)';
COMMENT ON TABLE first_order_principles IS 'Level 1 fundamental legal maxims (v2.3 - 70 principles)';
COMMENT ON TABLE principle_relationships IS 'Binary relationships between principles';
COMMENT ON TABLE hyperedges IS 'Multi-way relationships between principles';
COMMENT ON TABLE case_law IS 'Case law database with principle applications';
COMMENT ON TABLE simulation_results IS 'Results from multi-model simulations';

COMMENT ON COLUMN meta_principles.influence_score IS 'Quantitative influence metric (0-1)';
COMMENT ON COLUMN first_order_principles.conflict_priority IS 'Priority in principle conflicts (higher = higher priority)';
COMMENT ON COLUMN principle_relationships.relationship_strength IS 'Strength of relationship (0-1)';
