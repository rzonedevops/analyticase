-- ===================================================================
-- Lex Scheme Enhanced Database Schema - Version 2.0
-- Legal Framework Management for AnalytiCase
-- Supports hypergraph-based legal entity relationships
-- ===================================================================

-- ===================================================================
-- CORE LEGAL ENTITIES
-- ===================================================================

-- Legal Nodes Table (Base table for all legal entities)
CREATE TABLE IF NOT EXISTS lex_nodes (
    node_id VARCHAR(200) PRIMARY KEY,
    node_type VARCHAR(50) NOT NULL,
    name VARCHAR(500) NOT NULL,
    content TEXT,
    jurisdiction VARCHAR(10) DEFAULT 'za',
    status VARCHAR(50) DEFAULT 'active',
    version INTEGER DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb,
    properties JSONB DEFAULT '{}'::jsonb,
    embedding FLOAT8[],
    CONSTRAINT valid_node_type CHECK (node_type IN (
        'statute', 'section', 'subsection', 'case', 'precedent', 
        'principle', 'concept', 'party', 'court', 'judge', 'attorney',
        'regulation', 'amendment', 'interpretation'
    ))
);

CREATE INDEX IF NOT EXISTS idx_lex_nodes_type ON lex_nodes(node_type);
CREATE INDEX IF NOT EXISTS idx_lex_nodes_jurisdiction ON lex_nodes(jurisdiction);
CREATE INDEX IF NOT EXISTS idx_lex_nodes_status ON lex_nodes(status);
CREATE INDEX IF NOT EXISTS idx_lex_nodes_name ON lex_nodes USING gin(to_tsvector('english', name));
CREATE INDEX IF NOT EXISTS idx_lex_nodes_content ON lex_nodes USING gin(to_tsvector('english', content));
CREATE INDEX IF NOT EXISTS idx_lex_nodes_metadata ON lex_nodes USING gin(metadata);

-- Statutes Table (Specialized table for statutes)
CREATE TABLE IF NOT EXISTS lex_statutes (
    statute_id VARCHAR(200) PRIMARY KEY REFERENCES lex_nodes(node_id) ON DELETE CASCADE,
    statute_number VARCHAR(100),
    short_title VARCHAR(500),
    long_title TEXT,
    enactment_date DATE,
    effective_date DATE,
    repeal_date DATE,
    parent_statute_id VARCHAR(200) REFERENCES lex_statutes(statute_id),
    gazette_reference VARCHAR(200),
    assent_date DATE,
    commencement_date DATE,
    is_principal BOOLEAN DEFAULT true,
    amendment_count INTEGER DEFAULT 0,
    section_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_lex_statutes_number ON lex_statutes(statute_number);
CREATE INDEX IF NOT EXISTS idx_lex_statutes_effective_date ON lex_statutes(effective_date);
CREATE INDEX IF NOT EXISTS idx_lex_statutes_parent ON lex_statutes(parent_statute_id);

-- Sections Table (Sections within statutes)
CREATE TABLE IF NOT EXISTS lex_sections (
    section_id VARCHAR(200) PRIMARY KEY REFERENCES lex_nodes(node_id) ON DELETE CASCADE,
    statute_id VARCHAR(200) NOT NULL REFERENCES lex_statutes(statute_id) ON DELETE CASCADE,
    section_number VARCHAR(50) NOT NULL,
    section_title VARCHAR(500),
    section_content TEXT NOT NULL,
    parent_section_id VARCHAR(200) REFERENCES lex_sections(section_id),
    level INTEGER DEFAULT 1,
    ordinal_position INTEGER,
    is_repealed BOOLEAN DEFAULT false,
    repeal_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_lex_sections_statute ON lex_sections(statute_id);
CREATE INDEX IF NOT EXISTS idx_lex_sections_number ON lex_sections(section_number);
CREATE INDEX IF NOT EXISTS idx_lex_sections_parent ON lex_sections(parent_section_id);
CREATE INDEX IF NOT EXISTS idx_lex_sections_content ON lex_sections USING gin(to_tsvector('english', section_content));

-- Cases Table (Legal cases and precedents)
CREATE TABLE IF NOT EXISTS lex_cases (
    case_id VARCHAR(200) PRIMARY KEY REFERENCES lex_nodes(node_id) ON DELETE CASCADE,
    case_number VARCHAR(200) NOT NULL,
    case_name VARCHAR(500) NOT NULL,
    citation VARCHAR(200),
    court_id VARCHAR(200),
    judge_id VARCHAR(200),
    case_date DATE,
    decision_date DATE,
    case_type VARCHAR(100),
    case_status VARCHAR(50) DEFAULT 'pending',
    outcome VARCHAR(100),
    summary TEXT,
    facts TEXT,
    legal_issues TEXT,
    holding TEXT,
    reasoning TEXT,
    is_precedent BOOLEAN DEFAULT false,
    precedent_weight DECIMAL(3, 2) DEFAULT 0.5,
    citation_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_case_status CHECK (case_status IN (
        'pending', 'active', 'decided', 'appealed', 'closed', 'archived'
    ))
);

CREATE INDEX IF NOT EXISTS idx_lex_cases_number ON lex_cases(case_number);
CREATE INDEX IF NOT EXISTS idx_lex_cases_court ON lex_cases(court_id);
CREATE INDEX IF NOT EXISTS idx_lex_cases_judge ON lex_cases(judge_id);
CREATE INDEX IF NOT EXISTS idx_lex_cases_date ON lex_cases(case_date);
CREATE INDEX IF NOT EXISTS idx_lex_cases_status ON lex_cases(case_status);
CREATE INDEX IF NOT EXISTS idx_lex_cases_precedent ON lex_cases(is_precedent);
CREATE INDEX IF NOT EXISTS idx_lex_cases_name ON lex_cases USING gin(to_tsvector('english', case_name));

-- Parties Table (Parties involved in cases)
CREATE TABLE IF NOT EXISTS lex_parties (
    party_id VARCHAR(200) PRIMARY KEY REFERENCES lex_nodes(node_id) ON DELETE CASCADE,
    party_name VARCHAR(500) NOT NULL,
    party_type VARCHAR(50) NOT NULL,
    entity_type VARCHAR(50),
    contact_info JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_party_type CHECK (party_type IN (
        'plaintiff', 'defendant', 'appellant', 'respondent', 
        'petitioner', 'third_party', 'intervenor'
    ))
);

CREATE INDEX IF NOT EXISTS idx_lex_parties_type ON lex_parties(party_type);
CREATE INDEX IF NOT EXISTS idx_lex_parties_name ON lex_parties USING gin(to_tsvector('english', party_name));

-- Courts Table (Court information)
CREATE TABLE IF NOT EXISTS lex_courts (
    court_id VARCHAR(200) PRIMARY KEY REFERENCES lex_nodes(node_id) ON DELETE CASCADE,
    court_name VARCHAR(500) NOT NULL,
    court_level VARCHAR(50) NOT NULL,
    jurisdiction VARCHAR(100),
    location VARCHAR(200),
    parent_court_id VARCHAR(200) REFERENCES lex_courts(court_id),
    established_date DATE,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_court_level CHECK (court_level IN (
        'constitutional', 'supreme', 'appeal', 'high', 'magistrate', 
        'district', 'specialized', 'tribunal'
    ))
);

CREATE INDEX IF NOT EXISTS idx_lex_courts_level ON lex_courts(court_level);
CREATE INDEX IF NOT EXISTS idx_lex_courts_jurisdiction ON lex_courts(jurisdiction);
CREATE INDEX IF NOT EXISTS idx_lex_courts_parent ON lex_courts(parent_court_id);

-- Judges Table (Judge information)
CREATE TABLE IF NOT EXISTS lex_judges (
    judge_id VARCHAR(200) PRIMARY KEY REFERENCES lex_nodes(node_id) ON DELETE CASCADE,
    judge_name VARCHAR(500) NOT NULL,
    title VARCHAR(100),
    court_id VARCHAR(200) REFERENCES lex_courts(court_id),
    appointment_date DATE,
    retirement_date DATE,
    is_active BOOLEAN DEFAULT true,
    specializations TEXT[],
    cases_presided INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_lex_judges_court ON lex_judges(court_id);
CREATE INDEX IF NOT EXISTS idx_lex_judges_active ON lex_judges(is_active);
CREATE INDEX IF NOT EXISTS idx_lex_judges_name ON lex_judges USING gin(to_tsvector('english', judge_name));

-- ===================================================================
-- RELATIONSHIPS AND HYPEREDGES
-- ===================================================================

-- Legal Hyperedges Table (Multi-way relationships between legal entities)
CREATE TABLE IF NOT EXISTS lex_hyperedges (
    edge_id VARCHAR(200) PRIMARY KEY,
    relation_type VARCHAR(100) NOT NULL,
    node_ids TEXT[] NOT NULL,
    weight DECIMAL(5, 4) DEFAULT 1.0,
    confidence DECIMAL(5, 4) DEFAULT 1.0,
    source VARCHAR(200),
    effective_date DATE,
    expiry_date DATE,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb,
    properties JSONB DEFAULT '{}'::jsonb,
    CONSTRAINT valid_relation_type CHECK (relation_type IN (
        'cites', 'interprets', 'overrules', 'follows', 'distinguishes',
        'amends', 'repeals', 'applies_to', 'conflicts_with', 'supports',
        'depends_on', 'supersedes', 'consolidates', 'references'
    ))
);

CREATE INDEX IF NOT EXISTS idx_lex_hyperedges_type ON lex_hyperedges(relation_type);
CREATE INDEX IF NOT EXISTS idx_lex_hyperedges_active ON lex_hyperedges(is_active);
CREATE INDEX IF NOT EXISTS idx_lex_hyperedges_nodes ON lex_hyperedges USING gin(node_ids);
CREATE INDEX IF NOT EXISTS idx_lex_hyperedges_metadata ON lex_hyperedges USING gin(metadata);

-- Case-Party Relationships
CREATE TABLE IF NOT EXISTS lex_case_parties (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id VARCHAR(200) NOT NULL REFERENCES lex_cases(case_id) ON DELETE CASCADE,
    party_id VARCHAR(200) NOT NULL REFERENCES lex_parties(party_id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL,
    attorney_id VARCHAR(200),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(case_id, party_id, role)
);

CREATE INDEX IF NOT EXISTS idx_lex_case_parties_case ON lex_case_parties(case_id);
CREATE INDEX IF NOT EXISTS idx_lex_case_parties_party ON lex_case_parties(party_id);

-- Case Citations (Cases citing other cases or statutes)
CREATE TABLE IF NOT EXISTS lex_citations (
    citation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    citing_case_id VARCHAR(200) NOT NULL REFERENCES lex_cases(case_id) ON DELETE CASCADE,
    cited_node_id VARCHAR(200) NOT NULL REFERENCES lex_nodes(node_id) ON DELETE CASCADE,
    citation_type VARCHAR(50) NOT NULL,
    citation_context TEXT,
    page_number VARCHAR(50),
    paragraph_number VARCHAR(50),
    weight DECIMAL(3, 2) DEFAULT 0.5,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_citation_type CHECK (citation_type IN (
        'direct', 'indirect', 'distinguishing', 'supporting', 
        'critical', 'explanatory', 'comparative'
    ))
);

CREATE INDEX IF NOT EXISTS idx_lex_citations_citing ON lex_citations(citing_case_id);
CREATE INDEX IF NOT EXISTS idx_lex_citations_cited ON lex_citations(cited_node_id);
CREATE INDEX IF NOT EXISTS idx_lex_citations_type ON lex_citations(citation_type);

-- ===================================================================
-- LEGAL CONCEPTS AND PRINCIPLES
-- ===================================================================

-- Legal Principles Table
CREATE TABLE IF NOT EXISTS lex_principles (
    principle_id VARCHAR(200) PRIMARY KEY REFERENCES lex_nodes(node_id) ON DELETE CASCADE,
    principle_name VARCHAR(500) NOT NULL,
    principle_description TEXT,
    category VARCHAR(100),
    source_type VARCHAR(50),
    authority_level DECIMAL(3, 2) DEFAULT 0.5,
    application_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_lex_principles_category ON lex_principles(category);
CREATE INDEX IF NOT EXISTS idx_lex_principles_name ON lex_principles USING gin(to_tsvector('english', principle_name));

-- Legal Concepts Table
CREATE TABLE IF NOT EXISTS lex_concepts (
    concept_id VARCHAR(200) PRIMARY KEY REFERENCES lex_nodes(node_id) ON DELETE CASCADE,
    concept_name VARCHAR(500) NOT NULL,
    concept_definition TEXT,
    domain VARCHAR(100),
    related_concepts TEXT[],
    usage_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_lex_concepts_domain ON lex_concepts(domain);
CREATE INDEX IF NOT EXISTS idx_lex_concepts_name ON lex_concepts USING gin(to_tsvector('english', concept_name));

-- ===================================================================
-- INTEGRATION WITH ANALYTICASE MODELS
-- ===================================================================

-- Lex-AD Integration Mappings (Links legal entities to simulation agents/events)
CREATE TABLE IF NOT EXISTS lex_ad_mappings (
    mapping_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lex_node_id VARCHAR(200) NOT NULL REFERENCES lex_nodes(node_id) ON DELETE CASCADE,
    ad_entity_type VARCHAR(50) NOT NULL,
    ad_entity_id VARCHAR(200) NOT NULL,
    mapping_type VARCHAR(50) NOT NULL,
    confidence DECIMAL(5, 4) DEFAULT 1.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb,
    CONSTRAINT valid_ad_entity_type CHECK (ad_entity_type IN (
        'agent', 'event', 'stock', 'flow', 'hypergraph_node', 'hypergraph_edge'
    )),
    CONSTRAINT valid_mapping_type CHECK (mapping_type IN (
        'agent_to_legal_entity', 'event_to_legal_procedure', 
        'stock_to_legal_stage', 'case_to_simulation'
    ))
);

CREATE INDEX IF NOT EXISTS idx_lex_ad_mappings_lex ON lex_ad_mappings(lex_node_id);
CREATE INDEX IF NOT EXISTS idx_lex_ad_mappings_ad ON lex_ad_mappings(ad_entity_id);
CREATE INDEX IF NOT EXISTS idx_lex_ad_mappings_type ON lex_ad_mappings(mapping_type);

-- Legal Procedures Table (Maps to discrete events)
CREATE TABLE IF NOT EXISTS lex_procedures (
    procedure_id VARCHAR(200) PRIMARY KEY,
    procedure_name VARCHAR(500) NOT NULL,
    procedure_type VARCHAR(100) NOT NULL,
    description TEXT,
    required_steps TEXT[],
    typical_duration_days INTEGER,
    statute_references TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_procedure_type CHECK (procedure_type IN (
        'filing', 'discovery', 'hearing', 'trial', 'judgment', 
        'appeal', 'enforcement', 'settlement'
    ))
);

CREATE INDEX IF NOT EXISTS idx_lex_procedures_type ON lex_procedures(procedure_type);
CREATE INDEX IF NOT EXISTS idx_lex_procedures_name ON lex_procedures USING gin(to_tsvector('english', procedure_name));

-- Legal Stages Table (Maps to system dynamics stocks)
CREATE TABLE IF NOT EXISTS lex_stages (
    stage_id VARCHAR(200) PRIMARY KEY,
    stage_name VARCHAR(500) NOT NULL,
    stage_order INTEGER NOT NULL,
    description TEXT,
    entry_conditions TEXT[],
    exit_conditions TEXT[],
    typical_duration_days INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_lex_stages_order ON lex_stages(stage_order);

-- ===================================================================
-- ANALYTICS AND TRACKING
-- ===================================================================

-- Legal Analytics Table (Tracks usage and patterns)
CREATE TABLE IF NOT EXISTS lex_analytics (
    analytics_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    node_id VARCHAR(200) REFERENCES lex_nodes(node_id) ON DELETE CASCADE,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(15, 4),
    measurement_date DATE DEFAULT CURRENT_DATE,
    context JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_lex_analytics_node ON lex_analytics(node_id);
CREATE INDEX IF NOT EXISTS idx_lex_analytics_metric ON lex_analytics(metric_name);
CREATE INDEX IF NOT EXISTS idx_lex_analytics_date ON lex_analytics(measurement_date);

-- Legal Query History (Tracks HypergraphQL queries)
CREATE TABLE IF NOT EXISTS lex_query_history (
    query_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    query_text TEXT NOT NULL,
    query_type VARCHAR(50),
    execution_time_ms INTEGER,
    result_count INTEGER,
    user_id VARCHAR(200),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_lex_query_history_type ON lex_query_history(query_type);
CREATE INDEX IF NOT EXISTS idx_lex_query_history_user ON lex_query_history(user_id);
CREATE INDEX IF NOT EXISTS idx_lex_query_history_created ON lex_query_history(created_at);

-- ===================================================================
-- VERSIONING AND AUDIT
-- ===================================================================

-- Legal Node History (Tracks changes to legal entities)
CREATE TABLE IF NOT EXISTS lex_node_history (
    history_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    node_id VARCHAR(200) NOT NULL,
    version INTEGER NOT NULL,
    change_type VARCHAR(50) NOT NULL,
    changed_by VARCHAR(200),
    change_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    previous_data JSONB,
    new_data JSONB,
    change_reason TEXT,
    CONSTRAINT valid_change_type CHECK (change_type IN (
        'created', 'updated', 'deleted', 'amended', 'repealed', 'restored'
    ))
);

CREATE INDEX IF NOT EXISTS idx_lex_node_history_node ON lex_node_history(node_id);
CREATE INDEX IF NOT EXISTS idx_lex_node_history_version ON lex_node_history(version);
CREATE INDEX IF NOT EXISTS idx_lex_node_history_date ON lex_node_history(change_date);

-- ===================================================================
-- VIEWS FOR COMMON QUERIES
-- ===================================================================

-- Active Statutes View
CREATE OR REPLACE VIEW lex_active_statutes AS
SELECT 
    s.statute_id,
    n.name,
    s.statute_number,
    s.short_title,
    s.enactment_date,
    s.effective_date,
    s.section_count,
    s.amendment_count,
    n.jurisdiction
FROM lex_statutes s
JOIN lex_nodes n ON s.statute_id = n.node_id
WHERE s.repeal_date IS NULL
  AND n.status = 'active';

-- Precedent Cases View
CREATE OR REPLACE VIEW lex_precedent_cases AS
SELECT 
    c.case_id,
    c.case_number,
    c.case_name,
    c.citation,
    c.decision_date,
    c.outcome,
    c.precedent_weight,
    c.citation_count,
    co.court_name,
    j.judge_name,
    n.jurisdiction
FROM lex_cases c
JOIN lex_nodes n ON c.case_id = n.node_id
LEFT JOIN lex_courts co ON c.court_id = co.court_id
LEFT JOIN lex_judges j ON c.judge_id = j.judge_id
WHERE c.is_precedent = true
  AND n.status = 'active'
ORDER BY c.precedent_weight DESC, c.citation_count DESC;

-- Case Citation Network View
CREATE OR REPLACE VIEW lex_citation_network AS
SELECT 
    cit.citation_id,
    citing.case_name AS citing_case,
    citing.case_number AS citing_number,
    cited.name AS cited_entity,
    cited.node_type AS cited_type,
    cit.citation_type,
    cit.weight
FROM lex_citations cit
JOIN lex_cases citing ON cit.citing_case_id = citing.case_id
JOIN lex_nodes cited ON cit.cited_node_id = cited.node_id;

-- ===================================================================
-- FUNCTIONS AND TRIGGERS
-- ===================================================================

-- Function to update citation count
CREATE OR REPLACE FUNCTION update_citation_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE lex_cases
        SET citation_count = citation_count + 1
        WHERE case_id = (
            SELECT case_id FROM lex_cases WHERE case_id = NEW.cited_node_id
        );
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE lex_cases
        SET citation_count = GREATEST(citation_count - 1, 0)
        WHERE case_id = (
            SELECT case_id FROM lex_cases WHERE case_id = OLD.cited_node_id
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for citation count
CREATE TRIGGER trigger_update_citation_count
AFTER INSERT OR DELETE ON lex_citations
FOR EACH ROW
EXECUTE FUNCTION update_citation_count();

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply updated_at trigger to all relevant tables
CREATE TRIGGER trigger_lex_nodes_updated_at
BEFORE UPDATE ON lex_nodes
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trigger_lex_statutes_updated_at
BEFORE UPDATE ON lex_statutes
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trigger_lex_cases_updated_at
BEFORE UPDATE ON lex_cases
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- ===================================================================
-- COMMENTS AND DOCUMENTATION
-- ===================================================================

COMMENT ON TABLE lex_nodes IS 'Base table for all legal entities in the hypergraph';
COMMENT ON TABLE lex_statutes IS 'Statutes and legislation with versioning support';
COMMENT ON TABLE lex_sections IS 'Sections and subsections within statutes';
COMMENT ON TABLE lex_cases IS 'Legal cases with precedent tracking and analytics';
COMMENT ON TABLE lex_parties IS 'Parties involved in legal cases';
COMMENT ON TABLE lex_courts IS 'Court hierarchy and jurisdiction information';
COMMENT ON TABLE lex_judges IS 'Judge information and case assignments';
COMMENT ON TABLE lex_hyperedges IS 'Multi-way relationships between legal entities';
COMMENT ON TABLE lex_citations IS 'Citation relationships between cases and statutes';
COMMENT ON TABLE lex_principles IS 'Legal principles and doctrines';
COMMENT ON TABLE lex_concepts IS 'Legal concepts and definitions';
COMMENT ON TABLE lex_ad_mappings IS 'Integration mappings to AnalytiCase simulation models';
COMMENT ON TABLE lex_procedures IS 'Legal procedures mapped to discrete events';
COMMENT ON TABLE lex_stages IS 'Legal case stages mapped to system dynamics';
COMMENT ON TABLE lex_analytics IS 'Analytics and metrics for legal entities';
COMMENT ON TABLE lex_query_history IS 'HypergraphQL query execution history';
COMMENT ON TABLE lex_node_history IS 'Audit trail for legal entity changes';

-- ===================================================================
-- SAMPLE DATA INSERTION
-- ===================================================================

-- Insert sample court
INSERT INTO lex_nodes (node_id, node_type, name, jurisdiction, metadata)
VALUES ('court_constitutional_za', 'court', 'Constitutional Court of South Africa', 'za', '{"level": "constitutional"}'::jsonb)
ON CONFLICT DO NOTHING;

INSERT INTO lex_courts (court_id, court_name, court_level, jurisdiction, established_date)
VALUES ('court_constitutional_za', 'Constitutional Court of South Africa', 'constitutional', 'National', '1995-02-14')
ON CONFLICT DO NOTHING;

-- Insert sample legal procedures
INSERT INTO lex_procedures (procedure_id, procedure_name, procedure_type, typical_duration_days)
VALUES 
    ('proc_filing', 'Case Filing Procedure', 'filing', 1),
    ('proc_discovery', 'Discovery Procedure', 'discovery', 30),
    ('proc_hearing', 'Hearing Procedure', 'hearing', 1),
    ('proc_trial', 'Trial Procedure', 'trial', 5),
    ('proc_judgment', 'Judgment Procedure', 'judgment', 14),
    ('proc_appeal', 'Appeal Procedure', 'appeal', 60)
ON CONFLICT DO NOTHING;

-- Insert sample legal stages
INSERT INTO lex_stages (stage_id, stage_name, stage_order, typical_duration_days)
VALUES 
    ('stage_filing', 'Filing Stage', 1, 7),
    ('stage_discovery', 'Discovery Stage', 2, 30),
    ('stage_pretrial', 'Pre-Trial Stage', 3, 14),
    ('stage_trial', 'Trial Stage', 4, 5),
    ('stage_ruling', 'Ruling Stage', 5, 14),
    ('stage_closure', 'Closure Stage', 6, 7)
ON CONFLICT DO NOTHING;

